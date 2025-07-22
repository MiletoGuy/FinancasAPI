from flask import Flask, request, jsonify
from lancador import processar_lancamento

app = Flask(__name__)

@app.route('/')
def home():
    return "API funcionando no Azure!"

@app.route("/lancar", methods=["POST"])
def lancar():
    data = request.get_json()
    if not data:
        return jsonify({"erro": "JSON inválido"}), 400
    try:
        processar_lancamento(data)
        return jsonify({"status": "OK", "mensagem": "Lançamento processado."})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
