import time, json
import pandas as pd
from estrategia import analizar_mercado
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

# Cargar configuración
with open("config.json", "r") as f:
    config = json.load(f)

API_KEY = config["API_KEY"]
SECRET_KEY = config["SECRET_KEY"]
SYMBOLS = config["SYMBOLS"]

client = StockHistoricalDataClient(API_KEY, SECRET_KEY)

while True:
    print("🔄 Analizando mercado...")
    for simbolo in SYMBOLS:
        try:
            request_params = StockBarsRequest(
                symbol_or_symbols=simbolo,
                timeframe=TimeFrame.Minute,
                limit=300
            )
            bars = client.get_stock_bars(request_params).df
            df = bars[bars['symbol'] == simbolo]
            resultado = analizar_mercado(df)
            print(f"📈 Resultado en {simbolo}: {resultado}")
        except Exception as e:
            print(f"⚠️ Error analizando {simbolo}: {e}")
    time.sleep(300)