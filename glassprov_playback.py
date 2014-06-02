import gevent.monkey
gevent.monkey.patch_all()
import wearscript
import argparse
import time

from datetime import datetime
from datetime import timedelta
from apscheduler.scheduler import Scheduler
from time import sleep
import sys
import logging

client_name = ""
ws_global = ""

def ws_parse(parser):
    print "running ws_parse"
    wearscript.parse(callback, parser)

def periodic_send(ws):
    #TODO(scottgwald): catch dead websocket
    # ws.send('blob', 'theMessage34234', 'fromOneToTheOther')
    ws.send('android:glass:f88fca2619bd', 'To: the charcoal glass. Love, ' + client_name);
    ws.send('android:glass:f88fca25588b', 'To: the sky glass. Love, ' + client_name);
    ws.send('android:glass:f88fca26183f', 'To: the cotton glass. Love, ' + client_name);
    ws.send('android:glass:f88fca26273d', 'To: the shale glass. Love, ' + client_name);
    gevent.spawn_later(5, periodic_send, ws)

def send_time(time):
    print "Sending blob " + str(time)
    ws_global.send('blob', 'will', str(time));

def callback(ws, **kw):
    global client_name
    global ws_global
    ws_global = ws

    def get_ping(chan, resultChan, timestamp):
        print "Got ping %5f" % timestamp
        ws.send(resultChan, time.time());
        # ws.publish(resultChan, timestamp, time.time(), ws.group_device)

    def registered(chan, name):
        global client_name
        print "I'm registered as: " + name
        client_name = name

    def get_blob(chan, title, body):
        print "Got blob %s %s" % (title,body)

    client_name = "%.6f" % time.time()
    print "Client ws callback, trying to register as " + client_name
    # ws.subscribe('ping', get_ping)
    ws.subscribe('registered', registered)
    ws.subscribe('blob', get_blob)
    ws.send('register', 'registered', client_name)
    gevent.spawn_later(5, periodic_send, ws)
    ws.handler_loop()

def my_job(text):
    print text

def main(arg):
    sched = Scheduler()
    sched.start()
    logging.basicConfig()
    now = datetime.today()
    print "Now it's " + str( now )
    starttime = now + timedelta( seconds = 1 )
    delta5sec = timedelta( seconds = 5 )
    thistime = starttime

    one_min_every_5_sec = []
    print "Queueing jobs"
    for i in range(12):
        print "Queueing job at " + str( thistime )
        one_min_every_5_sec.append( sched.add_date_job( send_time, thistime, [ thistime ] ))
        thistime += delta5sec
    print "Queued jobs"
    while True:
        sleep( 1 )
        sys.stdout.write( '.' )
        sys.stdout.flush()


if __name__ == '__main__':
    serverGreenlet = gevent.spawn(ws_parse, argparse.ArgumentParser())
    schedulerGreenlet = gevent.spawn(main, "")
    print "And I made it past"
    # main()
    gevent.joinall([serverGreenlet, schedulerGreenlet])
