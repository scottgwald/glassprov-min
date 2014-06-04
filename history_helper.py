import msgpack
import redis
import argparse

def main():
    r = redis.StrictRedis('localhost', 6379)
    dat = msgpack.load(open(args.file_name))
    r.delete(args.set_name)
    for text, score in dat:
        enc = msgpack.dumps( [ text, score ] )
        r.zadd(args.set_name, score, enc)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('file_name')
    parser.add_argument('set_name')
    args = parser.parse_args()
    main()
