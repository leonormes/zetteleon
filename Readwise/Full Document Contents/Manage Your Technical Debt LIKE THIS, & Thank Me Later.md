# Manage Your Technical Debt LIKE THIS, & Thank Me Later

![rw-book-cover](https://i.ytimg.com/vi/Bq8w2fkyDnk/maxresdefault.jpg)

## Metadata
- Author: [[Modern Software Engineering]]
- Full Title: Manage Your Technical Debt LIKE THIS, & Thank Me Later
- Category: #articles
- Summary: Technical debt is like code debt that slows development if not managed well. The best way to handle it is by regular refactoring using good tools and skilled developers. Experts can help coach teams to improve code quality and keep software easy to change.
- URL: https://youtube.com/watch?v=Bq8w2fkyDnk&si=NNmCTDD2C5Q44vu5

## Full Document
Technical debt slows down new development. And if you let it get out of hand, everyone loses. Features take longer, bugs proliferate, and most of all, developers are miserable working with difficult, complex code and designs that are out of touch with real user needs. So what is the best strategy for handling technical debt? [Music] 

Hi, I'm Emily Bich. I'm a software developer and creator of Saman Coaching. Welcome to the modern software engineering channel where you can find world-class advice for the technical aspects of software engineering, how to build software using modern approaches, and wider commentary on our industry. Now, I expect you already have a general understanding of technical debt, especially if you've been watching Dave Farley's channel for a while, but I think it's useful to be specific about 

what we mean before I tell you about the best strategy to handle it. So, Ward Cunningham coined this term back in the 1990s to describe what happens if your internal code design gets out of sync with the business needs that the software supports. He says, "Shipping firsttime code is like going into debt. A little debt speeds development so long as it is paid back promptly with refactoring. The danger occurs when the debt is not repaid. Every minute spent 

on code that is not quite right for the programming task of the moment counts as interest on that debt. entire engineering organizations can be brought to a standstill under the debt load of an unfactored implementation. Now, this description is useful because it describes how depth happens. You you do what you need for the first version of the functionality to get it to work. But building software is a process of learning and as you learn, you realize 

there are better ways of designing the code. But you can't always just immediately update all of the design to reflect what you've learned. You need to get the first version out of the door and then improve the design. And if you don't do that promptly, new development slows down. The thing about modern software engineering is that we're doing continuous delivery. So we are continually learning new things that the software needs to do. There is a constant push for change and it is basically impossible to predict in 

advance what design you should have to support what's coming up. So essentially there will always be some technical debt and Ward Cunningham warns us about the dire consequences of technical debt that doesn't get addressed. It is entire engineering organizations that get brought to a standstill. So there are several ways to address this problem of technical debt and generative AI tools is one of them which I'm going to talk about in a minute. But before that I need to address a common 

misconception. Technical debt is not the same as bad code. As Dave Farley has said on many occasions, quality in software is defined by our ability to change it. And there are some code designs where we can say with certainty that they are not going to be easy to change in any direction. This is a property of the code itself. Bad code is so complex that everyone finds it difficult to read and everyone finds it difficult to change 

without breaking it. Static analysis tools can be good at spotting this kind of code. Tools like Sona Cube and Code Scene or Coarity, anything that will examine the source code and highlight things like excessively long lines, big classes, deep nesting, circular dependencies, all those kinds of things. code that has those problems is going to be difficult to change purely because the design is so complex it's no longer possible for ordinary human people to fully grasp what it does and nobody sets 

out to write code that complex. I hope it usually happens over time when several people are in making small unrelated changes that together add up to a big complex picture. So bad code is complex and hard to read. Technical debt is slightly different because it's not a property of the code itself. It's caused by your awareness of the situation you're in. Technical debt 

is a mismatch between the design as it is and the design you now realize you want to have given your current need to change the code. Static analysis tools can find bad code, but they cannot identify technical debt unless they also know what design changes you need to make next. So what I'm trying to say is that refactoring towards a different design is an essential aspect to tackling both bad code and technical debt and everyone 

doing modern software engineering will need a strategy for when to refactor. I would like to thank our channel sponsors who support us so that we can carry on making all these videos for you. Our sponsors are equal experts, transfig companies. They all have products and services that are very well aligned with the kinds of topics we talk about here on this channel. So, please do take a 

moment follow their links in the video description. The first strategy for tackling technical debt is the rewrite. You declare that the code is bad and you decide to just rewrite it from scratch. And this is very attractive to lots of developers because you change the task from one of refactoring into something you're probably good at and trained to do, developing new code. So a lot of developers do prefer new development work over refactoring. and they will 

just say code is bad when in fact it just has some technical debt and could be refactored. A rewrite can be a good choice sometimes particularly if the business needs have changed and it seems like they want an entirely different product. So then the the complete rewrite might give you an opportunity to build something with more capability in a a better way. But if all the functionality basically needs to say the same and the actual problem is that the the code is difficult to understand, 

then I'm not sure a big rewrite will really solve the problem. It could just cost a lot of time and money and the code might not be that much better afterwards either. Refactoring is an essential skill for creating flexible code designs and also when it comes to dealing with legacy code. So the main alternative to a big rewrite is a small rewrite, a ship of thesis approach where you break apart and replace the system one plank at a time. It's less risky, but it can still be expensive and you 

will still need refactoring skills to isolate those planks that you're going to replace. So how about instead of any kind of rewrites, we focus on taking the code as it is and improving the design through refactoring. We could do that by bringing in a cleaning crew of expert specialists who are very skilled with refactoring and they can use a a static analysis tool to show where to find all the bad code. Although bad code is not technical debt as I as I mentioned 

earlier unless you also need to change it. So a better approach to find where to start is to plot a graph like this. Complexity against frequency of change. This is called hotspot analysis. So the the code that you really need to worry about refactoring is the code that is both complex and changes often. And that's something you can measure and manage. So you can bring in your crack cleaning squad of expert refactoring specialists and put them onto the the worst hot spots in your code. And for some 

developers, that's their dream job. It can be really satisfying to clean up bad code. And this strategy will also keep your other developers happy because the people who enjoy writing new code can go and write new code and and leave the legacy refactoring to the experts. So on paper, this sounds like a great strategy. Your crack squad quickly makes an impact on your static analysis scores and and then you can redeploy them on a different codebase and soon all of your code quality dashboards are looking 

better. Okay, so rather than a crack squad of refactoring humans, what about if we ask a gen AI tool to improve the design? These tools are pretty universal these days. Everyone's got like co-pilot or chat GPT or something and they're great help often to write better code. Perhaps they could do the necessary refactoring. You may detect a note of skepticism here. The thing is these tools are good at many things, but so far refactoring doesn't seem to be one of them. This 

paper refactoring versus refactoring came out recently. They did a systematic study. They benchmarked the refactoring abilities of large language models on refactoring tasks for improving real world code. These tools did badly. They only refactored correctly in 37% of cases and the rest of the time the design either got worse or they introduced bugs. 

Maybe in a few years these gen AI tools will catch up, but actually I think they will fundamentally need to change the way they work on your code. Martin Fowler defined what's known as the refactoring Rubicon, the river you have to cross before you actually count something as a refactoring tool. He says refactoring tools have to analyze and manipulate the par tree of the program. That is the refactoring tool needs to keep an internal model of the programmatic structure of your code, not 

only the text of it. So when a refactoring tool is doing its work, it's manipulating this par tree structure and then translating that back into text that it can put in your editor. Now the current crop of AI tools are large language models. They are purely working at the level of the text in your code which is why they just can't accurately or reliably refactor it. Maybe that will change. 

But it brings me to the best strategy that I know for technical debt. That is you need to enable the developers who ordinarily work with the code to refactor it as part of their job and get them to do that using proven deterministic tools. You probably already have these tools built into your IDE and I often find people who are not making full use of them. I mean things like not only rename but extract function, inline function, introduce variable, introduce parameter, move 

method. I use things all the time. A lot of developers though never had any training in how to refactor and it's not something that comes up necessarily in an ordinary computer science education. So it might not actually take that long for a coach or a trainer to teach everyone the basics so that all the developers can get good enough to avoid technical debt building up. Apart from refactoring skill and tools, 

you need a policy and a culture of when ordinary developers should do this kind of tidying and refactoring. And I think rather than just using this hotspot analysis to find the most important bits of code to focus on, it's probably simpler just to have a preparatory refactoring or tidy first strategy. What I mean is like for every development task, you identify the part of the code that needs to change and as 

part of that task, you just spend some time improving that design before you start building the feature. If you've got a lot of technical debt already and some bad code, it can help to have that crack cleaning squad available. But not, as I mentioned before, to come in and take over and do everything. You need experts to come in and enable or coach, lead the ordinary developers through a particularly difficult refactoring and let them understand the 

tools and the techniques that they need to use for their code and take it from there. That's what a good technical coach would be able to do with a team. If you're looking to improve your refactoring skills, you can find lots of exercises to practice on and expert help through the SAM society that I organize. We have free events and a newsletter. And I've also written a free guide for how to use code carters for learning refactoring. There is a link to that in 

the show notes. I'd like to end by thanking all the members of my Patreon and the Patreon for this modern software engineering channel who support our work and remind you that there are additional resources available if you join. Happy coding. [Music]
