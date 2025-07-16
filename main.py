from estrategia import analizar_mercado
import requests, time, json
import alpaca_trade_api as tradeapi

# Cargar configuración
with open('config.json') as f:
    config = json.load(f)

API_KEY = config["API_KEY"]
SECRET_KEY = config["SECRET_KEY"]
BASE_URL = config["BASE_URL"]
SIMBOLOS = config["SYMBOLS"]
MONTO = config["MONTO"]

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL, api_version='v2')

def ejecutar_bot():
    while True:
        try:
            reloj = time.strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{reloj}] ⏳ Analizando mercado...")
            for simbolo in SIMBOLOS:
                resultado = analizar_mercado(api, simbolo)
                if resultado in ["COMPRA", "VENTA"]:
                    lado = 'buy' if resultado == "COMPRA" else 'sell'
                    precio_actual = api.get_last_trade(simbolo).price
                    stop_loss = round(precio_actual * 0.99, 2) if lado == 'buy' else round(precio_actual * 1.01, 2)
                    take_profit = round(precio_actual * 1.02, 2) if lado == 'buy' else round(precio_actual * 0.98, 2)

                    api.submit_order(
                        symbol=simbolo,
                        notional=MONTO,
                        side=lado,
                        type='market',
                        time_in_force='gtc',
                        order_class='bracket',
                        take_profit={'limit_price': take_profit},
                        stop_loss={'stop_price': stop_loss}
                    )
                    print(f"[{reloj}] ✅ {resultado} ejecutada en {simbolo} | TP: {take_profit} | SL: {stop_loss}")
                else:
                    print(f"[{reloj}] 🔍 Sin oportunidad en {simbolo}")
            time.sleep(60)
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    ejecutar_bot()
