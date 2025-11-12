# Explain By Example: VPN Gateway or ExpressRoute

![rw-book-cover](https://i.ytimg.com/vi/wU9QVF9iqOI/maxresdefault.jpg)

## Metadata
- Author: [[Explain By Example]]
- Full Title: Explain By Example: VPN Gateway or ExpressRoute
- Category: #articles
- Summary: Azure VPN Gateway uses encrypted connections over the public internet to securely link on-premises networks to Azure. ExpressRoute provides a private, faster connection by physically linking your network to Azure through a partner, but it is more expensive. Choosing between them depends on your business needs, balancing cost, security, and performance.
- URL: https://www.youtube.com/watch?v=wU9QVF9iqOI

## Full Document
hi youtube welcome to another one of these explained by example videos now today we are going to take a look at vpn gateway versus express route recently i watched frank abagnale's talk on youtube and to be frank i didn't know who he was or is now if you're like me you have also been 

living under a rock he is essentially the real life leonardo dicaprio of catch me if you can anyway between climbing out of this rock i've been living under and studying for the azure architecture certification i started thinking about the connection between undercover agents and azure networking or more specifically the commonly asked question about whether one should pick vpn gateway or express routes to connect to azure as 

usual i like to start with the basics before getting to the answer so what is vpn gateway azure vpn gateway allows you to connect your on-premises network to azure networks to send encrypted traffic over an insecure channel what does that really mean let's say you have a bunch of servers on premises which is just machines in some organization or some data center and you want some of those machines to be able 

to connect and communicate with a bunch of azure services also known as cloud services this is an example of site-to-site connection we have one site your on-premises connecting to another site your azure environment how does site-to-site connection work well to enable site-to-site connection or s2s we need to install a vpn device into one of the on-premises network this vpn device 

allows you to connect a vpn gateway which you have to put into your azure virtual network or azure vnet technically you have to carve out a section in your azure virtual network which is known as a subnet called the gateway subnet this subnet needs to have enough space for the vpn gateway to use so you need to use at least slash 27 for 32 addresses or slash 28 for 16 addresses for this gateway subnet you 

also need to create a local network gateway which is essentially a reflection of your vpn device that you have installed on premises the local network gateway takes in the public ip address of your vpn device think of it as this is where your vpn device is located on premises and the address space which is essentially the number of address spaces you have in that particular on-premises network the vpn device is installed on now remember 

what i said before about vpn gateway allowing you to send secure traffic over an insecure channel this is because the traffic gets encrypted before it is sent out like frank abagnale putting on a disguise before he took on an undercover job for the fbi or committing a crime when traffic is encrypted you don't really know what type of traffic it is nor the content of the traffic like when 

frank was an undercover agent or committing fraud in disguise you didn't really know it was frank you just know that it was some pilot some doctor or some lawyer which meant the traffic can traverse over the internet an insecure and public channel freely just like how frank could roam about firmly under the skies once we get to the destination we can decrypt the traffic to reveal its contents like 

removing a disguise to reveal frank's true identity to set up for encryption and decryption the vpn device must share encryption and decryption keys with vpn gateway this is called shared key or symmetric key encryption i won't go into details about encryption and decryption maybe it's a topic for another video but essentially the vpn device and vpn gateway share the same encryption in 

decryption keys which means before the traffic is sent out to the internet it is first encrypted when either party receives the traffic they can use the decryption key to decrypt the traffic all you need to know for now is that vpn gateway supports ipsec slash ike protocols which is the industry standard for cryptography when it comes to vpns once your vpn device knows the shared secret keys to be used 

in information exchange as well as the public ip address of the vpn gateway you can create a connection between the two and voila you have connected your on premises to azure vpn gateway also supports what is called point to site or p2s connections point of sight connections allows you to connect say your computer to your azure virtual network again the traffic goes over the public internet but because it is encrypted it 

remains anonymous safe and secure why would i use p2s connections well let's say you have successfully set up the s2s connection between your organization's on-premises networks to azure now after all that hard work your manager says well done you deserve a holiday so you hop on the next flight out to hawaii for a short vacation as soon as you touch down at inouye 

international airport you get a call from your manager help she starts to say one of our proud environment is down and we need you to fix it immediately you roll your eyes and think i should really get a raise this year but you don't say that instead you tell her no worries let me check into my hotel first so i can download the azure vpn clients to securely remote into azure through vpn gateway and fix it p2s connection is really great for any 

remote workers that need to connect into your azure v nets securely over the public internet after your vacation in hawaii you come back to find that everyone is talking about express route and you start to wonder what is azure express route azure express routes your manager starts to say allows us to physically connect our on-premises networks into azure yeah but why would we want to do that well we don't want our traffic going 

over the internet anymore and besides we have been experiencing latency with more members joining the team and we are getting internet outages it's just a nightmare also i overheard the ceo and the cto the other day talking about expanding the office to the other side of the country and sounds interesting enough so you pull up microsoft docs to have a little read on the features and benefits of express routes you find that to create an expressroute connection you first need 

to create a circuit the physical connectivity into azure is done by an express route partner so when you create a circuit you are essentially asking your chosen express route partner to set up a physical connection for you to connect to they on the other hand connect the circuit into azure once you've created circuit you need to extract the service key and pass that on to your chosen express route partner once your expressroute partner has connected you you will see the provider 

status and your circuit change from not provisioned to provisioned now that you have your express route circuits activated you can start connecting your azure virtual networks to your on-premises networks over express route similar to vpn gateway you need to create an express route gateway inside your virtual network before you can connect to the express route circuit like connecting to the vpn device an expressroute circuit can be connected to 10 different virtual networks and a 

virtual network can be connected to four different express route circuits all traffic is now traversed over your own organization's networks and the microsoft azure networks which means even if the public internet crashes it will not affect your traffic flow what happens when my express route circuit goes down your traffic flow to and from azure will obviously get cut off so typically to ensure for high availability you have two express route circuits set up one as a primary link 

and one as a secondary or backup link for disaster recovery you can set up one circuit and one region and another circuit in another region so even if the entire region or city goes down your connection to azure is not broken and if you are really concerned let's say you are worried that you might end up having a dispute with your express route partner you can set up multiple circuits across multiple regions with multiple different partners and if all that fails 

then we must have really hit strike on the doomsday clock what was that part about eavesdropping on the ceo and cto another advantage of using express route is leveraging the global microsoft network so your manager overheard that a new office is to be set up on the other side of the country and surely they would want to have two offices to communicate privately rather than exchange their communication over the 

public internet but setting up a gigantic wire to connect the two office networks together will be too expensive what can we do instead with expressroute globalreach you look up to find your manager say we can connect our two office networks together at a fraction of the cost by leveraging microsoft's global network gee she's really keen on this express route thing you think to yourself how does express route global reach work quite simple she says express 

throughout global reach connects express route circuits together which means if we connected our main office to an expressval circuit and our new office to another expressway circuit then link those two express our circuits together we will be able to do all our office communication privately over the microsoft network the ceo just happens to walk by and hears this and asks does private mean the communication is encrypted no the traffic that traverses over express routes is not encrypted but 

you can encrypt the traffic over express route if you really want to with ipsec and azure virtual when so should we pick azure vpn gateway or azure express route to connect to azure and the answer is that depends on your business requirements vpn gateway is typically cheaper than express routes and whilst you get the anonymity and security of encryption with vpn gateway you are still traversing over a publicly exposed and 

insecure channel and are dependent on internet providers for network consistency with express routes your traffic is not encrypted but it is private and you would experience lower latency than with vpn gateway think of express route like plugging a device straight into the ethernet port for faster internet speed versus vpn gateway relying on the wireless connection or wi-fi however this comes at a cost as you need to pay for hardware that is specifically 

dedicated to you that's it for now um if you enjoy this video please go and check out my other videos uh or feel free to follow my blog on medium.com michelle.z for more blog contents otherwise don't forget to like subscribe and leave me a comment
