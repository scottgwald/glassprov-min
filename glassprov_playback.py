from datetime import datetime
from datetime import timedelta
from apscheduler.scheduler import Scheduler
from time import sleep
import sys

def my_job(text):
    print text

def main():
    sched = Scheduler()
    sched.start()
    now = datetime.today()
    print "Now it's " + str( now )
    starttime = now + timedelta( seconds = 1 )
    delta5sec = timedelta( seconds = 5 )
    thistime = starttime

    one_min_every_5_sec = []
    print "Queueing jobs"
    for i in range(12):
        print "Queueing job at " + str( thistime )
        one_min_every_5_sec.append( sched.add_date_job( my_job, thistime, [ thistime ] ))
        thistime += delta5sec
    print "Queued jobs"
    while True:
        sleep( 1 )
        sys.stdout.write( '.' )
        sys.stdout.flush()

if __name__ == '__main__':
    print "Calling main."
    main()
