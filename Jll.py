import random
from sympy import gcd, mod_inverse, isprime
from sympy.ntheory import factorint
from sympy.polys.domains import ZZ
from sympy.polys import ring

def polynomial_selection(p, degree):
    R, x = ring('x', ZZ)
    f = x**degree + 1
    g = x + random.randint(2, p - 2)
    return f, g

def evaluate_polynomials(f, g, x_val, p):
    fx = f.eval(x_val) % p
    gx = g.eval(x_val) % p
    return (fx * gx) % p

def collect_smooth_relations(f, g, p):
    relations = []
    for a in range(2, p):
        val = evaluate_polynomials(f, g, a, p)
        if val == 0:
            continue
        factors = factorint(val)
        if all(prime < 1000 for prime in factors):  # smooth check
            relations.append((a, factors))
        if len(relations) >= 20:
            break
    return relations

def reduce_lattice(relations, p):
    keys = []
    for xval, factor_dict in relations:
        key = 1
        for base, exp in factor_dict.items():
            if gcd(base, p) == 1:
                try:
                    inv = mod_inverse(base, p)
                    key = (key * pow(inv, exp, p)) % p
                except:
                    continue
        keys.append(key)
    return keys

def joux_lercier_attack(p, degree):
    if not isprime(p):
        print("Invalid Prime. Aborting.")
        return []
    print(f"\n[CRYPTOGRAPHYTUBE] Finite Field: GF({p})\n")
    f, g = polynomial_selection(p, degree)
    print(f"Polynomials Chosen:\n f(x) = {f}\n g(x) = {g}\n")
    print("Collecting smooth relations...")
    relations = collect_smooth_relations(f, g, p)
    print(f"Total Relations Collected: {len(relations)}\n")
    if not relations:
        print("No useful relations found. Try with different prime or degree.\n")
        return []
    print("Performing lattice-like reduction...\n")
    reduced_keys = reduce_lattice(relations, p)
    return reduced_keys

if __name__ == "__main__":
    print("=== CRYPTOGRAPHYTUBE: Joux-Lercier Realistic Simulation ===")
    prime = int(input("Enter a large prime number (e.g., 10007): "))
    degree = int(input("Enter polynomial degree (e.g., 3 to 5): "))
    keys = joux_lercier_attack(prime, degree)
    if keys:
        print("\nFinal Extracted Keys:")
        for i, k in enumerate(keys, 1):
            print(f"Key {i}: {k}")
    else:
        print("No keys extracted.")
