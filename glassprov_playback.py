import gevent.monkey
gevent.monkey.patch_all()
import wearscript
import argparse
import time
import SimpleHTTPServer
import SocketServer

from datetime import datetime
from datetime import timedelta
from apscheduler.scheduler import Scheduler
from time import sleep
import sys
import logging

client_name = ""
ws_global = ""
actor_pointer = 0
actor_list = ["will", "russ", "lexie", "max", "paul"];
delta_to_start = 1
delta_between_messages = 2
number_of_messages = 50
PORT = 8991

def http_server(arg):
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(( "", PORT ), Handler )

    print "serving at port", PORT
    httpd.serve_forever()

def ws_parse(parser):
    print "running ws_parse"
    wearscript.parse( callback, parser )

def send_time(time):
    print "Sending blob to actor %s" % actor_list[actor_pointer]
    ws_global.send('blob', actor_list[actor_pointer], str(time))
    increment_actor_pointer()

def increment_actor_pointer():
    global actor_pointer
    actor_pointer += 1
    if actor_pointer > len(actor_list) - 1:
        actor_pointer = 0

def callback(ws, **kw):
    global client_name
    global ws_global
    ws_global = ws
    print "Client client_endpoint: " + str(ws.ws.sock.getpeername())

    def registered(chan, name):
        global client_name
        print "I'm registered as: " + name
        client_name = name

    def get_blob(chan, title, body):
        print "Got blob %s %s" % (title,body)

    client_name = "%.6f" % time.time()
    print "Client ws callback, trying to register as " + client_name
    ws.subscribe( 'registered', registered)
    ws.subscribe( 'blob', get_blob)
    ws.send( 'register', 'registered', client_name)
    webserverGreenlet = gevent.spawn(http_server, "")
    print "Open browser to http://localhost:" + str(PORT) + "/stage-displays/viewer.html"
    schedulerGreenlet = gevent.spawn(main, "")
    ws.handler_loop()

def main(arg):
    sched = Scheduler()
    sched.start()
    logging.basicConfig()
    now = datetime.today()
    print "Now it's " + str( now )
    starttime = now + timedelta( seconds = delta_to_start )
    delta5sec = timedelta( seconds = delta_between_messages )
    thistime = starttime

    jobs = []
    print "Queueing jobs"
    for i in range( number_of_messages ):
        print "Queueing job at " + str( thistime )
        jobs.append( sched.add_date_job( send_time, thistime, [ thistime ] ))
        thistime += delta5sec
    print "Queued jobs"
    while True:
        sleep( 1 )
        sys.stdout.write( '.' )
        sys.stdout.flush()

if __name__ == '__main__':
    serverGreenlet = gevent.spawn(ws_parse, argparse.ArgumentParser())
    # schedulerGreenlet = gevent.spawn(main, "")
    print "And I made it past"
    # main()
    gevent.joinall([serverGreenlet])
