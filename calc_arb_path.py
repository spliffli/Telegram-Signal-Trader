import pprint

sample_trades = [{'trade_number': '1',
                  'direction': 'BUY',
                  'base': 'IMX',
                  'quote': 'USDT',
                  'exchange': 'Poloniex'},
                {'trade_number': '2',
                 'direction': 'SELL',
                 'base': 'IMX',
                 'quote': 'USDT',
                 'exchange': 'Binance'}]


def calc_arb_path(signal_trades: list, funded_exchange: str, stake_currency: str = 'USDT', ):
    arb_path = []

    if stake_currency == 'USDT':
        arb_path.append({
            'type': 'trade',
            'direction': 'BUY',
            'base': 'XRP',
            'quote': 'USDT',
            'exchange': funded_exchange
        })

    if funded_exchange != signal_trades[0]['exchange']:
        arb_path.append({
            "type": "transfer",
            "coin": "XRP",
            "from": funded_exchange,
            "to": signal_trades[0]['exchange']
        })

    arb_path.append({
        "type": "trade",
        "direction": "SELL",
        "base": "XRP",
        "quote": signal_trades[0]['quote']
    })

    for trade in enumerate(signal_trades):

        # if exchange is not equal to the previous
        if trade[0] > 0 and trade[1]['exchange'] != signal_trades[trade[0]-1]['exchange']:
            arb_path.append({
                "type": "transfer",
                "coin": "XRP",
                "from": signal_trades[trade[0]-1]['exchange'],
                "to": trade[1]['exchange']
            })

        arb_path.append({
            "type": "trade",
            "direction": trade[1]['direction'],
            "base": trade[1]['base'],
            "quote": trade[1]['quote'],
            "exchange": trade[1]['exchange']
        })

    return arb_path


#my_trade_path = calc_trade_path(sample_trades)

# pprint.pprint(my_trade_path)
# print(my_parsed_trade_path)
