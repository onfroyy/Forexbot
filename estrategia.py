import pandas as pd
import requests

def obtener_datos(simbolo):
    url = f"https://api.coingecko.com/api/v3/coins/{simbolo}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "1",
        "interval": "minute"
    }
    response = requests.get(url, params=params)
    data = response.json()

    precios = data["prices"]  # [[timestamp, price], ...]
    df = pd.DataFrame(precios, columns=["timestamp", "close"])
    df["close"] = df["close"].astype(float)
    return df

def calcular_rsi(series, period=14):
    delta = series.diff()
    ganancia = delta.clip(lower=0)
    perdida = -delta.clip(upper=0)
    media_gan = ganancia.rolling(window=period).mean()
    media_per = perdida.rolling(window=period).mean()
    rs = media_gan / media_per
    return 100 - (100 / (1 + rs))

def analizar_mercado(simbolo):
    try:
        df = obtener_datos(simbolo)
        if len(df) < 200:
            return "NO_ENTRADA"

        df["EMA200"] = df["close"].ewm(span=200).mean()
        df["RSI"] = calcular_rsi(df["close"])

        ultima = df.iloc[-1]
        anterior = df.iloc[-2]
        anteanterior = df.iloc[-3]

        if ultima["close"] > ultima["EMA200"] and ultima["RSI"] < 30:
            if ultima["close"] > anterior["close"] and anterior["close"] < anteanterior["close"]:
                return "COMPRA ✅"
        elif ultima["close"] < ultima["EMA200"] and ultima["RSI"] > 70:
            if ultima["close"] < anterior["close"] and anterior["close"] > anteanterior["close"]:
                return "VENTA 🔻"
        else:
            return "NO_ENTRADA"
    except Exception as e:
        print(f"⚠️ Error analizando {simbolo}: {e}")
        return "NO_ENTRADA"
