import configparser
from telethon import TelegramClient, functions, events
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.patched import Message
import datetime
import pprint
import asyncio

from parse_msg import parse_msg_signals
from calc_trade_path import calc_trade_path, parse_trade_path_to_str
from execute_trades import execute_trades

# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)

# exchange = 'HitBTC'

with client:
    _peer = 'jonathon_test'  # '@C5543577423'  #
    entity = client.get_entity(_peer)

    # client.send_message(entity=entity, message="hello")

    @client.on(events.NewMessage())  # (pattern=f'Your arbitrage alert {exchange} has been triggered!'))
    async def handler(event):
        # here received message, do something with event
        msg_str = event.to_dict()['message'].to_dict()['message']
        # print(f"---------\n{msg_str}\n---------")  # check all possible methods/operations/attributes

        # reply once and then disconnect
        # reply = str(parse_msg_signals(msg_str))

        signal_trades = parse_msg_signals(msg_str)
        trade_path = calc_trade_path(signal_trades)
        print(f"[trade_path]\n{trade_path}\n[/trade_path]\n"
              f"[signal_trades]\n{signal_trades}\n[/signal_trades]\n")

        reply = ('\n\nTrade Signals detected. Initiating the following sequence of trades:\n'
                 f"\n{parse_trade_path_to_str(trade_path)}"
                 "\n\nThis is just a test to see if the telegram signals can be properly parsed, and no actual trades "
                 "were made")

        await event.reply(reply)
        execute_trades(trade_path, signal_trades)
        # await client.disconnect()


    client.run_until_disconnected()
