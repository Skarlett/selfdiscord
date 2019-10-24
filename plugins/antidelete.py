from .__init__ import GENERATE_CLASS
import logging
import aiohttp
import os
import gzip
import discord

guilds = {632751884461015051, 356094949659508736, 419424683188944897}
DIR = "/tmp/selfbot_media_tracker"

if not os.path.exists(DIR):
  try:
    os.mkdir(DIR)
  except Exception as e:
    logging.critical("Couldnt make media directory.")
    logging.exception(e)


@GENERATE_CLASS.event
async def on_message(bot, msg):
  if msg.author == bot.user:
    async with aiohttp.ClientSession() as session:
      for attachment in msg.attachments:
        path = os.path.join(DIR, attachment.url.split('/')[-1])
        resp = await session.get(attachment.url)
        with gzip.open(path, 'wb') as fd:
          try:
            fd.write(await resp.read())
          except Exception as e:
            logging.exception(e)
            logging.critical(f"Couldn't save \"{attachment.url}\" to {path}")
  
@GENERATE_CLASS.event
async def on_message_delete(bot, msg):
  if msg.author == bot.user and msg.guild.id in guilds:
    if msg.attachments:
      files = [
        discord.File(gzip.open(os.path.join(DIR, attachment.url.split('/')[-1]), 'rb'))
        for attachment in msg.attachments
      ]
    else:
      files = None
    
    await msg.channel.send(msg.content, files=files)
    
    if files:
      for x in files:
        x.close()

@GENERATE_CLASS.command()
async def antidelete(bot, ctx, args):
  if ctx.guild.id in guilds:
    guilds.remove(ctx.guild.id)
  else:
    guilds.add(ctx.guild.id)

