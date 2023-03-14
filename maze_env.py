"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the environment part of this example.
The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""


import numpy as np
import time
import sys
import random
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk



UNIT = 40   # pixels
MAZE_H = 8  # grid height
MAZE_W = 7  # grid width

# Iniciando aprendizagem com 3 metas no dia, com tempo de 30 minutos
# values_random = [random.randrange(0, MAZE_H - 1) for i in range(2)]
values_random = []
count = 0
while (count < 2):
    value_random = random.randint(0, MAZE_H - 1)
    if(value_random not in values_random): 
        values_random.append(value_random)
        count += 1
    
print(len(values_random))

class Maze(tk.Tk, object):
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd']
        self.n_actions = len(self.action_space)
        self.title('maze')
        self.geometry('{0}x{1}'.format(MAZE_W * UNIT, MAZE_H * UNIT))
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                           height=MAZE_H * UNIT,
                           width=MAZE_W * UNIT)
        origin = np.array([20, 20])
        
        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)
            
            
        self.COUNT = 0   
        self.hells = []
        self.ovals = []

        
        # create ovals primary
        for i in values_random: 
            self.create_oval(i, 0)

        
        # create red rect
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')

        # pack all
        self.canvas.pack()

    def reset(self, new_initial=0, coluna=0, linha=0):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.rect)
        if (new_initial == 0): 
            origin = np.array([20, 20])
            self.rect = self.canvas.create_rectangle(
                origin[0] - 15, origin[1] - 15,
                origin[0] + 15, origin[1] + 15,
                fill='red')
        else: 
            origin = np.array([20, 20])
            initial_point = origin + np.array([UNIT * coluna, UNIT * linha])
            self.rect = self.canvas.create_rectangle(
                initial_point[0] - 15, initial_point[1] - 15,
                initial_point[0] + 15, initial_point[1] + 15,
                fill='red')
            
            
        # return observation
        return self.canvas.coords(self.rect)

    def step(self, action):
        s = self.canvas.coords(self.rect)
        base_action = np.array([0, 0])
        if action == 0:   # up
            if s[1] > UNIT:
                base_action[1] -= UNIT
        elif action == 1:   # down
            if s[1] < (MAZE_H - 1) * UNIT:
                base_action[1] += UNIT
        # elif action == 2:   # right
        #     if s[0] < (MAZE_W - 1) * UNIT:
        #         base_action[0] += UNIT
        # elif action == 3:   # left
        #     if s[0] > UNIT:
        #         base_action[0] -= UNIT

        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

        s_ = self.canvas.coords(self.rect)  # next state

        list_arguments = []
    

        # reward function
        if s_ in [self.canvas.coords(i) for i in self.ovals]:
            list_arguments = [1, int(s_[0]//40), int(s_[1]//40) + 1]
            horas_float = (360 + ((s_[1]//40) * 30)) / 60
            horas_int = int(horas_float)
            minutos = (horas_float - horas_int) * 60
            response = input(f"Deseja estudar no horário de {int(horas_int)}:{int(minutos)} (S/N)?").lower()
            self.COUNT += 1
            if response == "s":   
                reward = 1
                done = True
                s_ = 'terminal'
            else: 
                reward = -1
                del self.ovals[[self.canvas.coords(i) for i in self.ovals].index(s_)]
                self.create_hell(int(s_[1]//40), int(s[0]//40))
                done = True 
                s_ = 'terminal'
        elif s_ in [self.canvas.coords(i) for i in self.hells]:
            reward = -1
            done = True
            s_ = 'terminal'
        else:
            reward = 0
            done = False

        print(self.COUNT)
        if (self.COUNT < 2): 
            return s_, reward, done, list_arguments, False
        else: 
            self.COUNT = 0
            return s_, reward, done, [], True

    def render(self):
        time.sleep(0.1)
        self.update()
    

    def create_hell(self, linha, coluna, position=-1): 
        origin = np.array([20, 20])
        hell = origin + np.array([UNIT * coluna, UNIT * linha])
        self.hells.append(self.canvas.create_rectangle(
            hell[0] - 15, hell[1] - 15,
            hell[0] + 15, hell[1] + 15,
            fill='black'))
         
    def create_oval(self, linha, coluna, position=-1): 
        origin = np.array([20, 20])
        oval_center = origin + np.array([UNIT * coluna, UNIT * linha])
        if (position == -1): 
            self.ovals.append(self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow'))
