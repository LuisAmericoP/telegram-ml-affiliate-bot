import os
import requests
from telegram import Bot

# ====== VARIÁVEIS DE AMBIENTE ======
TOKEN = os.getenv("TOKEN")
CANAL_ID = os.getenv("CANAL_ID")
AFILIADO = os.getenv("AFILIADO")
ML_APP_ID = os.getenv("ML_APP_ID")
ML_CLIENT_SECRET = os.getenv("ML_CLIENT_SECRET")
REDIRECT_URI = os.getenv("URL_DO_PAINEL")
CODIGO_TG = os.getenv("CODIGO_TG")

bot = Bot(token=TOKEN)

# ====== GERAR TOKEN MERCADO LIVRE ======
def gerar_token():
    url = "https://api.mercadolibre.com/oauth/token"

    payload = {
       "grant_type": "authorization_code",
        "client_id": ML_APP_ID,
        "client_secret": ML_CLIENT_SECRET,
        "code": CODIGO_TG, 
        "redirect_uri": URL_DO_PAINEL 
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    print("Token status:", response.status_code)
    print("Token response:", response.text)

    if response.status_code != 200:
        return None

    return response.json().get("access_token")

# ====== BUSCAR PRODUTO ======
def buscar_produto(query="notebook"):
    access_token = gerar_token()

    if not access_token:
        print("Erro ao gerar token")
        return None

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    url = f"https://api.mercadolibre.com/sites/MLB/search?q={query}"

    response = requests.get(url, headers=headers)

    print("Busca status:", response.status_code)
    print("Busca resposta:", response.text)

    if response.status_code != 200:
        print("Erro ao buscar produto")
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

    # Gera link afiliado
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
