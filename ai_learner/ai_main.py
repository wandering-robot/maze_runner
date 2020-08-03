from ai_learner.ai_window import Window
from ai_learner.agent_old import Agent

class AI_main:
    def __init__(self,cell_dict):
        self.cell_dict = cell_dict

        self.alpha = 0.15           #step size
        self.gamma = 0.75           #discount factor
        self.lamda = 0.8            #trace decay parameter
        self.epsilon = 0.05         #explorative parameter
        
        # self.window = Window(self)
        self.agent = Agent(self,cell_dict)

    def run_episodes(self):
        while True:
            self.agent.run_episode()
            self.agent.episode_number += 1
            self.agent.found_terminal = False


        
    
