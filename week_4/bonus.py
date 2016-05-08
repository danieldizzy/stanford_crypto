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
    ct_parts = parts[1:]
    print parts
    print IV
    print ct_parts

    iv_hex = int(IV, 16)

    print 'getting last byte of m[0]:'
    for i in range(0, 255):
        # print i
        iv_prime = '{0:x}'.format(iv_hex ^ 0x01 ^ i)
        test_ct = ''.join([iv_prime, ct_parts[0]])
        # print test_ct
        ret = po.query(test_ct)
        if ret:
            print 'last byte value = {0}, char = "{1}"'.format(i, chr(i))
            break


###################

if __name__ == '__main__':
    main()
