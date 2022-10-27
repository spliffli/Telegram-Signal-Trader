import re

urls = """
http://python-engineer.com
http://www.pyeng.net
"""

test_string = '123abc456789abc123ABC'

msg_example = """
Your arbitrage alert Coinbase Pro to Binance has been triggered!\n
\n
1.23% direct arbitrage with volume\n
(1) BUY ACH/USD @Coinbase Pro\n
(2) SELL ACH/USDT @Binance\n
 To make a maximum profit of 202.1927 USD\n
For more info visit this link https://www.koinknight.com/notification/6359563cf91a89333aa8056f
"""


def get_trades(msg):

    pattern = re.compile(r"\((?P<trade_number>\d)\) (?P<direction>[^\s]+) (?P<base>[^\/]+)/(?P<quote>[^\s]+) @(?P<exchange>[^\n]+)")
    matches = pattern.finditer(msg)
    trades = []

    for match in matches:
        trades.append(match.groupdict())

    return trades


def get_arb_percentage(msg):
    pattern = re.compile(r"(?<=\n)\d\.\d\d(?=%)")
    match = pattern.search(msg)
    return match.group()


def get_max_profit(msg):
    pattern = re.compile(r"(?<=maximum profit of )([^\s]+)(?= USD)")
    match = pattern.search(msg)
    return match.group()


def parse_msg(msg):
    percentage = get_arb_percentage(msg)
    max_profit = get_max_profit(msg)
    trades = get_trades(msg)

    signal = {
        "percentage": percentage,
        "max_profit": max_profit,
        "trades": trades
    }

    return signal


#signal = parse_msg(msg_example)
