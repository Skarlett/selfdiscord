import bootstrap
import logging

PREFIX = "!m "
MODULES = bootstrap.DynamicImport('plugins')

logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)
