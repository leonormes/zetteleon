# n-gram

# N-grams

Character n-grams refer to contiguous sequences of characters extracted from a string of text. In the context of string matching, n-grams are used to compare two strings by analyzing these small character sequences, which can help determine how similar the strings are, even if they aren't exact matches. This is particularly useful when working with text data that might have minor variations, such as spelling differences, abbreviations, or typographical errors.

Here's how character n-grams work:

## What is an N-gram?

- The "n" in n-gram represents the length of the character sequence you want to extract.

   - Unigrams (1-grams) are individual characters.

   - Bigrams (2-grams) are pairs of adjacent characters.

   - Trigrams (3-grams) are sequences of three adjacent characters.

   - n-grams can be generalized to any size (n = 1, 2, 3, 4, etc.).

## Example of Character N-grams

Let's take the word "Leon" as an example and see how character n-grams would be formed:

- Unigrams (n = 1):
   L, e, o, n

- Bigrams (n = 2):
   Le, eo, on

- Trigrams (n = 3):
   Leo, eon

## Application in String Matching

Character n-grams are used to break down two strings into smaller components, allowing for flexible comparison. This method is especially helpful when strings are not exact matches but share some common substrings. For example:

- String 1: "Leon Ormes"

- String 2: "L. Ormes"

Let's take bigrams (2-grams) as an example:

- Bigrams for "Leon Ormes":
   Le, eo, on, Or, rm, me, es

- Bigrams for "L. Ormes":
   L., .O, Or, rm, me, es

While the full names don't match exactly, many bigrams overlap between the two strings:
"Or," "rm," "me," "es" are common, indicating a possible match.

## Advantages of Character N-grams for String Matching

1. Handles Partial Matches: They can capture partial similarities, making them useful when strings differ slightly, such as in misspellings or abbreviations.

   - "Leon" vs. "L.": Using character n-grams, we still capture similarities like "L" and "eo" despite abbreviation.

2. Flexible for Typos: n-grams can tolerate minor character-level changes. For example, "Ormes" and "Omres" (a common typo) would still share a lot of bigrams.

3. Language Agnostic: Unlike word-level n-grams (which may be language-specific), character n-grams work across languages, since they operate at the character level.

## How it Helps in Record Linkage

Character n-grams are often used in approximate string matching algorithms like the Jaccard similarity or [Cosine similarity](Cosine%20similarity), where the goal is to compare the sets of n-grams from two strings to measure how similar they are.

In your case of matching records (e.g., patient names or addresses that may be written differently), character n-grams can help identify similarities between records that may otherwise be missed due to abbreviations, spelling variations, or other differences in how names are written across medical and social care systems.

## Conclusion

Character n-grams break a string into smaller, overlapping sequences of characters, which allows for a flexible comparison of two strings. This method is particularly effective for fuzzy matching tasks where exact string matches may be rare but partial similarities are significant. In the context of medical and social care records, using n-grams can help identify matches even when names, addresses, or other information differ slightly in format or spelling.