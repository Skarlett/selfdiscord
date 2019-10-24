from .__init__ import GENERATE_CLASS
import discord
import logging
import traceback
import asyncio

@GENERATE_CLASS.command()
async def purge(bot, ctx, args):
  if ctx.author == bot.user:
    if len(args) == 0:
      limit = 10000
    else:
      try:
        limit = int(args[1])
      except Exception as e:
        limit = 10000
    
    await bot.purge_messages(ctx.channel, limit)

@GENERATE_CLASS.command(name="help")
async def _help(bot, ctx, args):
  await ctx.channel.send(', '.join(bot.COMMANDS.keys()))

@GENERATE_CLASS.command()
async def status(bot, ctx, args):
  await bot.change_presence(activity=discord.Game(' '.join(args)))


@GENERATE_CLASS.command()
async def system(bot, ctx, args):
  proc = await asyncio.create_subprocess_shell(" ".join(args),
                                  stderr=asyncio.subprocess.PIPE,
                                  stdout=asyncio.subprocess.PIPE)
  result = await proc.stdout.read() + await proc.stderr.read()
  await ctx.channel.send("```"+result.decode('utf8')+'```')

@GENERATE_CLASS.command(name="eval")
async def _eval(bot, ctx, args):
  pkg = ctx.content[len(bot.prefix):].split('```')
  if not len(pkg) == 3:
    await ctx.channel.send("expects ``` code ```")
    return
  
  try:
    await ctx.channel.send(eval(pkg[1]))
  except Exception as e:
    logging.exception(e)
    await ctx.channel.send("```{}```".format(traceback.format_exc()))


@GENERATE_CLASS.event
async def on_message(bot, msg):
  if msg.author == bot.user and msg.content.startswith(bot.prefix):
    pkg = msg.content[len(bot.prefix):].split(' ')
    
    if len(pkg) >= 1 and pkg[0] in bot.__class__.COMMANDS:
      cmd = pkg[0]
      
      if len(pkg) >= 2:
        args = pkg[1:]
      else:
        args = []
      
      try:
        await bot.__class__.COMMANDS.get(cmd)(bot, msg, args)
      except Exception as e:
        logging.exception(e)

@GENERATE_CLASS.event
async def on_ready(bot):
  print(f"logged in as {bot.user}")


# @GENERATE_CLASS.background
# async def print_screen(bot):
#   print("hello!!!", bot)
#   await asyncio.sleep(10)
