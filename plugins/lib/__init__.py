from . import util
import discord
import logging

logging = logging.getLogger(__name__)

class SelfBot(discord.Client):
  COMMANDS = dict()  # 'name': fn()
  EVT_HOOK = dict()  # 'evtName': set([coro(self, *args, **kwargs), ...])
  BG_TASKS =  set()  # set([ (coro(self, wait_for_result), coro()) , ...])
  
  def __init__(self, prefix, plugin_manager, *args, **kwargs):
    logging.log(100, f"Discord.py[{discord.__version__}]")
    super().__init__(*args, **kwargs)
    self.prefix = prefix
    self.plugin_mgr = plugin_manager
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
      setattr(self, evt_name, wraps(evt_name))
      
  def _setup_bg_tasks(self):
    async def wrapper():
      while self.running:
        await coro(self)
    
    for coro in self.__class__.BG_TASKS:
      self.loop.create_task(wrapper())
    
  @classmethod
  @util.parametrized_decorator
  def command(coro, cls, name=None):
    # Assumes core.on_message is defined
    logging.debug(f"running command capture on {name or coro.__name__}")
    cls.COMMANDS[name or coro.__name__] = coro
    return coro
    
  @classmethod
  def event(cls, coro):
    container = cls.EVT_HOOK.get(coro.__name__)
    if container:
      container.add(coro)
    else:
      cls.EVT_HOOK[coro.__name__] = { coro }
    return coro
    
  @classmethod
  def background_task(cls, coro):
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
  


