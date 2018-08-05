from datetime import datetime
import threading

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
        # send to servers
        send_multicast_message(message.message)


def start_server():
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(Chat)
    ns.register(SERVER_NAME, str(uri))
    print(f'Ready to listen on {SERVER_NAME}')
    daemon.requestLoop()

def receive_multicast_messages():
    import socket
    import struct

    multicast_group = '224.3.29.71'
    server_address = ('', 10000)

    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind to the server address
    sock.bind(server_address)
    # Tell the operating system to add the socket to the multicast group
    # on all interfaces.
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    # Receive/respond loop
    while True:
        try:
            print('\nwaiting to receive message')
            data, address = sock.recvfrom(1024)
            
            print('received %s bytes from %s' % (len(data), address))
            print(data)

            print('sending acknowledgement to', address)
            sock.sendto(b'ack', address)
        except Exception as e:
            print(e)

def send_multicast_message(message):
    import socket
    import struct

    multicast_group = ('224.3.29.71', 10000)

    # Create the datagram socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set a timeout so the socket does not block indefinitely when trying
    # to receive data.
    sock.settimeout(0.2)
    # Set the time-to-live for messages to 1 so they do not go past the
    # local network segment.
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
    try:

        # Send data to the multicast group
        print('sending "%s"' % message)
        sent = sock.sendto(bytes(message, 'utf-8'), multicast_group)
        print(sent)
        # Look for responses from all recipients
        while True:
            print('waiting to receive')
            try:
                data, server = sock.recvfrom(16)
            except socket.timeout:
                print('timed out, no more responses')
                break
            else:
                print('received "%s" from %s' % (data, server))
    except Exception as e:
        print(e)
    finally:
        print('closing socket')
        sock.close()


if __name__ == '__main__':
    try:
        server_thread = threading.Thread(
            target=start_server, daemon=True)
        server_thread.start()
        receive_multicast_messages()
    except (KeyboardInterrupt, EOFError):
        print('Goodbye! (:')
        exit
