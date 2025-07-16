import json, time, requests
import pandas as pd
from estrategia import analizar_mercado
from alpaca_trade_api.rest import REST

def ejecutar_orden(api, simbolo, tipo, cantidad, sl, tp):
    print(f"📈 Ejecutando {tipo} en {simbolo} con SL={sl} y TP={tp}")
    try:
        orden = api.submit_order(
            symbol=simbolo,
            qty=cantidad,
            side="buy" if tipo == "COMPRA" else "sell",
            type="market",
            time_in_force="gtc"
        )
        print(f"✅ Orden enviada: {orden.id}")
    except Exception as e:
        print(f"❌ Error al enviar orden: {e}")

with open("config.json") as f:
    config = json.load(f)

api = REST(config["API_KEY"], config["SECRET_KEY"], base_url=config["BASE_URL"])

while True:
    for simbolo in config["SYMBOLS"]:
        print(f"🔍 Analizando {simbolo}...")
        resultado = analizar_mercado(api, simbolo)

        if resultado == "COMPRA":
            ejecutar_orden(api, simbolo, "COMPRA", config["MONTO"], sl=0.98, tp=1.05)
        elif resultado == "VENTA":
            ejecutar_orden(api, simbolo, "VENTA", config["MONTO"], sl=1.02, tp=0.95)
        else:
            print(f"🕵️‍♂️ Sin oportunidad en {simbolo}")
        time.sleep(10)
