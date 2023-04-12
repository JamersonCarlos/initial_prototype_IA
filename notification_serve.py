from datetime import datetime,timedelta
from firebase_admin import messaging
import threading 

class notification_serve:
    def __init__(self):
        pass
        
    def agendarNotifications(self,uid_message=str, horario=datetime, disciplina=str): 
        
        # Define a mensagem para a notificação push
        message = messaging.Message(
            notification = messaging.Notification(
            title = 'vamos estudar',
            body = 'agendamos um horario para você estudar'
            ),
            token=uid_message,   
        )

        print(f"horario no firebase :"+str(horario))
        intervalo = horario - datetime.now()
        if intervalo.total_seconds() > 0.0:
            threading.Timer(intervalo.total_seconds(), messaging.send, args=[message]).start() 

        return message

        
        

    def cancel_scheduled_notification(self,job_name):
    
        # Exclui o trabalho agendado com o nome especificado
        response = messaging.delete_scheduled_messaging_job(job_name)
        print("Trabalho de notificação agendado com o nome", job_name, "excluído com sucesso.") 