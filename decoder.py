#!/usr/bin/python
import json
import zlib

#data = open(sys.argv[1]).read()
data = raw_input('Please enter string:')
dl = data.split(':')

def decode(data):
    zflag = data[0]
    data = data[1:]
    res = ''
    for byte in data:
        res = res + chr(int(byte, 16))
    data = ''
    if zflag == '01':
        #print 'zip'
        data = zlib.decompress(res)
    else:
        #print 'nozip'
        data = res
    return data

def encoding_change(data):
    #print type(data)
    if type(data) == type(u''):
        #print data.encode('utf-8')
        return data.encode('utf-8')
    if type(data) == type([]):
        for i in range(len(data)):
            data[i] = encoding_change(data[i])
        return data
    if type(data) == type({}):
        for i in data.keys():
            data[i] = encoding_change(data[i])
        return data
    return data


idx = 0
while idx < len(dl):
    slen = dl[idx] + dl[idx+1]
    length = int(slen, 16)
    if length > 0:
        data = dl[idx+2:idx+length+2]
        res = decode(data)
        print json.dumps((json.loads(res)), sort_keys = False, indent = 4)
        if idx + length + 2 < len(dl):
            print '------------------------------------------------------------------'
    idx += length + 2

