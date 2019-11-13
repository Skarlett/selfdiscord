# import asyncio
# import time
# from ..lib import GENERATE_CLASS
# from ..models.repeater import Advertisement, AdvertisementSchema, AdvertisementMeta
# from ..models import Session
# from discord.ext import commands
# from base64 import urlsafe_b64encode
#
# def _make_translate_url(sourceText, targetLang, sourceLang='en'):
#   return "https://translate.googleapis.com/translate_a/single?client=gtx&sl=" \
#          + sourceLang + "&tl=" + targetLang + "&dt=t&q=" + urlsafe_b64encode(sourceText)
#
# @commands.is_owner()
# @GENERATE_CLASS.command()
# async def add_schema(bot, ctx, args):
#   session = Session()
#   ad = AdvertisementSchema()
#   session.add(ad)
#   session.commit()
#
#
# @GENERATE_CLASS.event
# async def on_guild_leave(bot, guild, user):
#   if user == bot.user:
#     session = Session()
#
#     for x in guild.channels:
#       session.delete(Advertisement).where(Advertisement.channel == x.id)
#
#     session.commit()
#
# @GENERATE_CLASS.background
# async def advertisement(bot):
#   session = Session()
#   for ad in session.query(Advertisement) \
#     .filter(
#       Advertisement.meta.timestamped + Advertisement.meta.repeater <= time.time(),
#       Advertisement.meta.active == True) \
#     .order_by(Advertisement.meta.timestamped.desc()):
#
#       try:
#         room = await bot.fetch_channel(ad.channel)
#         await room.send(ad.source.content)
#       except:
#         await asyncio.sleep(360)
#         return
#
#       session.update(AdvertisementMeta).where(ad.meta.uuid == AdvertisementMeta.uuid).values(
#         hits=ad.meta.hits+1,
#         timestamped=time.time(),
#       )
#
#   session.commit()
#
#   await asyncio.sleep(360)