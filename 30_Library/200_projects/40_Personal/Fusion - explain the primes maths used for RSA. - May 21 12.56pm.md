---
created: 2026-05-21T11:56:05+00:00
modified: 2026-05-22T08:31:23+00:00
---
# RSA Prime Mathematics and Manual Key Pair Generation on the CLI

## The Math Behind RSA

RSA's security rests on a single hard problem: **given n = p × q, factoring n back into its two large prime factors p and q is computationally infeasible** when p and q are hundreds of digits long.

### Step-by-Step Mathematics

| Symbol                | Meaning                                                                         |
| --------------------- | ------------------------------------------------------------------------------- |
| **p, q**              | Two large distinct primes (secret)                                              |
| **n = p × q**         | Modulus (public, appears in both keys)                                          |
| **φ(n) = (p−1)(q−1)** | Euler's totient — counts integers coprime to n (never published)                |
| **e**                 | Public exponent — chosen coprime to φ(n), commonly **65537** (0x10001)          |
| **d**                 | Private exponent — modular inverse of e mod φ(n), i.e. **e·d ≡ 1 (mod φ(n))**   |
| **Public key**        | (n, e)                                                                          |
| **Private key**       | (n, d) (often stored with CRT coefficients: d mod (p−1), d mod (q−1) for speed) |

### Worked Example (small numbers for illustration)

```
p = 61
q = 53
n = 61 × 53 = 3233
φ(n) = 60 × 52 = 3120
e = 65537   (gcd(65537, 3120) = 1 ✓)
d = 2753    (because 2753 × 65537 ≡ 1 mod 3120)
```

**Encryption**:  c = m^e mod n  
**Decryption**:  m = c^d mod n

This works because Euler's theorem gives m^φ(n) ≡ 1 (mod n), so m^(e·d) ≡ m (mod n).

---

## Manual Key Pair Generation Using CLI Primitives

### Method 1: Direct Generation (Recommended for Real Use)

```bash
# Generate a 2048-bit RSA private key
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out private.pem

# Extract the public key
openssl pkey -in private.pem -pubout -out public.pem

# Inspect the keys
openssl pkey -in private.pem -text -noout
openssl pkey -in public.pem -text -noout
```

### Method 2: Fully Manual Construction (Educational)

This mimics what OpenSSL does internally, using only CLI tools.

#### Step 1 — Generate two large primes

```bash
# Generate random 1024-bit primes (OpenSSL's prime uses Miller–Rabin)
openssl prime -generate -bits 1024 -out p.txt
openssl prime -generate -bits 1024 -out q.txt

cat p.txt
cat q.txt
```

> **⚠️ Warning**: For production, always use established libraries. Manual prime generation risks weak entropy and insufficient primality testing.

#### Step 2 — Compute n and φ(n)

```bash
P=$(cat p.txt)
Q=$(cat q.txt)
N=$(echo "$P * $Q" | bc)
PHI=$(echo "($P - 1) * ($Q - 1)" | bc)

echo "n = $N"
echo "φ(n) = $PHI"
```

#### Step 3 — Choose e and verify coprimality

```bash
E=65537

# Verify gcd(e, phi) = 1 using Python
python3 -c "
import math
p, q = int(open('p.txt').read()), int(open('q.txt').read())
phi = (p-1)*(q-1)
e = 65537
print(f'gcd({e}, {phi}) = {math.gcd(e, phi)}')
"
```

#### Step 4 — Compute d (modular inverse) using the Extended Euclidean Algorithm

```bash
# Using Python
python3 <<'PYEOF'
import sys

p = int(open('p.txt').read())
q = int(open('q.txt').read())
phi = (p-1)*(q-1)
e = 65537

# Extended Euclidean Algorithm
def modinv(a, m):
    t0, t1 = 0, 1
    r0, r1 = m, a
    while r1 != 0:
        q = r0 // r1
        t0, t1 = t1, t0 - q * t1
        r0, r1 = r1, r0 - q * r1
    if r0 != 1:
        raise ValueError("inverse does not exist")
    return t0 % m

d = modinv(e, phi)
print(f"d = {d}")
print(f"Verification: (d * e) mod phi = {(d * e) % phi}")
PYEOF
```

#### Step 5 — Assemble PEM-encoded keys

OpenSSL can convert the raw components into a PEM private key:

```bash
# Create a DER-formatted RSA private key from raw components
python3 <<'PYEOF' > private_raw.der
import struct

p = int(open('p.txt').read())
q = int(open('q.txt').read())
n = p * q
e = 65537
phi = (p-1)*(q-1)

# Extended Euclidean to get d
def modinv(a, m):
    t0, t1 = 0, 1
    r0, r1 = m, a
    while r1 != 0:
        q = r0 // r1
        t0, t1 = t1, t0 - q * t1
        r0, r1 = r1, r0 - q * r1
    return t0 % m

d = modinv(e, phi)

# Also compute CRT coefficients for efficiency
dp = d % (p-1)
dq = d % (q-1)
qinv = pow(q, -1, p)  # q^(-1) mod p

# Minimal PKCS#1 RSAPrivateKey (simplified — full format is complex)
# For real use, feed (n,e,d) into OpenSSL rather than hand-crafting DER
print(f"n={n}")
print(f"e={e}")
print(f"d={d}")
print(f"dp={dp}")
print(f"dq={dq}")
print(f"qinv={qinv}")
PYEOF

# Extract values
N=$(python3 -c "p=int(open('p.txt').read()); q=int(open('q.txt').read()); print(p*q)")
E=65537
D=$(python3 -c "
import sys
p=int(open('p.txt').read())
q=int(open('q.txt').read())
phi=(p-1)*(q-1)
e=65537
def modinv(a,m):
    t0,t1=0,1; r0,r1=m,a
    while r1!=0:
        q=r0//r1
        t0,t1=t1,t0-q*t1
        r0,r1=r1,r0-q*r1
    return t0%m
print(modinv(e,phi))
")

# Create PKCS#8 private key using OpenSSL's `rsa` command (if available)
# Or use the cryptography Python library to serialize:
python3 <<'PYEOF' - "$N" "$E" "$D"
import sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

n = int(sys.argv[1])
e = int(sys.argv[2])
d = int(sys.argv[3])

# Reconstruct key parameters
public_numbers = rsa.RSAPublicNumbers(e, n)
private_numbers = rsa.private.RSAPrivateNumbers(
    public_numbers=public_numbers,
    d=d,
    p=int(open('p.txt').read()),
    q=int(open('q.txt').read()),
    dmp1=d % (int(open('p.txt').read())-1),
    dmq1=d % (int(open('q.txt').read())-1),
    iqmp=pow(int(open('q.txt').read()), -1, int(open('p.txt').read()))
)

private_key = private_numbers.private_key(default_backend())

# Save PEM
with open('private_manual.pem', 'wb') as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Extract public key
public_key = private_key.public_key()
with open('public_manual.pem', 'wb') as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

print("Keys written: private_manual.pem, public_manual.pem")
PYEOF
```

> **Note**: Hand-crafting the raw DER encoding is complex and error-prone. The Python `cryptography` library is the practical way to go from raw (p, q, d, n) to PEM files on the CLI.

#### Step 6 — Verify the key pair

```bash
# Hash both keys — they should match when the public key is derived from the private
openssl pkey -in private_manual.pem -pubout | openssl md5
openssl pkey -in public_manual.pem -pubout | openssl md5

# Test encryption/decryption
echo "hello world" | openssl pkeyutl -encrypt -pubin -inkey public_manual.pem -out encrypted.bin
openssl pkeyutl -decrypt -inkey private_manual.pem -in encrypted.bin
```

### Method 3: Using `ssh-keygen`

```bash
ssh-keygen -t rsa -b 2048 -f id_rsa_manual -N ""
cat id_rsa_manual.pub
ssh-keygen -lf id_rsa_manual
```

### Method 4: Using GPG

```bash
gpg --full-generate-key
gpg --export -a "your-email" > public_key.asc
gpg --export-secret-keys -a "your-email" > private_key.asc
```

---

## Verification of the Math (Small-Number Example)

```bash
# Test with p=61, q=53
python3 <<'PY'
p, q, e = 61, 53, 65537
phi = (p-1)*(q-1)
n = p*q

def egcd(a, b):
    if b == 0:
        return (1, 0, a)
    x1, y1, g = egcd(b, a % b)
    return (y1, x1 - (a // b) * y1, g)

x, y, g = egcd(e, phi)
d = x % phi
print(f"d = {d}")
print(f"Verification: (d * e) mod phi = {(d * e) % phi}")
PY
```

---

## Important Security Notes

1. **Never use manual prime generation for production.** OpenSSL's `prime` command uses proper probabilistic primality testing (Miller–Rabin), but hand-rolled scripts may lack sufficient rounds or entropy.
2. **Key size matters**: 2048-bit minimum; 4096-bit for long-term security.
3. **CRT optimization**: Real RSA implementations store d mod (p−1) and d mod (q−1) alongside d to speed up decryption. This is automatically handled by libraries.
4. **Padding**: Raw RSA (textbook RSA) is insecure. In practice, **OAEP padding** is applied for encryption and **PKCS#1 v1.5** or **PSS** for signatures. The `openssl pkeyutl` commands above use the default padding scheme.
5. **Protect private keys**: Use `chmod 600` and consider encryption at rest.
6. **Consider ECC** for better performance at equivalent security levels.