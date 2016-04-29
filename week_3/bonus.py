"""Week 3 bonus.

Hash of a long video file.
"""

from lib.helpers import *

def blockize(s, block_size):
    # consider a bytearray:
    # http://stackoverflow.com/questions/3943149/
    # reading-and-interpreting-data-from-a-binary-file-in-python
    # ba = bytearray(s)
    return map(lambda i: s[i:i+block_size], range(0, len(s), block_size))

def rev_hash(s, block_size, hashfunc):
    # Given a string s, breaks it up into blocks of size block_size.
    # Then starting at the end (which may have size < block_size), it
    # applies a hash, and appends the output to the block before that,
    # and so on, until it runs out of blocks.  Returns:
    # (finalhash, [[block0, hash1], [block1, hash2], ... [blockn, None]])
    blocks = blockize(s, block_size)
    blocks.reverse()
    ret = [[blocks[0], '']]
    for i in range(1, len(blocks)):
        h = hashfunc(''.join(blocks[i-1]))
        ret.append([blocks[i], h])
    hsh = hashfunc(''.join(ret[-1]))
    ret.reverse()
    return (hsh, ret)
             
###################


def main():
    print 'hello'

if __name__ == '__main__':
    main()
