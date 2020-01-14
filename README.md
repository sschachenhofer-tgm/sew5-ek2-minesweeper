# Minesweeper

A Python implementation of the popular classic.

![image-20200114144429793](D:\Dokumente\_Schule\SEW\EK2 - Minesweeper\screenshot.png)



### How to play

#### The basic game

Try to find all the mines on the game board and open all the other fields.

`Left-click` on a field to open it

- If the field contains a mine, you lose
- Otherwise, the number displayed on the field tells you how many of the eight adjacent fields contain mines. With a little bit of logical thinking, you can figure out where the mines have to be.



#### Tagging fields

You can tag fields for yourself to keep track of which fields have to contain mines.

- `Right-click` a field once to tag it as *definitely containing a mine*
- `Right-click` it a second time to tag it as *possibly containing a mine*
- `Right-click` it a third time to untag it

Before you can open a tagged field, you need to untag it. Therefore, you can also use tagging fields as a security mechanism.



#### The game modes

There are three default game boards for different difficulties:

- **Easy**: 9x9 fields, 10 mines
- **Medium**: 16x16 fields, 40 mines
- **Difficult**: 30x16 fields, 99 mines

You can also start a **custom game** by clicking `New game` &rarr; `Custom` and enter the dimensions of the game board and the number of mines



#### Command-line usage

To simply start a default game with a 9x9 board and 10 mines, use:

``````bash
python minesweeper.py
``````

To start a custom game, you can pass the parameters as command-line options:

``````
python minesweeper.py <width> <height> <number of mines>
``````

This syntax will also be displayed if you call the help page using

``````
python minesweeper.py -h
``````

or 

``````
python minesweeper.py --help
``````