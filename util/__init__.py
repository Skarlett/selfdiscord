
def parametrized_decorator(decorator):
  def wraps(*args, **kwargs):
    def repl(function):
      return decorator(function, *args, **kwargs)
    return repl
  return wraps
