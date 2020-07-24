import pygame as py

class Handler:

    def __init__(self, main):
        self.main = main
    
    def handle(self):
        for event in py.event.get():    
            if event.type == py.QUIT:
                self.stop_running()
            elif event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.create_wall(py.mouse.get_pos())
                elif event.button == 3:
                    self.delete_wall(py.mouse.get_pos())

    def pixel2cell(self,pixel):
        cell_size = self.main.window.cell_size
        cell_id = (round(pixel[0]/cell_size),round(pixel[1]/cell_size))
        return cell_id

    def create_wall(self,pos):
        cell_id = self.pixel2cell(pos)
        self.main.window.cells[cell_id].purpose = 'wall'

    def delete_wall(self,pos):
        cell_id = self.pixel2cell(pos)
        self.main.window.cells[cell_id].purpose = None
    
    
    def stop_running(self):
        self.main.running = False
        py.quit()