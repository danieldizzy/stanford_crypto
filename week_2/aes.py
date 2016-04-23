
###################
# AES functions

# Implementations of the standard: http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf

# State
# sec 3.4 - The State

def load_state(vec):
    "create 4-row, 4-col table from 16-element vector."
    assert(len(vec) == 16)
    ret = map(lambda x: map(lambda n: vec[n], range(x, x+13, 4)), range(0, 4))
    assert(len(ret) == 4)
    return ret

def output_state(state):
    assert(len(state) == 4)
    ret = [state[r][c] for c in range(0, 4) for r in range(0, 4)]
    assert(len(ret) == 16)
    return ret

def poly_to_bin(poly, initializer = 0x00):
    return reduce(lambda h, val: h ^ (1 << val), poly, initializer)

def bin_to_poly(bin):
    ret = []
    curr = bin
    i = 0
    while curr > 0:
        if curr % 2 == 1:
            ret.append(i)
        i += 1
        curr = curr >> 1
    ret.reverse()
    return ret

def add_binary_poly(lhs, rhs):
    total = poly_to_bin(rhs, poly_to_bin(lhs))
    return bin_to_poly(total)

# 5.1.1 SubBytes()Transformation
def get_subbytes_transformation(s):
    raw_data = """63 7c 77 7b f2 6b 6f c5 30 01 67 2b fe d7 ab 76
ca 82 c9 7d fa 59 47 f0 ad d4 a2 af 9c a4 72 c0
b7 fd 93 26 36 3f f7 cc 34 a5 e5 f1 71 d8 31 15
04 c7 23 c3 18 96 05 9a 07 12 80 e2 eb 27 b2 75
09 83 2c 1a 1b 6e 5a a0 52 3b d6 b3 29 e3 2f 84
53 d1 00 ed 20 fc b1 5b 6a cb be 39 4a 4c 58 cf
d0 ef aa fb 43 4d 33 85 45 f9 02 7f 50 3c 9f a8
51 a3 40 8f 92 9d 38 f5 bc b6 da 21 10 ff f3 d2
cd 0c 13 ec 5f 97 44 17 c4 a7 7e 3d 64 5d 19 73
60 81 4f dc 22 2a 90 88 46 ee b8 14 de 5e 0b db
e0 32 3a 0a 49 06 24 5c c2 d3 ac 62 91 95 e4 79
e7 c8 37 6d 8d d5 4e a9 6c 56 f4 ea 65 7a ae 08
ba 78 25 2e 1c a6 b4 c6 e8 dd 74 1f 4b bd 8b 8a
70 3e b5 66 48 03 f6 0e 61 35 57 b9 86 c1 1d 9e
e1 f8 98 11 69 d9 8e 94 9b 1e 87 e9 ce 55 28 df
8c a1 89 0d bf e6 42 68 41 99 2d 0f b0 54 bb 16"""
    def make_int(x): return int(x, 16)
    data = [map(make_int, d.split(' ')) for d in raw_data.split('\n')]
    row, col = divmod(s, 16)
    return data[row][col]

def subbyte_transform_state(state):
    vec = output_state(state)
    tx = map(get_subbytes_transformation, vec)
    return load_state(tx)
