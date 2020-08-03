from shower_stuff.blitters import Cell, Avatar
from ai_learner.state_actions import State, Action
import pygame as py
import pickle

class Window:
    def __init__(self,main,cell_dict):
        self.main = main

        py.init()
        self.size = (500,500)
        self.cell_size = 100

        self.display_window = py.display.set_mode((self.size))
        self.background = py.Surface(self.display_window.get_size()).convert()
        self.background.fill((255,255,255))

        self.cells = cell_dict
        self.re_surface_cells()

        self.actions = self.calc_actions()
        self.avatar = Avatar(self.cell_size)

    #entire process of avatar moving based on what it thinks is best
    def avatar_acts(self):
        state_coord = self.avatar.coord
        best_action = self.find_best_action(state_coord)
        best_state = self.next_state(state_coord,best_action)
        self.move_avatar(best_state)

    #determines best action to take given the avatar's current state 
    def find_best_action(self,state_coord):
        actions = self.actions[:]   #make copy so can pop actions

        action_values = [self.main.qs[(state_coord,action.tup)].value for action in actions] #list of state-action pairs for the given state

        max_value = max(action_values)
        ind = action_values.index(max_value)

        max_action = actions.pop(ind)
        return max_action

    #returns the next state given a previous state and action
    def next_state(self,state_coord,action):
        next_coord = (state_coord[0]+action.tup[0], state_coord[1]+action.tup[1])
        cell_coord = (int(next_coord[0]),int(next_coord[1]))
        try:
            cell_prime = self.cells[cell_coord]
            if cell_prime.purpose == 'wall':       #agent can't enter wall so sends back to in front of wall
                return state_coord
            elif cell_prime.purpose == 'finish':   #agent doesn't do anything once hit terminal, nor does it get any rewards for continuously being there
                self.main.running = False
                return state_coord
            else:
                return cell_coord
        except:
            return state_coord        #if goes off map

    #simple method to move the avatar to pos_tup
    def move_avatar(self,pos_tup):
        self.avatar.coord = pos_tup

    #determine the starting position for the avatar by going through all the cells once to find the starting one
    def move2start(self):
        start_pos = None
        for cell in self.cells.values():
            if cell.purpose == 'start':
                start_pos = cell.coord
                break
        self.move_avatar(start_pos)


    def update_window(self):
        self.display_window.blit(self.background,(0,0))
        for cell in self.cells.values():
            cell.get_colour()
            self.display_window.blit(cell.tile,cell.coord)
        self.display_window.blit(self.avatar.tile,self.avatar.tile_coord())
        py.display.flip()

    def re_surface_cells(self):
        for cell in self.cells.values():
            cell.re_surface()        

    #create a list of all posible actions agent can take
    def calc_actions(self):
        actions = []
        for right in range(-1,2):
            for down in range(-1,2):
                actions.append(Action(right,down))
        return actions

    