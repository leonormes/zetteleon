# Tip 70 Act Upon a Collection of Files

Tip 70 Act Upon a Collection of Files

So far, we've stuck to tasks that were repeated in the same file, but we can play back a macro across a collection of files. Once again, we'll consider how to execute the macro in parallel and in series.

Let's start with a set of files that look something like this:

[macros/ruby_module/animal.rb](http://media.pragprog.com/titles/dnvim2/code/macros/ruby_module/animal.rb)

 ...\[end Of Copyright notice\] Class Animal # Implementation End

We'll wrap the class in a module to end up with this:

 ...\[end Of Copyright notice\] Module Rank Class Animal # Implementation... End End

# Preparation

Source these lines of configuration to reproduce the examples in this tip:

[macros/rc.vim](http://media.pragprog.com/titles/dnvim2/code/macros/rc.vim)
set nocompatible filetype plugin indent on set hidden if has("autocmd") autocmd FileType ruby setlocal ts=2 sts=2 sw=2 expandtab endif
The 'hidden' option is discussed in more depth in Enable the 'hidden' Setting Before Running ':do' Commands.

If you'd like to follow along, consult Downloading the Examples. The folder code/macros/ruby_module contains the files we'll be working with.

# Build a List of Target Files

Let's stake out the terrain by building a list of the files that we want to act upon. We'll keep track of them using the argument list (for more details, see Tip 38):
=> :cd code/macros/ruby_module=> :args .rb
Running :args without arguments reveals the contents of the list:
=> :args<= \[animal.rb\] banker.rb frog.rb person.rb
We can navigate through this list of files using :first, :last, :prev, and :next.

# Record a Unit of Work

Before we begin, let's make sure we're at the start of the arguments list:
=> :first
Now let's record a macro that performs the necessary work:
KeystrokesBuffer Contents
qa

 ...\[end Of Copyright notice\] Class Animal # Implementation... End

gg/class<CR>

 ...\[end Of Copyright notice\] Class Animal # Implementation... End

Omodule Rank<Esc>

 ...\[end Of Copyright notice\] Module Rank Class Animal # Implementation... End

j>G

 ...\[end Of Copyright notice\] Module Rank Class Animal # Implementation... End

Goend<Esc>

 ...\[end Of Copyright notice\] Module Rank Class Animal # Implementation... End End

q

 ...\[end Of Copyright notice\] Module Rank Class Animal # Implementation... End End

Each of these files begins with a copyright notice, so we have to take care to properly normalize the cursor position. Pressing gg places the cursor at the start of the file, and /class<CR> jumps forwards to the first occurrence of the word "class." Having made these preparatory steps, we can now proceed to make the changes.

We use the O command to open a new line above the cursor, inserting the new text. Then we advance our cursor to the next line, where we use the >G command to indent each line up to the end of the file. Finally, we jump to the end of the file by pressing G and then using the o command to create a new line below the cursor, inserting the end keyword there.

If you're following along with your editor, try to resist the urge to save your changes to the file by running :w. We'll see why in a moment.

# Execute the Macro in Parallel

The :argdo command allows us to execute an Ex command once for each buffer in the argument list (see :argdo[ⓘ](%3Chttp://vimhelp.appspot.com/editing.txt.html#%3Aargdo%3E)). But if we were to run :argdo normal @a right now, there would be side effects.

Think about it. Running :argdo normal @a executes the macro that we just recorded in all of the buffers in the argument list, including the first one: the one that we changed as we recorded the macro. As a result, the first buffer gets wrapped in a module twice over.

To prevent this, we'll revert all of the changes we just made to the first buffer in the argument list by running :edit! (see :edit

![](http://vimhelp.appspot.com/editing.txt.html#%3Aedit%21)

):
=> :edit!
If you had already written the changes to a file, then :edit! won't work. In this case, you could just use the u command repeatedly until the file looked as it did when you opened it.

Now we can go ahead and execute the macro in all of the buffers in the argument list:
=> :argdo normal @a
This technique takes a bit of setup, but that one command does a lot of work for us. Now let's see how we could adapt this macro to run in series.

# Execute the Macro in Series

Our macro performs a single unit of work on a single buffer. If we want to make it act upon multiple buffers, we could append a final step that advances to the next buffer in the list. (See Table 12, Executing the Macro in Series.)

Table 12. Executing the Macro in Series
KeystrokesBuffer Contents
qA
module Rank class Animal # implementation... end end
:next
class Banker # implementation... end
q
class Banker # implementation... end
22@a
module Rank class Person # implementation... end end

While we could run 3@a to execute the macro on each of the remaining files in the buffer list, there's no need to be so precise about it. When we reach the last buffer in the argument list, the :next command fails and the macro aborts. So, rather than specifying an exact count, we only have to ensure that we provide a number that's large enough: 22 will do, and it's easy to type.

# Save Changes to All Files

We've changed four files, but we haven't saved any of them yet. We could run :argdo write to save all files in the argument list, but it would be quicker simply to run this:
=> :wall
Note that this saves all files in the buffer list, so it's not exactly equivalent to :argdo write (see :wa[ⓘ](%3Chttp://vimhelp.appspot.com/editing.txt.html#%3Awa%3E)).

Another useful command is :wnext (see :wn[ⓘ](%3Chttp://vimhelp.appspot.com/editing.txt.html#%3Awn%3E)), which is equivalent to running :write followed by :next. If you are executing a macro in series across several files in the argument list, you may prefer to use this.

# Discussion

Suppose that something caused the macro to fail while executing on the third buffer in the argument list. If we were using the :argdo normal @a command, then the macro would fail only in that one buffer, whereas if we executed the macro in series by using a count, then it would abort, and any items that follow in the argument list would be left unchanged.

We've already seen this effect in Tip 68. But the consequences are slightly different this time. When we performed the same task on a block of adjacent lines, we could see everything at a glance. If anything went wrong, it was there right in front of our eyes.

This time we're working on a set of files, so we can't see everything in a single glance. If we execute the macro in series and it fails, then it will halt at the place where the error occurs, whereas if we execute the macro in parallel and it fails, we'll have to browse through the argument list until we find the buffer where the error was raised.

In the case where an error is raised, running the macro in parallel may complete the job faster, but it conceals useful information.

---

[Chapter 11 Macros.md](Chapter%2011%20Macros.md)