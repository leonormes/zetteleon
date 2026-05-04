## Tip 19 Overwrite Existing Text with Replace Mode

Replace mode is identical to Insert mode, except that it overwrites existing text in the document.

Suppose that we had an excerpt of text such as this: [insert_mode/replace.txt](http://media.pragprog.com/titles/dnvim2/code/insert_mode/replace.txt) Typing in Insert mode extends the line. But in Replace mode the line length doesn't change.

Instead of using two separate sentences, we're going to run this together into a single sentence by changing the period to a comma. We also have to downcase the "B" in the word "But." This example shows how we could do this using Replace mode.
KeystrokesBuffer Contents
{start}
Typing in Insert mode extends the line. But in Replace mode the line length doesn't change.
f.
Typing in Insert mode extends the line. But in Replace mode the line length doesn't change.
R,

![](images/000002.gif)

b<Esc>
Typing in Insert mode extends the line, but in Replace mode the line length doesn't change.

From Normal mode, we can engage Replace mode with the R command. As the example demonstrates, typing ", b" overwrites the existing ". B" characters. And when we're finished with Replace mode, we can hit the <Esc> key to return to Normal mode. Not all keyboards have an <Insert> key, but if yours does, then you can use it to toggle between Insert and Replace modes.

### Overwrite Tab Characters with Virtual Replace Mode

Some characters can complicate matters for Replace mode. Consider the tab character. This is represented by a single character in the file, but onscreen it expands to fill several columns, as defined by the 'tabstop' setting (see 'tabstop'[ⓘ](http://vimhelp.appspot.com/options.txt.html#%27tabstop%27)). If we placed our cursor on a tab stop and initiated Replace mode, then the next character we typed would overwrite the tab character. Supposing that the 'tabstop' option was set to 8 (the default), this would appear to replace eight characters with one, causing a drastic reduction in the length of the current line.

Vim has a second variant of Replace mode. Virtual Replace mode is triggered with gR and treats the tab character as though it consisted of spaces. Suppose that we position the cursor on a tab stop spanning eight columns of screen real estate. If we switch to Virtual Replace mode, we could type up to seven characters, each of which would be inserted in front of the tab character. Finally, if we typed an eighth character, it would replace the tab stop.

In Virtual Replace mode, we overwrite characters of screen real estate rather than dealing with the actual characters that would eventually be saved in a file. This tends to produce fewer surprises, so I would recommend using Virtual Replace mode whenever possible.

Vim also provides a single-shot version of Replace mode and Virtual Replace mode. The r{char} and gr{char} commands allow us to overwrite a single character before switching straight back to Normal mode (r[ⓘ](http://vimhelp.appspot.com/change.txt.html#r)).