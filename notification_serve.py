from datetime import datetime,timedelta
from firebase_admin import messaging
import threading 

class notification_serve:
    def __init__(self):
        pass
        
    def agendarNotifications(self,uid_message=str, horario=datetime): 
        
        # Define a mensagem para a notificação push
        message = messaging.Message(
            notification = messaging.Notification(
            title = 'vamos estudar',
            body = 'agendamos um horario para você estudar',
            payload='pomodoro'
            ),
            token=uid_message,   
        )

        # Define o horário para o trabalho agendado
        intervalo = horario - datetime.now()
        if intervalo.total_seconds() > 0.0:
            threading.Timer(intervalo.total_seconds(), messaging.send, args=[message]).start() 

        return message

        
        