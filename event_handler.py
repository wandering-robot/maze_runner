import pygame as py

class Handler:

    def __init__(self, main):
        self.main = main
        self.wall_maker_mode = False
        self.wall_delete_mode = False
    
    def handle(self):
        for event in py.event.get():    
            if event.type == py.QUIT:
                self.stop_running()
            elif event.type == py.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.wall_maker_mode = True
                elif event.button == 3:
                    self.wall_delete_mode = True
            elif event.type == py.MOUSEBUTTONUP:
                if event.button == 1:
                    self.wall_maker_mode = False
                elif event.button == 3:
                    self.wall_delete_mode = False
            elif event.type == py.KEYDOWN:
                if event.key == py.K_s:
                    self.make_start()
                elif event.key == py.K_f:
                    self.make_finish()
        if self.wall_maker_mode:
            self.create_wall()
        elif self.wall_delete_mode:
            self.delete_wall()

    def pixel2cell(self,pixel):
        cell_size = self.main.window.cell_size
        cell_id = (round(pixel[0]/cell_size),round(pixel[1]/cell_size))
        return cell_id

    def make_start(self):
        pos = py.mouse.get_pos()
        cell_id = self.pixel2cell(pos)
        self.main.window.cells[cell_id].purpose = 'start'

    def make_finish(self):
        pos = py.mouse.get_pos()
        cell_id = self.pixel2cell(pos)
        self.main.window.cells[cell_id].purpose = 'finish'

    def create_wall(self):
        pos = py.mouse.get_pos()
        cell_id = self.pixel2cell(pos)
        self.main.window.cells[cell_id].purpose = 'wall'

    def delete_wall(self):
        pos = py.mouse.get_pos()
        cell_id = self.pixel2cell(pos)
        self.main.window.cells[cell_id].purpose = None
    
    def stop_running(self):
        self.main.running = False
        py.quit()