"""
Suppose you are told that the one time pad encryption of the message "attack at dawn" is 09e1c5f70a65ac519458e7e53f36 (the plaintext letters are encoded as 8-bit ASCII and the given ciphertext is written in hex). What would be the one time pad encryption of the message "attack at dusk" under the same OTP key?

c1 = '09e ...'
m1 = 'attack at ...'
k XOR m1 = c1
k = c1 XOR m1

c2 = k XOR m2
c2 = (c1 XOR m1) XOR m2 = c1 XOR (m1 XOR m2)

"""

def str_to_int_array(s):
    return [ord(c) for c in s]

def xor_lists(a, b):
    return map(lambda x: x[0] ^ x[1], zip(a, b))

def hex_to_int_array(h):
    cparts = []
    c1_left = h
    while c1_left > 0:
        c1_left, r = divmod(c1_left, 256)
        cparts.append(int(r))
    cparts.reverse()
    return cparts

def int_array_to_hex_string(c):
    return ''.join(map(lambda x: hex(x)[2:].zfill(2), c))

# c1_hex = 0x09e1c5f70a65ac519458e7e53f36
c1_hex = 0x6c73d5240a948c86981bc294814d
m1_raw = "attack at dawn"
m2_raw = "attack at dusk"

c1 = hex_to_int_array(c1_hex)
m1 = str_to_int_array(m1_raw)
m2 = str_to_int_array(m2_raw)

# Sanity checks
assert('{0:x}'.format(c1_hex) == int_array_to_hex_string(c1).lstrip('0'))
assert(len(c1) == len(m1))

c2 = xor_lists(c1, xor_lists(m1, m2))
print '"{0}" cipher: 0{1:x}'.format(m1_raw, c1_hex)
print '"{0}" cipher: {1}'.format(m2_raw, int_array_to_hex_string(c2))

# Verify with key
key = xor_lists(c1, m1)
assert(c1 == xor_lists(key, m1))
assert(c2 == xor_lists(key, m2))


# ==================
# Misc notes
#
# print map(hex, c) # 1)
# print map(lambda x: hex(x), c)  # 2), same as 1)
# print map(lambda x: hex(x)[2:], c)  # 3), strip '0x'
# print map(lambda x: hex(x)[2:].zfill(2), c)  # 4), pad w/ 0

# Misc scratches:
# print 5 ^ 7  # ^ = python bitwise xor
# print [p ^ 7 for p in range(0, 22)]
# print [divmod(p, 7) for p in range(0, 22)]
# print int('f', 16)  = 15
# print int('10', 16) = 16
# print int('21', 16) = ...
# print 0x32a1  # A hex number
