---
captured: "2026-04-09T13:31:53+01:00 2026-04-09T13:31:53+01:00"
created: 2026-04-09T12:31:59+00:00
modified: 2026-04-20T13:21:27+00:00
source: "https://gemini.google.com/app/7b82caff9b277fe7"
status: "processing"
tags: ["input"]
title: HEAD Embeddings Explained Meaning as Geometry
type: "head"
---

## Raw Output / Content

You

<Https://youtube.com/watch?v=7aATI>\_t5UeY&si=UUYM40EMljxCHJYR

---

Gemini

Here is a comprehensive summary of the video "How Embeddings Actually Work" by Claudius Papirus.

The Core Concept of Embeddings

- Meaning as Geometry: Tokens are fundamentally just arbitrary IDs that mean nothing to a computer on their own. The crucial transition from a meaningless ID to a meaningful vector (a structured list of numbers) is called an "embedding" \[[01:15](http://www.youtube.com/watch?v=7aATI_t5UeY&t=75)\]. \* Vector Maths: Because words are converted into numerical coordinates in a high-dimensional space, models can perform literal maths to compute relationships. The most famous example of this spatial logic is: _king - man + woman = queen_ \[[00:00](http://www.youtube.com/watch?v=7aATI_t5UeY&t=0)\].
- Clustering by Context: Words with similar meanings—such as "happy", "joyful", and "cheerful"—naturally group together as neighbours in this geographical space \[[04:15](http://www.youtube.com/watch?v=7aATI_t5UeY&t=255)\].

The Evolution of the Architecture

- Word2Vec (2013): A researcher named Thomas Mikolov made meaning "trainable" by building a neural network tasked purely with predicting the words that surround a target word \[[03:01](http://www.youtube.com/watch?v=7aATI_t5UeY&t=181)\]. This successfully encoded complex relationships, such as gender, tense, and geography, into consistent geometric directions without any human labelling \[[04:35](http://www.youtube.com/watch?v=7aATI_t5UeY&t=275)\].
- The Polysemy Problem: Early static embeddings had one major flaw. A word with multiple meanings, like "bank", was assigned the exact same vector whether it referred to a riverbank or a financial institution, resulting in a blurry average of its definitions \[[05:32](http://www.youtube.com/watch?v=7aATI_t5UeY&t=332)\].
- Contextual Shift (2018): Breakthroughs like ELMo and BERT solved this by making embeddings dynamic \[[06:35](http://www.youtube.com/watch?v=7aATI_t5UeY&t=395)\]. The vector for "bank" next to "river" is now pulled in a completely different numerical direction than "bank" next to "investment" \[[06:42](http://www.youtube.com/watch?v=7aATI_t5UeY&t=402)\].

How Modern Models Utilise Them

- Transformer Reshaping: In modern architectures, tokens start with a general initial embedding, but the model's "attention mechanism" reshapes these vectors layer by layer. It continually adjusts their coordinates to capture the exact contextual nuances of the specific sentence \[[06:58](http://www.youtube.com/watch?v=7aATI_t5UeY&t=418)\].
- Real-World Applications: This underlying geometry powers much of the technology we use today. It allows modern search engines to match documents based on underlying meaning rather than exact word matches, and it drives advanced recommendation systems and language translations \[[08:21](http://www.youtube.com/watch?v=7aATI_t5UeY&t=501)\].

You can watch the full video here: [https://youtube.com/watch?v=7aATI\_t5UeY](https://www.google.com/search?q=https://youtube.com/watch%3Fv%3D7aATI_t5UeY)
