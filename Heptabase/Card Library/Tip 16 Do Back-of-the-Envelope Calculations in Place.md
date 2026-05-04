## Tip 16 Do Back-of-the-Envelope Calculations in Place

The expression register allows us to perform calculations and then insert the result directly into our document. In this tip, we'll see one application for this powerful feature.

Most of Vim's registers contain text either as a string of characters or as entire lines of text. The delete and yank commands allow us to set the contents of a register, while the put command allows us to get the contents of a register by inserting it into the document.

The expression register is different. It can evaluate a piece of Vim script code and return the result. Here, we can use it like a calculator. Passing it a simple arithmetic expression, such as 1+1, gives a result of 2. We can use the return value from the expression register just as though it were a piece of text saved in a plain old register.

The expression register is addressed by the = symbol. From Insert mode we can access it by typing <C-r>=. This opens a prompt at the bottom of the screen where we can type the expression that we want to evaluate. When done, we hit <CR>, and Vim inserts the result at our current position in the document.

Suppose that we've just typed the following:

[insert_mode/back-of-envelope.txt](http://media.pragprog.com/titles/dnvim2/code/insert_mode/back-of-envelope.txt)
6 chairs, each costing $35, totals $
There's no need to scribble on the back side of an envelope. Vim can do the math for us, and we don't even have to leave Insert mode. Here's how:
KeystrokesBuffer Contents

A

 6 chairs, each costing $35, totals $
<C-r>=635<CR>
6 chairs, each costing $35, totals $210

The expression register is capable of much more than simple arithmetic. We'll meet a slightly more advanced example in Tip 71.