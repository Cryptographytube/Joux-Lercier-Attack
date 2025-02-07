import random
from sympy import gcd, mod_inverse
from sympy.polys.domains import ZZ
from sympy.polys import ring
from sympy.ntheory.factor_ import factorint

def finite_field(p):
    return lambda x: x % p

def polynomial_selection(p, n):
    R, x = ring('x', ZZ)
    return x ** n + 1, x + random.randint(1, p - 1)

def collect_relations(f, g, p):
    relations = []
    for a in range(1, p):
        value = (f(a) * g(a)) % p
        factors = factorint(value)
        if factors:
            relations.append((a, factors))
    return relations

def lattice_reduction(relations, p):
    return [(1 if gcd(base, p) != 1 else mod_inverse(base, p) ** exp) % p 
            for _, factors in relations for base, exp in factors.items()]

def joux_lercier_attack(p, n):
    print(f"Using finite field GF({p})...\n")
    f, g = polynomial_selection(p, n)
    print(f"Selected polynomials:\n f(x) = {f}\n g(x) = {g}\n")
    print("Collecting relations...\n")
    relations = collect_relations(f, g, p)
    print(f"Collected {len(relations)} relations.\n")
    print("Reducing lattice to extract keys...\n")
    reduced_keys = lattice_reduction(relations, p)
    print(f"Reduced keys found: {len(reduced_keys)} keys.\n")
    return reduced_keys

print("\n=== CRYPTOGRAPHYTUBE: Joux-Lercier Attack ===\n")
prime = int(input("Enter Prime Number: "))
degree = int(input("Enter Polynomial Degree: "))

keys = joux_lercier_attack(prime, degree)

print("\nFinal Keys Extracted:")
for idx, key in enumerate(keys, start=1):
    print(f"Key {idx}: {key}")
