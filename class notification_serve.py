from datetime import datetime
from firebase_admin import credentials, messaging

class notification_serve:
    def __main__(self,crendentials_firebase=messaging):
        self.crendentials_firebase = crendentials_firebase
        
    
def agendarNotifications(self,uid=str, horario=datetime, disciplina=str): 
    
    # Define a mensagem para a notificação push
    message = self.credentials_firebase.messaging.Message(
        data={
            "title": "vamos estudar"+disciplina.str(),
            "body": "Marcamos 1 hora de estudo para você!!",
        },
        token=uid,
    )

    # Define a data e hora para enviar a mensagem
    datetime_obj = datetime.fromisoformat(horario)
    schedule_time = self.credentials_firebase.messaging.ScheduleTime(timestamp_millis=int(datetime_obj.timestamp() * 1000))

    # Envia a mensagem
    response = self.credentials_firebase.messaging.send(message, app=None, dry_run=False, schedule=schedule_time)
    print("Mensagem enviada: ", response)
    return response


def convertStringToDatetime(dia,horas):
    ano_atual = datetime.datetime.now().year
    mes_atual = datetime.datetime.now().month
    data = datetime.datetime(ano_atual, mes_atual, dia, horas)
    return data
    


def cancel_scheduled_notification(self,job_name):
  
    # Exclui o trabalho agendado com o nome especificado
    response = self.credentials_firebase.messaging.delete_scheduled_messaging_job(job_name)
    print("Trabalho de notificação agendado com o nome", job_name, "excluído com sucesso.") 