import bootstrap
import logging

PREFIX = "!m "
MODULES = bootstrap.DynamicImport('plugins')

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.CRITICAL)
