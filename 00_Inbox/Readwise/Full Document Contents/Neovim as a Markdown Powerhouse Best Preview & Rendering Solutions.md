# Neovim as a Markdown Powerhouse | Best Preview & Rendering Solutions

![rw-book-cover](https://i.ytimg.com/vi/TrbZlA4UIFU/maxresdefault.jpg)

## Metadata
- Author: [[MrJakob]]
- Full Title: Neovim as a Markdown Powerhouse | Best Preview & Rendering Solutions
- Category: #articles
- Summary: Neovim offers powerful plugins for previewing and rendering markdown files. The main tools discussed are Markdown Preview, Live Preview, and Render Markdown, each with unique features. These plugins help users see formatted markdown live, either in a browser or directly inside Neovim.
- URL: https://youtube.com/watch?v=TrbZlA4UIFU&si=VBAPj1fsUgFClu9x

## Full Document
hello and welcome back to another coding session with Mr Jacob as you have seen in my neovim from scratch series we actually can configure neovim from zero to a full-blown IDE for all of your development needs but there are a couple of things I want to tell you about neovim and its capabilities of integration and some of its plugins that may not be part of this series specifically but they are actually quite neat little and Nifty Things that we might want to use and one of those things are capabilities to properly 

render and display markdown or ease the working with markdown in general there are a couple of plugins for neovim which make working with markdown a little bit easier and nicer for us and today we want to concentrate on how to render and display markdown specifically therefore we want to take a look at three different plugins first of all we want to take a look on markdown preview then we want to take a look on the plug-in called live preview which kind of is an 

alternative to markdown preview and I will tell you why this might be a good alternative and then we will take a look at markdown at render markdown which actually is capable of rendering markdown within the neovim itself okay so let's go ahead and start taking a look markdown preview actually is the first thing that comes up if you Google something like I need a markdown previewing and rendering plug-in for neovim it is a very capable thing that 

allows you to render your markdown in a live fashion in a browser side by side to your neovim and display it there with all kinds of bells and wh whistles it is actually a neat little thing that runs uh note. JS server in the background that then connects to the browser and to the neovim on the other side and then all actions will actually be transferred using web sockets to this browser so that you have really a life update of what you are writing let's take a quick look on how this looks 

after we have installed it and then we will talk about why you might not want to use that specifically so as always we are simply scrolling down here to a section where we have the corresponding entries for our uh package manager which in our Cas case is lazy envin um if you want to know how to install that and you haven't followed my neovim from scratch series I have linked the playlist up there in the corner for you okay so we 

can actually decide if we want to install the thing with yarn or npm or if we want to do that without I have yarn or npm on my system so I simply copy this part here and go here into my uh plugins directory now just one of the ones that I have open there then I go into my file browser here and create something new that I call markdown preview. L okay we are saving that we are actually going into that that file then 

we are returning our plug-in configuration as we do already so often with all the other plugins we are cleaning it up a little bit and now we need to make sure that it actually calls not yarn but npm because I am using npm here in this configuration and actually not yarn okay so everything else can stay as it is it simply configures on what file types it should work what commands it should actually um be triggered on to load this plugin lazily and all of that stuff so that is a proper lazy enm configuration nice so we 

Simply Save that we now go out of our plug-in where I uh of our neovim where I obviously updated our readme we need to save that so now let's restart neovim which now should install markdown preview it calls the build step which in term is only done once it is installing now everything using npm so please make sure to have a note JS set up with npm or yarn if you just copy the example from the homepage uh ready to be run and 

running uh on your system when and before installing that okay so now we have everything installed so let's maybe see what happens if I now go back to my read me file here and take a look at the the usage instructions of this thing there are a couple of of configuration options that we can actually take here and that we can um use here but essentially what we want to do is we want to call markdown preview so let's 

call the markdown preview command but first of all let's move our browser window over to our newm or better besides it okay there we are so now we actually can call markdown preview and what now what now happens is automatically the server is started in the background and it will be uh connected to this document here via websockets and a really nice thing here actually is that if I scroll in this 

document it will actually scroll around in the document on the right side as well it will properly show this one so I think I can now x that out here and as you can see it automatically updated this preview here the same thing with if I write something new here um thank you for watching please consider subscribing and likeing 

so as you can see this is automatically updated so um yeah if I if I actually do anything to the markdown on the left here in my neovim it will automatically move over to the right side uh where it actually shows everything that we do there properly formatted and properly styled with the uh GitHub CSS styling actually it will do code as well so if I for example have something here like I'm adding a Jon something here so uh let me 

add a code block here which is Jon which um for example something like the answer uh as a key answer come on and it's 42 and now we have something like um question is still being processed therefore it's false you can actually see that it even does syntax highlighting of sorts so it has come on my browser is is getting in the way there so um actually we can have we have 

syntax highlighting here which um highlights the different languages there as well um if I do for example something else like for example let's do JavaScript and I have um a let's say a console. loock thanks for watching you can see that it understands um if my browser is not getting in the way there please go out of the way that it understands 

different languages and does different highlighting schemes for that as well okay um as we need those code blocks here for a different presentation later on with live preview and render markdown I will just keep them there for now and delete them later before pushing this to the repository which you by the way can find in the link Down Below in the video description okay as you have seen now we have marked down preview so why do we need something else like live prev preview which kind of sounds the same 

there is a problem with markdown preview actually even though this is a highly sophisticated plug-in which does exactly what it should and works very well we have a slight problem it depends on this nodejs server in the background which normally wouldn't be a a big problem just install node.js and have it ready ready for your system to to do markdown preview rendering However unfortunately this plug-in hasn't been really 

maintained for about 2 years because the author says uh for himself that he hasn't the time to do it actually the problem with that is that the dependencies used in This nodejs Server are kind of outdated by now so there are actually some which might have some security bucks in them to which could be exploited so if you have something like that running your new machine you might be um yeah in danger so to speak if you don't take care of 

that so please be aware of that if you use that plug-in here um it shouldn't be a problem if you are aware and take the corresponding precautions but please be aware of that okay so um if anyone of You by the way out there knows if there is a fork of this thing that is still maintained please give me a hint in the comments because I couldn't find one and I really liked this plugin for a long time until I discovered that it isn't maintained anymore and that we have this sort of problem there okay so let's take 

a look at live preview which might be a different thing here that can help us out so live preview actually is another plugin for neovin specifically that wants to take care of this live previewing in the browser thingy there and it actually doesn't only want to do that with markdown but with um HTML and um asy do as well as SVG so um let's quickly install that and then I will 

tell you what the differences are or what the main differences are so uh where is actually the installation I think I scrolled over it yeah there lazy envm we simply open that up we copy that as always so let's go into our plugins directory here let's do a live uh preview. Lua let's quickly create that file let's go into that file let's return the thing that we copied from the internet here here let's clean up our dependencies a 

little because this plug-in actually supports or has a functionality which needs um a file picker and it can either use telescope it can use fzf Lua or it can use mini pick we are using fzf Lua in our setup if you are in a neovim setup that uses something differently then just use the different one there please so we don't need um telescope we don't need mini pick what we don't but we need fzf Lu so we are ready here let's go out of neovim again let's restart it it will install the plugin 

there it is already started and if we now take a look at the usage here on the right side then we can see that of course we can configure it with some options there but it tells us that we should take a look at the help Pages within neovim uh on how to actually use that thing and how to configure it and I actually like that if a plug-in has a proper neovim based documentation so if we go into our documentation Chooser here and do a live preview search we see 

ah cool there it is so we can now scroll down there is the configuration we don't want to change anything from the default yet so uh we go a little bit further to usage and there we see okay we could issue a live preview start command and that should actually then uh Monitor and live preview the current document okay nice so let's do that let's go into our read me file again and let's issue a live preview start and as you can see there it is we have a 

live preview it isn't looking as fancy as um it was before and this here is actually a problem with my show Keys which I haven't fixed yet um it has nothing to do with live preview so um it doesn't look that sophisticated than markdown preview because it doesn't use that much styling it hasn't implementation for some of the markdown features like for example the checklist here and stuff like that but the basic feature set is actually the same so if I scroll around here it will scroll around 

in my browser it has syntax highlighting actually a a VAR A variation of syntax highlighting which I quite like a little bit better than the one that markdown uh um markdown preview actually generates but nevertheless it's there I can actually um update something Lively so if I mark this one here and delete it you will see that it's simply deleted the whole paragraph here so as you can see it is working out it is live updating 

stuff okay so um it is an alternative and the the best of all is it doesn't have any external dependencies because the whole websocket server and the whole server thing that it is need that it needs to actually render things and update them in your browser are written fully in lure within neovim so it doesn't have any external dependencies um it uses a couple of JavaScript 

libraries within the browser here to render stuff to highlight stuff um to do all the the the um this um the syntax highlighting and stuff like that but um it doesn't actually need any other dependency on your system which is quite nice it isn't as powerful as um the markdown preview but it hasn't the problem of this outdated note JS thingy there and it actually comes with and that integration I actually like it 

comes with an integration for um as I've said fzf Lua so if I do live previe pick here it will actually create um a a Chooser window here which will allow me to actually select which one I want to render um it will display all of the possible files that it can render at live preview and the one that you select will actually do the trick then so if I go ahead and just select Fu here and press enter you will see that it 

switched to uh this document here which is a simple HTML which is lying in the same um folder there that is then displayed just in my browser here on the right side automatically so I can easily configure that for example to a key binding and then could easily call that up and tell the system I want to preview a specific document which I have open somewhere uh nevertheless I mostly just type in the live preview start command because that's the thing I'm currently 

working with okay so um let's uh see what we can actually do here with another plugin that I have already mentioned here which is render markdown so let's just cross out the live preview here and let's talk quickly about render markdown I will move my browser over to a single screen so that everything is fine again we don't need this split screen anym now so there we are so now let's open up Renda markdown Renda markdown actually is quite an interesting idea it is an idea of 

rendering markdown within the neovim editor using uni code and nerd fonts and icon fonts and all that stuff together to make something up that looks like render markdown at least as close as possible to it so uh let's see what that actually looks like how we can actually use it and what it does so we are simply going here to installation um and wait a second where are we there lazy envm as 

as always we copy the thing for our package manager which is lazy envm we go back to our browser which needs to quickly resize here um we can uh now save the read me again and uh quickly go into our plugins directory we create a new file there which we simply call render markdown DOL let's save that to create the file and let's get in here to [Music] 

return whatever we just copied there okay so now we have a couple of entries here and the first one actually is the dependency on envm treesitter so it needs tree sitter to be capable of having all the different elements of markdown ready and to format them so if you haven't Trea installed or want to have details on that please check out the linked uh video I have on that in our neovim from scratch series up in the right corner so otherwise you already have that installed you don't need to 

worry about that just leave it in the dependency line nevertheless we are actually using uh not the full the full mini envm here we are using only the mini envm icons so I actually remov that line and you can see that in the next line which was until now hidden behind my face here I think um that there is actually a line uh using mini envm icons um as a dependency we don't use envm vde icon so that's just if you are using some other um setup there for the icon 

font and icon rendering then simply use this one please it's just that you can use it in different environments okay so um we actually only have some comments here about um the typing that we could use for autoc completion and stuff like that and we have the options table here which we for now leave at the default options we will change that uh in a couple of seconds SL minutes here um after have shown you what I want to 

configure there actually and what I think is a better configuration for uh render markdown so let me save that let's go out of here let's start up neovim again and there we see random markdown installed perfectly so we are going out of that we are going into our read me file and now you can see that this already looks quite different um it has now rendered this markdown file within neovim it um actually created neat little icons for all our links here 

um it kind of has these nice little code blocks here which are by the way highlighted correctly as you can see here they have those texts which show you um in the document as well as in the gut bar here that uh there is a specific language block here at this position they show you those neat little language icons um you have different headings denoted with this uh one here or um a little bit further down we have a heading of type three and so on and so 

on so we actually have a rendered markdown and we have this neat little check boxes here and as you can see if I'm going over those lines we are showing actually the uh the real uh the Real Deals so to speak we are showing what is actually um uh in this file as a raw text and if I now switch to insert mode it shows us the raw document mostly and that is a kind of a problem 

that I want to address with a couple of options in a second the problem that I have with that is that it is not perfectly showing the raw document when I'm in insert mode but that is what I would want so it's not showing us full links for example we only get them if we uh let me see if we go up there and we go into insert mode only if we are on the line itself and now you can't see that properly because it's um Ah that's that's a little bit 

uh uh bad so let's do something like hello and I want to link that to uh let's say Google um Google come on um so I now have this link and of course this Now does not work why doesn't it work okay that's uh that's strange what did I do there did I do do it the wrong way no 

the the that's the link syntax isn't it okay that's did I just somehow break the rendering some Hello link okay it doesn't like the link here why um that's strange actually it should work I think 

oh because we yeah because of another problem because we are in a JavaScript block uh we are actually still in this text block and we didn't even unfortunately see that uh and that's another problem so now we have our link but as you can see even if I'm in insert mode um it shows me still the link only when I'm on that line and and that's the most problematic thing you don't see the start and end of cod blocks you don't even see their language anymore because 

I'm in editing mode and we can only see this end of the block or this start of the block if our cursor is on top of that and I'm not sure if this is a buck or it's actually uh meant to be this way however I have found a quite easy way to configure this thing in a way that really works for me um by simply saying I only want in the normal command or terminal mode to have this rendering of a markdown and in insert mode I want it 

to be completely disabled and I just want the raw markdown let's see how we can actually do that by taking a look at the Rena markdown uh Vicky here so we go into the Vicki we simply uh take a look at where is it installation I think and there is an example and there are actually our render mode options so we can tell the render markdown that it should only render in normal mode in command mode and in terminal mode which actually makes perfect sense otherwise 

it I think it will choose some kind of intelligent mixture as we have seen but I don't like that intelligent mixture very much so let's quickly go into our render markdown plugin here let's go into the options Let's uh paste our new config option there let's quickly re quickly reent not so quickly but yeah let's reent this file um and let's go out of that one let's save our read me it's 

already I've destroyed that Beyond repair I think and I need to uh get that back from the uh repository in the end from the git but nevertheless let's go into our read me file again and as you can see we still have our rendering everything is neat and nice but if I now change to insert mode it's actually the raw mark down there so I now have my link regardless of uh if I'm on the line or not I have my code block descriptor here which say okay this is um a code 

block here and it starts and ends at a specific position so while I'm editing this thing for example creating quickly a table something like uh Fu and bar and we have a divider here and a divider there and then maybe we have just a and b and we have C and D or something like that you can see it's a perfect neat little asy table in markdown syntax but if I now go out of that into my um 

normal mode you will see that it renders everything really nice and neat it understands a lot and a lot of different syntax specifications that are mostly understood by GitHub for example and other markdown rendering systems so if we for example create a call out we could do something like creating a call out here and saying okay uh this is a note and if I now remembered correctly how to do this and I remembered correctly it seems we can see that it 

actually creates this call out as well um so um I think there are others like was it war or warning I think it is maybe warning then yeah warning for example you see they get different colors get different styling icons and so on so it is really neat and nice rendering markdown within your Kno him and I actually used this plug-in for uh quite some time until I real I ized most of the time I like to be in this raw 

editing mode and it's fully okay for me to just have correctly syntax highlighted markdown and I have correctly syntax highlighted markdown already so that's perfectly fine for me and if I need something more complicated to see how that works for example if I have a complex table or if I have some images included there and stuff like that then I actually now use live preview which I do seldomly but I use to just see okay how would this look in an 

HTML rendered document so that's what I do that's how I do that but that is the nice thing on neovim you can configure your environment in any way you see fit therefore I just wanted to show you those three different possibilities that are actually available at your fingertips if you are using neovim for a neater and better markdown editing experience so I hope you enjoyed this video you learned something and you 

might give it a thumbs up if you did so so please subscribe and hit the Bell you know the drill if you want to be informed once a new video is out on this channel and if you have any questions or you want to hint me at something for example tell me that there is a nice little markdown preview Branch out there which which is still maintained please leave me a comment and otherwise if you just liked the video please leave me a comment as well so uh the Youtube algorithm really likes kind of likes as well as comments and 

interaction in a video so if you want to help me out a little comment this video please so uh yeah I hope to see you in the next one until then bye
