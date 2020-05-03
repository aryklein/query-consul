#!/usr/bin/python

import urllib.request
import json
import argparse
import itertools
import threading
import time
import sys

# spinning cursor
def spinning_cursor():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        print('\033[1;32;40m\r{}\033[0m'.format(c),end = '')
        time.sleep(0.1)

# parser for command-line options
parser = argparse.ArgumentParser(description='Query Consul for a service in all datacenters.')
parser.add_argument('-a', '--consul-addr', dest='consul_addr', help='Consul address[:port]', required=True)
parser.add_argument('-s', '--consul-srv', dest='consul_srv', help='Consul Service', required=True)
args = vars(parser.parse_args())

# variables
consul_addr = args['consul_addr']
consul_srv = args['consul_srv']
dc_url = 'http://{}/v1/catalog/datacenters'.format(consul_addr)
srv_url = 'http://{}/v1/catalog/service/'.format(consul_addr)

# start spinning cursor :)
done = False
t = threading.Thread(target=spinning_cursor)
t.start()

try:
    req = urllib.request.urlopen(dc_url)
except urllib.error.URLError:
    done = True
    print('\rError: name or service not known')
    sys.exit(1)

dc_list = json.loads(req.read().decode('utf-8'))
for dc in dc_list:
    req = urllib.request.urlopen('{}{}?dc={}'.format(srv_url, consul_srv, dc))
    data = json.loads(req.read().decode('utf-8'))
    if data:
        print('\r******************')
        print('Consul datacenter: {}'.format(data[0]['Datacenter']))
        print('Node: {}'.format(data[0]['Node']))
        print('Port: {}'.format(data[0]['ServicePort']))

done = True
print('\r******************')
