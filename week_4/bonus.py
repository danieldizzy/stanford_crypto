"""Week 4 bonus.
"""

import sys
import urllib2

from lib.helpers import *

###################

# Initial string:
CIPHERTEXT = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4'

# Code from
# http://spark-university.s3.amazonaws.com/stanford-crypto/projects/pp4-attack_py.html

TARGET = 'http://crypto-class.appspot.com/po?er='

class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib2.quote(q)
        req = urllib2.Request(target)
        try:
            f = urllib2.urlopen(req)
        except urllib2.HTTPError, e:          
            if e.code == 404:
                return True # good padding
            return False # bad padding


def main():
    po = PaddingOracle()
    # print po.query(ct)
    sz = 128 / 4  # Each char is a hex digit, 4 bits.  128-bit block.
    parts = [CIPHERTEXT[i:i+sz] for i in range(0, len(CIPHERTEXT), sz)]
    IV = parts[0]
    m = parts[1:]
    print parts
    print IV
    print m
    print 'hello'

###################

if __name__ == '__main__':
    main()
