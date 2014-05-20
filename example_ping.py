import gevent.monkey
gevent.monkey.patch_all()
import wearscript
import argparse
import time

def ws_parse(parser):
    print "running ws_parse"
    wearscript.parse(callback, parser)

def periodic_send(ws):
	#TODO(scottgwald): catch dead websocket
    ws.send('blob', 'theMessage34234', 'fromOneToTheOther')
    gevent.spawn_later(5, periodic_send, ws)

def callback(ws, **kw):

    def get_ping(chan, resultChan, timestamp):
    	print "Got ping %5f" % timestamp
    	ws.send(resultChan, time.time());
        # ws.publish(resultChan, timestamp, time.time(), ws.group_device)

    def get_pong(chan, timestamp):
    	print "Got pong %5f" % timestamp

    def get_blob(chan, title, body):
    	print "Got blob %s %s" % (title,body)

    ws.subscribe('ping', get_ping)
    ws.subscribe('pong', get_pong)
    ws.subscribe('blob', get_blob)
    ws.send('ping', 'pong', time.time())
    gevent.spawn_later(5, periodic_send, ws)
    ws.handler_loop()

if __name__ == '__main__':
    serverThread = gevent.spawn(ws_parse, argparse.ArgumentParser())
    print "And I made it past"
    gevent.joinall([serverThread])

# wearscript.parse(callback, argparse.ArgumentParser())
