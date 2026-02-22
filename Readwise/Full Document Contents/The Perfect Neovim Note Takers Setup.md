# The Perfect Neovim Note Takers Setup

![rw-book-cover](https://i.ytimg.com/vi/DgKI4hZ4EEI/maxresdefault.jpg)

## Metadata
- Author: [[DevOps Toolbox]]
- Full Title: The Perfect Neovim Note Takers Setup
- Category: #articles
- Summary: This video shows how to use Neovim for taking great markdown notes with helpful plugins like markdown envm. It explains how to make notes look good and easy to read, including features like call outs and code block icons. The author also shares tools for previewing and managing notes, plus tips for using Obsidian with Neovim.
- URL: https://youtube.com/watch?v=DgKI4hZ4EEI&si=fc0sfI--lLl4beB6

## Full Document
taking good notes with neovim is more than just 
a cool thing to do if you're a Vim or NVM User   it's essential having your most productive 
text editing space serve as your primary not   taking tool is probably the best thing you can 
do for your writing and note taking system I've   previously covered how I built my second brain 
video link above and even a system to make your   NE your writing partner but the missing piece 
in this Trilogy assuming you're already set   with these is making markdown my format of choice 
not only look great but also function as if it's   

ingrained into the editor by the end of this video 
my goal is to make neovim such a great markdown   utility that it wouldn't make any sense to even 
consider an alternative with that in mind let's   review this system for n markdown notet takers 
and I'll share a surprise at the end about taking   your writings and notes out of your machine and 
into the wild ready let's go the first and most   important everyday add-on in my eyes is rendering 
markdown so that it's not only visually pleasing   

but also easier to track most envin kickstarters 
comes with some markdown for matter that knows   how to differentiate headings by using different 
colors and highlighting code Boxes Etc but it's   never good enough and mostly good up to a point if 
you use tables checkboxes or modern callouts they   will either be completely unsupported or lacking 
in many ways for this reason and many others for   a while I decided taking on nework as the system 
and format of choice it worked great and you're   

welcome to check the video I made about it up 
here but eventually it wasn't markdown it required   learning new syntax and relying on something most 
Frameworks and tools you'll see further in this   video don't support this brings me to markdown 
envm a relatively new plugin gaining popularity   and does a great job with all of the above you'll 
see headlines turn into numbered icons lists and   nested lists add visually distinct separators 
tables renders as they would in the browser and   even latex get attention to start exploring these 
options let's install the plugin by adding it to   

Lazy I'm using the defaults here but this thing is 
fully customizable to the level of specific icons   nesting levels and shape of separators it uses Tre 
seater and one of two icon packages you can choose   from to create the visuals you will see next since 
Nick's home manager is now taking care of my DOT   files and the video is up here if you're curious 
I'm running home manager switch to populate the   changes let's take a nice R me to use as an 
example my teamac session XR me is perfect for   

that out of the box you can already see multiple 
new visuals headings are marked with their   level while the image isn't rendered and I don't 
bother with integrating that into neovim I'll add   relevant resources in the description if you're 
interested another cool addition is marking code   blocks in a few ways first it marks the formatter 
and if the language is known it gets a nice icon   next to it the block is also highlighted from 
the top to bottom so it's easier to track let's   create a new test mark markdown file to explore 
the rest of the features next to the convenient   

little Flags added to the headlines for even extra 
readability go code gets a nice gopher making   things easier on the Eye Quotes are also rendered 
nicer with a heavy border next to them that both   marks the block and separates it from surrounding 
text and here's a real visual game changer tables   are perfectly drawn around what's used to be 
only half baked presentations of other plugins   I'm probably going to get comments in the known 
style of IMX headed for GE bro I know not using ax   

therefore I get to be excited going back to titles 
the nested icons go pretty deep I can't remember   when was the last time I used even a fourth level 
nested title but anyway this thing covers way more   to-do L also get attention marking undone tasks 
done and delayed ones this is actually one space   where the obsidian plugin does a little bit 
better job but it's nitpicking and we'll get   to obsidian users in a bit one of the most widely 
used patterns in mark is numbered list and bullet   

points this was one thing I absolutely loved about 
newor it visually separated different nesting   levels of bullet points beautifully and I missed 
it so much after going back to markdown well with   markdown enim it comes back this is a Tipping 
Point where I think the rendered markdown becomes   even better than the real life web rendered 
version moving on to a recent markdown Edition   call outs call outs add visual blocks you may 
have already seen around GitHub with tips warning   

examples Etc all wrapped like code blocks markdown 
EnV supports call outs with many options you   probably can't remember alone from notes through 
tips warnings dangers success bugs examples and   quotes there's a call out for anything it renders 
beautifully as a block on neovim on GitHub and if   you're an obsidian user I recently discovered 
it's supported beautifully in the obsidian UI   as well and I've been take a quick break and 
thank the sponsor of this video ever worried   about the security of your remote work setup 
today's sponsor twin gate has got you covered   

twin gate is a modern cloud-based alternative to 
traditional vpns it provide secure remote access   to your company's network resources making it 
easier and safer for teams to work from anywhere   with twing gate you get easy setup in minutes 
instead of days you get seamless user experience   across all of your devices and enhanced security 
based on zero trust principles want to see how Twi   gate can transform your remote work security visit 
tate.com to start your free Tru the and experience   

the future of secure remote access twin gate also 
offers a free plan of up to five users perfect for   small teams or to test the waters now back to the 
video markdown envm is amazing but sometimes even   that's not enough not because it's lacking but a 
it may be beautiful but you want to know exactly   what it's going to look like in production and 
B you may have lots of images videos or other   integrated Media or non-media that just requires 
web rendering for these my my weapon of choice   

is markdown preview a quick add to Lazy with the 
defaults and I'll pause to remind you that this   and every other config you see are publicly 
available on my DOT file so feel free to copy   or use it for reference with markdown preview 
installed one simple markdown preview and Vim   command and the browser pops with a rendered file 
beyond the perfect preview the plug-in also tracks   your NE Vim movements so you can scroll through 
the text jump up and down or move between search   results and the browser tracks everything updates 
in real time and help you finish your work no more   

of the days of pushing to GitHub just to see if 
the table is rendered like I planned it real devs   testing production so there's a way to render a 
neovim and a browser tracking file changes enough   isn't it well not quite there's another must 
command line tool that does some magic markdown   rendering named glow glow belongs to the amazing 
sueto charm bracelet it can be installed via any   package manager yes including NYX and can serve 
in two main ways the first if we run glow file the   

file is directly rendered and sent back as output 
the second and much nicer way in my opinion is   its TW mode run glow alone and it'll show a fuzzy 
Searcher with locally available markdown files in   the current path you can use standard motions to 
scroll between them hit enter to open one where   it's sent to a page of utility like less then you 
can scroll through read within the render document   and step back to the list when you're done glow 
has its own way of parsing markdown and it's   been my go go to for quick rendering that doesn't 
require a dedicated plug-in opening the browser   

and other hassles a quick CLI and a visually 
pleasing UI on top if you're a dedicated notaker   you've probably heard of obsidian now I'm not 
advocating for obsidian use but it's definitely my   choice when it comes to General notes and a second 
brain system specifically after trying notion Rome   research raw apple notes and just a notebook I've 
been a longtime user of obsidian and for me it's   the absolute best one of the reasons I like it 
so much is its easy portability to neim with a   

plugin called obsidian envm which if you go to its 
page and check out the title It'll point you to an   excellent YouTube video for a preview so feel free 
to check out the video I made about obsidian any   of him later but let's give you a quick tldr after 
a quick installation I'll open my notes folder   there's a reason for this structure this is called 
a second brain so instead of placing a sponsored   segment here I'll just tell you that last year I 
made a minicourse where I explain the basics of   a second brain after reading multiple books on a 
topic I built a second brain from scratch and add   

x-ray to help anyone build their system from zero 
no prior knowledge needed I show the integration   with neovim and go through all of the features and 
it even includes a recording of a live follow-up   workshop with students asking questions and 
me answering them if you're interested in   building a second brain with neovim in under 
90 minutes the link is down below use the code   special 10 off for a 10% discount as a thank 
you for being an awesome viewer maybe even a   subscriber back to our video obsidian comes with 
a large option menu inside neovim you can use it   

to create new notes it injects raw front matter to 
help you later with classification and discovery   of noes it can help you link to existing noes 
which is one of the superpowers of having a note   system and it can follow links from within yourm 
with a dedicated command of its own it's worth   mentioning that obsidian and Vim comes with its 
own markdown for matter and it can sometimes clash   with markdown envm it's probably wise to this 
able obsidian as the markdown UI if you're using   

markdown envm as I do within the plugins read 
me within a nice node call out there's a short   config line to help you do exactly that lastly I 
promised a surprise and I'm not going to let you   down if you want to start your own blog maybe put 
your note system in public for everyone to see an   Envy or simply run a local web server rendering 
your note structure quartz is for you all you   have to do to start using quartz is clone the repo 
and after installing all the dependencies with npm   install run npx quartz create and either 
change the settings or follow the defaults   

and don't worry it's all configurable later as 
well from this point you can start serving by   running npx quartz build minus minus serve let's 
pop the browser on local hostport 8080 showing   a nice index which is the default note under the 
content directory from this point anything under   content will be rendered and served I'll grab 
an old version of my notes back when I first   spelled it and place the entire thing as is inside 
content now check this one out similar to obsidian   

if you're familiar with it it shows a beautiful 
graph of notes with topics links preview popups   and even tags anything you can ask for if you 
want to really take words even a step further and   deploy it remotely while you can do it on your own 
rather easily the docs take you hand inand running   it on cloud flare pages and like I mentioned 
earlier this is a great way of publishing a   new blog straight from a local markdown directory 
on your machine what more can you ask for let me   know what you think of the idea in the comments 
below and whether you've found other uses for   

quartz also feel free to share links to your 
blogs or other systems running on quartz in   the wild with markdown all set up you're good to 
go but are you making the most out of neovim as   a tool for writers here's your next watch where I 
explore pushing the limits of neovim making it an   incredible writing system even authors use thank 
you for watching and I'll see you on the next one
