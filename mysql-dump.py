import MySQLdb
from time import mktime
import datetime
import msgpack

outfile = "awe-lines.msgpack"
db = MySQLdb.connect( host = "localhost", user = "root", passwd = "", db = "dashboard" )

cur = db.cursor()

cur.execute( "select * from voting_line" )

dat = []

for id, text, dt in cur.fetchall():
    if type(dt) is datetime.datetime:
        dat.append([text, mktime(dt.timetuple())])
        print text, mktime(dt.timetuple())
    else:
        dat.append([text, "+inf"])
        print text, "Never used"

msgpack.dump(dat, open(outfile, 'w'))



