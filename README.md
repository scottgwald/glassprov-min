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

## Brainstorming

Need simplest possible protocol for GlassProv.

Requirements:

1. Need the browser client to be able to 
   send lines/cues to all the Glasses

   - open question: do Glasses get all messages
     and pick out their own, or do we have the
     sender specify who gets them? 

2. The sender definitely needs to know the names
   of the devices/channels in order to specify 
   which client gets which. 

3. Server needs to be able to send "script" commands

With everyone talking to everyone, it might be
worthwhile to introduce narrowcasting similar to
the Go server.

Could do narrowcast/broadcast commands.

Am a little constrained by the lack of a catch-all
callback option in wearscript-python.

Two sync strategies:
deltas
full lists

Make sure that, if all Glasses are getting all messages,
a Glass [x] receiving a message that is meant for [y],
with (x != y) will not modify its behavior.




