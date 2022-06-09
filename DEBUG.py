from telethon.sync import TelegramClient, events

api_id = "15640594"
api_hash = "c3d8899579d7c8bf657b7bbb0d47a1e5"


with TelegramClient('name', api_id, api_hash) as client:
   client.send_message('me', 'Hello, myself!')
   print(client.download_profile_photo('me'))

   @client.on(events.NewMessage(pattern='(?i).*Hello'))
   async def handler(event):
      await event.reply('Hey!')

   client.run_until_disconnected()