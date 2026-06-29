---
aliases: []
created: 2025-08-17 12:31:05+00:00
last_reviewed: ''
modified: 2026-06-08 11:49:24+00:00
project_category: development
project_name: Cryptography
project_status: archived
see_also: []
status: ''
superseded_by: ''
supersedes: ''
tags: []
title: mini rsa
type: ''
updated: null
permalink: llmeon/30-library/200-projects/mini-rsa
---

Of course. Let's build a complete, tiny RSA system using numbers small enough that you can see the results for yourself.

The modulus creates a small "clock" for our numbers to cycle around. The totient is the secret number of steps in that cycle, which is what allows us to reverse the encryption.

A Tiny RSA System from Scratch ⚙️

1. Choose Two Primes (p and q)
   We'll use the smallest ones that make for a good example.

- p = 7
- q = 11

1. Calculate the Modulus (n)
   This sets the size of our "clock." All our maths will wrap around this number.

- n = p _q = 7_ 11 = 77

1. Calculate the Totient (λ(n))
   This is the "magic number" that tells us the length of the exponentiation cycle.

- λ(n) = lcm(p - 1, q - 1) = lcm(6, 10) = 30

1. Choose the Public Exponent (e)
   We need a number that is coprime to our totient (30). Let's pick:

- e = 13

1. Calculate the Private Exponent (d)
   We need the unique number d where (13 \* d) % 30 = 1. By testing numbers, we find:

- d = 7 (since 13 \* 7 = 91, and 91 % 30 = 1)
  Our Keys:
- Public Key: (n = 77, e = 13)
- Private Key: (n = 77, d = 7)
  Encryption & Decryption in Action
  Let's pick a number to be our secret message, M = 5.
  Encryption (using the Public Key)
  Ciphertext = M^e % n = 5^13 % 77
  5^13 is a huge number (30,517,578,125), but when we find the remainder after dividing by 77, we get:
- Ciphertext = 26
  Decryption (using the Private Key)
  Message = Ciphertext^d % n = 26^7 % 77
  26^7 is another huge number (8,031,810,176), but again we find the remainder after dividing by 77:
- Message = 5
  It worked perfectly! We got our original message back.
  Visualising the "Magic Cycle" 🔄
  So why did this work? It's because of the totient (λ(n) = 30).
  The rule is that any number raised to the power of the totient will equal 1 (in our mod 77 system). Let's check:
  5^30 % 77 = 1 (You can verify this with a calculator).
  Now, look at what happens when we combine the encryption and decryption steps. We are effectively calculating:
  (M^e)^d = M^(e_d) = 5^(13_ 7) = 5^91
  Why does 5^91 % 77 give us back 5? Because the exponent 91 is related to our magic cycle length of 30.
- 91 = (3 _30) + 1
  This means we are going around the cycle 3 full times and then taking 1 extra step. Let's break it down:
  5^91 % 77
  = 5^(3_30 + 1) % 77
  = (5^(3_30)_ 5^1) % 77
  = ((5^30)^3 _5) % 77
  Since we know 5^30 % 77 = 1, we can substitute that in:
  = ((1)^3_ 5) % 77
  = (1 _5) % 77
  = 5 % 77
  This leaves us with our original number, 5. The private key d was specifically calculated to ensure that e_ d would be exactly one step more than a multiple of the totient's cycle length, guaranteeing the process always works.