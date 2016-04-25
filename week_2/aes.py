import itertools
import re

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
    """Create a binary number from an iterable of exponents.

    Note that if the same exponent appears twice, it is
    xored against itself and removed from the returned value."""
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

# syntactic sugar
def poly_from_string(s):
    """Helper, turn, eg, 'x^2 + 1' into [2, 0] (exponents)"""
    if s == '':
        return []

    def clean_term(x):
        tmp = re.sub(r' ', '', x)
        if tmp == '1':
            tmp = 'x^0'
        if tmp == 'x':
            tmp = 'x^1'
        if not '^' in tmp:
            raise ValueError('missing carat in poly term {0}'.format(x))
        tmp = re.sub(r'.*?\^', '', tmp)
        return int(tmp)

    d = s.split('+')    
    ret = map(clean_term, d)
    return ret

# sec 4.2 Multiplication
def poly_divmod(numerator, denom):
    """returns (quotient, remainder) of polynomials of the form
    sum(i=0..n)x^i.  Note all coefficients are 1.

    Args:
      numerator, denom: sets of ints, powers of x.
      e.g., (5, 3, 1, 0) = x^5 + x^3 + x + 1
    """
    # print 'divmod of {0} / {1}'.format(numerator, denom)
    quotient = []
    remainder = []
    left = numerator
    maxdenompower = max(denom)
    while len(left) > 0:
        # print 'left: {0} with len {1}'.format(left, len(left))
        if maxdenompower > max(left):
            for e in left:
                remainder.append(e)
            left = []
        else:
            # the next term to add to the quotient is the
            # max. power in what's left divided by the maxdenompower
            addexp = max(left) - maxdenompower
            quotient = add_binary_poly(quotient, [addexp])
            subtractpoly = map(lambda x: x + addexp, denom)

            # Odd: subtracting binary poly in mod 2 is the same as
            # xoring (adding) ?
            left = add_binary_poly(left, subtractpoly)
    return (quotient, remainder)


def _multiply_poly(a, b):
    """Multiplies binary polys (ref page 11)

    First, creates all pairs of exponents, then sums them.
    By converting the resulting poly to a bin, like
    exponent values cancel themselves out.  It's then converted
    back to a bin."""
    powers = [x + y for (x, y) in itertools.product(a,b)]
    return bin_to_poly(poly_to_bin(powers))

def multiply_poly_in_galois_field_256(bin_a, bin_b):
    t = _multiply_poly(bin_to_poly(bin_a), bin_to_poly(bin_b))
    divisor = (8, 4, 3, 1, 0)
    d, remainder = poly_divmod(t, divisor)
    return remainder

def bigdot_multiply(bin_a, bin_b):
    return multiply_poly_in_galois_field_256(bin_a, bin_b)

def xtime(bin_a):
    return poly_to_bin(multiply_poly_in_galois_field_256(bin_a, 0x02))


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

def shift_single_row(r, left_shift_count):
    def shift_once(r):
        return [r[1], r[2], r[3], r[0]]
    for i in range(0, left_shift_count):
        r = shift_once(r)
    return r

def shift_rows(state):
    return [shift_single_row(state[i], i) for i in range(0, 4)]

# 5.1.3 MixColumns() Transformation

def GF_256_byte_mult(bin_a, bin_b):
    """Galois Field (256) Multiplication of two bytes."""
    # ref https://en.wikipedia.org/wiki/Rijndael_mix_columns
    p = 0
    for counter in range(0, 8):
        if bin_b & 1:
            p ^= bin_a
        hi_bit_set = (bin_a & 0x80 != 0)
        # print 'curr val:  {0}'.format(bin_a)
        bin_a <<= 1
        # print 'shifted:   {0}'.format(bin_a)
        (_, bin_a) = divmod(bin_a, (1 << 8))
        # print 'remainder: {0}'.format(bin_a)
        if hi_bit_set:
            bin_a ^= 0x1b;  # x^8 + x^4 + x^3 + x + 1
        bin_b >>= 1
    return p

def mix_single_column(c):
    (s0, s1, s2, s3) = (c[0], c[1], c[2], c[3])

    def dot(a, b):
        # return GF_256_byte_mult(a, b)
        return poly_to_bin(bigdot_multiply(a, b))

    # using 'rn' = 's-prime-n'
    r0 = dot(2, s0) ^ dot(3, s1) ^ s2         ^ s3
    r1 = s0         ^ dot(2, s1) ^ dot(3, s2) ^ s3
    r2 = s0         ^ s1         ^ dot(2, s2) ^ dot(3, s3)
    r3 = dot(3, s0) ^ s1         ^ s2         ^ dot(2, s3)

    return [r0, r1, r2, r3]
