# Week 2 assignment

import math

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
    log10t = 128 * math.log(2, 10) - (math.log(5, 10) + 18 * math.log(10, 10))
    print log10t
    t = 10 ** log10t
    print t # seconds
    seconds_per_year = 60 * 60 * 24 * 365
    print 'will take {0} years'.format(t / seconds_per_year)

    log10years = log10t - math.log(seconds_per_year, 10)
    print 'double check:'
    print 'will take {0} years'.format(10 ** log10years)


def main():
    question_1()
    question_2()

if __name__ == '__main__':
    main()
