from ._bot import SelfBot, download_message_attachments

import re
import os
import discord
import gzip
import shutil
import asyncio

DIR = "/tmp/goodies/"

# channel id
dropsites = (
  643995012522049536,
)

email = re.compile(r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*", re.MULTILINE)

# channel or guild id
sourcesites= (
  # https://discord.gg/m4nKChS net.cracking.es
  576992679640956948,
  
  # https://discord.gg/9UasgE9 - strife
  621414243421519883
)


@SelfBot.event
async def on_message(bot, msg):
  files = None
  attachments_stored_at = os.path.join(DIR, str(msg.id))
  
  if msg.channel.id in sourcesites or msg.guild and msg.guild.id in sourcesites:
    g = email.finditer(msg.content)
    try:
      if next(g):
        if msg.attachments:
          await download_message_attachments(attachments_stored_at, msg)
          files = [
            discord.File(gzip.open(os.path.join(DIR, attachment.url.split('/')[-1]), 'rb'))
            for attachment in msg.attachments
          ]
        
        for x in dropsites:
          channel = await bot.fetch_channel(x)
          await channel.send(f"Drop Supplied from {msg.guild}@{msg.channel} by **{msg.author}**")
          await channel.send(msg.content, files=files)
          try:
            nmsg = await bot.wait_for('message', check=lambda ctx: ctx.author == msg.author and ctx.channel == msg.channel, timeout=60)
            await channel.send(nmsg.content)
          except asyncio.TimeoutError:
            pass
          
    except StopIteration:
      pass
  
  if files:
    shutil.rmtree(attachments_stored_at)
  