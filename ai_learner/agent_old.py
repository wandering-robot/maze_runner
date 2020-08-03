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

        self.episode_number = 1
        self.found_terminal = False     #use this to differentiate between episodes, changed in the next_state method

        self.step_size = 0.15
        self.discount = 0.8
        self.epsilon = 0.15

    def run_episode(self):
        self.episode_itr = 0

        state = self.starting_state
        action = self.get_action(state)
        while not self.found_terminal:
            q = self.qs[(state.coord,action.tup)]

            state_prime, reward = self.next_state(state,action)
            action_prime = self.get_action(state_prime)
            q_prime = self.qs[(state_prime.coord,action_prime.tup)]

            q.value = q.value + self.step_size*(reward + self.discount*q_prime.value - q.value) 

            self.episode_itr += 1
            state, action = state_prime, action_prime


        self.finish_episode()

    def get_action(self,state):
        actions = self.actions[:]
        action_values = [self.qs[(state.coord,action.tup)].value for action in actions]

        max_value = max(action_values)
        ind = action_values.index(max_value)

        max_action = actions.pop(ind)

        if randint(0,1) > self.epsilon:
            return max_action
        else:
            return choice(actions)


    def get_max_Qp(self,state):
        action = self.e_greedy(state)
        return self.qs[(state,action)]

    #prints inormatin about episode run
    def finish_episode(self):
        print(f'Episode {self.episode_number} took {self.episode_itr} iterations')

    #update eligibility values for all the qs in list, increasing the value for the q provided (the most recent one) and removing qs that are below the threshold
    def update_eligibles(self,new_q):
        self.add2eligible(new_q)    #add new q to list
        new_q.eligibility = (new_q.eligibility + 1)/self.main.gamma/self.main.lamda      #increase eligibility of current q and made to cancel with first decay
        for q in self.eligible_qs[:]:       #use copy of list so that can remove qs without screwing up order
            q.eligibility = q.eligibility * self.main.gamma * self.main.lamda #decay all of them
            if q.eligibility < self.eligible_thresh:
                self.eligible_qs.remove(q)      #remove them from the list if they have decayed out of relevancy

    #add a q to the list of eligible qs
    def add2eligible(self,q):
        if q not in self.eligible_qs:
            self.eligible_qs.append(q)

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

    #goes through values in qs and resets eligibilities to 0
    def reset_eligibilities(self):
        for q in self.qs.values():
            q.eligibility = 0

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
            