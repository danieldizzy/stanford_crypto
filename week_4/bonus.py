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

def get_blocked_decoded_message(msg, block_size):
    """Breaks decoded message into blocks, building the blocks from last char.
    eg, ('hello', 4) => ['h', 'ello']
    """
    mr = msg[::-1]
    mrparts = [mr[i:i + block_size] for i in range(0, len(mr), block_size)]
    mrparts = map(lambda x: ''.join(reversed(x)), mrparts)
    mrparts.reverse()
    return mrparts
    
def get_message_block_remainder(msg, block_size, total_blocks, current_block, current_block_position):
    char_count = block_size - current_block_position - 1
    assert(0 <= char_count and char_count < block_size)

    if char_count == 0: return None

    mb = get_blocked_decoded_message(msg, block_size)
    mb.reverse()
    i = total_blocks - current_block - 1
    m = mb[i]
    return m[(-1 * char_count):]


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
    

def print_current_message(msg_rev):
    msg = list(msg_rev)
    msg.reverse()
    print ''.join(map(chr, msg))


def get_most_likely_char_ords():
    """Provide ords for guesses with likely candidates first.
    These are looped through in order for positional guesses,
    so no sense in wasting time on non-printing chars."""
    ords = range(ord('a'), ord('z'))
    ords.extend(range(ord('A'), ord('Z')))
    ords.extend([i for i in range(32, 126) if i not in ords])
    ords.extend([i for i in range(0, 255) if i not in ords])
    return ords


def decode(ciphertext_string, block_size, oracle, max_iterations = 1000):

    # Convert to byte array, reverse it, starting at the beginning.
    # To check a position, xor it with the rev. of the message decoded
    # thus far, chop off any blocks at the start, xor the first few
    # positions with the pad as needed.  This is the base.  xor the
    # current pos with the guess, reverse, and check.  If successful,
    # set the message to this.
    

    DPB = 2  # digits per byte
    css = [ciphertext_string[i:i + DPB] for i in range(0, len(ciphertext_string), DPB)]
    ct = map(lambda x: int(x, 16), css)
    ct.reverse()  # Solved from last char to first.

    num_blocks = len(ct)/block_size
    msg_rev = [0] * len(ct)

    message_ord_code_candidates = get_most_likely_char_ords()
    
    ubound = block_size + min(max_iterations, len(msg_rev))
    for pos in range(block_size, ubound):
        # print 'calc at position {0}'.format(pos)
        xored = map(lambda x: x[0]^x[1], zip(msg_rev, ct))
        curr_block = pos/block_size
        chopped_ct = list(xored[(block_size * curr_block):])
        # print xored
        # print block_size
        # print curr_block
        # print chopped_ct

        padlen = (pos % block_size) + 1
        # print 'padlen: {0}'.format(padlen)
        for i in range(0, padlen):
            chopped_ct[i] ^= padlen

        # print chopped_ct

        # prepend the prior block from the original ct
        prior_block = ct[(curr_block - 1)*block_size:(curr_block*block_size)]
        actual_base = list(prior_block)
        actual_base.extend(chopped_ct)

        # position within the block we're guessing
        guess_pos = block_size + pos % block_size

        found_match = False
        for guess in message_ord_code_candidates:
            attempt = list(actual_base)
            attempt[guess_pos] ^= guess
            attempt.reverse()
            attempt = ''.join(map(lambda x: hex(x)[2:].zfill(2), attempt))
            print 'guess {0} for position {1}'.format(guess, pos)

            if oracle(attempt):
                found_match = True
                msg_rev[pos] = guess
                # print 'MATCH!'
                print_current_message(msg_rev)
                break
        
        if not found_match:
            raise ValueError('No match found at position {0}'.format(pos))

    msg_rev.reverse()
    return msg_rev

###################

if __name__ == '__main__':
    po = PaddingOracle()
    test = 'f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd'
    msgbytes = decode(test, 128/8, po.query, 7)
    print msgbytes
    print ''.join(map(chr, msgbytes))
