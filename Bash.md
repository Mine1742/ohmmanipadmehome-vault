#linux #bash #script


`*` wildcard matches on zero or more characters -  ls  \*.jp\*g
the `?` wildcard represents a single character - ls 000?.jpg

lists all the files in the current directory whose names contain a period immediately followed a lowercase J or P. It lists all the **.jpg**, **.jpeg**, and **.png** files, but not **.gif** files:  ls \*.\[jp\]\*

Expressions in square brackets can represent ranges of characters: lists all the files in the current directory whose names begin with a lowercase letter:   ls \[a-z\]\*  lists all the files in the current directory whose names begin with a lowercase _or_ uppercase letter: ls \[a-zA-Z\]\*


If you want to create a subdirectory and another subdirectory under it with one command, use the `--parents` flag:   mkdir --parents orders/2019


if you use the `-i` (for "interactive") flag, Bash warns you before deleting existing files.

You can use wildcards to copy several files at once.:  cp \* photos

To copy all the files in a subdirectory named **photos** into a subdirectory named **images**:  cp photos\/\* images


