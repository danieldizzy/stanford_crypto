# Functions.  At some point this will probably not be useful, as it's
# just a collection of one-liners that belong in the calling program.

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

def int_array_to_string(a):
    return ''.join(map(chr, a))
    
def string_to_chunked_array(s, n):
	if len(s) % n != 0:
		raise ValueError('len(s) = {0}, not div by {1}, for s = "{2}"'.format(len(s), n, s))
	parts = [s[i:i+n] for i in range(0, len(s), n)]
	return parts

def hexstring_to_int_array(s):
	return [int(e, 16) for e in string_to_chunked_array(s, 2)]

def string_to_hexstring(s):
	return int_array_to_hex_string(str_to_int_array(s))

def hexstring_to_char_string(s):
    return ''.join([chr(p) for p in hexstring_to_int_array(s)])

def xor_hex_strings(lhs, rhs):
    minlen = min(len(lhs), len(rhs))
    lhs_ia = hexstring_to_int_array(lhs[0:minlen])
    rhs_ia = hexstring_to_int_array(rhs[0:minlen])
    return map(lambda x: x[0] ^ x[1], zip(lhs_ia, rhs_ia))

def main():
    # misc manual tests
    print hexstring_to_int_array('ffaa01')
    print map(len, ['a','b'])

    input_string = 'hello'
    h = string_to_hexstring(input_string)
    print hexstring_to_char_string(h)
    print hexstring_to_char_string('00ffaa32')
    # for i in range(0, 256):
    #    print i, chr(i), chr(i ^ ord(' '))

    x = xor_hex_strings('00ff', '1111')
    print x
    print int_array_to_string(x)

    print string_to_hexstring('tim') # = 74696d
    x = xor_hex_strings('706061', '0409')
    print x
    print int_array_to_string(x)
    
if __name__ == '__main__':
    main()

# TODO - add test cases

# ==================
# Misc notes
#
# c1_hex = 0x09e1c5f70a65ac519458e7e53f36
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
# print '"{0}" cipher: 0{1:x}'.format(m1_raw, c1_hex)
# assert(c1 == xor_lists(key, m1))
# c1_hex = 0x6c73d5240a948c86981bc294814d
# c1 = hex_to_int_array(c1_hex)
# assert('{0:x}'.format(c1_hex) == int_array_to_hex_string(c1).lstrip('0'))
# c2 = xor_lists(c1, xor_lists(m1, m2))
# print string_to_chunked_array('string', 2)
# print string_to_chunked_array('string', 3)
