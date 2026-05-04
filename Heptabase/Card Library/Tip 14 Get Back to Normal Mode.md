## Tip 14 Get Back to Normal Mode

Insert mode is specialized for one task---entering text---whereas Normal mode is where we spend most of our time (as the name suggests). So it's important to be able to switch quickly between them. This tip demonstrates a couple of tricks that reduce the friction of mode switching.

The classic way of getting back to Normal mode is with the <Esc> key, but on many keyboards that can seem like a long reach. Alternatively, we can press <C-\[>, which has the same.

| Keystrokes | Effect | 
|---|---|
| <Esc> | Switch to Normal mode | 
| <C-\[> | Switch to Normal mode | 
| <C-o> | Switch to [Insert Normal mode.md](Insert%20Normal%20mode.md) | 

Vim novices frequently become fatigued by the constant need to switch modes, but with practice it starts to feel more natural. Vim's modal nature can feel awkward in one particular scenario: when we're in Insert mode and we want to run only one Normal command and then continue where we left off in Insert mode. Vim has a neat solution to ease the friction caused by switching modes: [Insert Normal mode.md](Insert%20Normal%20mode.md)

### Meet [Insert Normal mode.md](Insert%20Normal%20mode.md)

[Insert Normal mode.md](Insert%20Normal%20mode.md) is a special version of Normal mode, which gives us one bullet. We can fire off a single command, after which we'll be returned to Insert mode immediately. From Insert mode, we can switch to Insert Normal mode by pressing <C-o> (i_CTRL-O[ⓘ](http://vimhelp.appspot.com/insert.txt.html#i_CTRL-O)).

When the current line is right at the top or bottom of the window, I sometimes want to scroll the screen to see a bit more context. The zz command redraws the screen with the current line in the middle of the window, which allows us to read half a screen above and below the line we're working on. I'll often trigger this from Insert Normal mode by tapping out <C-o>zz. That puts me straight back into Insert mode so that I can continue typing uninterrupted.

Remap the Caps Lock Key
For Vim users, the Caps Lock key is a menace. If Caps Lock is engaged and you try using the k and j keys to move the cursor around, you'll instead trigger the K and J commands. Briefly: K looks up the man page for the word under the cursor (K[ⓘ](http://vimhelp.appspot.com/various.txt.html#K)), and J joins the current and next lines together (J[ⓘ](http://vimhelp.appspot.com/change.txt.html#J)). It's surprising how quickly you can mangle the text in your buffer by accidentally enabling the Caps Lock key!

Many Vim users remap the Caps Lock button to make it act like another key, such as <Esc> or <Ctrl>. On modern keyboards, the <Esc> key is difficult to reach, whereas the Caps Lock key is handy. Mapping Caps Lock to behave as an <Esc> key can save a lot of effort, especially since the <Esc> key is so heavily used in Vim. I prefer to map the Caps Lock button to behave instead as a <Ctrl> key. The <C-\[> mapping is synonymous with <Esc>, and it's easier to type when the <Ctrl> key is within easy reach. Additionally, the <Ctrl> key can be used for many other mappings, both in Vim and in other programs too.

The simplest way to remap the Caps Lock key is to do it at the system level. The methods differ on OS X, Linux, and Windows, so rather than reproducing instructions here for each system, I suggest that you consult Google. Note that this customization won't just affect Vim: it applies system-wide. If you take my advice, you'll throw away the Caps Lock key forever. You won't miss it, I promise.