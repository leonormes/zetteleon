---
captured: "2026-04-14T17:33:36+01:00 2026-04-14T17:33:36+01:00"
created: 2026-04-14T16:33:52+00:00
modified: 2026-04-19T18:30:45+00:00
source: "https://gemini.google.com/app/fd82eba6b861f9b4"
status: "processing"
tags: ["input"]
title: HEAD Passkeys
type: "head"
---

## Raw Output / Content

You

<https://youtu.be/xYfiOnufBSk?si=ZbnX30oH6iIGOTVJ>

---

Gemini

This video from Computerphile explains the mechanics and security advantages of Passkeys, a modern authentication method designed to replace traditional passwords.

### The Core Technology: Public Key Cryptography

Passkeys are built on WebAuthn technology and utilise public key cryptography rather than traditional hashed passwords.

- The Key Pair: When you create a passkey, two keys are generated: a public key (stored on the website's server) and a private key (stored securely on your local device).
- Digital Signatures: Instead of sending a secret password over the internet, the website sends a unique "challenge" or token. Your device signs this token using its private key and sends back a digital signature \[[03:05](http://www.youtube.com/watch?v=xYfiOnufBSk&t=185)\]. The website then verifies this signature using your public key to grant access.

### Key Components in the Process

The video identifies three main parties involved in every passkey transaction \[[04:06](http://www.youtube.com/watch?v=xYfiOnufBSk&t=246)\]:

1. Relying Party (RP): The website or service you are trying to access (e.g., an online shop).
2. Client: The software you use to browse, such as Google Chrome or Safari.
3. Authenticator: The hardware or software that holds the private key and performs the signing, such as Windows Hello, an Apple device, a YubiKey, or a mobile phone \[[08:00](http://www.youtube.com/watch?v=xYfiOnufBSk&t=480)\].

### Why Passkeys Are More Secure

- Anti-Phishing: Passkeys are "context-bound" to a specific domain. If you are tricked into visiting a fake website, your device will recognise that the domain ID does not match your stored passkey and will refuse to sign the request \[[14:10](http://www.youtube.com/watch?v=xYfiOnufBSk&t=850)\].
- No Replay Attacks: Every login session uses a "fresh" token that is only valid for a very short time, meaning an attacker cannot intercept and reuse a signature later \[[14:26](http://www.youtube.com/watch?v=xYfiOnufBSk&t=866)\].
- No Shared Secrets: Unlike passwords, the website never knows your private key. If the website's database is breached, hackers only get public keys, which are useless for logging into your account.

### Current Challenges

- Portability: If you create a passkey on a specific laptop, you generally cannot use it on your phone unless you use a synchronised credential provider like a password manager \[[09:15](http://www.youtube.com/watch?v=xYfiOnufBSk&t=555)\].
- Device Loss: Losing the device that holds your private key can result in being locked out. Currently, most systems still rely on a traditional password as a fallback, which means the vulnerability to phishing hasn't been entirely eliminated yet \[[16:18](http://www.youtube.com/watch?v=xYfiOnufBSk&t=978)\].
- User Verification: To prevent someone who steals your phone from accessing your accounts, most authenticators require a PIN or biometrics (face/fingerprint) before they will sign a login request \[[17:33](http://www.youtube.com/watch?v=xYfiOnufBSk&t=1053)\].

[http://www.youtube.com/watch?v=xYfiOnufBSk](http://www.youtube.com/watch?v=xYfiOnufBSk)
