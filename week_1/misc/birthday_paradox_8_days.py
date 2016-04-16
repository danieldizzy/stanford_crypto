# ref https://www.coursera.org/learn/crypto/discussions/Mmr3fACqEeaftQ4Vb9ltCw

import itertools

def print_prob_of_dup_in_selected(source):
    # print source
    selection_size = len(source[0])
    def has_dups(list): return len(list) != len(set(list))
    have_dups = [p for p in source if has_dups(p)]
    prob = (1.0 * len(have_dups)) / len(source)

    print
    print "Selection size {0}".format(selection_size)
    print "   groups with at least one dup: {0}".format(len(have_dups))
    print "   possible groups:              {0}".format(len(source))
    print "   Prob of duplicate:            {0}".format(prob)


data = ('000','001','010','011','100','101','110','111')

for i in range(2, 6):
	print_prob_of_dup_in_selected([p for p in itertools.product(data, repeat=i)])


# Output:

# Selection size 2
#    groups with at least one dup: 8
#    possible groups:              64
#    Prob of duplicate:            0.125

# Selection size 3
#    groups with at least one dup: 176
#    possible groups:              512
#    Prob of duplicate:            0.34375

# Selection size 4
#    groups with at least one dup: 2416
#    possible groups:              4096
#    Prob of duplicate:            0.58984375
