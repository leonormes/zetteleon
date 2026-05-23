---
title: "New chat"
source: "https://gemini.google.com/app/ff068b421626f686"
captured: "2026-05-23T12:46:35+01:00 2026-05-23T12:46:35+01:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
**You**

Find a youtube video that explains how the maths behind rsa works. I want to understand the different maths components like Euler's totient how the Modulus is used and so on. Find a popular video that is clearly explained without a need to be formally trained in maths!

---

**Gemini**

A fantastic, highly popular video that explains the maths behind RSA cryptography in an accessible way is **"Prime Numbers & RSA Encryption Algorithm"** by Computerphile.

The video does an excellent job of stripping away intimidating mathematical jargon and explaining the system using a simple, real-world example with small numbers instead of the massive 300-digit primes used in modern security.

### Prime Numbers & RSA Encryption Algorithm - Computerphile

- **Video URL:**
	[http://www.youtube.com/watch?v=JD72Ry60eP4](http://www.youtube.com/watch?v=JD72Ry60eP4)

Here is a breakdown of how the video explains the core mathematical components of RSA, using its intuitive "clock" analogy:

### 1\. The Core Trapdoor: Prime Factorisation

The entire security of RSA relies on a mathematical asymmetry: it is incredibly easy for a computer to multiply two numbers together, but exceptionally difficult to do the reverse (factorising a massive number back into its original primes). If a computer is given a 600-digit number, it could take longer than the age of the universe to figure out which two prime numbers were multiplied to create it.

### 2\. The Modulus (n) as an Analogue Clock

To make encryption work, RSA relies heavily on **modular arithmetic**, which the video explains using the familiar concept of an analogue clock face. On a standard clock, numbers wrap around after 12.

In RSA, the **Modulus ($n$)** is the size of your primary clock.

- The video uses the prime numbers **7** and **13** as an example.
- Multiplying them together gives a Modulus of **91** ($7 \times 13 = 91$).
- This creates a "91-hour clock" where every mathematical operation wraps around 91. If you raise a message to a power on this clock, you get a scrambled number between 0 and 90.

### 3\. Euler's Totient Function: The Secret Second Clock

This is the part that trips many people up, but the video handles it elegantly. To figure out how to *reverse* the scrambling process, the person generating the keys has to build a completely separate, secret "maths clock". This is where **Euler's Totient Function** comes in.

For a product of two primes, Euler's totient is calculated by taking the number *just before* each prime and multiplying them together:

- Instead of 7 and 13, you take **6** ($7 - 1$) and **12** ($13 - 1$).
- Multiplying these gives **72** ($6 \times 12 = 72$).
- You now have a hidden **72-hour clock**. This number (72) is the value of Euler's totient function for 91.

### 4\. Generating the Public (e) and Private (d) Keys

With the secret 72-hour clock established, you can choose your keys:

- **The Public Key Exponent ($e$):** You pick a number that doesn't share any factors with 72. The video picks **5**. This number 5 is made public, along with the clock size of 91.
- **The Private Key Exponent ($d$):** You need to find a "magic companion number" that perfectly undoes the power of 5. On our secret 72-hour clock, you look for a number that, when multiplied by 5, lands exactly on **1**.
- That number is **29**, because $5 \times 29 = 145$. On a 72-hour clock, 145 wraps around twice ($72 + 72 = 144$) and leaves a remainder of exactly **1**.

### Why it Keeps Secrets Safe

When you want to send a message, you use the public numbers (**5** and **91**) to encrypt it. To decrypt it, you absolutely *must* know the secret companion number (**29**).

An eavesdropper can see the numbers 5 and 91, but to calculate that the secret key is 29, they would need to know the structure of the hidden 72-hour clock. The only way to find that 72-hour clock is to know the original prime factors (7 and 13). Because factorising the modulus is computationally impossible when the numbers are large, the secret remains completely safe.

Want to look at the exact step-by-step math of how the keys encrypt and decrypt a number?

![](https://www.youtube.com/watch?v=JD72Ry60eP4)

[Prime Numbers & RSA Encryption Algorithm - Computerphile](http://www.youtube.com/watch?v=JD72Ry60eP4) [Computerphile](https://www.youtube.com/channel/UC9-y-6csu5WGm29I7JiwpnA) **RSA** is widespread on the Internet, and uses large prime numbers - but how does it work? Dr Tim Muller takes us through the...

![](https://www.youtube.com/watch?v=-ShwJqAalOk)

[Breaking RSA - Computerphile](http://www.youtube.com/watch?v=-ShwJqAalOk) [Computerphile](https://www.youtube.com/channel/UC9-y-6csu5WGm29I7JiwpnA) If you pick the wrong prime numbers, cracking **RSA** becomes a cinch. Dr Mike Pound explains the findings of researcher Hanno...

![](https://www.youtube.com/watch?v=NmM9HA2MQGI)

[Secret Key Exchange (Diffie-Hellman) - Computerphile](http://www.youtube.com/watch?v=NmM9HA2MQGI) [Computerphile](https://www.youtube.com/channel/UC9-y-6csu5WGm29I7JiwpnA) How do we exchange a secret key in the clear? Spoiler: We don't - Dr Mike Pound shows us exactly what happens. **Mathematics**...

![](https://www.youtube.com/watch?v=hm8s6FAc4pg)

[The RSA Encryption Algorithm - How Does It Actually Work + Step-by-Step Example.](http://www.youtube.com/watch?v=hm8s6FAc4pg) [BrainWave](https://www.youtube.com/channel/UCiIgTqRPghspH6irR5S62Cw) By the end of this video, you'll have a solid understanding of how **RSA** works, from key generation to **encryption** and decryption,...

![](https://www.youtube.com/watch?v=hm8s6FAc4pg)

[The RSA Encryption Algorithm - How Does It Actually Work + Step-by-Step Example.](http://www.youtube.com/watch?v=hm8s6FAc4pg) [BrainWave](https://www.youtube.com/channel/UCiIgTqRPghspH6irR5S62Cw) By the end of this video, you'll have a solid understanding of how **RSA** works, from key generation to **encryption** and decryption,...

![](https://www.youtube.com/watch?v=wcbH4t5SJpg)

[How to Encrypt with RSA (but easy)](http://www.youtube.com/watch?v=wcbH4t5SJpg) [connor\_codes](https://www.youtube.com/channel/UC68_Xy9RPpejBR3Fzw7MJvA) A **simple explanation** of the **RSA encryption** algorithm. Includes a demonstration of encrypting and decrypting with the popular...

![](https://www.youtube.com/watch?v=qph77bTKJTM)

[How does RSA Cryptography work?](http://www.youtube.com/watch?v=qph77bTKJTM) [Tom Rocks Maths](https://www.youtube.com/channel/UCRfo-DAifrP3lzcxUHtGm_A) Oxford Sedleian Professor of Natural Philosophy Jon Keating explains the **RSA Cryptography** Algorithm. Get 25% off Blinkist...

![](https://www.youtube.com/watch?v=JD72Ry60eP4)

[Prime Numbers & RSA Encryption Algorithm - Computerphile](http://www.youtube.com/watch?v=JD72Ry60eP4) [Computerphile](https://www.youtube.com/channel/UC9-y-6csu5WGm29I7JiwpnA) **RSA** is widespread on the Internet, and uses large prime numbers - but how does it work? Dr Tim Muller takes us through the...[Eddie Woo · 1.3m views](http://www.youtube.com/watch?v=4zahvcJ9glg)
