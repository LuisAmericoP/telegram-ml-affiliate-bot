import requests
import os
from telegram import Bot

TOKEN = os.getenv("8795534220:AAEPWrJw7gVtqGOVIGoy9kob7f6K2sGLjLg")
CANAL_ID = os.getenv("https://t.me/achadosmercadolivrezk")
AFILIADO = os.getenv("11751955")

bot = Bot(token=TOKEN)

url = "https://api.mercadolibre.com/sites/MLB/search?q=notebook&limit=1"
response = requests.get(url)
data = response.json()

if "results" in data and len(data["results"]) > 0:
    produto = data["results"][0]
else:
    print("Erro ao buscar produto")
    exit()

titulo = produto["title"]
preco = produto["price"]
link = produto["permalink"]

link_afiliado = f"{link}?matt_tool={AFILIADO}"

mensagem = f"""
🔥 {titulo}

💰 R$ {preco}

🛒 Compre aqui:
{link_afiliado}
"""

bot.send_message(chat_id=CANAL_ID, text=mensagem)

print("Postado com sucesso!")
