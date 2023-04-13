from datetime import datetime, timedelta
from flask import Flask, request
import main as IA
from notification_serve import notification_serve as msg

app = Flask(__name__)

@app.route('/firstLogin/<uid>')
def primerioLogin(uid):
    IA.FirstUpdate(uid)   
    return 'chamar alocação para criar o objeto de metas'

@app.route('/updatePriorit/<id>')
def updatepriorit(id):
    IA.alocarDisciplina(id)
    return '',200

@app.route('/sendnotificaion/<id>')
def sendnotificaion(id):
    msg.agendarNotifications(horario=datetime.now()+timedelta(seconds=10),uid_message='yqEenvOBLDPwiX1bwRY8KpfMMmQ2')
    return 'sua menssagem veio da ia',200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

