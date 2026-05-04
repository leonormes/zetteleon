# Tip 68 Repeat a Change on Contiguous Lines

Tip 68 Repeat a Change on Contiguous Lines

We can make light work out of repeating the same set of changes on a range of lines by recording a macro and then playing it back on each line. There are two ways to do this: executing the macro in series or in parallel.

As a demonstration, we'll transform this snippet of text: [macros/consecutive-lines.txt](http://media.pragprog.com/titles/dnvim2/code/macros/consecutive-lines.txt) 1\. one 2. two 3. three 4. four

We'll make it look like this:

1. One 2) Two 3) Three 4) Four
   The task may look trivial, but it presents a couple of interesting challenges.

# Record One Unit of Work

To begin, we record all changes made to the first line:
KeystrokesBuffer Contents
qa

1. one 2. two
   0f.

2. one 2. two
   r)

3. one 2. two
   w\~

4. One 2. two
   j

5. One 2. two
   q

6. One 2. two

Note the use of motions in this macro. We begin with the 0 command, which normalizes our cursor position by placing it at the start of the line. This means that our next motion always starts from the same place, making it more repeatable.

Some might look at the next motion, f., and consider it wasteful. It moves the cursor only one step to the right, same as the l command. Why use two keystrokes when one would do?

Once again, it's a matter of repeatability. In our sample set, we have lines numbered only one to four, but suppose the numbers ran into double digits?

1. one 2. two ... 10. ten 11. eleven
   On the first nine lines, 0l takes us to the second character of the line, which happens to be a period. But from line ten onward, that motion stops short of the target, whereas f. works on all of these lines and would continue to work into triple digits and beyond.

Using the f. motion also adds a safety catch. If no . characters are found on the current line, the f. command raises an error and macro execution aborts. We'll exploit this later, so keep that thought at the back of your mind.

# Execute Macro in Series

We can execute the macro we just recorded by pressing @a. This carries out the following steps: jump to the first . character on the line, change it to ), uppercase the first letter of the next word, and finish by advancing to the next line.

We could invoke the @a command three times to complete the task, but running 3@a is quicker:
KeystrokesBuffer Contents
{start}

1. One 2. two 3. three 4. four
   3@a

2. One 2) Two 3) Three 4) Four

Let's introduce a new obstacle. Suppose our file contains comments.

[macros/broken-lines.txt](http://media.pragprog.com/titles/dnvim2/code/macros/broken-lines.txt)

1. one 2. two // break up the monotony 3. three 4. four
   Now watch what happens if we attempt to replay the same macro on this file.
   KeystrokesBuffer Contents
   {start}

2. one 2. two // break up the monotony 3. three 4. four
   5@a

3. One 2) Two // break up the monotony 3. three 4. four

The macro stalls on line three---the one containing the comment. When the f. command is executed, it finds no . characters and the macro aborts. We've tripped the safety catch, and it's a good thing too. If the macro had successfully executed on this line, then it would have made changes that were probably unwanted.

But we are left with a problem. We asked Vim to execute the macro five times, and it bailed out on the third repetition. So we have to invoke it again on the next lines to complete the job. Let's look at an alternative technique.

# Execute Macro in Parallel

The Tip 30, Demonstrated a Method for Running the Dot Command on a Series of Consecutive Lines. We Can Apply the Same Technique here

KeystrokesBuffer Contents
qa

1. one
   0f.r)w\~

2. One
   q

3. One
   jVG

4. One 2. two // break up the monotony 3. three 4. four
   :'<,'>normal @a

5. One 2) Two // break up the monotony 3) Three 4) Four

We've re-recorded the macro from scratch. This one is almost identical, except that we've omitted the final j command to advance to the next line. We won't be needing it this time.

The :normal @a command tells Vim to execute the macro once for each line in the selection. Just as before, the macro succeeds on the first two lines and then aborts on line three, but it doesn't stall there this time---it completes the job. Why?

Previously, we queued up five repetitions in series by running 5@a. When the third iteration aborted, it killed the remaining items in the queue. This time, we've lined up five iterations in parallel. Each invocation of the macro is independent from the others. So when the third iteration fails, it does so in isolation.

# Deciding: Series or Parallel

Which is better, series or parallel? The answer (as always): it depends.

Executing a macro on multiple items in parallel is more robust. In this scenario, it's the better solution. But if we raise an error when we execute a macro, maybe we want those alarms to go off. Executing a macro on multiple items in series makes it clear when and where any errors occur.

Learn both techniques, and you'll develop a knack for knowing which one is right for the occasion.

---

[Chapter 11 Macros.md](Chapter%2011%20Macros.md)