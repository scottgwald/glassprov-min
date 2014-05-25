## The state of the state

The only thing that works is example_ping. Run these in
separate terminals.

    python example_ping.py client ws://localhost:8112/
    python example_ping.py server 8112

Standard out shows them talking to each other.

# Random notes

## Random

* perhaps should do all sending on separate greenlets? 

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
