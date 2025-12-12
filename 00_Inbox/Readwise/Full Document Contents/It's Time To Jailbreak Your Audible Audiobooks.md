# It's Time To Jailbreak Your Audible Audiobooks

![rw-book-cover](https://i.ytimg.com/vi/75QmbZTIbKM/maxresdefault.jpg)

## Metadata
- Author: [[dmg - (formerly Definitive Mac Upgrade Guide)]]
- Full Title: It's Time To Jailbreak Your Audible Audiobooks
- Category: #articles
- Document Tags: [[pkm]] 
- Summary: In this video, I reveal how Audible removed 12 of my purchased books from my library and show you how to take back control of your digital content. I walk you through:

✅ How to backup your entire Audible library without DRM in 3 minutes
✅ Creating your own private audiobook server using a $50 Raspberry Pi
✅ Accessing your audiobooks anywhere in the world with an internet connection

TIMESTAMPS:
0:00 - Why Backup your Library?
3:02 - Libation
4:00 - Tutorial with Libation
7:04 Creating my own web app

LINKS:
Blog post:
https://blog.greggant.com/posts/2025/05/02/jailbreak-audible-library.html

Libation 
https://getlibation.com/
https://github.com/rmcrackan/Libation

Raspberry Pi 4
https://www.audiobookshelf.org/

Personal Website for File Serving (Project in the video)
https://github.com/fuzzywalrus/website-for-fileserving

​⁠@DammitJeff - It's time to jailbreak your kindle
https://www.youtube.com/watch?v=Qtk7ERwlIAk
- URL: https://youtube.com/watch?v=75QmbZTIbKM&si=w7pKLW7x3NE6JP_u&utm_source=ZTQxO

## Full Document
Recently, when I was browsing my Audible library, I noticed 12 of my books are no longer available. These are all books that I bought, or rather used credits, same concept, with the implication that I purchased them. I gave Amazon money. They gave me a digital copy in return. However, they revoked my rights to access them. This ticked me off, so I decided to do something about it. And here's how you can, too. The solution is to download all the books without DRM, aka digital rights management, the copy protection. So, you can play these back 

on any device you see fit without a Audible subscription or application. I may have gone a little overboard as I ended up writing my own web application to create my own private audiobook server with a $50 Raspberry Pi so I could download my audiobooks from my phone anywhere in the world with an internet connection. The crazy part is it wasn't that difficult, especially the first part. This digital adventure started where many do. YouTube. I watched the video, It's Time to 

Jailbreak Your Kindle by Damn It Jeff, where he makes a damn compelling case why you should jailbreak your Kindle. Hence the title of this video, It's Time to Jailbreak Your Audible Library. This was a moment of inspiration for me. I'm a pretty big Audible fan. I've been a member since 2011 and I have a total of about 850 books in my library and I've spent over 15 months 16 days actively listening to Audible. It's pretty safe to say that audiobooks are my favorite form of digital entertainment. It's no secret that digital purchases are not 

the same thing as owning physical copies. Infamously, when Google sunseted its streaming service Stadia, gamers lost access to all their purchases. But Google made an attempt to make things correct by refunding everyone their purchases. Microsoft did the same thing when they closed their digital bookstore. I highlighted these two because they represent about the best case scenario and the exception to the rule. We have plenty of examples where the consumer gets nothing back. This has also happened on Amazon with various movies and TV shows like the WB TV show 

Final Space and on video game stores like Ubisoft with the game The Crew. This doesn't even begin to touch on services that have shut down like Ultraviolet, Nintendo's various ehops, Yahoo Music, and so on. There's also examples of individual episodes of TV shows being pulled from services, usually on the grounds of censorship, or sometimes offending material edited out or the music changing due to licensing. If you ever want to fall down an internet rabbit hole, people log the changes in TV show music, like that 70s 

Show, which has multiple versions of each episode with often entirely different music. I'd be here all day if I tried to list every time a digital store removed access to a movie, TV show, video game, book, or album, or otherwise altered them, thus removing access to the original media. But this video is here to help you, at least on the Audible front. Editor Greg here. At the time, I thought that take was fine, but I nearly flubbed every single line in that. Oh well, that's why I'm not a 

pro YouTuber. What makes this all possible is an open-source application called Libation that's available for Mac OS, Windows, and Linux. Open- source means free. It is largely the creation of just two developers, but it enables the ability to easily download your entire Audible library and losslessly remove the DRM. In other words, they'll back up your entire library in a file format that can be played back on a ton of different applications, and it does not require you to maintain an active Audible subscription or account. Even if 

Audible shut down its service tomorrow, you would still have access to your entire audiobook library using this solution. And it's not even that difficult to do. It just takes a few minutes. And that's why I want to do a quick tutorial to walk you through setting up and getting started with Libation. And if you're not particularly interested in following that, you can just skip ahead because I do more geeky experiments and build my own personal cloud service so I can serve up my audiobook library without Audible. The 

first step is to download Libation by going to the official GitHub page, then going to releases. Links are in the description. I am using Apple Silicon Mac for this demo, so I want a Mac ARM 64 version. Intel Mac users would want a x64 version and Windows users would want to nab the Windows version and so on. Fair warning, I'm going to take about 25 seconds, explain some Mac specific instructions, and then we'll move on. The first time you try to open Libation, Mac OS users will get a spooky message about Apple not being able to verify the 

application. This is because this is a unsigned application, meaning the software developers have not paid for an Apple developer account. For Mac OS 11 through 14, you can rightclick open to bypass this message. But in Mac OS 15, you need to whitelist this by going to the system preferences and then going to security and then clicking open. The process to whitelist applications may change in future versions of Mac OS. All right, that's enough Mac specific talk. Now that I've launched Libation, we'll be asked if we want to do the guided tour. If you're like me, your default 

inclination is to say no, but this makes life much easier as the guided tour will help us configure libation. This is pretty quick and straightforward, and we will follow the on-screen prompts. The first screen is the account section. Just type in your Audible email, and then be sure to fill out your location. The next tab lets you specify where you want to leave your books. I'm going to leave this as the default for this demo, but be warned, if you have a large library, it can use up a lot of space. For my 850-ish books, it takes up about 

roughly 400 gigabytes, so you may want to store them on another drive. In the import library tab, you probably don't want episodes as they are almost entirely podcasts and will clog up your library. I highly recommend unchecking them. Then, in the download decrypt section, there are two things I will change. The first one everyone should do, that is to change the setting when liberating books to retry later. That way, it will skip any problematic titles, like the ones that Audible has removed access to, and continue downloading the rest of your library. 

You can always attempt to redownload later. The other change I'm going to make is how it names folders. I prefer having my folders by the author name, then the book title. So, I'm going to edit this setting and then double click first author. So, it's now naming the folders by author name and title. In the audio files section, we want to leave this as lossless, so we're not going to lose any quality, but you have the option to reduce the quality for space if you would like. Finally, it'll prompt you for your Audible password. Just plug it in and it should automatically grab your library and display more oncreen 

prompts about how to search. After that, we are now ready to download our library. Just make sure the filter at the top is cleared out and then go to visible books menu and click liberate. This will take a fair amount of time depending on your internet connection and your library size. That is all it takes to back up your library of audiobooks and make them playable in different applications. I'm not going to cover individual applications. And I do have linked in the description of this video a blog post that has clients for various operating systems like Mac OS, 

Windows, iOS, and Android. Pretty cool, right? If you're like me, you prefer to carry around your audiobooks on a phone. Having the books stored on a random hard drive means I'd have to transfer them to my phone anytime I wanted to listen to a particular book. And that's kind of annoying. What I want to be able to do is download my books on my iPhone at any time like Audible. So that's where I decided to take this to the next level. In my hand is a Raspberry Pi 4. This is a $50 micro computer. And believe it or 

not, this is more than overkill for me to create my own personal web server that hosts all my audiobooks and serves them up via a website that I can use to download directly to my phone. First, I installed Raspberry Pi OS, a Linux flavor that's specifically designed for pies. Then, I configured my own Apache web server capable of running PHP. For the web developers and programmers out there, you're probably not very enthralled by these technologies, nor am I. But for everyone else, these are two core technologies that have powered the 

web for about 20 years now. Apache is a web server and PHP is a programming language that'll run within that environment. And both are super well supported and very well documented and most importantly will run on damn near anything. One of the reasons why Raspberry Pies are so great is there's tons of documentation for these guys. And if you get stuck, AI agents like Claude or Chat GPT can easily help you debug and configure them. Full disclosure, this is the first time I've used an SBC, a single board computer, 

aka little guys designed for lowcost, low power embedded computing projects. It's absolutely perfect for what I want to do. I do have a bit of a leg up here as a web developer, but I haven't created my own servers beyond development environments. So, this project was a bit of uncharted territory for me. However, this did not take much time. a weekend project I pulled off between going between two hikes. I'm not going to go into much detail here because I think one tutorial per video is enough. Plus, the blog post will cover all this in greater detail. The 

core software packages I installed were Apache, PHP, and Docker. I also bought my own domain name and mapped it to Cloudflare for additional security and privacy. Then, I configured a Cloudflare tunnel via Docker so my Raspberry Pi could connect to my domain name. This task would probably be the most difficult for most people, but it's kind of my job. So, I banged out a hyperminimalist web app. It's pretty cool. So, let's take a look at what I built. This web app lets me browse and search the contents of my web server, so I can directly download things to a 

device over the internet. Check this out. Let's search for Corey, as in James SA Corey, the last name of the pen name for the tag team duo of authors Daniel Abram and Ty Frank, writers of the popular series The Expanse. As expected, it'll search all the files on my web server and match anything with the name Corey. It also lets me view files that web browsers directly support. To demonstrate this, I've written a quick demo page that has instructions on how to download audiobooks to iOS. I basically created my own media server 

for about $70 and I could have gone cheaper. Oh, and I should probably mention that my media is stored on a Synology Naz, a networkattached storage device. I have my Raspberry Pi connected to it as a readonly client. That said, I could plug in any old USB drive or buy a bigger micro SD card and have an entire server self-contained. This code is all available on my GitHub for free. Now, do I expect most watchers to go to the lengths I did? Nah. You can use services like iCloud, Google Drive, Dropbox to 

aid storage or other web services to function as a private proxy for your book backups. The important point I'm trying to make is that you have plenty of options when it comes to backing up your personal media. And you can even recreate the conveniences of streaming services, whether it's jailbreaking a Kindle or creating your own personal media server using Plex or Jellyfin. Unfortunately, we are in a new era of media ownership or lack thereof where you could lose your entire library in a moment's notice. The only thing you can 

do to protect yourself is to take matters into your own hands. There are people fighting back like video game preservation movements and with the right to repair. Solutions will vary quite a bit between different media platforms and services, but I just want to contribute to this conversation in my very small way by demonstrating a completely self-owned solution. I hope you enjoyed this video and if you're already backing up your media, let me know how you're doing in the comments as I find this topic interesting.
