# Tip 2 Don't Repeat Yourself

# Tip 2 Don't Repeat Yourself

For such a common use case as appending a semicolon at the end of a series of lines, Vim provides a dedicated command that combines two steps into one.

Suppose that we have a snippet of JavaScript code like this: [the_vim_way/2_foo_bar.js](http://media.pragprog.com/titles/dnvim2/code/the_vim_way/2_foo_bar.js) var foo = 1 var bar = 'a' var foobar = foo + bar

We need to append a semicolon at the end of each line. Doing so involves moving our cursor to the end of the line and then switching to Insert mode to make the change. The $ command will handle the motion for us, and then we can run a;<Esc> to make the change.

To finish the job, we could run the exact same sequence of keystrokes on the next two lines, but that would be missing a trick. The dot command will repeat that last change, so instead of duplicating our efforts, we could just run j$. twice. One keystroke (.) buys us three (a;<Esc>). It's a small saving, but these efficiencies accumulate when repeated.

But let's take a closer look at this pattern: j$.. The j command moves the cursor down one line, and then the $ command moves it to the end of the line. We've used two keystrokes just to maneuver our cursor into position so that we can use the dot command. Do you sense that there's room for improvement here?

## Reduce Extraneous Movement

While the a command appends after the current cursor position, the A command appends at the end of the current line. It doesn't matter where our cursor is at the time, pressing A will switch to Insert mode and move the cursor to the end of the line. In other words, it squashes $a into a single keystroke. In Two for the Price of One, we see that Vim has a handful of compound commands.

Two for the Price of One
We could say that the A command compounds two actions ($a) into a single keystroke. It's not alone in doing this. Many of Vim's single-key commands can be seen as a condensed version of two or more other commands. The table below shows an approximation of some examples. Can you identify anything else that they all have in common?

| Compound | Command | Equivalent in Longhand | 
|---|---|---|
|  |  |  | 

C

c$

s

cl

S

^C

I

^i

A

$a

o

A<CR>

O

ko

If you catch yourself running ko (or worse, k$a<CR>), stop! Think about what you're doing. Then recognize that you could have used the O command instead.

Did you identify the other property that these commands share? They all switch from Normal to Insert mode. Think about that and how it might affect the dot command.

Here is a refinement of our previous example:
KeystrokesBuffer Contents
{start}
var foo = 1 var bar = 'a' var foobar = foo + bar
A;<Esc>
var foo = 1; var bar = 'a' var foobar = foo + bar
j
var foo = 1; var bar = 'a' var foobar = foo + bar
.
var foo = 1; var bar = 'a'; var foobar = foo + bar
j.
var foo = 1; var bar = 'a'; var foobar = foo + bar;

By using A instead of $a, we give the dot command a boost. Instead of having to position the cursor at the end of the line we want to change, we just have to make sure it is somewhere (anywhere!) on that line. Now we can repeat the change on consecutive lines just by typing j. as many times as it takes.

One keystroke to move, another to execute. That's about as good as it gets! Watch for this pattern of usage, because we'll see it popping up in a couple more examples.

Although this formula looks terrific for our short example, it's not a universal solution. Imagine if we had to append a semicolon to fifty consecutive lines. Pressing j. for each change starts to look like a lot of work. For an alternative approach, skip ahead to Tip 30.

---

[Chapter 1 The Vim Way.md](Chapter%201%20The%20Vim%20Way.md)