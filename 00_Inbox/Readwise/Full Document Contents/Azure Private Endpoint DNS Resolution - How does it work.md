# Azure Private Endpoint DNS Resolution - How does it work?

![rw-book-cover](https://i.ytimg.com/vi/nRzX6QYvvto/maxresdefault.jpg)

## Metadata
- Author: [[LA NET LTD]]
- Full Title: Azure Private Endpoint DNS Resolution - How does it work?
- Category: #articles
- Summary: Azure Private Endpoint DNS resolution uses private DNS zones and a private DNS resolver to map service names to private IP addresses within a virtual network. This setup allows both Azure resources and on-premises machines (via VPN) to securely resolve private endpoints without exposing public IPs. The private DNS resolver handles inbound and outbound queries, enabling seamless name resolution across connected networks.
- URL: https://www.youtube.com/watch?v=nRzX6QYvvto

## Full Document
Hi everyone. In this video
we're going to talk about Azure private endpoint name resolution. Im joined
by Adam and Conor from our team. He'll be showing us
some demos and what it looks like. What we're
going to do is look at how private endpoints work
looking at it from the DNS zones, how do you resolve
those private endpoints for those PaaS resources
and also how do you resolve those from on premises networks. Okay, as
you can see in our diagram below, 

we're going
to show and demo all this working environment
from Adam and Conor. But I'll just
quickly take you through what's happening here.
We've got a private DNS zones, that's where the records are for our private endpoints. We've got storage
accounts set up for the private endpoint
which is linked to a network. We've got a virtual machine. We'll use that
for resolving that private endpoint. And on the Azure, sorry on the on
premises side we've got a domain controller with conditional
forwarder setup to point to the private
DNS resolver which is a service in 

Azure to
go and get those private endpoint IP addresses back for us. I
will show you that working as well. Now the private
DNS resolver itself is a service. There are other ways. You could add a server
in there with the DNS service on there. You
could use ad, you could use apds, you could
also use an Azure firewall as well. But we're going to use the private DNS resolver in this example. So
let's get straight to it and switch to, let's take a look at the Azure side and look at those resources. Let's look at the
private DNS resolver and the zones 

and the private
endpoint and storage account. Conor? Yes, let's take a look
at our private DNS resolver here. So we've got one set up here. So two main components
of a private DNS resolver are these two sections here in this, you can see
in this overview page the inbound endpoint
and the outbound endpoint. And so that's going
to allow you to resolve your DNS, your
private DNS on inbound resolution. So from your on
prem into your Azure or outbound so out from
your Azure out onto your on prem. 

So let's take a look at these. So with our inbound, here's
our IP address and for our inbound resolution and remember this, we're going to
see this later on and when we go on prem
and we have also a subnet as well. This is tied to with outbound. This
is also again tied to a subnet and but
has a rule set associated with it. So this is
rules that if we take a look in here 

we can
see this goes down to our on prem. So again this allows
us to go down to on prem and resolve
anything we want down there and we also here as well. Yeah
and we can also use that outbound one to resolve other services. So you may have other
DNS services outside of Azure. You can
then add that to your outbound end points here as well. So if you're
not using that we suggest you, you can
just delete the outbound because 

you do pay for the service, one for your
inbound and one for outbound. So
if you only need it for inbound just, just
use the inbound section and you. The whole
point of this is it creates a private resource that you
can use to do that DNS resolution. So that's great
kind of we've seen that we can see that
it's in our private network there using that subnet section there. And we did capture
the IP address if you just click on inbound again so
we can see the IP address 10.63.0.4 

and we'll see
where that comes into play later. So now if we look at the DNS zone. So actually
let's look at the storage account. Let's
take a look at the storage account and the private endpoint. Okay, no problem. Yes we've
just got a very standard basic storage account set up here. Our main interesting
bit is over here networking. Weve got the public
network access disabled for this. 

What we do have is
a private endpoint connection set up with a couple set
up here we have one set up that is into the
production in Azure we can resolve this and access the
storage account from an Azure as we also have one
here that goes to our Hub network. Anything
coming in from our VPN can access it through that private endpoint. Okay cool. And now let's take a look at the private DNS zone
and we should see corresponding 

records
for this storage account in there. Yeah so we
jump over here, see this one here, this
privatelink.blob.core.windows.net and we can see record sets. Yeah there
we are, we see our SA productions. Yeah Brilliant. So you've got that
one record and now we can see the IP address
of that storage account is 10.6.0.132. And just about to see that there. What that is telling us is that if we 

want
to access that storage account, we
can't get it via the public endpoint anymore
because we've locked it down. It's
only available by the 132 IP address. Now if we take a look at your. I guess you've
got a virtual machine in Azure. So
let's do a name resolution on that. Yeah,
of course, let's hop over to that. We're hopped
over here into the vm in Azure. And so you were
just going to do an NSLOOKUP of the storage account DNS name I've
already typed in previously here. 

So here we go. You can see that's
the public URL of the machine of the storage account in this case, and
it's come back with the private IP address of that storage account. And
you can see the name is also the privatelink.blob.core.windows.net
so it's come back with the private
link. Now the way it's done that, it's gone off to the wire server, which I think
that's IP address in there in Azure. And because that zone is linked to that production network as well. 

So it's worth
just having a quick look at the link between the zone and
the network that your VM is on, Conor. So can we see that quickly? Yeah,
of course, let's take a look at that. Yeah so if we're back over here, we can take
a look at our virtual network links. In this case, we've
got it linked to kind of everywhere, but yeah, we can
see it's linked to that production. Excellent. Okay,
brilliant. Thank you very much. 

So you can see that
if I go back now to the diagram. Thank
you Conor, very much for that. I'll flip
over here. So we can see from that. That's the DNS zone
linked to the production network. We've seen the
storage account private endpoint, and we've done a resolution
using the public name of the storage account
and it's come back and given us the private
IP address using NSLookum. That's exactly
how you'd want that to work. Now in that scenario
we're not even using the private DNS resolver because
this has got a direct connection 

via the wire server to this here. Now if we
flip over to the on premises side. Thank you very much. Conor, let's bring
Adam back and let's flip to the on premises side and
see how this part is working here. So we'll do that next. Okay Adam, so let's leave over
to your side if you want to share your screen
and we'll take it from your side list. Okay, we're back
on our domain controller here. 

So
this is on our on premise network and connected over
the VPN to our Azure environment. So we'll just have
a look at the IP address here so we can see
it's the local IP address is 10.0.255.5. So if, okay, so we'll just do
an NSlookup for the name of the storage
account and we'll see what comes back with that for that for now. Okay, so at the
moment we can see the public IP address
coming back for that account. 

We do have public access disabled, so if we
tried going to that account at the moment
we wouldn't be able to access it. But
just because it was enabled before, that record sort of still lingering on the DNS servers. So what we're going
to do now is we'll jump over to the DNS console
for this dc and then we'll actually add
in those conditional forwarders. So we'll get that loaded up. Now at the moment
we can see there's no conditional forwarders in here at all. What we'd want to
do is if we just right click on here 

and we do new conditional
forwarder for the DNS name. You want
the name of the DNS zone in Azure. In this case
that will be blob core windows.net for the IP address here, we want the private
IP of the DNS resolver endpoint. So in this case that's 10.63.0.4. And once we add that in here, we'll be able
to see it go green because it can 

establish connectivity
to that endpoint over the vpn. Well also take this box. This
is a standalone domain controller, but if you had multiple
controllers that are on your domain that
would replicate the DNS records to those controllers as well. Then
we'll go ahead and add that in. Now that that conditional
forward is added we should be sending all those DNS lookups to the DNS resolver in Azure. We're Just going to
jump onto the workstation VM that we've got set up
and then we can see that resolving 

we're on the workstation VM now. What we'll do
is we'll open up a terminal session and
we'll do another NS lookup here. If we do an NSlookup
now we can see that we're going to our local DNS
server on the DC and then we get a response back
of the private IP address for the private endpoint
on that storage account in Azure. Thats exactly what we want. 

Now when we're trying
to do these lookups from on Prem and connect to these
Azure services and we're actually going over the VPN and we've got those private IP addresses. Whats
the reason that we put those conditional forwarders in place? I know we've seen
customers do it slightly differently but what's
the benefit of the conditional forwarder specifically? Right, so the benefit of
using those conditional forwarders is what it's doing is basically offloading those zones to the 

private DNS resolver
that will then go and find the zones and the records
in there and just bring back the results. What
some people do or were doing, I don't know
if they still do it is set each of those A records up manually
on their on premises domains. So when
they create a new private endpoint they create a manual record, they create a zone
and put a record underneath and it will work and
that's perfectly fine but it's not as efficient as
just sending any request to Blob. Just send it off to
the private DNS resolver and that 

will go and get the
results for you without you having to manage and
maintain all those A records which can get
in a mess and they can get wrong. So it's just best
to let the system manage it for you. So what you do need
to do is make sure those zones are kept tidy
and when you're looking at your DNS
zones doing any troubleshooting, start there starting your DNS zone. Make sure that
zone record is connect correct it's going to the private
correct private endpoint for the correct resource
and then also make sure you're 

getting
the like you've got SA product make sure
you haven't got any typos in there, you've
got the right domain name at the end of it and yeah, should be fine. So thanks very much Adam. Thanks Conor. We had
a good demo there and we could see each of the steps of, you know what
that private endpoint looks like. Looking
at the A record, the DNS zone link. We looked at how to
resolve that private endpoint from both from the Azure side and also from the on prem side. 

We took a look
at the private DNS resolver and the conditional forwarders from the DC to the private DNS resolver. And also we did the
test from the workstation which goes
to the DC to the private resolver, private DNS resolver
and back to the workstation, pulling out and
sending back the actual internal ip which then
allows us to lock down the Internet part of those PAAS resources. In this case we use
the storage account but it could also
be something like a SQL Server 

and various other PAAS resources. So that's kind of
a demo of how we would set that private DNS
up and how the resolution works. So hopefully you found that useful. You might find that
useful for your troubleshooting as well.
Any questions? Give us a shout, drop us a comment
or get in touch by our website and follow us on YouTube
if you like the video and found it useful.
Thanks guys. Thanks everyone.
