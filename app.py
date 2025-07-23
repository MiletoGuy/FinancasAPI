from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulando um banco de dados em memória
tarefas = [
    {"id": 1, "titulo": "Aprender Flask", "concluida": False},
    {"id": 2, "titulo": "Construir uma API", "concluida": False},
]


@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensagem": "Bem-vindo à API de tarefas!"})


# Rota GET - listar todas as tarefas
@app.route("/tarefas", methods=["GET"])
def listar_tarefas():
    return jsonify(tarefas)

# Rota GET - obter tarefa por ID
@app.route("/tarefas/<int:id>", methods=["GET"])
def obter_tarefa(id):
    tarefa = next((t for t in tarefas if t["id"] == id), None)
    if tarefa:
        return jsonify(tarefa)
    return jsonify({"erro": "Tarefa não encontrada"}), 404

# Rota POST - adicionar uma nova tarefa
@app.route("/tarefas", methods=["POST"])
def criar_tarefa():
    nova = request.get_json()
    nova["id"] = tarefas[-1]["id"] + 1 if tarefas else 1
    tarefas.append(nova)
    return jsonify(nova), 201

# Rota PUT - atualizar uma tarefa existente
@app.route("/tarefas/<int:id>", methods=["PUT"])
def atualizar_tarefa(id):
    tarefa = next((t for t in tarefas if t["id"] == id), None)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    dados = request.get_json()
    tarefa.update(dados)
    return jsonify(tarefa)

# Rota DELETE - remover uma tarefa
@app.route("/tarefas/<int:id>", methods=["DELETE"])
def deletar_tarefa(id):
    global tarefas
    tarefas = [t for t in tarefas if t["id"] != id]
    return jsonify({"mensagem": f"Tarefa {id} removida"}), 200
