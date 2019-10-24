from plugins import GENERATE_CLASS
import settings
import logging

if __name__ == "__main__":
    logging.info("Starting...")
    settings.MODULES.load()
    client = GENERATE_CLASS(settings.PREFIX)
    with open('token.secret') as fd:
        token = fd.read().strip()
    
    client.run(token, bot=False)