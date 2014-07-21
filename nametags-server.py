from bottle import route, run, template
import redis

print "Starting app"
r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set("foo", "bar")
r.set("foos", "bars")
r.set("fooz", "barz")

res = r.get("foo")

print "got key 'foo' and result %s" % res

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/get')
def get():
	keys = r.keys()
	return template("""
		<ul>
		  % for key in keys:
		  	% val = r.get(key)
    		<li> {{ key }} {{ val }}</li>
  		  % end
		</ul>
		""", keys=keys, r=r)

@route('/set/<key>/<value>')
def set(key, value):
	r.set(key, value)
	keys = r.keys()
	return get()

run(host='scrumdiddly.dyndns.org', port=8111)

