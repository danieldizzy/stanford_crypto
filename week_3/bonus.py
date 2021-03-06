"""Week 3 bonus.

Hash of a long video file.
"""

import sys

from Crypto.Hash import SHA256
from lib.helpers import *

def pycrypto_sha256(message):
    hash = SHA256.new()
    hash.update(message)
    s = hash.hexdigest()
    return hexstring_to_int_array(s)

def create_blocks(s, block_size):
    return map(lambda i: s[i:i+block_size], range(0, len(s), block_size))

def rev_hash(s, block_size, hashfunc, save_all_block_hashes = True):
    if not isinstance(s, bytearray):
        raise ValueError('must be bytearray')

    # Given a string s, breaks it up into blocks of size block_size.
    # Then starting at the end (which may have size < block_size), it
    # applies a hash, and appends the output to the block before that,
    # and so on, until it runs out of blocks.  Returns:
    # (finalhash, [[block0, hash1], [block1, hash2], ... [blockn, None]])
    blocks = create_blocks(s, block_size)
    blocks.reverse()
    hashes = [None]
    for i in range(1, len(blocks)):
        print '  hashing block {0} of {1}'.format(i, len(blocks))
        tmp = bytearray(blocks[i - 1])
        if hashes[-1] is not None:
            tmp.extend(hashes[-1])
        h = hashfunc(tmp)

        # Hacky.
        if save_all_block_hashes:
            hashes.append(h)
        else:
            hashes[0] = h

    tmp = bytearray(blocks[-1])
    h = hashes[-1]
    if h is not None:
        tmp.extend(h)
    hsh = hashfunc(tmp)

    if not save_all_block_hashes:
        return (hsh, [])

    ret = zip(blocks, hashes)
    ret.reverse()
    return (hsh, ret)
             
###################


def main(filename):
    with open(filename, 'rb') as f:
        data = bytearray(f.read())
    ret = rev_hash(data, 1024, pycrypto_sha256)
    h = ret[0]
    return int_array_to_hex_string(h)

###################
# Prep:
#
# Get the test files given in the assignment:
#
# sample file with the given sha:
# $ wget https://class.coursera.org/crypto-preview/lecture/download.mp4?lecture_id=28 -O test.mp4
# $ python -m week_3.bonus test.mp4
#
# Actual file:
# $ wget https://class.coursera.org/crypto-preview/lecture/download.mp4?lecture_id=27 -O actual.mp4
# $ python -m week_3.bonus actual.mp4

if __name__ == '__main__':
    filename = sys.argv[1]
    if filename is None:
        print 'filename required'
    else:
        print main(filename)
