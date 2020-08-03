import pygame as py

class Avatar:
    def __init__(self,size):
        self.size = size
        self.tile = py.Surface((self.size,self.size)).convert()
        self.colour = (255,255,255)
        self.tile.fill(self.colour)
        
        self.coord = None

    def tile_coord(self):
        return (self.coord[0]*self.size,self.coord[1]*self.size)



class Cell:
    def __init__(self,coord,size):    #initialize with a coordinate tuple
        self.coord = (coord[0]*size,coord[1]*size)
        self.size = size

        self.purpose = None
        self.tile = py.Surface((self.size,self.size)).convert()
        self.get_colour()

    def __repr__(self):
        return f'Cell@{self.coord[0]}&{self.coord[1]}'
    
    #Called once it needs to redraw the tiles
    def re_surface(self):
        self.tile = py.Surface((self.size,self.size)).convert()

    #Called to remove surface values for saving
    def de_surface(self):
        self.tile = None

    #Gets the tile's colour depending on it's purpose
    def get_colour(self):
        if self.purpose == None:
            self.colour = (0,255,0)     #walkable is green
        elif self.purpose == 'start':
            self.colour = (255,0,0)     #start is red
        elif self.purpose == 'finish':
            self.colour = (0,0,255)     #end is blue
        else:
            self.colour = (0,0,0)       #walls are black
        self.tile.fill(self.colour)
