import pygame as py

class Handler:

    def __init__(self, main):
        self.main = main
    
    def handle(self):
        for event in py.event.get():    
            if event.type == py.QUIT:
                self.stop_running()

    #shutting down the program
    def stop_running(self):
        self.main.drawing = False
        py.quit()