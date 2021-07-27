import pygame
import time
import random
import numpy as np
import os
import argparse
import time

'''
This program is a modification of the program available in https://github.com/Josephbakulikira/Conway-s-Game-of-life---Python

This program was made by Luis Felipe Cedeño Pérez student of genomics science at the UNAM México

The idea of this program is to have a grid additional to the grid that is going to be displayed that will have
the information of how many neighbours an specific square has, so now it won't need to calculate that information
each time it iterates for each square in the grid, and this grid is updated each time a change occurs in the grid
of the cells.

###Comparison of speed from the version downloaded from github###
This test were done running at the same time in ubuntu, using the following paameters
-f 500, this is a value set high to see what is the amount of frames it can run
-s 5
-p 0.5
-w 1024
-e 576

Previous program runned at an average of 7 fps
This program 42 fps
During the test the processor was running at an average speed of 3.8GHz 

###Example of usage of the program###
python3 conways_game_of_life.py -f 60 -p 0.5 -s 5 -w 1024 -e 576
'''

parser = argparse.ArgumentParser(description="")
parser.add_argument("-p", "--prob", dest="prob", required=True) #probability of 1 in the grid when generated
parser.add_argument("-f", "--fps", dest="fps", required=True) #frames per second
parser.add_argument("-s", "--scale", dest="scale", required=True) #1 is the minimum and smaller value
parser.add_argument("-w", "--width", dest="width", required=True) #width of the window 1024
parser.add_argument("-e", "--height", dest="height", required=True) #height of the window 576
args = parser.parse_args()

class Grid:
    def __init__(self, width, height, scale, offset, prob_1):
        self.scale = scale

        self.columns = int(height/scale)
        self.rows = int(width/scale)

        self.prob_1=prob_1

        #self.size = (self.rows, self.columns)
        self.grid_array=[[0 for j in range(self.columns)] for i in range(self.rows)]
        self.neighbours_array=[[[0 for j in range(self.columns)] for i in range(self.rows)]]
        self.offset = offset

    #this function is used to set the first random grid using an specific probability for the first generation
    def random2d_array(self):
        for x in range(self.rows):
            for y in range(self.columns):
                #here this was commented so the probability of 0 or 1 can be different from 0.5
                #self.grid_array[x][y] = random.randint(0,1)
                value=np.random.choice([0,1],p=[1-self.prob_1,self.prob_1])
                self.grid_array[x][y] = value
                if(value==1):
                    self.setting_neighbours(x,y)


    def Conway(self, off_color, on_color, surface, pause):
        for x in range(self.rows):
            for y in range(self.columns):
                y_pos = y * self.scale
                x_pos = x * self.scale
                if self.grid_array[x][y] == 1:
                    pygame.draw.rect(surface, on_color, [x_pos, y_pos, self.scale-self.offset, self.scale-self.offset])

                else:
                    pygame.draw.rect(surface, off_color, [x_pos, y_pos, self.scale-self.offset, self.scale-self.offset])

        if pause == False:
            #for each new generation a new grid is generated as well as a new matrix were the values of the
            #neighbours are going to be updated as the grid is upgraded.
            next=[[0 for j in range(self.columns)] for i in range(self.rows)]
            self.neighbours_array.append([[elem for elem in row] for row in self.neighbours_array[0]])
            for x in range(self.rows):
                for y in range(self.columns):
                    state = self.grid_array[x][y]
                    #neighbours = self.get_neighbours( x, y)
                    neighbours=self.neighbours_array[0][x][y]
                    #when the state of a cell is changed the grid of the neigbors is updated using sum or 
                    #sum neighbours
                    if state == 0 and neighbours == 3:
                        next[x][y] = 1
                        self.sum_neighbours(x,y)
                    elif state == 1 and (neighbours < 2 or neighbours > 3):
                        next[x][y] = 0
                        self.sub_neighbours(x,y)
                    else:
                        next[x][y] = state
            #once the generation is updated the program values of the next generation are changed, so the new grid
            #is going to be grid, and with pop it will delete the older grid leaving the new grid in the position
            #0 of the list
            self.grid_array = next
            self.neighbours_array.pop(0)

    #This function is for changing the value from 0 to 1 of a given square, it uses the function setting 
    #neighbours to update the value of the neighbours grid, but it will only do this if the square isn't 1 already
    def HandleMouse(self, x, y):
        _x = x//self.scale
        _y = y//self.scale
        if(self.grid_array[_x][_y]!=1):
            self.setting_neighbours(_x,_y)
        if self.grid_array[_x][_y] != None:
            self.grid_array[_x][_y] = 1

    #this function is used when the matrix is created or the value of a square is updated by the user, so in this
    #case it just needs to update the values around the square
    def setting_neighbours(self,x,y):
        for n in range(-1,2):
            for m in range(-1,2):
                if(n!=0 or m!=0):
                    temp_x=x+n
                    temp_y=y+m
                    if(temp_x>=0 and temp_x<self.rows):
                        if(temp_y>=0 and temp_y<self.columns):
                            #print(temp_x,temp_y)
                            self.neighbours_array[0][temp_x][temp_y]+=1

    #this function is for when the next generation is being calculated, and the square is passing from 0 to 1, so
    #the squares around this one need to be updated to add 1 to them
    def sum_neighbours(self,x,y):
        for n in range(-1,2):
            for m in range(-1,2):
                if(n!=0 or m!=0):
                    temp_x=x+n
                    temp_y=y+m
                    if(temp_x>=0 and temp_x<self.rows):
                        if(temp_y>=0 and temp_y<self.columns):
                            self.neighbours_array[-1][temp_x][temp_y]=self.neighbours_array[-1][temp_x][temp_y]+1

    #this is for when a cell passes from 1 to 0, so in this case we need to substract 1 from the squares aroun 
    #this one
    def sub_neighbours(self,x,y):
        for n in range(-1,2):
            for m in range(-1,2):
                if(n!=0 or m!=0):
                    temp_x=x+n
                    temp_y=y+m
                    #print(temp_x,temp_y)
                    if(temp_x>=0 and temp_x<self.rows):
                        if(temp_y>=0 and temp_y<self.columns):
                            self.neighbours_array[-1][temp_x][temp_y]=self.neighbours_array[-1][temp_x][temp_y]-1


os.environ["SDL_VIDEO_CENTERED"]='1'

#resolution
#width, height = 1024,576
width=int(args.width)
height=int(args.height)
size = (width, height)

pygame.init()
pygame.display.set_caption("CONWAY'S GAME OF LIFE")
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
fps=int(args.fps)

black = (0, 0, 0)
blue = (0, 121, 150)
blue1 = (0,14,71)
white = (255, 255, 255)

offset = 1

cont_gen=0

Grid = Grid(width,height, int(args.scale), offset, float(args.prob))
Grid.random2d_array()

pause = False
run = True
while run:
    start=time.time()
    clock.tick(fps)
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                pause = not pause
    
    Grid.Conway(off_color=white, on_color=blue1, surface=screen, pause=pause)

    if pygame.mouse.get_pressed()[0]:
        mouseX, mouseY = pygame.mouse.get_pos()
        Grid.HandleMouse(mouseX, mouseY)

    pygame.display.update()
    if(pause==False):
        print(1/(time.time()-start))
        #print(cont_gen)
        cont_gen+=1

pygame.quit()