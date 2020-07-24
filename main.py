from window import Window
from event_handler import Handler

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

if __name__ == "__main__":
    main = Main()
    main.run()
