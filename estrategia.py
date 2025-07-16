import pandas as pd
import requests

def analizar_mercado(api, simbolo):
    try:
        tipo = "stocks"
        if "/" in simbolo:
            tipo = "crypto"

        if tipo == "stocks":
            df = api.get_bars(simbolo, '5Min', limit=50).df
            df = df[df['symbol'] == simbolo]
        else:
            # Para cripto usamos la API REST directamente (por ahora)
            url = f"https://data.alpaca.markets/v1beta1/crypto/bars?symbols={simbolo.replace('/', '')}&timeframe=5Min&limit=50"
            headers = {
                "APCA-API-KEY-ID": api._key_id,
                "APCA-API-SECRET-KEY": api._secret_key
            }
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"❌ Error al obtener datos de {simbolo}: {response.text}")
                return "NO_ENTRADA"
            data = response.json()
            bars = data.get(simbolo.replace('/', ''), [])
            if not bars:
                return "NO_ENTRADA"
            df = pd.DataFrame(bars)
            df['close'] = df['c']
            df.index = pd.to_datetime(df['t'])

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
