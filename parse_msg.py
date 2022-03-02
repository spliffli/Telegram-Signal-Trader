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


def parse_msg(msg: str):
    first_index = sample_msg.find('(1)')
    second_index = sample_msg.find('(2)')

    signal_first_trade_str = sample_msg[first_index:sample_msg.find('\n', first_index)]
    signal_second_trade_str = sample_msg[second_index:sample_msg.find('\n', second_index)]

    signal_first_trade_arr = signal_first_trade_str.split()
    signal_second_trade_arr = signal_second_trade_str.split()

    keys = ['id', 'direction', 'pair', 'exchange']
    first_trade = dict(zip(keys, signal_first_trade_arr))
    second_trade = dict(zip(keys, signal_second_trade_arr))

    def split_pair(pair: str):
        if '/' in pair:
            return pair.split('/')
        else:
            raise ValueError('Invalid trading pair')

    first_trade['base'] = split_pair(first_trade['pair'])[0]
    first_trade['quote'] = split_pair(first_trade['pair'])[1]

    second_trade['base'] = split_pair(second_trade['pair'])[0]
    second_trade['quote'] = split_pair(second_trade['pair'])[1]

    return [first_trade, second_trade]


pprint.pprint(parse_msg(sample_msg))