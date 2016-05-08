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

def get_pad(length):
    # [p] * p gives an array [p, p, p ...] of len p.
    return reduce(lambda x, y: (x << 8) ^ y, [length] * length, 0)

def get_modified_ciphertext(ct, block_size, current_block, current_position, guess, decoded):
    assert(isinstance(ct, str))
    assert((len(ct) % block_size) == 0)
    assert(isinstance(decoded, str))
    assert(0 <= current_position and current_position < block_size)
    
    parts = [ct[i:i + block_size] for i in range(0, len(ct), block_size)]
    b = parts[current_block]
    pad_len = (block_size - current_position + 1)
    pad = get_pad(pad_len)

    char_count = (block_size - current_position + 1)

    actual_guess = (guess << (block_size - current_position - 1))
    modded_block = int(b, 16) ^ pad ^ actual_guess ^ 1
    
    
def test_guess(ct_up_to_current_block, current_block, guess_position, decoded_msg):
    """
    The full CT is ct_up_to_current_block || current_block.
    decoded_msg is the bits decoded from the current_block, starting from the end.
    All numbers are in hex.
    eg, if ct_up_to_current_block = 1111
           current_block          = 2222
           decoded_msg            =   03

    the bits would line up as follows:
    11112222
          03

    """
    pass
               
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

    # print 'getting last byte of m[0]:'
    # for i in range(0, 255):
    #     iv_prime = '{0:x}'.format(iv_hex ^ 0x01 ^ i)
    #     test_ct = ''.join([iv_prime, ct_parts[0]])
    #     ret = po.query(test_ct)
    #     if ret:
    #         last_byte = ret
    #         print 'last byte value = {0}, hex = {0:x}, char = "{1}"'.format(i, chr(i))
    #         break

    last_byte = 32
    
    print 'getting 2nd-last byte:'
    for i in range(0, 255):
        print i
        iv_prime = '{0:x}'.format(iv_hex ^ 0x0202 ^ last_byte ^ (i << 8))
        test_ct = ''.join([iv_prime, ct_parts[0]])
        # print test_ct
        ret = po.query(test_ct)
        if ret:
            print '2nd last byte value = {0}, hex = {0:x}, char = "{1}"'.format(i, chr(i))
            break
    

###################

if __name__ == '__main__':
    main()
