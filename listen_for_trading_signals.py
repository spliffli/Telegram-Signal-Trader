import configparser
from telethon import TelegramClient, functions, events
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.patched import Message
import datetime
import pprint
import asyncio

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
    _peer = 'jonathon_test'
    entity = client.get_entity(_peer)
    # client.send_message(entity=entity, message="hello")


    @client.on(events.NewMessage(pattern=f'Your arbitrage alert {exchange} has been triggered!'))
    async def handler(event):
        # here received message, do something with event
        pprint.pprint(event.to_dict()['message'])  # check all possible methods/operations/attributes

        history = await client(GetHistoryRequest(
            peer=_peer,
            offset_id=0,
            offset_date=None,
            add_offset=0,
            limit=5,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if history.messages:
            # asyncio.create_task(result)
            for message in history.messages:
                mdict = message.to_dict()
                pprint.pprint(mdict['message'])
                # pprint.pprint(message.message.to_dict())

        # reply once and then disconnect
        await event.reply("have a nice day")
        # await client.disconnect()


    client.run_until_disconnected()
