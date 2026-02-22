# gemini-cli: Access Gemini models from the command-line

![rw-book-cover](https://eli.thegreenplace.net/favicon.ico)

## Metadata
- Author: [[thegreenplace.net]]
- Full Title: gemini-cli: Access Gemini models from the command-line
- Category: #articles
- Summary: The gemini-cli tool, developed in Go, facilitates data analysis using Google's Gemini models through the command line. By embedding text into vectors, users can find related content, such as blog posts, by leveraging the tool's capabilities. With easy installation and the ability to work with large corpora efficiently, gemini-cli provides a quick way to prototype and experiment with different text processing tasks. The tool's versatile features extend to chatting with the model, querying the API, and offer extensive documentation for developers interested in utilizing LLMs for free.
- URL: https://eli.thegreenplace.net/2024/gemini-cli-access-gemini-models-from-the-command-line/

## Full Document
This post is about a new command-line tool I've recently built in Go - [gemini-cli](https://github.com/eliben/gemini-cli), and how to use it for LLM-based data analysis with Google's Gemini models.

Background: I've been reading [Simon Willison's](https://simonwillison.net/) posts about LLMs with interest, especially his work on tools that leverage LLMs and SQLite to create [fun little analysis pipelines for local documents](https://til.simonwillison.net/llms/openai-embeddings-related-content). Since I've recently done some Go work on [Google's Gemini SDKs](https://github.com/google/generative-ai-go) (also in [langchaingo](https://github.com/tmc/langchaingo)) and wrote a [couple of](https://eli.thegreenplace.net/2023/using-gemini-models-from-go/) [blog posts](https://eli.thegreenplace.net/2024/using-gemini-models-in-go-with-langchaingo/) about it, I was interested in creating a similar pipeline for myself using Go and Gemini models. This is how the idea for gemini-cli was born.

#### The tool

Like any Go command-line tool, gemini-cli is very easy to install:

```
$ go install github.com/eliben/gemini-cli@latest

```

And you're good to go! It will want a Gemini API key set in the GEMINI\_API\_KEY env var or passed with the --key flag. If you don't have an API key yet, you can get one quickly and for free from <https://ai.google.dev/>

#### The motivating task

For a while I've been interested in adding a "related posts" feature to my blog. It was clear that I'll want to use [embeddings](https://en.wikipedia.org/wiki/Sentence_embedding) to convert my posts to vector space and then use vector similarity to find related posts. Check out my earlier [post on RAG](https://eli.thegreenplace.net/2023/retrieval-augmented-generation-in-go/) for additional information on these techniques.

Before starting to write the code, however, I wanted to experiment with a command-line tool so I could rapidly prototype. Think of it as crafting some text processing pipeline from classical Unix command-line tools before trying to implement it in a programming language. gemini-cli excels for precisely such prototyping.

#### Finding related posts

Let's see how to use gemini-cli for my task. I have access to the contents of my blog posts on the file system as a large bunch of [reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) and HTML files. These are private, but you're free to replicate this experiment for any collection of textual documents you have handy. It will even work on programming language source code!

Let's first get the lay of the land - how many files are there [[1]](https://eli.thegreenplace.net/2024/gemini-cli-access-gemini-models-from-the-command-line/#footnote-1)?

```
$ pss -f --rst content/|wc -l
279
$ pss -f --html content/|wc -l
1064

```

OK, so a bit over 1300 overall. Let's start by computing the embeddings for the reST files. We'll ask gemini-cli to write it into a new SQLite DB called blogemb.db, using its embed db subcommand:

```
$ export GEMINI_API_KEY=...
$ gemini-cli embed db blogemb.db --files content/,"*.rst"
Found 279 values to embed
Splitting to 9 batches
Embedding batch #1 / 9, size=32
Embedding batch #2 / 9, size=32
Embedding batch #3 / 9, size=32
Embedding batch #4 / 9, size=32
Embedding batch #5 / 9, size=32
Embedding batch #6 / 9, size=32
Embedding batch #7 / 9, size=32
Embedding batch #8 / 9, size=32
Embedding batch #9 / 9, size=23
Collected 279 embeddings; inserting into table embeddings

```

Let's look at the DB file using the sqlite3 command-line tool:

```
$ sqlite3 blogemb.db
SQLite version 3.37.2 2022-01-06 13:25:41
Enter ".help" for usage hints.

sqlite> .tables
embeddings

sqlite> .schema
CREATE TABLE embeddings (
id TEXT PRIMARY KEY,
embedding BLOB
);

sqlite> select count(*) from embeddings;
279

sqlite> select id, length(embedding) from embeddings limit 10;
content/2014/blogging-setup-with-pelican.rst|3072
content/2014/c++-perfect-forwarding-and-universal-references.rst|3072
content/2014/derivation-normal-equation-linear-regression.rst|3072
content/2014/goodbye-wordpress.rst|3072
content/2014/highlight-tab-gnome-terminal.rst|3072
content/2014/meshgrids-and-disambiguating-rows-and-columns-from-cartesian-coordinates.rst|3072
content/2014/samples-for-llvm-clang-library.rst|3072
content/2014/sfinae-and-enable-if.rst|3072
content/2014/summary-of-reading-july-september-2014.rst|3072
content/2014/summary-of-reading-october-december-2014.rst|3072

```

As expected, we see 279 entries in the table; for each row the id column value is the path of the file and embedding contains the embedding as a blob. Embeddings are returned by the model as arrays of 32-bit floats, and gemini-cli encodes them into a blob as follows:

```
// encodeEmbedding encodes an embedding into a byte buffer, e.g. for DB
// storage as a blob.
func encodeEmbedding(emb []float32) []byte {
  buf := new(bytes.Buffer)
  for _, f := range emb {
    err := binary.Write(buf, binary.LittleEndian, f)
    if err != nil {
      panic(err)
    }
  }
  return buf.Bytes()
}

```

Each float32 thus occupies 4 bytes; since our DB blobs are 3072 bytes long, we can infer that each embedding vector has 768 elements; the embedding model projects our text into 768-dimensional space [[2]](https://eli.thegreenplace.net/2024/gemini-cli-access-gemini-models-from-the-command-line/#footnote-2)!

Back to our task, though. Note that gemini-cli uses the batch-embedding API of Gemini under the hood, so it's efficient for large input corpora. We can control the batch size with a flag; just for fun, let's do this when embedding the HTML files since there are so many of them:

```
$ gemini-cli embed db blogemb.db --batch-size=64 --files content/,"*.html"
Found 1064 values to embed
Splitting to 17 batches
Embedding batch #1 / 17, size=64
Embedding batch #2 / 17, size=64
Embedding batch #3 / 17, size=64
Embedding batch #4 / 17, size=64
Embedding batch #5 / 17, size=64
Embedding batch #6 / 17, size=64
Embedding batch #7 / 17, size=64
Embedding batch #8 / 17, size=64
Embedding batch #9 / 17, size=64
Embedding batch #10 / 17, size=64
Embedding batch #11 / 17, size=64
Embedding batch #12 / 17, size=64
Embedding batch #13 / 17, size=64
Embedding batch #14 / 17, size=64
Embedding batch #15 / 17, size=64
Embedding batch #16 / 17, size=64
Embedding batch #17 / 17, size=40
Collected 1064 embeddings; inserting into table embeddings

```

A brief note on performance: with a batch size of 64, this process took only 17 seconds - not bad for over a thousand documents. In the future I plan to improve this time further with more concurrency and smarter batch size selection [[3]](https://eli.thegreenplace.net/2024/gemini-cli-access-gemini-models-from-the-command-line/#footnote-3).

Let's examine the resulting SQLite DB with all the embeddings:

```
$ stat -c %s blogemb.db
5627904
$ echo "select count(*) from embeddings" | sqlite3 blogemb.db
1343

```

All 1343 entries have made it into the embeddings table, and the total size of the DB is just over 5 MiB.

Now we're ready to look for related posts. The embed similar subcommand takes the name of a SQLite DB that holds all embeddings (like the one we've just created) and a string of content to compare; it also accepts - as an indication that the input content will be piped through standard input, so let's use that:

```
$ gemini-cli embed similar blogemb.db - < content/2023/better-http-server-routing-in-go-122.rst
{"id":"content/2023/better-http-server-routing-in-go-122.rst","score":"1.0000001"}
{"id":"content/2021/rest-servers-in-go-part-2-using-a-router-package.rst","score":"0.8904768"}
{"id":"content/2021/life-of-an-http-request-in-a-go-server.rst","score":"0.83037585"}
{"id":"content/2021/rest-servers-in-go-part-5-middleware.rst","score":"0.8136583"}
{"id":"content/2022/serving-static-files-and-web-apps-in-go.rst","score":"0.7732284"}

```

The output is in [the JSON Lines format](https://jsonlines.org/examples/), and by default prints the ID and the similarity score (using cosine similarity), sorted by decreasing similarity. Unsurprisingly, the most similar post is... itself, with a perfect similarity score of 1.0

The results look pretty good! The most similar posts found indeed are very relevant to the one we were asking about. For fun, let's try a book review and now with a larger list of output candidates (by using the topk flag):

```
$ gemini-cli embed similar blogemb.db --topk=10 - < content/2011/book-review-the-voyage-of-the-beagle-by-charles-darwin.html
{"id":"content/2011/book-review-the-voyage-of-the-beagle-by-charles-darwin.html","score":"1"}
{"id":"content/2008/book-review-the-origin-of-species-by-charles-darwin.html","score":"0.80570847"}
{"id":"content/2006/book-review-the-selfish-gene-by-richard-dawkins.html","score":"0.7845073"}
{"id":"content/2011/summary-of-reading-april-june-2011.html","score":"0.7939675"}
{"id":"content/2004/book-review-a-short-history-of-nearly-by-bill-bryson.html","score":"0.7784306"}
{"id":"content/2005/book-review-around-the-world-in-80-days-by-jules-verne.html","score":"0.7792236"}
{"id":"content/2005/book-review-the-double-helix-by-james-watson.html","score":"0.7658307"}
{"id":"content/2008/book-review-after-tamerlane-by-john-darwin.html","score":"0.7641713"}
{"id":"content/2005/book-review-mysterious-island-by-jules-verne.html","score":"0.7605505"}
{"id":"content/2008/book-review-the-adventures-of-tom-sawyer-by-mark-twain.html","score":"0.75610566"}

```

#### What's next

For my task, I now have the basic information available to implement it, and all the infrastructure for running experiments; with gemini-cli in hand, this took less than 5 minutes. All I needed to do is [write the tool](https://xkcd.com/1205/) :-)

I really enjoyed building gemini-cli; it's true to the spirit of simple, textual Unix CLIs that can be easily combined together through pipes. Using SQLite as the storage and retrieval format is also quite pleasant, and provides interoperability for free.

For you - if you're a Go developer interested in building stuff with LLMs and getting started for free - I hope you find gemini-cli useful. I've only shown its embed \* subcommands, but the CLI also lets you chat with an LLM through the terminal, query the API for various model details, and everything is configurable with extra flags.

It's [open-source](https://github.com/eliben/gemini-cli), of course; the README file rendered on GitHub has extensive documentation, and more is available by running gemini-cli help. Try it, ask questions, open issues!

|  |  |
| --- | --- |
| [[1]](https://eli.thegreenplace.net/2024/gemini-cli-access-gemini-models-from-the-command-line/#footnote-reference-1) | I like using [pss](https://github.com/eliben/pss/), but feel free to use your favorite tools - git grep, ag or just a concoction of find and grep. |

|  |  |
| --- | --- |
| [[2]](https://eli.thegreenplace.net/2024/gemini-cli-access-gemini-models-from-the-command-line/#footnote-reference-2) | A word of caution: LLMs have limited context window sizes; for embeddings, if the input is larger than the model's context window it may get truncated - so it's the user's responsibility to ensure that input documents are properly sized. gemini-cli will report the maximal number of input tokens for supported models when you invoke the gemini-cli models command. |
