import time, json
from estrategia import analizar_mercado
from alpaca.data.historical import CryptoHistoricalDataClient

# Cargar configuración
with open("config.json", "r") as f:
    config = json.load(f)

API_KEY = config["API_KEY"]
SECRET_KEY = config["SECRET_KEY"]
SYMBOLS = config["SYMBOLS"]
MONTO = config["MONTO"]

# Conectar a Alpaca
api = CryptoHistoricalDataClient(API_KEY, SECRET_KEY)

# Bucle principal
while True:
    print("🔄 Analizando mercado...")
    for simbolo in SYMBOLS:
        resultado = analizar_mercado(api, simbolo)
        print(f"📊 Resultado en {simbolo}: {resultado}")
    time.sleep(60 * 5)
