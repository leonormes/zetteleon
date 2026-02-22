# DNS & Amazon Route 53 Deep dive

![rw-book-cover](https://i.ytimg.com/vi/94vdYMBcE5Y/maxresdefault.jpg)

## Metadata
- Author: [[EICIT Learning]]
- Full Title: DNS & Amazon Route 53 Deep dive
- Category: #articles
- Document Note: **Background:** I am configuring private networks for Amazon EKS (Elastic Kubernetes Service) and I want to ensure that I can access DNS records from a peered Azure network.
   ### Key Takeaways:
   🌐 **Establish Private Connectivity:** Ensure that the VPC (Virtual Private Cloud) in AWS is properly peered with the Azure Virtual Network, allowing seamless communication and access to DNS records across both environments.
   🛠️ **Configure Route 53:** Set up Amazon Route 53 to manage DNS records effectively. Make sure to create the necessary private hosted zones and link them to your EKS cluster for proper DNS resolution.
   🔒 **Implement Security Measures:** Review and implement security configurations, such as security groups and network ACLs, to allow DNS traffic between the peered networks while maintaining security best practices.
- Summary: The text discusses DNS and Amazon Route 53, explaining how domain names work and the role of authoritative DNS. It highlights the difference between naked domains and fully qualified domain names, and how DNS resolves these to IP addresses. Route 53 acts as the authoritative DNS for domains, allowing users to manage domain records and routing.
- URL: https://www.youtube.com/watch?v=94vdYMBcE5Y&list=WL&index=9&t=4s

## Full Document
okay so let's get started off with uh giving a quick uh introduction about myself this is me Fel Khan I'm currently founder and CEO at two organizations Ecom India Cloud it as well as exite logic um Ecom Cloud it is based in Hyderabad India exite logic based in the us both uh born on the cloud companies and uh we're building products uh that'll help people both move on to the AWS Cloud as well as you know other services S Services on AWS 

club uh as far as AWS itself is concerned uh my contribution on the side of AWS is that I am also a user group leader in Hyderabad which is basically a community of uh people who uh talk about AWS who want to learn AWS and I would actually encourage you to join uh the community the user group in any of the city that you're currently uh coming from uh that you're currently in uh on the certification front I'm as Solutions 

architect professional certified I've also been uh an abls Community builder for a couple of years um and then I kind of graduated you could say to the AWS Community Heroes program uh what do I do in my free time I have a couple of things that I do uh first of all I have some uh training that I do for AWS under the eicit learning uh Channel um and I recently started a new brand called racer parot which is based basically something to do with Formula 1 

uh so if you guys know Formula 1 there are these uh radio messages that the drivers actually call out right so I kind of take those messages and design uh t-shirts around that and and other merchandise so do check it out if you need to uh and I uh recently built out a community Forum called let's St AWS uh it's where you can go and ask questions about AWS or you know talk about what you're doing uh even share your knowledge if you wish to 

okay with that out of the way let's look at what we're going to cover today so let's just quickly look at some of the basic concepts of domain names and uh then we'll talk about DNS routing and we'll talk about some of the common DNS record types that you have and then we'll talk about Route 53 itself um and we'll talk about the different routing policies that you have within Route 53 some of the traffic policies and something known as R3 resolver and then I should be able to show you some lab SC 

okay uh some of the domain name Basics here there are different levels when you talk about domain names so there is something called top level domains these are your Dooms your nets and your orgs right so like the the last bit of your domain names uh these are known as tlds or top level domains then you have something called The Naked domain which is is basically the name plus the TLD 

okay so this is the name plus your TLD which kind of is basically your naked domain um there's a reason it's called a naked domain which I'll explain in a second and then you have something called a sub domain which is your naked domain plus something in front of it okay now you might have uh so far thought I mean if you know this well and good but so far uh you would be forgiven to think that these are the same they 

aren't these are actually completely two different domains so I can have a completely different site on example.com and I can have a completely different site on www.example.com these are completely two different domains okay because one is a sub domain and one is a naked domain but to make uh you know things convenient whenever someone creates a website they actually redirect www.example.com to example.com so even if you type example.com or even if you type ww. example.com you're kind of 

redirected to one and you're only using that one but ideally you know if you choose to you can have complete different website on example.com and a completely different website on ww. example.com they are in the same thing just keep that in mind now a subdomain can also be like uh mail. example.com or app. example.com all of these are subdomains right because they are sub of the main naked domain you can also call it as a fully 

qualified domain name in some cases but ideally speaking a fully qualified domain name or an fqdn okay fqdn a fully qualified domain name is something where you are describing that in as much detail as possible all right for example server one refers to the server like us hyphen a refers to where it is uhpr refers whether it's PR or test and then finally you have the naked domain so this is kind of like defining the domain as much as possible so that you can have 

multiple combinations of it this is what you would call a fully qualified domain name or an fqdn so keep these things in mind because we'll need it in the future slides so um before I go into how DNS Works let's just look at a basic flow of DNS so there is something called the resolver the root DNS the TLD DNS and the authoritative DNS and the flow is always like this the resolver will ask the root DNS the root DNS will pass that 

information to the TLD DNS and the tldd DS will pass that information to the authority DNS which will then finally pass the information back to the resolver okay this is a flow but I'll I'll show you how this flow happens okay um yeah Harish has a question could you please show a small demo for naked domain and subdomain so far I have used both seems same um that is exactly the points I will show it you today um 

hopefully within the next 15 minutes if you have the time but I should be able to show it to you no problems okay um the resolver is the one that actually does the resolving so what is DNS per se DNS is domain name system where basically you have uh a name being resolved to an IP Okay the reason is simple uh as humans we are not good at remembering numbers because IP address I mean of course there are geniuses who 

can remember big numbers but not all of us are geniuses so we have issues remembering numbers and some of us are not good at maths so we're not good at remembering numbers okay but we good kind of better at least in Remembering names so it's easier for us to remember like google.com instead of remembering the IP address of google.com right um I think there was a time when we used to all remember our phone numbers of our family and everyone but today we have it as contacts in our phone books so yeah 

same thing so DNS allows you to convert a name to an IP address because as humans we are good at remembering names but computers still use the concept of IP addresses they need to know where they need to know the IP address in order to fetch something okay so DNS allows that translation to happen between name to IP so a resolver is the one that actually starts that process so the resolver goes and finds out what is the IP that's the job of the resolver 

okay um the root DNS is a set of servers I believe it's a set of 13 clustered servers which has information about all of the TLD servers okay so the TLD servers are what the Dooms the Nets Etc so uh these are managed by certain uh organizations for example uh I believe is managed by verisign uh 

verisign uh I think yeah I think it's managed by verisign where they take care of the complete.com tlds right so the root DNS uh has information about the servers about Doom the servers about net Etc right it doesn't have all of the information about the domain names itself but it has information about the servers that are handling the tlds okay and the tlds have the information about the servers that are handling the naked domain for example example.com 

okay this is a naked domain so the TLD dnss for those particular um tlds has information about the servers that are handling each and every um naked domain belonging to that TLD let me show you the diagram it will become a little bit more clear so as an example over here we have a user who's trying to go to www.example.com so there is the web server which he 

needs to access the web server's IP address is 102.5 2.91 and this is the web address okay so in order to fetch this page www.example.com the user needs oops what happened there yeah so in order for uh the user to load 

the web page on the on the computer this computer needs to go ahead and find out this IP address once it finds out the IP address it will make a direct connection and then load the web page that's the whole idea right so over here you have the web server and then you have something called the authoritative DNS or name server this name server or the authoritative DNS is the one that holds the information about the naked domain so the naked domain here is example.com it holds the information about all of 

the subdomains of the naked domain so for example here www.example.com mail. example.com db. example.com this authorita DNS knows the IP address of each of this okay it knows the IP address of each of this because it's in the same network or you know it's kind of associated so the authority knows the IP address of ww. example.com is this that information is with the authoress so ideally speaking 

this computer needs to ask the authority DNS the IP address for this in order to get this IP and then make a direct connection but it is not that simple because there are other servers that are involved in the process which is the root DNS the TLD DNS and the resolving DNS your resolving DNS is normally your internet service provider when you have your connection setup for the first time um your internet service provider will kind of configure the resolving DNS on on your uh connection on your router and 

whenever you your system wants to find out something it'll go ask the resolving DNS and then it will start from there let's see a flow how this happens so the user wants to find out the IP address of www.example.com let's assume that this is the first time they're doing it because if they've already done it normally the IP is stored in the cache of the system but let's just assume that this is the first time that they're doing it so the first step is the system will ask the resolving DNS can you find out the IP of 

www.example.com for me the resolving DNS will then first ask the root DNS hey root DNS can you tell me the IP address of www.example.com remember the root DNS does not have information about that subdomain or that naked domain but it does have information about the TLD servers that is handling.com so what it will do is is it will tell uh the resolving DS I don't 

know the exact IP address of www.example.com but I know the IP address of the Doom servers so here is the IP address go ahead and ask the Doom server okay so the resolving DNS will get the IP address of theom TLD it will then ask theom TLD hey can you give me the IP address of www.example.com here again the TLD does not have the information about the subdomain but it has information uh about about the naked 

domain as in it knows the server that is handling the naked domain so it will reply back saying I don't know the exact IP address of www.example.com but I know the server that is handling example.com here is the IP go ahead and ask it okay so that IP will be returned which is basically the IP of the name server or the authority and finally the resolving DS will ask the same question hey can you give me the IP address of ww. example.com and obviously this time the authority does have that IP because it it has the 

information about that subdomain and it will return back that IP which is 1.21 15.29 and it will return then that IP to the system which then once the system gets the IP it will then establish the connection to the server all of this process whenever you type a website address happens just like that at the Split Second all of this is actually happening in the background when you search for 

domain name okay so keep this in mind if DNS system does not exist your internet is not going to work okay so this is a very core function uh DNS for the internet to survive uh and you're not always directly connecting there's all these queries that are happening however in order to save this process from happening again and again and again every single time once you get the IP address you send you tend to store that IP in the cache of the local system okay so that every time it does not have to ask this question that you need to ask a 

we you need the IP because the next time you need to access this it will go ahead and just directly connect to the IP okay um Can someone tell me which part of this do you think is Route 53 where is Route 53 here which which is the system Route 53 here is it the resolving DNS is the root DNS is the TLD is it the author DNS which part is Route 53 here do you think nobody anybody which part do you think 

is Route 53 over here this is your Route 53 okay basically you are going to add your domain to Route 53 and this is your easy to instance okay so you're going to add your domain in Route 53 and all of the records will be created inside Route 53 so all of the records for ww. example.com mail. example.com d weor example.com Etc will be created inside 

your Route 53 which will act as the authoritative DNS for your domain what that basically means is once you add your domain to Route 53 if anybody wants to find out the IP address of your domain the end request will have to come to Route 53 and Route 53 will answer giving back the IP address so that's the job of Route 53 route 53's job is to answer queries on your behalf for your domain name and then it will always return the IP address address of wherever you have hosted that um domain 

okay now uh remember I told you about the cach over here it is also important to specify that cache when you create the record so for example if you create a record for ww. example.com inside Route 53 um you have to specify that cache and this is where that cach concept of TTL or time to live comes in okay so if you specify a TL of 30 minutes that basically means means this IP address will remain in the 

user's cache only for 30 minutes after 30 minutes that cash will expire so if the user needs to again go to that website after 30 minutes he needs to again go through this whole process again in order to get that IP okay uh if you say uh a TTL of 1 minute then obviously the cash will expire after 1 minute you have to decide between um you know how long you want to keep your TTL and how short you want to keep your TTL because if you keep your TTL too short let's say you kept your T only 1 minute 

okay this means anybody accessing your domain will have to again and again after every minute they'll have to come ask the question to Route 53 and Route 53 charges you based on how many queries it's answering okay so if it answers 100 queries you pay less if it answers 10,000 queries you pay more so you if you keep it too low then you answering more queries from Route 53 however you don't want to keep it too long as well for example if you keep let's say A Tail of one one day okay uh everybody will 

have this IP stored on their system for one day but what if something happens to your server and you had to change the IP and now ww. example.com goes to 92 instead of 91 what happens then when people try to access it they will try to go to 91 because their detail is still one day and the website won't load all right so you have to kind of balance this between um you know how quickly you want to refresh the cash versus how long you want to let the cash be there so that up to 

you a couple of important things to just keep in mind a record is basically IP of a domain name okay so if you have like example.com the a record for that will basically be pointing to an IP address like 52693 or something like that okay it'll just be pointing to an IP NS record is basically the IP address of the name service so every domain will have an associated DNS or a name server so every 

domain name will have a name server IP that is associated with it this is so that they can find out which name server to get to the C name or Alias record so this is where one domain name points to another domain name this is the example where I wanted to tell you about the uh www.example.com pointing to example.com so this is where you normally create a cname record and you say that anybody typing an example.com it's a c name of example.com which means it's basically 

one domain redirecting to another domain that's essentially what a c name is I mean there is more to it but that's essentially what a c name is then you have MX records if you have mail servers um then you have something called s SOA records or start off Authority this will always be there by default this is basically establishing like who's the Authority for your particular uh DNS then you have something called txt records you use this if you want to do additional valid ation for example if you want to verify that you are the 

owner of the domain uh you will get some txt records that you have to create within your DNS so that you know they can confirm that you are the owner of that particular domain all right um Route 53 itself is going to act as the authority DNS for your domain name so it'll answer queries on behalf of your domain name so you will create uh you will add your domain name in Route 53 and you will add the records um for Route 53 inside that uh there are different types of routing 

that are available there is something called latency basic routing or lbr there is geolocation based routing uh it also integrates with other AWS services and of course if you want you can register a domain name so let's talk about the different uh routing policies let's start with a simple routing policy so in Route 53 a simple routing policy is essentially you are creating something called an a record you are having a domain name that you're routing to an IP address in our for example over here I have a load 

balancer which has some ec2 instances behind it now normally you would actually have a domain name that is associated with your load balancer but let's take an example over here and let's just assume that this load balancer has an IP address okay so we want to send anybody looking for ww. example.com we want to send them to this IP address that's our goal so what we will do is in Route 53 we'll create this record in Route 53 and when some on queries for the domain name it will pass through all of those steps um 

that I just showed you in the previous screen and then it will finally hit Route 53 and uh It'll ask for the IP address of ww. example.com and 53 will say here is the IP address go ahead and connect to this and then the user will make the connection to that IP address remember Route 53 does not route the traffic keep that in mind okay it does not route the traffic through Route 53 it only responds and gives the IP back to the user the user us then has to make a connection separately to that IP 

address okay just keep that in mind so it's not it's not a routing traffic like elb or anything like that so that's a simple routing policy then you have something called latency based routing policy this is if you have multiple environments and then you have to uh you can basically route users based on their latency between their location and the nearest region so for example over here there are three regions that I'm using North Virginia Oregon and North California and I have the same content in all of the regions 

right I don't want to have different content because I don't want I don't want to have different users going to different content I want to have the same content across all of them so I have a website running the same content across all of the three regions I will set up latency base routing uh and what happens is Route 53 because it's it's uh highly available and highly scaled system it knows the latency between the users location and all of the different regions so it knows the users's latency 

between North Virginia and the user is 20 milliseconds the latency between Oregon and the user is 35 milliseconds and the latency between North California and the user is 42 milliseconds so what do you think is going to happen here which IP do you think Route 53 will return Route 53 will return the lowest latency uh routing in this case which means it will return the North Virginia IP so it will return back to the user uh go to IP 10. 65.2 do6 now this might not 

always be the same the next time if the user queries if this is for example 18 M seconds or something like that then the next time he will get this IP instead of the other one right so this is what it is you can always get the user to connect to the quickest uh region that is next to him okay this is assuming that you have something set up there okay it's not just going to directly just give that you have to have something set up then you have waited routing policy this works in a similar fashion but this 

does not look at where the user is rather this looks at trying to balance your environment in some way okay so let's assume that you have set up a uh you know waiting weightage of 25% goes to North Virginia 15% goes to Oregon and 16% goes to uh California remember here this is not traffic percentage you are not doing load balancing okay you are just saying that if somebody queries the number of 

queries that is coming in you respond back in this percentage okay I'm telling Route 53 to do that so when people query for example www example.com 25% of the time they will get this IP 15% of the times they will get this IP 60% of the times they will get this IP now even if I made this 33 33 and 33 it's still not load balance maybe the first time it's load balanced but then 

after that it is not balanced because okay stay with me for one quick minute here I'm going to try to explain this to you if 100 users come in at 10:00 a.m. and requested for the site IP 33 of them will get this one 33 of them will get this one and let's say 34 here okay 34 of them will get this one okay um maybe at 11 a.m. out of this 

100 50 people returned okay at 11:00 a.m. 50 people returned now do I know which 50 people those are it might be 33 from here and 20 from here right I don't know like you can't control that once the user gets the IP you can't control where how many people come back to that same environment so this is not load balancing okay but when you are I mean it does it on some level but this you don't do the load balancing over here you use something else which we will 

discuss in our next session how you actually do Global load balancing um using other services but you do this again if you only have the same content you don't want to do this if you have different content and then you have something called geolocation routing policy uh the way I would describe this is think of it like YouTube where if you go to youtube.com depending on which country you're opening it from you will see different content right so if you're 

opening it from the US you will kind of see us related content if you're opening it from India you will see India related content this is because you are being redirected to an environment that you are supposed to go to okay this is where I'm hard coding saying that if anybody is coming from us always return them the IP address of North Virginia okay if anybody is coming from the European Union region always return them the IP address of London if 

anybody's coming from the Asia region always return the IP address of Mumbai so this way I'm controlling from which region people are coming and which uh region I need to redirect them to this way I can have different content in each of these environments uh that are specific specifically suited for that particular country or for that particular region so that they see only that content this is essentially what geolocation routing is and I'll show I'll definitely 

show you this in action and then the final one is failover routing policy fail over routing policy is where you have something called an active which is primary and then you have a standby which is secondary okay your Route 53 will always return the primary always return the IP address of primary so whenever someone queries for it it will always return the IP address of primary unless and of course something happens to the primary then it will stop returning the IP address of primary and it will start 

returning the IP address of your secondary so it's up to you whether you want to completely keep an environment running in secondary always or maybe you just want to have like a static web page on S3s which says that we are currently experiencing some difficulty please come back later or something like that right it's it's completely up to you but the idea here is that you will have a primary and you will have a secondary and there will be a health check that you're running and if primary fails for some reason then it'll start giving the IP address of the secondary till that time it'll always give primary Harish has a question um does 

GPS takes place part in geolocation routing policy so not really GPS uh what happens is um there is uh there is globally uh a list of ips that belong to certain regions right so for example when you are logging in uh from India regardless of your GPS location you are connecting with some data provider right if you're using a Sim you're obviously using a cellular data provider if if you're at home you're using some Broadband provider all of these 

providers have a block of IP addresses and those IP addresses belong to a certain region right so based on that IP location they will kind of decide where you're coming from so if you're coming from a IP block that belongs to like say India then you will you will be identified as someone coming from India which is why when you go to certain websites it tells you that this content is not available in your region that's basically that they look at your IP and then decide which region you're coming from 

okay um now we talked about all of these different routing policies right simple routing policy latency based routing policy weighted routing policy uh geolocation policy failover policy um you actually have the choice of either using these policies individually or you can also kind of chain them okay using something called traffic policy so over here as an example I can start off with a failover routing policy I can have a prim primary and a failover okay so in 

that failover routing policy under primary I can have weighted So within primary itself I can have a waiter routing policy where they go to two separate end points so that the traffic is kind of balanced I would say but if for some reason this entire primary fails uh then I can switch over to the fail over and it can go to endpoint so I can I can in fact kind of chain multiple policies together in order to create something called a traffic policy okay any questions on this before I go and show show you the 

labs so in Route 53 there is something called hosted zones this is where basically you add your domain uh into Route 53 um there is a question about the cost so in Route 53 you can choose to either register your domain uh in Route 53 which will cost you depending on the extension for example I think aom domain costs you around $13 or something like that right but it's not necessary for you to register your domain with 

Route 53 in order to use Route 53 you can use uh you can register your domain someplace else like GoDaddy or in fact you can use um our service which is outpour hosting.com and you can register your domain there but once you register your domain you need to still add that domain into rout 53 you do that under hosted zones so regardless of whether you bought the domain from Route 53 or not you still have to add your domain under hosted zones so you just create a hostage Zone type in your domain name 

over here and it will mostly be public private is if you want to use DNS only within your VPC okay uh but this time we we just using uh public so type in your naked domain here and you can just create a hosted Zone when you do that you will see your domain over here for example I have this domain here awsy training.in which is which is a naked domain that I've created over here okay so I've created a I've added this naked domain into uh Route 53 and 

as you can see I already have some records uh in Route 53 uh normally when you create or add the domain into rout 53 you will see two records that are created and those are these two records the NS record and the SOA record remember I told you s SOA is like start of authority this will always be there by default don't delete this uh and NS is basically the name service so it's uh basically route is telling the whole world that if you have any questions 

about AWS training.in the name servers that are responsible for answering that question are these four name servers okay so all of the queries about AWS training.in will hit these four name servers and these four name servers will make use of all of these records that I've entered here uh in order to answer the question okay so once you add your domain name into R 53 you need to make sure that your domains name server matches these four records and once you 

do that you can then go ahead and start creating records so let's do that let's first start off and let me quickly create yeah let me quickly launch um maybe one or two instances and I'll just show you I'm just going to put a couple of simple websites on just give me one quick second 

so I'm creating an E2 instance which has a website on it and 

that in fact I'm just creating quickly couple of instances which I can show you how 

the routing works just give me two minutes 

okay so I have about three websites and 

we should be good let me okay as an example I have uh an 

ec2 okay I have an ec2 with a public IP address inside which I have basically installed this website okay this website is called editorial and right now as you can see I'm opening up this website with IP address right but I don't want to use IP address I want to use a name because I can't give this IP address to everyone else it's hard for them to remember it so I need I need to use TNS so what I'll do is I'll take this IP address which I will need and I'll go to Route 

53 and I will say create record okay now like I said you have multiple routing policies simple routing policy weighted geolocation Etc so let me first create a simple routing policy and show you how this works so I'll select simple routing policy I will keep a low detail of 1 minute because I'm just doing it now for temporary use and let's say I am creating this site called um site. awst 

training.in and I will put in this IP address over here as a value and it's an a record and a Rec cord basically means name to IP okay so the the website is basically site. awsy training.in and the value the IP address is this it's a simple routing policy and dtl is 60 seconds and I'm creating the record 

so as you can see here this is the record that's got created simple record for site. aw training.in that goes to that IP address now if I take this name and if I put this here and hit enter as you can see it works in fact you can try going to this website right now and see if it works go to site. awsh training.in site sit. awsy 

training.in you can go to the site and you can see it works so essentially I got a website up and running in under 5 minutes with the use of ec2 instances with some quick code in it along with DNS so it barely took me 5 minutes to put up a website does it work for anyone I do want to mention that if you do add your domain into Route 53 there is a cost of uh 50 cents per domain name 

per month so that's half a dollar uh per domain name per month okay so just keep that in mind it's not much of a charge but it's still a charge so keep that in mind did the website open up for anyone else okay so that is a simple routing policy so I have one server handling one 

IP okay that is one routing policy so let me just go ahead and create the other routing policies that I mentioned so for example I will create um a weighted routing policy and you guys need to actually play along with this because I will create something called W1 and I will actually use this website which is uh the other two servers one is called 40 and one is 

called massively so I have two other websites that I want to show you one is called massively and one is called 40 so I'll use these IP addresses to create so I'll again I I will basically create a weighted routing policy and I will say this and because this is 0 to 255 I will say a waiter dotting policy of um 126 6 

127 and then I will add another record and I will do the same thing W1 so it's the same record that I'm creating W1 aw training.in and W1 aw training.in but I'm sending this to two different IP addresses let me just show you that as you can see here the two values are different right the two values are different and I'm using Ved routing policy for both of them and the values are split 127 127 each okay but both of 

them are going to W1 aw7 training.in and if I make this to one minute make this also to one minute create the records okay I just need to give it a name so I think this belongs to massively so I'm just going to call this massively and I'm going to call this 4 so just a name for identification create 

records as you can see I have created a waiter routing policy for the same domain w. aw7 training.in so I want you to go to the site quickly and tell me what site are you getting so if I go to w. aw7 training.in I'm getting 40 please tell me what sites are you getting whoever is trying it quickly please anybody getting the massively website 

because ideally it's supposed to be 50-50 but like I said it's not exactly a load balance so you're not going to get exactly the correct split but okay so someone else caught massively anybody else who tried it D Chri got massively Harish and mohmad are you still on if you can just quickly tell me what you 

got Mohammad also got massively but as you can see I got 40 now if I refresh this I get massively because my TTL was uh 60 seconds right so uh the cach got cleared and now I'm getting massively right after 1 minute if I try this I will again get something else so that's basic basically the waiter routing policy similarly you can create 

your geolocation routing policy latency routing policy I mean I can't really demonstrate this to you right now because we are all in the same region if there were people from different regions we could actually test this out uh especially with latency is just a matter of um you know depending on where you are it'll give you a site so I can't really say what site you're going to get but just to show you uh what it would look like if you were to configure geolocation so if I where to configure geolocation I will get the option which says which location do you want to send 

so I have multiple options here I can say continent wise so Africa Antarctica Asia Europe North America Oceania and South America so I can send entire continents to a particular IP address or I can send it country-wise right so if I say uh for example India if I say everyone from India should only go to if I say everyone from India should only go to uh massively site then they 

will only get massively site they will not get any of the other ones regardless of how many times you refresh regardless of how many times your cash expires because I am um hard coding here saying that anyone coming from India will be routed to this IP address similarly I can do it for other countries as well the only thing that you need to uh remember additionally over here is that if you do select United States uh in US you actually get to send them statewise so if if you are 

selecting us you can actually redirect people uh based on States within us so you can send people from certain states to certain uh environments and certain other people from certain states to different environments so you could do that if you wish to okay um how is this going to be different when you have uh not IP addresses but for example if you had a load balancer right if you had a load balancer in inad of selecting an IP address over here you would actually select Alias so you would turn on Alias 

and you would choose an endpoint and you would say something like uh your your application load balancer right and then you would choose your region where your application load balancer is for example Mumbai and then if your load balancer is there created it will show up on the list but right now I don't have a load balancer created that's why it's obviously not showing up in the list but it's the same idea instead of an IP address you're going to use the load balancer so whatever instances are behind your load balancer that will load up now the last thing I want to show you here is um running a website off of 

S3 so if you go to your S3 buckets you can actually have uh websites running off of S3 as long as your bucket name matches the domain name for example you see over here I have a bucket name www. awsy training.in okay if you go in there it's basically some static web files so I have that bucket name there and if I go into um create a 

record I can say for example www it has to match the bucket name okay this is important if you're doing uh if you're sending uh websites to S3 so www. AWS training.in and here obviously I will select Alias because it's an S3 bucket so I'll select Alias and I will select S3 website endpoint and I will select okay where where is that bucket this bucket is 

in Mumbai I'll select Mumbai and okay uh the reason it's not showing up here is because I have already created this record but essentially it will just show up that bucket name over here and you just need to select that bucket name let me show you that record that's already created here is that record okay I've sent this to cloudfront let me 

see I've created somewhere else let me see ww why is it not 

retrieving canot retrieve okay I think that is because oh yeah um I've already created 

the WW record right so obviously it's not going to like allow me to create another one because it's a simple record if I had created it under weighted or if I had created it under geolocation or something like that then I can create multiple records of the same name but because it's a simple record it's not going to let me uh do that but uh let me see I think I have another bucket I can show you yeah so there is this site. AWS 

training.in yeah I think I can show you that let me actually edit this record so I'm editing this site. awsf training.in I will select Alias I will select a 3B endpoint that bucket is in North Virginia now that pocket is in Mumbai okay and I will select 

Mumbai okay there you go so I have a bucket called site. aw training.in so I selected endpoint I selected bucket name simple routing policy and save now because I actually overwrote a record remember this was already created this was the first one I just created when we started our Labs so obviously this is already casted in memory so it might not directly open up the bucket but let's 

see so it's still opening the cast information right so remember this is why TTL matters if you're constantly changing your environment if you keep your TTL too high uh then obviously people are going to get the old one right so let me see I think yeah there you go so the detail was just a one minute detail right so there you go this is actually the a site loading from S3 right so this site is basically a static website loading from the S3 bucket now I think I need to go back and 

answer that question of can you show the website running with ww and aw training.in right so let me show you that www. aw training. in this actually goes to another AWS bucket through a cloudfront distribution okay so here is a site www.7 training.in and okay I have actually set up a redirect 

hold on so aw7 training.in yeah let me do one thing let me edit this edit record 

so you see here I had actually already selected redirect so that gets redirected to this right this is the reason that it's actually going back to the WW it right but if I want I can just host a static website over here and I can say 

index.html I can save this and I go back to the bucket I can upload give me a second 

why is all of them failed 

okay so this is 

www.w training.in and then if I just take my browser might still redirect because it probably still has cach but let's see okay there you go so I I hope this answers your question that I can have completely different websites let me just refresh this to confirm so you can see I can have completely different websites on www. awon training.in and a.in right so this is what I meant by saying that they are completely different domains of course 

for convenience I can have it redirected some back to the same uh domain in order to avoid confusion because I don't want people to go to two different websites when they type the two different domains I just want to make sure they're in the same one right so any questions all right I think we have Tak up too much time today so I'm going to stop here for the day and hopefully once 

we come back U next week in our next session we can actually go ahead and do the remainder which is cloud front as well as Global accelerator if anybody has any questions please do post it in the chat uh and for those of you who are watching this after the after the live session if you're watching the recording uh please do post any questions that you have within within the uh comment section and we'll definitely try to answer it and uh if you're unable to do that you can always uh come to our 

Discord session and post it there so with that I'd like to thank everyone for listening in and let me hand it back over to sanchit
