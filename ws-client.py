import gevent.monkey
gevent.monkey.patch_all()
import wearscript
import argparse

def ws_parse(parser):
    print "running ws_parse"
    wearscript.parse(callback, parser)

def periodic_send(ws):
    ws.send('blob', 'url', 'fromClientToServer')
    gevent.spawn_later(5, periodic_send, ws)

def callback(ws, **kw):
    def nametag_received(chan, payload):
        print "Nametag received %s" % payload

    def blob_received(chan, payload):
        print "Client blob received %s" % payload

    print('Got args[%r]' % (kw,))
    print('Demo callback, prints all inputs and sends nothing')
    ws.send('blob', 'url', 'fromClientToServer')
    # ws.subscribe('nametags', nametag_received)
    # ws.subscribe('blob', blob_received)
    gevent.spawn_later(5, periodic_send, ws)
    loop = gevent.spawn(ws.handler_loop)
    # while 1:
    #     print("I am the server receiving the content %s" % ws.receive())

if __name__ == '__main__':
    # wearscript.parse(callback, argparse.ArgumentParser())
    clientThread = gevent.spawn(ws_parse, argparse.ArgumentParser())
    print "And I made it past"
    gevent.joinall([clientThread])

#        loop = gevent.spawn(ws.handler_loop)
