import time, json
import requests
import pandas as pd
from estrategia import analizar_mercado

# Cargar configuración
with open("config.json", "r") as f:
    config = json.load(f)

API_KEY = config["API_KEY"]
SECRET_KEY = config["SECRET_KEY"]
SYMBOLS = config["SYMBOLS"]
MONTO = config["MONTO"]
DATA_URL = config["DATA_URL"]

HEADERS = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": SECRET_KEY
}

def obtener_datos_cripto(symbol):
    url = f"{DATA_URL}/v1beta3/crypto/us/bars"
    params = {
        "symbols": symbol,
        "timeframe": "5Min",
        "limit": 200
    }
    try:
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            data = response.json()
            bars = data['bars'][symbol]
            df = pd.DataFrame(bars)
            df.rename(columns={'t': 'timestamp', 'c': 'close'}, inplace=True)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
            return df
        else:
            print(f"❌ Error al obtener datos de {symbol}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"⚠️ Error inesperado en {symbol}: {e}")
        return None

# Bucle principal
while True:
    print("🔄 Analizando mercado...")
    for simbolo in SYMBOLS:
        df = obtener_datos_cripto(simbolo)
        if df is not None:
            resultado = analizar_mercado(df)
            print(f"📊 Resultado en {simbolo}: {resultado}")
        else:
            print(f"⛔ No se pudo analizar {simbolo}")
    time.sleep(60 * 5)
