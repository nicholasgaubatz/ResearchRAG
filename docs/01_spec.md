# RAGFRA: RAG Functional data analysis Research Assistant (v1)

February 17, 2026

Authors:
1. Nicholas Gaubatz*
2. Mark Carpenter*

*Department of Mathematics & Statistics, Auburn University

## Overview

This project develops a **retrieval-augmented generation (RAG)** assistant designed to assist with:
- Mathematical research (theorem and proof lookups)
- Technical document summarization
- Citation-grounded question answering over FDA-specific copora

See `docs/index.md` for a detailed overview.

## v1 Scope

Inputs
- Supported file types: born-digital pdfs
  - Not supported by v1: scanned pdfs, OCR, .tex
- Location: `data/raw_pdfs/`

Outputs
- Required: answer text + citations
- Required failure behavior: "If no good sources, then refuse + explain + suggest next step"

Citation policy
- See [citation_format.md](02_citation_format.md)

Retrieval assumptions
- Chunking strategy: TODO
- RAG framework: Llamaindex
- Embedding model name: *BGE-base* (power, unless this bottlenecks)
- Vector store name: *Chroma* (persistent storage, easy to use)
- Top-k retrieval default: $k=5$ (keep it small)

Non-goals
- No OCR, TeX parsing
- No table/figure parsing
- No LaTeX reconstruction from images
- No LaTeX rendering, but possible raw LaTeX output
- No cross-document symbolic math verification
- No web browsing
- No fancy UI; CLI only

Success criteria
- On eval set: $\geq 80\%$ questions answered with at least 2 citations
- Latency: $<30$ seconds for a typical query
- Refusal rate acceptable: $\leq 10\%$ hallucination response when sources missing

Known risks
- PDF text extraction quality
- Differing math notation and terminology between sources
- Long-context limitations
- Long textbooks mixed with short academic papers and notes
- TeX mixed with plain text
