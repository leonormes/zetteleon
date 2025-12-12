---
aliases: []
confidence: 
created: 2025-10-25T20:33:21Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T11:06:54Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Encryption - A Data-Centric View
type:
uid: 
updated: 
version:
---

*From a data-centric perspective explain how encryption works. Start with a very simple cipher to explain and then describe a modern secure encryption process*

Okay, let's break down encryption from a data-centric perspective, starting simple and moving towards modern methods, formatted for Obsidian.

## **Encryption: A Data-Centric View**

At its core, encryption is about **data transformation**. The goal is to take readable data (**plaintext**) and transform it into an unreadable format (**ciphertext**) using a specific method (**algorithm**) and a secret piece of information (**key**). Only someone possessing the correct key can reverse the transformation to recover the original plaintext. The entire purpose is to protect the **confidentiality** of the data – ensuring it remains secret from unauthorized eyes, whether it's stored somewhere (data at rest) or being sent across a network (data in transit).

### **1\. Simple Cipher Example: The Caesar Cipher**

Let's start with one of the oldest and simplest known ciphers, the Caesar Cipher.

- **Data:** We focus on textual data, specifically letters of the alphabet.  
- **Algorithm:** The rule is simple: shift each letter in the plaintext forward by a fixed number of positions in the alphabet.  
- **Key:** The "fixed number of positions" is the key. For example, a key of 3 means A becomes D, B becomes E, and so on, wrapping around from Z back to A.  
- **Plaintext Data:** SECRET  
- **Key:** 3  
- **Transformation Process (Data Point by Data Point):**  
  - S (position 19\) \+ 3 \= position 22 \-\> V  
  - E (position 5\) \+ 3 \= position 8 \-\> H  
  - C (position 3\) \+ 3 \= position 6 \-\> F  
  - R (position 18\) \+ 3 \= position 21 \-\> U  
  - E (position 5\) \+ 3 \= position 8 \-\> H  
  - T (position 20\) \+ 3 \= position 23 \-\> W  
- **Ciphertext Data:** VHFUHW

**Decryption (Data Recovery):** To get the original data back, someone needs the algorithm (Caesar Cipher) and the *same key* (3). They apply the reverse transformation: shift each letter *backward* by 3 positions.

- **Ciphertext Data:** VHFUHW  
- **Key:** 3  
- **Reverse Transformation:**  
  - V \- 3 \-\> S  
  - H \- 3 \-\> E  
  - F \- 3 \-\> C  
  - U \- 3 \-\> R  
  - H \- 3 \-\> E  
  - W \- 3 \-\> T  
- **Recovered Plaintext Data:** SECRET

**Data-Centric Weaknesses:**

- **Limited Key Space:** There are only 25 possible keys (shifts 1 through 25; shift 0 or 26 results in the original data). This makes **brute-force attacks** trivial – an attacker can simply try transforming the ciphertext with every possible key until readable plaintext appears.  
- **Preserves Data Patterns:** The frequency of letters in the ciphertext mirrors the frequency in the plaintext (e.g., if 'E' is common in the plaintext language, the letter 'E' shifted by the key will be common in the ciphertext). This allows **frequency analysis** to break the cipher easily, even without trying all keys. The underlying statistical properties of the data are poorly hidden.

### **2\. Modern Secure Encryption: Symmetric Encryption (e.g., AES)**

Simple ciphers are easily broken by modern computers. Modern encryption uses vastly more complex algorithms and keys. Let's look at **Symmetric Encryption**, where the *same key* is used for both encryption and decryption. The Advanced Encryption Standard (AES) is the most widely used example.

- **Data:** Modern encryption operates on **binary data** – sequences of bits (0s and 1s). Text, images, videos, etc., are all represented as bits before encryption. AES specifically operates on fixed-size **blocks** of data, typically 128 bits (16 bytes).  
- **Key:** The key is also a sequence of bits. AES supports key lengths of 128, 192, or 256 bits.  
  - **Data-Centric Significance:** A 128-bit key has 2\<sup\>128\</sup\> possible combinations. A 256-bit key has 2\<sup\>256\</sup\> combinations. These numbers are astronomically large, making brute-force attacks (trying every key) computationally infeasible with current and foreseeable technology.  
- **Algorithm (AES):** AES is a **block cipher** that applies multiple rounds of complex mathematical operations to each 128-bit block of plaintext data. The number of rounds depends on the key size (10 rounds for 128-bit keys, 12 for 192, 14 for 256).  
  - **Key Schedule:** The initial key is expanded into a series of unique **round keys**, one for each round. This means the transformation changes slightly in each round, adding complexity.  
  - **Round Operations (Applied to the Data Block):** Each round (except the last) typically involves four transformations performed on the 16 bytes (128 bits) of data, often visualized as a 4x4 matrix:  
    1. **SubBytes (Substitution):** Each byte of data is substituted with another byte according to a predefined lookup table called the S-box.  
       - *Data Effect:* This is a non-linear step, crucial for obscuring the relationship between the plaintext, the key, and the ciphertext. It provides **confusion**, making the ciphertext statistics complex even if the plaintext statistics are simple.  
    2. **ShiftRows (Permutation):** The bytes in the last three rows of the 4x4 data matrix are shifted cyclically by different offsets.  
       - *Data Effect:* This shuffles the byte positions within the block, spreading the influence of individual plaintext bits across the entire block. This provides **diffusion**, meaning a change in one plaintext bit should ideally affect roughly half the ciphertext bits.  
    3. **MixColumns (Mixing):** Each column of the data matrix is transformed using a specific mathematical operation (matrix multiplication in a finite field).  
       - *Data Effect:* This further enhances diffusion, mixing data *between* bytes within a column, ensuring changes propagate rapidly across the block.  
    4. **AddRoundKey (Key Addition):** The current data block is combined with the round key for that round using a bitwise XOR operation.  
       - *Data Effect:* This incorporates the secret key material into the data block during each round. Without the correct round keys (derived from the main key), this step cannot be reversed.  
- **Transformation Process (Conceptual):**  
  1. The initial 128-bit plaintext block is XORed with the first round key.  
  2. The block goes through Rounds 1 to N-1 (where N is the total number of rounds), each applying SubBytes, ShiftRows, MixColumns, and AddRoundKey (using the respective round key).  
  3. The final round (Round N) applies SubBytes, ShiftRows, and AddRoundKey (it typically omits MixColumns).  
- **Ciphertext Data:** The output after the final round is the 128-bit ciphertext block corresponding to the input plaintext block. It should appear statistically random and bear no discernible relationship to the plaintext without the key.

**Handling Data Larger Than One Block (Modes of Operation):**  
Real-world data is usually larger than 128 bits. Simply encrypting each block independently (called Electronic Codebook \- ECB mode) is insecure because identical plaintext blocks produce identical ciphertext blocks, revealing data patterns. **Modes of Operation** define how to securely encrypt sequences of blocks.

- **Example: Cipher Block Chaining (CBC):**  
  - An **Initialization Vector (IV)** – a random or pseudo-random block of data – is required. It should be unique for each encryption process with the same key.  
  - **Data Flow:**  
    1. The first plaintext block is XORed with the IV.  
    2. The result is encrypted using the AES algorithm and key, producing the first ciphertext block.  
    3. For subsequent blocks: The *previous* ciphertext block is XORed with the *current* plaintext block.  
    4. The result is encrypted using AES and the key, producing the current ciphertext block.  
  - *Data Effect:* Each ciphertext block depends on all preceding plaintext blocks. Changing one bit in a plaintext block affects that ciphertext block and all subsequent ones during decryption. Identical plaintext blocks will produce different ciphertext blocks if they appear at different positions in the sequence. The IV ensures that even if the same message is encrypted twice with the same key, the resulting ciphertexts will be different.  
- **Other Modes (e.g., GCM \- Galois/Counter Mode):** Modern modes like GCM not only provide confidentiality but also **data integrity** and **authenticity**. They generate an **authentication tag** alongside the ciphertext. If the ciphertext or the tag is tampered with during transmission or storage, the tag verification will fail during decryption, alerting the recipient that the data is corrupted or forged. This adds protection beyond just secrecy.

**Decryption (Data Recovery with AES):**  
Decryption uses the *same* key and essentially reverses the AES steps: Inverse ShiftRows, Inverse SubBytes, AddRoundKey, Inverse MixColumns (applied in the appropriate order). The key schedule is also used to generate the necessary round keys. For modes like CBC, the IV is also needed, and the chaining process is reversed.

### **3\. Asymmetric (Public-Key) Encryption**

For completeness, it's worth mentioning asymmetric encryption.

- **Key Pair:** Uses two mathematically linked keys: a **Public Key** (shared openly) and a **Private Key** (kept secret).  
- **Data Transformation:**  
  - Data encrypted with the Public Key can *only* be decrypted with the corresponding Private Key.  
  - Data encrypted (or signed) with the Private Key can be verified (or decrypted) with the corresponding Public Key.  
- **Data-Centric Use Cases:**  
  - **Confidentiality:** Anyone can encrypt data for a recipient using their Public Key, but only the recipient with the Private Key can decrypt it.  
  - **Authentication/Digital Signatures:** A sender can sign data with their Private Key. Anyone can verify the signature using the sender's Public Key, proving the data originated from them and hasn't been tampered with.  
- **Performance:** Asymmetric encryption is computationally much slower than symmetric encryption.

### **4\. Hybrid Encryption (Common Practice)**

Because of the speed difference, large amounts of data are rarely encrypted directly with asymmetric algorithms. Instead, a **hybrid approach** is common:

1. Generate a temporary, random **session key** for a fast symmetric cipher like AES.  
2. Encrypt the actual **bulk data** using AES and this session key.  
3. Encrypt the **session key** itself using the recipient's **Public Key** (asymmetric encryption).  
4. Send the AES-encrypted data *and* the asymmetrically-encrypted session key to the recipient.  
5. The recipient uses their **Private Key** to decrypt the session key.  
6. The recipient uses the now-decrypted session key to decrypt the bulk data using AES.

**Data-Centric View:** This combines the efficiency of symmetric encryption for the large volume of primary data with the secure key distribution mechanism of asymmetric encryption for the small, crucial session key.

### **Conclusion**

From a data-centric viewpoint, encryption is the science of applying reversible, key-dependent transformations to data to make it unintelligible without the secret key. Modern methods like AES employ complex, multi-round operations involving substitution and permutation on blocks of data bits, driven by large keys, to achieve a high degree of confusion and diffusion. This ensures that the ciphertext reveals practically no statistical information about the plaintext and is resistant to brute-force attacks. Modes of operation and hybrid systems extend these principles to handle large data volumes securely and efficiently, often adding layers for data integrity and authenticity checks, ensuring comprehensive data protection.
