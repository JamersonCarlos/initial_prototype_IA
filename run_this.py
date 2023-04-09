"""
Sarsa is a online updating method for Reinforcement learning.

Unlike Q learning which is a offline updating method, Sarsa is updating while in the current trajectory.

You will see the sarsa is more coward when punishment is close because it cares about all behaviours,
while q learning is more brave because it only cares about maximum behaviour.
"""

import ast
from maze_env import Maze
from RL_brain import SarsaTable
import time
import numpy as np
import pandas as pd
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from datetime import datetime

def returnStringHorario(minutos): 
    hor = minutos // 60 
    min = minutos - hor * 60
    return f"{hor}:{min}"

cred = credentials.Certificate('./studyup-584d3-firebase-adminsdk-2gkiq-c2b31ee3b3.json')
firebase_admin.initialize_app(credential=cred)
db = firestore.client()

uid = '4hxFrIxLzDdCzf4AdtcZ5nCazha2'


possiveisQTable = [i for i in range(50) if i % 2 != 0 and i >= 5]
capacidadeQTable = [value for value in range(8, 48 + 1, 4)]
request = db.collection(u'users').stream()
listUsers = [[doc.id, doc.to_dict()] for doc in request]

#Inicio do dia ás 8:00 da manhã e termino do dia ás 22:00
difHoras = [(datetime.strptime("8:00", "%H:%M") - datetime.strptime("22:00", "%H:%M")).total_seconds()/(60) for i in range(7)]
QtdIntervalosPossiveis = [(value//60) for value in difHoras]
lengthMap = []
possiveisHorarios = []

for i in range(7): 
    horaInicioMinutos = datetime.strptime("8:00", "%H:%M").hour * 60 
    horaFinalMinutos = datetime.strptime("22:00", "%H:%M").hour * 60 
    possiveisHorarios.append([returnStringHorario(minutos=value) for value in range(horaInicioMinutos, horaFinalMinutos, 60)])    

interfaces = []

for i in range(7): 
    interfaces.append(Maze(lengthMap=9, possiveisHorarios=possiveisHorarios[i]))
    
qTables = [SarsaTable(actions=list(range(interfaces[i].n_actions)), datafraim=[]) for i in range(len(interfaces))]
metasSemana = [] 
QTableSemana = []


for i in range(7): 
    
    env = interfaces[i]
    RL = qTables[i]
    
    for v in range(6):
        observation = env.reset()    
        
        # RL choose action based on observation
        action = RL.choose_action(str(observation))

        while True:
            
            # RL age e obtém a próxima observação e recompensa
            observation_, reward, done, horaAgendada = env.step(action)

            # RL escolhe a ação com base na próxima observação
            action_ = RL.choose_action(str(observation_))

            # RL learn from this transition (s, a, r, s, a) ==> Sarsa
            RL.learn(str(observation), action, reward, str(observation_), action_)

            # swap observation and action
            saveObservation = observation
            saveAction = action
            observation = observation_
            action = action_

            # break while loop when end of this episode
            if done:
                saveAction = ast.literal_eval(str(saveAction))
                action = ast.literal_eval(str(action))
                metasSemana.append({"dia": i, "horario_meta": horaAgendada, "recompensa": reward, "action_back": saveAction, "action_next": action, "observation_back": saveObservation, "observation_next": observation})
                QTableSemana.append({"dia": i, "DataQTable": str(RL.q_table.values.tolist())})
                break    
        env.restart()
    

db.collection(u'users').document(uid).set({
    u'metas': metasSemana
}, merge=True)

db.collection(u'users').document(uid).set({
    u'QTableIA': QTableSemana
}, merge=True)

print("success")