import pygame as py

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
        #import all cells from main
        self.cells = self.main.cell_dict