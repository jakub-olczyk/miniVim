# miniVim

Basic text editor inspired by the classic Unix editor - Vi. It was written as
an assignment for 'Design patterns' class at univesity using:

* Python  `curses` module
* Vim - text editor :)

## Basic movements

To move around the buffer you should use standard Vi keys:

		    ^
	< h  j  k  l >
		 v

Jump movements are also implemented. If you are unfamiliar with those here's a
quick example:
(`^` marks the positon of the cursor):

	A line of simple text.
	  ^

After hitting `ww` the cursor will move to this position:

	A line of simple text.
	          ^
To put it in words the `w` command is used for jumping one word forward.

There is a way to move one word backwards - it is the `b` command.  Here's what
happens after hitting `b` once:

	A line of simple text.
	       ^

### Inserting text

Like in Vi there is a bunch of commads for inserting text. They are really
useful in day to day editing. I chose to implement only selected few - namely 
`i`, `I`, `A` and `o`.

* `I` - jumps to the beginning of the line before going to the insert mode.
* `i` - goes to the insert mode right where the cursor is.
* `A` - jumps to the end of line before going to the insert mode.
* `o` - jumps one line and then goes to the insert mode.

### Deleting text

Basically there are two commands implemented - `d` and `D`. Uppercase `D`
deletes text from current positon to the end of the line. Lowercase `d` is a
bit more complex because it needs direction as an argument. The standard
movements are the possible arguments. 

#### Example

	Przykladowa linijka tekstu.
	    ^
(`^` marks the cursor position).

There are 2 possible movements:
1. `dl` - deletes the letter under cursor
2. `dh` - deletes the letter before cursor

After execution of 1st possibility.

	Przyladowa linijka tekstu.
	    ^

After execution of 2nd possibility.

	Przkladowa linijka tekstu.
	   ^

### Substitution

To use substitute command unlike original Vi you just type `s` and substitution
prompt should appear at the bottom of the screen. **Only first** match is
substituted.

	s/<old_text>/<new_text>/

Last `/` isn't mandatory. 
