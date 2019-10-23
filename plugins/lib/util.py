import logging.handlers
import os
import shutil
import gzip
import traceback


####
# Custom Log rotate handler
# + Gunzip Compressed
# + Timed
# + Auto Deleted
class TimedGunzippedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
  def doRollover(self):
    if self.stream:
      self.stream.close()
    
    if self.backupCount > 0:
      for i in range(self.backupCount - 1, 0, -1):
        sfn = "%s.%d.gz" % (self.baseFilename, i)
        dfn = "%s.%d.gz" % (self.baseFilename, i + 1)
        if os.path.exists(sfn):
          if os.path.exists(dfn):
            os.remove(dfn)
          os.rename(sfn, dfn)
      
      dfn = self.baseFilename + ".1.gz"
      if os.path.exists(dfn):
        os.remove(dfn)
      
      with open(self.baseFilename, 'rb') as f_in, gzip.open(dfn, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    
    self.mode = 'w'
    self.stream = self._open()

def parametrized_decorator(decorator):
  def wraps(*args, **kwargs):
    def repl(function):
      return decorator(function, *args, **kwargs)
    return repl
  return wraps

async def SOS():
  '''
  Incase of unhandled exception, message maintainers the exception traceback
  '''
  logging.info("Sending SOS messages to Maintainers.")
  stack_str = "I've had an accident! Please help. Heres the details...\n\n```{}```".format(traceback.format_exc())
  if bot.sos:
    await bot.sos.send(stack_str)


