import ast
import random

from click import DateTime
from maze_env import Maze
from RL_brain import SarsaTable
import time
import numpy as np
import pandas as pd
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import messaging
from datetime import datetime
import json
from datetime import timedelta, date
import threading
from notification_serve import notification_serve as msg


#Convert minutos em horas 
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
    
    dataAtual = datetime.now()
    dataInicio = (dataAtual - timedelta(dataAtual.weekday())).date()

    for i in range(7): 
        
        env = interfaces[i]
        RL = qTables[i]
        
        dif = dataInicio.day - dataAtual.day
        if (dif < 0): 
            recompensa = 0 
        else: 
            recompensa = -2 
        
        for v in range(6):
            observation = env.reset()    
            
            # RL choose action based on observation-
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
                    metasSemana.append({"dia": i, "horario_meta": horaAgendada, "recompensa": recompensa, "action_back": saveAction, "action_next": action, "observation_back": saveObservation, "observation_next": observation, "disciplina": "", "dataMeta": str(dataInicio)})
                    QTableSemana.append({"dia": i, "DataQTable": str(RL.q_table.values.tolist())})
                    break    
            env.restart()
        dataInicio = dataInicio + timedelta(1)

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
    
    dataAtual = datetime.now()
    dataInicio = (dataAtual - timedelta(dataAtual.weekday())).date()
    

    for i in range(7): 
        
        env = interfaces[i]
        RL = qTables[i]
        
        dif = dataInicio.day - dataAtual.day
        if (dif < 0): 
            recompensa = 0 
        else: 
            recompensa = -2 
        
        
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
                    metasSemana.append({"dia": i, "horario_meta": horaAgendada, "recompensa": recompensa, "action_back": saveAction, "action_next": action, "observation_back": saveObservation, "observation_next": observation, "disciplina": "", "dataMeta": str(dataInicio)})
                    QTableSemana.append({"dia": i, "DataQTable": str(RL.q_table.values.tolist())})
                    break    
            env.restart()
            
        dataInicio = dataInicio + timedelta(1)


    db.collection(u'users').document(uid).set({
        u'metas': metasSemana
    }, merge=True)

    db.collection(u'users').document(uid).set({
        u'QTableIA': QTableSemana
    }, merge=True)

#Ao final da semana atualiza todos os horários e carrega os resultados 
def updateAllUsers():
    request = db.collection(u'users').stream()
    listUsers = [doc.id for doc in request]
    for user in listUsers: 
        updateMetaUser(user)

#Aloca disciplina tendo em vista a quantidade de horas por semana para dedicação
def alocarDisciplina(uid):         
    #Pega todos os usuários do banco de dados 
    request = db.collection(u'users').stream()
    user = [[doc.id, doc.to_dict()] for doc in request if doc.id == "yqEenvOBLDPwiX1bwRY8KpfMMmQ2"]
    titleSubjects = [subject["title"] for subject in user[0][1]["disciplinas"]]
    # weightSubjects = [(subject["horas_dedicadas_por_semana"]/50) * 100 for subject in user[0][1]["disciplinas"] ]
    weightSubjects = []
    for k in range(len(user[0][1]["disciplinas"]), 0, -1): 
        prioriti = (k/len(user[0][1]["disciplinas"])) * 100
        if (prioriti == 100): 
            prioriti = 80 
        if (prioriti > 80): 
            prioriti = prioriti - (prioriti - 80) - 2
        weightSubjects.append(prioriti)
    
    #Em caso de 1 Disciplina cadastrada 
    if len(titleSubjects) == 1: 
        randomList = random.choices(titleSubjects, weights=weightSubjects, k= 21)
        #Dias da semana
        for k in range(7): 
            #Contador de metas diárias
            countMetasDiarias = 0
            for i in range(len(user[0][1]["metas"])): 
                if user[0][1]["metas"][i]["dia"] == k and countMetasDiarias < 3: 
                    #Alocando disciplina
                    user[0][1]["metas"][i]["disciplina"] = randomList[i]
                    countMetasDiarias += 1
    #Em caso de 2 ou mais Disciplinas cadastradas
    else: 
        randomList = random.choices(titleSubjects, weights=weightSubjects, k= 42)
        #Dias da semana 
        for k in range(7): 
            #Contador de metas diárias 
            countMetasDiarias = 0
            for i in range(len(user[0][1]["metas"])): 
                if user[0][1]["metas"][i]["dia"] == k and countMetasDiarias < 6: 
                    #Alocando Disciplina
                    user[0][1]["metas"][i]["disciplina"] = randomList[i]
                    countMetasDiarias += 1
    
    #Atualizado banco de dados 
    db.collection(u'users').document(user[0][0]).set({ 
        u'metas': user[0][1]["metas"]
    }, merge=True)




def send_notification(id):
    request = db.collection(u'users').document(id).get().to_dict()['metas']
    id_notification = db.collection(u'users').document(id).get().to_dict()['TokenMessaging']
    print(id_notification)
    datasUser = [value["dataMeta"] for value in request]
    horasUser = [value["horario_meta"] for value in request]
    datas_fomarted = merge_data_with_hrs(datasUser=datasUser,horasUser=horasUser)
    for i in range(len(datas_fomarted)):                                    
        msg().agendarNotifications(uid_message=id_notification, horario=datas_fomarted[i])

    return     
   
        
def merge_data_with_hrs(datasUser,horasUser): 
    datetime_object = []
    for i in range(len(horasUser)):
        data = datasUser[i]+"-"+horasUser[i]
        datetime_object.append(datetime.strptime(data, '%Y-%m-%d-%H:%M'))
        
    return datetime_object



def sendMensageTeste(id):
    id_notification = db.collection(u'users').document(id).get().to_dict()['TokenMessaging']
    msg().agendarNotifications(uid_message=id_notification, horario=datetime.now() + timedelta(seconds=10))
    return True



