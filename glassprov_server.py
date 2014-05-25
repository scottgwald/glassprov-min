import gevent.monkey
gevent.monkey.patch_all()
import geventwebsocket.exceptions
import wearscript
import argparse
import time
import sys

ws_dict = {}

def ws_parse(parser):
    print "running ws_parse"
    wearscript.parse(callback, parser)

def ws_send(ws, *argv):
    global ws_dict
    print "Sending to socket " + ws_dict[ws]
    try:
        ws.send(*argv)
    except geventwebsocket.exceptions.WebSocketError:
        print "Sending failed, removing ws from ws_dict: " + ws_dict[ws], sys.exc_info()[0]
        del ws_dict[ws]
    except:
        print "Unexpected exception while sending, removing ws from ws_dict: " + ws_dict[ws], sys.exc_info()[0]
        del ws_dict[ws]

# broadcasts to all but the sender
def broadcast(ws_src, *argv):
    global ws_dict
    for ws in ws_dict.keys():
        # don't send it back to the source websocket
        if ws is not ws_src:
            gevent.spawn(ws_send, ws, *argv)

def callback(ws, **kw):
    global ws_dict
    def register_client(chan, resultChan, timestamp):
        if ws not in ws_dict.itervalues():
            print "Registering websocket: " + timestamp
            ws_dict[ws] = timestamp
        else:
            print "Got a registration ping from the same websocket"
        ws.send(resultChan, timestamp)

    def get_blob(chan, title, body):
        print "Server: Got blob %s %s" % (title,body)
        broadcast(ws, title, body)

    ws.subscribe('register', register_client)
    ws.subscribe('blob', get_blob)
    ws.handler_loop()

if __name__ == '__main__':
    serverThread = gevent.spawn(ws_parse, argparse.ArgumentParser())
    print "And I made it past"
    gevent.joinall([serverThread])

# wearscript.parse(callback, argparse.ArgumentParser())
