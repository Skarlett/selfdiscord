from .__init__ import GENERATE_CLASS
import logging
import aiohttp
import os

media = set()
media_path = "/tmp/selfbot_media_tracker"

guilds = set()

try:
  os.mkdir(media_path) 
except Exception as e:
  logging.exception(e)



async def fetch(session, url):
    filename = url.split('/')[-1]
    try:  
      async with session.get(url) as response, open(filename, 'wb') as fd:
        fd.write(await response.text())
    except Exception as e:
      logging.exception(e)


@GENERATE_CLASS.event
async def on_message(bot, msg):
  if msg.author == bot.user and msg.attachments:
    async with aiohttp.ClientSession() as session:
      async for x in msg.attachments:
         resp = await session.get(url)
         resp.content


@GENERATE_CLASS.event
async def on_message_delete(bot, msg):
  if msg.author == bot.user and msg.guild.id == 632751884461015051 and msg.attachments:
      await msg.channel.send('\n'.join(x.url for x in msg.attachments))



