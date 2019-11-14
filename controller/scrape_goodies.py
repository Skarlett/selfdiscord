from ._bot import SelfBot, download_message_attachments

import re
import os
import discord
import gzip
import shutil


DIR = "/tmp/goodies/"

# channel id
dropsites = (643974069477310477, 643995012522049536)


# channel or guild id
sourcesites= (
  # https://discord.gg/m4nKChS net.cracking.es
  580794788006068254,
  576992679640956948
)

email = re.compile(r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
                   r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*", re.MULTILINE)


@SelfBot.event
async def on_message(bot, msg):
  files = None
  attachments_stored_at = os.path.join(DIR, str(msg.id))
  
  if msg.channel.id in sourcesites or msg.guild and msg.guild.id in sourcesites:
    g = email.match(msg.content)
    if g and g.group():
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
  
  if files:
    shutil.rmtree(attachments_stored_at)
  