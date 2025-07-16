import time
from estrategia import analizar_mercado

SYMBOLS = ["bitcoin", "ethereum"]

while True:
    print("🔄 Analizando mercado...")
    for simbolo in SYMBOLS:
        resultado = analizar_mercado(simbolo)
        print(f"📊 Resultado en {simbolo.upper()}: {resultado}")
    time.sleep(60 * 5)
