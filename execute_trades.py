import ccxt
import configparser
from pprint import pprint
from datetime import datetime


config = configparser.ConfigParser()
config.read("config.ini")

binance = ccxt.binance()
bitfinex = ccxt.bitfinex()
bitstamp = ccxt.bitstamp()
bittrex = ccxt.bittrex()
cex = ccxt.cex()
coinbasepro = ccxt.coinbasepro({
    'apiKey': config['Coinbase Pro']['apiKey'],
    'secret': config['Coinbase Pro']['secret'],
    'password': config['Coinbase Pro']['password'],
    'enableRateLimit': True,
})
exmo = ccxt.exmo()
gemini = ccxt.gemini()
hitbtc = ccxt.hitbtc({
    'apiKey': config['HitBTC']['apiKey'],
    'secret': config['HitBTC']['secret'],
    'enableRateLimit': True,
})
kraken = ccxt.kraken()
kucoin = ccxt.kucoin()
mxc = ccxt.mexc()
poloniex = ccxt.poloniex()



def get_free_balances(_exchange):
    all_balances = _exchange.fetch_balance()
    nonzero_balances = {}
    for coin_balance in all_balances['free']:
        if all_balances.get(coin_balance)['free'] != 0.0:
            nonzero_balances[coin_balance] = all_balances.get(coin_balance)

    return nonzero_balances


def send_market_order(pair, direction, quantity, live_trade=True):
    # print(f"Opened Market Order: \n{direction} {quantity} {pair}")
    timestamp = (f"timestamp: \n"
                 f"{datetime.utcnow().strftime('%m/%d | %H:%M:%S.%f')}")
    print(f"--------------------------------------------------------------------------------"
          f"\nOpening Market Order: "
          f"{direction} {quantity} {pair}\n"
          f"timestamp: \n{timestamp}"
          f"--------------------------------------------------------------------------------")

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


def open_buy_order(exchange, pair, cost, live_trade=False):
    #  order = exchange.createOrder(pair, 'market', 'buy', quantity)
    # Since create_market_order() requires price as a param for HitBTC and doesn't accept cost instead, I need to
    # calculate the price derived from the desired cost which will be the stake amount of USDT for the first trade,
    # and the full balance of any subsequent coins in the trade path, taking fees into account. This is only
    # necessary on the buy side, not the sell side where the cost and the amount are the same

    ticker_price = exchange.fetch_ticker(pair)
    pprint(ticker_price)
    fees = 0
    amount = cost / ticker_price.get('ask') * 0.9
    test_amount = amount

    if live_trade:
        # order = exchange.create_market_buy_order(pair, test_amount)
        order = exchange.createOrder(pair, 'market', 'buy', amount)



        # pprint(order)
        # pprint(get_free_balances(exchange))
    elif not live_trade:
        order = f"create_market_buy_order({pair}, ({test_amount}))"
    return order


def open_sell_order(exchange, pair, cost, live_trade=False):
    if live_trade:
        # order = exchange.create_market_sell_order(pair, test_amount)
        order = exchange.createOrder(pair, 'market', 'sell', cost)
        # pprint(order)
        # pprint(get_free_balances(exchange))

    elif not live_trade:
        order = f"create_market_sell_order({pair}, (ticker_price / {cost}))"
    return order


current_trade_qty = 0   # Should find a way to not have to declare this globally
                        # since it's only used by the function execute_trades

# def check_profit(trade_path):
#     print(f"check_profit() called\n"
#           f"{str(trade_path)}")
#     usdt_start_balance = get_free_balances(exchange)['USDT']['free']
#
#     current_tickers = {}
#     sim_balance = usdt_start_balance
#     for item in enumerate(trade_path):
#         current_tickers[item[1]['pair']] = exchange.fetch_ticker(item[1]['pair'])
#         if item[1]['direction'] == 'BUY':
#             current_ask = current_tickers[item[1]['pair']]['ask']
#             trade_path[item[0]]['ask'] = current_ask
#             if item[0] > 0:
#                 trade_path[item[0]]['post-balance'] = trade_path[item[0]-1]['post-balance'] / current_ask
#             elif item[0] == 0:
#                 trade_path[item[0]]['post-balance'] = usdt_start_balance / current_ask
#             pass
#         elif item[1]['direction'] == 'SELL':
#             current_bid = current_tickers[item[1]['pair']]['bid']
#             trade_path[item[0]]['bid'] = current_bid
#             if item[0] > 0:
#                 trade_path[item[0]]['post-balance'] = trade_path[item[0] - 1]['post-balance'] * current_bid
#             elif item[0] == 0:
#                 trade_path[item[0]]['post-balance'] = usdt_start_balance * current_ask
#             pass
#         pass
#
#     end_balance = trade_path[-1]['post-balance']
#     profit = end_balance - usdt_start_balance
#     breakpoint()
#     return profit

# def execute_trades(trade_path, signal_trades):
#     start_usdt_balance = get_free_balances(exchange).get('USDT').get('free')
#     trade_log = ''
#     """
#     print(f"Executing trades on {exchange}...\n"
#           f"Starting USDT Balance: {usdt_free_balance}")
#     """
#     trade_log += (f"Executed signal on {exchange}...\n\n"
#                          )
#     current_trade = 0
#     global current_trade_qty
#     stake_qty = start_usdt_balance  # TODO: calculate optimal stake_qty from signal max_profit
#
#     executed_trades = []
#
#     for trade in enumerate(trade_path):
#         global current_trade_qty
#
#         if current_trade == 0:
#             current_trade_qty = stake_qty
#
#         current_trade += 1
#         pair = trade[1].get('pair')
#         direction = trade[1].get('direction')
#         order = send_market_order(pair, direction, current_trade_qty, live_trade=True)
#         executed_trades.append(order)
#
#
#         try:
#             if direction == 'BUY':
#                 next_coin = trade[1].get('base')
#
#             elif direction == 'SELL':
#                 next_coin = trade[1].get('quote')
#
#             current_trade_qty = get_free_balances(exchange).get(next_coin).get('free')
#             """
#             print(f"{trade[0] + 1}. "
#                   f"Opened Market Order: \n{direction} {current_trade_qty} {pair}\n")
#
#             trade_log += (f"{trade[0] + 1}. "
#                                  #  f"Opened Market Order: \n"
#                                  f"{direction} {current_trade_qty} {pair}\n")
#             """
#         except:
#             trade_log += f"\nError: Failed to {direction.lower} {pair} as there wasn't enough balance.\nTrade sequence aborted."
#
#     for trade in enumerate(executed_trades):
#         datetime = trade[1]['datetime']
#         direction = trade[1]['side']
#         qty = trade[1]['amount']
#         pair = trade[1]['symbol']
#         cost = trade[1]['cost']
#
#         trade_log += (f"{trade[0] + 1}. "
#                       #  f"Opened Market Order: \n"
#                       f"{direction.upper()} {'{:f}'.format(qty)} {pair}\n")
#
#     end_usdt_balance = get_free_balances(exchange).get('USDT').get('free')
#     trade_log += (f"\nStart Balance: ${start_usdt_balance} (USDT)\n"
#                   f"End Balance: ${end_usdt_balance} (USDT)\n"
#                   f"Profit: ${end_usdt_balance-start_usdt_balance} (USDT)")
#     return trade_log


def convert_all_balances_to_usdt(exchange):
    """
    Not sure if this isn't working properly or if it's because
    the balances are too small. This function is just for debugging
    """

    balances = get_free_balances(exchange)
    # pprint(balances)
    print(f"Selling these balances:\n")

    for balance in enumerate(balances):
        if balance[1] != 'USDT':
            print(f"{balance[1]}: "
                  f"{'{:f}'.format(balances[balance[1]]['free'])}"
                  )
            open_sell_order(f"{balance[1]}/USDT", '{:f}'.format(balances[balance[1]]['free']))

    pprint(get_free_balances(exchange))


# ###########[TESTING]###############
# pprint(get_free_balances(exchange))
# open_sell_order('BTC/USDT', 3.618668e-06*0.99)
# exchange.createOrder('BTC/USDT', 'market', 'sell', 3.618668e-06)
# convert_all_balances_to_usdt(exchange)
# pprint(get_free_balances(exchange))

# print(execute_trades(sample_trade_path, sample_signal_trades))

# ###################################
