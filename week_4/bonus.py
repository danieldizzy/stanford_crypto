"""Week 4 bonus.

This code is pretty messy ... don't have time to look for something
more elegant.
"""

import sys
import urllib2

from lib.helpers import *

###################

# Code from
# http://spark-university.s3.amazonaws.com/stanford-crypto/projects/pp4-attack_py.html
class PaddingOracle(object):
    def query(self, q):
        TARGET = 'http://crypto-class.appspot.com/po?er='
        target = TARGET + urllib2.quote(q)
        req = urllib2.Request(target)
        try:
            f = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            if e.code == 404:
                return True # good padding
            return False # bad padding
        return True  # Good padding (and no error!!)

def print_current_message(msg_rev):
    msg = list(msg_rev)
    msg.reverse()
    print ''.join(map(chr, msg))

def get_most_likely_char_ords():
    """Provide ords for guesses with likely candidates first.
    These are looped through in order for positional guesses,
    no sense in wasting time on non-printing chars."""
    ords = list(set([ord(c) for c in 'the and are is']))
    ords.extend(range(ord('a'), ord('z') + 1))
    ords.extend(range(ord('A'), ord('Z') + 1))
    ords.extend([i for i in range(0, 256) if i not in ords])
    return ords

def decode(ciphertext_string, block_size, oracle):
    """Messy decode function.

    The padding attack is done backwards from the end of the string,
    skipping the last block entirely, to the start of the string, i.e:

    +-------+-------------------------------+----------------+
    |  IV   | (working block)     g   pad   |  ct left as-is |
    +-------+-------------------------------+----------------+

    - 'g' is the guess
    - 'pad' is the ct xor the message xor the pad we're faking

    This method reverses the entire CT, skips the first block
    (which is the 'ct left as-is' block), and then works forwards:

                              pos
                               V
    +----------------+-------------------------------+-------+
    |  ct left as-is |    pad  g     (working block) |   IV  |
    +----------------+-------------------------------+-------+

    To check the padding oracle, the above is again reversed and
    then sent to the oracle.

    The decoded message is stored in an array initialized to zero,
    and is filled in as successful guesses are recorded:

    +----------------+-------------------------------+-------+
    |  . g 0 0 0 ... | 0 0 0 ...                     | 0 0 ..|
    +----------------+-------------------------------+-------+

    Note that only the block immediately before the current "working
    block" is needed when checking the oracle.

    """

    DPB = 2  # digits per byte
    css = [ciphertext_string[i:i + DPB] for i in range(0, len(ciphertext_string), DPB)]
    ct = map(lambda x: int(x, 16), css)
    ct.reverse()  # Solved from last char to first.

    num_blocks = len(ct)/block_size
    msg_rev = [0] * len(ct)

    message_ord_code_candidates = get_most_likely_char_ords()

    for pos in range(block_size, len(msg_rev)):
        curr_block = pos/block_size  # indexed from 0

        working_block = map(lambda x: x[0]^x[1], zip(msg_rev, ct))
        working_block = list(working_block[(block_size * curr_block):])
        padlen = (pos % block_size) + 1
        for i in range(0, padlen):
            working_block[i] ^= padlen

        # prepend the as-is block from the original (reverse) ct
        as_is_block = ct[(curr_block - 1)*block_size:(curr_block*block_size)]
        actual_base = list(as_is_block)
        actual_base.extend(working_block)

        # position within the block we're guessing
        guess_pos = block_size + (pos % block_size)

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
                print_current_message(msg_rev)
                break

        if not found_match:
            raise ValueError('No match found at position {0}'.format(pos))

    msg_rev.reverse()
    return msg_rev

###################

if __name__ == '__main__':

    # The full ciphertext:
    m =  'f20bdba6ff29eed7b046d1df9fb70000'
    m += '58b1ffb4210a580f748b4ac714c001bd'
    m += '4a61044426fb515dad3f21f18aa577c0'
    m += 'bdf302936266926ff37dbf7035d5eeb4'

    po = PaddingOracle()
    msgbytes = decode(m, 128/8, po.query)

    print msgbytes
    print ''.join(map(chr, msgbytes))
