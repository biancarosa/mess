from datetime import datetime

import Pyro4

from config import SERVER_NAME

@Pyro4.expose
class Chat(object):
    def send_message(self, text):
        now = datetime.now()
        print(f'{text} - received at {now:%H:%M:%S} \n')

def start_server():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(Chat)
    ns.register(SERVER_NAME, str(uri))
    print(f'Ready to listen on {SERVER_NAME}')
    daemon.requestLoop()


if __name__ == '__main__':
    try:
        start_server()
    except (KeyboardInterrupt, EOFError):
        print('Goodbye! (:')
        exit