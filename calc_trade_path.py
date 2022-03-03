import pprint

sample_trades = [{'base': 'BTC',
                  'direction': 'BUY',
                  'exchange': '@Bittrex',
                  'id': '(1)',
                  'pair': 'BTC/USDT',
                  'quote': 'USDT'},
                 {'base': 'BTC',
                  'direction': 'SELL',
                  'exchange': '@Bittrex',
                  'id': '(2)',
                  'pair': 'BTC/EUR',
                  'quote': 'EUR'}]
sample_trades_2 = [{'base': 'BTC',
                    'direction': 'BUY',
                    'exchange': '@Bittrex',
                    'id': '(1)',
                    'pair': 'BTC/ETH',
                    'quote': 'ETH'},
                   {'base': 'BTC',
                    'direction': 'SELL',
                    'exchange': '@Bittrex',
                    'id': '(2)',
                    'pair': 'BTC/EUR',
                    'quote': 'EUR'}]


def trade_obj(pair, direction):
    trade_obj = {'base': pair.split('/')[0],
                 'quote': pair.split('/')[1],
                 'direction': direction,
                 'pair': pair,
                 }

    return trade_obj


def calc_trade_path(signal_trades: list):
    trade_path = []
    if signal_trades[0]['quote'] != 'USDT':
        trade_path.append(trade_obj(f"{signal_trades[0]['quote']}/USDT", 'BUY'))

    trade_path.append(trade_obj(signal_trades[0]['pair'], signal_trades[0]['direction']))

    trade_path.append(trade_obj(signal_trades[1]['pair'], signal_trades[1]['direction']))

    if signal_trades[1]['quote'] != 'USDT':
        trade_path.append(trade_obj(f"{signal_trades[1]['quote']}/USDT", 'SELL'))
    return trade_path


def parse_trade_path_to_str(trade_path: list):
    lst = []

    for trade in trade_path:
        # print(trade)
        lst.append(f"{trade['direction']} {trade['pair']}")

    parsed_str = '\n'.join(lst)

    return parsed_str


my_trade_path = calc_trade_path(sample_trades)
my_parsed_trade_path = parse_trade_path_to_str(my_trade_path)

# pprint.pprint(my_trade_path)
# print(my_parsed_trade_path)
