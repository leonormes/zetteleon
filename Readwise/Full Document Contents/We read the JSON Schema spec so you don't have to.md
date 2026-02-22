# We read the JSON Schema spec so you don't have to

![rw-book-cover](https://i.forbesimg.com/144X144-F.png)

## Metadata
- Author: [[Owen Shepherd]]
- Full Title: We read the JSON Schema spec so you don't have to
- Category: #articles
- Summary: Generating structured JSON output with large language models is hard because many tools silently ignore important constraints, causing errors in real use. The authors built a new engine, dotjson, that treats JSON schema translation like compiling code to avoid these silent failures. Dotjson supports more features than other tools and clearly reports unsupported ones, ensuring reliable and correct output.
- URL: https://share.google/vHQhZWT3dDlk3CMgO

## Full Document
![json-schema-comparison-snippet.png](https://blog.dottxt.ai/images/json-schema-comparison-snippet.png)
Figure 1: [Click here to see the full comparison](https://blog.dottxt.ai/json-schema-comparison.html)

#### Structured generation is harder than you think

The beating heart of a thousand AI success stories, from code agents to information extraction, is the ability for an LLM to generate blocks of correctly structured JSON output. While there have been a number of other attempts to solve this problem (like begging the model, or iterative re-prompting), the only guaranteed solution is [structured generation](https://blog.dottxt.ai/how-fast-cfg.html).

The catch: structured generation is easy to *demo*, it is hard to get correctly.

#### Silent failures

Most structured generation libraries will accept your JSON schema and produce an output that *looks* right. However they sometimes silently ignore constraints they don't fully support. Your agent passes every test, then breaks in production on an edge case the library quietly decided not to handle.

We call this *silent constraint violation*, and it's more common than you'd expect.

Here's a simple schema that most engines will not handle correctly:

```
{
  "type": "string",
  "format": "date",
  "pattern": "^2026"
}

```

This should limit output to dates in 2026. But many implementations—including XGrammar, the default in most inference servers—will silently ignore the pattern constraint and allow any date. No error, no warning. Just wrong output.

**The whole point of structured generation is enforceable guarantees.** A library that silently drops constraints defeats the purpose entirely.

#### This is a compiler problem

One of the reasons for silent failures is that libraries will directly translate JSON Schema into a grammar with string manipulations. That may work for simple use cases, but breaks down as schemas get more complex.

We took a different approach: we treat JSON schema translation as a compiler problem.

Our engine transforms JSON schema through a sequence of three intermediate representations, each pass lowering JSON constraints closer to a context-free grammar. During this lowering phase, we validate that constraints are realizable and propagate and combine them according to the [JSON schema formal specification](https://json-schema.org/draft/2020-12/draft-bhutton-json-schema-00). For people who speak compilers, what we've built is a little ✨ *micropass transpiler* ✨.

We also built our own regex engine from scratch. Turns out this was necessary—existing engines couldn't handle the intersection of regex patterns and grammar constraints that JSON schemas require. It's fast, it supports features we needed that nothing else did, and it might deserve its own post.

This architecture lets us either support a feature correctly or tell you explicitly that we don't. No silent failures.

#### How we compare

We've completely rebuilt **dotjson**, \*our JSON schema engine. We now support more features than any other structured generation product out there (that we've tested).

Here's how **dotjson** stacks up against XGrammar on feature support:

|  | Supported | Partial | Unsupported | Unsound |
| --- | --- | --- | --- | --- |
| dotjson | 43 | 1 | 14 | 1 |
| XGrammar | 28 |  | 19 | 12 |

There are three failure modes that have been separated out in this table: *unsupported* features throw an error when you attempt to use them, *partially supported* features compile with some limitations, and *unsound* features compile but do not behave correctly.

Of these three failure modes, *unsound* is by far the most dangerous for LLM applications. As such, **dotjson** has a strong preference towards explicitly listing features as *unsupported*. What we promise is what we deliver.

The canny reader will have noticed that our engine still has a single *unsound* feature. This is [`oneOf`](https://json-schema.org/understanding-json-schema/reference/combining#oneOf), which officially functions as an `xor` between schemas. As per the official advice, most applications do not want this, and instead want `anyOf`. Because of this, we followed the practice of most of the other major JSON generation libraries, and by default treat `oneOf` constraints as `anyOf` constraints. This feature can be turned off, in which case `oneOf` becomes unsupported.

We have a full feature support table, clipped above, that has been auto-generated from a small set of test cases. It is available [here](https://blog.dottxt.ai/json-schema-comparison.html). You can expand down on the details to see the failed tests.
