# Tip 10 Use Counts to Do Simple Arithmetic

# Tip 10 Use Counts to Do Simple Arithmetic

Tip 10 Use Counts to Do Simple Arithmetic

Most Normal mode commands can be executed with a count. We can exploit this feature to do simple arithmetic.

Many of the commands that are available in Normal mode can be prefixed with a count. Instead of executing the command just once, Vim will attempt to execute the command the specified number of times (see count[ⓘ](http://vimhelp.appspot.com/intro.txt.html#count)).

The <C-a> and <C-x> commands perform addition and subtraction on numbers. When run without a count they increment by one, but if we prefix a number, then we can add or subtract by any whole number. For example, if we positioned our cursor on a 5 character, running 10<C-a> would modify it to read 15.

But what happens if the cursor is not positioned on a numeric digit? The documentation says that the <C-a> command will "add \[count\] to the number at or after the cursor" (see ctrl-a[ⓘ](http://vimhelp.appspot.com/change.txt.html#CTRL-A)). So if the cursor is not already positioned on a number, then the <C-a> command will look ahead for a digit on the current line. If it finds one, it jumps straight to it. We can use this to our advantage.

Here's a snippet of CSS: [normal_mode/sprite.css](http://media.pragprog.com/titles/dnvim2/code/normal_mode/sprite.css) .blog, .news { background-image: url(/sprite.png); } .blog { background-position: 0px 0px }

We're going to duplicate the last line and make two small modifications to it: replace the word "blog" with "news," and change "0px" to "-180px." We can duplicate the line by running yyp and then using cW to change the first word. But how should we deal with that number?

One approach would be to jump to the digit with f0 and then dip into Insert mode to change the value by hand: i-18<Esc>. But it's quicker just to run 180<C-x>. Since our cursor isn't on a digit to begin with, it jumps forward to the first one that it finds. That saves us the step of moving the cursor by hand. Let's see this work flow in action:
KeystrokesBuffer Contents
{start}
.blog, .news { background-image: url(/sprite.png); } .blog { background-position: 0px 0px }
yyp
.blog, .news { background-image: url(/sprite.png); } .blog { background-position: 0px 0px } .blog { background-position: 0px 0px }
cW.news<Esc>
.blog, .news { background-image: url(/sprite.png); } .blog { background-position: 0px 0px } .news { background-position: 0px 0px }
180<C-x>
.blog, .news { background-image: url(/sprite.png); } .blog { background-position: 0px 0px } .news { background-position: -180px 0px }

In this example, we've only duplicated the line once and made changes. But suppose we had to make ten copies, subtracting 180 from the number in each successive copy. If we were to switch to Insert mode to amend each number, we'd have to type something different each time (-180, then -360, and so on). But by using the 180<C-x> command, our work flow is identical for each successive line. We could even record our keystrokes as a macro (see Chapter 11, Macros) and then play it back as many times as needed.

Number Formats
What follows 007? No, this isn't a James Bond gag; I'm asking what result would you expect if you added one to 007.

If you answered 008, then you might be in for a surprise when you try using Vim's <C-a> command on any number with a leading zero. As is the convention in some programming languages, Vim interprets numerals with a leading zero to be in octal notation rather than in decimal. In the octal numeric system, 007 + 001 = 010, which looks like the decimal ten but is actually an octal eight. Confused?

If you work with octal numbers frequently, Vim's default behavior might suit you. If you don't, you probably want to add the following line to your vimrc:
set nrformats=
This will cause Vim to treat all numerals as decimal, regardless of whether they are padded with zeros.

---

[Chapter 2 Normal Mode.md](Chapter%202%20Normal%20Mode.md)