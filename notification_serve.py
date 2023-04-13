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
            title = 'vamos estudar<API>',
            body = 'agendamos um horario para você estudar',
            
            ),
            token=uid_message,   
        )

        # Define o horário para o trabalho agendado
        intervalo = horario - datetime.now()
        print(f"token = "+uid_message)
        if intervalo.total_seconds() > 0.0:
            print(intervalo.total_seconds())
            threading.Timer(intervalo.total_seconds(), messaging.send, args=[message]).start() 

        return message

        
        