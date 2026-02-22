# Zero trust security whitepaper

![rw-book-cover](https://www.pexip.com/hubfs/downloadable-assets/guides/secure-spaces/zero-trust/ZT-thumbnail.png)

## Metadata
- Author: [[pexip.com]]
- Full Title: Zero trust security whitepaper
- Category: #articles
- Summary: Zero trust security means never trusting any user or system by default and always verifying access to data. It focuses on protecting data through strict policies rather than relying on network boundaries or zones. This approach assumes attackers may already be inside and limits damage by tightly controlling who can access what.
- URL: https://share.google/2JTs8NqzdmBD3pmTn

## Full Document
![Zero Trust guide cover](https://www.pexip.com/hubfs/downloadable-assets/guides/secure-spaces/zero-trust/ZT-ebook-Cover.svg?noresize) 
#### What is zero trust?

As you build your zero trust program, it is critical to understand that zero trust is neither a technology nor a process, and it cannot be achieved by simply implementing a given product suite. Instead, a true zero trust approach prioritizes data over hardware, shifting the security architecture paradigm from networks to policy. Zero trust means that networks, components, and systems do not inherently provide security, instead they are tools that may or may not be beneficial depending on how they are deployed. Instead of relying on logically (or physically) separated zones and domains for data access control, zero trust enables organizations and data owners to share information across domains, or even in the absence of domains, all while enforcing strict information access policy under the principle of “never trust, always verify”.

In a true zero trust architecture, all data is theoretically accessible from a technical perspective but is strictly limited in access based on a centralized governing policy. Zero trust architecture impacts all levels of the Open Systems Interconnect (OSI) model, from physical access through application permissions and even beyond, into the area of human/manual activities. Policy, as implemented by zero trust architecture systems and components, controls and executes all data requests, whether synchronous or asynchronous, momentary or perpetual, X or Y, based on predetermined access rules. While this initially may sound like an unwanted new constriction on how we all do business, zero trust instead offers exciting new possibilities in areas of data collaboration that have previously been either impossible or extremely complicated to achieve.

#### “To a shower of gold most things are penetrable.”

###### - Thomas Carlyle,*The French Revolution, A History,* Ch 1.3.VII

The legacy approach to cybersecurity is based on the notion that attacks come from “outside,” while everything that needs to be protected should be “inside”. Cybersecurity historically focused on defining and defending the **perimeter**, by which we mean the boundary between the known and the unknown, or, operationally, what you control within your network vs. what you don’t control, such as the Internet or another organization’s infrastructure. After all, you lock the doors of your house to keep bad things out and your family safe – so from the outset, it makes sense that your network should be the same. Even the terms associated with networks (e.g., firewalls, demilitarized zones, gateways, gatekeepers) imply that there is a right side and wrong side of the network boundary, with our precious systems and data surrounded by barriers that keep it all safe.

![Traditional-security-assumes that-internal-systems-are-less-risky-than-external-ones](https://www.pexip.com/hubfs/downloadable-assets/guides/secure-spaces/zero-trust/Traditional-security-assumes%20that-internal-systems-are-less-risky-than-external-ones.svg)Traditional-security-assumes that-internal-systems-are-less-risky-than-external-ones
Under this perceived threat model, legacy network architecture assigns devices (and the data they carry) to logical zones, or data enclaves, within the networks you control. We have many terms for these – Virtual Local Area Networks (VLANs), Virtual Routing and Forwarding (VRFs), Virtual Networks (VNETs), Security Groups (SGs), Access Control Lists (ACLs) – which all ultimately operate in the same way: some traffic is allowed in, and some is not. While that works well in theory, the key weakness in the perimeter-centric model is that *wi*thin each enclave, all data and users are considered equivalent – and that’s where things fall apart.

The weakness of these setups lies in the inherent assumption that all systems within each enclave are equally protected simply by benefit of their location in the architecture. The structural vulnerability within this approach is exposed when – not if – a given internal system becomes compromised. If all other systems within that same zone assume that all others are “safe,” then one compromised component becomes the foothold for other attacks within that same zone. This is known as “East-West” penetration, also referred to as **lateral movement**.

It’s important to recognize that critical systems themselves are rarely the first target of an attack; rather, a lesser system, more easily impacted, falls victim to a traditional “North-South,” or boundary, attack, which then gives the attackers a base of operations within the existing logical zone. The initial beachhead may not even be under your control. In one well-known example, the primary impact of the 2020 [Solarwinds attack](https://www.techtarget.com/whatis/feature/SolarWinds-hack-explained-Everything-you-need-to-know) was not on the company, but on the customers who used their compromised software.

There are two main problems with the traditional perimeter-centric network approach from a security perspective:

First, if we focus all our resources on establishing external barriers while ignoring similar protections internally, then it only takes one crack in the dyke for our data protection levee to break.

Second, it turns out that blithely ignoring half of each public network transaction – for example, assuming all outbound traffic is valid – essentially guarantees that when your system is breached, the bad guys will have free reign to do whatever they want … in many cases, without you even knowing that they’re doing it. Such “insider threats” have proven extremely difficult to combat under traditional network security concepts – think of phishing and social media attacks, for example.

By focusing so much energy on reinforcing the perimeter, cybersecurity architects over the years have committed two cardinal sins. For one, we haven’t achieved the actual core objective of protecting our data’s [confidentiality, integrity, and availability](https://www.pexip.com/blog1.0/video-meeting-encryption-in-the-pexip-ecosystem) (the “C-I-A Triad”). Additionally, and perhaps even more critically, this approach has made legitimate cross-boundary uses much harder to implement, especially for video collaboration traffic.

Communications engineers have endured this environment for decades, and we have all experienced its negative operational impacts. Up until now, however, we have all been led to believe that perimeter data restrictions are necessary structural limitations in service of the greater good of protecting the network.

This is a fundamentally false assumption.

![Boundary-penetrations-light](https://www.pexip.com/hubfs/downloadable-assets/guides/secure-spaces/zero-trust/Boundary-penetrations-light.svg)
#### “You must unlearn what you have learned.”

Let’s reflect for a minute.

How do you interact with the world today? Mobile apps, websites, social media, corporate intranets – almost everything you do is online. And being online means that your data is being transmitted, processed, and stored … *somewhere*. It’s exceedingly rare these days for any organization to have all its data hosted on internally owned and provisioned servers. Realistically, at any one point in time, your data could be anywhere on the globe.

In that context, what does it even mean to have an “outside” and an “inside” when data moves between people, systems, services, and organizations on an hourly basis? With globally integrated microservices, a single application may pull data from dozens or even hundreds of different sources. How do you define a perimeter in that circumstance?

To put it another way, do perimeters still matter?

The key is to protect your data. That’s what you care about. In a cloud-based world, where your data can be anywhere at any time, zonal trust is an outdated concept. The fact is, if you are defending the perimeter, you must be right all the time, every time – but the attackers have hundreds of thousands of chances to be right, and they only need one. Furthermore, the main attack threats come from the inside of your organization anyway, which you basically can’t defend under perimeter-centric security. Those are long odds on which to build your entire network security plan.

Secondly, it’s worth considering that the notion of “trust” is outdated and dangerous. Fundamentally, trust is a human concept. Machines do not have any notion of trust. If a user is assigned a set of permissions, the machine will let them do what it’s been instructed to allow them to do. The machine doesn’t know if it’s in a DMZ, on the public internet, or in a highly secured government facility. Machines only ever follow instructions. That’s what they’re made to do.

Zero trust assumes, point blank, that the bad guys are already in your network. Even if they aren’t inside, it’s just because they haven’t gotten around to you yet. This is anathema to traditional security architecture, which, after all, is built on the notion of keeping “Them” out. If They are already here, haven’t we already failed?

Well…not exactly.

You see, if what we care about is *data*, then what really matters is *whether that data has been compromised*. The network is almost irrelevant in that regard. The impact of a breach is not about how the bad guys got in, but what data they were able to see and **exfiltrate**, or export, while they were there. You can, and will, live with inbound breaches under Zero trust, because they will essentially have no impact on your operations. That’s the beauty of zero trust.

It sounds amazing, but how is it possible?

###### - Earl of Gloucester, *King Lear*, Act II Scene I

Fundamentally, zero trust works on the concept of deny-by-default. Permissions are only ever explicitly granted, so that only authorized transactions may occur.

The first building block that zero trust uses to implement this methodology is known asmicrosegmentation. Instead of assuming that all traffic is valid within a given network segment, microsegmentation implements ... [[Dowload full whitepaper to continue reading]](https://www.pexip.com/whitepaper/optimizing-your-zero-trust-security?&utm_term=&utm_campaign=UKI_PMAX_GA&utm_source=google&utm_medium=cpc&utm_content=-dm_pcrid__pkw__pmt__slid__pgrid__ptaid__&hsa_acc=8142768401&hsa_cam=21038459185&hsa_grp=&hsa_ad=&hsa_src=&hsa_tgt=&hsa_kw=&hsa_mt=&hsa_net=adwords&hsa_ver=3&gad_source=1&gad_campaignid=21028326600&gclid=CjwKCAjwqKzEBhANEiwAeQaPVW3S1M__XChY5P4qgQg-2Zigef19SFqQ-e2ykJcnfWu8l8UCRlVyMhoC2C4QAvD_BwE#continue-reading)

![Zero-Trust-building-blocks](https://www.pexip.com/hubfs/downloadable-assets/guides/secure-spaces/zero-trust/Zero-Trust-building-blocks.svg)
Joel advocates on behalf of enterprise users in the areas of application security, secure system design, risk management, policy development, and framework compliance. He has over 25 years of experience designing, implementing, and sustaining video and broadcast networks in security-conscious environments such as government/military, healthcare, and financial services. He holds CISSP and CCSP certifications from (ISC)2.
