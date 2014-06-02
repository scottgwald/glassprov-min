## The state of the state

Working: glassprov\_client, glassprov\_server. Example:

    python glassprov_server.py server 8112
    python glassprov_client.py client ws://localhost:8112/

Standard out shows them talking to each other.

# Random notes

## TODO

* Does reconnection (e.g. when server is restarted and clients 
    subsequently reconnect) fail to call callback?

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

## Model for narrowcasting

The Android client treats the channel with name equal to
its own groupDevice string specially: for instance it
checks to see if the second argument ("command") is "script"
or "lambda". So I'll adopt the convention that we narrowcast
to channels with a groupDevice name ("x") of a connected device,
but we keep the channel name "x" rather than stripping it
away and sending the rest of the arguments only to that device.

## How to launch "playback"

    python glassprov_server.py server 8112
    python glassprov_playback.py client ws://localhost:8112/
    http://localhost:8112/stage-displays/viewer.html

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

## Bugs

client occasionally dies when I switch back and forth between playground and custom endpoint

restarting client leads to duplicated messages broadcast by server:

    Sending to socket dashboard:02/06/2014 @ 10:43:37 with args ('blob', 'max', '2014-06-02 10:43:54.399516')
    server: Packing and sending
    Sending to socket dashboard:02/06/2014 @ 10:43:37 with args ('blob', 'max', '2014-06-02 10:43:54.399516')
    server: Packing and sending
    Sending to socket dashboard:02/06/2014 @ 10:43:37 with args ('blob', 'max', '2014-06-02 10:43:54.399516')
    server: Packing and sending

Hypothesis: multiple reconnecting websockets register with same id, 1-sec resolution is
too coarse

## Todos

1. wake feature
2. ping back indicating glasses connected

nice features:
(1) clear screen
(2) allow curation

make sure I can turn off debug to stop reuse

## before we go

* iconic ar video



