## The state of the state

Working: glassprov\_client, glassprov\_server. Example:

    python glassprov_server.py server 8112
    python glassprov_client.py client ws://localhost:8112/

Standard out shows them talking to each other.

# Random notes

## Registration protocol

The server callback subscribes to 'register' messages.
The client sends a 'register' message declaring its
channel/socket name. The server keeps a dictionary of
these names, keyed on the websocket objects. 

We'll have the client send its own name as a string.
It can always use a (e.g. microsecond) timestamp as
an id to easily come up with a unique name. 

When the clients are phones and Glasses, they can use
WS.groupDevice() to get their channel name. Then this
will be consistent with the way the Go server works. 
