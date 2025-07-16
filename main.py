import time
import json
import requests
from alpaca.data.historical import CryptoHistoricalDataClient
from estrategia import analizar_mercado

# ========= CONFIGURACIÓN ==========
with open("config.json") as f:
    config = json.load(f)

API_KEY = config["API_KEY"]
SECRET_KEY = config["SECRET_KEY"]
BASE_URL = config["BASE_URL"]
DATA_URL = config["DATA_URL"]
SYMBOLS = config["SYMBOLS"]
MONTO = config["MONTO"]

TG_TOKEN = "8150581922:AAEQUSrzHHpK31NmZ4DbCOjSE7iS-uyOgt0"
TG_CHAT_ID = "1517821730"

# ========= CONEXIÓN A ALPACA DATA ==========
api = CryptoHistoricalDataClient(API_KEY, SECRET_KEY)

# ========= FUNCIONES ==========
def enviar_telegram(mensaje):
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        data = {"chat_id": TG_CHAT_ID, "text": mensaje}
        requests.post(url, data=data)
    except Exception as e:
        print(f"❌ Error al enviar a Telegram: {e}")

# ========= CICLO PRINCIPAL ==========
while True:
    print("⏳ Analizando mercado...")
    for simbolo in SYMBOLS:
        resultado = analizar_mercado(api, simbolo)
        tipo = resultado["tipo"]

        if tipo != "NO_ENTRADA":
            mensaje = (
                f"📈 Señal detectada en {simbolo}:\n"
                f"🔸 Tipo: {tipo}\n"
                f"🎯 Entrada: {resultado['entrada']}\n"
                f"✅ TP: {resultado['tp']}\n"
                f"❌ SL: {resultado['sl']}"
            )
            print(mensaje)
            enviar_telegram(mensaje)
        else:
            print(f"🔍 Sin oportunidad en {simbolo}")

    time.sleep(300)  # Espera 5 minutos
