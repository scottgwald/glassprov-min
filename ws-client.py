import wearscript
import argparse

if __name__ == '__main__':
    def callback(ws, **kw):
        print('Got args[%r]' % (kw,))
        print('I am the client. Demo callback, prints all inputs and sends nothing')
        ws.send('blob', 'url', 'fromClientToServer')
        while 1:
        	print('I am the client receiving the content %s' % ws.receive())

    wearscript.parse(callback, argparse.ArgumentParser())

