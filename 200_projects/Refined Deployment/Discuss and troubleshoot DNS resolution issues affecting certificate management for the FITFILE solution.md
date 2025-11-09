---
aliases: []
confidence: 
created: 2025-10-02T09:32:19Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:10Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [project/work/cuh, topic/technology/networking/dns]
title: Discuss and troubleshoot DNS resolution issues affecting certificate management for the FITFILE solution
type:
uid: 
updated: 
version:
---

Dear all,

Thank you for your time on the call yesterday. It was very helpful to talk through the options and get a clearer understanding of the issues.

**Meeting Purpose**
[Discuss and troubleshoot DNS resolution issues affecting certificate management for the FITFILE solution.](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=13.0)

**Key Takeaways**

- [Current DNS setup is causing conflicts between private and public resolution, preventing proper certificate issuance](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=13.0)
- [All traffic from Azure must route through on-premises infrastructure for security reasons, complicating the solution](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=405.0)
- [Team will investigate options to bypass DNS conflicts while maintaining security requirements](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1823.0)

**Topics**
**Current DNS Configuration Issues**

- [Private DNS zones in both Azure and on-premises are causing conflicts](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=13.0)
- [Certificate manager unable to resolve public DNS records needed for ACME challenge](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=69.0)
- [Traffic routing requirements prevent direct internet access from Azure](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=405.0)

**Proposed Solutions and Challenges**

- [Removing Azure private DNS zone won't solve issue due to similar zone on-premises](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1823.0)
- [Modifying CoreDNS to use on-premises DNS (10.252.154.40) proposed, but may face same conflicts](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1351.0)
- [Exploring options to bypass DNS conflicts:](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1759.0)
- [Standalone DNS server for certificates (not recommended due to complexity)](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1759.0)
- [Potential Netscaler solution to redirect specific DNS queries](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1905.0)

**Security and Networking Constraints**

- [All traffic from Azure must route through on-premises infrastructure and Telefónica firewalls](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=405.0)
- [Direct internet access from Azure subscription not allowed for security reasons](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=405.0)
- [Need to maintain security boundaries while finding DNS resolution solution](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=405.0)

**Certificate Management Options**

- [Preferred: Automated certificate lifecycle management using ACME protocol](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1642.0)
- [Fallback options if DNS issues persist:](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1642.0)
- [Manual certificate provisioning by Telefónica](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1660.0)
- [FITFILE creating certificate chain for manual installation](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1660.0)
- Fallback options are undesirable as they would require more work from both FITFILE and Telefonica

**Next Steps for Investigation**

- FITFILE to update the DNS resolution for the AKS cluster to use CUH on premise DNS resolver.
- FITFILE to remove the unused Azure private DNS zones (done)
- [Telefónica to check Azure Firewall rules with Ahmed](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=2198.0)
- [Explore Netscaler options with Scott and Ryan](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=2198.0)

**Actions**

- [Continue discussion asynchronously via Teams chat](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=2114.0)
- [FITFILE to email CUH and SDE team about potential application downtime during DNS changes](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=2226.0)
- Oyo to send p[laceholder for meeting on Monday at 3:00pm to review progress](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=2571.0)
- [Hold off on existing firewall change request until clear solution is identified](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=2504.0)
- TT to think internally about how traffic can be routed to 1.1.1.1:53 for the [cuh-prod-1.privatelink.fitfile.net](https://cuh-prod-1.privatelink.fitfile.net) DNS01 challenge without resolving locally to the CUH on-premise DNS resolver

 Many thanks.

## FITFILE - Certificate Management Solution RITM0245534 - October 01

[**VIEW RECORDING - 45 mins (No highlights)**](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT)

### Meeting Purpose

[Discuss and troubleshoot DNS resolution issues affecting certificate management for the FITFILE solution.](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=13.0 "PLAY @0:13")

### Key Takeaways

- [Current DNS setup is causing conflicts between private and public resolution, preventing proper certificate issuance](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=13.0 "PLAY @0:13")
- [All traffic from Azure must route through on-premises infrastructure for security reasons, complicating the solution](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=405.0 "PLAY @6:45")
- [Team will investigate options to bypass DNS conflicts while maintaining security requirements](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1823.0 "PLAY @30:23")
- [Potential solutions include modifying CoreDNS configuration or exploring Netscaler options](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1351.0 "PLAY @22:31")

### Topics

#### Current DNS Configuration Issues

- [Private DNS zones in both Azure and on-premises are causing conflicts](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=13.0 "PLAY @0:13")
- [Certificate manager unable to resolve public DNS records needed for ACME challenge](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=69.0 "PLAY @1:09")
- [Traffic routing requirements prevent direct internet access from Azure](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=405.0 "PLAY @6:45")

#### Proposed Solutions and Challenges

- [Removing Azure private DNS zone won't solve issue due to similar zone on-premises](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1823.0 "PLAY @30:23")
- [Modifying CoreDNS to use on-premises DNS (10.252.154.40) proposed, but may face same conflicts](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1351.0 "PLAY @22:31")
- [Exploring options to bypass DNS conflicts:](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1759.0 "PLAY @29:19")
  - [Standalone DNS server for certificates (not recommended due to complexity)](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1759.0 "PLAY @29:19")
  - [Potential Netscaler solution to redirect specific DNS queries](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1905.0 "PLAY @31:45")

#### Security and Networking Constraints

- [All traffic from Azure must route through on-premises infrastructure and Telefónica firewalls](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=405.0 "PLAY @6:45")
- [Direct internet access from Azure subscription not allowed for security reasons](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=405.0 "PLAY @6:45")
- [Need to maintain security boundaries while finding DNS resolution solution](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=405.0 "PLAY @6:45")

#### Certificate Management Options

- [Preferred: Automated certificate lifecycle management using ACME protocol](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1642.0 "PLAY @27:22")
- [Fallback options if DNS issues persist:](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1642.0 "PLAY @27:22")
  - [Manual certificate provisioning by Telefónica](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1660.0 "PLAY @27:40")
  - [Fitfile creating certificate chain for manual installation](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=1660.0 "PLAY @27:40")

#### Next Steps for Investigation

- [Fitfile to modify CoreDNS config to use on-premises DNS IP](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=2166.0 "PLAY @36:06")
- [Remove Azure private link stub zone](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=2166.0 "PLAY @36:06")
- [Telefónica to check Azure Firewall rules with Ahmed](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=2198.0 "PLAY @36:38")
- [Explore Netscaler options with Scott and Ryan](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=2198.0 "PLAY @36:38")

### Next Steps

- [Continue discussion asynchronously via Teams chat](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=2114.0 "PLAY @35:14")
- [Fitfile to email stakeholders about potential application downtime during DNS changes](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=2226.0 "PLAY @37:06")
- [Placeholder meeting set for Monday at 3:00 PM to review progress](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=2571.0 "PLAY @42:51")
- [Hold off on existing firewall change request until clear solution is identified](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=2504.0 "PLAY @41:44")
- [Susannah to send calendar invite for Monday's follow-up meeting](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT?tab=summary&timestamp=2571.0 "PLAY @42:51")

### FITFILE - Certificate Management Solution RITM0245534 - October 01

[**VIEW RECORDING - 45 mins (No highlights)**](https://fathom.video/share/VRxj9zbszVvinQZoe9YYYsnNigq9MpJT)

[@0:00](https://fathom.video/calls/427244928?timestamp=0.0) - **Oliver Rushton**

Link local resolver, so these draws resolver, and using 1.1.1.1, so Cloudflash resolver, that will be directed out of our private network, but through to the on-premise, where there is already a DNS record, you're saying, which loops back.

Yes.

[@0:13](https://fathom.video/calls/427244928?timestamp=13.54) - **Andrew Bell (Telefónica Tech EN)**

So we've got a stub zone called privatelink.fitfile.net, which is where we've got the ear records in for, I think, cuh-poc and cuh-prod-1, which allows the likes of Alexis, when he goes to resolution, it looks to there, points straight down through the express link into that subscription.

I see. But think, from what I gather, then, that's the bit that's kind of causing your certificate issue, because it's trying to do resolve back, and it's coming back, oh, hold on, here it is, they're here, and you're expecting it to be somewhere else.

[@0:47](https://fathom.video/calls/427244928?timestamp=47.3) - **Oliver Rushton**

I thought somebody else also said that traffic on port 53 was blocked outside of the... I think direct external to public, I think...

[@1:00](https://fathom.video/calls/427244928?timestamp=60.032) - **Andrew Bell (Telefónica Tech EN)**

It's it's blocked, and all your traffic comes through to our DNS internal. I could well be wrong.

[@1:09](https://fathom.video/calls/427244928?timestamp=69.332) - **Oliver Rushton**

It's only because when we were running this and looking at the logs of cert manager, we weren't seeing, you know, the logs that suggested it was able to still find the DNS resolver, but there was no text record.

It was saying it was just hanging and then would eventually time out, saying it cannot reach. So it could be both, uh, parts, um, both being a mixture of both, yeah.

[@1:34](https://fathom.video/calls/427244928?timestamp=94.892) - **Andrew Bell (Telefónica Tech EN)**

But if, if you were to come through to our internal, so hypothetically, if, if DNS isn't open from within that, there's a subscription to come through the express link to our DNS servers, and we enabled it, you would, you would still see our stub zone, wouldn't you, for privatelink.fitfile.net.

And it wouldn't have the text entry that you're expecting to get, I'm assuming, for your certificate resolution.

[@1:59](https://fathom.video/calls/427244928?timestamp=119.832) - **Oliver Rushton**

I'm assuming, to to it would resolve it. So it would be a um the text records are under that host name right so they're an even more um limited path or another subdomain on that right aren't they yeah um and you're saying so even even with that they would still be resolved to us yeah uh okay um we were thinking i mean is it possible any way to do away with our dns private dns zone in azure uh just thinking of this as like another solution like we don't actually use it for any of our internal networking we use it i guess so that you guys can forward traffic to that resolver which will then return the ip for the um we shouldn't need that then if you've got that in azure because we've got that on site on on prem exactly so if we could remove it then we wouldn't need to direct our traffic

We could go through the Azure link local which will eventually go out to 1.1.1 and it won't be looking up the, it won't be directed to our private DNS resolver and therefore it will go out to the public internet, will find the correct text record in Cloudflare, I think.

Do we have that, Sean? Have we got an allowance in for that though for that?

[@3:23](https://fathom.video/calls/427244928?timestamp=203.756) - **Andrew Bell (Telefónica Tech EN)**

For the private resolver? Yeah, can the guys go external from that Azure subscription for DNS resolution though? Is it not all locked down that you cannot pass and all that type of thing?

I thought it was locked to the hilt. It's not for DNS traffic as far as we're aware, if we go through the Azure link local, right?

[@3:49](https://fathom.video/calls/427244928?timestamp=229.376) - **Oliver Rushton**

So, because that's not technically leaving the VNet, it's going straight to Azure's DNS resolver, which will then forward it onto other DNS resolvers.

Okay. Because that's how we're able to obtain the certificate for the non-private link domain. Gotcha, yeah.

[@4:08](https://fathom.video/calls/427244928?timestamp=248.308) - **Andrew Bell (Telefónica Tech EN)**

Well, a good way of testing is we don't, that private, if you've got, if there's a stub zone there, you've got for privatelink.fitfile.net, it's currently not being used by Alexis, so I'm going to use it as a reference point, for when he's resolving to point them in.

So we've got, basically, the stub zone, private link.fitfile.net, then we've got three EA records in there, all pointing to 10, 250, 16.7, 16.7.

So there's no C name or anything?

[@4:37](https://fathom.video/calls/427244928?timestamp=277.908) - **Oliver Rushton**

Yeah. Okay, so we don't need it. So we can get rid of it.

[@4:41](https://fathom.video/calls/427244928?timestamp=281.948) - **Andrew Bell (Telefónica Tech EN)**

you could get rid of it, and if that resolves your problem for that, that's a win. That generally might, yes.

[@4:49](https://fathom.video/calls/427244928?timestamp=289.488) - **Oliver Rushton**

Yes, we can probably give that a go today, can't we, Leon, just to see if we clear up that resource, whether the certificate deploys.

Yeah. Okay, it's something to try. It's worth a try. See, if it does, brilliant.

[@5:05](https://fathom.video/calls/427244928?timestamp=305.18) - **Andrew Bell (Telefónica Tech EN)**

If it doesn't, then we'll have to come back to the drawing board, so to speak.

[@5:11](https://fathom.video/calls/427244928?timestamp=311.1) - **Oliver Rushton**

Okay. That sounds good. Is everyone else okay with that? Like Alexis and Oya? It may work. It may. It may also not, but it may.

[@5:27](https://fathom.video/calls/427244928?timestamp=327.8) - **MCKENNA, Alexis (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

So are we, like, does anything need to go out to the internet at all for this? Is there, so do we need to get to, say, a certificate revocation list, which is at a third party, say, the cloud fair?

[@5:45](https://fathom.video/calls/427244928?timestamp=345.62) - **Oliver Rushton**

Well, I don't believe, I mean, so the certificates we're getting are from ACME issuer. They are a trusted certificate authority, and I believe they'll be trusted by default on all of your.

Yeah. So that should be okay. And then in terms of what, you know, what is this, what is the actual routes for the traffic?

Well, it'll be the same as the ones that we're doing for the previous certificate. So the requests over port 53 are actually going through Azure's link local resolver, which will then forward them on to any kind of public, you know, resolvers, DNS resolvers as well, I guess, like, like Cloudflare's or Google's one.

That's, that's how the, the DNS traffic is currently flowing. I don't know whether that's something that's been discussed before.

Okay.

[@6:45](https://fathom.video/calls/427244928?timestamp=405.012) - **MCKENNA, Alexis (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

So I do, the difficulty is that we need all traffic to the Fitfile to come through the trust network via the firewalls and proxies, and then up through the express route.

So we can't have a situation where any traffic is going from the Fitfile. FITFile direct to an external service via Azure.

[@7:07](https://fathom.video/calls/427244928?timestamp=427.864) - **Oliver Rushton**

So not just HTTP traffic? Anything at all.

[@7:13](https://fathom.video/calls/427244928?timestamp=433.464) - **MCKENNA, Alexis (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

So all traffic, anything that goes into or out of that FITFile subscription has got to get there through the Microsoft Express route.

And the difficulty is that we don't have a security boundary in Azure and Azure is unmanaged. So we've got, so Telefónica have got to hold the perimeter.

What does that mean on your side, Andrew and Sean?

[@7:44](https://fathom.video/calls/427244928?timestamp=464.304) - **Andrew Bell (Telefónica Tech EN)**

Where Alexis is saying that so nice and eloquently is kind of like Gandalf, you shall not pass. So theoretically DNS resolution from what you're saying, Alexis, shouldn't be allowed to go out and all DNS traffic has to come in via.

Oh, yeah. As The on-prem DNS service that we have for the trust. Yes. So Azure, the whole Azure resource needs to be seen as kind of like a branch office, if you like.

Because the difficulty is, yeah, because the landings, the whole tenant is unmanaged.

[@8:15](https://fathom.video/calls/427244928?timestamp=495.476) - **MCKENNA, Alexis (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

And if we've got any traffic flow that goes from Azure not through the Telefónica perimeter, then that's something we've got no control over and it's a potential breach.

[@8:30](https://fathom.video/calls/427244928?timestamp=510.616) - **Andrew Bell (Telefónica Tech EN)**

So we can't have that.

[@8:32](https://fathom.video/calls/427244928?timestamp=512.876) - **MCKENNA, Alexis (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

I know it's a bit of a, I mean, it basically puts the whole of Azure environment in something of a backward way.

We're not operating as efficiently and effectively as we could, but that's where we are commercially with our Azure support, which is not.

So any traffic going into that, into any of Azure subscriptions needs to go through that express route and through the Telefónica firewalls and proxy.

[@9:02](https://fathom.video/calls/427244928?timestamp=542.988) - **Oliver Rushton**

I would need to look into this bit more, but I'm not sure that every possible thing could, because obviously some of, when the Kubernetes cluster is talking to other Azure services, that wouldn't be able to necessarily go through on-premise to get there.

I think the way that Azure is necessarily, you know, builds its networking for the internal kind services. So I'm, I'm not sure that all of this can work.

Obviously for the, for this particular DNS request, it could be possible to do it, do the way you're suggesting.

I don't know what has to be done from, from the on-prem side though, because then we'd go back to the similar issue, right?

Of, you would have the same issue that you currently got, because we've got the stub zone, this conflict with what you're expecting.

Exactly. Exactly, yeah.

[@10:05](https://fathom.video/calls/427244928?timestamp=605.48) - **MCKENNA, Alexis (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

So do we have further issues with, say, is this Kubernetes reliant on traffic flows out? Not out, sorry, not out to the internet, but to the Azure APIs.

[@10:21](https://fathom.video/calls/427244928?timestamp=621.04) - **Oliver Rushton**

Hang on, Leon, I might be getting this completely wrong. We've already whitelisted all of the, like, Microsoft APIs, haven't we, and they're all going through.

They all go via the proxy, yeah. Okay, maybe I'm misunderstanding that. So from the, from our cluster. though, but, like, DNS does go through Azure's link local, I'm pretty sure, for everything.

[@10:40](https://fathom.video/calls/427244928?timestamp=640.96) - **Leon Ormes**

Yeah, so it's set up that any IP, so any IPs that are inside the Kubernetes cluster, that's fine. Any that are not, the next hop was originally to that, to Telefónica's firewall.

That didn't work. So now the next, it doesn't. It doesn't go out to the internet. There isn't a route out to the internet, and any traffic that isn't inside our network goes to the proxy server.

That's why we have problems sometimes if we don't no proxy stuff that's actually inside Azure. So those Azure endpoints, they're all in the no proxy list.

Sorry, they're all in the list that the web proxy has. So there isn't any traffic going to the internet.

[@11:28](https://fathom.video/calls/427244928?timestamp=688.312) - **Oliver Rushton**

So just, so A azurelink local i think that's where we are okay and i think the is the azure of the however it's set up the bit that's not in our control does resolve to the internet

[@12:01](https://fathom.video/calls/427244928?timestamp=721.984) - **Leon Ormes**

Let's hope it's not home invasion.

[@12:03](https://fathom.video/calls/427244928?timestamp=723.884) - **Andrew Bell (Telefónica Tech EN)**

I don't know if Alexis is going to wiggle a cable to see if that'll work.

[@12:08](https://fathom.video/calls/427244928?timestamp=728.264) - **Oliver Rushton**

There you go.

[@12:10](https://fathom.video/calls/427244928?timestamp=730.464) - **Andrew Bell (Telefónica Tech EN)**

He's just going to switch it off and on again. That's all we do.

[@12:16](https://fathom.video/calls/427244928?timestamp=736.064) - **Leon Ormes**

This is it. That's all I ever do, to be fair. But it's very possible that this is routing properly, but Telefónica is not allowed, because obviously everything's blocked by default and you have to allow things, that that port 53 and UDP, because it's...

To allow that to come through to our DNS. Well, to go out, because I thought telling the resolver to use the server 1111, to use the server, the Cloudflare server, it wouldn't, your stub wouldn't get in the way.

You're deliberately telling it, go and ask this server as the main server, and so it should be able to, but if Telefónica is blocking...

Just because everything's blocked by default, the port 53 and UDP, then it's just going to get blocked.

[@13:10](https://fathom.video/calls/427244928?timestamp=790.396) - **Andrew Bell (Telefónica Tech EN)**

See, I thought Armored originally set everything up to go to 53 to then, when it comes through, to then hit our DNS load balancer, which then would do the resolution, if we haven't got it cascades at all, it'll be up and gets you off to the internet for DNS.

Yeah. Maybe it hasn't.

[@13:29](https://fathom.video/calls/427244928?timestamp=809.516) - **Leon Ormes**

Or if he hasn't, that protocol might not, he might have overlooked that protocol, or and us saying one, one, one, one, might be being blocked, but that was one of the ones we asked to be unblocked.

[@13:49](https://fathom.video/calls/427244928?timestamp=829.976) - **Andrew Bell (Telefónica Tech EN)**

We're going to have to have a chat with, Sean, need to have a chat with Ahmed to see what he's done for the rules wise then, through the Azure firewall, and see.

If you have, where he's got 53, go on to us, sort of thing.

[@14:03](https://fathom.video/calls/427244928?timestamp=843.708) - **Leon Ormes**

And last time, the problem was that the rule, because they're, they kind of, they're in order, aren't they? So your, your traffic goes through the rules, and the first one will be the one it uses.

[@14:13](https://fathom.video/calls/427244928?timestamp=853.188) - **Andrew Bell (Telefónica Tech EN)**

So maybe that was it again.

[@14:20](https://fathom.video/calls/427244928?timestamp=860.308) - **Leon Ormes**

And also, the other thing is, do, do, can you get logs? Because we can see logs, some logs, but they're more to do with our application logs.

What we can't see is the firewall and the proxy logs.

[@14:32](https://fathom.video/calls/427244928?timestamp=872.448) - **Andrew Bell (Telefónica Tech EN)**

Yeah. So Armored will be able to see the firewall, would have to get somebody from security team, would be able to check the proxy logs to see where you're coming.

Because we've done that once before, I think, just to see what things were getting hit. Just to go through.

So if we can see your, Armored should be able to backtrack and see any requests that have gone through that are getting blocked.

Yeah. On the firewalls. Because like Oli's saying, if they, if it's just timing out, that's usually because the things that, the

[@15:00](https://fathom.video/calls/427244928?timestamp=900.48) - **Leon Ormes**

Any firewalls or any security groups, don't send back saying, oh, no, we're blocking you. They just drop it because obviously it's a security.

If you send back to the hacker, oh, yeah, this service is blocking you, then they've got information.

[@15:12](https://fathom.video/calls/427244928?timestamp=912.08) - **Andrew Bell (Telefónica Tech EN)**

So usually just, so that'd be why it's hanging.

[@15:14](https://fathom.video/calls/427244928?timestamp=914.36) - **Leon Ormes**

We wouldn't know particularly that some rule was blocking it. But we don't, like I say, we don't see the logs, so we can't.

I thought, I'll be honest, I did think he'd sorted out the on-prem DNS, but yeah, I'm going to have go and get a check out with him.

Well, is it, are we doing the split, are we doing the private DNS, but we have to have that one record public, because that's how cert manager works?

[@15:46](https://fathom.video/calls/427244928?timestamp=946.36) - **Oliver Rushton**

Well, yeah, no, that, that, that is exactly what we're trying to achieve, obviously having that record in CLAPA so that we can do the DNS 101 challenge and get a certificate for it.

It has, it has to be there. I may be wrong in. Perhaps the traffic is going not via Azure's resolver and it is actually going outside of the thing.

We need somewhere proving that.

[@16:12](https://fathom.video/calls/427244928?timestamp=972.632) - **Leon Ormes**

There is no, that default route, the 0000 thing is, isn't, normally when you first set up your, your cluster, that is pointing to the internet.

We turn that off. So there's no, there isn't a route to the internet from our cluster.

[@16:26](https://fathom.video/calls/427244928?timestamp=986.852) - **Oliver Rushton**

But I'm unsure on the behaviour of Azure's resolver and how DNS traffic, specifically from the Kubernetes cluster, is directed to that and whether that has different rules over the route table that we defined, which says that yes, all traffic has to go through to the firewall.

I just don't know how we, how we prove it. I mean, because we're not, could we trace with it?

Could you not just.

[@17:01](https://fathom.video/calls/427244928?timestamp=1021.78) - **Andrew Bell (Telefónica Tech EN)**

If you did an NSLOOKUP for an internal server, you would get a response if you're hitting the internal one.

If you're going external, you'd get nothing, wouldn't you? So if I told you an internal server name hypothetically, and you did an NS, you were on command line, did NSLOOKUP for it, and you got a resolution back from it, that would then mean that you could then talk to our internal DNS servers, but if you get basically a thank you, no, it means you'd going external.

Okay, so do you mind if we just try this now?

[@17:30](https://fathom.video/calls/427244928?timestamp=1050.42) - **Oliver Rushton**

I'm just logging into that.

[@17:31](https://fathom.video/calls/427244928?timestamp=1051.28) - **Andrew Bell (Telefónica Tech EN)**

by all means, I was literally just going to say, I'm just going to go, I'll pick a random server.

Okay. Let's have a look.

[@17:39](https://fathom.video/calls/427244928?timestamp=1059.8) - **Oliver Rushton**

I'll pick one just to mesh with Sean a little bit.

[@17:44](https://fathom.video/calls/427244928?timestamp=1064.5) - **Andrew Bell (Telefónica Tech EN)**

Let's have a look. Let's have a look. Two seconds, I'll grab that there. Andy, I just pinged you the Ahmed's firewall rule from the Natin.

[@17:57](https://fathom.video/calls/427244928?timestamp=1077.86) - **Laurence Coleby-Frater (Telefónica Tech EN)**

Oh, no worries. I'll have a shift of that in two seconds for them. Nope. See if you can resolve that box.

[@18:03](https://fathom.video/calls/427244928?timestamp=1083.52) - **Andrew Bell (Telefónica Tech EN)**

Okay. Thank you.

[@18:09](https://fathom.video/calls/427244928?timestamp=1089.94) - **Oliver Rushton**

So we're just connecting to the thing. There we go. So would it matter though I'm on the jump box or I don't know.

I think all traffic is directed. Yeah, they're inside the same. So you want me to NSLOOKUP, was it?

[@18:41](https://fathom.video/calls/427244928?timestamp=1121.06) - **Leon Ormes**

Yeah.

[@18:41](https://fathom.video/calls/427244928?timestamp=1121.58) - **Andrew Bell (Telefónica Tech EN)**

I'm just thinking if we do an NSLOOKUP for that and not even do ping and see what it comes, see if it comes back with anything.

Hopefully it'll come back with a... I'll not find it yet.

[@18:54](https://fathom.video/calls/427244928?timestamp=1134.3) - **Oliver Rushton**

Is it using the... Do I know to be inside of the cluster? Yeah. Thank you, That's what I was thinking.

No, I think it's all the same track.

[@19:03](https://fathom.video/calls/427244928?timestamp=1143.25) - **Leon Ormes**

No, it's all inside the same range.

[@19:09](https://fathom.video/calls/427244928?timestamp=1149.97) - **Oliver Rushton**

But don't forget that Kubernetes has core DNS and core DNS has been configured to root the DNS calls. Differently.

Yeah, let me just... Right, let's try the same thing inside the cluster. Right. So I can't find this, but it's going...

Which is the core DNS IP right now. I don't know. M.2.0.10. Yeah, it's the kubedns. And so we want to look at the resolve comp here.

How do we do, oh, go on, do you go onto the, onto the VM?

[@20:39](https://fathom.video/calls/427244928?timestamp=1239.06) - **Leon Ormes**

The actual node itself.

[@20:40](https://fathom.video/calls/427244928?timestamp=1240.56) - **Oliver Rushton**

The node, yeah. Yeah. Do you remember how to do that? It was like, there's a QTDL debug or something like that, wasn't it?

Oh, yeah. No, don't remember the exact command.

[@20:56](https://fathom.video/calls/427244928?timestamp=1256.06) - **Leon Ormes**

We might be able to find it elsewhere.

[@20:58](https://fathom.video/calls/427244928?timestamp=1258.7) - **Oliver Rushton**

Um. It's the top one. you. Sorry, was it Andrew and Sean, what were you hoping to see from this particular call?

[@21:15](https://fathom.video/calls/427244928?timestamp=1275.33) - **Andrew Bell (Telefónica Tech EN)**

So the idea is if you can get an IP address from that resolution, that means you must be talking to our internal DNS server.

But if you can't resolve it, then I'm going to guess that you're not talking to our internal DNS server, which is it must be going external.

I see.

[@21:30](https://fathom.video/calls/427244928?timestamp=1290.61) - **Oliver Rushton**

This is why we had, yeah, this makes more sense, because when we did this for the database connection, we modified core DNS resolvers, kind of resolve.

[@21:45](https://fathom.video/calls/427244928?timestamp=1305.65) - **Andrew Bell (Telefónica Tech EN)**

Because haven't they got, don't you have a, do you not have like a little stub zone that you've got for net.addenbrook's NHS UK that you've got an ear record in there for?

Yeah, we do. It's, you know, git.

[@21:57](https://fathom.video/calls/427244928?timestamp=1317.05) - **Oliver Rushton**

Let's confirm that. Let's confirm confirm confirm Let's that. Let's Let's that. Let's Kind of mean the thing that you're kind of not going next, you're not coming out to our, our DNS.

[@22:07](https://fathom.video/calls/427244928?timestamp=1327.2) - **Andrew Bell (Telefónica Tech EN)**

I see, I see, okay, so this is called DNS, uh, with a custom.

[@22:17](https://fathom.video/calls/427244928?timestamp=1337.44) - **Oliver Rushton**

Yeah, here's the stuff. Yeah. one.

[@22:22](https://fathom.video/calls/427244928?timestamp=1342.04) - **Andrew Bell (Telefónica Tech EN)**

Okay, if you were coming out to our DNS, then you wouldn't need the stub, would you? Yes, yep, yep, yep.

[@22:29](https://fathom.video/calls/427244928?timestamp=1349.06) - **Oliver Rushton**

This is all making sense. Okay. So we need to figure out how to modify Kubernetes default behavior to not use kubedns, uh, or to somehow configure core DNS to forward all traffic to your DNS.

What, what, what's the, um, what's like the, the, the resolver, like the DNS resolver IP address then? So, so theoretically, the result of his classes at all?

[@23:00](https://fathom.video/calls/427244928?timestamp=1380.74) - **Andrew Bell (Telefónica Tech EN)**

All the way out through our DNS, you should theoretically be able to get to, I'll pop it in chat because it's a lot easier, 10, 252, 154, and I think it should be 40 off the top of my head.

It will be that IP address there you'd get to, and that would be the DNS load balance that we have set up for BC1 while Cambridge.

[@23:25](https://fathom.video/calls/427244928?timestamp=1405.6) - **Oliver Rushton**

OK. But, so we're just saying that if we can figure out, so you're saying this is the IP address for the DNS resolver that's on-premise?

Yeah. OK, fantastic. So, we may have to leave that with us for a bit.

[@23:48](https://fathom.video/calls/427244928?timestamp=1428.74) - **Andrew Bell (Telefónica Tech EN)**

But, theoretically, would you not get hit with the same issue because we've got a stub zone and for private link, you're still back in stage problem.

Exactly.

[@23:57](https://fathom.video/calls/427244928?timestamp=1437.94) - **Oliver Rushton**

Yeah, we would have the same issue. Yeah. Is there a way that you can direct, I don't know, the kind of, I think it's like a different path, like underscore, underscore, underscore, underscore challenge.

Something like that is another subdomain of CUH.1.4. Yeah. So, yeah, so it would be, the first bit dot that, is there a way that you can direct, that traffic, differently?

I, will have to have a think on that one.

[@24:47](https://fathom.video/calls/427244928?timestamp=1487.25) - **Andrew Bell (Telefónica Tech EN)**

I should probably put it, the full thing together.

[@24:56](https://fathom.video/calls/427244928?timestamp=1496.63) - **Oliver Rushton**

Hmm. Oh. Yeah.

[@25:00](https://fathom.video/calls/427244928?timestamp=1500.8) - **Andrew Bell (Telefónica Tech EN)**

Because that's what the guys, see the entries that we've got there, are what they're using for resolution, it's kind of what was, Alexis is using for resolution to send them off down the express to that, but.

[@25:14](https://fathom.video/calls/427244928?timestamp=1514.24) - **MCKENNA, Alexis (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

I've got some instruction here for reconfiguring Kubernetes to point it at an external DNS service, so some of this might help.

Yes. May need a bit, I'm not sure you might be comfortable sort of absorbing it over a period of time, rather than Hacking it out on the call, but.

[@25:35](https://fathom.video/calls/427244928?timestamp=1535.28) - **Oliver Rushton**

Yeah, yeah, I don't think we'll be able to do it on this call necessarily, because it might be stuff we want to do via Terraform, which we're going go through like pipelines and things, but thank you, yeah.

So wait, hang on, where are we?

[@25:53](https://fathom.video/calls/427244928?timestamp=1553.16) - **Andrew Bell (Telefónica Tech EN)**

I just keep thinking everything we do, we're going to end up with a pretty convoluted system. And it can't go to a different on-premise resolver.

[@26:07](https://fathom.video/calls/427244928?timestamp=1567.41) - **Oliver Rushton**

They're all of the same entries. They're all the same, okay. Yeah.

[@26:16](https://fathom.video/calls/427244928?timestamp=1576.85) - **Andrew Bell (Telefónica Tech EN)**

So actually, the only other way to do it, I don't know, you still wouldn't. I mean, could you have a rule which would, I was thinking, could you have a DNS set of, in that subscription, as a DNS server, that then resolves, bypasses us, but goes to the NHS, NHS DNS resolver, the CNS 01, that would buy, that would then bypass our...

There were internal records for that, which would allow it, but it's that then classified as all traffic is coming through, because it would have to come through the data center network per se, and then out.

[@27:20](https://fathom.video/calls/427244928?timestamp=1640.64) - **Oliver Rushton**

Oh, it's a sticky wicket, this one. Yeah, so this was, this was obviously the option, the most desired option, to allow Fitfile to just continuously manage certificate lifecycle, so like we'd always have valid certificates and they would automatically update themselves every x period of time.

If we cannot get this working, then we can fall back to the, one of the other options that we had, which was essentially supplying, you know, either TT supplying certificate, certificates that, you know, on a manual period that we would then, yeah, install into the application, or vice versa, us create.

Making a, you know, certificate chain, you know, giving it a certificate chain for any certificates that we release. They are the fallbacks.

I was gonna say that.

[@28:14](https://fathom.video/calls/427244928?timestamp=1694.0) - **Andrew Bell (Telefónica Tech EN)**

Alexa's gonna love it because you'd need to modify the whole impact assessment for the entire thing if we have to supply certificates.

Really. Is there a means of putting a certificate on a load balancer?

[@28:25](https://fathom.video/calls/427244928?timestamp=1705.24) - **MCKENNA, Alexis (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

I'm not sure where the route to the express route happens to be. Is that, is that, would you, Andy, would you know if it's in the data center?

So could we put a certificate in place and have it, and sit it on the load balancer so that we don't have, we don't need a certificate at all, I suppose, in the Kubernetes cluster?

The traffic just gets passed through.

[@28:46](https://fathom.video/calls/427244928?timestamp=1726.74) - **Andrew Bell (Telefónica Tech EN)**

Yeah. Expressing some campus networks.

[@28:50](https://fathom.video/calls/427244928?timestamp=1730.28) - **Oliver Rushton**

Yeah. Some campus.

[@28:54](https://fathom.video/calls/427244928?timestamp=1734.16) - **Andrew Bell (Telefónica Tech EN)**

And that way, Telefónica can manage it, but they control where it happens to be, so. But that means it will terminate.

[@29:00](https://fathom.video/calls/427244928?timestamp=1740.82) - **Oliver Rushton**

we're Not on the, you know, on the ingress controller. So you won't, you'll have an insecure kind of part of the connection still.

[@29:11](https://fathom.video/calls/427244928?timestamp=1751.21) - **MCKENNA, Alexis (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

Yeah, from the, yeah, okay.

[@29:12](https://fathom.video/calls/427244928?timestamp=1752.97) - **Andrew Bell (Telefónica Tech EN)**

Yeah. Short answer is they kind of need to bypass our DNS for the certificate piece. The ridiculous response is, and the horrible one, which I would not recommend, is we stand up a standalone DNS server that literally is just a fit file for just a certificate that is on premise, which comes in, that doesn't have our full DNS stack on it, and literally just comes in and resolves it.

And chucks it straight out. Um. I know, I wonder, should we, should we get, get the log, get the logs from whatever's happening and see, because they might be something in the logs that could make, makes this clearer, they might not.

[@30:23](https://fathom.video/calls/427244928?timestamp=1823.22) - **Oliver Rushton**

I think Andrew's talking sense, like, in terms of, like, the reason why our current one was failing was because of, you know, the private DNS zone that we have, even though it was you, the DNS traffic was going out through, as yours kind of resolver.

If we make the fixes that we want to make to make sure that all DNS traffic goes out through there, then it's the same problem, because they have the exact same zone on that side.

the exact same, we need to find a way of bypassing, the only way, unfortunately, of doing that is.

[@30:53](https://fathom.video/calls/427244928?timestamp=1853.28) - **Andrew Bell (Telefónica Tech EN)**

It's to have a second, somewhere where it can't see that DNS entry, that's the zone that we've got, so it can't resolve anything.

So where do you need to get to? I'm just wondering, can we do some sort of crazy GSLB something?

We need to get to one of the public resolvers, I guess.

[@31:19](https://fathom.video/calls/427244928?timestamp=1879.75) - **Oliver Rushton**

I think any kind of core public DNS resolver, like 1.1.1.1 or 8.8.8.

[@31:27](https://fathom.video/calls/427244928?timestamp=1887.07) - **Leon Ormes**

Yeah, so in that, in that request, um, whatever you call it, that changed, that we wanted, that's where we want to get that, 1.1.1.1.53.

Hmm.

[@31:38](https://fathom.video/calls/427244928?timestamp=1898.13) - **Oliver Rushton**

Okay.

[@31:45](https://fathom.video/calls/427244928?timestamp=1905.99) - **Andrew Bell (Telefónica Tech EN)**

Unless, could we stand something up on a net scaler that literally does that? You come into that, no entry here, move along, kicks you across to that at the next, is to, we don't host it, host your DNS entry here, move along to that.

Yes. That would work for you. It would, theoretically, would come in onto the campus networks. Need to have a chat with Scott and Ryan probably on that because they deal with all the net scalers.

Just think if we could do some sort of like on the GSLB or something on the side where we've got a DNS zone, we have that in the, on one of the net scalers, and then you use that as a hop, skip, and a jump, so to speak, across.

So then you'd have this configured to speak to that kind of VIP address. It would come in, and then that would pass your S straight out.

[@32:51](https://fathom.video/calls/427244928?timestamp=1971.92) - **Oliver Rushton**

Pathetically, it's possible.

[@32:57](https://fathom.video/calls/427244928?timestamp=1977.36) - **Andrew Bell (Telefónica Tech EN)**

I don't particularly want to stand up a VM just for DNS just for this because that just. Seems a bit, a overkill.

Yeah. And I don't know, I don't know a way that I can get you so you can come into our current DNS, but you can't see these DNS entries.

There's not a magical masking option for it. I'm going to have to go and have a think and have a chat with Scott and Ryan, think, on Netscaler.

See if there's something that we can do on, something that can be possible to get done on there. Yeah.

To alleviate it.

[@33:37](https://fathom.video/calls/427244928?timestamp=2017.28) - **Oliver Rushton**

I just want to, I think I've shared it in the docs as well, but just wanted to see if there was.

Hang on. Yes, sir one challenge. This one. Wanted to see if there's any other configuration options that people have.

going to bring to this section. I'm Yes, yeah, okay. Because what they're saying is obviously to solve the issue that you're having with having the kind of private DNS zone or starboard, if we call it, which resolves that thing, go somewhere else.

And we're saying, we cannot go anywhere else. Yeah, that's the problem, yeah.

[@34:26](https://fathom.video/calls/427244928?timestamp=2066.13) - **Andrew Bell (Telefónica Tech EN)**

Theoretically, you're damned if you do and you're damned if you don't. You get rid of the Fitfile stub zone that you've got.

[@34:30](https://fathom.video/calls/427244928?timestamp=2070.53) - **Oliver Rushton**

Oh, brilliant.

[@34:31](https://fathom.video/calls/427244928?timestamp=2071.81) - **Andrew Bell (Telefónica Tech EN)**

Pass it to us, we've got Fitfile stub zone.

[@34:37](https://fathom.video/calls/427244928?timestamp=2077.11) - **Oliver Rushton**

Frustrating. Just to cut in, Guy at Chaps, because I'm realising that we're going to run out of time as well.

[@34:49](https://fathom.video/calls/427244928?timestamp=2089.65) - **Susannah Thomas (Fitfile)**

Do we want to just take this offline and kind of both parties have a look at, see what other options?

[@34:55](https://fathom.video/calls/427244928?timestamp=2095.21) - **Andrew Bell (Telefónica Tech EN)**

Yeah. Yeah.

[@34:56](https://fathom.video/calls/427244928?timestamp=2096.83) - **Susannah Thomas (Fitfile)**

I'm just wondering whether maybe we slot in a time on. okay. I'm glad I'm Um, Monday afternoon to try and kind of reconvene and see if we've see where we've got to.

Would that make sense to have another chat on Monday afternoon? Does that give us some time to try and have a bit more investigation over the next couple of days?

[@35:14](https://fathom.video/calls/427244928?timestamp=2114.4) - **Oliver Rushton**

Uh, I mean, I don't know, obviously, whether this works for you guys, but if we could have some open channel that we could obviously just bounce around ideas in, um, that means we wouldn't have to just wait a long period of time before we next get together.

Obviously, no requirements on having to respond within a certain time or anything like that, but just being able to, like, at least send people, you know, asynchronously and have that good conversation, it could be quite useful.

Yeah. Do you want to do that on Teams?

[@35:47](https://fathom.video/calls/427244928?timestamp=2147.02) - **Andrew Bell (Telefónica Tech EN)**

I've got Sean on Teams, haven't you?

[@35:49](https://fathom.video/calls/427244928?timestamp=2149.36) - **Oliver Rushton**

I love how I'm nominating him.

**ACTION ITEM: Modify CoreDNS config - direct DNS traffic to 10.252.154.40 - [WATCH](https://fathom.video/calls/427244928?timestamp=2155.9999)**

[@35:51](https://fathom.video/calls/427244928?timestamp=2151.0) - **Andrew Bell (Telefónica Tech EN)**

There we go. Yeah, I've got, I've got Leon on Teams anyway, so. Yeah. Yeah. And Sean has always been very quick on responding, so.

[@35:59](https://fathom.video/calls/427244928?timestamp=2159.02) - **Leon Ormes**

Oh, there you go. go. You That was my assessment.

[@36:04](https://fathom.video/calls/427244928?timestamp=2164.17) - **Oliver Rushton**

Okay. But just in terms of, like, action points for us, something that Fitfile will work on now is the, you know, change to the core DNS config to ensure that all DNS traffic goes through, goes to that IP that you've sent in the chat.

**ACTION ITEM: Remove private link stub zone in Azure - [WATCH](https://fathom.video/calls/427244928?timestamp=2178.9999)**

**ACTION ITEM: Discuss DNS setup w/ Ahmed - ensure proper Azure Firewall config - [WATCH](https://fathom.video/calls/427244928?timestamp=2187.9999)**

So we'll do that in the meantime anyway. No worries.

[@36:29](https://fathom.video/calls/427244928?timestamp=2189.95) - **Andrew Bell (Telefónica Tech EN)**

And you'll able to get rid of your private link stub zone as well, yeah. Yeah, if we're not, we're not using it to a while, we say.

[@36:37](https://fathom.video/calls/427244928?timestamp=2197.05) - **Oliver Rushton**

Yeah, we'll get rid of them.

[@36:38](https://fathom.video/calls/427244928?timestamp=2198.27) - **Andrew Bell (Telefónica Tech EN)**

And then, Sean and I, we're going to go and have a chat with Ahmed first of all, just to make sure that the DNS is through the fight from the Azure Firewalls that we've got to come through, make sure that's all set up okay for that, and we're going to hit the same issue.

**ACTION ITEM: Consult Scott/Ryan - NetScaler use for DNS resolution workaround - [WATCH](https://fathom.video/calls/427244928?timestamp=2202.9999)**

But at least that's step one. And then step two is we'll have a word with Scott and Ryan about see if we can utilize the net scalers or something to try and...

... ... ... Pulsome jiggery-pogry.

[@37:04](https://fathom.video/calls/427244928?timestamp=2224.62) - **Oliver Rushton**

That sounds great. Also, Alexis, just want let you know, when we make this change for the DNS stuff, we may experience, you know, issues in the application.

So it may be that we have some downtime when we're messing around with the networking we finally thought was working.

Okay, sure, that's fine.

[@37:26](https://fathom.video/calls/427244928?timestamp=2246.6) - **MCKENNA, Alexis (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

So if I communicate with Waikyeong and just tell him where we're at, I'll ask him what he's doing, because I know that there's, I know that Jakob and people have been playing around, but I'm not sure whether they're doing much of substance or whether they're just tinkering.

**ACTION ITEM: Email re potential app downtime during DNS changes - [WATCH](https://fathom.video/calls/427244928?timestamp=2265.9999)**

So if we can just make them aware ahead of some likely downtime, that might be, that may be handy.

[@37:56](https://fathom.video/calls/427244928?timestamp=2276.02) - **Oliver Rushton**

Sure thing, I can send out an email and then when somebody replies and okays it, then we'll start the work.

Yeah, trouble at all. That's fine.

[@38:04](https://fathom.video/calls/427244928?timestamp=2284.8) - **MCKENNA, Alexis (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

By the way, just for information, I'm away next week and the first two days of the week after, so I'm out until the 15th.

That's abuse for interest or not. Can I just also – okay, thanks, Lawrence.

[@38:22](https://fathom.video/calls/427244928?timestamp=2302.96) - **Susannah Thomas (Fitfile)**

Are you away the whole of next week, Lawrence, as well?

[@38:26](https://fathom.video/calls/427244928?timestamp=2306.04) - **Laurence Coleby-Frater (Telefónica Tech EN)**

Yeah, I'm sending Michael to help with this project whilst I'm off just because of the situation that it's in, so Oyo knows Michael, and she can forward any emails and bring him on to any calls.

Okay, brilliant. Sean knows the schedule as well.

[@38:47](https://fathom.video/calls/427244928?timestamp=2327.92) - **Susannah Thomas (Fitfile)**

The only other thing that we've got, I think, to resolve is just that IP address that – regarding the Grafana cloud updates, and I think the last thing was that it needs to go to

C-U-H-I-G for approval, and that's where it is, isn't it? think you said, Oyoye? Yeah, Laurence confirmed that it's written, IG for approval.

[@39:11](https://fathom.video/calls/427244928?timestamp=2351.31) - **UDOH, Oyovwike (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

Well, can I just check, how urgent is that? Because looking at the emails, I think I understood from the emails that it's something that can go through the normal change process and is not urgent, and it was raised on Friday, or it was, yeah, I think the email sent was on Friday, meaning it should go to CAB this week, and maybe implementation later this week, or next week.

Yeah, so just checking out, Jen, because I know, Susanna, you were saying you want it implemented by the end of this week.

[@39:42](https://fathom.video/calls/427244928?timestamp=2382.93) - **Susannah Thomas (Fitfile)**

Well, was, it was more, I mean, I know that there's just aspects, but I think probably just in terms of invoicing, I think, that everyone's waiting on.

That's the only, that's the, I know that that's outstanding. only thing, based on, I think, Telefonica's side, and also on ours as well.

But, But, yeah, I mean, it doesn't need to kind of, you know, be escalated in terms of the approval process.

Okay.

[@40:08](https://fathom.video/calls/427244928?timestamp=2408.6) - **UDOH, Oyovwike (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

It can go through those normal approvals. Yeah. So, yeah, it may take a while because we've been informed that the IGE team, they're short of staff now, so they're not responding to requests, or maybe they're just dealing with urgent requests.

[@40:36](https://fathom.video/calls/427244928?timestamp=2436.6) - **Susannah Thomas (Fitfile)**

They're trying to have to be, in a earlier about making downtime to the application, is that just like.

[@41:01](https://fathom.video/calls/427244928?timestamp=2461.31) - **Laurence Coleby-Frater (Telefónica Tech EN)**

The fitfile environment, because I know there's linkages to Jakob systems, and the only thing I would just want to just double check is that if, like, Jakob systems go down, his servers are live, and they would, like, cause incidents and stuff for our desk.

[@41:21](https://fathom.video/calls/427244928?timestamp=2481.75) - **Oliver Rushton**

So I just wanted to just double check. We can't possibly do anything to bring his systems down, which are, I think, on premise and things.

So we're just talking about the Azure virtual network. That's right, I just was getting worried there for a second.

[@41:38](https://fathom.video/calls/427244928?timestamp=2498.75) - **Laurence Coleby-Frater (Telefónica Tech EN)**

I don't want people ringing me. Can I just check quickly?

[@41:44](https://fathom.video/calls/427244928?timestamp=2504.09) - **UDOH, Oyovwike (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

So the request Alexis raised, do we need to cancel that, or is it still going ahead? So the firewall request open, is it port 53?

So based on today's discussion, is that still going?

[@41:58](https://fathom.video/calls/427244928?timestamp=2518.01) - **Laurence Coleby-Frater (Telefónica Tech EN)**

Andy would probably jump in. I think Andy said it wouldn't... where are the Thank Fix it. It is still open.

Do you want, do you want me to cancel it for you guys? Is it going to actually do anything, Andy?

It wouldn't do anything at the moment. I would just hold off just until we can identify exactly what we want to get done to kind of get this fixed.

[@42:15](https://fathom.video/calls/427244928?timestamp=2535.72) - **Andrew Bell (Telefónica Tech EN)**

And then we can put a nice clear one together rather than just putting in a bit here and a bit there.

Yeah, makes sense.

[@42:27](https://fathom.video/calls/427244928?timestamp=2547.88) - **Susannah Thomas (Fitfile)**

And so if we, if we communicate on Teams, did we want to meet up on and have another quick chat on Monday or just let's just see how things go on Teams over the next couple of days?

[@42:42](https://fathom.video/calls/427244928?timestamp=2562.0) - **Oliver Rushton**

Yeah, it'd be good to maybe have a placeholder just in case we do need to be like, have a finalised, you know, proper discussion to really agree.

But yeah, we'll also just be checking Teams.

[@42:51](https://fathom.video/calls/427244928?timestamp=2571.58) - **Susannah Thomas (Fitfile)**

Okay, so just briefly with, whilst we've got everyone on the call, if we can check diaries quickly with everyone.

Does 2.30 or 3 o'clock work at all on Monday? Or four? Any time, really, I think, from our diaries after 2.30.

Yeah, that's good for me.

[@43:16](https://fathom.video/calls/427244928?timestamp=2596.22) - **Laurence Coleby-Frater (Telefónica Tech EN)**

Michael's free. I was going to say, what time is it? Is it three o'clock, TCR 3.30?

[@43:22](https://fathom.video/calls/427244928?timestamp=2602.0) - **Andrew Bell (Telefónica Tech EN)**

I've got stuff at four o'clock, but I'm going to be on site. Well, we can do any time from 2.30.

So, I'm free at three o'clock. Okay. Alexis, does that work for you as well? I'm out next week. Oh, yes, you are.

Sorry.

**ACTION ITEM: Send cal invite - Mon 3pm mtg - [WATCH](https://fathom.video/calls/427244928?timestamp=2619.9999)**

[@43:39](https://fathom.video/calls/427244928?timestamp=2619.32) - **Susannah Thomas (Fitfile)**

You're away. Okay. That's fine.

[@43:42](https://fathom.video/calls/427244928?timestamp=2622.62) - **Andrew Bell (Telefónica Tech EN)**

All right. Well, let's put in a quick half an hour at three o'clock on Monday as a placeholder.

[@43:49](https://fathom.video/calls/427244928?timestamp=2629.66) - **Susannah Thomas (Fitfile)**

Okay. I can send out an invite for that.

[@43:51](https://fathom.video/calls/427244928?timestamp=2631.98) - **UDOH, Oyovwike (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

And also, you just mentioned that I'm off from the 13th to the 15th of October. So, Alexis and I will be off then.

right. So I'm not sure, oh, you can, it's term that maybe you can send an email to if there are any issues.

[@44:15](https://fathom.video/calls/427244928?timestamp=2655.73) - **Oliver Rushton**

Well, I'll cover for you from the PM side. yeah, okay, you'll be back then.

[@44:20](https://fathom.video/calls/427244928?timestamp=2660.73) - **Laurence Coleby-Frater (Telefónica Tech EN)**

Yeah, I'm only off for the 10th. Just last week, okay. Thank you.

[@44:31](https://fathom.video/calls/427244928?timestamp=2671.67) - **Oliver Rushton**

Okay, great.

[@44:32](https://fathom.video/calls/427244928?timestamp=2672.91) - **UDOH, Oyovwike (CAMBRIDGE UNIVERSITY HOSPITALS NHS FOUNDATION TRUST) (Nhs)**

All right. Thanks so much, everyone.

[@44:35](https://fathom.video/calls/427244928?timestamp=2675.15) - **Susannah Thomas (Fitfile)**

Useful chat. Good to talk about it at this because we, at least we, we know that what we were proposing to do wasn't necessarily going to be the right solution, so it's good to have a chat about it.

[@44:45](https://fathom.video/calls/427244928?timestamp=2685.33) - **Oliver Rushton**

Hi Susannah, Just an update on CUH cert work:

- I have removed the unused private DNS zone, and the previous pending DNS01 challenge to obtain the certificates has passed. So we have certificates until end of November installed in the node.
- I have also implemented the work to get `[cuh-prod-1.privatelink.fitfile.net](http://cuh-prod-1.privatelink.fitfile.net/)` hostname plugged in to our ingress controller - so that should work and be secure for CUH users.
- TT have come back with a proposed solution which will permit our DNS traffic specifically for the DNS01 challenge from cert-manager to be routed to 1.1.1.1:53 without the need to go through CUH on prem. They asked for some more information which we have provided, so they are going to continue to scope the work.
- In the meantime, I tested whether we can direct all our DNS traffic to their on premise DNS resolver, however, we cannot reach the IP address of the DNS server they provided us in our last call. So we still cannot route all the other DNS traffic through their premise. We have notified laurence of this, and are now awaiting his response.

![white_tick](https://a.slack-edge.com/production-standard-emoji-assets/14.0/apple-small/2705@2x.png)![eyes](https://a.slack-edge.com/production-standard-emoji-assets/14.0/apple-small/1f440@2x.png)![raised_hands](https://a.slack-edge.com/production-standard-emoji-assets/14.0/apple-small/1f64c@2x.png)

[17:10](https://fitfile.slack.com/archives/C07LS99JZLK/p1759421445201749)

So in conclusion, we've done all we can our side

![white_tick](https://a.slack-edge.com/production-standard-emoji-assets/14.0/apple-small/2705@2x.png)![eyes](https://a.slack-edge.com/production-standard-emoji-assets/14.0/apple-small/1f440@2x.png)![raised_hands](https://a.slack-edge.com/production-standard-emoji-assets/14.0/apple-small/1f64c@2x.png)

![](https://ca.slack-edge.com/T01FHF0A4P6-U07HX5WQ6RY-737915d7cda4-48)

Susannah Thomas  [17:24](https://fitfile.slack.com/archives/C07LS99JZLK/p1759422283172959)

Hi Ollie,  Thanks very much - good to hear.Is everything back up and running on the SDE Node?  I asked Laura a little while ago to ask Mag to check and try running queries again. Haven't heard anything back as yet so assuming no news is good news!

![white_tick](https://a.slack-edge.com/production-standard-emoji-assets/14.0/apple-small/2705@2x.png)![eyes](https://a.slack-edge.com/production-standard-emoji-assets/14.0/apple-small/1f440@2x.png)![raised_hands](https://a.slack-edge.com/production-standard-emoji-assets/14.0/apple-small/1f64c@2x.png)

![](https://ca.slack-edge.com/T01FHF0A4P6-U02NE8C2HJB-g349956c797c-48)

Ollie Rushton  [17:37](https://fitfile.slack.com/archives/C07LS99JZLK/p1759423032936809)

Yes we fixed it around 11:30am
