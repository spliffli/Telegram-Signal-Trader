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

sample_signal_trades = [{'id': '(1)', 'direction': 'BUY', 'pair': 'GALA/USDT', 'exchange': '@HitBTC', 'base': 'GALA', 'quote': 'USDT'},
                        {'id': '(2)', 'direction': 'SELL', 'pair': 'GALA/BTC', 'exchange': '@HitBTC', 'base': 'GALA', 'quote': 'BTC'},
                        '0.07',
                        'intra_exchange arbitrage with volume',
                        '1.9917']


def get_free_balances(_exchange):
    all_balances = _exchange.fetch_balance()
    nonzero_balances = {}
    for coin_balance in all_balances['free']:
        if all_balances.get(coin_balance)['free'] != 0.0:
            nonzero_balances[coin_balance] = all_balances.get(coin_balance)

    return nonzero_balances


""" [DEBUG/TEST]
pprint(get_free_balances(exchange))
order = exchange.createOrder('DOGE/USDT', 'market', 'buy', 1)
pprint(f"Order:\n{order}\n"
       f"------------------------------\n"
       f"New Balances:\n")
pprint(get_free_balances(exchange))

# print(exchange.fetch_order('DOGE/USDT'))
"""

def send_market_order(pair, direction, quantity, live_trade=True):
    # print(f"Opened Market Order: \n{direction} {quantity} {pair}")

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


current_trade_qty = 0   # Should find a way to not have to declare this globally
                        # since it's only used by the function execute_trades


def execute_trades(trade_path, signal_trades):
    start_usdt_balance = get_free_balances(exchange).get('USDT').get('free')
    trade_log = ''
    """
    print(f"Executing trades on {exchange}...\n"
          f"Starting USDT Balance: {usdt_free_balance}")
    """
    trade_log += (f"Executed signal on {exchange}...\n\n"
                         )
    current_trade = 0
    global current_trade_qty
    stake_qty = start_usdt_balance  # TODO: calculate optimal stake_qty from signal max_profit

    executed_trades = []


    for trade in enumerate(trade_path):
        global current_trade_qty

        if current_trade == 0:
            current_trade_qty = stake_qty

        current_trade += 1
        pair = trade[1].get('pair')
        direction = trade[1].get('direction')
        order = send_market_order(pair, direction, current_trade_qty, live_trade=True)
        executed_trades.append(order)


        try:
            if direction == 'BUY':
                next_coin = trade[1].get('base')

            elif direction == 'SELL':
                next_coin = trade[1].get('quote')

            current_trade_qty = get_free_balances(exchange).get(next_coin).get('free')
            """
            print(f"{trade[0] + 1}. "
                  f"Opened Market Order: \n{direction} {current_trade_qty} {pair}\n")
            
            trade_log += (f"{trade[0] + 1}. "
                                 #  f"Opened Market Order: \n"
                                 f"{direction} {current_trade_qty} {pair}\n")
            """
        except:
            trade_log += f"\nError: Failed to {direction.lower} {pair} as there wasn't enough balance.\nTrade sequence aborted."

    for trade in enumerate(executed_trades):
        datetime = trade[1]['datetime']
        direction = trade[1]['side']
        qty = trade[1]['amount']
        pair = trade[1]['symbol']
        cost = trade[1]['cost']

        trade_log += (f"{trade[0] + 1}. "
                      #  f"Opened Market Order: \n"
                      f"{direction.upper()} {qty} {pair}\n")


    end_usdt_balance = get_free_balances(exchange).get('USDT').get('free')
    trade_log += (f"\nStart Balance: ${start_usdt_balance} (USDT)\n"
                  f"End Balance: ${end_usdt_balance} (USDT)\n"
                  f"Profit: ${end_usdt_balance-start_usdt_balance} (USDT)")
    return trade_log



# ###########[TESTING]###############

# print(execute_trades(sample_trade_path, sample_signal_trades))

# ###################################
