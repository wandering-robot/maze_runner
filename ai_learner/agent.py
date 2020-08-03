from ai_learner.state_actions import State, Action, Q

from random import randint, choice

class Agent:
    def __init__(self,main,cell_dict):
        self.main = main
        self.cell_dict = cell_dict

        self.starting_state = None      #updated to the actual starting state in calc_states()

        self.actions = self.calc_actions()
        self.states = self.calc_states()
        self.qs = self.calc_qs()

        self.eligible_thresh = 0.01
        self.eligible_qs = []           #list of all recently visited qs that have eligibility above eligibility_thresh

        self.episode_number = 1
        self.found_terminal = False     #use this to differentiate between episodes, changed in the next_state method

    def run_episode(self):
        self.episode_itr = 0

        state = self.starting_state
        action = self.get_action(state)
        while not self.found_terminal:
            q = self.qs[(state.coord,action.tup)]

            state_prime, reward = self.next_state(state,action)
            action_prime = self.get_action(state_prime)
            q_prime = self.qs[(state_prime.coord,action_prime.tup)]

            delta = reward + self.main.gamma*q_prime.value - q.value
            self.update_eligibles(q_prime)
            for q_all in self.eligible_qs:
                q_all.value += self.main.alpha*delta*q_all.eligibility

            self.episode_itr += 1
            state, action = state_prime, action_prime


        self.finish_episode()

    #prints inormatin about episode run
    def finish_episode(self):
        print(f'Episode {self.episode_number} took {self.episode_itr} iterations')

    #method that returns (next state, reward) given a state-action pair
    def next_state(self,state,action):
        next_coord = (state.coord[0]+action.tup[0], state.coord[1]+action.tup[1])
        try:
            state_prime = self.states[next_coord]
            reward = state_prime.reward
            if state_prime.purpose == 'wall':       #agent can't enter wall so sends back to in front of wall
                return state, reward
            elif state_prime.purpose == 'finish':   #agent doesn't do anything once hit terminal, nor does it get any rewards for continuously being there
                self.found_terminal = True
                return state, reward
            else:
                return state_prime, reward
        except:
            return state, -1            #assign -1 reward when goes off map

    #obtain an action object given an e-greedy policy
    def get_action(self,state):
        actions = self.actions[:]   #make copy so can pop actions later
        action_values = [self.qs[(state.coord,action.tup)].value for action in actions] #list of state-action pairs for the given state

        max_value = max(action_values)
        ind = action_values.index(max_value)

        max_action = actions.pop(ind)

        if randint(0,1) > self.main.epsilon:
            return max_action
        else:
            return choice(actions)

    #create a list of all posible actions agent can take
    def calc_actions(self):
        actions = []
        for right in range(-1,2):
            for down in range(-1,2):
                actions.append(Action(right,down))
        return actions

    #create a dictionary of all possible states, indexed by its coordinate
    def calc_states(self):
        states = {}
        for coord, cell in self.cell_dict.items():
            states[coord] = State(coord,cell.purpose)
            if cell.purpose == 'start':
                self.starting_state = states[coord]
        return states

    #create a dictionary of all possible qs, indexed by (state.coord,action.tup)
    def calc_qs(self):
        qs = {}
        for coord,state in self.states.items():
            for action in self.actions:
                q = Q(state,action)
                qs[(coord,action.tup)] = q
        return qs
            