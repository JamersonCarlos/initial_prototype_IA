from sqlite_db import SqliteDB
from flask import Flask, jsonify, request
import app as IA

app = Flask(__name__)
bd = SqliteDB()  # instanciando a classe SqliteDB



@app.route('firstLogin/<id>')
def primerioLogin():   
    return 'chamar alocação para criar o objeto de metas'



#@app.route('/cadastrarUser/<idUser>', methods=['POST','GET']) #talvez não precise# 
#def add_novo_user(idUser, id_notification):
#    res = bd.casdastrar_novo_user(idUser, id_notification)
#    if res:
#        return 'Usuário cadastrado com sucesso',204
#    return 'Não foi possivel cadastrar este usuario', 404



@app.route('deletedisciplina/<id>/<disciplina>') #vai pagar o objeto disciplina e remover o nome das metas #
def deletedisciplina(id,disciplina):
    AI.deletedisciplina(id,disciplina)
    return '',200

@app.route('updatePriorit/<id>')
def updatepriorit(id):
    IA.alocardispliciplina(id)
    return '',200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)