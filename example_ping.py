import gevent.monkey
gevent.monkey.patch_all()
import wearscript
import argparse
import time

def ws_parse(parser):
    print "running ws_parse"
    wearscript.parse(callback, parser)

def callback(ws, **kw):

    def get_ping(chan, resultChan, timestamp):
    	print "Got ping %5f" % timestamp
    	ws.send(resultChan, time.time());
        # ws.publish(resultChan, timestamp, time.time(), ws.group_device)

    def get_pong(chan, timestamp):
    	print "Got pong %5f" % timestamp

    ws.subscribe('ping', get_ping)
    ws.subscribe('pong', get_pong)
    ws.send('ping', 'pong', time.time())
    ws.handler_loop()

if __name__ == '__main__':
    serverThread = gevent.spawn(ws_parse, argparse.ArgumentParser())
    print "And I made it past"
    gevent.joinall([serverThread])

# wearscript.parse(callback, argparse.ArgumentParser())
