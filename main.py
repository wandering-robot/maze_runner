from map_creation.drawing_window import Window
from map_creation.drawing_event_handler import Handler
from ai_learner.ai_main import AI_main

class Main:
    def __init__(self):
        self.window = Window(self)
        self.handler = Handler(self)

        self.running = True
        self.run()

    def run(self):
        while self.running:
            self.window.update_window()
            self.handler.handle()
        ai_section = AI_main(self.window.cells)       #pass the created maze to the AI_learner by exiting the previous window

if __name__ == "__main__":
    main = Main()
    main.run()
