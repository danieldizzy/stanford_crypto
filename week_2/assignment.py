# Week 2 assignment

import math
from lib.helpers import *

def question_1():
    """
Q:
Consider the following five events:
Correctly guessing a random 128-bit AES key on the first try. (1/(2^128))
Winning a lottery with 1 million contestants (the probability is 1/10^6 ).
Winning a lottery with 1 million contestants 5 times in a row (the probability is (1/10^6)^5 ).
Winning a lottery with 1 million contestants 6 times in a row.
Winning a lottery with 1 million contestants 7 times in a row.
What is the order of these events from most likely to least likely?

most likely to least = smallest denominator to largest
take log of each denom.
log(x^n) = nlogx

lot1 = 6 * math.log(10, 10) = 6
lot5 = 30
lot6 = 36
lot7 = 42
"""
    print '\nQ1:'
    aes = 128 * math.log(2, 10)
    print aes # = 38.53
    # ans: lottery, then 5, 6, AES, 7

def question_2():
    """
Suppose that using commodity hardware it is possible to build a computer
for about $200 that can brute force about 1 billion AES keys per second.
Suppose an organization wants to run an exhaustive search for a single
128-bit AES key and was willing to spend 4 trillion dollars to buy these
machines (this is more than the annual US federal budget). How long would
it take the organization to brute force this single 128-bit AES key with
these machines? Ignore additional costs such as power and maintenance.



total_spend = 10^12
cost_per_c = 2 * 10^2
total_comps = total_spend / cost_per_c
  = 10^10 / 2
  = 5 * 10^9

search_per_c_per_second = 10^9
search_per_second = total_comps * search_per_c_per_second
  = 5 * 10^9 * 10^9
  = 5 * 10^18 search/s

single AES key = 2^128 possibilities
will take
t = 2^128 / 5 * 10^18 seconds

log(t) = log(aes/search_per_second)
 = log(aes) - log(search_per_second)
 = 128 * math.log(2, 10) - log(5 * 10^18)
log(t) = 128 * math.log(2, 10) - (log(5) + 18 * math.log(10, 10))

total_years = t / seconds_per_year
log(total_years) = log(t) - log(seconds_per_year)

"""
    print '\nQ2:'
    log10t = 128 * math.log(2, 10) - (math.log(5, 10) + 18 * math.log(10, 10))
    # print log10t
    t = 10 ** log10t
    # print t # seconds
    seconds_per_year = 60 * 60 * 24 * 365
    print 'will take {0} years'.format(t / seconds_per_year)

    log10years = log10t - math.log(seconds_per_year, 10)
    print 'double check:'
    print 'will take {0} years'.format(10 ** log10years)

    # check 2:
    length = (2 ** 128) / \
             (10 ** 9) / \
             (10 ** 12 / 200) / \
             (60 * 60 * 24 * 365)
    print 'will take {0} years'.format(length)


def question_4():
    print '\nQ4:'
    def print_xor(zero_64, one_32_zero_32):
        x = xor_hex_strings(zero_64, one_32_zero_32)
        msg = 'xor {0}, {1} = {2}'.format(zero_64, one_32_zero_32, x)
        print msg

    pairs = (
        ("e86d2de2e1387ae9", "1792d21db645c008"),
        ("5f67abaf5210722b", "bbe033c00bc9330e"),
        ("7c2822ebfdc48bfb", "325032a9c5e2364b"),
        ("7b50baab07640c3d", "ac343a22cea46d60")
    )

    for (a, b) in pairs:
        print_xor(a, b)

def question_8():
    print '\nQ8:'
    def print_stats(pt):
        bytes = len(pt)
        bits = len(pt) * 8
        blocksize = 128
        blocks, remainder = divmod(bits, blocksize)
        print 'msg: {0}'.format(pt)
        msg = '  {0} bytes = {1} bits\n  {2} blocks, {3} bits remaining'
        print msg.format(bytes, bits, blocks, remainder)
        print '    check: {0}'.format(blocks * blocksize + remainder)
        blocks_after_padding = blocks
        if remainder != 0: blocks_after_padding += 1
        iv_length = blocksize
        total_msg_size = iv_length + blocks_after_padding * blocksize
        payload_bytes = total_msg_size / 8
        msg = '  {0} blocks after padding\n  {1} iv + bits-in-blocks (bits)\n  {2} size (bytes)'
        print msg.format(blocks_after_padding, total_msg_size, payload_bytes)
        if payload_bytes == 128:
            print '  ****** possible answer ******'

    msgs = (
        'If qualified opinions incline to believe in the exponential conjecture, then I think we cannot afford not to make use of it.',
        'In this letter I make some remarks on a general principle relevant to enciphering in general and my machine.',
        'The most direct computation would be for the enemy to try all 2^r possible keys, one by one.',
        'The significance of this general conjecture, assuming its truth, is easy to see. It means that it may be feasible to design ciphers that are effectively unbreakable.'
    )
    for m in msgs:
        print_stats(m)

def main():
    print "\nWeek 2"
    question_1()
    question_2()
    question_4()
    question_8()

if __name__ == '__main__':
    main()
