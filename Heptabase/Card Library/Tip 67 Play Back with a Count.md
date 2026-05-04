# Tip 67 Play Back with a Count

# Tip 67 Play Back with a Count

Tip 67 Play Back with a Count

The Dot Formula can be an efficient editing strategy for a small number of repeats, but it can't be executed with a count. Overcome this limitation by recording a cheap one-off macro and playing it back with a count.

In Tip 3, we used the Dot Formula to transform this: [the_vim_way/3_concat.js](http://media.pragprog.com/titles/dnvim2/code/the_vim_way/3_concat.js) var foo = "method("+argument1+","+argument2+")";

What we want is for it to look like this:
var foo = "method(" + argument1 + "," + argument2 + ")";
The Dot Formula meant that we could complete the task simply by repeating ;. a few times. What if we faced the same problem but on a larger scale?
x = "("+a+","+b+","+c+","+d+","+e+")";
We can approach this in exactly the same way. But when we have to invoke the two commands ;. so many times to complete the job, it starts to feel like a lot of work. Isn't there some way that we could apply a count?

It's tempting to think that running 11;. would do the trick, but it's no use. This instructs Vim to run the ; command eleven times, and then the . command once. The equivalent mistake is more obvious if we run ;11., which tells Vim to invoke ; once and then . eleven times. We really want to run ;. eleven times.

We can simulate this by recording one of the simplest possible macros: qq;.q. Here, qq tells Vim to record the following keystrokes and save them to the q register. Then we type our commands ;. and finish recording the macro by pressing q one final time. Now we can execute the macro with a count: 11@q. This executes ;. eleven times.

Let's put all of that together.
KeystrokesBuffer Contents{start} x = "("+a+","+b+","+c+","+d+","+e+")"; f+ x = "("+a+","+b+","+c+","+d+","+e+")"; s + <Esc> x = "(" + a+","+b+","+c+","+d+","+e+")"; qq;.q x = "(" + a + ","+b+","+c+","+d+","+e+")"; 22@q x = "(" + a + "," + b + "," + c + "," + d + "," + e + ")";
The ; command repeats the f+ search. When our cursor is positioned after the last + character on the line, the ; motion fails and the macro aborts.

In our case, we want to execute the macro ten times. But if we were to play it back eleven times, the final execution would abort. In other words, we can complete the task so long as we invoke the macro with a count of ten or more.

Who wants to sit there and count the exact number of times that a macro should be executed? Not me. I'd rather give a count that I think is high enough to get the job done. I often use 22, because I'm lazy and it's easy to type. On my keyboard, the @ and 2 characters are entered with the same button.

Note that it won't always be possible to make approximations when providing a count to a macro. It works in this case because the macro has a built-in safety catch: the ; motion will fail if no more + symbols are left on the current line. See Abort When a Motion Fails, for more details.

---

[Chapter 11 Macros.md](Chapter%2011%20Macros.md)