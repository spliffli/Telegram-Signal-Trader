import configparser
import asyncio
import platform
import colorama

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError

from parse_msg import parse_msg
from calc_arb_path import calc_arb_path
#from execute_trades import execute_trades, check_profit


# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
tg_api_id = int(config['Telegram']['api_id'])
tg_api_hash = str(config['Telegram']['api_hash'])

phone = config['Telegram']['phone']
username = config['Telegram']['username']

client = TelegramClient(username, tg_api_id, tg_api_hash)

notification_channel_id = config['Telegram']['notification_channel_id']


async def authenticate():
    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))


@client.on(events.NewMessage(pattern=f'Your arbitrage alert'))
async def handler(event):
    # here received message, do something with event
    # TODO: confirm that signal is coming from specified channel ID, otherwise don't execute
    
    msg_str = event.to_dict()['message'].to_dict()['message']
    signal = parse_msg(msg_str)

    for trade in signal['trades']:
        print(trade)

    if float(signal['percentage']) > 2 and float(signal['max_profit']) > 100:
        arb_path = calc_arb_path(signal['trades'], "HitBTC")

    breakpoint()





    breakpoint()
    
with client:
    jackpot_art_file = open('./jackpot-art-light.ans')
    jackpot_art = jackpot_art_file.read()
    print(jackpot_art)
    print("Listening for signals...")
    # breakpoint()
    client.loop.run_until_complete(authenticate())

    client.run_until_disconnected()
