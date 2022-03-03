import configparser
from telethon import TelegramClient, functions, events
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.patched import Message
import datetime
import pprint
import asyncio

from parse_msg import parse_msg_signals

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

exchange = 'Bitrexx'

with client:
    _peer = 'jonathon_test'  # '@C5543577423'  #
    entity = client.get_entity(_peer)

    # client.send_message(entity=entity, message="hello")

    @client.on(events.NewMessage(pattern=f'Your arbitrage alert {exchange} has been triggered!'))
    async def handler(event):
        # here received message, do something with event
        msg_str = event.to_dict()['message'].to_dict()['message']
        pprint.pprint(msg_str)  # check all possible methods/operations/attributes

        # reply once and then disconnect
        # reply = str(parse_msg_signals(msg_str))

        signal_trades = parse_msg_signals(msg_str)
        pprint.pprint(signal_trades)

        reply = ('\n\nTrade Signals detected. Initiating the following sequence of trades:'
                 f"\nBUY {signal_trades[0]['quote']}/USDT"
                 f"\n{signal_trades[0]['direction']} {signal_trades[0]['pair']}"
                 f"\n{signal_trades[1]['direction']} {signal_trades[1]['pair']}"
                 f"\nSELL {signal_trades[1]['quote']}/USDT"
                 "\n\nThis is just a test to see if the telegram signals can be properly parsed, and no actual trades "
                 "were made")

        await event.reply(reply)
        # await client.disconnect()


    client.run_until_disconnected()
