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

#intervalo de horário - 6:00 ás 10:00 = 4 horas 
horariosAgenda = ["6:00", "6:30", "7:00", "7:30", "8:00", "8:30", "9:00", "9:30", "10:00"]
mapHorarios = []

Qtd_horários = (4 * 60) / 30; #Intervalo de 6 horas ás 9 horas e 30 minutos 
length_colunas = 5 
length_linhas = 5
center_index = (length_linhas - 1)/2

#Inicializando matriz
map = [["-"] * length_colunas for i in range(length_linhas)]

def preencherMap(): 
    count = 0
    # create ovals matriz - W 
    for i in range(length_linhas): 
        for g in range(length_colunas): 
            if (g % 2 == 0 and i == 0):
                print("linha superior")
                map[i][g] = "W"
                mapHorarios.append({"hora": horariosAgenda[count], "i_line": i, "i_column": g}) 
                count += 1
    for i in range(length_linhas): 
        for g in range(length_colunas): 
            if (g == length_colunas - 1 and i % 2 == 0 and i != 0 and i != length_linhas - 1): 
                print("linha right")
                map[i][g] = "W"
                mapHorarios.append({"hora": horariosAgenda[count], "i_line": i, "i_column": g})
                count += 1 
    for i in range(length_linhas): 
        for g in range(length_colunas): 
            if (i == len(map) - 1 and g % 2 == 0) :
                print("linha inferior")
                map[i][g] = "W"
                mapHorarios.append({"hora": horariosAgenda[count], "i_line": i, "i_column": g})
                count += 1
    for i in range(length_linhas): 
        for g in range(length_colunas): 
            if (g == 0 and i % 2 == 0 and i != 0 and i != length_linhas - 1): 
                print("linha left")
                map[i][g] = "W" 
                mapHorarios.append({"hora": horariosAgenda[count], "i_line": i, "i_column": g})
                count += 1
                
    print(mapHorarios)
                           

def initialPositionAgent(): 
    for i in range(length_linhas): 
        for g in range(length_colunas): 
            if (g == center_index and i == center_index): 
                map[i][g] = "O"
                return g, i
            
def search_horario(i_line, i_column): 
    for i in range(len(mapHorarios)): 
        if mapHorarios[i]['i_line'] == i_line and mapHorarios[i]['i_column'] == i_column: 
            return mapHorarios[i]["hora"]
                
def viewMap(): 
    # os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(length_linhas): 
        for g in range(length_colunas): 
            print(map[i][g], end= " ")
        print("\n")

# Iniciando aprendizagem com 3 metas no dia, com tempo de 30 minutos


class Maze():
    
    
    def __init__(self):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r']
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
        time.sleep(0.5)
        return [self.i_column, self.i_line]
    
    def restart(self): 
        self.i_column, self.i_line = initialPositionAgent()
    
    def step(self, action):

        
        
        if action == 0: 
            #Move up
            if self.i_line > 0: 
                aux = self.i_line
                self.i_line -= 1
                if(map[self.i_line][self.i_column] == "W" or map[self.i_line][self.i_column] == "B"):
                    map[self.i_line][self.i_column] += "O"
                map[aux][self.i_column] = "-"
            
        elif action == 1:  
            #Move down
            if (self.i_line < length_linhas - 1): 
                aux = self.i_line
                self.i_line += 1
                if(map[self.i_line][self.i_column] == "W" or map[self.i_line][self.i_column] == "B"):
                    map[self.i_line][self.i_column] += "O"
                map[aux][self.i_column] = "-"
                
        elif action == 2: 
            #Move left
             if (self.i_column > 0): 
                 aux = self.i_column
                 self.i_column -= 1
                 if(map[self.i_line][self.i_column] == "W" or map[self.i_line][self.i_column] == "B"):
                    map[self.i_line][self.i_column] += "O"
                 map[self.i_line][aux] = "-"
                 
        elif action == 3: 
            #Move right
             if (self.i_column < length_colunas - 1): 
                 aux = self.i_column
                 self.i_column += 1
                 if(map[self.i_line][self.i_column] == "W" or map[self.i_line][self.i_column] == "B"):
                    map[self.i_line][self.i_column] += "O"
                 map[self.i_line][aux] = "-"

        print(f"position actual = column: {self.i_column}, line: {self.i_line}")
        viewMap()
        
        if map[self.i_line][self.i_column] == "WO":
            
         
            response = input(f"Deseja estudar no horário de {search_horario(self.i_line, self.i_column)} (S/N)?").lower()
            
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
            
             
            response = input(f"Deseja estudar no horário de {search_horario(self.i_line, self.i_column)} (S/N)?").lower()
            
            if response == "s":   
                reward = 2
                map[self.i_line][self.i_column] = "W"
                done = True
                s_ = 'terminal'
            elif response == "n": 
                reward = -2
                map[self.i_line][self.i_column] = "B"
                done = True 
                s_ = 'terminal'
                
        else:
            reward = 0
            s_ = [self.i_column, self.i_line]
            done = False
        
        return s_, reward, done

