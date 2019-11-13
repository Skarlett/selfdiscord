from util import parametrized_decorator
import discord
import logging
import aiohttp
import os
import gzip


logging = logging.getLogger(__name__)

# Couldn't get the discord.ext.Bot framework to work
# So lets just make our own framework.
class SelfBot(discord.Client):
  COMMANDS = dict()  # 'name': fn()
  EVT_HOOK = dict()  # 'evtName': set([coro(self, *args, **kwargs), ...])
  BG_TASKS =  set()  # set([ (coro(self, wait_for_result), coro()) , ...])
  
  def __init__(self, prefix, *args, **kwargs):
    logging.info(f"Discord.py[{discord.__version__}]")
    super().__init__(*args, **kwargs)
    self.prefix = prefix
    self.running = True
    
    self._setup_event_hooks()
    self._setup_bg_tasks()
    
  def _setup_event_hooks(self):
    def wraps(name):
      async def evt_wrapper(*args, **kwargs):
        for coro in self.__class__.EVT_HOOK[name]:
          await coro(self, *args, **kwargs)
      return evt_wrapper
    
    for evt_name in self.EVT_HOOK:
      logging.info(f"Adding event {evt_name}")
      setattr(self, evt_name, wraps(evt_name))
      
  def _setup_bg_tasks(self):
    async def wrapper():
      while self.running:
        await coro(self)
    
    for coro in self.__class__.BG_TASKS:
      logging.info(f"Adding background task {coro.__name__}")
      self.loop.create_task(wrapper())
    
  @classmethod
  @parametrized_decorator
  def command(coro, cls, name=None):
    # Assumes core.on_message is defined
    logging.info(f"Adding command {name or coro.__name__}")
    cls.COMMANDS[name or coro.__name__] = coro
    return coro
    
  @classmethod
  def event(cls, coro):
    container = cls.EVT_HOOK.get(coro.__name__)
    if container:
      container.add(coro)
    else:
      cls.EVT_HOOK[coro.__name__] = { coro }
    
    logging.info(f"Hooking event {coro.__name__}")
    return coro
    
  @classmethod
  def background(cls, coro):
    cls.BG_TASKS.add(coro)
    return coro
  
  async def purge_messages(self, channel, limit):
    async for message in channel.history(limit=limit):
      if message.author == self.user: # and not message.is_system():
        try:
          await message.delete(delay=0.6)
        except Exception as e:
          logging.warning(e)
          continue
  

async def download_message_attachments(directory, msg):
  async with aiohttp.ClientSession() as session:
      for attachment in msg.attachments:
        path = os.path.join(directory, attachment.url.split('/')[-1])
        resp = await session.get(attachment.url)
        with gzip.open(path, 'wb') as fd:
          try:
            fd.write(await resp.read())
          except Exception as e:
            logging.exception(e)
            logging.critical(f"Couldn't save \"{attachment.url}\" to {path}")
      
      
async def SOS(bot):
  '''
  Incase of unhandled exception, message maintainers the exception traceback
  '''
  logging.info("Sending SOS messages to Maintainers.")
  stack_str = "I've had an accident! Please help. Heres the details...\n\n```{}```".format(traceback.format_exc())
  if bot.sos:
    await bot.sos.send(stack_str)
