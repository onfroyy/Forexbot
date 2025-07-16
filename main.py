
import time
import requests
import pandas as pd
import json
from estrategia import analizar_mercado

with open("config.json", "r") as f:
    config = json.load(f)

SYMBOLS = config["SIMBOLOS"]
MONTO = config["MONTO"]

def obtener_datos(symbol):
    try:
        url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
        params = {"vs_currency": "usd", "days": "1", "interval": "minutely"}
        response = requests.get(url, params=params)
        data = response.json()

        precios = data.get("prices", [])
        if not precios:
            raise ValueError("No hay precios")

        df = pd.DataFrame(precios, columns=["timestamp", "close"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.set_index("timestamp", inplace=True)
        return df
    except Exception as e:
        print(f"⚠️ Error analizando {symbol}: {e}")
        return None

while True:
    print("🔄 Analizando mercado...")
    for simbolo in SYMBOLS:
        df = obtener_datos(simbolo)
        if df is not None:
            resultado = analizar_mercado(df)
            print(f"📊 Resultado en {simbolo.upper()}: {resultado}")
        else:
            print(f"❌ No se pudo analizar {simbolo.upper()}")
    time.sleep(60 * 5)
