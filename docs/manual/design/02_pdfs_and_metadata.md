TODO

Steps:
- Design what to store per chunk
- Chunk first pdf in `data/raw_pdfs/`

---

## Introduction

The goal of this section is to overview how document chunking parameters are chosen and implemented in this project. Here, we create
1. a minimal schema, or Python type that represents a chunk,
2. a sample artifact of one chunked PDF, and
3. a clear decision about what metadata we preserve forever.

## Part 1: `src/schema.py`

This file defines how we store metadata for documents and chunks within documents. Recall that we have a directory of documents as our starting point, but we need a way for our tools to realistically interact with each document. The way to do this is by chunking each document: each chunk is a group of text with around the same number of tokens or characters, and each chunk overlaps a bit so we don't abruptly cut off and miss context.

The Document and Chunk dataclasses are relatively straightforward, the only nontrivial part is the `doc_id` field. A good design choice is to keep this dependent only on the document's contents, which are fixed, as opposed to the document's name in our directory, which may change. We hash the document's contents to produce a 16-character string for the `doc_id`; this effectively produces a unique string for each pdf that is collision-proof in that changing even a single character in the document drastically changes the hash result and finding two documents that produce the same string is virtually impossible.
