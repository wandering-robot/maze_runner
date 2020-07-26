import pygame as py
from map_creation.cell import Cell

class Window:
    def __init__(self,main):
        self.main = main

        py.init()
        self.size = (500,500)
        self.cell_size = 10
        #initialize the window and background
        self.display_window = py.display.set_mode((self.size))
        self.background = py.Surface(self.display_window.get_size()).convert()
        self.background.fill((255,255,255))
        #initialize all the cells as default empty
        self.cells = {}
        self.generate_cells()

    def generate_cells(self):
        for i in range(int(self.size[0]/self.cell_size)):
            for j in range(int(self.size[1]/self.cell_size)):
                self.cells[(i,j)] = Cell((i,j),self.cell_size)

    def update_window(self):
        self.display_window.blit(self.background,(0,0))
        for cell in self.cells.values():
            cell.get_colour()
            self.display_window.blit(cell.tile,cell.coord)
        py.display.flip()
            




if __name__ == "__main__":
    window = Window()
    print(window.objects)
