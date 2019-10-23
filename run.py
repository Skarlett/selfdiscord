from plugins import GENERATE_CLASS
import settings
import logging

if __name__ == "__main__":
    logging.info("Starting...")
    settings.MODULES.load()
    client = GENERATE_CLASS(settings.PREFIX, settings.MODULES)
    client.run("MTkxNzkzNDM2OTc2ODczNDcz.XKTGQA.BTDW1P90j3XAulAqOByKyI4djso", bot=False)