PyAutomata
==========

A simple Python module for generating cellular automata.

running the script will create a directory called `png` which will contain a largish png of each of the 256 cellular automata rules. You can change the number of rows and the scalling factor by changing the arguments to the `make_pngs` function at the bottom of the script.

There is a lot of unused functionality, including the ability to print out the results to a terminal instead of making a png, and choosing the color pallete for either case. The colorized printing is obviously not something that windows can do. I need to add proper argument parsing to make usage easier, and perhaps not force someone to make every single automata at once :p .
