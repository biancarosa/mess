from datetime import datetime

import Pyro4

from config import SERVER_NAME

class Message(object):

    def __init__(self, message):
        self.message = message
        self.date = datetime.now()

    def __str__(self):
        return f'{self.message} - received at {self.date:%H:%M:%S} \n'

CLIENTS = {}

@Pyro4.expose
class Chat(object):
    
    def register(self, name):
        print(f'Client {name} registered')
        client = Pyro4.Proxy(f"PYRONAME:{name}")
        CLIENTS[name] = client

    def send_message(self, sender, text):
        message = Message(text)
        print(f"Received {message} from {sender}")
        for name in CLIENTS.keys():
            client = CLIENTS[name]
            client.print_message(sender, message.__str__())

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