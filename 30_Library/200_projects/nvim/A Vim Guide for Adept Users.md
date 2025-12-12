---
aliases: []
author: ["[[Matthieu Cneude]]"]
confidence: 
created: 2025-07-07T00:00:00Z
description: Continuing our path to Vim mastery with digraphs, interesting keystrokes in VISUAL and INSERT MODE, thorough explanations of Vim's regex engine, and more!
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:16Z
published: 2021-04-13
purpose: 
review_interval: 
see_also: []
source: https://thevaluable.dev/vim-adept/
source_of_truth: []
status: 
tags: []
title: A Vim Guide for Adept Users
type:
uid: 
updated: 
version:
---

1. How to manipulate multiple quickfix and location lists.
2. What are digraphs and how to use them.
3. Useful keystrokes in INSERT mode.
4. Useful keystrokes in VISUAL mode.
5. Vim regular expressions.
6. Using shell commands in Vim.
7. Folding content.
8. Try in Vim what’s described while reading the article.
9. Create your own cheatsheet. It will help you remember all the shenanigans and you can even refer to it in your daily work.
10. Pick and choose new concepts from this article from time to time and try to integrate them to your own workflow.

What did Dave learn in his adventure?

## Multiple Quickfix and Locations Lists

We saw in the [last article](https://thevaluable.dev/vim-advanced/) how useful the quickfix lists are. But it didn’t explain how to access the stack of these lists.

Indeed, each time we create a quickfix list, it will be added to a stack and the previous one will be pushed down. This stack can contain 10 quickfix lists maximum; each time you create a quickfix list, the 10th on the stack will disappear forever in the Forgotten Pit of Quickfix Lists.

This is true for location lists too: you’ll have a stack containing 10 of them *per window open*.

You can use these commands to manipulate this stack:

- `:chistory` or `:chi` - Show the stack of quickfix lists and point out the current one.
- `:colder` or `:col` - Change the current quickfix list to the next older one.
- `:cnewer` or `:cnew` - Change the current quickfix list to the next newer one.

You can add a count after `:colder` and `:cnewer`. For example, running `:colder 3` will select the quickfix list which is 3 positions down the current one.

To change your current location list, you can replace the first letter `c` (qui `c` kfix) of the commands above with a `l` (`l` ocation).

`:help quickfix-error-lists`

## Digraphs

Vim allows you to insert special characters easily using *digraphs*. To insert these special characters, you need to know their *representations*, always two “normal” characters.

Here are some useful commands:

`:digraphs` or `:dig` - Display the digraphs available.`:digraphs <char1><char2> <number>` - Create a new digraph represented with the characters `<char1><char2>`. The `<number>` is its decimal representation (Unicode character).

You can also use the following keystrokes in INSERT mode to spit these good digraphs:

- `CTRL+K <char1><char2>` - Insert the digraph represented with the characters `<char1>` and `<char2>`.
- `<char1><BS><char2>` - Insert the digraph represented with the characters `<char1>` and `<char2>` (only if the option `digraph` is set to true).

Here are some examples:

- `CTRL+K ->`: →
- `CTRL+K TM`: ™
- `CTRL+K Co`: ©
- `CTRL+K Rg`: ®
- `CTRL+K Eu`: €
- `CTRL+K +-`: ±
- `CTRL+K OK`: ✓
- `CTRL+K XX`: ✗

I owe my sanity to digraphs when I was trying to [solve some problems in propositional logic](https://raw.githubusercontent.com/Phantas0s/playground/master/cs/04-math/discrete-math-applications/1/1.3/1.3.md) full of “∧” (`CTRL+k AN`), “∨” (`CTRL+k OR`) or “∈” (`CTRL+k (-`).

A last tip: you can use the keystroke `ga` in NORMAL mode to display the digraph of the character under the cursor (if there is one).

- `:help digraph`
- `:help digraph-table`

## Useful Keystrokes in Insert Mode

We saw many keystrokes for NORMAL mode throughout this series, but what about INSERT mode? We need more equality between modes in this world.

Keystrokes in INSERT mode are prefixed with `CTRL`, specifying to Vim that we don’t want to insert some text.

### Inserting and Deleting

- `CTRL+a` - Insert the l `a` st content inserted.
- `CTRL+@` - Insert the l `a` st content inserted and quit INSERT mode.
- `CTRL+h` - Delete the character before the cursor.
- `CTRL+w` - Delete the `w` ord under the cursor.
- `CTRL+u` - Delete everything before the c `u` rsor.
- `CTRL+t` - Add one indenta `t` ion.
- `CTRL+d` - `D` elete one indentation.

We saw already in the [previous article](https://thevaluable.dev/vim-advanced/) how to spit the content of a register in INSERT mode. Let’s introduce some subtleties here:

- `CTRL+R <reg>` - Spit the content of the register `<reg>` *as if you typed it*.
- `CTRL+R CTRL+R <reg>` - Same as `CTRL+R`, but insert the text literally.
- `CTRL+R CTRL+P <reg>` - Spit the literal content of the register `<reg>` with the correct indentation.

When you look at the content of your registers, you might find some weird characters like `^M` or `^I`. You can think of them as `CTRL+m` and `CTRL+i`, which means, if you recorded some macros while being in INSERT more, end-of-line and tabulation respectively.

The first keystroke `CTRL+R <reg>` will insert these end-of-lines and tabulations. For example, if you have the characters `^M` in your register when you display them via `:reg`, it will become an end-of-line when you insert it.

If you use `CTRL+R CTRL+R <reg>`, you’ll have the literal characters `^M` inserted in your buffer. It’s handy to spit a recording for a macro, modify it, and then save it back to your register `<reg>`. From there, you can execute your modified macro.

To know what the literal version of a key is, you can use `CTRL+V` (or `CTRL+Q`) in INSERT mode followed by the key. For example, `CTRL+V ENTER` will display `^M`.

Since we’re speaking about `CTRL+V`, you can also use it followed by the decimal, octal, or hexadecimal value of a character. It’s another way to insert special characters without using digraphs. You can run `man ascii` to have access to the ASCII table in your shell and choose whatever character you want.

The keystrokes `CTRL+V` and the equivalent `CTRL+Q` can be used in COMMAND-LINE mode too.

### Back to NORMAL Mode

The keystroke `CTRL+o` in INSERT mode allows you to come back to NORMAL mode for one keystroke (or one command in COMMAND-LINE mode). When it’s done, you’ll be automatically back in INSERT mode.

### Undo in Insert Mode

You can stop the undo sequence if you use `CTRL+G u` in INSERT mode.

For example, try to insert some text in INSERT mode and then undo your insertion with `u` in NORMAL mode. Everything you’ve inserted is now gone.

If you want to undo each word you’ve inserted instead of everything, you can use this command:

```sh
:inoremap <space> <C-G>u<space>
```

Now, each time you press `SPACE` in INSERT mode, you’ll stop the undo sequence. When you hit `u` in NORMAL mode, it will undo what you’ve inserted after hitting the last `SPACE`. If you undo again, it will undo another word, and so on. There is a drawback, however: abbreviations won’t work anymore in insert mode.

You can think of `CTRL+G u` as creating chunks of undo.

- `:help ins-special-keys`
- `:help insert−index`

## Useful Keystrokes in Visual Mode

There are also interesting keystrokes you can hit in the different variants of VISUAL mode.

### Visual Mode and Visual Mode Linewise

- `o` - Move your cursor to the `o` pposite side of the selection (or the `o` ther end if you prefer). Doesn’t work in VISUAL mode linewise.
- `R` or `S` - Delete the selected lines and start INSERT mode.
- `U` - `U` ppercase the selection.
- `gv` - Switch back and forth between the previous selection and the current one.

Another tip: You can switch between VISUAL mode linewise and VISUAL mode blockwise *without coming back to NORMAL mode* with `CTRL+v` and `SHIFT+v`.

### Visual Mode Blockwise

- `o` - Move to the `o` pposite corner of the selection.
- `O` - Move to the `o` pposite side of the selection.
- `I` - `I` nsert some content at the beginning of every line selected.
- `A` - `A` ppend some content on every line selected after the highlighted area.
- `$A` - `A` ppend some content at the end of every line selected.
- `c` - Delete selected lines and begin INSERT mode *on every line*.
- `:help visual-index`
- `:help blockwise-operators`

## Vim Regular Expressions

We’re now at the crux of this article: Vim’s regexes are really powerful for searching in your content or transforming it. As a Venerable Vim Adept, you need to harness its power.

This section won’t go into the details of regexes in general. I assume that you know your basic metacharacters. If not, I’ve [written another article about them](https://thevaluable.dev/regular-expression-basics-vim-grep/). I’ve also recorded [videos about the basics of regexes using Grep](https://www.youtube.com/watch?v=LIVBktatfQI&list=PLRU13thWaP5kNYXveE9iF8aoEOlp4lgwN&index=2) (with exercises) if you’re interested to learn more about them. It’s not that hard, and the benefits are huge.

If you know already some “Perl style” regex engines like PCRE (the Perl regex engine, implemented in many tools and programming languages), you won’t be too much surprised by Vim’s regexes. The basics are the same, even if Vim introduces original concepts which are… interesting? If you want to quickly see the differences between Perl’s regexes and Vim’s ones, you’ll find a summary by running `:help perl-patterns`.

In this article, I call “metacharacter” any character which has semantics: for example, the semantics for `^` is “beginning of the line”.

### The Concept of Atom

You’ll see often this confusing notion of *atom* in Vim’s help. It’s just any metacharacter or group of metacharacters matching one character. For example, `[A-Z]` is an atom because it matches only one character from `A` to `Z`.

### Magic and Nomagic

As we saw quickly in the [previous article](https://thevaluable.dev/vim-advanced/), Vim’s regexes can have four different levels of magic: *Very magic*, *magic*, *nomagic*, and *very nomagic*. My advice in this madness: remember that *very magic* will allow you to use every regex metacharacter without escaping them, and that *very nomagic* oblige you to escape these metacharacters to use them.

The level of magic is set with the option `magic`. You might be tempted to change its value; please don’t. Every plugin out there expect this option set to `magic`. Instead, we’ll see different ways to change the magic level for each regex.

Because everybody has the level of magic set to “magic”, you’ll see many Vim regexes out there with a tonne of backslash to escape *some* metacharacters. That’s why Vim’s regexes often look so ugly, confusing, and hard to read. I propose this simple rule:

- When you need a regex, use “very magic” by adding `\v` before your pattern.
- When you don’t need a regex, use “very nomagic” by adding `\V` before your pattern.

For example, `:%s/\v(emacs)/\1 is bad/` will work flawlessly.

If you’re curious what level of magic allows what metacharacter, take a look at `:help \magic`. You’ll be granted with a wonderful table nobody remembers.

### Character Classes

Similarly to other regex engines, you’ll have access to many character classes in Vim. You’ll need to use the backslash preceding them whatever the level of magic you use.

#### Useful Character Classes

Here are the character classes I find the most useful:

- `\s` or `[:blank:]` - whitespace characters.
- `[A-Z]` or `\u` or `[:upper:]` - Uppercase.
- `[a-z]` or `\l` or `[:lower:]` - Lowercase.
- `[0-9]` or `\d` or `[:digit:]` - Digits.
- `\_` - Character class with end of line included.

For example, to illustrate a bit more the last one, if you want to include uppercase characters *and* line breaks in your regex, you can use `\_u`.

Most of the time, you can use the uppercase version of the character class to negate it. For example, `\L` is equivalent to `[^a-z]` (every character except the characters in the range `a` to `z`).

#### Character Classes Set Via Options

These character classes are interesting because you can change the characters they can match by changing the value of an option:

- `\f` - Filename characters (option `isfname`)
- `\i` - Identifier characters (option `isident` option)
- `\k` - Keyword character (option `iskeyword`)
- `\p` - Printable character (option `isprint`)

Changing these options can have consequences: they are sometimes used for other commands or keystrokes. For example, the keystroke `gf` use `isfname` under the hood.

Another tip: if you see for example the value `48-57` in these options, it means the ASCII characters from 48 to 57, which are the numbers from 0 to 9.

### Zero-width

A zero-width lookaround assertion allows you to match a pattern looking forward of backward without adding it to the match. As a result, these metacharacters don’t match any character by themselves. For example, `^` and `$` are zero-width.

If you try to substitute them, you won’t replace anything because there is nothing to replace. Instead, you’ll insert some text. To understand that, you can try to run `:%s/^/->` in a buffer for example.

You’ll need to use the backslash for these metacharacters whatever the level of magic you’re using. Here are the ones which might be useful:

- `\zs` - Only match your pattern if what’s before the metacharacter `\zs` match what’s before your pattern.
- `\ze` - Only match your pattern if what’s after the metacharacter `\ze` match what’s after your pattern.
- `\<` - Match the beginning of a word.
- `/>` - Match the end of a word.
- `\%^` - Match the beginning of the file.
- `\%$` - Match the end of the file.
- `\%V` - Match inside the visual selection (or the previous one if you’re not in VISUAL mode).

For example, in COMMAND-LINE mode after hitting `/` for searching:

- `\v^\s+\zsfor` - Only match `for` if there are one or more whitespace before the pattern.
- `\<if\>` - Only match the word `if` and not the substring `if` in `cliff` for example.
- `end\%$` - Only match the pattern `end` if it’s just before the end of the current file.

Another concrete example: I’m using [Zsh](https://thevaluable.dev/zsh-install-configure-mouseless/) to edit command lines in Vim and I often end up with the following when I want to rename a file:

```sh
mv my-file-name.jpg my-file-name.jpg
```

The goal is to replace the hyphen `-` with underscores `_` in the filename `my-file-name.jpg`. I could:

1. Switch to VISUAL mode
2. Select the second `my-file-name.jpg`
3. Run the following:

```sh
:'<,'>s/-/_/g
```

But it doesn’t work. My substitute will replace *every hyphen on the line* thanks to the `g` flag, and, if I don’t use it, I only replace *the first hyphen on the line*.

To solve the problem, I can use `\%V`:

```sh
:'<,'>s/\%V-/_/g
```

It works as expected because the pattern only match what’s inside the selection I’ve made.

### Regexes and Marks

What about using marks in our regexes?

`\%<'m` - Matches before the position of mark m.`\%>'m` - Match after the position of mark m.

For example, `/\%>'mcat\%<'a` search the pattern `cat` between the mark `m` and `a`.

If you want to dive more into Vim’s regex engine, [this article should answer your need](https://thevaluable.dev/vim-regular-expressions-in-depth/).

- `:help regex`
- `:help /magic`
- `:help holy-grail`
- `:help pattern`
- `:help pattern-atoms`
- `:help pattern-overview`

## Using Your Shell Commands in Vim

Vim is powerful by itself, but coupling Vim with the shell is switching your life’s GODLIKE mode. Additionally, if your development environment is built around the shell and your tools allow you to stay as much as you can on your keyboard, you’ll be unstoppable.

If you want to build a complete Mouseless Development Environment, [you might be interested by this book](https://themouseless.dev/).

### Executing External Command

Here are the commands you can use to summon the Unfathomable Power of The Shell®:

- `:! <cmd>` - Execute the shell command `<cmd>`.
- `:!!` - Repeat the last command executed.

For example, We saw in this article that we can look at the ASCII table if we run `man ascii` in a shell. Now, you can look at it directly in Vim with `:!man ascii`.

What about inserting the output of a shell command in your buffer?

- `:read! <cmd>` or `:r! <cmd>` - Execute the command `<cmd>` and insert the output in the current buffer.
- `:read!!` or `:r!!`\- Repeat the last command executed and insert the output in the current buffer.

Now, everybody in the universe can feel your brain radiating with The Power.

- `:help :!`
- `:help :read!`

### Filter

Did you ever dream, during the warm summer nights, about feeding the lines of your Vim buffers into the input stream of your favorite command, and replace these lines with the resulting output?

Your dream will become a reality. Using `:!` with a range will help you fulfill your destiny. For example, you could:

1. Select a couple of lines in VISUAL mode
2. Run `:'<,'>!grep <pattern>`

Every line without the pattern `<pattern>` will disappear in a magical cloud. Show that to your friends, your family, or your boss, and they’ll respect you forever.

This functionality is called “filter”, but it’s quite misleading to me. If I use `1,10:!sort`, it won’t filter anything, it will replace the input I gave to `sort` and it will replace it with the output.

`:help filter`

## Folding

A good way to manage complexity is to hide what we don’t need. In that regard, folding can be handy for complex codebases and long files.

### Choosing Your Fold Method

The value of the option `foldmethod` will determine how you want to manage your folds. There are 6 in total:

- `manual` - You manually define folds with the commands below.
- `indent` - Folds are created depending on the indentation level.
- `expr` - Folds are created depending on a Vimscript expression defined in `foldexpr`.
- `syntax` - Fold are created depending on the syntax highlighting (if the syntax highlighting defines them).
- `diff` - Fold unchanged text.
- `marker` - Fold depending on markers.

For the foldmethod `marker`, here’s an example I use in my `.vimrc`:

```vim
" Install Plugins ---------------------- {{{

"

" Some config here

"

" }}}

" Plugins Config ---------------------- {{{

"

" Some config here

"

" }}}
```

If you forgot how to set and unset options, I cover that in the [first article of the series](https://thevaluable.dev/vim-beginner/).

### Keystrokes

All these keystrokes begins with `z`. When you look at this wonderful letter, you can let your imagination going into foreign worlds and see a fold. Folded: `-`. Unfolded: `z`. Think about unfolding an old manuscript full of hidden Vim knowledge. Impressed? Me too.

#### Creating and Deleting Folds

These keystrokes only work if your foldmethod is set to `manual` or `marker`.

- `zf` - Create a `f` old. It can be used in VISUAL mode or with a motion.
- `zd` - `d` elete the fold under the cursor (but not the nested ones).
- `zD` - `D` elete the fold under the cursor, including the nested ones.
- `zE` - `E` liminate every fold in the window. It deletes the markers if your foldmethod is set to `marker`. Brutal.

#### Opening and Closing Folds

- `zo` - `o` pen the fold under the cursor.
- `zc` - `c` lose the fold under the cursor.
- `za` - Toggle the fold under the cursor (close it if it’s open, open it if it’s close).
- `zx` - Undo opened and closed folds.

Uppercase variants of these keystrokes (`zO` for example) can be used to propagate the action to every nested fold.

#### Opening and Closing All Folds

- `zM` - Close all folds
- `zR` - Open all folds
- `zi` - Toggle the use of folds (option `foldenable`).

#### Moving Through Folds

- `[z` - Move to the start of the current fold.
- `]z` - Move to the end of the current fold.
- `zj` - Move downward to the start of the next fold.
- `zk` - Move upward to the start of the next fold.

### Commands

You can also use these commands to manipulate folds. Each of them accept a range as prefix.

- `:foldopen` or `foldo` - Open folds.
- `:foldclose` or `foldc` - Close folds.
- `:folddoopen <cmd>` or `:foldd <cmd>` - Execute command `<cmd>` on all opened fold.
- `:folddoclosed <cmd>` or `:folddoc <cmd>` - Execute command `<cmd>` on all closed fold

Using a bang `!` for the first two ones (`foldo!` and `foldc!`) will open or close all nested folds too.

- `:help Folding`
- `:help fold-methods`
- `:help fold-commands`

## Are We There Yet

Suddenly, Dave woke up in his bed. This was all a dream! The hooded figures, the telepathic Vim course, everything! But he has now a lot of knowledge about Vim he didn’t have before falling asleep. Was it real? Was it a dream? Is our reality just a dream? Are we part of a weird Sim-like simulation? Are raspberries better than strawberries?

So many questions, so few answers! At least, we learned together the following:

- We can have access to 10 global quickfix lists, and 10 location lists per window.
- The NORMAL mode is powerful, but many useful keystrokes wait for our fingers to type them in INSERT and VISUAL modes.
- Vim regular expressions can be more or less “magic”, deciding what metacharacter you can use in your patterns without escaping them.
- An atom in Vim regexes is any pattern matching one character.
- Zero-width metacharacters don’t match any character but help you narrow down your match depending on its context.
- You can use marks in your regexes too.
- You can run any shell command with `:!`.
- You can spit output of shell commands in Vim with `:read`.
- Folding can be useful when you’ve too much content on your screen.
- Folding can also be used to apply a specific command on folded lines with `:foldd` and `:folddoc`.

This is not over. More discoveries will be made in the Name of Vim, and we’ll all get Its Highest Power to build new applications which will save the world.
