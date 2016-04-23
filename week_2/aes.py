
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
