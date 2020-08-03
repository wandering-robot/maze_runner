from shower_stuff.showing_window import Window
from shower_stuff.shower_event_handler import Handler

import pickle
import dill
from time import sleep

class MainShower:
    """meant to be read show-er, not a place where you clean yourself"""

    def __init__(self):
        self.qs = self.get_knowledge()

        self.map = self.get_map()

        self.handler = Handler(self)
        self.running = True

    #main method to run the display
    def run(self):
        self.window = Window(self,self.map)
        #move the avatar to the starting location
        self.window.move2start()
        while self.running:
            self.window.update_window()
            self.window.avatar_acts()
            self.handler.handle()
            sleep(0.5)

    def move_avatar(self):
        current_pos = self.window.avatar.pos

    #Method to import the map
    def get_map(self):
        try:
            infile = open(self.name,'rb')
        except:
            print('Error 404: File not found')
        cells = dill.load(infile)
        infile.close()
        return cells

    #method to import all the state-action pairs and their values
    def get_knowledge(self):
        file_got = False
        while not file_got:
            self.name = input('Which map would you like to load?\t').lower()
            self.number = input('Which episode number would you like?\t')
            try:
                infile = open(self.name+'_ai_'+self.number,'rb')
                file_got = True
            except:
                print('I have no record of this, please check your inputs carefully')
        qs = dill.load(infile)
        infile.close()
        return qs

if __name__ == "__main__":
    main = MainShower()
    main.run()
    
