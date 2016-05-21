import math
import gmpy2
import sys
from gmpy2 import mpz
from gmpy2 import mpfr

gmpy2.get_context().precision=200

def print_result(title, N, A, x):

    print "\n\n" + title

    p = A - x
    q = A + x

    msg = """
N: {0}
A: {1}
x: {2}
p: {3}
q: {4}
N - p * q: {5}""".format(N, A, x, p, q, N - p * q)
    print msg


# ========================================
# Factoring challenge 1:

N = mpz(179769313486231590772930519078902473361797697894230657273430081157732675805505620686985379449212982959585501387537164015710139858647833778606925583497541085196591615128057575940752635007475935288710823649949940771895617054361149474865046711015101563940680527540071584560878577663743040086340742855278549092581)
data = gmpy2.isqrt_rem(N)
A = data[0] + 1
x, r = gmpy2.isqrt_rem(A ** 2 - N)
assert(r == 0)

print_result("challenge 1", N, A, x)


# ========================================
# no 2:

N = mpz(648455842808071669662824265346772278726343720706976263060439070378797308618081116462714015276061417569195587321840254520655424906719892428844841839353281972988531310511738648965962582821502504990264452100885281673303711142296421027840289307657458645233683357077834689715838646088239640236866252211790085787877)

isqrtN, _ = gmpy2.isqrt_rem(N)
A = None
x = None
assert(isqrtN ** 2 < N)
isqrtN += 1
assert(isqrtN ** 2 >= N)
curr = isqrtN
while curr <= isqrtN + 2 ** 80:
    x, r = gmpy2.isqrt_rem(curr ** 2 - N)
    if r == 0:
        A = curr
        break
    curr += 1

if A is None:
    raise ValueError('A not found')

print_result("challenge 2", N, A, x)

