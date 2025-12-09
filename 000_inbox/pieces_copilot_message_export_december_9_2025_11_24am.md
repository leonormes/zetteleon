*Shared from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Tuesday Dec 9, 2025 - 11:24 AM*
---
You’re right – in your pattern the jumpbox itself has no public IP and is reached via Bastion, so that wording is misleading.

Here’s an updated version of that part of the one‑pager (Section **3.1 Conditional Access: Test Azure CLI from the Jumpbox**), adjusted for a private jumpbox reached via Bastion:

---



---

If you’d like, I can also tweak the earlier “Who Does What” / prerequisites text to explicitly say “outbound IP of the hub firewall/NAT used by the spoke VNet” instead of “jumpbox public IP”.