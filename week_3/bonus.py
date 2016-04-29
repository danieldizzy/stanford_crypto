"""Week 3 bonus.

Hash of a long video file.
"""

import sys

from Crypto.Hash import SHA256
from lib.helpers import *

def pycrypto_sha256(message):
    hash = SHA256.new()
    hash.update(message)
    return hash.digest()

def blockize(s, block_size):
    # consider a bytearray:
    # http://stackoverflow.com/questions/3943149/
    # reading-and-interpreting-data-from-a-binary-file-in-python
    # ba = bytearray(s)
    return map(lambda i: s[i:i+block_size], range(0, len(s), block_size))

def rev_hash(s, block_size, hashfunc, debug = False):
    if not isinstance(s, bytearray):
        raise ValueError('must be bytearray')

    # Given a string s, breaks it up into blocks of size block_size.
    # Then starting at the end (which may have size < block_size), it
    # applies a hash, and appends the output to the block before that,
    # and so on, until it runs out of blocks.  Returns:
    # (finalhash, [[block0, hash1], [block1, hash2], ... [blockn, None]])
    blocks = blockize(s, block_size)
    blocks.reverse()
    hashes = [None]
    for i in range(1, len(blocks)):
        if debug:
            print '  hashing block {0} of {1}'.format(i, len(blocks))
        tmp = bytearray(blocks[i - 1])
        if hashes[-1] is not None:
            tmp.extend(hashes[-1])
        h = hashfunc(tmp)
        hashes.append(h)

    tmp = bytearray(blocks[-1])
    tmp.extend(hashes[-1])
    hsh = hashfunc(tmp)

    ret = zip(blocks, hashes)
    ret.reverse()
    return (hsh, ret)
             
###################


def main(filename):
    with open(filename, 'rb') as f:
        data = bytearray(f.read())
    ret = rev_hash(data, 1024, pycrypto_sha256)
    h = ret[0]
    print h
    print '{0:x}'.format(h)

if __name__ == '__main__':
    filename = sys.argv[1]
    if filename is None:
        print 'filename required'
    else:
        main(filename)
