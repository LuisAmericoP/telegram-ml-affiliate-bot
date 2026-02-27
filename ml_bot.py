import os
import requests
from telegram import Bot

# ====== VARIÁVEIS DE AMBIENTE ======
TOKEN = os.getenv("TOKEN")
CANAL_ID = os.getenv("CANAL_ID")
AFILIADO = os.getenv("AFILIADO")

ML_APP_ID = os.getenv("ML_APP_ID")
ML_CLIENT_SECRET = os.getenv("ML_CLIENT_SECRET")
ML_REFRESH_TOKEN = os.getenv("ML_REFRESH_TOKEN")

bot = Bot(token=TOKEN)


# ====== ATUALIZAR ACCESS TOKEN ======
def atualizar_token():
    url = "https://api.mercadolibre.com/oauth/token"

    payload = {
        "grant_type": "refresh_token",
        "client_id": ML_APP_ID,
        "client_secret": ML_CLIENT_SECRET,
        "refresh_token": ML_REFRESH_TOKEN
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    print("Refresh status:", response.status_code)
    print("Refresh response:", response.text)

    if response.status_code != 200:
        return None

    data = response.json()
    return data.get("access_token")


# ====== BUSCAR PRODUTO ======
def buscar_produto(query="notebook"):
    access_token = atualizar_token()

    if not access_token:
        print("Erro ao atualizar token")
        return None

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}"

    response = requests.get(url, headers=headers)

    print("Busca status:", response.status_code)

    if response.status_code != 200:
        print("Erro ao buscar produto:", response.text)
        return None

    data = response.json()

    if "results" not in data or len(data["results"]) == 0:
        print("Nenhum produto encontrado")
        return None

    return data["results"][0]


# ====== ENVIAR PARA TELEGRAM ======
def enviar_produto():
    produto = buscar_produto("notebook")

    if not produto:
        return

    titulo = produto["title"]
    preco = produto["price"]
    link = produto["permalink"]

    link_afiliado = f"{link}?matt_tool={AFILIADO}"

    mensagem = f"""
🔥 {titulo}

💰 Preço: R$ {preco}

🛒 Comprar agora:
{link_afiliado}
"""

    bot.send_message(chat_id=CANAL_ID, text=mensagem)

    print("Produto enviado com sucesso!")


# ====== EXECUTAR ======
if __name__ == "__main__":
    enviar_produto()
