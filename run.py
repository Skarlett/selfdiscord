from controller import SelfBot
import settings
import logging

if __name__ == "__main__":
    logging.info("Starting...")
    client = SelfBot(settings.PREFIX)
    with open('token.secret') as fd:
        token = fd.read().strip()
    
    client.run(token, bot=False)