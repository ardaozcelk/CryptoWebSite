import hmac
import time
import hashlib
import requests
from urllib.parse import urlencode
import ta
import pandas as pd
import ta.momentum
import ta.trend
import ta.volatility

KEY =""
SECRET = ""
BASE_URL = "https://testnet.binancefuture.com"     # testnet base url

symbol_list = ["BTC","ETH","DOGE","XRP","ADA","SOL","MANA","DOT","LINK"]

def hashing(query_string):
    return hmac.new(
        SECRET.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256
    ).hexdigest()

def get_timestamp():
    return int(time.time() * 1000)

def dispatch_request(http_method):
    session = requests.Session()
    session.headers.update(
        {"Content-Type": "application/json;charset=utf-8", "X-MBX-APIKEY": KEY}
    )
    return {
        "GET": session.get,
        "DELETE": session.delete,
        "PUT": session.put,
        "POST": session.post,
    }.get(http_method, "GET")

# used for sending request requires the signature
def send_signed_request(http_method, url_path, payload={}):
    query_string = urlencode(payload)
    # replace single quote to double quote
    query_string = query_string.replace("%27", "%22")

    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = "timestamp={}".format(get_timestamp())

    url = (
        BASE_URL + url_path + "?" + query_string + "&signature=" + hashing(query_string)
    )
    params = {"url": url, "params": {}}
    response = dispatch_request(http_method)(**params)
    return response.json()

# used for sending public data request
def send_public_request(url_path, payload={}):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + "?" + query_string
    response = dispatch_request("GET")(url=url)
    return response.json()

def create_order(symbol, quantity):
    data = get_data(symbol)
    price = float(data[4][len(data)-1])
    symbol_quantity = round(quantity/price,3)
    params = {
        "symbol": symbol+"USDT",
        "side": "BUY",
        "type": "MARKET",
        "quantity": symbol_quantity,
        "currency": "USDT"
    }
    return send_signed_request("POST", "/fapi/v1/order", params)

def get_open_order():
    return send_signed_request("GET", "/fapi/v1/openOrders", {})

def get_open_position():
    open_positions = []
    positions = send_signed_request("GET", "/fapi/v1/allOrders", {})
    for i in range(len(positions)):
        if (positions[i]["status"] == "FILLED" and positions[i]["closePosition"] == False):
            open_positions.append(positions[i])
    return open_positions

def close_position():
    open_position = get_open_position()[-1]

    params = {
        "symbol": open_position['symbol'],
        "side": "SELL",
        "type":"MARKET",
        "quantity": open_position['executedQty'],
        "closeposition":False
    }
    return send_signed_request("POST", "/fapi/v1/order", params)

def close_position_amount(profit_rate):
    open_position = get_open_position()[-1]

    params = {
        "symbol": open_position['symbol'],
        "side": "SELL",
        "type":"LIMIT",
        "quantity": open_position['executedQty'],
        "timeinforce":"GTC",
        "closeposition":False,
        "price":round(float(open_position['avgPrice'])*(round(1+(profit_rate/100),2)),2)
    }
    return send_signed_request("POST", "/fapi/v1/order", params)

def get_data(symbol):
    response = send_public_request(
        "/fapi/v1/klines", {"symbol": symbol+"USDT", "interval": "5m"}
    )
    df = pd.DataFrame(response)
    df[4] = pd.to_numeric(df[4])
    return df

def macd(data):
    close_list = data[4]
    macd_signal = ta.trend.macd_signal(close_list)
    macd_line = ta.trend.macd(close_list)
    return macd_line.tolist()[-1],macd_signal.tolist()[-1], macd_line.tolist()[-2],macd_signal.tolist()[-2]

def rsi(data):
    close_list = data[4]
    rsi = ta.momentum.RSIIndicator(close_list)
    return list(rsi.rsi())

def ema(data):
    close_list = data[4]
    ema_50 = ta.trend.EMAIndicator(close_list,50)
    ema_100 = ta.trend.EMAIndicator(close_list,100)
    return ema_50.tolist()[-1],ema_100.tolist()[-1], ema_50.tolist()[-2],ema_100.tolist()[-2]

def bollinger_bands(data):
    close_list = data[4]
    indicator_bb = ta.volatility.BollingerBands(close=close_list, window=20, window_dev=2)
    high_band = indicator_bb.bollinger_hband()
    return close_list.to_list()[-1],high_band.to_list()[-1]


def presentation_bot(api_key,api_secret, symbol, amount):
    global KEY
    global SECRET
    KEY = api_key
    SECRET = api_secret

    create_order(symbol,amount)
    time.sleep(15)
    close_position()



#RSI indikatörüne bakar her işlem için %3 kar ile satmaya çalışır
def rsi_bot(api_key,api_secret, amount):
    global KEY
    global SECRET
    KEY = api_key
    SECRET = api_secret
    symbol_list = ["BTC","ETH","DOGE","XRP","ADA","SOL","MANA","DOT","LINK"]

    for i in range(len(symbol_list)):
        data = get_data(symbol_list[i])
        symbol_rsi = rsi(data)

        if symbol_rsi[i] < 30:
            create_order(symbol_list[i],amount)
            close_position_amount(3)

#MACD indikatörüne bakar her işlem için %5 kar ile satmaya çalışır
def macd_bot(api_key,api_secret, amount):
    global KEY
    global SECRET
    KEY = api_key
    SECRET = api_secret
    symbol_list = ["BTC","ETH","DOGE","XRP","ADA","SOL","MANA","DOT","LINK"]

    for i in range(len(symbol_list)):
        data = get_data(symbol_list[i])
        symbol_macd = macd(data)

        if(symbol_macd[0] > symbol_macd[1] and symbol_macd[3] > symbol_macd[2]):
           create_order(symbol_list[i],amount)
           close_position_amount(5)

#EMA indikatörüne bakar her işlem için %8 kar ile satmaya çalışır
def ema_bot(api_key,api_secret, amount):
    global KEY
    global SECRET
    KEY = api_key
    SECRET = api_secret
    symbol_list = ["BTC","ETH","DOGE","XRP","ADA","SOL","MANA","DOT","LINK"]

    for i in range(len(symbol_list)):
        data = get_data(symbol_list[i])
        symbol_ema = ema(data)

        if(symbol_ema[0] > symbol_ema[1] and symbol_ema[3] > symbol_ema[2]):
            create_order(symbol_list[i],amount)
            close_position_amount(8)

#Bollinger Bands indikatörüne bakar her işlem için %6 kar ile satmaya çalışır
def bollinger_bands_bot(api_key,api_secret, amount):
    global KEY
    global SECRET
    KEY = api_key
    SECRET = api_secret
    symbol_list = ["BTC","ETH","DOGE","XRP","ADA","SOL","MANA","DOT","LINK"]

    for i in range(len(symbol_list)):
        data = get_data(symbol_list[i])
        symbol_bollinger_bands = bollinger_bands(data)

        if(symbol_bollinger_bands[0] > symbol_bollinger_bands[1]):
            create_order(symbol_list[i],amount)
            close_position_amount(6)


