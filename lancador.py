import msal
import requests
import json
import os
from msal import SerializableTokenCache

# Caminho do arquivo onde o cache será salvo
CACHE_PATH = "token_cache.json"

# === CONFIGURAÇÕES ===
CLIENT_ID = "40806653-a5ec-43a1-b3a9-cdd38b1ff378"
TENANT_ID = "consumers"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPES = ["Files.ReadWrite", "User.Read"]

EXCEL_FILE_ID = "762E8B9DC95EFC50!s2ef358514d2f429c9a71afe74ede77c3"  # ID correto da sua planilha
TABLE_NAME = "Lancamentos"  # Nome da tabela no Excel

def processar_lancamento(dados):
    """
    Recebe um dicionário com os campos:
    data, fatura, descricao, tipo, forma, categoria, valor
    """
    row_data = [[
        dados.get("data"),
        dados.get("fatura"),
        dados.get("descricao"),
        dados.get("tipo"),
        dados.get("forma"),
        dados.get("categoria"),
        dados.get("valor")
    ]]

    # === INICIALIZA TOKEN CACHE ===
    token_cache = SerializableTokenCache()
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            token_cache.deserialize(f.read())

    app = msal.PublicClientApplication(
        client_id=CLIENT_ID,
        authority=AUTHORITY,
        token_cache=token_cache
    )

    # === TENTA USAR TOKEN EXISTENTE ===
    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])
    else:
        result = None

    # === SE PRECISAR, FAZ LOGIN COM DEVICE CODE ===
    if not result:
        flow = app.initiate_device_flow(scopes=SCOPES)
        if "user_code" not in flow:
            raise Exception("Falha ao iniciar device flow.")
        print(f"Acesse {flow['verification_uri']} e insira o código: {flow['user_code']}")
        result = app.acquire_token_by_device_flow(flow)

    if "access_token" not in result:
        raise Exception("Erro na autenticação: " + str(result))

    access_token = result["access_token"]

    # === SALVA TOKEN CACHE SE ALTERADO ===
    if token_cache.has_state_changed:
        with open(CACHE_PATH, "w") as f:
            f.write(token_cache.serialize())

    # === ENVIA OS DADOS PARA O EXCEL ===
    url = f"https://graph.microsoft.com/v1.0/me/drive/items/{EXCEL_FILE_ID}/workbook/tables/{TABLE_NAME}/rows/add"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "values": row_data
    }

    response = requests.post(url, headers=headers, data=json.dumps(body))

    if response.status_code == 201:
        print("✅ Lançamento inserido com sucesso!")
    else:
        raise Exception(f"Erro ao inserir lançamento: {response.status_code}\n{response.text}")
