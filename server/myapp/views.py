from django.shortcuts import render
from django.http import HttpResponse
from .models import KeyPair
# Create your views here.


import random
import hashlib
import sympy
from sympy import *


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


def get_keys():
    p = 0
    q = 0
    g = 1
    while not isprime(q):
        q = generate_random_number(512)
    print('q =', q)
    m = generate_random_number(512)
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



    w = random.randint(1, q-1)
    y = pow(g, q-w, p)
    return p, q, g,w,y


# # Пример использования
# p, q, g,w,y = get_keys()
# print("p:", p)
# print("q:", q)
# print("g res pow:", pow(g,q,p),"g==", g)
#
#
# t = generate_random_number(3)
#
# r = random.randint(1,q-1)
# x = pow (g,r,p)
#
# e = random.randint(0,pow(2,t)-1)
#
# s = pow((r + w*e),1,p-1)
#
# res = pow(pow(g,s,p)*pow(y,e,p),1,p)
#
# if res == x:
#     print("success")
#     exit(0)
# print("pepec")



def index(request):
    # Генерация ключевой пары
    p, q, g, w, y = get_keys()

    # Создание новой записи KeyPair в базе данных
    key_pair = KeyPair.objects.create(p=p, q=q, g=g, y=y)
    key_pair.save()

    # Возвращение на экране секретного ключа и его ID
    response_text = f"Секретный ключ: {w}, ID пользователя: {key_pair.id}"
    return HttpResponse(response_text)

def authentication_form(request):
    return render(request, 'auth/auth.html')
def index_html(request):
    return render(request,'auth/index.html')


from django.shortcuts import render
from .models import KeyPair
from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from .models import KeyPair



def authenticate_user(request):
    if request.method == 'POST':
        identifier = int(request.POST.get('identifier'))
        secret_key = int(request.POST.get('secret_key'))

        try:
            key_pair = KeyPair.objects.get(id=identifier)
            key_info = f"p: {key_pair.p}, q: {key_pair.q}, g: {key_pair.g}, y: {key_pair.y}"
            t = generate_random_number(3)

            r = random.randint(1, int(key_pair.q) - 1)
            x = pow(int(key_pair.g), r, int(key_pair.p))

            e = random.randint(0, pow(2, t) - 1)

            s = (r + secret_key * e) % (int(key_pair.p) - 1)

            res = (pow(int(key_pair.g), s, int(key_pair.p)) * pow(int(key_pair.y), e, int(key_pair.p))) % int(key_pair.p)

            if res == x:
                return redirect('key_info', identifier=key_pair.id)
            else:
                return render(request, 'auth/auth.html', {'key_info': "bad key"})
        except KeyPair.DoesNotExist:
            return render(request, 'auth/auth.html', {'key_info': "bad key"})

    return HttpResponse("Method not allowed")

def key_info(request, identifier):
    try:
        key_pair = KeyPair.objects.get(id=identifier)
        return render(request, 'auth/key_info.html', {'key_pair': key_pair})
    except KeyPair.DoesNotExist:
        return HttpResponse("Key information not found")