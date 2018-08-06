from datetime import datetime
import threading
import socket
import struct

import Pyro4

from config import SERVER_NAME


class Message(object):

    def __init__(self, message):
        self.message = message
        self.date = datetime.now()

    def __str__(self):
        return f"{self.message}\nreceived at {self.date:%H:%M:%S} \n"


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
        send_multicast_message(f"{sender}_{message.__str__()}")
    
    def send_message_to_clients(self, sender, text):
        for name in CLIENTS.keys():
            client = CLIENTS[name]
            client.print_message(sender, text)

def start_server():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(Chat)
    ns.register(SERVER_NAME, str(uri))
    print(f'Ready to listen on {SERVER_NAME}')
    daemon.requestLoop()

def receive_multicast_messages():
    multicast_group = '224.3.29.71'
    server_address = ('', 10000)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        try:
            print('\nwaiting to receive message')
            data, address = sock.recvfrom(1024)
            
            print('received %s bytes from %s' % (len(data), address))
            chat = Chat()
            data = data.decode("utf-8").split('_')
            chat.send_message_to_clients(data[0], data[1])

            print('sending acknowledgement to', address)
            sock.sendto(b'ack', address)
        except Exception as e:
            print(e)

def send_multicast_message(message):
    try:

        print('sending "%s"' % message)
        SOCK.sendto(bytes(message, 'utf-8'), multicast_group)
        while True:
            print('waiting to receive')
            try:
                data, server = SOCK.recvfrom(16)
            except socket.timeout:
                print('timed out, no more responses')
                break
            else:
                print('received "%s" from %s' % (data, server))
    except Exception as e:
        print(e)

SOCK = None

if __name__ == '__main__':
    try:
        server_thread = threading.Thread(
            target=start_server, daemon=True)
        server_thread.start()

        multicast_group = ('224.3.29.71', 10000)
        SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        SOCK.settimeout(5)
        receive_multicast_messages()
    except (KeyboardInterrupt, EOFError):
        print('Goodbye! (:')
        exit
    finally:
        print('closing socket')
        SOCK.close()
