import pandas as pd
import requests

def analizar_mercado(api, simbolo):
    try:
        df = api.get_crypto_bars([simbolo], timeframe="5Min").df
        df = df[df['symbol'] == simbolo]

        df['EMA200'] = df['close'].ewm(span=200).mean()
        df['RSI'] = calcular_rsi(df['close'])

        if len(df) < 3:
            return "NO_ENTRADA"

        ultima = df.iloc[-1]
        anterior = df.iloc[-2]

        if ultima['close'] > ultima['EMA200'] and ultima['RSI'] < 30:
            if ultima['close'] > anterior['close'] and anterior['close'] < df.iloc[-3]['close']:
                return "COMPRA"
        if ultima['close'] < ultima['EMA200'] and ultima['RSI'] > 70:
            if ultima['close'] < anterior['close'] and anterior['close'] > df.iloc[-3]['close']:
                return "VENTA"

        return "NO_ENTRADA"
    except Exception as e:
        print(f"⚠️ Error en análisis de {simbolo}: {e}")
        return "NO_ENTRADA"

def calcular_rsi(series, period=14):
    delta = series.diff()
    ganancia = delta.where(delta > 0, 0)
    perdida = -delta.where(delta < 0, 0)
    media_gan = ganancia.rolling(window=period).mean()
    media_per = perdida.rolling(window=period).mean()
    rs = media_gan / media_per
    return 100 - (100 / (1 + rs))
