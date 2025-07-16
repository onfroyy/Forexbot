
import requests
import pandas as pd

def calcular_rsi(data, period=14):
    delta = data.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def analizar_mercado(simbolo):
    try:
        symbol = simbolo.split("/")[0]
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=5m&range=1d"
        response = requests.get(url)
        data = response.json()

        close_prices = data["chart"]["result"][0]["indicators"]["quote"][0]["close"]
        df = pd.DataFrame(close_prices, columns=["close"]).dropna()
        df["EMA200"] = df["close"].ewm(span=200).mean()
        df["RSI"] = calcular_rsi(df["close"])

        ultima = df.iloc[-1]
        anterior = df.iloc[-2]
        previa = df.iloc[-3]

        if ultima["close"] > ultima["EMA200"] and ultima["RSI"] < 30:
            if ultima["close"] > anterior["close"] > previa["close"]:
                return "COMPRA"
        elif ultima["close"] < ultima["EMA200"] and ultima["RSI"] > 70:
            if ultima["close"] < anterior["close"] < previa["close"]:
                return "VENTA"

        return "NO_ENTRADA"
    except Exception as e:
        print(f"⚠️ Error analizando {simbolo}: {e}")
        return "NO_ENTRADA"
