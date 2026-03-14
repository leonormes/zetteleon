---
captured: "2026-03-07T16:53:24+00:00 2026-03-07T16:53:24+00:00"
created: 2026-03-07T16:53:25+00:00
modified: 2026-03-14T11:10:41+00:00
source: "https://claude.ai/chat/95d15f66-de75-4e66-9e22-583f4eb32b93"
status: "processing"
tags: ["input", 10, 4]
title: HEAD Finding outbound IP address from private cluster pod
type: "head"
---

## Raw Output / Content

from a pod in a private cluster using netshoot i want to find out the outbound ip address, how it would appear to a cluster receiving a request from it. I need to whitelist the sending cluster's ip

---

From your netshoot pod, run:

That returns the public IP as seen by the destination—which is exactly the IP you need to whitelist.

Why this works: Traffic from a private AKS cluster exits through either the Azure Load Balancer's outbound IP or a NAT Gateway (depending on your egress config). `ifconfig.me` simply echoes back the source IP it sees on the incoming connection, so you get the exact address the receiving cluster would see.

Alternatives if `ifconfig.me` is unreachable (some corporate firewalls block these):

One thing to watch: If your cluster uses multiple outbound IPs (e.g. a Load Balancer with several frontend IPs, or a NAT Gateway with a prefix), traffic may rotate across them. To check all possible egress IPs, run it a few times or, more reliably, check the Azure resource directly:

Then resolve those resource IDs to actual IPs. That gives you the full set to whitelist rather than relying on whichever one `curl` happened to hit.

---

how do I get the inbound ip address for my reciving cluster

---

It depends on how your ingress is set up. Here are the most common scenarios:

---

If you're using an Ingress Controller (e.g. NGINX, Traefik):

The `EXTERNAL-IP` column is your inbound IP—that's what you'd whitelist as the destination the sending cluster talks to, and more importantly, what you'd configure to only accept traffic from the sending cluster's outbound IP.

---

If you're using a LoadBalancer-type Service directly:

---

If traffic comes through Cloudflare (which it likely does for your FITFILE setup):

The "inbound IP" the outside world sees is Cloudflare's edge, not your cluster directly. In that case:

1. The sending cluster hits Cloudflare's IP (resolved from DNS)
2. Cloudflare proxies to your cluster's actual ingress IP

So whitelisting works differently—you'd either:

- Whitelist at Cloudflare (WAF/firewall rule allowing the sending cluster's outbound IP)
- Or if the sending cluster bypasses Cloudflare and hits the cluster ingress directly, whitelist on the Azure NSG or the ingress controller itself

---

Quick way to confirm what the sending cluster actually resolves:

From your netshoot pod on the sending cluster:

That tells you exactly which IP the sending cluster will try to connect to—and therefore where the firewall rule needs to live.

Immediate next step: Run that `nslookup` from the sending cluster. The answer tells you whether you're whitelisting at Cloudflare, at an Azure NSG, or on the ingress controller directly.

---

kubectl get svc -n ingress-nginx -l app.kubernetes.io/name=ingress-nginx NAME TYPE CLUSTER-IP EXTERNAL-IP PORT(S) AGE ingress-nginx-controller LoadBalancer 10.2.0.251 10.200.80.50 80:32073/TCP,443:32635/TCP 10d ingress-nginx-controller-admission ClusterIP 10.2.0.48 <none> 443/TCP 10d

---

That `10.200.80.50` is a private IP—your ingress controller is using an internal Azure Load Balancer, which is exactly what you'd expect for a private cluster.

This means:

1. There's no public inbound IP to whitelist. The receiving cluster isn't exposed to the internet.
2. Traffic must flow over private networking—VNet peering, VPN, or similar. The sending cluster needs network-level connectivity to that `10.200.80.50` address.

So the whitelisting question becomes about NSGs and/or Network Policies, not public IPs.

You need to ensure:

- VNet peering (or equivalent connectivity) exists between the sending and receiving clusters' VNets
- The route tables allow traffic between the two address spaces
- The NSG on the receiving cluster's subnet allows inbound from the sending cluster's pod/node CIDR
- If you're using Kubernetes NetworkPolicies, they permit ingress from the sending cluster's source range

Immediate next step—confirm the network topology from the sending cluster:

If it times out, the private network path isn't there yet. If you get a connection (even a 404), the routing works and it's a firewall/NSG rule you need to open.

---

I have been told the inbound is 20.90.82.168 Attached is the sg I think we need to update

---

Good—that `20.90.82.168` is likely the public IP on the Azure Load Balancer fronting your ingress controller. Since the sending cluster's traffic will arrive from the public internet (not via VNet peering), it'll be seen as a non-VNet source and hit your Deny-All-Inbound at priority 4096.

You need a new rule slotted between the existing allows and the deny. Something like:

Why these values:

- Priority 120—evaluated after VNet (100) and AzureLB (110), but well before Deny-All (4096)
- Source—the sending cluster's outbound IP (the one you got from `curl ifconfig.me` on the netshoot pod)
- Destination `10.200.80.50`—your ingress controller's internal LB IP. Traffic arrives at the public IP `20.90.82.168` on the Azure LB, which DNATs it to this private IP on the node subnet
- Port 443 only—principle of least privilege rather than opening all ports

Before you run that, two things to confirm:

1. Get the sending cluster's outbound IP if you haven't already—`curl -s https://ifconfig.me` from the netshoot pod
2. Check if there are multiple outbound IPs—if the sending cluster uses a NAT Gateway with multiple IPs, you'll need all of them in `--source-address-prefixes` (space-separated)

Since this NSG is managed by Terraform, you'll likely want to add this rule in your Terraform config rather than via CLI, to avoid drift. But the CLI is fine for validating connectivity first.

---

outbound from sending cluster is 20.68.120.178

---

Right, so the concrete command:

Once that's applied, validate from the netshoot pod on the sending cluster:

You should get a connection (likely a 404 or default backend response from NGINX, which is fine—it proves the network path is open). A timeout means something else is blocking—check whether there's a second NSG on the AKS node subnet itself, as AKS sometimes attaches its own.

---

\# mtr -n -T -P 443 -r -c 10 $TIP Start: 2026-03-06T16:35:25+0000 HOST: tmp-shell Loss% Snt Last Avg Best Wrst StDev 1.|-- 172.25.7.5 0.0% 10 0.1 0.1 0.1 0.1 0.0 2.|--??? 100.0 10 0.0 0.0 0.0 0.0 0.0

---

MTR with TCP can be misleading here—intermediate hops often drop TTL-exceeded replies for TCP probes, so `???` at hop 2 doesn't necessarily mean traffic is blocked. It just means that hop didn't respond to the probe.

The real test is end-to-end connectivity. Try a direct curl from the same netshoot pod:

If that also times out, then the issue is genuine. In that case, check from the sending side:

1\. Is outbound to that specific IP blocked?

2\. What does the sending cluster's egress path look like? The `172.25.x.x` first hop suggests this might be an AWS EKS cluster. If so, check the security group on the EKS nodes—it may restrict outbound to specific ports/destinations rather than allowing all egress.

If general internet works but `20.90.82.168:443` specifically doesn't, the block is on the receiving side. That would mean either:

- The NSG rule hasn't propagated yet (give it a minute)
- The Azure LB doesn't have a load balancing rule forwarding port 443 to the backend pool
- The NSG we updated (`nsg-lca-uks-prd-system`) isn't attached to the subnet the LB actually delivers traffic to—check if there's a separate NSG on the AKS node subnet

---

here is another sg

---

This one—`nsg-default-fflz-01`—has zero custom rules. Only Azure defaults. That means the only inbound allows are `VirtualNetwork` and `AzureLoadBalancer`. Any traffic from a public IP like `20.68.120.178` would hit `DenyAllInBound` at 65500.

The critical question is: which subnet is this NSG attached to? Check with:

If this NSG is on the subnet where the AKS nodes or the internal load balancer live, then this is your actual blocker—not the first NSG. Azure evaluates NSGs per-subnet, so both the source and destination subnets' NSGs must allow the traffic.

You likely need the allow rule on both NSGs. For this one:

Immediate next step: Run that `az network nsg show` query to confirm which subnet this is attached to. That tells you whether this NSG is in the traffic path, and whether it's the one actually blocking you.

---

az network nsg rule create \\ --resource-group rg-lca-uks-prd-net \\ --nsg-name nsg-lca-uks-prd-system \\ --name Allow-SendingCluster-Inbound \\ --priority 120 \\ --direction Inbound \\ --access Allow \\ --protocol Tcp \\ --source-address-prefixes 20.68.120.178 \\ --source-port-ranges '\*' \\ --destination-address-prefixes 10.200.80.50 \\ --destination-port-ranges 443 bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) { "access": "Allow", "destinationAddressPrefix": "10.200.80.50", "destinationAddressPrefixes": \[\], "destinationPortRange": "443", "destinationPortRanges": \[\], "direction": "Inbound", "etag": "W/\\"ada12dbf-72e9-4585-a295-bc6e3150c19f\\"", "id": "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/rg-lca-uks-prd-net/providers/Microsoft.Network/networkSecurityGroups/nsg-lca-uks-prd-system/securityRules/Allow-SendingCluster-Inbound", "name": "Allow-SendingCluster-Inbound", "priority": 120, "protocol": "Tcp", "provisioningState": "Succeeded", "resourceGroup": "rg-lca-uks-prd-net", "sourceAddressPrefix": "20.68.120.178", "sourceAddressPrefixes": \[\], "sourcePortRange": "\*", "sourcePortRanges": \[\], "type": "Microsoft.Network/networkSecurityGroups/securityRules" } ➜ ~ curl -v [https://20.90.82.168](https://20.90.82.168/) --insecure -m 10 \* Trying 20.90.82.168:443… ^C ➜ ~ az network nsg show \\ -g rg-vnet-fflz-01 \\ -n nsg-default-fflz-01 \\ --query "subnets\[\].id" -o tsv bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) ➜ ~ az network nsg rule create \\ --resource-group rg-vnet-fflz-01 \\ --nsg-name nsg-default-fflz-01 \\ --name Allow-SendingCluster-Inbound \\ --priority 100 \\ --direction Inbound \\ --access Allow \\ --protocol Tcp \\ --source-address-prefixes 20.68.120.178 \\ --source-port-ranges '\*' \\ --destination-address-prefixes 10.200.80.50 \\ --destination-port-ranges 443 bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) { "access": "Allow", "destinationAddressPrefix": "10.200.80.50", "destinationAddressPrefixes": \[\], "destinationPortRange": "443", "destinationPortRanges": \[\], "direction": "Inbound", "etag": "W/\\"e161fed0-e511-4822-8a2f-d23dc4854219\\"", "id": "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/rg-vnet-fflz-01/providers/Microsoft.Network/networkSecurityGroups/nsg-default-fflz-01/securityRules/Allow-SendingCluster-Inbound", "name": "Allow-SendingCluster-Inbound", "priority": 100, "protocol": "Tcp", "provisioningState": "Succeeded", "resourceGroup": "rg-vnet-fflz-01", "sourceAddressPrefix": "20.68.120.178", "sourceAddressPrefixes": \[\], "sourcePortRange": "\*", "sourcePortRanges": \[\], "type": "Microsoft.Network/networkSecurityGroups/securityRules" }

---

Two things jump out from that output:

The `nsg-default-fflz-01` returned no subnets—the query came back empty. So that NSG isn't attached to anything and isn't in the traffic path. The rule you added there is harmless but irrelevant.

The curl still timed out, which points to a more fundamental problem: your ingress controller is on an internal load balancer (EXTERNAL-IP `10.200.80.50` is a private IP). An internal Azure LB has no public frontend—it's unreachable from the internet by design.

So the question becomes: what actually is `20.90.82.168`? Check it:

It might be a public IP on the AKS outbound LB (used for egress, not ingress), or attached to something else entirely like the jumpbox or Bastion.

If the sending cluster needs to reach this private cluster over the public internet, you'd need one of:

- A public-facing Azure Load Balancer or Application Gateway in front of the ingress
- An Azure VPN Gateway or ExpressRoute connecting the two networks
- If both clusters are in Azure, VNet peering—then the sending cluster talks directly to `10.200.80.50` over the private network, no public IP needed

Immediate next step: Run that `az network public-ip list` query to find out what `20.90.82.168` is actually attached to. That determines the whole approach from here.

---

az network public-ip list \\ --query "\[?ipAddress=='20.90.82.168'\].{name:name, rg:resourceGroup, associated:ipConfiguration.id}" \\ -o table bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) Name Rg Associated ------------------------- ----------------------- ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- pip-fflz-lb-uks-public-01 RG-CONNECTIVITY-FFLZ-01 /subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01/frontendIPConfigurations/fipcfg-fflz-lb-uks-public-01

---

That's a separate public-facing load balancer (`lb-fflz-uks-public-01`) in the connectivity resource group. So the architecture is:

The missing piece is whether this public LB is actually configured to forward traffic to the AKS nodes. Check its load balancing rules and backend pool:

If there are no load balancing rules for port 443 (or the backend pool is empty), that's your problem—the public IP exists but nothing is wired up to forward traffic through to the cluster.

The fix would depend on the intended architecture. If this public LB is meant to front the ingress controller, it needs a rule forwarding port 443 to the AKS nodes on NodePort 32635 (from your earlier `kubectl get svc` output showing `443:32635/TCP`).

---

\# What rules does it have? az network lb rule list \\ -g RG-CONNECTIVITY-FFLZ-01 \\ --lb-name lb-fflz-uks-public-01 \\ -o table # What's in the backend pool? az network lb address-pool list \\ -g RG-CONNECTIVITY-FFLZ-01 \\ --lb-name lb-fflz-uks-public-01 \\ -o table bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) BackendPort DisableOutboundSnat EnableFloatingIP EnableTcpReset FrontendPort IdleTimeoutInMinutes LoadDistribution Name Protocol ProvisioningState ResourceGroup ------------- --------------------- ------------------ ---------------- -------------- ---------------------- ------------------ --------------------------- ---------- ------------------- ----------------------- 443 False False False 443 4 Default lb-fflz-uks-public-01-rule1 Tcp Succeeded RG-CONNECTIVITY-FFLZ-01 bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) Name ProvisioningState ResourceGroup ------------------------- ------------------- ----------------------- bap-fflz-lb-uks-public-01 Succeeded RG-CONNECTIVITY-FFLZ-01

---

Good—there's a rule forwarding 443→443 and a backend pool exists. Two things to check now:

1\. Does the backend pool actually have members?

If that comes back empty, the LB is forwarding to nothing—that's your blocker.

2\. The backend port might be wrong. The rule forwards to backend port 443, but your ingress controller's NodePort is 32635 (from the `kubectl get svc` output: `443:32635/TCP`). If the backend pool targets AKS nodes directly, the LB should be forwarding to 32635, not 443. Port 443 on the node itself won't have anything listening unless the backend targets the internal LB IP or a VM running a reverse proxy.

So: run that query, and share what the backend pool members are. That'll tell us whether this is a "no backends" problem or a "wrong port" problem.

---

az network lb address-pool show \\ -g RG-CONNECTIVITY-FFLZ-01 \\ --lb-name lb-fflz-uks-public-01 \\ -n bap-fflz-lb-uks-public-01 \\ --query "backendIPConfigurations\[\].id" -o tsv bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) ➜ ~

---

Empty. The backend pool has zero members. That's your blocker—the public LB is accepting traffic on 443 but has nowhere to send it, so connections just hang (exactly the timeout behaviour you're seeing).

You need to decide the forwarding target. There are two common patterns:

Option A: Point the backend pool at the AKS nodes (NodePort)

This forwards traffic to the ingress-nginx NodePort on the AKS nodes. You'd need to add the AKS node NICs to the backend pool, and change the backend port from 443 to 32635.

Option B: Point the backend pool at the internal LB IP

This is cleaner—the public LB forwards to `10.200.80.50:443` (your internal ingress LB). But Azure LB-to-LB chaining doesn't work natively; you'd need an NVA or Azure Application Gateway in between.

Before wiring anything up, it's worth asking: was this public LB intentionally left empty? Given your split-horizon DNS setup with Cloudflare, the intended ingress path for external traffic might be through Cloudflare (which would connect via a Cloudflare Tunnel or similar), not through this public LB at all. In that case, this LB might be a leftover or reserved for a different purpose.

Immediate next step: Check with whoever set up `lb-fflz-uks-public-01` (or check your Terraform) to understand its intended purpose. If it's meant to receive external cluster-to-cluster traffic, Option A is the path—add AKS node NICs and fix the backend port. If external ingress is meant to go through Cloudflare, then the sending cluster should be configured to reach the service via the Cloudflare-proxied hostname instead.

---

Two important things from those files:

1\. The LB rule has no health probe (shown as `-`). Even once you add backends, the LB won't know if they're healthy and may not forward traffic.

2\. There's an AKS-managed NSG you haven't checked yet:`aks-agentpool-31829346-nsg` in `rg-lca-uks-prd-aks`. This is the NSG Azure automatically attaches to the AKS node NICs—it's always in the traffic path and could independently block traffic even if every other NSG allows it.

Check its rules:

But stepping back—the fundamental blocker is still the empty backend pool. The full chain of issues is:

1. Backend pool has no members—nothing receives forwarded traffic
2. No health probe—LB can't determine backend health
3. Backend port is 443—but nginx NodePort is 32635
4. Potentially missing NSG rules on the AKS-managed NSG

Before spending time on items 2-4, you need to resolve the architecture question: is this public LB the correct path for this cluster-to-cluster traffic, or should the sending cluster be reaching you via VNet peering or a Cloudflare tunnel? That answer determines whether you should be populating this backend pool or taking a completely different approach.

If this LB _is_ the right path, the sequence would be: add AKS nodes to backend pool → fix backend port to 32635 → add a health probe on 32635 → verify NSG rules on `aks-agentpool-31829346-nsg`. Happy to walk through each step once you've confirmed the approach.

---

az network lb address-pool show \\ -g RG-CONNECTIVITY-FFLZ-01 \\ --lb-name lb-fflz-uks-public-01 \\ -n bap-fflz-lb-uks-public-01 \\ --query "backendIPConfigurations\[\].id" -o tsv bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) ➜ ~ az network nsg rule list \\ -g rg-lca-uks-prd-aks \\ --nsg-name aks-agentpool-31829346-nsg \\ -o table bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) Name ResourceGroup Priority SourcePortRanges SourceAddressPrefixes SourceASG Access Protocol Direction DestinationPortRanges DestinationAddressPrefixes DestinationASG ------------------- ------------------ ---------- ------------------ ----------------------- ----------- -------- ---------- ----------- ----------------------- ---------------------------- ---------------- Allow-NWSDE-Inbound rg-lca-uks-prd-aks 100 \* 20.68.120.178 None Allow \* Inbound 443 \* None ➜ ~

---

Someone's already been here before you—that `Allow-NWSDE-Inbound` rule on the AKS-managed NSG is pre-configured for exactly `20.68.120.178` on port 443. So the NSG layer is sorted. The only blocker is the empty backend pool on the public LB.

The LB rule forwards 443→443 (not 443→32635), and the NSG allows 443—this suggests the intended design is to target the internal LB IP (`10.200.80.50`) as a backend address, not the AKS node NICs. That's consistent with IP-based backend pools on Azure Standard LB.

Check if the backend pool is IP-based:

If it's an empty array, you can add the internal LB IP as a backend:

Before running the add command, confirm the VNet resource ID is correct—adjust if the VNet name differs. You can check with:

This would complete the chain: public LB (20.90.82.168:443) → internal LB (10.200.80.50:443) → ingress-nginx pod. The NSGs are already allowing it.

---

az network lb address-pool show \\ -g RG-CONNECTIVITY-FFLZ-01 \\ --lb-name lb-fflz-uks-public-01 \\ -n bap-fflz-lb-uks-public-01 \\ --query "loadBalancerBackendAddresses" -o json bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) \[{ "adminState": "Up", "ipAddress": "10.200.80.50", "name": "bap-fflz-lb-uks-public-01-ipaddress1", "virtualNetwork": { "id": "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/rg-vnet-fflz-01/providers/Microsoft.Network/virtualNetworks/vnet-fflz-uks-01", "resourceGroup": "rg-vnet-fflz-01" } } \]

---

The backend pool is configured—it already has `10.200.80.50` as an IP-based member, `adminState: Up`. So the earlier `backendIPConfigurations` query returned empty because that field is for NIC-based backends, not IP-based ones. My mistake.

So the chain _should_ work, but the curl still timed out. The remaining suspect is the missing health probe. The LB rules CSV showed the probe as `-`. On an Azure Standard LB, no health probe = all backends considered unhealthy = no traffic forwarded. That's almost certainly your blocker.

Check current probes:

If empty, create one and attach it to the rule:

Once that's in place, retry the curl from the sending cluster. The LB should start forwarding as soon as the probe marks `10.200.80.50` as healthy (within a few seconds).

---

{ "backendAddressPool": { "id": "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01/backendAddressPools/bap-fflz-lb-uks-public-01", "resourceGroup": "RG-CONNECTIVITY-FFLZ-01" }, "backendAddressPools": \[{ "id": "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01/backendAddressPools/bap-fflz-lb-uks-public-01", "resourceGroup": "RG-CONNECTIVITY-FFLZ-01" } \], "backendPort": 443, "disableOutboundSnat": false, "enableFloatingIP": false, "enableTcpReset": false, "etag": "W/\\"a18f6b95-b695-4587-9e0e-e9194d9e591a\\"", "frontendIPConfiguration": { "id": "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01/frontendIPConfigurations/fipcfg-fflz-lb-uks-public-01", "resourceGroup": "RG-CONNECTIVITY-FFLZ-01" }, "frontendPort": 443, "id": "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01/loadBalancingRules/lb-fflz-uks-public-01-rule1", "idleTimeoutInMinutes": 4, "loadDistribution": "Default", "name": "lb-fflz-uks-public-01-rule1", "probe": { "id": "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01/probes/probe-https-443", "resourceGroup": "RG-CONNECTIVITY-FFLZ-01" }, "protocol": "Tcp", "provisioningState": "Succeeded", "resourceGroup": "RG-CONNECTIVITY-FFLZ-01", "type": "Microsoft.Network/loadBalancers/loadBalancingRules" } ➜ ~ az network lb probe list \\ -g RG-CONNECTIVITY-FFLZ-01 \\ --lb-name lb-fflz-uks-public-01 \\ -o table bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) IntervalInSeconds Name NumberOfProbes Port ProbeThreshold Protocol ProvisioningState ResourceGroup ------------------- --------------- ---------------- ------ ---------------- ---------- ------------------- ----------------------- 5 probe-https-443 2 443 1 Tcp Succeeded RG-CONNECTIVITY-FFLZ-01

---

Probe's attached and the rule looks fully wired now. Time to test—from the netshoot pod on the sending cluster:

If it connects, you should get a response from nginx (likely a 404 or default backend). If it still times out, check the probe health status:

And also check if the backend is showing as healthy in the portal under Load Balancer → Backend pool → Health probe status, as the CLI doesn't surface probe health directly. If the probe can't reach `10.200.80.50:443`, the backend stays unhealthy and the LB won't forward—which would point to an NSG or routing issue between the LB's subnet and the internal LB subnet.

---

az network lb show \\ -g RG-CONNECTIVITY-FFLZ-01 \\ -n lb-fflz-uks-public-01 \\ --query "probes\[0\].provisioningState" -o tsv bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) Succeeded

---

That just confirms the probe resource was provisioned—it doesn't tell us whether the backend is actually passing health checks. Did the curl test work?

If it's still timing out, the probe is likely failing (meaning the LB can't reach `10.200.80.50:443` from its probing infrastructure). To confirm, check the backend health via:

But the most reliable way is in the portal: Load Balancer → Insights (or Monitoring → Metrics → "Health Probe Status"). That'll show you whether the probe is returning up or down for `10.200.80.50`.

If the probe is failing, the issue is that the public LB's health probes originate from Azure's infrastructure network (service tag `AzureLoadBalancer`), and they need to reach `10.200.80.50:443` across the VNet. Check whether the NSG on the subnet hosting the internal LB allows `AzureLoadBalancer` inbound on 443—the `nsg-lca-uks-prd-system` does have `Allow-AzureLB-Inbound` at priority 110, but only if it's on the right subnet.

---

az network lb probe list \\ -g RG-CONNECTIVITY-FFLZ-01 \\ --lb-name lb-fflz-uks-public-01 \\ -o table bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) IntervalInSeconds Name NumberOfProbes Port ProbeThreshold Protocol ProvisioningState ResourceGroup ------------------- --------------- ---------------- ------ ---------------- ---------- ------------------- ----------------------- 5 probe-https-443 2 443 1 Tcp Succeeded RG-CONNECTIVITY-FFLZ-01 ➜ ~ az network lb show \\ -g RG-CONNECTIVITY-FFLZ-01 \\ -n lb-fflz-uks-public-01 \\ --query "probes\[0\].provisioningState" -o tsv bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) Succeeded

---

Those are the same commands again—they only confirm the probe _exists_, not whether it's passing. The key question is: did the curl work?

From the netshoot pod on the sending cluster:

That's the real test. Everything else is secondary until we know if traffic is flowing end-to-end.

---

Good context. The internal LB (`kubernetes-internal`) is properly configured—two rules (80 and 443), a `kubernetes` backend pool (which AKS automatically populates with node NICs), and a health probe on port 31363 (that's the nginx ingress health check NodePort).

So the full chain is:

The internal side is solid. The question remains: can the public LB's health probe reach `10.200.80.50:443`? The probe needs a TCP handshake to succeed, and the internal LB _should_ accept it since it's listening on 443.

Have you been able to run the curl test from the sending cluster yet?

If you haven't got access to the netshoot pod right now, you could also test from the jumpbox (`vmlcajmp01`) since it's on the same VNet—that would at least confirm the public LB → internal LB path works:

Either way, the curl result is the single piece of information that determines the next step.

---

how can I check the endpoint from the jumpbox

---

From the jumpbox, just run:

If curl isn't installed on the jumpbox:

One caveat: If the jumpbox is in the same VNet, Azure might hairpin the traffic differently than an external source would. To get a true external test, you could also try from your own local machine or Cloud Shell:

Cloud Shell would be the closest to what the sending cluster actually experiences.

---

I mean by hitting the private endpoint in the cluster from the jmp just to check that it works locally

---

Ah—just hit the internal LB IP directly:

If that returns a response (even a 404), the internal ingress is healthy and the problem is isolated to the public LB → internal LB path. If it times out, the issue is deeper than the public LB.

---

That worked. give me commands to run a forensic investigation into all the components

---

Good—internal path is confirmed working. So the problem is between the public LB and `10.200.80.50`. Here's a systematic walkthrough:

---

1\. Public LB health probe status (the most likely culprit)

2\. Public LB full configuration dump

3\. Public IP configuration

4\. Subnet and NSG mapping for every subnet in the VNet

5\. Route tables (a UDR could be blackholing traffic)

6\. All NSG rules across every NSG in the environment

7\. NSG flow logs (if enabled—shows actual traffic decisions)

8\. Effective routes on an AKS node NIC (checks for blackhole UDRs)

9\. Effective NSG rules on an AKS node NIC (the ultimate truth)

10\. Azure LB metrics via CLI (probe health over last 5 minutes)

---

Start with 10 and 4. The metrics will tell you immediately if the probe is failing. The subnet listing will tell you if there's a route table (UDR) in the path that might be sending traffic to a firewall or NVA instead of directly to the internal LB. Those two results will narrow the problem to either a routing issue or a probe/NSG issue.

---

This is really useful. Here's what the forensics tell us:

Subnet layout (critical finding):

`10.200.80.50` falls in `snet-lca-uks-prd-system` (10.200.80.0/26), protected by `nsg-lca-uks-prd-system`. No route tables on any subnet—so no UDR blackholing. Good.

NSG summary—all look fine:

- `nsg-lca-uks-prd-system` → has `Allow-AzureLB-Inbound` (priority 110), which should allow health probes from `168.63.129.16`
- `aks-agentpool-31829346-nsg` → has `Allow-NWSDE-Inbound` for `20.68.120.178`
- `nsg-default-fflz-01` → not attached to any subnet (confirmed earlier), so irrelevant

Still missing two pieces. Run these:

The probe metrics will give us a definitive answer. If `average: 0`, the probe is failing and the LB considers `10.200.80.50` dead—meaning it'll never forward traffic regardless of how correct everything else is. If `average: 100`, the probe is passing and the issue is elsewhere (which would be surprising given the current evidence).

---

kubectl get svc -A -o wide | grep 20.90.82.168 ➜ ~ # 1. Route table contents (it exists but may not be attached) az network route-table route list \\ -g rg-vnet-fflz-01 \\ --route-table-name rt-default-fflz \\ -o table # 2. Health probe metrics??? THE key diagnostic az monitor metrics list \\ --resource "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01" \\ --metric "HealthProbeStatus" \\ --interval PT1M \\ -o json | jq '.value\[0\].timeseries\[0\].data\[-5:\] |.\[\] | {timeStamp, average}' # 3. And the actual curl test if you haven't yet curl -v [https://20.90.82.168](https://20.90.82.168/) --insecure -m 10 bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) AddressPrefix HasBgpOverride Name NextHopIpAddress NextHopType ProvisioningState ResourceGroup --------------- ---------------- ------- ------------------ ---------------- ------------------- --------------- 0.0.0.0/0 False default 10.200.0.4 VirtualAppliance Succeeded rg-vnet-fflz-01 bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) ERROR: (BadRequest) Failed to find metric configuration for provider: Microsoft.Network, resource Type: loadBalancers, metric: HealthProbeStatus, Valid metrics: VipAvailability,DipAvailability,ByteCount,PacketCount,SYNCount,SnatConnectionCount,AllocatedSnatPorts,UsedSnatPorts Code: BadRequest Message: Failed to find metric configuration for provider: Microsoft.Network, resource Type: loadBalancers, metric: HealthProbeStatus, Valid metrics: VipAvailability,DipAvailability,ByteCount,PacketCount,SYNCount,SnatConnectionCount,AllocatedSnatPorts,UsedSnatPorts \* Trying 20.90.82.168:443… \* Connection timed out after 10001 milliseconds \* Closing connection 0 curl: (28) Connection timed out after 10001 milliseconds ➜ ~

---

Found it. The route table `rt-default-fflz` has a default route:

That's a firewall or NVA. Although the subnet listing showed `routeTable: null` on the subnets we checked, we need to verify it's not attached to a subnet the AKS nodes use. But more importantly—there's a fundamental architecture problem here.

You can't reliably chain a public Azure LB → internal Azure LB VIP as an IP-based backend. The public LB's health probe (sourced from `168.63.129.16`) needs to TCP-connect to `10.200.80.50:443`. But that's another LB's frontend IP, not a NIC—Azure's health probe infrastructure may not be able to reach it in the same way a VM on the VNet can.

Let's confirm with the correct metric name (it's `DipAvailability`, not `HealthProbeStatus`):

If that shows `average: 0`, the probe is failing and that confirms the LB-to-LB chaining doesn't work.

Also check what `10.200.0.4` is:

If there is a firewall at `10.200.0.4`, the correct architecture for external ingress would typically be: public IP → Azure Firewall (DNAT rule) → internal LB (10.200.80.50). That's a supported pattern and the firewall was likely intended to be the entry point, not the public LB directly.

---

az monitor metrics list \\ --resource "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01" \\ --metric "DipAvailability" \\ --interval PT1M \\ -o json | jq '.value\[0\].timeseries\[0\].data\[-5:\] |.\[\] | {timeStamp, average}' bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) jq: error (at <stdin>:22): Cannot iterate over null (null) Or an NVA/VM? az network nic list --query "\[?ipConfigurations\[?privateIPAddress=='10.200.0.4'\]\].{name:name, rg:resourceGroup, vm:virtualMachine.id}" -o table bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) Preview version of extension is disabled by default for extension installation, enabled for modules without stable versions. Please run 'az config set extension.dynamic\_install\_allow\_preview=true or false' to config it specifically. The command requires the extension azure-firewall. Do you want to install it now? The command will continue to run after the extension is installed. (Y/n): y Run 'az config set extension.use\_dynamic\_install=yes\_without\_prompt' to allow installing extensions without prompt. bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) ➜ ~

---

The metrics returned null—meaning there's likely zero probe data, which confirms the probe has never succeeded. The NIC query didn't return output either. Let's try broader approaches:

bash

```bash
# Raw metrics output (skip jq to see the structure)
az monitor metrics list \
  --resource "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01" \
  --metric "DipAvailability" \
  --interval PT1M \
  -o json | jq '.value[0].timeseries'

# Find what 10.200.0.4 is — check all NICs in the connectivity RG
az network nic list \
  --query "[?ipConfigurations[?privateIPAddress=='10.200.0.4']].{name:name, rg:resourceGroup, vm:virtualMachine.id}" \
  -o table

# Also check if it's a firewall (extension should be installed now)
az network firewall list -o table
\`\`\`

Regardless of those results, the picture is clear enough to call it:

1. The health probe has never passed — the public LB considers \`10.200.80.50\` dead
2. The backend is an internal LB VIP, not a NIC — Azure health probes can't reliably reach another LB's frontend IP
3. There's an NVA/firewall at \`10.200.0.4\` with a \`0.0.0.0/0\` UDR, suggesting the intended inbound path is through that appliance

The likely correct approach is a DNAT rule on the firewall, not LB-to-LB chaining. The pattern would be:
\`\`\`
Internet → Firewall public IP (or 20.90.82.168 routed to FW) 
  → DNAT to 10.200.80.50:443 
    → ingress-nginx
```

Find out what the firewall is (the `az network firewall list` above), and we can check whether it already has a DNAT rule or needs one created. That's the proper fix—the public LB with an IP-based backend pointing at another LB was never going to work for health-probed traffic.

---

az network nic list \\ --query "\[?ipConfigurations\[?privateIPAddress=='10.200.0.4'\]\].{name:name, rg:resourceGroup, vm:virtualMachine.id}" \\ -o table # Also check if it's a firewall (extension should be installed now) az network firewall list -o table bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) \[\] bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8)

---

Both empty—it's not an Azure Firewall and no NIC has that IP. It could be a third-party NVA (like Palo Alto, FortiGate, etc.), or something else entirely. Let's hunt it down:

bash

```bash
# Check all private IPs across all NICs in the subscription
az network nic list \
  --query "[].{name:name, rg:resourceGroup, ips:ipConfigurations[].privateIPAddress}" \
  -o json | jq '.[] | select(.ips[] == "10.200.0.4")'

# Check if it's a private endpoint
az network private-endpoint list \
  --query "[].{name:name, rg:resourceGroup, ips:customDnsConfigs[].ipAddresses}" \
  -o json | jq '.[] | select(.ips[][]? == "10.200.0.4")'

# What subnet is 10.200.0.x in?
az network vnet subnet list \
  -g rg-vnet-fflz-01 \
  --vnet-name vnet-fflz-uks-01 \
  -o json | jq '.[] | select(.addressPrefix | startswith("10.200.0")) | {name, addressPrefix, nsg: .networkSecurityGroup.id}'

# Brute force — find anything with that IP
az resource list \
  --query "[?location=='uksouth']" \
  -o json | jq '.[].id' | head -50
```

The subnet query is the most likely to help—`10.200.0.4` sits in a different /24 from your AKS subnets (`10.200.80.x`), so there's probably a dedicated subnet for the NVA/gateway appliance. Once we know the subnet name, we can identify what's sitting in it.

Also—is this infrastructure managed by someone else (e.g. the LCRCA network team)? The `RG-CONNECTIVITY-FFLZ-01` naming and the route table pattern strongly suggest a hub-spoke or Azure Landing Zone topology, where the connectivity hub (including the NVA) might be managed by a separate team. They'd know what `10.200.0.4` is and whether it already has DNAT rules.

---

Key finding: `10.200.0.4` doesn't exist in this subscription. This is a hub-spoke landing zone—the NVA/firewall lives in a separate hub subscription. But here's the thing: the route table isn't attached to any subnet anyway. All four subnets showed `routeTable: null` earlier. So the UDR isn't actually in the traffic path—it's an orphaned route table.

That rules out routing as the blocker. Which brings us back to the core problem:

The public LB health probe is almost certainly failing because the backend `10.200.80.50` is another load balancer's VIP, not a NIC. Azure LB health probes (from `168.63.129.16`) may not be able to TCP-handshake with an internal LB frontend in this configuration.

Let's confirm once and for all:

If timeseries is empty or null, there's no probe data at all—confirming the probe never passes.

At this point you have three realistic options:

1. Azure Application Gateway—Replace the public LB with an AppGW. AppGW natively supports backend pools pointing at private IPs (including internal LB VIPs) and does its own HTTP/HTTPS health probing. This is the Azure-recommended pattern for public-to-private ingress.
2. DNAT on the hub firewall—If the hub subscription has a firewall/NVA, request a DNAT rule: `20.90.82.168:443 → 10.200.80.50:443`. The firewall can forward to the internal LB VIP because it's a regular VNet-routed connection, not a health-probed LB backend. You'd move the public IP to the firewall or route traffic to it.
3. Point the public LB at AKS nodes directly—Change from an IP-based backend to a NIC-based backend using the AKS VMSS NICs. Change the backend port to 32635 (the NodePort). The health probe would target actual NICs and work. Downside: you're coupling the public LB to the AKS node pool VMSS, which is AKS-managed.

My recommendation: Option 2 is the most architecturally correct for a landing zone pattern. Reach out to whoever manages the hub subscription and ask what the NVA at `10.200.0.4` is and whether they can add a DNAT rule. If that's too slow, Option 3 is the quickest to get traffic flowing today.

---

az monitor metrics list \\ --resource "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01" \\ --metric "DipAvailability" \\ -o json | jq '.value\[0\].timeseries' bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) \[\] ➜ ~

---

Confirmed. Empty timeseries—the probe has never passed a single check. The public LB has been silently dropping all traffic because it considers `10.200.80.50` permanently dead.

The LB-to-LB chaining is the root cause. That's a dead end architecturally.

Given you need this working now, Option 3 (NIC-based backend on AKS nodes) is the fastest path. Here's the step-by-step:

1\. Get the VMSS details for the system node pool:

2\. Remove the current IP-based backend address:

3\. Update the LB rule backend port from 443 to 32635 (the nginx NodePort):

4\. Update the health probe to target the nginx health NodePort (31363):

5\. Associate the VMSS with the backend pool:

A word of caution on step 5: Modifying AKS-managed VMSS directly is supported but can be overwritten by AKS reconciliation (e.g. during upgrades or scaling). For a permanent solution, you'd want this in Terraform or use the AKS node pool's `--node-pool-additional-configs`. But for proving connectivity today, this works.

After step 5, the probe should start hitting the actual node NICs on port 31363. Give it 10-15 seconds, then test:

---

az vmss list \\ -g rg-lca-uks-prd-aks \\ --query "\[\].{name:name, id:id}" -o table bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) Name --------------------------- aks-system-38063810-vmss aks-workflows-84955532-vmss

---

Good—`aks-system-38063810-vmss` is the one you want (that's where ingress-nginx will be scheduled). Proceed with steps 2 through 5:

Run those three first, then we'll do the VMSS association (step 5)—that's the more impactful change so worth confirming the LB config is right before touching the AKS node pool.

---

az network lb address-pool address remove \\ -g RG-CONNECTIVITY-FFLZ-01 \\ --lb-name lb-fflz-uks-public-01 \\ --pool-name bap-fflz-lb-uks-public-01 \\ --name bap-fflz-lb-uks-public-01-ipaddress1 # Step 3: Change backend port to NodePort az network lb rule update \\ -g RG-CONNECTIVITY-FFLZ-01 \\ --lb-name lb-fflz-uks-public-01 \\ --name lb-fflz-uks-public-01-rule1 \\ --backend-port 32635 # Step 4: Probe targets nginx health NodePort az network lb probe update \\ -g RG-CONNECTIVITY-FFLZ-01 \\ --lb-name lb-fflz-uks-public-01 \\ -n probe-https-443 \\ --port 31363 bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) { "backendAddressPool": { "id": "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01/backendAddressPools/bap-fflz-lb-uks-public-01", "resourceGroup": "RG-CONNECTIVITY-FFLZ-01" }, "backendAddressPools": \[{ "id": "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01/backendAddressPools/bap-fflz-lb-uks-public-01", "resourceGroup": "RG-CONNECTIVITY-FFLZ-01" } \], "backendPort": 32635, "disableOutboundSnat": false, "enableFloatingIP": false, "enableTcpReset": false, "etag": "W/\\"29004238-31fb-4f4a-9f80-125e06e86145\\"", "frontendIPConfiguration": { "id": "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01/frontendIPConfigurations/fipcfg-fflz-lb-uks-public-01", "resourceGroup": "RG-CONNECTIVITY-FFLZ-01" }, "frontendPort": 443, "id": "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01/loadBalancingRules/lb-fflz-uks-public-01-rule1", "idleTimeoutInMinutes": 4, "loadDistribution": "Default", "name": "lb-fflz-uks-public-01-rule1", "probe": { "id": "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01/probes/probe-https-443", "resourceGroup": "RG-CONNECTIVITY-FFLZ-01" }, "protocol": "Tcp", "provisioningState": "Succeeded", "resourceGroup": "RG-CONNECTIVITY-FFLZ-01", "type": "Microsoft.Network/loadBalancers/loadBalancingRules" } bash: warning: setlocale: LC\_ALL: cannot change locale (en\_GB.UTF-8) { "etag": "W/\\"d68b5c87-60d4-4c5c-b99a-c8c30cccb4a6\\"", "id": "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01/probes/probe-https-443", "intervalInSeconds": 5, "loadBalancingRules": \[{ "id": "/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01/loadBalancingRules/lb-fflz-uks-public-01-rule1", "resourceGroup": "RG-CONNECTIVITY-FFLZ-01" } \], "name": "probe-https-443", "numberOfProbes": 2, "port": 31363, "probeThreshold": 1, "protocol": "Tcp", "provisioningState": "Succeeded", "resourceGroup": "RG-CONNECTIVITY-FFLZ-01", "type": "Microsoft.Network/loadBalancers/probes" }

---

LB config looks correct—backend port 32635, probe port 31363. Now the VMSS association:

Once that succeeds, apply to existing instances:

Note: The `update-instances` will reimage/update the VMSS instances in-place. It shouldn't restart the nodes, but it may briefly disrupt network connections on each node as the NIC config is applied. If you're concerned, you can apply to individual instance IDs one at a time instead of `"*"`.

---

az vmss update \\ -g rg-lca-uks-prd-aks \\ -n aks-system-38063810-vmss \\ --add virtualMachineProfile.networkProfile.networkInterfaceConfigurations\[0\].ipConfigurations\[0\].loadBalancerBackendAddressPools \\ "{\\"id\\":\\"/subscriptions/d1043e25-5695-4d25-b658-456f3ac3e91e/resourceGroups/RG-CONNECTIVITY-FFLZ-01/providers/Microsoft.Network/loadBalancers/lb-fflz-uks-public-01/backendAddressPools/bap-fflz-lb-uks-public-01\\"}" zsh: no matches found: virtualMachineProfile.networkProfile.networkInterfaceConfigurations\[0\].ipConfigurations\[0\].loadBalancerBackendAddressPools ➜ ~

---

Zsh is treating the square brackets as glob patterns. Escape the path:

Single quotes prevent zsh from expanding `[0]` as a glob.

---

VMSS model updated successfully—both backend pools are now in the config: the original `kubernetes-internal` and the new `lb-fflz-uks-public-01`. Now apply to the running instances:

This updates the NIC config on all 3 nodes. Once it completes, give it 10-15 seconds for the probe to pass, then test:
