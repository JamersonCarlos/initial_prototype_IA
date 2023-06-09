from datetime import datetime, timedelta
from flask import Flask, request
import main as IA
from notification_serve import notification_serve as msg
import refreashIA as refreash

app = Flask(__name__)

refreash.start_thread(IA.updateAllUsers)  #atualiza base de dados toda segunda #

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
    IA.sendMensageTeste(id)
    return 'sua menssagem veio da ia',200


if __name__ == "__main__":
    app.run(host="192.168.0.106 ", port=8000)


