# See docs/demos/llamaindex_citation_baseline.md

import asyncio
import logging

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.prompts import PromptTemplate
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

from researchrag.llamaindex_demo import (
    CitationConfig,
    CitationQueryEngineWorkflow,
    parse_args,
)

CITATION_QA_TEMPLATE = PromptTemplate(
    "Please provide an answer based solely on the provided sources. "
    "When referencing information from a source, "
    "cite the appropriate source(s) using their corresponding numbers. "
    "Every answer should include at least one source citation. "
    "Only cite a source when you are explicitly referencing it. "
    "If none of the sources are helpful, you should indicate that. "
    "For example:\n"
    "Source 1:\n"
    "The sky is red in the evening and blue in the morning.\n"
    "Source 2:\n"
    "Water is wet when the sky is red.\n"
    "Query: When is water wet?\n"
    "Answer: Water will be wet when the sky is red [2], "
    "which occurs in the evening [1].\n"
    "Now it's your turn. Below are several numbered sources of information:"
    "\n------\n"
    "{context_str}"
    "\n------\n"
    "Query: {query_str}\n"
    "Answer: "
)

CITATION_REFINE_TEMPLATE = PromptTemplate(
    "Please provide an answer based solely on the provided sources. "
    "When referencing information from a source, "
    "cite the appropriate source(s) using their corresponding numbers. "
    "Every answer should include at least one source citation. "
    "Only cite a source when you are explicitly referencing it. "
    "If none of the sources are helpful, you should indicate that. "
    "For example:\n"
    "Source 1:\n"
    "The sky is red in the evening and blue in the morning.\n"
    "Source 2:\n"
    "Water is wet when the sky is red.\n"
    "Query: When is water wet?\n"
    "Answer: Water will be wet when the sky is red [2], "
    "which occurs in the evening [1].\n"
    "Now it's your turn. "
    "We have provided an existing answer: {existing_answer}"
    "Below are several numbered sources of information. "
    "Use them to refine the existing answer. "
    "If the provided sources are not helpful, you will repeat the existing answer."
    "\nBegin refining!"
    "\n------\n"
    "{context_msg}"
    "\n------\n"
    "Query: {query_str}\n"
    "Answer: "
)

DEFAULT_CITATION_CHUNK_SIZE = 512
DEFAULT_CITATION_CHUNK_OVERLAP = 20
DEFAULT_TOP_K = 8

logging.basicConfig(level=logging.ERROR)

for name in [
    "llama_index",
    "sentence_transformers",
    "transformers",
    "huggingface_hub",
    "httpx",
    "urllib3",
]:
    logging.getLogger(name).setLevel(logging.ERROR)


async def main():
    args = parse_args()

    # Define model.
    llm = Ollama(
        model=args.model,
        request_timeout=30.0,
        verbose=False,
    )

    # Create an index.
    documents = SimpleDirectoryReader(args.pdf_dir).load_data()
    index = VectorStoreIndex.from_documents(
        documents=documents,
        embed_model=HuggingFaceEmbedding(model_name="BAAI/bge-small-en"),
    )

    # Run the workflow.
    citation_configs = CitationConfig(
        qa_template=CITATION_QA_TEMPLATE,
        refine_template=CITATION_REFINE_TEMPLATE,
        chunk_size=DEFAULT_CITATION_CHUNK_SIZE,
        chunk_overlap=DEFAULT_CITATION_CHUNK_OVERLAP,
        top_k=DEFAULT_TOP_K,
    )
    w = CitationQueryEngineWorkflow(llm=llm, config=citation_configs)
    result = await w.run(query=args.question, index=index)

    # Display the response.
    print("Response:")
    print("------------------")
    print(result)
    print()
    print("==================")
    print()

    # Display the first two citations.
    citation_1 = result.source_nodes[0]
    citation_2 = result.source_nodes[1]
    print(f"Citation 1 id: {citation_1.node.node_id}, score: {citation_1.score}")
    print(citation_1.node.get_text())
    print()
    print()
    print("==================")
    print()
    print(f"Citation 2 id: {citation_2.node.node_id}, score: {citation_2.score}")
    print(citation_2.node.get_text())
    print()
    print("==================")
    print()

    # Display all the citation ids.
    print(f"Citation ids: {[node.node.node_id for node in result.source_nodes]}")
    print()
    print("==================")
    print()

    # Display all the citation similarity scores.
    print(f"Citation similarity scores: {[node.score for node in result.source_nodes]}")
    print()
    print("==================")
    print()


if __name__ == "__main__":
    asyncio.run(main())
