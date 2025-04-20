# Minesweeper Project

This project is simply just to showcase I have the knowledge to be able to code and use python. The project itself is my own minesweeper game where you can change the board size and game difficulty.

## How It's Made

Packages Used: Python, pygame, tkinter, numpy

My minesweeper works by first showing a dialog box prompting the user to select a board size (small, medium, large), and a game difficulty (easy, medium, hard). It then will generate a board using pygame by randomly placing either Box() or Bomb() objects with a percentage chance based on the selected difficulty level and storing that data in a 2D matrix array. One the boxes/bombs are placed, the script will then go back over every placed cell to determine if a) the cell is a box, and b) if it is, how many bombs is it touching. Using that info it will update the box image to match the number of touching bombs. 

Once the board is generated the game itself is a cycle of reading, processing, and updating inputs until the game ends by checking if cells are marked visible or flagged and updating textures accordingly, and updating cell attributes based on left or right clicks by the mouse.


## Lessons Learned

I learned a lot from this project. The biggest thing I learned was how to actually code in Python since this was the first time I ever have. I learned the syntax and key differences of Pythron from other scripts like Java. Additionally, I learned how to use the packages pygame, tkinter, numpy, os, and random at their most basic level.

I do, however, have a lot more to learn especially when it comes to optimization, condensing code, and if I'd like, more advances uses of the previously mentioned packages.

## How to Play

Simply run the script
