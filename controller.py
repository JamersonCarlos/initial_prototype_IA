from flask import Flask, request
import app as IA

app = Flask(__name__)

@app.route('firstLogin/<uid>')
def primerioLogin(uid):
    IA.FirstUpdate(uid)   
    return 'chamar alocação para criar o objeto de metas'


@app.route('deletedisciplina/<id>/<disciplina>',methods=['POST']) #vai pagar o objeto disciplina e remover o nome das metas #
def deletedisciplina(id,disciplina):
    IA.deleteDisciplina(id,disciplina)
    return '',200


@app.route('updatePriorit/<id>')
def updatepriorit(id):
    IA.alocardispliciplina(id)
    return '',200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)