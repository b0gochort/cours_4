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

# Пример значений
s = 10
r = 3
e = 4
p = 23

w = find_w(s, r, e, p)
print(f"Значение w: {w}")
