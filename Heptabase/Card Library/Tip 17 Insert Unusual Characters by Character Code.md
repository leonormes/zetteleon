## Tip 17 Insert Unusual Characters by Character Code

Vim can insert any character by its numeric code. This can be handy for entering symbols that are not found on the keyboard.

We can tell Vim to insert any arbitrary character if we know its numeric code. From Insert mode, we just have to type <C-v>{code}, where {code} is the address of the character that we want to insert.

Vim expects the numeric code to consist of three digits. Suppose, for example, that we wanted to insert an uppercase "A" character. The character code is 65, so we would have to enter it as <C-v>065.

But what if we wanted to insert a character whose numeric code is longer than three digits? For example, the Unicode Basic Multilingual Plane has an address space for up to 65,535 characters. It turns out that we can enter all of these using a four-digit hexadecimal code if we type <C-v>u{1234} (note the u preceding the digit this time). Let's say we wanted to insert an inverted question mark symbol ("¿"), which is represented by the character code 00bf. From Insert mode, we would just have to type <C-v>u00bf. See i_CTRL-V_digit[ⓘ](http://vimhelp.appspot.com/insert.txt.html#i_CTRL-V_digit) for more details.

If you want to find out the numeric code for any character in your document, just place the cursor on it and trigger the ga command. This outputs a message at the bottom of the screen, revealing the character code in decimal and hexadecimal notations (see ga[ⓘ](http://vimhelp.appspot.com/various.txt.html#ga)). Of course, this is of little help if you want to know the code for a character that is not already present in your document. In that case, you might want to look up the unicode tables.

In another scenario, if the <C-v> command is followed by any nondigit key, it will insert the character represented by that key literally. For example, if the 'expandtab' option is enabled, then pressing the <Tab> key will insert space characters instead of a tab character. However, pressing <C-v><Tab> will always insert a tab character literally, regardless of whether 'expandtab' is enabled or not.

Table 3, Inserting Unusual Characters, summarizes the commands for entering unusual characters.

Table 3. Inserting Unusual Characters
KeystrokesEffect
<C-v>{123}
Insert character by decimal code
<C-v>u{1234}
Insert character by hexadecimal code
<C-v>{nondigit}
Insert nondigit literally
<C-k>{char1}{char2}

Insert character represented by {char1}{char2} digraph