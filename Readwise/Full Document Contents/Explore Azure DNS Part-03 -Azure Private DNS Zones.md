# Explore Azure DNS Part-03 -Azure Private DNS Zones

![rw-book-cover](https://i.ytimg.com/vi/lj64eVHnM-o/maxresdefault.jpg?sqp=-oaymwEmCIAKENAF8quKqQMa8AEB-AH-CYACqgWKAgwIABABGBMgUCh_MA8=&rs=AOn4CLCDUcmPtHRQVVZcWdxHGOdHHLBdIg)

## Metadata
- Author: [[cloud-labs]]
- Full Title: Explore Azure DNS Part-03 -Azure Private DNS Zones
- Category: #articles
- Summary: Azure Private DNS Zones help automatically register and manage internal DNS records without manual effort. You can link private DNS zones to virtual networks for easy name resolution across resources. This service supports many DNS record types and can handle thousands of records, making internal DNS simpler and more scalable.
- URL: https://www.youtube.com/watch?v=lj64eVHnM-o

## Full Document
okay today's video we're going to discuss uh another uh video for name resolution inure environment uh last two videos we discussed how do we to use as default DNS and and uh custom DNS in the name resolution 

in the of environment what we going to do today today we going to discuss the service is provide which is called is private DNS how do we going to use is private DNS in h environment so if I briefly explain this private DNS private DNS is a service as provide right for the uh name resolution 

uh we had a look what are the uh advantages and disadvantages when you're using each uh DNS method that in previous two videos so private DNS uh is a service we can create here in private DNS homes once you create a private DNS s uh you can link uh the wi uh to into 

that private uh DNS Zone and you can enable auto registration uh once you enable auto registration uh if you create any resource like a virtual machine in that link uh weit it will automatically create an register the record in private DNS Z so not like in using a custom DNS 

uh zones um it would prevent uh that overhead we have to create the um every single record manually so this is a uh easy way to create all internal uh DNS records uh without you manually involving right so the uh other uh advantage of private DNS 

is um it does support all DNS records like like if I see some examples like text records a records for a records uh server record Sr and then you can create mail exchanger record uh C canical Name Records and whatever DNS it does support that's a another 

Advantage so uh I briefly explain the uh limitations and the things you can use private DNS and one private DNS Zone can be linked up to uh 1,000 uh weix uh only 100 uh uh vits you can enable auto registration but 

up to, wies you can use for uh name resolution uh only thing again it can uh use for one DNS private DNS Zone can be linked to 100o registration uh BS but the other other thing is one private DNS support 25,000 uh record so we can huge number 

of record T about um all right uh now what we going to do is we going to uh I'm just getting my environment created here so we're going to create as I explain in this diagram so I'm going to create a private DNS on here and then I'm going to link 

private DNS on to these two v head office vit and B vit and we going to look into how it's registered records automatically and then we going to test uh whether the resolution Works in between them right all right let's get it started so I'm going to go to a oh this is all my resources being created uh that is the same thing I mean no any different in like I just r that 

script and got this 21 resources right right okay now let's create a private private DNS so this is what we going to do okay so create private DNS on 

okay so call it Cloud La ABC and go next Editor to edit anything here just going to go View and create it's running for final validation now okay PA and create 

so one other thing is auto registration is easy but still if you want man create records you still can create man in there I'm going to show you in the uh video later how do you going to create records as well but first 

just do book registration and see how registration works right Dey progress they are very quick won't take to long once this private DNS cre okay so spe done resour right so this is DN also you can 

see all of the properties here just go go to DNS management here record set you can add record set manually right okay so this is where you link vir Network link right so let's link this one first one Link Link name okay say head up here 

this link so this is head this link l link name must begin why all right YP underscore let me try something else okay that of 

is L sometime so here use and take this on for enable registration so this will register for my resources automatically right okay so creting virtual Network link 

so while is creating the link is going to update the record as well all right so it's seeing it's in prog right let's see when it's finish 

right probably be updating all the inside the should create records internet virtual machine server virtual machine and virtual machine so you go to over right is created here and see you can see four report 

here and virtu links one let me go to this one yeah you can see this through automatically has created all this three Machin right and recordes and you can even edit them right uh go this okay 

so I want to show you something okay go to home right get you see right to link s let one of them see that you can see that uh link 

right that this so This goes to which link and see provided DN okay so that one is done uh let's add second one as well so go add this br 

[Music] link probably okay so say so I can go with registration right but what I'm going to do is to show you how you going to create manually I'm not going to enable this one so enable AO registration so go 

create just going to create link but it's not going to create any records automatically virtual Network pleas is being created so you can see the link completed what your network registration is is enabled go 

back to internet disabled so can edit him here 

okay so what your links to right that what to show you when you create a uh private DNS Z this is the 

details just want to show you right this is good doing exam maybe they can ask so so number of Records this this private DNS S one record right of record that's what see uh 

maximum number of record this is record right so 25,000 you can number of virtual Network links right you can do, right and see number of network link with the registration you can go up to 100 right right so so that's what it is 

that's what it says okay let's go back Cloud right okay so let go toing let's go back into Branch one right so cck on BR one right see BR created and it says auto registration 

right record right so click that all right so what we going to do I'm going to create a one record right for the uh virtual Network link the second one right so go 

add name so it's a aord right leave it as it is so here the IP address 1 1926 

a this one the set see that ored PS right if you if if you click on registration when link uh link is is this one is going to 

uh uh register the dnf record but because of uh we haven't Ted on that hav come up with that all right let's go vir machines go to internet 

come SL bra copy just kind to loging into this mission 

body open a little some reason I don't know can paste open AC BR it in here 

asword just going to copy password all right I'm mute let me make it a little bit bigger you can see that contr L all right 

so [Music] we. ABC yes was to S out that one let's go 

into Cent [Music] region and let me BR to in was 

as well and what about [Music] ww.com yeah was able to sort out uh looking into Branch one now right this is H [Music] 

and 19 28 4 yes passw yeah I'm in a BRI in this look okay let's look up 

CL ABC yes PM yes we able to SC 

uh let me try sorry and look let try going into. google.com yeah funny so 

uh we are able to S out private TNS so so I showed you how to create a manual records as well um uh I think uh this is uh this is for this video and what we going to do uh we're going to discuss a few others uh 

top in the next video we're going to do looking into D it's not private DNS how do we uh how someone going to sold out or I sold the name from external to inter whatever internal let's say you put a web server or something how how do we resol that web server address someone looking from my outside external link um so if I quickly 

discuss the advantage advantage of this uh uh private DNS is it's make like very easy rather than using custom DNS sort of automatic registration and no overhead you can work up to thousands of me and 25,000 records in a one DNS Z so it's going to make it easy 

but again there are few uh things one thing if you if you need to use a conditional F sort of things is still private DNS we don't have option to enter that uh conditional forward um in say that uh I'm going to have end up this video and uh uh I see 

you uh you guys from next video thank you very much
