import pprint

sample_msg = ('Your arbitrage alert Bitrexx has been triggered!\n'
              '\n'
              '*My message, to you rudy*\n'
              '\n'
              '0.10% intra_exchange arbitrage with volume\n'
              '(1) BUY BTC/USDT @Bittrex\n'
              '(2) SELL BTC/EUR @Bittrex\n'
              ' To make a maximum profit of 22.2784 USD\n'
              'For more info visit this link '
              'https://www.koinknight.com/notification/621e86d0866655178cf6d339')


def split_pair(pair: str):
    if '/' in pair:
        return pair.split('/')
    else:
        raise ValueError('Invalid trading pair')


def parse_msg_signals(msg: str):
    first_index = msg.find('(1)')
    second_index = msg.find('(2)')

    signal_first_trade_str = msg[first_index:msg.find('\n', first_index)]
    signal_second_trade_str = msg[second_index:msg.find('\n', second_index)]

    signal_first_trade_arr = signal_first_trade_str.split()
    signal_second_trade_arr = signal_second_trade_str.split()

    percent_gain = msg[msg.find('%')-4:msg.find('%')]
    signal_type = msg[msg.find('% ')+2:msg.find('\n', msg.find('%'))]

    max_profit_index = msg.find('maximum profit of ')+18
    max_profit = msg[max_profit_index:msg.find(' USD', max_profit_index)]

    keys = ['id', 'direction', 'pair', 'exchange']
    first_trade = dict(zip(keys, signal_first_trade_arr))
    second_trade = dict(zip(keys, signal_second_trade_arr))

    first_trade['base'] = split_pair(first_trade['pair'])[0]
    first_trade['quote'] = split_pair(first_trade['pair'])[1]

    second_trade['base'] = split_pair(second_trade['pair'])[0]
    second_trade['quote'] = split_pair(second_trade['pair'])[1]

    return [first_trade, second_trade, percent_gain, signal_type, max_profit]


# pprint.pprint(parse_msg_signals(sample_msg))
