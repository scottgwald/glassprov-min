# Python: Client or Server
import wearscript
import argparse
import time

def callback(ws, **kw):

    def get_ping(chan, resultChan, timestamp):
    	print "Got ping %s" % timestamp
        ws.publish(resultChan, timestamp, time.time(), ws.group_device)

    ws.subscribe('ping', get_ping)
    ws.send('ping', 'url', 'fromServerToClientLater')
    ws.handler_loop()

wearscript.parse(callback, argparse.ArgumentParser())
