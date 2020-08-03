
class State:
    def __init__(self,coord,purpose):
        self.coord = coord
        self.purpose = purpose

        self.reward = self.calc_reward()

    def __repr__(self):
        return f'{self.purpose}@{self.coord}'

    #defines how much reward each state gives depending on its purpose
    def calc_reward(self):
        if self.purpose == 'wall':
            return -5
        elif self.purpose == 'finish':
            return 5
        else:
            return -1

class Action:
    def __init__(self,right,down):
        self.tup = (right,down)
        
        self.right, self.down = self.tup

    def __repr__(self):
        return f'R{self.right}D{self.down}'

class Q:
    def __init__(self,state,action):
        self.state = state
        self.action = action

        self.value = 0
        self.eligibility = 0

    def __repr__(self):
        return f'V{self.value:.2f}E{self.eligibility:.2f}'

