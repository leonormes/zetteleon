# Tip 71 Evaluate an Iterator to Number Items in a List

Tip 71 Evaluate an Iterator to Number Items in a List

Being able to insert a value that changes for each execution of a macro can be useful. In this tip, we'll learn a technique for incrementing a number as we record a macro so that we can insert the numbers 1 to 5 on consecutive lines.

Suppose that we want to create a numbered list from a series of items on adjacent lines. To demonstrate, we'll start with this text: [macros/incremental.txt](http://media.pragprog.com/titles/dnvim2/code/macros/incremental.txt) partridge in a pear tree turtle doves French hens calling birds golden rings

We'll transform it to look like this:

1. partridge in a pear tree 2) turtle doves 3) French hens 4) calling birds 5) golden rings
   We've already learned a couple of ways to make Vim perform simple arithmetic. We can either use the <C-a> and <C-x> commands with a count (see Tip 10), or we can use the expression register (see Tip 16). For this solution, we'll use the expression register with a touch of Vim script.

# Rudimentary Vim Script

Let's begin by stepping through a few simple command-line invocations. Using the let keyword, we can create a variable called i and assign it a value of 0. The :echo command allows us to inspect the current value assigned to a variable.
=> :let i=0=> :echo i<= 0
We can increment the value of i:
=> :let i += 1=> :echo i<= 1
The :echo command is fine for revealing the value that is assigned to a variable, but ideally we want to insert that value into the document. We can do that using the expression register. In Tip 16, we saw that the expression register can be used to do simple sums and to insert the result into the document. We can insert the value stored in variable i just by running <C-r>=i<CR> in Insert mode.

# Record the Macro

Now let's put all of this together:
KeystrokesBuffer Contents
:let i=1
partridge in a pear tree
qa
partridge in a pear tree
I<C-r>=i<CR>) <Esc>

1. partridge in a pear tree
   :let i += 1

2. partridge in a pear tree
   q

3. partridge in a pear tree

Before we begin recording the macro, we set the variable i to 1. Inside the macro, we use the expression register to insert the value stored in i. Then, before we finish recording the macro, we increment the value stored in the variable, which should now contain the value 2.

# Execute the Macro

We can then play it back for the remaining lines.
KeystrokesBuffer Contents
{start}

1. partridge in a pear tree turtle doves French hens calling birds golden rings
   jVG

2. partridge in a pear tree turtle doves French hens calling birds golden rings
   :'<,'>normal @a

3. partridge in a pear tree 2) turtle doves 3) French hens 4) calling birds 5) golden rings

The :normal @a command tells Vim to execute the macro on each of the selected lines (see Execute Macro in Parallel). The value of i is 2 to begin with, but it gets incremented each time the macro executes. The end result is that each line is prefixed with consecutive digits.

We could also use the yank, put, and <C-a> commands to accomplish this same task. Try it yourself for exercise!

---

[Chapter 11 Macros.md](Chapter%2011%20Macros.md)