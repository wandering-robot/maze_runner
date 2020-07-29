from map_creation.drawing_window import Window
from map_creation.drawing_event_handler import Handler
from ai_learner.ai_main import AI_main

import pickle
from map_creation.cell import Cell          #think I need this to pickle/unpickle

import atexit

class Main:
    def __init__(self):
        #self.window is created in the self.run() method now
        self.handler = Handler(self)        

        self.maze_file_name = None          #name of file for loading/saving purposes
        self.cell_dict = None               #data that gets loaded/saved

        self.drawing = True

    #main method to run all of the program
    def run(self):
        self.drawing = self.load_or_make()
        self.get_file_name()

        if not self.drawing:
            self.cell_dict = self.load_file()
        else:
            self.window = Window(self)              #moved this here so that it won't pop up until asked for
            while self.drawing:
                self.window.update_window()
                self.handler.handle()
            self.cell_dict = self.window.cells
        self.ai_section = AI_main(self.cell_dict)       #pass the created maze to the AI_learner by exiting the previous window
        self.ai_section.run_episodes()


    #method called at end of session to save experience
    def save_ai_knowledge(self):
        qs = self.ai_section.agent.qs
        outfile = open(self.maze_file_name + f'_ai_{self.ai_section.agent.episode_number:04}', 'wb')
        pickle.dump(qs,outfile,protocol=pickle.HIGHEST_PROTOCOL)

    #by using self.maze_file_name, return a dictionary of all the cells
    def load_file(self):
        got_file = False
        while not got_file:
            try:
                infile = open(self.maze_file_name,'rb')
                got_file = True
            except:
                self.maze_file_name = input('That file name does not exist, please re-enter file name:\t')
        self.cell_dict = pickle.load(infile)
            #will eventually need to reinvoke this when wanting to draw it out
        # for cell in self.cell_dict.values():
        #     cell.re_surface()
        infile.close()
        return self.cell_dict

    #saves file using self.window.cells
    def save_file(self):
        outfile = open(self.maze_file_name,'wb')
        for cell in self.window.cells.values():
            cell.de_surface()
        pickle.dump(self.window.cells,outfile,protocol=pickle.HIGHEST_PROTOCOL)
        outfile.close()

    #defines maze_file_name
    def get_file_name(self):
        if not self.drawing:
            self.maze_file_name = input('Please input old maze name:\t').lower()
        else:
            self.maze_file_name = input('Please create new maze name:\t').lower()

    #method that asked for user input if they want to load a file or create a new one
    def load_or_make(self):
        while True:
            user_input = input("[L]oad file or [N]ew file:\t").lower()
            if user_input == 'n':
                return True
            elif user_input == 'l':
                return False
            else:
                print('That is not a recognized input :(')


if __name__ == "__main__":
    main = Main()
    atexit.register(main.save_ai_knowledge)
    main.run()

