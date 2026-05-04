# Tip 65 Record and Execute a Macro

Tip 65 Record and Execute a Macro

Macros allow us to record a sequence of changes and then play them back. This tip shows how.

Many repetitive tasks involve making multiple changes. If we want to automate these, we can record a macro and then execute it.

# Capture a Sequence of Commands by Recording a Macro

The q key functions both as the "record" button and the "stop" button. To begin recording our keystrokes, we type q{register}, giving the address of the register where we want to save the macro. We can tell that we've done it right if the word "recording" appears in the status line. Every command that we execute will be captured, right up until we press q again to stop recording.

Let's see this in action:
KeystrokesBuffer Contents
qa
foo = 1 bar = 'a' foobar = foo + bar
A;<Esc>
foo = 1; bar = 'a' foobar = foo + bar
Ivar

![](images/000002.gif)

<Esc>
var foo = 1; bar = 'a' foobar = foo + bar
q
var foo = 1; bar = 'a' foobar = foo + bar

Pressing qa begins recording and saves our macro into register a. We then perform two changes on the first line: appending a semicolon and prepending the word var. Having completed both of those changes, we press q to stop recording our macro (q[ⓘ](http://vimhelp.appspot.com/repeat.txt.html#q)).

We can inspect the contents of register a by typing the following:
=> :reg a<= --- Registers --- "a A;^\[Ivar ^\[
It doesn't make for easy reading, but the same sequence of commands that we recorded moments ago should be recognizable. The only surprise might be that the symbol ^\[ is used to stand for the Escape key. See Keyboard Codes in Macros, for an explanation.

# Play Back a Sequence of Commands by Executing a Macro

The @{register} command executes the contents of the specified register (see @[ⓘ](http://vimhelp.appspot.com/repeat.txt.html#%40)). We can also use @@, which repeats the macro that was invoked most recently.

Here's an example:
KeystrokesBuffer Contents
{start}
var foo = 1; bar = 'a' foobar = foo + bar
j
var foo = 1; bar = 'a' foobar = foo + bar
@a
var foo = 1; var bar = 'a'; foobar = foo + bar
j@@
var foo = 1; var bar = 'a'; var foobar = foo + bar;

We've executed the macro that we just recorded, repeating the same two changes for each of the subsequent lines. Note that we use @a on the first line and then @@ to replay the same macro on the next line.

In this example, we played the macro back by running j@a (and subsequently j@@). Superficially, this has some resemblance to the Dot Formula. It involves one keystroke to move (j) and two to act (@a). Not bad, but there's room for improvement.

We have a couple of techniques at our disposal for executing a macro multiple times. The setup differs slightly for each technique, but more importantly, they react differently on encountering an error. I'll explain the differences by way of a comparison with Christmas tree lights.

If you buy a cheap set of party lights, the chances are that they will be wired in series. If one bulb blows, they all go out. If you buy a premium set, they're more likely to be wired in parallel. That means any bulb can go out, and the rest will be unaffected.

I've borrowed the expressions in series and in parallel from the field of electronics to differentiate between two techniques for executing a macro multiple times. The technique for executing a macro in series is brittle. Like cheap Christmas tree lights, it breaks easily. The technique for executing a macro in parallel is more fault tolerant.

# Execute the Macro in Series

Picture a robotic arm and a conveyor belt containing a series of items for the robot to manipulate.

![](images/000010.jpeg)

Recording a macro is like programming the robot to do a single unit of work. As a final step, we instruct the robot to move the conveyor belt and bring the next item within reach. In this manner, we can have a single robot carry out a series of repetitive tasks on similar items.

One consequence of this approach is that if the robot encounters any surprises, it sounds an alarm and aborts the operation. Even if items on the conveyor belt still need to be manipulated, the work stops.

# Execute the Macro in Parallel

When we execute the macro in parallel, it's as though we've dispensed with the conveyor belt entirely. Instead, we deploy an assemblage of robots,\[19\] all programmed to do the same simple task. Each is given a single job to do. If it succeeds, very well. If it fails, no matter.

Under the hood, Vim always executes macros sequentially, no matter which of these two techniques we use. The term in parallel is intended to draw an analogy with the robustness of parallel circuits. It is not meant to suggest that Vim executes multiple changes concurrently.

In Tip 68, as well as Tip 70, we'll see examples of a macro being executed both in series and in parallel.

---