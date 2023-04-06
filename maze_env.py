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
import pandas as pd




#intervalo de horário - 6:00 ás 10:00 = 4 horas 


# Iniciando aprendizagem com 3 metas no dia, com tempo de 30 minutos
class Maze():
    
    def __init__(self, lengthMap, possiveisHorarios):
        super(Maze, self).__init__()
        self.action_space = ['u', 'd', 'l', 'r', 'tl', 'tr', 'bl', 'br']
        self.n_actions = len(self.action_space)
        self.length_linhas = lengthMap
        self.length_colunas = lengthMap
        self.horariosAgenda = possiveisHorarios
        self.horariosAgendados = []
        self.mapHorarios = []
        self.map =  [["-"] * self.length_colunas for i in range(self.length_linhas)]
        self.preencherMap()
        self.i_column, self.i_line = self.initialPositionAgent()

        
        #Armazena o index das linhas acessadas 
        self.steps_lines = []
        #Armazena o index das colunas acessadas 
        self.steps_columns = []


    def reset(self):
        time.sleep(0.2)
        return [self.i_column, self.i_line]
    
    def restart(self): 
        self.i_column, self.i_line = self.initialPositionAgent()
    
    #Movimentação do Agente
    def step(self, action):
        if action == 0: 
            #Move up
            if self.i_line > 0: 
                aux = self.i_line
                self.i_line -= 1
                if(self.map[self.i_line][self.i_column] == "W" or self.map[self.i_line][self.i_column] == "B"):
                    self.map[self.i_line][self.i_column] += "O"
                self.map[aux][self.i_column] = self.checkState(aux, self.i_column)
            
        elif action == 1:  
            #Move down
            if (self.i_line < self.length_linhas - 1): 
                aux = self.i_line
                self.i_line += 1
                if(self.map[self.i_line][self.i_column] == "W" or self.map[self.i_line][self.i_column] == "B"):
                    self.map[self.i_line][self.i_column] += "O"
                self.map[aux][self.i_column] = self.checkState(aux, self.i_column)
                
        elif action == 2: 
            #Move left
             if (self.i_column > 0): 
                 aux = self.i_column
                 self.i_column -= 1
                 if(self.map[self.i_line][self.i_column] == "W" or self.map[self.i_line][self.i_column] == "B"):
                    self.map[self.i_line][self.i_column] += "O"
                 self.map[self.i_line][aux] = self.checkState(self.i_line, aux)
                 
        elif action == 3: 
            #Move right
             if (self.i_column < self.length_colunas - 1): 
                 aux = self.i_column
                 self.i_column += 1
                 if(self.map[self.i_line][self.i_column] == "W" or self.map[self.i_line][self.i_column] == "B"):
                    self.map[self.i_line][self.i_column] += "O"
                 self.map[self.i_line][aux] = self.checkState(self.i_line, aux)
                 
        elif action == 4: 
        
            #Move top left
            if (self.i_column > 0 and self.i_line > 0): 
                 aux_column = self.i_column
                 aux_line = self.i_line
                 self.i_column -= 1
                 self.i_line -= 1
                 if(self.map[self.i_line][self.i_column] == "W" or self.map[self.i_line][self.i_column] == "B"):
                    self.map[self.i_line][self.i_column] += "O" 
                 self.map[aux_line][aux_column] = self.checkState(aux_line, aux_column)
                 
                
        elif action == 5: 
        
            #Move top right
            if (self.i_column < self.length_colunas - 1 and self.i_line > 0): 
                 aux_column = self.i_column
                 aux_line = self.i_line
                 self.i_column += 1
                 self.i_line -= 1
                 if(self.map[self.i_line][self.i_column] == "W" or self.map[self.i_line][self.i_column] == "B"):
                    self.map[self.i_line][self.i_column] += "O"
                 self.map[aux_line][aux_column] = self.checkState(aux_line, aux_column)
        
        elif action == 6: 
        
            #Move bottom left
            if (self.i_line > self.length_linhas - 1 and self.i_column > 0): 
                 aux_column = self.i_column
                 aux_line = self.i_line
                 self.i_column -= 1
                 self.i_line += 1
                 if(self.map[self.i_line][self.i_column] == "W" or self.map[self.i_line][self.i_column] == "B"):
                    self.map[self.i_line][self.i_column] += "O"
                 self.map[aux_line][aux_column] = self.checkState(aux_line, aux_column)
                 
        elif action == 7: 
        
            #Move top left
            if (self.i_column < self.length_colunas - 1 > 0 and self.i_line < self.length_linhas - 1): 
                 aux_column = self.i_column
                 aux_line = self.i_line
                 self.i_column += 1
                 self.i_line += 1
                 if(self.map[self.i_line][self.i_column] == "W" or self.map[self.i_line][self.i_column] == "B"):
                    self.map[self.i_line][self.i_column] += "O"
                 self.map[aux_line][aux_column] = self.checkState(aux_line, aux_column)
  

        
        resultCheck = False
        for value in self.horariosAgendados: 
            if (value["i_line"] == self.i_line and value["i_column"] == self.i_column): 
                resultCheck = True 
      
                
        if self.map[self.i_line][self.i_column] == "WO" and not resultCheck:
            
            self.horariosAgendados.append(self.search_horario(self.i_line, self.i_column, returnHora=False)) 
            # response = input(f"Deseja estudar no horário de {self.search_horario(self.i_line, self.i_column)} (S/N)?").lower()
            
            # if response == "s":   
            #     reward = 1
            #     self.map[self.i_line][self.i_column] = "W"
            #     done = True
            #     s_ = 'terminal'
            # elif response == "n": 
            #     reward = -1
            #     self.map[self.i_line][self.i_column] = "B"
            #     done = True 
            #     s_ = 'terminal'
            
            horario = self.search_horario(self.i_line, self.i_column)
            reward = 0
            self.map[self.i_line][self.i_column] = "W"
            done = True
            s_ = 'terminal'
            
            self.steps_lines.append(self.i_line)
            self.steps_columns.append(self.i_column)

        elif self.map[self.i_line][self.i_column] == "BO" and not resultCheck:
            
            self.horariosAgendados.append(self.search_horario(self.i_line, self.i_column, returnHora=False)) 
            # response = input(f"Deseja estudar no horário de {self.search_horario(self.i_line, self.i_column)} (S/N)?").lower()
            
            # if response == "s":   
            #     reward = 2
            #     self.map[self.i_line][self.i_column] = "W"
            #     done = True
            #     s_ = 'terminal'
            # elif response == "n": 
            #     reward = -2
            #     self.map[self.i_line][self.i_column] = "B"
            #     done = True 
            #     s_ = 'terminal'
        
            horario = self.search_horario(self.i_line, self.i_column)
            reward = 0
            self.map[self.i_line][self.i_column] = "W"
            done = True
            s_ = 'terminal'
                
        elif self.map[self.i_line][self.i_column] == "BO" and resultCheck: 
            horario = 0
            reward = 0 
            self.map[self.i_line][self.i_column] = "B"   
            done = False
            s_ = 'terminal'

        elif self.map[self.i_line][self.i_column] == "WO" and resultCheck: 
            horario = 0
            reward = 0 
            self.map[self.i_line][self.i_column] = "W"
            done = False
            s_ = 'terminal'
                
                
        else:
            horario = 0
            reward = 0
            s_ = [self.i_column, self.i_line]
            done = False
        
        return s_, reward, done, horario
    
    
    def preencherMap(self): 
        count = 0
        # create ovals matriz - W 
        for i in range(self.length_linhas): 
            for g in range(self.length_colunas): 
                if (g % 2 == 0 and i == 0):
                    if (count < len(self.horariosAgenda)): 
                        
                        self.map[i][g] = "W"
                        self.mapHorarios.append({"hora": self.horariosAgenda[count], "i_line": i, "i_column": g}) 
                        count += 1 
                    else: 
                        break
        for i in range(self.length_linhas): 
            for g in range(self.length_colunas): 
                if (g == self.length_colunas - 1 and i % 2 == 0 and i != 0 and i != self.length_linhas - 1): 
                    if (count < len(self.horariosAgenda)): 
                   
                        self.map[i][g] = "W"
                        self.mapHorarios.append({"hora": self.horariosAgenda[count], "i_line": i, "i_column": g})
                        count += 1 
                    else: 
                        break
        for i in range(self.length_linhas): 
            for g in range(self.length_colunas): 
                if (i == len(self.map) - 1 and g % 2 == 0) :
                    if (count < len(self.horariosAgenda)): 
                      
                        self.map[i][g] = "W"
                        self.mapHorarios.append({"hora": self.horariosAgenda[count], "i_line": i, "i_column": g})
                        count += 1
                    else : 
                        break
        for i in range(self.length_linhas): 
            for g in range(self.length_colunas): 
                if (g == 0 and i % 2 == 0 and i != 0 and i != self.length_linhas - 1): 
                    if (count < len(self.horariosAgenda)): 
                       
                        self.map[i][g] = "W" 
                        self.mapHorarios.append({"hora": self.horariosAgenda[count], "i_line": i, "i_column": g})
                        count += 1 
                    else: 
                        break
                    
    def initialPositionAgent(self): 
        center_index =  ( self.length_colunas - 1 )// 2 
        for i in range(self.length_linhas): 
            for g in range(self.length_colunas): 
                if (g == center_index and i == center_index): 
                    self.map[i][g] = "O"
                    return g, i
                
    def viewMap(self): 
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in range(self.length_linhas): 
            for g in range(self.length_colunas): 
                print(self.map[i][g], end= " ")
            print("\n")
    
    def checkAgenda(self,line, column):
        for value in self.horariosAgendados: 
            if (value["i_line"] == line and value["i_column"] == column): 
                return True 
            return False
        
    def checkState(self,line, column): 
        if self.map[line][column] == "W": 
            return "W"
        elif self.map[line][column] == "B": 
            return "O"
        else: 
            return "-"
    
    def search_horario(self, i_line, i_column, returnHora = True): 
        for i in range(len(self.mapHorarios)): 
            if self.mapHorarios[i]['i_line'] == i_line and self.mapHorarios[i]['i_column'] == i_column: 
                if (returnHora): 
                    return self.mapHorarios[i]["hora"]
                return self.mapHorarios[i]
            