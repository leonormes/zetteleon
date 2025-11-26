---
title: "Search with broot - the good moves"
source: "https://dystroy.org/blog/search-with-broot-the-good-moves/"
created: 2025-11-25
tags:
---
This article is both for people who don't know broot yet, and for those who do but are probably less efficient at searching than they could be.

## broot

Broot is a file manager with a trimmed tree view which helps explore big directories.

To install it, either run `cargo install broot`, or head to [https://dystroy.org/broot/install/](https://dystroy.org/broot/install/) for more options.

With broot installed and first launched, follow its suggestion and go read and edit the config file, at least to ensure it opens text files in your favourite editor.

## Scenarios

I'll introduce the good moves with a few search scenarios.

To make them realistic, I'll search my ~/dev folder, which contains about 800k files taking about 120GB.

When searching the right way, matches are instantly displayed while you type, even in such a huge directory, and only a few keystrokes are necessary, that's what I'll show.

I really suggest you read this document in order, at least at first.

### Go to a file, following filenames

Simplest case: I know I have an old library about caching, I can't remember the name but it must contain "cache".

I launch broot in the console as `br`, then I type a few letters.

With experience, I know that 3 letters are usually enough, I type "cac", the view is updated while I type, with the most probable match selected:

![cac](https://dystroy.org/blog/search-with-broot-the-good-moves/cac.png)

The fuzzy matching algorithm ranks matches higher when the letters are together, or at the start of a word, that's why typing "cac" was enough.

To go to that directory, I hit enter:

![bounded-cache](https://dystroy.org/blog/search-with-broot-the-good-moves/bounded-cache.png)

What I really want is to have a look at the JS code. It's obviously in `js/bounded-cache.js`.

To navigate to that file, I could use the ↓ key a few times, or the tab key. But it's often faster to just type some letters again:

![bounded-cache-js](https://dystroy.org/blog/search-with-broot-the-good-moves/bounded-cache-js.png)

With the right file now focused I can either preview the file with ctrl →, or hit enter to open the file in my text editor.

The whole process took about 5 seconds.

### Super simple composite pattern

I never remember how I named my Rust project dedicated to tests. Is it "rust-tests"? Or "test-rust" perhaps?

In such case, I type what I know: there's both "rust" and "test" in the name.

So the search pattern is `rust&test`

As usual, no need to type it completely:

![rusttes](https://dystroy.org/blog/search-with-broot-the-good-moves/rusttes.png)

I want to go the the `main.rs` file. I don't need to first focus the directory, I just add a few letters of the filename to the pattern:

![rusttesmai](https://dystroy.org/blog/search-with-broot-the-good-moves/rusttesmai.png)

To have a look at the content, I hit ctrl →:

![rusttesmaipreview](https://dystroy.org/blog/search-with-broot-the-good-moves/rusttesmaipreview.png)

### Search on content

If I want my pattern to apply not to the file's path but to the file's content, I prefix it with `c/`.

So to search occurences of "regex\_switch!", I type `c/regex_switch!`.

Note how the view also display text extracts.

![cregexs](https://dystroy.org/blog/search-with-broot-the-good-moves/cregexs.png)

Looking at this view, I decide I want to have a look at all the occurences in the bacon project.

I use the ↑ key to move the selection to the `bacon/src` directory. Then to *focus* the directory while keeping the pattern, I hit ctrl f:

![cregexs-bacon](https://dystroy.org/blog/search-with-broot-the-good-moves/cregexs-bacon.png)

Hitting ctrl →, I can see the selected file in a preview panel to the right, with the pattern copied so that the file is filtered (with some lines before and after):

![cregexs-bacon-preview](https://dystroy.org/blog/search-with-broot-the-good-moves/cregexs-bacon-preview.png)

A new hit ctrl → gives the focus to the preview panel, and another ctrl → reveals the other lines, while staying at the same position in the file:

![cregexs-bacon-preview-unfiltered](https://dystroy.org/blog/search-with-broot-the-good-moves/cregexs-bacon-preview-unfiltered.png)

At this point, I can also hit enter to open the file at the right line in my favorite text editor.

### Search on content but filter by name

Let's assume I now want to look for projects importing the "termimad" library, and see the version.

What I want is to find the "termimad" string in `Cargo.toml` files. The search query combines both a name filter (`cargot`) and a content filter (`c/termimad`). Together, they make `cargot&c/termimad`:

![cargot-termimad](https://dystroy.org/blog/search-with-broot-the-good-moves/cargot-termimad.png)

As usual, I can jump between matches with tab and ctrl tab, open a file with enter, or look at the preview with ctrl →.

## A few notes

Starting from the last scenario, we can dive into several enlightening disgressions:

### Case and diacritics

We typed `cargot` to find `Cargo.toml` files, which works because the fuzzy search algorithm ignores the case.

But it also ignores diacritics, which means you could type `foret` to match `forêt`, and it applies unicode equivalence rules, which means you don't even have to know that, at byte level, there are several ways to write a `è` (well, if you know about [unicode equivalence](https://en.wikipedia.org/wiki/Unicode_equivalence), you might better understand the behavior of some programs which don't care about it).

What if we wanted to first search by content and then add the filename pattern?

It would have been a little slower (filtering by filename is faster to exclude files) but this is still a frequent operation because you don't always initialy realize that you also want to filter on file names.

The query would then have been `c/termimad/&cargot`.

As you see, a `/` is necessary after "termimad". To understand it, you need to know that a simple (not composite) query's canonical form is `<prefix>/<pattern>/`, eg `c/termimad/`. There's no `<prefix>/` nor ending slash when the query is for a fuzzy filepath filtering, and the second slash can be omited when there's nothing after (ie it's not a composite query).

### Search with a regular expression

What if we wanted to search not "Cargo.toml" files, but any "toml" file? And not use fuzzy filtering but be sure to match only files ending in "toml" or ".toml"?

Then we could have use a regex filtering, which is between slashes: `/toml$/` or `/\.toml$/` (the `$` matches the end of the string). Combined with the content pattern, this makes `/toml$/&c/termimad`.

Regular expressions, by default, are case-sensitive. JavaScript developpers won't be surprised to learn that you can make the expression case-insensitive by adding a `i` at the end, that is `/toml$/i` to match both "TOML" and "toml" (the combined pattern becomes `/toml$/i&c/termimad`).

It's also possible to use a regular expression to seach on file content, using `cr/` as a prefix instead of `c/`.

For example, here's searching for the termimad import specified with a patch precise version in Cargo.toml files:

![cr](https://dystroy.org/blog/search-with-broot-the-good-moves/cr.png)

### Complex query composition

Most often, you'll use a simple pattern, be it a fuzzy search pattern or a regular expression.

You'll also combine two patterns with the `&` (and) operator.

But sometimes, you'll need the power of boolean expressions to combine patterns with `&` but also `|` and `!` and even braces.

Here are a few examples:

- `/js$/&!c/;`: js files which do not contain any semicolon
- `/miaou/|c/miaou`: files whose name or content contains "miaou"
- `/js$/&(c/miaou/|c/ouaf/)`: js files containing either "miaou" or "ouaf"

### Escaping

Usual escaping rules apply in regular expressions. We saw the dot escaped in `/\.toml/`, but you also need to escape `[`, `)`, `+`, etc. depending on their position.

Some escapings are also needed out of regular expressions.

To start with, a `/` must be escaped as it normally closes a pattern.

Then, the `:` and space normally separate the search query from the verb which may follow, so they need to be escaped too if you want to search for them.

### Ignored files

If you're a developper, chances are that the files you're interested into are in smaller number than the ones in the `build`, `target`, `node_modules`, etc. directories.

And files whose name starts with a dot are usually hidden files.

That's why broot hides "ignored" and "git-ignored" files.

Small flags at the bottom right tell you whether the ignoring rules are applied. When hidden files are filtered out, you see `h:y`. When "hidden" files are shown but not git-ignored ones, you have this:

To toggle those filtering, use alt h and alt i.

### Search again

The ctrl s shortcut has two purposes:

If you searched, then did something else, it restores the last search query.

If broot search wasn't complete, ie broot stopped because it had enough well ranked matches to fill the screen, then you may ask broot to search more, looking for deeper matches which would be even better ranked

## Recap, all the shortcuts

- launch broot with `br`
- type a few letters for a fuzzy search
- prefix a pattern with `/` to do a regex search, maybe case insensitive (eg `/toml/i`)
- prefix a pattern with `c/` to search the content of files
- prefix a pattern with `cr/` to search the content of files with a regular expression
- use `&`, `|`, `!`, `(`, and `)` for composite searches
- move with either the arrow keys, or tab and back tab
- focus a directory with enter
- ctrl f to focus a directory *and* keep the search pattern
- ctrl s to search again
- ctrl → opens the matching file in preview
- enter opens the file in your editor (at the right line if you searched by content)

For more details, head to [broot's input reference](https://dystroy.org/broot/input/)