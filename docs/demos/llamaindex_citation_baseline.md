# LlamaIndex citation baseline

LlamaIndex already provides a nice [tutorial](https://developers.llamaindex.ai/python/examples/workflow/citation_query_engine/) on a basic citation-based RAG system, so we wrote a [script](../../scripts/demos/llamaindex_citation_baseline.py) to demonstrate this.

Command line usage (make sure you're in the repo home directory `ResearchRAG/` and you have the virtual environment enabled):
> python3 scripts/demos/llamaindex_citation_baseline.py --pdf_dir data/llamaindex_citation_baseline_pdfs --question "What is this paper about?" --model llama3:8b

Parameters:
- pdf_dir: The location of the pdf. Here, kept separate from the project's main reference corpus
- question: The prompt to give the RAG system
- model: The model to use, assumed to be installed via Ollama:
  - > ollama run [model-name]

Baseline configuration:
- Embedding: BAAI/bge-small-en
- Chunk size: 512
- Chunk overlap: 20
- Top-k chunk retrieval: 8
- No reranking
- No metadata filtering
- No citation validation
- No structured section parsing

The moral of this demo is that LlamaIndex contains a quick, minimal citation-based RAG workflow, but with these parameters it can generally miss the mark for response quality with unclear and possibly duplicate citations.
