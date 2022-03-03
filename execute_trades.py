import ccxt
import configparser
from pprint import pprint

config = configparser.ConfigParser()
config.read("config.ini")

hitbtc = ccxt.hitbtc({
    'apiKey': config['HitBTC']['apiKey'],
    'secret': config['HitBTC']['secret']
})

kucoin = ccxt.kucoin({
  "apiKey": config['KuCoin']['apiKey'],
  "secret": config['KuCoin']['secret'],
  "password": config['KuCoin']['password']
})

if config['Bot Settings']['exchange'] == 'hitbtc':
    exchange = hitbtc
elif config['Bot Settings']['exchange'] == 'kucoin':
    exchange = kucoin

sample_trade_path = [{'base': 'GALA', 'quote': 'USDT', 'direction': 'BUY', 'pair': 'GALA/USDT'},
                     {'base': 'GALA', 'quote': 'BTC', 'direction': 'SELL', 'pair': 'GALA/BTC'},
                     {'base': 'BTC', 'quote': 'USDT', 'direction': 'SELL', 'pair': 'BTC/USDT'}]


def get_free_balances(_exchange):
    all_balances = _exchange.fetch_balance()
    nonzero_balances = {}
    for coin_balance in all_balances['free']:
        if all_balances.get(coin_balance)['free'] != 0.0:
            nonzero_balances[coin_balance] = all_balances.get(coin_balance)

    return nonzero_balances


pprint(get_free_balances(exchange))
order = 'None'  # exchange.createOrder('ETH/USDT', 'market', 'buy', 2.2640401e-05)
pprint(f"Order:\n{order}\n"
      f"------------------------------\n"
      f"New Balances:\n{get_free_balances(exchange)}")


def execute_trades(trade_path):
    for trade in trade_path:
        pass

    return 1


def send_market_order(pair, direction, quantity, live_trade=False):
    print(f"Opening Market Order: \n{direction} {quantity} {pair}")
    if direction == 'BUY':
        if not live_trade:
            return open_buy_order(pair, quantity, live_trade=False)
        elif live_trade:
            return open_buy_order(pair, quantity, live_trade=True)
    if direction == 'SELL':
        if not live_trade:
            return open_sell_order(pair, quantity, live_trade=False)
        elif live_trade:
            return open_sell_order(pair, quantity, live_trade=True)


def open_buy_order(pair, quantity, live_trade=False):
    if live_trade:
        order = exchange.createOrder(pair, 'market', 'buy', quantity)
    elif not live_trade:
        order = f"open_market_order({pair}, {quantity}, live_trade=False)"
    return order


def open_sell_order(pair, quantity, live_trade=False):
    if live_trade:
        order = exchange.createOrder(pair, 'market', 'sell', quantity)
    elif not live_trade:
        order = f"open_market_order({pair}, {quantity}, live_trade=False)"
    return order


