from datetime import datetime
import sys
import threading

import uuid
import asyncio
import Pyro4

from config import SERVER_NAME

uuid = uuid.uuid4()
CALLBACK_SERVER_NAME = f'mess.client.{uuid}'

@Pyro4.expose
class Callback(object):

    def print_message(self, name, text):
        if name != CALLBACK_SERVER_NAME:
            print(text)


def register_callback_server():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(Callback)
    ns.register(CALLBACK_SERVER_NAME, str(uri))
    print(f'Ready to listen on {CALLBACK_SERVER_NAME}')
    daemon.requestLoop()

async def start_chatting(loop):
    text = ''
    server = Pyro4.Proxy(f"PYRONAME:{SERVER_NAME}")
    server.register(CALLBACK_SERVER_NAME)
    while (text != 'exit'):
        text = await loop.run_in_executor(None, sys.stdin.readline)
        text = text.strip()
        now = datetime.now()
        server.send_message(CALLBACK_SERVER_NAME, text)
        print(f'sent at {now:%H:%M:%S} \n')

if __name__ == '__main__':
    try:
        callback_thread = threading.Thread(
            target=register_callback_server, daemon=True)
        callback_thread.start()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_chatting(loop))
        loop.close()
    except (KeyboardInterrupt, EOFError):
        print('Goodbye! (:')
        exit
