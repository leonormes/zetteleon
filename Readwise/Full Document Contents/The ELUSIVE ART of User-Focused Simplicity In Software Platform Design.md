# The ELUSIVE ART of User-Focused Simplicity In Software Platform Design

![rw-book-cover](https://i.ytimg.com/vi/IiShnllocNM/maxresdefault.jpg)

## Metadata
- Author: [[Modern Software Engineering]]
- Full Title: The ELUSIVE ART of User-Focused Simplicity In Software Platform Design
- Category: #articles
- Summary: Simplicity in software design is very hard to achieve but important. Removing unnecessary parts makes systems easier and more elegant. Good design balances simple common cases with flexible options for complex needs.
- URL: https://youtube.com/watch?v=IiShnllocNM&si=x1fB06WaVyAseiI-

## Full Document
I feel really conflicted about this one because because I' I've heard sort of I haven't seen the actual experiment which is fascinating in terms of like how big that difference is. But you know you see this argument a lot and you see it for example something like the React framework where people go this is just so huge it makes it big it makes it harder. What problem were we even trying to solve and let's go back to HTML? Um and I think perhaps because I'm a natural optimist I I find it really uncomfortable this idea that we're not making things better even though there is evidence that that we're not. And I think you're right that sometimes what 

we're we're getting is something that's more subtle. So we're getting, you know, better security or we're getting better browser, you know, compatibility or or something like that. Um, but yeah, it it does seem that we sort of we try and make things better and we make it worse, which is just sad. It seems to me it's the kind of complex adaptive system thing. You prod it in one place and it pops out in another and all of those kind those sorts of things. 

And that the pressures on a successful opensource producer are kind of different. You you want to keep releasing new stuff and so you end up growing something like Spring, which I thought started out as a nice simple thing and now is so massive and over complicated I don't want to use it to be honest. uh and and and and that seems like a common sort of trend 

uh very often. And I'm a I'm a I'm old and so I have a limited memory these days. So I I want uh I want stuff that's easy to think about. I I want I want the surface area of, you know, the tools that I use to be simple enough to help me and, you know, no more complicated than that idea. ideally clever but not not not but easy to use. Yeah. And simplicity is is absolutely the hardest thing to achieve. And it's 

hard to achieve and it's even harder to maintain because you're right that there is there's always new feature requirements. There's always and there's just always this sort of you know gravitational accumulation of of cr in a codebase but then also in the user interface. Yeah.
 And I think what makes it hard to talk about simplicity is is that there's sort of two kinds of simplicity, isn't there? So there's this sort of
 I think, you know, going back to that argument of I tried to do it the old way and it it was much simpler, but 

was I actually doing a like for like equivalent? You know, sometimes you can do something where you say, okay, I've just reimplemented this, you know, using basic HTML, using C, whatever. Look how small it is. And you've actually, you haven't implemented the same thing. you've just implemented the, you know, the really naive equivalent that looks superficially the same but isn't.
 Yeah. And that's, you know, that's sort of one argument about, oh, we're, you know, we need to be simpler. But then on the other hand, you do get the the cases where it the system is so elegant and you do have something that did achieve 

everything that it needed to and it did it while getting rid of a whole bunch of external complexity and a whole bunch of pitfalls for the user and that kind of thing. And I think that those systems are really really fantastic. So, so, so I I don't know whether this is an unfair question, but but what sorts of techniques would you use to try and achieve that kind of elegant 

simplicity rather than stupid simplicity? This is something that I I've been thinking about a lot. um partly be just because it's an interesting question. Um but I've I've so one thing I've been thinking about is you know sort of in the context of my day job which which is Quarkus and and you know we certainly believe that we've achieved something which you know is giving you that kind of double win where it's elegant and then it is easier to use and faster and better and and and all of that. But I 

think one of the ways that we did that is which I think is totally general generalizable is to look for the assumptions that are no longer true and then if you can carve out everything that's related to supporting this assumption that's no longer true then things if get a lot easier. So so with Quarkus for example and you know this is just one example of an assumption um Java used to be really heavily optimized for dynamism. So I used to work on OSGI and with OSGI the whole point the 

problem being solved was can I change the engine while the plane is flying and now we're running in containers you know you should not be sshing into your container to you know try and dynamically patch your Java runtime to like introduce new classes you know that is you should be using CI because CI is a thing and you know just rebuilding the whole thing. So all of this dynamism there was you know in terms of the um you know the sort of the runtime complexity there was a a tax being paid 

for it but then
 also in terms of just the the sort of the the architecture of the system and then the implications for how you programmed it. There was all this stuff related to dynamism that you just in 98% of the cases don't need. So if we get rid of that then, you know, things become easier. And I think there's probably equivalent, you know, answers from like other things where we can just say, well, wait a minute. Why are we why are we even doing this anymore? Let's get rid of this. And then it just takes this sort of cascade of 

other crap that we didn't want along with it. Yeah. Yeah. That that's an interesting idea. I I I I've I've thought about something a similar idea, I think, but from a slightly different angle. I I I I was kind of quite in influenced from a process point of view by lean ideas and the idea of trying to, you know, get more out for for less work. And so it's trying to take work out of the process and and and driving it that way. And 

that feels to me like a very similar idea to what you what you're describing is trying to find those ways in which you know we can remove stuff that we don't you know we remove those assumptions that we don't care about anymore. And it's it's again that part you can't really predict those things you know as you say the dynamism thing sounded like a decent you know a good idea at the time
 and it's just turned out that it wasn't good enough to to it wasn't as important as other things. 

Yeah. Or or it was necessary at the time, but the world the world changed
 or the world Yeah. one of those things. Absolutely. Um so, you know, we we we've got to kind of keep that focus. So one one one of the one of the techniques that I I think about and seems increasingly part of the way that I think about so software development is to be much more strongly outcome focused and sort of designing from the outside in rather than the 

inside out and thinking you know what's the minimum that a user of my my software needs to do to achieve whatever it is that they want to achieve and trying to make sure that I'm able to do that. I've always liked software that was that was doing clever things but was easy to use. There was a there was a years ago there was a um a a a paint program called Corell Draw which I thought was wonderful because it was elegantly simple much simpler than 

others at the time but you could do quite powerful things and I've always liked Gradel is a good example of that. Gradel, I can have a oneline build build script. If I if I want to take all of their suggestions, I just say um import Java or whatever the equivalent is. I can't remember now, but you know, it's a Java build and then I could just take the defaults and it will work. And I like that kind of that smartness, but I can override it and I can make it do smarter thing, tailor it if I need to. 

Yeah, I think that's another sort of Yeah. Oh, I've got two things to say so I need to remember because um because one I think that outside in perspective is so powerful and I think you know a really good team will have the combination of some people who are maybe outsiders so then they can bring that outside in perspective better and then the people with the deep knowledge because I I sometimes have with my team you know a conversation where I say well let's make it work like this because you know that's the nicest experience and then you know my colleagues will say well that's nice except it's impossible and I'm like okay well let's fix the fact that it's impossible and then we 

can you know because that's what it should And most things that seem impossible are are fixable eventually. But I think I think that idea of extending and going past the simple is really important too because you you know we have such a problem in our industry of kind of the demo wear, don't we? Or the sort of the the golden path which is surrounded by barbed wire. And so like you know as long as you're on the golden path you're like oh this is so great. this is so simple and then you want to do one tiny little other thing and then you spend you know 3 weeks reading the user manual and like 

fighting it and you know you just you can't and so you need to have it so that the you know the 80% of the use cases are really simple and the other 20% of the use cases they might not be easy but at least they're possible.
 Yeah. Yeah. It's I've always thought of that as the kind of low code problem. Yeah.
 Or as it used to be called before low code the 4GL problem. you know, you you you you kind of you have you build something that's good at do building things in a niche but step, you know, half a step outside the niche and it's either 

impossible or at least very hard.
 Yeah. Um and you know, there's a reason why general purpose programming languages are more popular. It's because they're general purpose and we can we can solve any problem that you can think of pretty much. This clip was taken from my podcast, The Engineering Room, with Dave Farley. A monthly podcast with some of the brightest minds in software engineering. You can find full episodes on all your favorite podcast platforms, including Spotify, Apple Podcasts, and Amazon Music. Your support helps us to 

bring you these regular episodes. So, please leave your positive review on your preferred podcast platform to help us to continue to grow and bring you great guests and their insights. Thank you very much for listening.
