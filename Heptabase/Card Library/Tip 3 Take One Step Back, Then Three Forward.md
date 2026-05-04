# Tip 3 Take One Step Back, Then Three Forward

# Tip 3 Take One Step Back, Then Three Forward

We can pad a single character with two spaces (one in front, the other behind) by using an idiomatic Vim solution. At first it might look slightly odd, but the solution has the benefit of being repeatable, which allows us to complete the task effortlessly.

Suppose that we have a line of code that looks like this:

[the_vim_way/3_concat.js](http://media.pragprog.com/titles/dnvim2/code/the_vim_way/3_concat.js)
var foo = "method("+argument1+","+argument2+")";
Concatenating strings in JavaScript never looks pretty, but we could make this a little easier on the eye by padding each + sign with spaces to make it look like this:
var foo = "method(" + argument1 + "," + argument2 + ")";

## Make the Change Repeatable

This idiomatic approach solves the problem:

KeystrokesBuffer Contents{start} var foo = "method("+argument1+","+argument2+")"; f+ var foo = "method("+argument1+","+argument2+")"; s

![](images/000002.gif)

\+

![](images/000002.gif)

<Esc> var foo = "method(" + argument1+","+argument2+")"; ; var foo = "method(" + argument1+","+argument2+")"; . var foo = "method(" + argument1 + ","+argument2+")"; ;. var foo = "method(" + argument1 + "," + argument2+")"; ;. var foo = "method(" + argument1 + "," + argument2 + ")";
The s command compounds two steps into one: it deletes the character under the cursor and then enters Insert mode. Having deleted the + sign, we then type 

![](images/000002.gif)

\+

![](images/000002.gif)

 and leave Insert mode.

One step back and then three steps forward. It's a strange little dance that might seem unintuitive, but we get a big win by doing it this way: we can repeat the change with the dot command; all we need to do is position our cursor on the next + symbol, and the dot command will repeat that little dance.

## Make the Motion Repeatable

There's another trick in this example. The f{char} command tells Vim to look ahead for the next occurrence of the specified character and then move the cursor directly to it if a match is found (see f[ⓘ](http://vimhelp.appspot.com/motion.txt.html#f)). So when we type f+, our cursor goes straight to the next + symbol. We'll learn more about the f{char} command in Tip 50.

Having made our first change, we could jump to the next occurrence by repeating the f+ command, but there's a better way. The ; command will repeat the last search that the f command performed. So instead of typing f+ four times, we can use that command once and then follow up by using the ; command three times.

## All Together Now

The ; command takes us to our next target, and the . command repeats the last change, so we can complete the changes by typing ;. three times. Does that look familiar?

Instead of fighting Vim's modal input model, we're working with it, and look how much easier it makes this particular task.

---

[Chapter 1 The Vim Way.md](Chapter%201%20The%20Vim%20Way.md)