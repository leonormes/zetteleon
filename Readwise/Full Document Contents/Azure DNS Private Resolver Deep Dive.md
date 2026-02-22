# Azure DNS Private Resolver Deep Dive

![rw-book-cover](https://i.ytimg.com/vi/V8ChsYAyxTc/maxresdefault.jpg)

## Metadata
- Author: [[John Savill's Technical Training]]
- Full Title: Azure DNS Private Resolver Deep Dive
- Category: #articles
- Summary: Azure DNS Private Resolver lets you connect Azure DNS with your own DNS servers using inbound and outbound endpoints. Inbound endpoints let your DNS servers receive queries from Azure DNS, while outbound endpoints allow Azure DNS to forward queries to your DNS servers. This setup helps manage DNS resolution across virtual networks and on-premises environments easily.
- URL: https://www.youtube.com/watch?v=V8ChsYAyxTc

## Full Document
Hey everyone, in this video I want totalk about the Azure DNS PrivateResolver capability, solving a number ofchallenges we had in the past aboutresolving Azure Private DNS zones fromour own DNS servers,and forwarding fromAzure DNS to our DNS servers. So we'regoing to address both of thosechallenges. As always, a like andsubscribe is appreciated. So take a stepback.

If I think about in Azure, we have theidea of a virtual network.So I have my VNet,and for resources that deploy into myvirtual network,we have the nice Azure DNS service thatis used by default.Now, the way we can communicate to thatis there is an IP address to everyvirtual network; it's always this168.63.129.16.

So from within a virtual network,if Italk to this IP address,it's actually going to go and talk toAzure DNS, this just built-in native DNSservice.And one of the things we commonly doWe create Azure private DNS zonesso I can create these as resources.

This private DNS zonecould be some custom name that I'mcreating,like x.net, whatever that is. Then Ihave various records that are supportedwithin there.Or maybe it's part of private link;it's something.private.blob.core.windows.net, all the otherservices.

Azure is automatically going to publishrecords into there as it creates privateendpoints into our virtual network.Of course, DNS is a core part of privatelink functioning.What I can do is when I createthose private DNS zones,I link themto one or more virtual networks.When I query Azure DNS,because it's linked to that VNet,it will now resolvenames that are part of that.

So all is well, all is happy. If I'msitting within that virtual network, I'msitting in Azure; all is good.What about, though, if I have my ownCustom DNS, as well as maybe running ActiveDirectory Domain Controllers, and I haveDNS running on those.

Well, if that DNS server — that custom DNS— is running in Azure,it’s really not that bad,because I could change the VNet to usecustom DNS and point to the IP addressof whatever this was.Then it could forwardto 168.63.129.16 for all the things that AzureDNS knows about, like my private DNSzones, so that’s a very simple solution.

Because it lives in Azure, it can talkto this address. So, I can either do justforwarding; I could do conditionalforwarding. All is well.But what if that’s not my scenario?What if instead my scenario is, "Hey, I’mon-premises?"So, I have some on-premises environment,and I've got some DNS here,which again has its own IP address inthis network,and it has certain zones that it isauthoritative for.Now I’ve connected these together;there’s some connection between these.

Networks, this is going to be the casefor all the things we talk about.This connection could be a sitesite-to-site VPN. It could be apoint-to-site VPN; that’s probably notlikely.Could be ExpressRoute private peering.Basically, I’m enabling IP routing and apath between my on-premises network andAzure.

But I can’t forward to 168.63.129.16;it’s a special address that only existsin the VNet. So if I wanted to have acustom DNS to resolve records in myAzure private DNS zones that were linkedto the VNet,I have to deploy something extra.

I have to deploy, for example,a DNS forwarder,which has an IP address,and then I configure my DNSto either conditionally forward orforwardto this, and then it can then talk to the168.63because it’s sitting in the virtualnetwork. So there were ways to solve it,but it was kind of ugly. I’m having tomaintain these various things.

And then maybe it’s the inverse.

What if I wanted to use Azure DNSbut I did have some zones that werehosted on my own DNS servers that Iwanted this to be. Until 4.2, there wasreallyno way to achieve that.So what we're going to look at now isthis Azure DNS private resolverthat solves both of these challenges.

So what we're going to think about isthis new type of resource, and it'sactually multiple new types of resources.As we go through this, we'll create one in theportal. So if I were to jump over to theportal super quickly, this is specialbecause it’s in preview as I’m recordingthis.But we have this new DNS privateresolver, and I’m going to go ahead andcreate a new one.

So what we see straight away is, okay, Ihave to create it in a resource group.I've done this before, and I deleted it,so my DNS folder resource groupI give it a name. This is a regionalresource, so this is my South Central DNSresolver.It lives in South Central, so it'sgetting deployed into a specific region.

And then it gets deployed basically intoa virtual network. So I'm going to use myVNet; it has to be in the same regionin South Central.So it's its own object. Now, the firstthing we have the option of doingis adding an inbound endpoint. So I'mgoing to say, okay, this is myinbound—myBD DNS. You can see I've already donethis before.So I'm just going to reuse the same oneI did before:Private DNS endpoint. Now, it binds toa subnet.And if I hit save, so I'm creating aninbound endpoint. So let's think aboutwhat we're doing so far.

So the thing we're doing is we're going tocreate this new type of resource.So we're deployingan object;it's a resource, a privateresolver,which is an Azure DNS private resolver.And these are all regional, so a keything to think about is the VNetand the other things we do.Make it a little bit bigger. These areRegional, I cannot span regions with thistoday. So, these are regional; they're allin the same region.

So I'm going to create this privateresolver resource now. In the portal, it's actuallygoing to go ahead and create a bunch ofdifferent resources for me. If I wasdoing it for a template or PowerShell,I'm creating each of them individually.

So the first thing it wants is aninbound endpoint,so I have to have a dedicated subnet.That's an important point here. So I'mgoing to have a particular subnetthat I'm going to use. Let's clean upthat arrow because it's going to getconfusing.

It's a particular subnet for, in thiscase, my inboundendpoint. Now I can have multipleendpoints; each one of them would requiretheir ownsubnet. This is dedicated perendpoint.

The minimum is a slash 28; therecommendation is to do a slash 24.It gives me that ability to scale in thefuture. You can think about, well, how manyqueries per second am I going to need toHandle, so I may want to have thatadditional ability to grow.

And so,what we're going to do here is we'regoing to add an inbound endpoint.So it's nowbasically creatingand using an IP from this subnetthat goes to this private resolver.This is adding the inboundendpoint.Well,at this point, there's now an IP addressthat exists in my virtual network; it's aregular IP addressthat's routablejust over regular IP connected networks.This will now route to thisand what this is basically now doing isvia thiswell,it goes and resolves against Azure DNS.So what can I do? Well, instead of havingto mess around with this old DNSforwarder and doing manual stuff, which Ireally don't want to do,I can eliminate all of thatand instead of forwarding to myon-premises DNS.Hey, fantastic! What I'm now going to doIsforward over here.

Now, this could just be forwardingeverythingthat it's not forward to. So, hey, Idon't have an answer in my zones,send it to here, which will send it tothe DNS resolver, which sends it to AzureDNS. Or, this could be conditionalforwarding; you have a choice.I.e.,hey,only forward if it’sx.net,then forward it to the IP address thatit's adding in that subnet.

So, you can think about this as solvingthe idea of DNS servers that exist outside Azure.They could be on-premises, could be in otherclouds, whatever that is,as long as it has an IP path. There's aconnection to this VNet.I can now forward from my custom DNSserversto the IP address it's creating via thatinbound endpoint,to now resolve against Azure DNS andresolve records in those private DNScustom ones, private link, whatever I need.

And again, I could add additionalendpoints if I wanted to, maybe for scalepurposes.Maybe I’ve got different business unitsthat are going to use this. I want to buildback, so I’d create a different endpoint.If I added a second inbound endpoint, ithas to be a different subnet; it’s onededicated subnet per endpoint. I can’tshare them.

So this is solvingthe idea of, “Hey, I want to resolve toAzure DNS from outside the virtualnetwork without having to manually worryabout DNS forwarders. Deploying it’s justdoing that for me. I could absolutelystop there. I can say that that’s all I needed.Hey,that’s the functionality I need from theAzure DNS Private Resolver.

But then there’s a second part offunctionality I may want,and that’s the idea that, “Hey, I’m usingAzure DNS,but I have some records,some zones hosted on my own custom DNSservers. It could be in Azure; it could beon-premises, that have IP addresses.So from Azure DNS,I want to be able to forwardTo other DNS servers that host thosezones, and today there's no way to dothat.

Well, that's the next part of what we canconfigure in the portal.So once we've added, optionally, rememberI don't have to do this. Maybe I don'twant the inbound functionality. I have achoice if I want to enable thisfunctionality or not, but I'm going tosay yes, I want to add an inboundendpoint.

Now I can optionally add outboundendpoints.So once again,um, let's just do outbound. I didn't useconsistent naming. Notice the subnet Ipicked for my inbound is now grayed out.I can't use the same one; I have to pick adifferent subnet, and I'm using slash 24.So I've got future scale; I'll save that.

So it now has an outbound endpoint.Now, at this point, you might be wonderingwhat on earth do I needan outbound endpoint for.So let's think that through. Azure DNSis this Azure service;it's floating out there, it goes andlinks to these private zones throughresolution.

I'm now in a scenario where I have my own DNSserver. My own DNS server has an IPaddress that might beon my virtual network.It might be on a different networkthat’s connected via my virtual network,so I have to be able to talk to it. Well,Azure DNS has noexistencein this virtual network.I might not have an inbound endpoint, andit doesn’t want to do dual duty anyway.

So, it needs an IP address that it canuseto communicate with two things via IP.So, the way we do that is, well, okay,we're now going to addso it needs its own subnet. Again, asecond dedicated subnet,so this is going to be for my outboundand once again, I can add multipleoutbound endpoints if I wanted to.

And once again, it could be a slash 28,the recommendation, though, is to use aslash 24.And once again,it’s going to createan IP address.

And this is now an outbound.

Endpoint, and this is the important part, so thinkabout when I'm going to go and now have somerecords to say, "Hey, I want to queryanother DNS server." If I'm a client andI'm querying Azure DNS,this solution is not going to afford myclient to say, "Hey, go and talk to thisDNS server." No, Azure DNS is going to goand talk to the DNS server on my behalf,and it’s going to go and get the answerand give it straight to me. So Azure DNShas to have a path to get to the DNSserver it’s going to fall to. So when Igo and query Azure DNS for some record

that’s hosted on this DNS server or thisDNS server,what’s going to happen is this privateresolver, using this IP address,will now go and communicate to that DNSserver to get me the answer, orcommunicate over the site-to-site VPN orExpressRoute and talk to this DNSserver to get the answer. So it’s usingthe outbound endpoint to get meIP connectivity to the DNS servers I’mThe recordis set so it can answer that requesting client.

It's not pointing the client to adifferent DNS server, so the client needsthe connectivity. It doesn’t, Azure DNSneeds the connectivity so it can go andhave a path to query it. That's why itneedsthat outbound endpoint. Again, I could addadditional onesfor scale. Again, maybe multiple businessunits. I want to be able tocharge back in certain scenarios.So it has an outbound endpoint.

Um,but what am I conditionally forwarding?So then the next part, if we actually goand look in the portal,is once I’ve created that outboundendpoint,I have to create a rule set. Now, I coulddo this later on, but this rule set is aseparate resource. Again, the portal isdoing it all for me.But it’s a separate resource. Now noticeI have to bind it toan endpoint.Because that rule set, obviously, hey, I’mgoing to set a bunch of rules.

Now, the way it talks to the serversis going to use the outbound endpoint.What I’m going to do nowis go aheadand createthis idea of a DNSforwardrule set,which is just going to be a bunch ofrules.You have that whole idea of, okay, well,the zone you want to talk toand kind of the IP address, and then itwill kind of be the IP address. So, I haveto create the DNS rule set, and I’m goingto bind itto an outboundendpoint,because that’s how it’s actually goingto go and do the communication. So, it’s aseparate resource, but it’s going to get

bound to an outbound endpoint of aparticular private resolver. So that whenit has to do these forwarding rules, itcan go and use that IP to go and talk tothe DNS to get the answer to give to therequesting client.So,if we continue this through,okay, I’ve bound it to a certainEndpointand thenwell, I add rules. I can add multiplewalls. Hey, my rule name maybe it's SavileTechcom is hosted on my zone. What is thedomain, the DNS zone? So it'ssaviletech.com, and then you end with adot. I'm going to enable it. I have to addthe destination. Well, this is hosted on10.0.1.10.

Notice it's destination port 53,and maybe I've got multiple servers. Itcan also go to 10.0.1.11.And I can add thatand I can add multiple rules.So I can go through and add the variousrules,and what's happening is this is bydefault, just linking itto this particular virtual network. So asI'm going through the portal,what it's now going to dois, yes, I'm creating this DNS foldingrule setand it's alsogoing to take thisrule set with all the various rules thatI'm adding to it,and it's going to link itto the virtual network.

And that's really that kind of completepicture.So now, it's linked these forwardingrules to the virtual network in the sameway I link private DNS zones to avirtual network.When anything in this virtual networknow queries Azure DNSfor something in one of these zones I'veadded as rules,well, as your DNS now knows about it,it will go to the private resolverwhich will use the outbound endpoint togo and query the DNS server I'vespecified,get the answer,and then give it back to the client,so that's the key idea of this.I may have a hub-and-spoke pattern; this mightbe my hub where I deploy the DNS privateresolver. I may have other virtualnetworks. Well, if I have kind of spokevirtual networkshere,I would link thisto them as well so they have the samecommon sets of conditional forwarding.Now, this they have to be in the same region,so I'm drawing this all in the sameregion; these are regional resources.

Commonly, these are going to be peered.That's normal,and so I want them to have a common setof conditional forwardings, have the sameresolution, so they're all going to havethe same for every peer. I’d probablylink the sameforwarding rule set to all of thosespoke virtual networks. They’re allconsistent.But it actually doesn’t have to bepeered because remember what’s the flowof communication. Let’s sayI linked this rule set to a virtualnetwork that wasn’t peered to this hub.

Would it still work?Absolutely, it would.Becausewhat’s the communication path?I’ve linked the rule set.A client in here talks to Azure DNS,hey saviletech.com.Azure DNS savvilletech.com becauseremember I’ve linked this rule set.Okay, it knows it’s handled by thisoutbound endpoint of this privateresolver.So Azure DNS Cloud Service has the rulethat says, "Okay, for this zone talk toWe will use the outbound endpoint to go andget the answerand then Azure DNS gives it backto the client in this virtual network.

This virtual network doesn’t actuallyneed IP connectivity to the DNS serversthat the conditional forwarding ruleapplies because it’s not the client thatgets redirected.Azure DNSis doing the lookup for me,so typically, yes, they’re going to bepeered because I probably have ahub-and-spoke model, and so they’ve got thatcommon. But if it wasn’t that scenario, ifthis was just a VNet, but it still didneed resolution from those DNS servers,it doesn’t have to have an IP path tothose DNS servers; it’s not required. It’sgoing to be the normal case, but itdoesn’t need it because the DNS path isnot going from the client to the DNSserver. The path is, “Hey, I’m talking toAzure DNS.”Azure DNShas the forwarding rule because it’slinked to the virtual network.The rule set is bound to this outboundendpoint at the private resolver, and ittalks via that.

The answer is, that's really kind of the key pointof this, and again I use as much or as little asthis as I want. Maybe I just need theinbound. I have my own DNS services thatI want to be able to resolve records inprivate DNS zones. Great! I just deploythe inbound endpoint part.Maybe I only need, hey, from Azure DNStalking to my DNS servers. Hey, I don’tdeploy an inbound endpoint; I only deploythe outbound endpoint, andthe NS forwarding rule sets. I have tohave the rule set outbound endpoint onits own; it’s useless. I have to have theoutbound, the rule set, to actually tellit what to forward to. I could just usethe outbound and the rule set,or hey, I want both sets of thatfunctionality. I deploy as much or aslittle as that as I actually want.

Um,it does have to be in the same region,so if I had multiple regions today,well, I obviously need a DNS privateresolver in Avena in that region.Today, the forwarding would say I’d haveto create the other regions as well.I don’t know what’s happening in theIn the future, but that's where it is today.

The scale I would expect to also comeinto play later on today is, I think, afixed scale. But I would imagine overtime, based on how many queries persecond I’m doing, there'll be some scalemechanism in play. The documentation saysit can be a 28, but 24 is recommended.The only reason it would recommend apotentially bigger one is because itintends to scale things inside thosesubnets. So, I think it’s fairly plain tosee at some point there will probably be somescale functionality.

But that’s it.That’s what the Azure DNS PrivateResolver does; it removes me having toif I want to from my DNS serversoutside of Azure resolve private DNSzones. I don’t have to manage somecustom DNS folder.And now I can actually forward fromAzure DNSto zones hosted on my DNS servers, be itin Azure or outside Azure.The VNet doesn’t actually need a path;the only path I need to the custom DNSservers is the outbound pointthat is bound to the DNS forwarding rule.Set.

So, that's it. I hope that kind ofexplained what this is,why you'd use it, and as always,until next video, take care.You.
