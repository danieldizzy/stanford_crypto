"""
Many Time Pad

Let us see what goes wrong when a stream cipher key is used more than once. Below are eleven hex-encoded ciphertexts that are the result of encrypting eleven plaintexts with a stream cipher, all with the same stream cipher key. Your goal is to decrypt the last ciphertext, and submit the secret message within it as solution.

Hint: XOR the ciphertexts together, and consider what happens when a space is XORed with a character in [a-zA-Z].
"""

import sys
import itertools

from lib.helpers import *

# ==========

c1 = "315c4eeaa8b5f8aaf9174145bf43e1784b8fa00dc71d885a804e5ee9fa40b16349c146fb778cdf2d3aff021dfff5b403b510d0d0455468aeb98622b137dae857553ccd8883a7bc37520e06e515d22c954eba5025b8cc57ee59418ce7dc6bc41556bdb36bbca3e8774301fbcaa3b83b220809560987815f65286764703de0f3d524400a19b159610b11ef3e"

c2 = "234c02ecbbfbafa3ed18510abd11fa724fcda2018a1a8342cf064bbde548b12b07df44ba7191d9606ef4081ffde5ad46a5069d9f7f543bedb9c861bf29c7e205132eda9382b0bc2c5c4b45f919cf3a9f1cb74151f6d551f4480c82b2cb24cc5b028aa76eb7b4ab24171ab3cdadb8356f"

c3 = "32510ba9a7b2bba9b8005d43a304b5714cc0bb0c8a34884dd91304b8ad40b62b07df44ba6e9d8a2368e51d04e0e7b207b70b9b8261112bacb6c866a232dfe257527dc29398f5f3251a0d47e503c66e935de81230b59b7afb5f41afa8d661cb"

c4 = "32510ba9aab2a8a4fd06414fb517b5605cc0aa0dc91a8908c2064ba8ad5ea06a029056f47a8ad3306ef5021eafe1ac01a81197847a5c68a1b78769a37bc8f4575432c198ccb4ef63590256e305cd3a9544ee4160ead45aef520489e7da7d835402bca670bda8eb775200b8dabbba246b130f040d8ec6447e2c767f3d30ed81ea2e4c1404e1315a1010e7229be6636aaa"

c5 = "3f561ba9adb4b6ebec54424ba317b564418fac0dd35f8c08d31a1fe9e24fe56808c213f17c81d9607cee021dafe1e001b21ade877a5e68bea88d61b93ac5ee0d562e8e9582f5ef375f0a4ae20ed86e935de81230b59b73fb4302cd95d770c65b40aaa065f2a5e33a5a0bb5dcaba43722130f042f8ec85b7c2070"

c6 = "32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd2061bbde24eb76a19d84aba34d8de287be84d07e7e9a30ee714979c7e1123a8bd9822a33ecaf512472e8e8f8db3f9635c1949e640c621854eba0d79eccf52ff111284b4cc61d11902aebc66f2b2e436434eacc0aba938220b084800c2ca4e693522643573b2c4ce35050b0cf774201f0fe52ac9f26d71b6cf61a711cc229f77ace7aa88a2f19983122b11be87a59c355d25f8e4"

c7 = "32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd90f1fa6ea5ba47b01c909ba7696cf606ef40c04afe1ac0aa8148dd066592ded9f8774b529c7ea125d298e8883f5e9305f4b44f915cb2bd05af51373fd9b4af511039fa2d96f83414aaaf261bda2e97b170fb5cce2a53e675c154c0d9681596934777e2275b381ce2e40582afe67650b13e72287ff2270abcf73bb028932836fbdecfecee0a3b894473c1bbeb6b4913a536ce4f9b13f1efff71ea313c8661dd9a4ce"

c8 = "315c4eeaa8b5f8bffd11155ea506b56041c6a00c8a08854dd21a4bbde54ce56801d943ba708b8a3574f40c00fff9e00fa1439fd0654327a3bfc860b92f89ee04132ecb9298f5fd2d5e4b45e40ecc3b9d59e9417df7c95bba410e9aa2ca24c5474da2f276baa3ac325918b2daada43d6712150441c2e04f6565517f317da9d3"

c9 = "271946f9bbb2aeadec111841a81abc300ecaa01bd8069d5cc91005e9fe4aad6e04d513e96d99de2569bc5e50eeeca709b50a8a987f4264edb6896fb537d0a716132ddc938fb0f836480e06ed0fcd6e9759f40462f9cf57f4564186a2c1778f1543efa270bda5e933421cbe88a4a52222190f471e9bd15f652b653b7071aec59a2705081ffe72651d08f822c9ed6d76e48b63ab15d0208573a7eef027"

c10 = "466d06ece998b7a2fb1d464fed2ced7641ddaa3cc31c9941cf110abbf409ed39598005b3399ccfafb61d0315fca0a314be138a9f32503bedac8067f03adbf3575c3b8edc9ba7f537530541ab0f9f3cd04ff50d66f1d559ba520e89a2cb2a83"

target = "32510ba9babebbbefd001547a810e67149caee11d945cd7fc81a05e9f85aac650e9052ba6a8cd8257bf14d13e6f0a803b54fde9e77472dbff89d71b57bddef121336cb85ccb8f3315f4b52e301d16e9f52f904"

# =========================

def is_letter(n):
    return (n >= ord('a') and n <= ord('z')) or (n >= ord('A') and n <= ord('Z'))

def int_array_to_human_string(a):
    """Prints out a string where the value at the index is a letter if possible, otherwise prints ."""
    def get_letter(n):
        if is_letter(n): return chr(n)
        return '.'
    return map(get_letter, a)

def message_string(m):
    return ''.join(map(lambda x: '.' if x == 0 else chr(x), m))

def print_messages(ms, heading):
    print
    print 'Messages ({0})'.format(heading)
    for i in range(0, len(ms)):
        print '    m{0:02d}: {1}'.format(i, message_string(ms[i]))

def recalc_messages():
    """Recalculate all messages after changes in the message 0."""
    xors_from_first = [xor_hex_strings(ciphertexts[0], ciphertexts[p]) for p in range(0, len(messages))]
    for i in range(0, len(messages)):
        new_msg = map(lambda x: x[0] ^ x[1] if x[0] <> 0 else 0, zip(messages[0], xors_from_first[i]))
        assert(len(new_msg) == len(messages[0]))
        assert(len(new_msg) == len(xors_from_first[i]))
        messages[i] = new_msg

def substitute_text(msg_no, position, substitute):
    """Manually hack at messages.

    Setting any one chr code in a message fills out the other messages,
    and can try looking at the other messages as each char is filled
    in.
    """

    ords = [ord(c) for c in substitute]
    # print ords

    xors_from_first = [xor_hex_strings(ciphertexts[0], ciphertexts[p]) for p in range(0, len(messages))]
    xors = xors_from_first[msg_no][position:position+len(substitute)]
    assert(len(ords) == len(xors))
    repl = map(lambda x: x[0] ^ x[1], zip(xors, ords))
    # print repl
    for i in range(0, len(repl)):
        messages[0][position + i] = repl[i]

    recalc_messages()
    print_messages(messages, 'substiting "{0}" starting position {1} in message {2}'.format(substitute, position, msg_no))


# =========================

ciphertexts = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, target]

# Truncate unneeded info.
ciphertexts = map(lambda x: x[0:len(target)], ciphertexts)

num_msgs = len(ciphertexts)
cols = len(target) / 2  # each ascii char takes 2 hex chars
messages = []
for i in range(0, num_msgs):
    r = [0] * cols
    messages.append(r)

print_messages(messages, 'initial state')

# For each crypto cN corresponding to message mN, xor with cI (I !=
# N).  Check all char positions p of all cI.  If they're all letters,
# it's _likely_ that position p in mN is a space, and the messages
# have the letter of the opposite case.
#
# Build array of all CT's xor'd with the current CT, where each entry
# is marked as "1" (True) for a character A-Z or a-z, else 0.  Mark
# the current CT as "1".  Then AND each column in each row separately
# (i.e., transpose the matrix, AND each row, and re-transpose) -
# columns with "1" mark likely locations for spaces.  eg.:
#
# c0: 1 1 1 1 1 1
# c1: 0 0 1 0 0 1
# c2: 1 0 1 1 0 0
# c3: 0 1 1 0 0 0
#
# c0 is the "current" CT being investigated.  c1-3 all have letters at
# position 3, but nowhere else do they all have a letter.  So, assume
# that position 3 in c0 is a space, and that c1-c3 have letters at
# that location.
#
indices = range(0, num_msgs)
for curr in indices:
    # print 'c{0}:'.format(curr + 1)
    xors = [ [None] * cols ] * num_msgs
    letters = [ [0] * cols ] * num_msgs
    letters[curr] = [1] * cols
    for second in [p for p in indices if p != curr]:
        xors[second] = xor_hex_strings(ciphertexts[curr], ciphertexts[second])
        letters[second] = map(lambda x: 1 if is_letter(x) else 0, xors[second])

    # Transpose to find letters
    # http://stackoverflow.com/questions/4937491/matrix-transpose-in-python
    test_letters_raw = [list(i) for i in zip(*letters)]
    test_letters = [reduce(lambda x, y: x and y, r_raw, True) for r_raw in test_letters_raw]
    # print test_letters

    # For each each place in test_letters that's 1, assume that the underlying
    # message for ciphertexts[curr] is a space, and for the other texts it's
    # the letter that was shown (opposite case).
    for c in range(0, cols):
        if test_letters[c] == 1:
            messages[curr][c] = ord(' ')
            for second in [p for p in indices if p != curr]:
                # print 'loading col {0} of {1}'.format(c, second)
                messages[second][c] = xors[second][c] ^ ord(' ')


print_messages(messages, 'after analyzing for spaces')


substitutions = (
    (1, 12, 'probably'),
    (4, 0, "You don't want to"),
    (3, 0, "The ciphertext produced by "),
    (9, 0, " The Concise OxfordDictionary"),
    (5, 0, "There are two types of cryptography "),
    (4, 0, "You don't want to buy a set of car keys "),
    (6, 0, "There are two types of cyptography: one that allows "),
    (10, 0, "The secret message is: When using a stream cipher, never use the key more than once")
)
for m, p, text in substitutions:
    substitute_text(m, p, text)
