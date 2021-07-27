# Game_of_life_python
In this repository there are programs of Conway's game of life

## Prerequisites
Pygame -> pip install pygame
numpy  -> pip install numpy

### Information
This program is a modification of the program available in https://github.com/Josephbakulikira/Conway-s-Game-of-life---Python

This program was made by Luis Felipe Cedeño Pérez student of genomics science at the UNAM México

The idea of this program is to have a grid additional to the grid that is going to be displayed that will have
the information of how many neighbours an specific square has, so now it won't need to calculate that information
each time it iterates for each square in the grid, and this grid is updated each time a change occurs in the grid
of the cells.

### Example of usage of the program
python3 conways_game_of_life.py -f 60 -p 0.5 -s 5 -w 1024 -e 576

### Comparison of speed from the version downloaded from github
This test were done running at the same time in ubuntu, using the following paameters
-f 500, this is a value set high to see what is the amount of frames it can run in the actual test
-s 5
-p 0.5
-w 1024
-e 576

Previous program runned at an average of 7 fps
This program 42 fps
During the test the processor was running at an average speed of 3.8GHz 
