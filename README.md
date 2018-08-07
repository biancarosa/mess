# mess
mess is a distributed chat system that uses smart objects to send and receive messages and multicast sockets to share messages across multiple servers

# docs

current docs in pt-br here: [http://biancarosa.com.br/mess/](http://biancarosa.com.br/mess/)

# architecture

The system can have one or more from multiple nodes. The nodes can live in the same machine or in differente machines.
Each node has two modules: a client and a server. A node needs to have one server and zero or more clients.

- Client module: The client module is responsible for giving the user and interface to send an read messages sent from other clients.
In order to achieve this, the client has a small server responsible for receiving messages sent from other clients.

- Server module: The server module is responsible for receiving messages from clients and sending the message from other clients, across multiple nodes.
In order to achieve this, the server sends the message to all clients registered in this node and also uses a multicast socket to send the message across servers. The server must listen to a multicast socket to listen from other clients.

# usage

You'll need a vagrant in your machine. If you want to run without a VM, you should run the ansible-playbook in your machine or the equivalent commands for your OS.

# packaging 

There is a script named `generate_artefacts.sh` that creates artefacts based on the project folder.

# credits

made with :heart: with Python 3.6
