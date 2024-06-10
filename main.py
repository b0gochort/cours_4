import random
from random import randint
import hashlib
import sympy
from sympy import *
import math
from libnum.factorize import factorize
import libnum
from sympy.ntheory import factorint
from sympy.ntheory import discrete_log

import libnum
from libnum.factorize import factorize

def baby_steps_giant_steps(a,b,p,N = None):
    if not N: N = 1 + int(math.sqrt(p))

    #initialize baby_steps table
    baby_steps = {}
    baby_step = 1
    for r in range(N+1):
        baby_steps[baby_step] = r
        baby_step = baby_step * a % p

    #now take the giant steps
    giant_stride = pow(a,(p-2)*N,p)
    giant_step = b
    for q in range(N+1):
        if giant_step in baby_steps:
            return q*N + baby_steps[giant_step]
        else:
            giant_step = giant_step * giant_stride % p
    return "No Match"

def primfacs(n):
   i = 2
   primfac = []
   while i * i <= n:
       while n % i == 0:
           primfac.append(i)
           n = n / i
       i = i + 1
   if n > 1:
       primfac.append(n)
   return primfac
def isMillerRabinPassed(num, number_test):
    maxDivisionByTwo = 0
    m = num - 1
    while m % 2 == 0:
        m >>= 1
        maxDivisionByTwo += 1
    assert(2**maxDivisionByTwo * m == num -1)
    def trialComposite(a):
        if pow(a, m, num) == 1:
            return False
        for i in range(maxDivisionByTwo):
            if pow(a, 2**i * m, num) == num-1:
                return False
        return True
    numberOfRabinTrials = number_test
    for i in range(numberOfRabinTrials):
        a = random.randrange(2, num)
        if trialComposite(a):
            return False
    return True

def generate_random_number(num_bit):
    num_bit = int(num_bit)
    iter = 0
    checker = True
    while checker:
        num = random.getrandbits(num_bit-1) | (1 << (num_bit-1)) | 1
        iter+=1
        if num >= 2000:
            prime_list = sympy.primerange(3, 2000)
        else:
            prime_list = sympy.primerange(3, num)
        if all(num % prime != 0 for prime in prime_list):
            if isMillerRabinPassed(num, 5):
                checker = False
    return num


def find_primitive_root(n):
    # Поиск первообразного корня по модулю n
    for a in range(2, n):
        if is_primitive_root(a, n):
            return a
    return None

def is_primitive_root(a, n):
    phi = sympy.totient(n)
    phi = int(str(phi))
    factors = sympy.factorint(phi)
    for factor in factors:
        if pow(a, phi // factor, n) == 1:
            return False
    return True


def is_primitive_roott(g, p, q):
    exp = (p - 1) // q
    result = pow(g, exp, p)
    return result == 1
def get_random_positive_number(bits):
    return random.randint(2**(bits), 2**(bits + 1))
def get_p_based_on_q(q, bits_magnitude):
    p = 0
    while True:
        r = get_random_positive_number(bits_magnitude - q.bit_length())
        p = (q * r) + 1
        if p % 2 == 0 or not sympy.isprime(p):
            continue
        return p


def gcd(a, b):
    """ Returns gcd(a, b) """
    """ Complexity: O( log^3(N) ) """
    if a > b:
        return gcd(b, a)

    if a == 0:
        return b

    return gcd(b % a, a)

def moduloPower(a, i, N):
    """ Returns a**i (mod N) """
    """ Complexity: O( log(B) * log^2(N) ) """
    val = 1
    while i > 0:
        if i % 2:
            val *= a
            val %= N
        a *= a
        a %= N
        i //= 2  # Use integer division for Python 3
    return val

def PollardRhoAttack(a, N, B):
    """ Implementation of Pollard's Rho - 1 Attack """
    """ Worst Case Complexity: O( ( B * log(B) + log(N) ) * log^2(N) ) """

    # computing a**(B!) (mod N)
    for i in range(2, B + 1):  # Use range instead of xrange for Python 3
        # computing a**(i!) (mod N)
        a = moduloPower(a, i, N)

        # computing gcd(a - 1, N)
        d = gcd(a - 1, N)

        if 1 < d < N:
            print('Prime Factorization of', N)
            print('(', d, ',', N // d, ')')
            return N,True

    # d = 1 or d = N
    return N,False

def prime_factors(n):
    factors = []
    divisor = 2

    while n > 1:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 1

def canonical_decomposition(n):
    if n < 2:
        return [n]

    factors = prime_factors(n)
    unique_factors = set(factors)
    decomposition = []

    for factor in unique_factors:
        count = factors.count(factor)
        if count > 1:
            decomposition.append(factor)
        else:
            decomposition.append(factor)

    return decomposition


def generate_random_prime(bits):
    return sympy.randprime(2**(bits-1), 2**bits)

def find_primitive_root(p,q):
    # Перебираем все числа от 2 до p-1
    for g in range(2, p):
        # Проверяем, является ли g примитивным корнем по модулю p
        if pow(g, q, p) == 1:
            return g
    return None
def extended_gcd(a, b):
    """Расширенный алгоритм Евклида для нахождения наибольшего общего делителя и коэффициентов."""
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

def mod_inverse(e, mod):
    """Нахождение мультипликативного обратного элемента."""
    gcd, x, y = extended_gcd(e, mod)
    if gcd != 1:
        raise ValueError(f'Обратного элемента не существует для {e} по модулю {mod}')
    return x % mod

def find_w(s, r, e, p):
    """Нахождение w из уравнения s = r + we (mod (p-1))."""
    mod = p - 1
    e_inv = mod_inverse(e, mod)
    w = (s - r) * e_inv % mod
    return w

def get_keys():
    p = 0
    q = 0
    g = 1
    while not isprime(q):
        q = generate_random_number(26)
    print('q =', q)
    m = generate_random_number(26)
    while not isprime(p):
        m += 1
        p = q * m + 1
    print('p =', p)
    while True:
        e = random.randint(1, p - 1)
        # print('e =', e)
        g = pow(e, m, p)
        if pow(g, q, p) == 1:
            print('a =', g)
            break



    w = random.randint(1, p)
    print(w)
    y = pow(g, -1*w, p)
    return p, q, g,w,y


# Пример использования
p, q, g,w,y = get_keys()
print("p:", p)
print("q:", q)
print("g res pow:", pow(g,q,p),"g==", g)

q_solved = factorint(p-1)
print(q_solved)


t = generate_random_number(3)

r = random.randint(1,q-1)
print("r",r)
x = pow (g,r,p)

# r_pp,t = PollardRhoAttack(g,x,p)
# print("r",r_pp)
r_solved = baby_steps_giant_steps(g,x,p)
print(r_solved)

def find_secret_key(s, r, e, p):
    try:
        inv_e = pow(e, -1, p)
    except ValueError:
        print(f"Не удалось найти обратное для e={e} по модулю p={p}")
        return None
    return (s - r) * inv_e % p
e = random.randint(((pow(2,t)-1)//2),pow(2,t)-1)

s = pow((r + w*e),1,p-1)

res = pow(pow(g,s,p)*pow(y,e,p),1,p)

secret_key = find_secret_key(s, r_solved, e, p-1)

print(secret_key ,'!!')

if res == x:
    print("success")
    exit(0)
print("pepec")


