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
import os
if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk



UNIT = 40   # pixels
MAZE_H = 8  # grid height
MAZE_W = 7 * 2 # grid width


Qtd_horários = 7; #Intervalo de 6 horas ás 9 horas e 30 minutos 
Qtd_dias = 6 * 2; #Dias de Segunda á Sábado 

#Inicializando matriz
map = [["-"] * Qtd_dias for i in range(Qtd_horários)]

def preencherMap(): 
     # create ovals matriz - W 
        for i in range(Qtd_horários): 
            for g in range(Qtd_dias): 
                if (g % 2 == 0): 
                    map[i][g] = "W"

def initialPositionAgent(): 
    for i in range(Qtd_horários): 
        for g in range(Qtd_dias): 
            if (g == 1 and i == Qtd_horários // 2): 
                map[i][g] = "O"
                return g, i
                
def viewMap(): 
    # os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(Qtd_horários): 
        for g in range(Qtd_dias): 
            print(map[i][g], end= " ")
        print("\n")
    print("**************************************************************\n\n\n\n\n")

# Iniciando aprendizagem com 3 metas no dia, com tempo de 30 minutos


class Maze():
    
    
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l']
        self.n_actions = len(self.action_space)
        preencherMap() 
        self.i_column, self.i_line = initialPositionAgent()
        print("column: " + str(self.i_column) + " line: " + str(self.i_line))
        viewMap()
        
        #Armazena o index das linhas acessadas 
        self.steps_lines = []
        #Armazena o index das colunas acessadas 
        self.steps_columns = []


    def reset(self):
        time.sleep(3)
        return [self.i_column, self.i_line]
    
    def restart(self): 
        self.i_column, self.i_line = initialPositionAgent()
    
    def step(self, action):

        viewMap()
        
        if action == 0: 
            #Move up
            if self.i_line > 0: 
                aux = self.i_line
                self.i_line -= 1
                map[self.i_line][self.i_column] = "O"
                map[aux][self.i_column] = "-"
            
        elif action == 1:  
            #Move down
            if (self.i_line < len(map)): 
                aux = self.i_line
                self.i_line += 1
                map[self.i_line][self.i_column] = "O"
                map[aux][self.i_column] = "-"
                
        elif action == 2: 
            #Move left
             if (self.i_column > 0): 
                 aux = self.i_column
                 self.i_column -= 1
                 if(map[self.i_line][self.i_column] == "W" or map[self.i_line][self.i_column] == "B"):
                    map[self.i_line][self.i_column] += "O"
                 map[self.i_line][aux] = "-"

        print(f"position actual = column: {self.i_column}, line: {self.i_line}")
        if map[self.i_line][self.i_column] == "WO" and self.i_line not in self.steps_lines:
            
            #Calcula do horário 
            horas_float = (360 + (self.i_line * 30)) / 60
            horas_int = int(horas_float)
            minutos = (horas_float - horas_int) * 60

            viewMap()
            response = input(f"Deseja estudar no horário de {int(horas_int)}:{int(minutos)} (S/N)?").lower()
            
            if response == "s":   
                reward = 1
                map[self.i_line][self.i_column] = "W"
                done = True
                s_ = 'terminal'
            elif response == "n": 
                reward = -1
                map[self.i_line][self.i_column] = "B"
                done = True 
                s_ = 'terminal'
            
            self.steps_lines.append(self.i_line)
            self.steps_columns.append(self.i_column)

        elif map[self.i_line][self.i_column] == "BO":
            reward = -1
            map[self.i_line][self.i_column] = "B"
            done = True
            s_ = 'terminal'
        elif self.i_line in self.steps_lines and self.i_column in self.steps_columns: 
            reward = 0
            map[self.i_line][self.i_column] = map[self.i_line][self.i_column][0]
            done = True 
            s_ = 'terminal'
        else:
            reward = 0
            s_ = [self.i_column, self.i_line]
            done = False
        
        return s_, reward, done

