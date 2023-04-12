from flask import Flask, request
import main as IA

app = Flask(__name__)

@app.route('/firstLogin/<uid>')
def primerioLogin(uid):
    IA.FirstUpdate(uid)   
    return 'chamar alocação para criar o objeto de metas'

@app.route('/updatePriorit/<id>')
def updatepriorit(id):
    IA.alocarDisciplina(id)
    return '',200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

