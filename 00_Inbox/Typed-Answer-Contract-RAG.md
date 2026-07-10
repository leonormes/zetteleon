---
created: 2026-07-10T17:08:29+00:00
modified: 2026-07-10T17:10:28+00:00
permalink: llmeon/00-inbox/typed-answer-contract-rag
tags: [8A]
title: Typed-Answer-Contract-RAG
type: note
---

## Typed Answer Contract (TAC): RAG Hallucination Prevention via Structured Output

> TDS Article: _Stop Returning Text from RAG: The Typed Answer Contract That Prevents Hallucination_ (July 4, 2026)[^1]

*

### Executive Summary

The article argues that returning free-form text from a RAG pipeline is the _primary architectural source_ of hallucinations in production systems—not just bad retrieval. The fix is to replace the "answer in prose" step with a Typed Answer Contract (TAC): a strict Pydantic/JSON Schema that the LLM must populate. If the output doesn't conform to the schema, the pipeline rejects it. This transforms the LLM from a creative writer into a deterministic data extractor—verifiable, testable, and integrable directly into downstream systems.[^2][^3]

*

### The Core Problem: Unlimited Degrees of Freedom

Standard RAG pipelines end with an instruction like _"Based on the context, answer the question."_ That gives the model unlimited latitude to:

- Blend pre-training knowledge with retrieved context, overriding what the documents actually say
- Sound confident while being factually wrong—_hallucination camouflage_ in prose[^3]
- Produce output downstream systems (CRM, ERP, workflows) cannot parse without error-prone regex or another LLM call[^2]

Production debugging data cited in the article estimates ~30% of hallucinations are not due to bad retrieval but due to the LLM generating content with no grounding in the provided text—because fluency is rewarded over accuracy in training. A block of free-form text hides false dates, wrong prices, or fabricated legal clauses in plain sight.[^4][^5]

*

### The Solution: Schema is the Contract

A TAC reframes the generation step as a structured data extraction task. Instead of asking _"What does this document say?"_, the pipeline asks the model to populate a Pydantic model. Each field in the schema is a discrete, checkable question:[^1][^3]

```python
from pydantic import BaseModel, Field

class RAGAnswer(BaseModel):
    answer: str = Field(description="Answer derived ONLY from context.")
    is_definitive: bool = Field(description="True if context contains a clear answer.")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence from 0 to 1.")
    source_ids: list[str] = Field(description="Chunk IDs used as evidence.")
    missing_info: bool = Field(description="True if context is insufficient.")
```

The `missing_info` field is the critical innovation here: it replaces the LLM's vague "I don't know" with a programmatic boolean. If `missing_info is True`, the pipeline _never surfaces the answer to the user_. If `confidence < 0.6`, a disclaimer is appended automatically. The schema enforces honesty via structure, not via prompting.[^4][^3]

#### Evidence Fields for Zero-Hallucination Extraction

The article recommends adding an `evidence` field to each extracted data point, forcing the model to cite the exact source quote. If no direct quote exists, the field stays empty:[^3]

```python
class EvidenceField(BaseModel):
    value: str
    source_quote: str = Field(description="Direct snippet from context proving this value.")
    page_number: int
```

*

### Implementation: The `instructor` Library

Enforcement relies on constrained decoding at the API level. Every major LLM provider as of 2026 supports structured output modes—OpenAI `response_format` with JSON Schema, Anthropic Tool Use, Gemini `response_mime_type`. The recommended library is `instructor` (v3.x), which wraps any LLM client and enforces Pydantic validation with automatic retry:[^6][^4][^2]

```python
import instructor
from openai import OpenAI

client = instructor.patch(OpenAI())

def ask_rag(question: str, context: str) -> RAGAnswer:
    return client.chat.completions.create(
        model="gpt-4o",
        response_model=RAGAnswer,
        messages=[
            {"role": "system", "content": "Produce structured answers. Follow the contract strictly."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
        ]
    )
```

`instructor` automatically converts the Pydantic model to a JSON schema, passes it as a tool definition, validates the response, and retries with the validation error message if it fails—achieving 95%+ correction on first retry. For self-hosted infrastructure (vLLM, llama.cpp), constrained decoding enforces JSON grammar at the token-generation level, making non-conforming outputs structurally impossible.[^7][^6]

*

### Text-based RAG vs. Typed Answer Contract

| Feature | Text-based RAG | Typed Answer Contract |
|---|---|---|
| Output format | Natural language prose | Validated JSON / Pydantic object |
| Validation | Manual review / LLM-eval | Schema-level, automated |
| Hallucination risk | High—hidden in text | Low—constrained by types and evidence fields |
| Downstream integration | Requires regex / secondary parsing | Native programmatic integration |
| Testability | Hard to unit test | Unit-testable like any typed object |
| Auditability | Weak—no source linkage | Strong—every field tied to a chunk ID |
| Failure handling | Silent wrong answer | Pipeline rejects or flags automatically |

[^8][^2][^3]

*

### Validation and Completeness Checks

The article goes beyond schema enforcement and introduces two additional safety layers:[^2]

Self-assessment fields—Confidence scores, extraction methods, and `evidence_conflict` flags are embedded directly in the schema. This turns the LLM into an active diagnostic tool: it signals whether retrieved context was complete or whether contradictions were found, enabling the pipeline to trigger a broader retrieval search before presenting results.[^2]

Overlap page verification—Because LLMs can only evaluate what they see, a truncated document may _look_ complete. The architecture pulls an additional overlap page alongside the primary retrieved context. While the model generates its response, the pipeline checks the trailing page to confirm whether lists or clauses were cut off artificially. If continuation content is found, the partial result is rejected and retrieval is retried.[^2]

*

### Claimed Results and Validation

The article's companion implementation report for a legal document Q&A system cites hallucination rate dropping from 12% to 1.7%—not because the model improved, but because ~30% of outputs were rejected before reaching users. This is independently supported by peer-reviewed research (arXiv, April 2024) showing that structured output RAG significantly reduces hallucinations and improves generalization in out-of-domain settings.[^9][^4]

The approach is further corroborated by AWS Bedrock's February 2026 structured output announcement, which frames constrained decoding as the solution to JSON generation failures that "routinely break integration" in production. The `instructor` library underpinning the implementation is independently validated in production DevOps environments, consistently handling multi-provider LLM output with automatic retry.[^10][^11][^6]

What the article does _not_ claim:

- TAC is not a complete fix—broken retrieval still produces broken answers within a valid schema[^4]
- Schema complexity is a genuine trade-off; schemas with 15+ nested fields degrade model performance[^4]
- Self-assessed confidence fields can themselves be overconfident; secondary validation or a second LLM call is recommended for critical fields[^4]

*

### What This Offers You (Leon—DevOps / AI Pipeline Context)

Given your Go learning track, infrastructure automation focus, and LLM prompt engineering work, the TAC pattern is highly applicable:

#### Immediate Applications

- Infrastructure document Q&A—Any internal RAG over runbooks, Terraform docs, or Helm chart references can return structured, auditable objects instead of chatty prose. `kubectl` or ArgoCD context queries become programmatically parseable.
- AI-assisted triage pipelines—Alerts or incident summaries can return `{ severity: Enum, affected_services: List[str], confidence: float, source_chunk_id: str }` rather than paragraphs your on-call automation cannot parse.
- Go TDD compatibility—Typed JSON outputs map cleanly to Go structs. Schema-first design means you define the expected output as a Go type, test it, and assert against it—exactly aligning with your TDD workflow.

#### Tooling Stack

- Python: `instructor` + `pydantic v2`—lowest friction path[^6][^10]
- Self-hosted / open-source models: `vLLM` or `llama.cpp` with grammar-constrained decoding—no proprietary API required[^7]
- Multi-provider failover: n1n.ai or LangChain's `with_structured_output` for model-agnostic enforcement[^12][^3]

#### ADHD-workflow Fit

The pattern removes ambiguity from the _output_ of AI tools you use in your own workflow. A structured response with `confidence`, `missing_info`, and `source_ids` gives you immediate, scannable signal—no need to re-read a paragraph to judge if an AI answer is trustworthy.

*

### Key Takeaway

The Typed Answer Contract is not a novel concept, but the article synthesises it into a clear, production-validated pattern: treat LLM generation as a typed data extraction step, not a text completion step. The schema is the contract between document, model, and downstream system. Structure gives you the power to programmatically check for truth—something unstructured prose will never allow.[^4][^2]

---

### References

1. [Stop Returning Text from RAG: The Typed Answer Contract That Prevents Hallucination](https://towardsdatascience.com/stop-returning-text-from-rag-the-typed-answer-contract-that-prevents-hallucination/) - Enterprise Document Intelligence [Vol.1 8A] - The schema is the contract: every field is a question…
2. [Typed Answer Contract Prevents Hallucination in RAG Systems](https://hyper.ai/en/stories/24f099ae0e9b0af55b0edc9669b4eccf) - Build the Future of Artificial Intelligence
3. [Implementing Typed Answer Contracts to Prevent Hallucination](https://explore.n1n.ai/blog/stop-returning-text-from-rag-typed-answer-contracts-2026-07-04) - Learn why raw text responses are the weakest link in your RAG pipeline and how to implement schema-b…
4. [Prevent RAG hallucinations with typed answer contracts: complete guide](https://ai-manual.ru/article/typed-answer-contracts-the-only-way-to-stop-rag-hallucinations-with-code/) - Learn how to use typed answer contracts (Pydantic + structured generation) to prevent RAG hallucinat…
5. [Դադարեցրեք տեքստային պատասխանները RAG-ում. տիպայնացված պայմանագիր՝ հալյուցինացիաները կանխելու համար](https://www.aoodax.com/hy/blog/stop-returning-text-from-rag-prevent-ai-hallucination-via-typed-answers-mr6sgurk) - Դադարեցրեք տեքստային պատասխանները RAG-ից. մուտքագրված պատասխանի պայմանագիր, որը կանխում է հալյուցինա…
6. [LLM Output Validation with Instructor + Pydantic in Production](https://devopsboys.com/blog/llm-output-validation-instructor-pydantic-production-2026) - LLMs return unpredictable text. Instructor + Pydantic turns that into validated, typed Python object…
7. [LLM Structured Outputs: Schema Validation for Real Pipelines (2026)](https://collinwilkins.com/articles/structured-output) - If you're running models on your own infrastructure (vLLM, llama.cpp, TGI), constrained decoding eng…
8. [Stop RAG Hallucinations: Force Your Bot to Cite Sources](https://theaiinternship.com/blog/stop-rag-hallucinations-citations/) - RAG reduces hallucinations but does not eliminate them. Structured output and citation enforcement g…
9. [Reducing hallucination in structured outputs via Retrieval ... - arXiv](https://arxiv.org/abs/2404.08189) - A common and fundamental limitation of Generative AI (GenAI) is its propensity to hallucinate. While…
10. [Learning](https://python.useinstructor.com/learning/) - A lightweight library for structured outputs with LLMs.
11. [Structured outputs on Amazon Bedrock: Schema-compliant AI ... - AWS](https://aws.amazon.com/blogs/machine-learning/structured-outputs-on-amazon-bedrock-schema-compliant-ai-responses/) - Today, we're announcing structured outputs on Amazon Bedrock—a capability that fundamentally transfo…
12. [9. RAG with Structured Outputs — JSON Mode + Pydantic](https://idir-mellaz.fr/structured-outputs-pydantic/) - Force your RAG pipeline to always return valid, typed data. Combine OpenAI JSON mode, Pydantic v2 sc…
