*Shared from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday Dec 10, 2025 - 3:49 PM*
---
From FITFILE’s side this looks broadly right for what they need CAB approval for, and it aligns with the design you’ve already agreed with them (hub‑spoke, forced egress via their firewall, App Gateway fronting our node).

I would treat it as “good to go” with only a couple of clarifications/tweaks, not additional scope.

---

### 1. Peering / Routing – minor clarification

He currently says:

> Peered connection between vnet-hub-uks-01  

I’d suggest tightening that to make the two VNets explicit and to reflect the forced‑tunnelling intent:

> Peered connection between `vnet-hub-uks-01` (hub) and `vnet-default-fitf-uks-01` (FITFILE workload VNet), with gateway/route‑server forwarding enabled so that all outbound traffic from the FITFILE VNet is routed via the central firewall.

In the “Change Plan” bullets he’s already mentioning:

- “On the hub Vnet peer – Allow gateway or route server to forward traffic”
- “On the FITFILE peer – Enable hub Vnet remote gateway or route server.”

That’s exactly what we need; I’d just make the VNet names explicit so CAB can see which two networks are being tied together.

No extra routing objects beyond that need to go into the email – our own UDRs inside the FITFILE subscription will be handled by our Terraform.

---

### 2. Firewall rule collection – already correct

The bullets:

> Create a Firewall rule collection for the FITFILE Vnet  
> – Our standard rules to reach LCRCA services for monitoring, updates etc.  
> – The required FITFILE URLs and Services (doc attached)

…are exactly what we need them to seek approval for. The attached FITFILE endpoint list is where all the “Auth0 / Azure mgmt / GitLab / TFC / Vault / Grafana / Cloudflare” specifics live, so nothing more needs to be spelled out in this email as long as that document is indeed attached to the change.

No change required here.

---

### 3. Application Gateway / NSG – looks fine

What he’s proposing on App Gateway and NSG matches the agreed pattern:

- AppGW public listeners (HTTP/HTTPS, multi‑site).
- Backend pool pointing at the FITFILE Node’s private IP/FQDN.
- Rules mapping the hostnames to the `fitfile-service` backend.
- NSG adjustment on the AppGW frontend subnet to allow 80/443 from the relevant public IPs.

Two optional wording tweaks (not extra scope):

- Where he says `IP address or FQDN -> fitfile IP address`, I’d nudge to:

  > Backend targets: Private IP address of the FITFILE Node ingress controller

  just to avoid anyone thinking this is a direct public IP on our AKS nodes.

- If they already know the final public hostnames (for Cloudflare / DNS), you could suggest he replaces `http‑tbc` / `https‑tbc` with the real hostnames in the change text; otherwise “tbc” is acceptable as long as the design doc spells them out.

DNS/Cloudflare itself can stay outside this CAB item if that’s handled through their normal web/DNS change process.

---

### 4. Test plan – minor extension (optional)

His current test plan is:

> FITFILE team to test that they have egress connectivity and can perform a creation of their AKS cluster. To check that traffic is going through the appropriate route, we can utilise Network Watcher’s connection monitor and verify that the next hop is that of the Firewall IP address.

That is acceptable for CAB and covers the critical egress + firewall path.

If you want to be thorough, you could add one line:

> FITFILE will also validate inbound access by hitting the agreed FITFILE hostname(s) through the Application Gateway to confirm TLS and HTTP routing to the Node’s APIs.

But I wouldn’t hold up the change for that – it’s a documentation tweak only.

---

### 5. Nothing else *network‑wise* is missing

Other prerequisites we’ve discussed with them (service principal, jumpbox access, Conditional Access, etc.) are important but are **separate tasks** and don’t have to be bundled into this specific “network configuration” change. For CAB, the three things Jamie lists:

1. Hub–spoke VNet peering with gateway forwarding.
2. Firewall rule collection for FITFILE outbound URLs/services.
3. App Gateway + NSG changes for public ingress.

…are exactly the network changes we require in their tenant.

---

**Recommendation:**  
You can reply that from FITFILE’s perspective the change description is correct and complete for CAB purposes, with only these minor clarifications suggested:

- Name both VNets explicitly in the peering bullet.
- Optionally be more explicit about the FITFILE backend being our ingress private IP.
- Optionally add a sentence to the test plan about validating inbound HTTP(S) via AppGW.

If you want, I can draft you a 3–4 line reply you can paste straight back to Jamie.