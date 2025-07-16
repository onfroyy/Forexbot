
import time, json
from estrategia import analizar_mercado
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

# Cargar configuración
with open("config.json", "r") as f:
    config = json.load(f)

API_KEY = config["API_KEY"]
SECRET_KEY = config["SECRET_KEY"]
SYMBOLS = config["SYMBOLS"]
MONTO = config["MONTO"]

client = TradingClient(API_KEY, SECRET_KEY, paper=True)

# Bucle principal
while True:
    print("🔄 Analizando mercado...")
    for symbol in SYMBOLS:
        resultado = analizar_mercado(symbol)
        print(f"📊 Resultado en {symbol}: {resultado}")

        if resultado == "COMPRA":
            try:
                order = MarketOrderRequest(
                    symbol=symbol.split("/")[0],
                    qty=MONTO,
                    side=OrderSide.BUY,
                    time_in_force=TimeInForce.GTC
                )
                client.submit_order(order)
                print(f"✅ COMPRA ejecutada en {symbol}")
            except Exception as e:
                print(f"❌ Error al comprar {symbol}: {e}")

        elif resultado == "VENTA":
            try:
                order = MarketOrderRequest(
                    symbol=symbol.split("/")[0],
                    qty=MONTO,
                    side=OrderSide.SELL,
                    time_in_force=TimeInForce.GTC
                )
                client.submit_order(order)
                print(f"✅ VENTA ejecutada en {symbol}")
            except Exception as e:
                print(f"❌ Error al vender {symbol}: {e}")

    time.sleep(60 * 5)
