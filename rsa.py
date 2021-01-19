import random

def quicks(a, b, c):
    """
    quick power
    """
    ans = 1
    a = a % c
    while b != 0:
        if b&1:
            ans = (ans * a) % c
        b = b >> 1
        a = (a * a) % c
    return ans

def Miller_Rabin(n):
    """
    determine whether n is a prime
    """
    t = 0
    b = n - 1
    while b&1 == 0:
        t = t + 1
        b = b >> 1
    a = random.randint(2, n-1)
    x = quicks(a, b, n)
    for i in range(1, t+1):
        y = quicks(x, 2, n)
        if y == 1 and x != 1 and x != n-1:
            return False
        x = y
    if x != 1:
        return False
    else:
        return True

def generate_big_prime(n):
    """
    generate two big primes(has n digits) that are not equal
    """
    p, q = 0, 0
    flag = False
    while flag != True:
        p = random.randint(2**(n-1), 2**n)
        flag = Miller_Rabin(p)
    flag = False
    while flag != True or q == p:
        q = random.randint(2**(n-1), 2**n)    
        flag = Miller_Rabin(q)
    return (p, q)

def gcd(a, b):
    """
    calculate the gcd of a and b
    """
    while b != 0:
        a, b = b, a % b
    return a

def coprime(a, b):
    """
    check if a and b are coprime
    """
    return gcd(a, b) == 1

def choose(n):
    """
    calculate e satisfying 1 < e < n and gcd(n, e) = 1
    """
    e = 0
    flag = False
    while flag != True:
        e = random.randint(2, n)
        flag = coprime(e, n)
    return e

def ext_euclid(a, b):
    """
    extend euclid
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    if b == 0:
        return 1, 0, a
    else:
        while (r != 0):
            q = old_r // r
            old_r, r = r, old_r - q * r
            old_s, s = s, old_s - q * s
            old_t, t = t, old_t - q * t
    return old_s, old_t, old_r

def inv(a, p):
    """
    calculate inverse of a module p
    """
    _a, _, _ = ext_euclid(a, p)
    return ((_a % p) + p) % p

def generate_key(len):
    """
    generate e, n, d for rsa
    """
    p, q = generate_big_prime(len/2)
    n = p * q
    phi = (p-1)*(q-1)
    e = choose(phi)
    d = inv(e, phi)
    return (e, n, d)
    
def square(a, b, p):
    """
    square-multipy
    """
    y = 1
    while True:
        if(b == 0):
            return y
        while b > 0 and b % 2 == 0:
            a = (a*a) % p
            b = b / 2
        b = b - 1
        y = (a * y) % p

def count_set_bytes(n):
    """
    count how many bytes a integer take
    """
    count = 0
    while(n):
        n >>= 8
        count += 1
    return count   

def strtoint(s):
    """
    convert string to big integer
    """
    return int.from_bytes(bytes(s, "utf-8"), 'big')

def inttostr(n):
    """
    convert big integer to string
    """
    return n.to_bytes(count_set_bytes(n), 'big').decode()

def group(plain, n):
    """
    group plain into appropriate size
    """
    plain_list = []
    head, tail = 0, 1
    while tail < len(plain):
        m = strtoint(plain[head: tail])
        while m < n:
            tail = tail + 1
            if tail == len(plain):
                tail = tail + 1
                break
            m = strtoint(plain[head: tail])    
        m = strtoint(plain[head: tail - 1])
        plain_list.append(m)
        head = tail - 1
    return plain_list

def degroup(array):
    """
    convert integer array to string
    """
    s = ""
    for n in array:
        s = s + inttostr(n)
    return s

print("RSA encrypt and decript")
key_len = 32
e, n, d = generate_key(key_len)

print("plain:")
plain = input()
plain_list = group(plain, n)

cipher_list = []
for m in plain_list:
    c = square(m, e, n)
    cipher_list.append(c)

print("cipher:")
for c in cipher_list:
    if c != cipher_list[-1]:
        print(c, end=" ")
    else:
        print(c)

flag = False
ch = 'y'
while flag != True:
    print("decryt now?(y/n)")
    ch = input()
    flag = (ch == 'y' or ch == 'n')

if ch == 'y':
    decipher_list = []    
    for c in cipher_list:
        de = square(c, d, n)
        decipher_list.append(de)
    decipher = degroup(decipher_list)
    print("decipher:")
    print(decipher)