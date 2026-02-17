## Citation decisions

Citation format
- Every substantive claim must have at least one citation
- If a chunk is used, cite it
- If confidence is low, say so and cite what you do have

Citation schema
- `[{doc_id}, page {page}, chunk {chunk_id}]`

Example answer with citation
- Prompt: "Can you explain functional linear regression with a roughness penalty?"
- Ideal example response: "[ramsay_silverman_fda_2005, page 123, chunk 4] Functional linear regression with a roughness penalty, as described in Ramsay & Silverman (2005) chapter 15, involves representing both functional inputs and the regression function in a particular basis, and penalizing a chosen roughness function, typically described as [math] ... [ramsay_hooker_graves_fda_r_matlab, page 456, chunk 1] Documentation for an implementation in R can be found in chapter ...

Example refusal from low confidence
- Prompt: "What is the Snake Lemma in homological algebra?"
- Ideal example response: "I'm not finding any matches close to this prompt in my database. The 3 closest matches are 1. [source_1, page 3, chunk 9] a paragraph of an academic paper where the authors apply functional linear discriminant analysis to a classification problem involving images of snakes, ..."
