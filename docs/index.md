# RAGFRA: RAG Functional data analysis Research Assistant

Authors:
1. Nicholas Gaubatz*
2. Mark Carpenter*

*Department of Mathematics & Statistics, Auburn University

## Overview

This project develops a **retrieval-augmented generation (RAG)** assistant designed to assist with:
- Mathematical research (theorem and proof lookups)
- Technical document summarization
- Citation-grounded question answering over FDA-specific copora

The aim is the build a system that is:
- **Citation-first and fail-closed**
  - always provide citations and explicitly fail if no such citation exists
- **Reproducible**
  - this repository aims to lay out fully reproducible steps for building such an assistant
- **Auditable**
  - the assistant's performance is evaluated rigorously on technical FDA questions
- **Transferable**
  - ideally, the assistant template will be able to adapt to whatever corpus is provided

This repository documents the full development process, including design decisions, experiments, and evaluation methodology.

## Problem statement

Large language models (LLMs) such as ChatGPT are great for answering questions about technical domains such as FDA, but they tend to hallucinate answers and citations in such domains, especially when prompts contain very advanced topics. This is detrimental to research workflows, which typically require
- Precise citations
- Cross-document comparisons
- Reproducibility of claims

This project explores whether a carefully engineered RAG pipeline can provide
1. Reliable citation-grounded answers involving technical concepts
2. Reduced hallucination in high-stakes contexts
3. Identification of theorems across differing notations, a common occurrence in the FDA field

---

## High-level architecture

Core components:

1. **Document ingestion pipeline** (.pdf or .tex to text)
2. **Chunking strategy** (math/theorem-aware)
3. **Embedding model** (chunk to vector)
4. **Vector storage**
5. **Retriever** (Retrieval)
6. **Citation-first generation policy** (Augmentation and Generation)
7. **Evaluation framework**

In particular, this architecture is designed around the Separation of Concerns philosophy, e.g. if a particular model is performing poorly, the user can switch it out quickly and easily.

See:

- `docs/manual/architecture/` for component details
- `docs/manual/design/` for design decisions
- `docs/decisions/` for architecture decision records (ADRs)

---

## Design Principles

- **Fail-closed:** If evidence is insufficient, the system notifies.
- **Citation-first:** Every single claim must be traceable.
- **Reproducible experiments:** All evaluation runs are configuration-driven.
- **Separation of retrieval and reasoning:** Each part of RAG is treated independently.
- **Minimal black-boxing:** All steps and choices are inspectible.

---

## Evaluation Plan

The system is evaluated using
- Retrieval quality metrics
- Citation accuracy metrics
- Human judgement for faithfulness
- Latency benchmarks

Ablation studies are performed on
- Chunk size
- Embedding model
- Retrieval strategy
- Prompt policy

See `docs/manual/design/evaluation.md` for the full protocol.

---

## Repository Structure

```
.
├── docs
│   ├── decisions
│   ├── experiments
│   ├── index.md
│   ├── manual
│   │   ├── api
│   │   ├── architecture
│   │   ├── design
│   │   ├── experiments
│   │   └── how-to
│   ├── notes
│   ├── paper
│   └── results
├── LICENSE
├── Makefile
├── notebooks
├── pyproject.toml
├── README.md
├── scripts
├── src
├── tests
```

---

## Current status

- [ ] Ingestion pipeline
- [ ] Chunking experiments
- [ ] Embedding evaluation
- [ ] Retrieval benchmarking
- [ ] Citation enforcement
- [ ] Human evaluation
- [ ] Paper draft

---

## Reproducibility

To reproduce results:

```bash
git clone https://github.com/nicholasgaubatz/ResearchRAG.git
cd ResearchRAG
make setup
make ingest
make evaluate
```

Full instructions are available in `docs/manual/how-to/reproduce`
