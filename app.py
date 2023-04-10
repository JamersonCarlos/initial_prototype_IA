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
import json

def returnStringHorario(minutos): 
    hor = minutos // 60 
    min = minutos - hor * 60
    return f"{hor}:{min}"

cred = credentials.Certificate('./studyup-584d3-firebase-adminsdk-2gkiq-c2b31ee3b3.json')
firebase_admin.initialize_app(credential=cred)
db = firestore.client()

#Primeira Definição de metas para novos usuários 
def FirstUpdate(uid): 
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
                    metasSemana.append({"dia": i, "horario_meta": horaAgendada, "recompensa": -2, "action_back": saveAction, "action_next": action, "observation_back": saveObservation, "observation_next": observation, "disciplina": ""})
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

#Atualização das metas de um usuário(uid)
def updateMetaUser(uid):     
    request = db.collection(u'users').document(uid).get().to_dict()
    diasSemana = [ast.literal_eval(value["DataQTable"]) for value in request["QTableIA"]]
    mapRecompensas = [value for value in request["metas"]]

    possiveisHorarios = []

    for i in range(7): 
        horaInicioMinutos = datetime.strptime("8:00", "%H:%M").hour * 60 
        horaFinalMinutos = datetime.strptime("22:00", "%H:%M").hour * 60 
        possiveisHorarios.append([returnStringHorario(minutos=value) for value in range(horaInicioMinutos, horaFinalMinutos, 60)])    

    interfaces = []

    for i in range(7): 
            interfaces.append(Maze(lengthMap=9, possiveisHorarios=possiveisHorarios[i]))
            
    qTables = [SarsaTable(actions=list(range(interfaces[i].n_actions)), datafraim=diasSemana[i]) for i in range(len(interfaces))]

    count = 0

    #Update ambiente de aprendizagem 
    for i in range(7): 
        print(f'--------------------------{i}----------------------------')
        while(count <= 41 and mapRecompensas[count]["dia"] == i):
            observation = mapRecompensas[count]["observation_back"]
            action = np.int64(mapRecompensas[count]["action_back"])
            recompensa = mapRecompensas[count]["recompensa"]
            _observation = mapRecompensas[count]["observation_next"]
            _action = np.int64(mapRecompensas[count]["action_next"])
            qTables[i].learn(observation, action, recompensa, _observation, _action)
            count+=1

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
                    metasSemana.append({"dia": i, "horario_meta": horaAgendada, "recompensa": -2, "action_back": saveAction, "action_next": action, "observation_back": saveObservation, "observation_next": observation, "disciplina": ""})
                    QTableSemana.append({"dia": i, "DataQTable": str(RL.q_table.values.tolist())})
                    break    
            env.restart()
        

    db.collection(u'users').document(uid).set({
        u'metas': metasSemana
    }, merge=True)

    db.collection(u'users').document(uid).set({
        u'QTableIA': QTableSemana
    }, merge=True)


def updateAllUsers():
    request = db.collection(u'users').stream()
    listUsers = [doc.id for doc in request]
    for user in listUsers: 
        updateMetaUser(user)
    
def alocarDisciplina():         
    pass 

def deleteDisciplina(): 
    pass

def agendarNotifications(): 
    pass