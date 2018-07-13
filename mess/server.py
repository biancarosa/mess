from datetime import datetime

import Pyro4

from config import SERVER_NAME

class Message(object):

    def __init__(self, message):
        self.message = message
        self.date = datetime.now()

@Pyro4.expose
class Chat(object):
    def send_message(self, text):
        message = Message(text)
        print(f'{message.message} - received at {message.date:%H:%M:%S} \n')
        

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