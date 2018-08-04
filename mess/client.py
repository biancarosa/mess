from datetime import datetime
import sys
import Pyro4
import asyncio

from config import SERVER_NAME

server = Pyro4.Proxy(f"PYRONAME:{SERVER_NAME}")

async def start_chatting(loop):
    text = ''
    while (text != 'exit'):
        text = await loop.run_in_executor(None, sys.stdin.readline)
        text = text.strip()
        now = datetime.now()
        server.send_message(text)
        print(f'sent at {now:%H:%M:%S} \n')

if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_chatting(loop))
        loop.close()
    except (KeyboardInterrupt, EOFError):
        print('Goodbye! (:')
        exit