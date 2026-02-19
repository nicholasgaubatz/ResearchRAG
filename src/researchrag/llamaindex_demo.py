# See docs/demos/llamaindex_citation_baseline.md

import argparse
from dataclasses import dataclass

from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.prompts import PromptTemplate
from llama_index.core.response_synthesizers import (
    ResponseMode,
    get_response_synthesizer,
)
from llama_index.core.schema import (
    MetadataMode,
    NodeWithScore,
    TextNode,
)
from llama_index.core.workflow import (
    Context,
    Event,
    StartEvent,
    StopEvent,
    Workflow,
    step,
)
from llama_index.llms.ollama import Ollama


class RetrieverEvent(Event):
    """Result of running retrieval"""

    nodes: list[NodeWithScore]


class CreateCitationsEvent(Event):
    """Add citations to the nodes."""

    nodes: list[NodeWithScore]


@dataclass
class CitationConfig:
    qa_template: PromptTemplate
    refine_template: PromptTemplate
    chunk_size: int = 512
    chunk_overlap: int = 20
    top_k: int = 8


class CitationQueryEngineWorkflow(Workflow):
    def __init__(self, llm: Ollama, config: CitationConfig, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.llm = llm
        self.config = config

    @step
    async def retrieve(self, ctx: Context, ev: StartEvent) -> RetrieverEvent | None:
        "Entry point for RAG, triggered by a StartEvent with `query`."
        query = ev.get("query")
        if not query:
            return None

        print(f"Query the database with: {query}")

        # store the query in the global context
        await ctx.store.set("query", query)

        if ev.index is None:
            print("Index is empty, load some documents before querying!")
            return None

        retriever = ev.index.as_retriever(similarity_top_k=self.config.top_k)
        nodes = retriever.retrieve(query)
        print(f"Retrieved {len(nodes)} nodes.")
        return RetrieverEvent(nodes=nodes)

    @step
    async def create_citation_nodes(self, ev: RetrieverEvent) -> CreateCitationsEvent:
        """
        Modify retrieved nodes to create granular sources for citations.

        Takes a list of NodeWithScore objects and splits their content
        into smaller chunks, creating new NodeWithScore objects for each chunk.
        Each new node is labeled as a numbered source, allowing for more precise
        citation in query results.

        Args:
            nodes (List[NodeWithScore]): A list of NodeWithScore objects to be processed.

        Returns:
            List[NodeWithScore]: A new list of NodeWithScore objects, where each object
            represents a smaller chunk of the original nodes, labeled as a source.
        """
        nodes = ev.nodes

        new_nodes: list[NodeWithScore] = []

        text_splitter = SentenceSplitter(
            chunk_size=self.config.chunk_size,
            chunk_overlap=self.config.chunk_overlap,
        )

        for node in nodes:
            text_chunks = text_splitter.split_text(
                node.node.get_content(metadata_mode=MetadataMode.NONE)
            )

            for chunk_idx, text_chunk in enumerate(text_chunks):
                text = f"Source {len(new_nodes) + 1}:\n{text_chunk}\n"

                new_node = NodeWithScore(
                    node=TextNode(
                        text=text,
                        id_=f"{node.node.node_id}_chunk_{chunk_idx}",
                        metadata=node.node.metadata,
                    ),
                    score=node.score,
                )

                new_nodes.append(new_node)

        return CreateCitationsEvent(nodes=new_nodes)

    @step
    async def synthesize(self, ctx: Context, ev: CreateCitationsEvent) -> StopEvent:
        """Return a streaming response using the retrieved nodes."""
        query = await ctx.store.get("query", default=None)

        synthesizer = get_response_synthesizer(
            llm=self.llm,
            text_qa_template=self.config.qa_template,
            refine_template=self.config.refine_template,
            response_mode=ResponseMode.COMPACT,
            use_async=True,
        )

        response = await synthesizer.asynthesize(query, nodes=ev.nodes)
        return StopEvent(result=response)


def parse_args():
    parser = argparse.ArgumentParser(
        description="A simple LlamaIndex citation-based RAG demo from the docs"
    )

    parser.add_argument(
        "--pdf_dir",
        type=str,
        default="data/llamaindex_citation_baseline_pdfs",
        help="The location of the pdf to reference.",
    )
    parser.add_argument("--question", type=str, help="The prompt to give the RAG system")
    parser.add_argument(
        "--model",
        type=str,
        default="llama3:8b",
        help="The model to use, assumed to be installed via Ollama",
    )

    return parser.parse_args()
