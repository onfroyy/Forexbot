import pandas as pd
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame

def calcular_rsi(series, period=14):
    delta = series.diff()
    ganancia = delta.where(delta > 0, 0)
    perdida = -delta.where(delta < 0, 0)
    media_gan = ganancia.rolling(window=period).mean()
    media_per = perdida.rolling(window=period).mean()
    rs = media_gan / media_per
    return 100 - (100 / (1 + rs))

def analizar_mercado(api, simbolo):
    try:
        request_params = CryptoBarsRequest(
            symbol_or_symbols=simbolo,
            timeframe=TimeFrame.Minute,
            start="2025-07-15T00:00:00Z"
        )
        barset = api.get_crypto_bars(request_params)
        df = barset.df

        if df.empty or simbolo not in df.index.get_level_values(0):
            print(f"⚠️ No hay datos para {simbolo}")
            return "NO_ENTRADA"

        df = df.loc[simbolo]
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
