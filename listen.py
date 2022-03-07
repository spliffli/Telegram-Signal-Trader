import configparser
import asyncio
import platform
if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

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

notification_channel_id = config['Telegram']['notification_channel_id']
exchange = config['Bot Settings']['exchange']


async def authenticate():
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))


@client.on(events.NewMessage(pattern=f'Your arbitrage alert {exchange} has been triggered!'))
async def handler(event):
    # here received message, do something with event
    msg_str = event.to_dict()['message'].to_dict()['message']

    # TODO: confirm that signal is coming from specified channel ID, otherwise don't execute

    signal_trades = parse_msg_signals(msg_str)
    trade_path = calc_trade_path(signal_trades)
    """
    print(f"[trade_path]\n{trade_path}\n[/trade_path]\n"
          f"[signal_trades]\n{signal_trades}\n[/signal_trades]\n")
    """
    reply = ('\n\nTrade Signals detected. Initiating the following sequence of trades:\n'
             f"\n{parse_trade_path_to_str(trade_path)}"
             # f"\n{execute_trades(trade_path, signal_trades)}"
             )
    await client.send_message(entity=notification_channel_id, message=reply)
    trade_log = execute_trades(trade_path, signal_trades)
    await client.send_message(entity=notification_channel_id, message=trade_log)

with client:
    client.loop.run_until_complete(authenticate())

    client.run_until_disconnected()
