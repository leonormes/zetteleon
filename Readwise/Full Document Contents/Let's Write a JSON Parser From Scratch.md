# Let's Write a JSON Parser From Scratch

![rw-book-cover](https://sushantdhiman.dev/content/images/2026/02/https-3a-2f-2fsubstack-post-media-s3-amazonaws-com-2fpublic-2fimages-2fdc1e0bfd-36b5-4dc8-a131-3af489f44757_1280x720-png.jpg)

## Metadata
- Author: [[Sushant Dhiman]]
- Full Title: Let's Write a JSON Parser From Scratch
- Category: #articles
- Summary: The author explains how to build a simple JSON parser by first creating a tokenizer that breaks the JSON string into tokens. Then, these tokens are used to make an Abstract Syntax Tree (AST) representing the JSON structure. This approach helps understand parsing and how JSON data can be processed step by step.
- URL: https://sushantdhiman.dev/lets-write-a-json-parser-from-scratch/

## Full Document
Hi,

It's been a long time since I wrote something in this newsletter. Recently I was learning about language parsing and abstract syntax trees. After getting some knowledge about this, I decided to write a JSON parser from scratch.

###### Parsing:

It is the process of analysing the structure of a string (basically any programming language syntax). Parsing helps us to determine the meaning of the text. Writing a parser for a programming language is a very complex task because programming languages generally have a lot of keywords and syntax rules. Handling all those syntax and keywords can be overwhelming and highly difficult. But in the case of JSON we have a very limited number of keywords and syntax rules. So writing a JSON parser is a relatively easier task.

###### Tokenization:

It is the process that is done before parsing. Tokenization means breaking down and categorizing string of character into smallest units called tokens. Below table will give you a solid idea of what tokens look like.

```
JSON:
{
  "name": "iPhone 6s",
  "price": 649.99,
  "isAvailable": true
}

Token       : Type
------------:--------------
{           : BRACE_OPEN  
name        : STRING  
:           : COLON  
iPhone 6s   : STRING  
,           : COMMA  
price       : STRING  
:           : COLON  
649.99      : NUMBER  
,           : COMMA  
isAvailable : STRING  
:           : COLON  
true        : TRUE  
}           : BRACE_CLOSE  

```

Once tokenization break down string into tokens than these tokens are given to Parser which created an Abstract Syntax Tree. We will discuss it later in this post. But your 1st step is to create a tokenizer.

###### Writing The Tokenizer:

Now let’s get into the code part where we tokenize a JSON string.

I wrote a function called `Tokenize` which takes a JSON string and returns a list of tokens. It loops through the string, character by character, and breaks it down into meaningful pieces like `{`, `"key"`, `:` or `123`. These pieces are what we call **tokens**.

Here’s the full code, broken down step by step.

We will first start with creating some basic types for all the tokens.

![](https://sushantdhiman.dev/content/images/2026/02/0b3765fa-b45c-4e40-be83-f8acc7242471_2080x2012.png)
We start with a `current` pointer to keep track of where we are in the string. `stringLength` helps us not go out of bounds, and `tokens` is the slice where we’ll collect all the tokens we generate.

![](https://sushantdhiman.dev/content/images/size/w2400/2026/02/2b523d02-44fb-4037-b769-f8cc3557db70_2912x3364.png)
###### Skipping Whitespace

We loop through the entire string. If we hit whitespace, we skip it because whitespace doesn't matter in JSON.

Than we handle all the simple symbols here. These don’t need much logic — just push them to the tokens list and move on.

![](https://sushantdhiman.dev/content/images/size/w2400/2026/02/7fdeb73a-21ce-4e9b-a2c3-c6301d42ed54_2656x2192.png)
###### Handling Strings

When we encounter a `"`, we start reading a string. We look for the closing quote, while also making sure to skip escaped quotes like `\"`. If the string is never closed, we throw an error. Otherwise, we extract the string and add it as a token.

![](https://sushantdhiman.dev/content/images/size/w2400/2026/02/83371a2e-050f-4ad1-89f3-734ca32869ad_2836x1564.png)
###### Literals and Numbers

We check for `true`, `false`, and `null` first. If we see one of these keywords, we push it to the tokens list and jump ahead accordingly.

![](https://sushantdhiman.dev/content/images/size/w2400/2026/02/19f95384-b3f9-4c94-83bb-0d431e70636d_3680x5524.png)
###### Numbers (slightly tricky)

JSON numbers can get complex. They might contain decimals, negative signs, and exponential notation (like `1.2e+10`). We carefully walk through each character to build the number string. I also added validations to reject bad formats like `00`, multiple dots, or missing exponent digits.

![](https://sushantdhiman.dev/content/images/size/w2400/2026/02/de01a872-b4ff-4b2b-b641-93433c085bb3_3680x1112.png)
###### If nothing matches

If none of the above matched, the character is invalid in JSON — so we just throw an error.

![](https://sushantdhiman.dev/content/images/size/w2400/2026/02/a800a5f3-9a5f-4970-b6e5-6a7cbb476791_3680x1744.png)
###### Number validation helper

This method is used to check for bad leading numbers in JSON.

![](https://sushantdhiman.dev/content/images/size/w2400/2026/02/14046010-e79d-4177-8286-f76094ac37bf_3680x1204.png)
This just prints the list of tokens in a nice readable format. Super handy when testing your tokenizer.

###### Tokenization Output

If we give below JSON to our tokenizer we will get following output.

```
{
  "name": "iPhone 6s",
  "price": 649.99,
  "isAvailable": true
}
```

![](https://sushantdhiman.dev/content/images/2026/02/a76b8015-070e-423d-8c8d-c0f88bd52019_836x658.png)
Now our JSON is nicely tokenized and each character had been given its appropriate token type.

###### Parsing & AST

We have now created a tokeniser that converts JSON objects to tokens. The next step is to create a parser that can convert these tokens into an abstract syntax tree. But first, let's understand what an abstract syntax tree is.

###### Abstract Syntax Tree (AST)

It is a Tree structure that represent syntactic structure of source code. To learn more about it refer to this awesome article: <https://dev.to/balapriya/abstract-syntax-tree-ast-explained-in-plain-english-1h38>

###### Writing The Parser:

![](https://sushantdhiman.dev/content/images/size/w2400/2026/02/109429aa-6e9e-4cc2-b3a4-a2cdc494722f_3680x4984.png)
This is the base interface for all AST node types. Every node will implement the `Type()` method, which is a simple way to identify what kind of data (Object, Array, String, etc.) it holds.

![](https://sushantdhiman.dev/content/images/size/w2400/2026/02/5e73860a-7aaf-41b0-9f76-761fff595503_3680x1204.png)
* This is the main function you call to parse the token stream.
* It checks if there’s anything to parse. Then it initializes a `current` pointer (used as an index into the `tokens` slice).
* Delegates to `parseValue`, which handles all the different types.

![](https://sushantdhiman.dev/content/images/size/w2400/2026/02/89a13323-fee7-4605-abec-1fcb47e26fa1_3680x3992.png)
Basic safety check: if the current token is past the end, return an error.

Now comes the type-checking:

* String token → wrap it in `StringNode`.
* Number → parse into float64.
* Booleans and null are direct mappings.
* Delegates to specialized functions for objects (`{}`) and arrays (`[]`).
* Anything unexpected = throw an error.

![](https://sushantdhiman.dev/content/images/size/w2400/2026/02/a6ccdd46-799b-4127-b0fd-d26912ffa9bc_3680x4264.png)
* Skip the `{` token.
* Initialize an `ObjectNode`.
* Extract the key from the object and parse the value using the already written `parseValue()` function.

![](https://sushantdhiman.dev/content/images/size/w2400/2026/02/58fc9c95-0bef-4442-94b2-e6fae7804acc_3680x3092.png)
* Start parsing array (skip the `[` token).
* Loop through all values.
* Each value is parsed with `parseValue` and append value to initialized array.
* Ensure the array ends correctly with `]`.

Below is the output we will get if we parse the tokens of JSON that we used above.

```
{
    map[isAvailable:{true}
    name:{iPhone 6s} 
    price:{649.99}]
}
```

* Try converting this AST node to native Golang data structure and use it.

###### Let’s Connect

I'm always willing to get to make new connections.

###### Final Thoughts

So this was how we could implement a simple JSON tokenizer and parser from scratch. If you have any suggestions or doubts, you can always comment below. **Consider subscribing to my newsletter to get notified for new posts.**
