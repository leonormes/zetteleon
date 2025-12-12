# Digitize Your Life | Deploying a Paperless Document System You Can Access Anywhere

![rw-book-cover](https://i.ytimg.com/vi/NcpOnOcMoA0/maxresdefault.jpg)

## Metadata
- Author: [[Twingate]]
- Full Title: Digitize Your Life | Deploying a Paperless Document System You Can Access Anywhere
- Category: #articles
- Document Note: **Background:** The author presents valuable insights and a novel approach regarding the implementation of a paperless document system. I am interested in evaluating whether these insights are indeed useful and if the author’s methodology offers any new perspectives.
   ### Top 3 Takeaways:
   📂 **Adopt a Centralized Storage Solution:** The author emphasizes the importance of having a single, centralized location for all digital documents. This not only streamlines access but also enhances organization and retrieval efficiency. Consider using cloud-based storage to ensure accessibility from anywhere.
   🛠️ **Implement an Efficient Tagging System:** A key insight shared is the implementation of a robust tagging system for documents. This enables quick searches and categorization, making it easier to find necessary files at a moment's notice. Evaluate your current system and think about how you can enhance it with tags.
   🔄 **Regularly Review and Update Your System:** The author suggests that a paperless system is not a one-time setup but requires ongoing maintenance. Schedule regular reviews of your document organization and ensure that your processes stay relevant and efficient, adapting as your needs change.
- Document Tags: [[pkm]] 
- Summary: Get started with Twingate for FREE - http://twingate.com/?source=youtube

In this video, we're going to talk about what I like to call digitizing your life. 

We'll walk through deploying an open-source solution called paperless-ngx in your own homelab or on a private server, allowing you to take all your important physical papers and transform them into a searchable, private, online archive, and best of all, how to securely access them when you need them from anywhere using Twingate.

Timestamps
00:00 Intro
00:53 What is Paperless-ngx
01:44 Installation and usage
05:36 Remote access solution
09:35 Automated backups
12:04 Recommended workflow

Mentioned links
Paperless-ngx - https://docs.paperless-ngx.com/
Twingate - http://twingate.com/?source=youtube
Twingate Reddit - https://www.reddit.com/r/twingate/
Code - https://github.com/travis-tg/twingate-yt-videos

#homelab #twingate
- URL: https://www.youtube.com/watch?v=NcpOnOcMoA0

## Full Document
Hey everyone, Travis here with Twin Gate. Today we're going to look at what I like to call digitizing your life with an open- source project called Paperless NGX. So, we have all these drawers full of papers we don't feel like we can ever throw away. Important invoices, tax returns, lab records, recipes, insurance policies, upcoming itineraries, whatever. And in my case, I'm running out of space. I have too many physical papers. And as a tech guy, whenever I identify these kinds of problems, I like to think, what could I deploy or set up to eliminate this problem? How can you 

take your many important papers lying about and digitize them all for good? Well, in today's video, I'm going to walk you through how you can deploy paperless NGX in your own home lab or on a private server to take all of those important papers, transform them into a searchable, private online archive, and best of all, how to securely access them when you need them from anywhere using Twig. Let's get started. So, Paperless NGX is a community supported open-source document management system that transforms your physical documents into a searchable online archive so you can 

keep well less paper. And one thing I really like is that it performs OCR or optical character recognition on the documents you upload, which means it extracts the text and associates it with that document in the database. Meaning you can then search your documents based on their content, not just file names or tags. Even images that then get converted to PDF get a text layer that can be searched. And this is all done under the hood with the OCR my PDF Python package. In addition, while the 

goal is to transfer your paper documents to its digital equivalent, it's also a great place to store long-term your important PDFs or ebooks or documents that are already on your computer, but you want to keep them in a more important and central location. So, first off, let's install it. So, there are multiple ways to install Paperless. We're going to use this nice interactive script that they provide to set up a docker compose installation on a spare Ubuntu server I have in my house. For more customization and say to set custom configuration options, you can use one of their docker compose templates. You 

can build the image and note that there are volumes that will persist as well as two bind mounts for export and consuming. So I'll grab this script and I have an SSH session to my Ubuntu server and I'm just simply going to paste it in and this should run the install process. Enter. What URL will it be available at? Well, it's going to be local host, so I can leave it blank. Which port? Let's change this to 801. Current time zone, America/ New York. And what 

database backend do I want? Postgress, SQLite, or Mariab. I'm just going to do SQLite for this demonstration. I don't want that. OCR language, I can keep that English. User ID, 1,00 is good. 10,00 for the group. And then it asks me about my target folders. So these all look good. Consume folder. Good. Media folder. Data folder. Paper list. Username. Let's keep it Travis. And 

password. Let's set a password to log in. Email's fine. And press any key to install. So again, this is the equivalent of these Docker Compose files. So you can choose SQLite here. The instructions on how to deploy it here. And it's basically the same thing but in a more interactive install. So press any key to install. And this should spin up my Docker image. And we can do a docker ps to see that the container is running. And with that I should be able to go to my IP 

address and port and access my new application. So here's paperless. Let's log in Travis and the password I set. And there we go. Now of course there's much more you can do here. You can add a TLSert, assign it a subdomain, make it more official. You'll have to configure that according to your own setup and liking in your private network. For now, we're going to stick with the IP address. So, let's upload a document. I have here just a mock document called lab results. I've put my very important lab results at the top and then just some Lauram Ipsum text. 

Again, realistically, this can be any document you can scan, take a photo of, or that lives on your computer. So, all I need to do is simply drag it in. And what happens now is it one performs OCR on the document. Two it creates an archable PDF/ a document from your document and three it performs automatic matching of tags and type before storing it in the database. And of course it always stores the original document. So once it uploads and processes I can then 

manually tag it. So let's add the tags of labs. Save that. And let's do 2025. Save that. Also, there weren't any tags yet, so it didn't look to do so automatically. And because it performs optical character recognition on your documents, you can search via any part of the text in it. So, let's save and close this. And we can search even for like Lauram. There it is. Lab results. So, for example, here's an error message that I have a screenshot of. I can search from that message even. So, let's 

drag that in and go to documents. So, because this has text, I can say was restarted just for example, and it's going to find that document. And there's much more to it. The documentation is great. So, be sure to check out the configuration options you have there as there's a lot of flexibility on storage paths and all that. You can set up paperless NGX to consume documents from your email accounts with mail rules that you set up. So, say anything you drag into a certain mail folder gets consumed by paperless NGX. You can also set up 

workflows that trigger specific actions along the document pipeline. So, lots of customization overall, but we have to now ask, what's the point of having all these important documents digitized in a private secure network if we can't then access them from anywhere when we need them? Well, we can, and we can do so securely with Twing. Twing will allow us to access any of our documents from our phones, our laptops, whatever, while away from our private network. And it does so without having to expose your private network to the public web. No inbound rules are required. So, if you 

haven't used Twin Gate, go to twinggate.com. Try Twin Gate for free and sign up. Just follow the prompts to create your network. So, I'm going to log in via Google to my network. And once you're in the admin panel, the first thing to do is to create a remote network. This is just a logical separation of resources. So, I'm going to call this home private network. So, hit the plus, change this to on premise, home private network. So, that's my remote network. 

Next, I need to deploy a connector within my private network. So, I'll go to connectors next. And you'll see when I created this remote network, I have two connectors created for me automatically. These are not deployed anywhere. They were just created. So, I'm going to delete one of these because I don't need high availability in my setup. So, let's delete this one. I just need one. So, I'll select this connector and I'll just deploy this as a Docker container on the same Ubuntu server. Click Docker. And then step two, I'll 

generate connector tokens. So click generate tokens. It's going to need me to authenticate again to do that. Step three, you can customize the Docker command. This is optional. And then step four, run the Docker command. You'll see here that all this is populated for us. All we have to do is copy it and deploy this connector in our private network. So I'm going to go back to my Ubuntu server. Let's clear this and run this command. And immediately you'll see that things are green status is connected and we're 

done there. So again we have our remote network our logical separation of resources that we've defined here. We've deployed a connector into our private network that's showing green and connected. Now we just have to add a resource. So let's go to resources. Click plus and let's add paperless ngx. So, I'm going to say paperless. That is at 1 192.168.1.11. And as far as ports, we can allow all ports. I'm going to make 

it a little more secure and only allow port 801 block UDP ports. And I also want to add an alias. So, I'm going to call this paperless. That gives us an alias to use instead of the IP address itself. So, click create resource. I'm going to give access to everyone. So, grant access and you're all set. So, now 

you're out in town and you need to access one of your documents, say on your mobile phone. Obviously, you can't just punch in your private IP address or type in paperless. It's not going to do anything. But with the Twin Gate client or app that I can download on my cell phone or my MacBook, whatever, you can log in and your resource will then be available for you to access. So you'll see here I'm not connected to my home network and I'll try to enter this IP address 801 and nothing will happen obviously because that's my private network. I'm not connected to it. You 

can't access those private resources on the public web. But if I open up Twgate and I log into my network, so sign in to connect. I'm going to use Google to sign in. I now see this application in my list. Again, I'm not connected to my home network, but I can choose, let's say, open in Chrome, and it's going to go to paperless. All I need to do is add the port on it, 8001. And there we have it. I can access my app from anywhere. So, here I just need to log in, Travis. Now, I go to my 

documents, and there's my lab records. Awesome. So finally, what good is this app if you aren't able to restore your documents should something go wrong? Let's go ahead and cover that. Here under administration, there's a section on backups and there's a command that you can run. So under making backups, choose document exporter and there's this command docker compose exec-t web server. So this is execing into our web server service and then running the command document exporter and then the location you want to export your 

documents to. But you'll note in the docker compose configuration here that we have a volume mount for the export directory this bind mount. So we should be able to export our data to that directory and thus save it on our host machine in the export folder. So if we go to our server and do an ls and go into the paperless ngx folder there's this export folder. We cd into it. There's nothing in it but we should be able to run this command docker compose exec-t web server. So, execing into the web server service, running document exporter and 

exporting to that directory, user source paperless export, which then should show up in this export folder on our host machine. Let's try it. So, let's CD into export and see what we got. And there we have our lab results and our screenshot and then some manifest and metadata information. So, let's create a script. Let's go back. Clear this. So, let's create a script. pseudovi paperless 

backup.sh. Put our bin bash at the top. Let's cd into that folder. So, home travis paperless ngx and get rid of that. And then run that command. And I'm going to put a - z at the end to zip it. That'll save us a little space. All right. So, let's save that. Let's make it executable. chod plus 

x. And then let's make sure this works. Let's run it. See what happens. And there's our zip. See if it has any data to it. Yep. So the final step is to add this to a cron job. So run cron tab e. So, put a 12 here to run it at 12 UTC every day and save it. And we have daily 

backups. And I'll be sure to provide a link to all of these code snippets down in the description. So, finally, let's look at a few tips that they suggest for creating a sustainable system here. So, Paperless NGX actually has a recommended workflow for managing your documents. So, it's great and all to upload documents, but how do you actually transform it into a system that you'll actually use? Well, here's their diagram. It all begins with tagging every document initially with an inbox tag. So let's create one called to-do. Every document that gets uploaded gets this to-do tag. So go to 

tags, click create, call this one to-do, and make sure you check the inbox tag box and save it. Now for every document you upload, it will initially get that to-do tag. Next, are you keeping the physical document? If yes, write an ASN or an archive serial number on it. scan it and archive it. And be sure to include that ASN in your digital copy as well. So you can open your document and add your ASN here to match. And if you're not keeping the physical 

document, scan it and then trash it. That's the whole point behind much of this. Next, tag appropriately. And then finally, remove the inbox tag. Now, let me remind you again to back up your data. This is important stuff, and you definitely don't want to lose it. So, what do you think? Do you have too many physical documents that could use some digitizing? Let's discuss below. If you have any twin gate questions or comments, you can leave them below. Or better yet, jump over to our subreddit and leave it there. There'll be a link below to that. Thanks for watching.
