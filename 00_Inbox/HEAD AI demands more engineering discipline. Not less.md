---
captured: 2026-06-17T10:35:35+01:00 2026-06-17T10:35:35+01:00
created: 2026-06-17T09:35:37+00:00
modified: 2026-07-20T16:34:36+00:00
permalink: llmeon/20-thinking/21-workbench/head-ai-demands-more-engineering-discipline.-not-less
source: https://charitydotwtf.substack.com/p/ai-demands-more-engineering-discipline
status: processing
tags: [input]
title: HEAD AI demands more engineering discipline. Not less
type: head
---

## Raw Output / Content

A few days back I wrote a piece called " [AI enthusiasts are in a race against time, AI skeptics are in a race against entropy](https://charitydotwtf.substack.com/p/ai-enthusiasts-are-in-a-race-against)."

I have notes on a whole pile of AI-related topics that I'd like to cover in depth: AI mandates, communication norms, code review, AI art, and more. Unfortunately, I got too many interesting responses to my last piece, and now I have to address those before I can move on to other topics. 😉

There were two types of interesting responses: the first on the technical merits, the second on ethical grounds. I will respond to each of these separately. Let's take the technical side first, because it's easier.

Somehow, a subset of readers came away believing I was telling everyone to ditch code review and push their shittiest code straight into production without reading it, _right now,_ tout suite.[^1]

That is not what I am doing. That is not what I think you _should_ do. But I did not pick that example at random, and I will tell you why.

![](https://substackcdn.com/image/fetch/$s_!3g6N!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F87a779c4-2e63-495a-aa1b-b44f1558a24f_903x241.png)

## In 2025, the Question Was whether AI Could Ever Generate "Good" cOde

It's easy to forget, but for most of 2025, the idea that AI-generated code was slop and might always be slop was not only a reasonable position to hold, it was the default, mainstream position.[^2]

That question was answered decisively last November. Ever since Opus 4.5 came out, AI has been able to generate code that is approximately as good as that of the median software engineer, at least for common patterns, and much faster and more cheaply. I came out of a book hole and realized this in January, and over the first few months of 2026, it seemed like everyone around me was having a similar realization.

But many saw it coming much sooner.

The popular narrative holds that Opus 4.5 was what changed. But Opus 4.5 was more like the tipping point. Agentic harnesses (the code that wraps the LLM in a loop with tools) became a real thing in mid 2025, with precursors building back to late 2024. Tool use, function calling, MCPs…all of this wave was building over the course of 2025, and crested into real general purpose usability at the end of the year.

That's what the enthusiasts were trying to tell us last year. Not only "this is coming", but "this is coming faster than you think."

As it turns out, they were right.

## It Was Reasonable to Be Skeptical the First time

As you may know, I come from the reliability side of the house. The compliment I will pay to myself and my people is that we do not struggle to adapt to new realities. As soon as a problem is real and in front of us, we adjust smoothly, even eagerly, thanks to an unwholesome zest for lapping up disgusting technical messes (and the campfire tales we get to tell later).

![](https://substackcdn.com/image/fetch/$s_!jEKP!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F60b0224a-8572-43fa-85d5-0579487ed15f_787x301.png)

The un-compliment I will pay myself and my people is that we sometimes struggle to accept that _progress is real_, that the continued existence of bugs and edge cases does not diminish the fact that huge swaths of problem space do get more-or-less solved over time, to the point they can be taken for granted by most people.[^3]

The speed at which code went from total crap to "ah damn, that's not bad" is what I have in the back of my mind, as enthusiasts are telling us that harness engineering and AI validation is real, it's already here, and it's getting better astonishingly fast.

Holding out for "I'll believe it when I see it" was forgivable the first time, but much less so the second time. This is what it feels like to be on the inside of an exponential change curve, turns out.[^4]

## What Happened in 2025, Exactly?

I want to pause here and be very clear about what I think is happening. Then I'm going to tell you what specifically I am excited about, and why.

You are under no obligation to join me there. But there are way too many sweeping statements out there right now about "it was never X"—"it was always Y"—"the future belongs to xyzzy" 🤮—and I want to be crystal clear how conditional and specific and contextual my claims are.

What happened in 2025 was this: the economics of code production were turned upside down. Instead of being very hard, time-consuming, and expensive to generate code, it became effectively free and instant. Lines of code went from being treasured, reused, cared for and carefully curated, to being disposable and regenerable, practically overnight.

For most of computing history, the primary way people have learned to understand software is by writing the code. Once you've achieved some mastery, reading and discussing code gets you most of the way there. (I might argue that software engineers have always relied far too heavily on _the code_ instead of sensemaking _the system_ through observability.)

![](https://substackcdn.com/image/fetch/$s_!3-TF!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb45ec2a6-8f65-4ece-af9f-27720fbbaeb2_779x318.png)

## "The rEal pRoduct of a sOftware tEam is sHared uNderstanding"

Many great software engineers hold that true product of every (good) software engineering team has always been a shared understanding of the software we own. That it gets stored as cache state in our fragile little meat brains, frequently flushed to disk, deployed to production, committed to github, but our minds are where meaning has always lived.

Is it any wonder that software has always been such a fiercely collectivist endeavor, exquisitely sensitive to relationship dynamics and manners and questions of fairness and emotional valence? It's exactly what you'd expect when part of your brain lives in other people's brains, and your collective interdependence is sky high.

It's something that I love about this industry. But there's no denying that minds have been a poor container for certain aspects of the software development model. We are forgetful, distractible, impatient. We are bad at spotting small details, we grow habituated to repetition. Worst of all, the model in our heads diverges massively and perpetually from the world our users interact with.

Anyway, SREs have never quite bought that explanation. To us, it's clear that the true product of every (good) software engineering team is production.

Only prod is prod. Test in prod, or live a lie.

(This is all backstory. I am getting to the point, I promise.)

## Turns Out, This is an Engineering Problem after All

We issued our AI mandate last August.[^5] I had seen enough to know that this was happening, and it was time to do the responsible thing. [Honeycomb](http://honeycomb.io/) is a devtools company, and people come to us to help with hard problems on the forefront of technology. I was all in on AI, but I can't say I was super excited about it, in my heart of hearts.[^6]

![](https://substackcdn.com/image/fetch/$s_!lHkQ!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf09736c-8384-4a8b-8055-0e629d3c70f6_786x296.png)

Then I found Chad Fowler's writings on [Phoenix Architectures](https://aicoding.leaflet.pub/).

If you don't know what I'm talking about, you should honestly stop reading my shit right now and [go read his](https://aicoding.leaflet.pub/). Chad is the guy who coined the term " [immutable infrastructure](https://chadfowler.com/articles/trash-your-servers-and-burn-your-code.html) " in 2013. His best-known essay is " [Relocating Rigor](https://aicoding.leaflet.pub/3mbrvhyye4k2e) ", because Martin Fowler [^7] mentioned it [recapping a Thoughtworks meetup](https://www.thoughtworks.com/about-us/events/the-future-of-software-development) on the future of software. I replied with " [Production Is Where the Rigor Goes](https://www.honeycomb.io/blog/production-is-where-the-rigor-goes) ", complaining that they didn't talk about production enough.

When I wrote that, I think "Relocating Rigor" was the only piece I had read. But soon I found the rest of it, and after reading two or three essays, it _just_ _clicked_. I knew exactly what he was talking about. I could predict the rest of what he was going to say. And then, reader…then I got _excited_.

## This Has All Happened Before, and This Will All Happen Again

I am going to give you a small sample of Chad quotes, just enough to get the gist. Here's one from " [The Death and Rebirth of Programming](https://aicoding.leaflet.pub/3malrv6poy22a) ".

> Immutable infrastructure. Stateless services. Containers. Blue-green deployments. Infrastructure as code.
>
> These ideas all share a common premise: never fix a running thing. Replace it.
>
> AI pushes this premise beyond infrastructure and into application code itself. When rewriting is cheap, editing in place becomes risky. Mutation accumulates entropy. Replacement resets it.

Another favorite: " [The Deletion Test](https://aicoding.leaflet.pub/3md5ftetaes2e) ".

![](https://substackcdn.com/image/fetch/$s_!WxpU!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98d0d940-6230-4da3-8f73-38d275b056bc_779x295.png)

> Here's a simple test you can apply to any software system you work on:
>
> Imagine deleting the entire implementation.
>
> Most engineers experience deletion as existential. Code feels like _the thing_. It's what we write, review, version, deploy, and debug. Losing it feels like losing the system itself.
>
> When people say, "We can't just throw the code away," what they usually mean is something more precise:
>
> - We don't know exactly what behavior is required.
> - We don't know which failures are unacceptable.
> - We don't know what invariants must always hold.
> - We don't know how to tell if a new version is correct.
> - We don't know which bugs are intentional fixes for forgotten edge cases.
> 
> Those are not code problems. They are evaluation problems.
>
> Code becomes precious when it is the only place knowledge lives.

and,

![](https://substackcdn.com/image/fetch/$s_!TaBS!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8910be06-8ab1-4348-a6c2-63c426bc93b6_782x333.png)

> For most of software history, treating code as durable was reasonable.
>
> We treated code as permanent because the labor to produce it was the bottleneck. Rewriting was expensive. Re-validation was risky. Implementations accumulated meaning over time. Structure, tests, comments, bug fixes, and tribal knowledge fused into something you learned not to disturb.
>
> That made sense when production was the constraint.
>
> When regeneration is easy, code stops being an asset and starts acting as a cache: a materialized view of understanding that is useful while current, disposable when stale.

" _A materialized view of understanding that is useful while current, disposable when stale_." I think that might have been the exact line that made it click in my head.

## Do You Remember the Sysadmins?

I am just barely old enough that my first job title was "System Administrator". I was a teenager, working at the university, with root on every machine in the days before they learned they should definitely _not do that_.[^8]

I lived through the shift from handcrafted server pets to immutable infrastructure cattle. I didn't really understand what was happening at the time, but I've contemplated it a lot in recent years. I wrote this in the final chapter of "Observability Engineering", 2nd edition (available for download as of Wednesday, June 17th!):

> The shift from handcrafted servers to immutable infrastructure taught us that mutability is the sworn enemy of understanding. Any artifact that is edited in place creates drift. Drift is what makes systems impossible to maintain.
>
> Our ability to kill and regenerate infrastructure components is the reason we trust it. At Honeycomb, we kill the oldest Kafka node off via cron every Tuesday. That's why we are confident in our bootstrapping and balancing processes: everything is repeatable, the data can be regenerated, the commitments live elsewhere.
>
> The fact that we cannot regenerate our code in the same way is a sign that we do not understand it. We do not know which commitments we have made, we do not know which dependencies will break. We find them by breaking them, mostly.

![](https://substackcdn.com/image/fetch/$s_!_xw8!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3181579b-618e-4ef5-b7da-33756cc15ff8_888x281.png)

Think of all the years of your working life you have wasted on painful migrations and rewrites. Think of replacing load-bearing legacy code. Think of all the [strangler figs](https://martinfowler.com/bliki/StranglerFigApplication.html).

Lines of code have been doing _too much_. The code has been the bundled up repository of developer intent, user expectations, implicit and explicit behaviors, the only fossilized composite record we have of bugs gone by. It's too much!

## Lines of Code Are not the Ideal Artifact to Review

And look at all the domains that have been neglected due to the towering, all-consuming expense of maintaining and mutating lines of code. Where are the artifacts I can review and discuss to understand how our architecture is evolving? Where are our architecture artifacts, period? What if we could discuss and converge on an architecture diagram, and the code could be regenerated from changes to the architecture, instead of the architecture being kinda-sorta inferred from the code?

I am _not_ asserting that all code will eventually be AI-generated to spec, bypassing human understanding. The feasibility of this whole endeavor hangs on the question of what a spec is, or what a spec could be. Anyone who has ever done a painful database migration should have learned some goddamn humility about our ability to extract and formalize users' expectations in a replayable, automate-able way.

But I think that every step we can take in that direction will be _good for us_.

The tools to do this don't exist yet, but many of the ideas do exist. Most come from operations and QA, two domains that software engineering has historically been rather snobbish about.

Those tests and techniques are not about testing for correctness or what _ought_ to be happening, they are about observing and encoding what _is_ happening. Behavioral tests, characterization tests, capture/replay, traffic splitters. Observability (the good kind).

![](https://substackcdn.com/image/fetch/$s_!2r_p!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0156e490-2a09-4246-af73-6d6264cf5324_792x274.png)

## Our Brains Were not Built for Validation

Having nondeterministic code in production is finally forcing us to do the things we should have done all along. Instrumenting with traces. Tests and evals in production. Production is not what happens after development is over, production is a stage of development.

Human brains are _not good_ at validation. The nitpickiness, the repetition. This is the worst thing to be clinging to, y'all. There are so many better things for us to want to preserve and assert for ourselves in the production and maintenance of software. We are never going to beat the machine when it comes to _validation_—we are literally the weakest link!

My money's on humans for a good long time when it comes to creativity, inspiration, leaps of logic, and a lot of other things, but PLEASE do not rest your killer argument for humans in software on us being the best _quality gate_. OMG. 🙈

Alright. I'm almost done here. Just one more thing.

## Nondeterministic Systems Will Require More Engineering Discipline, not less

I think what many engineers have found so alienating and terrifying about the last two years of AI discourse has been the way so many prominent AI voices appear to be gleefully declaring that software is no longer an engineering problem. " [SaaS is dead](https://www.forrester.com/blogs/saas-as-we-know-it-is-dead-how-to-survive-the-saas-pocalypse/)!" " [Making AI great at coding was the strategy that unlocks everything else](https://www.linkedin.com/pulse/something-big-happening-matt-shumer-so5he/) ", and so on. Even [Adam Jacob](https://www.adamhjk.com/blog/as-we-build-so-we-believe/), one of my dearest friends and someone who is rarely wrong about technology, seems to anticipate a bloodbath of software jobs.[^9]

If 2025 was the year of vibe coding, where AI got as good at generating lines of code as the median software engineer, and the range of possible futures often felt destabilizingly, impossibly wide open, I feel like 2026 is shaping up to be a return to discipline.

![](https://substackcdn.com/image/fetch/$s_!HQKd!,w_1456,c_limit,f_webp,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F60407b92-d6c2-4436-8f5b-cf9b33fdb42f_860x282.png)

The knowledge in our heads is unavailable to AI until we encode it into the system, after all. The returns on those investments will be massive and nonlinear. We might argue that they always would have paid for themselves in the long run. But now every CEO in existence is chomping at the bit to get some of those AI cookies, so let's give it to them. Discipline first, cookies second.

## This is Our Chance to Bring Our Engineering Values to the Mainstream

The share of software engineering teams that work in short, fast feedback loops (the cardinal sign of discipline in my book) is, and always has been, appallingly small. Five percent, maybe? Definitely less than 10%. AI tooling [brings this more within reach](https://www.honeycomb.io/blog/you-had-one-job-why-twenty-years-of-devops-has-failed-to-do-it) than ever before. Or it can. It could. The discontinuous returns on investment in engineering discipline are real enough that it just might happen.

I am not worried, at least in the near term, about AI creating massive, discontinuous returns on investment in the absence of engineering discipline. (Many will try, and it will be entertaining to watch.)

But value is backed by durability, not disposability, and I don't see that changing. Bits are cheap and fast and governed by the rules of logic and language, but anything with value must ultimately resolve with physical systems: persistence on the one side, user experience on the other.

People _do not want_ to wake up every day and log in to Slack and find the buttons and menus all subtly moved around. People _do not want_ financial transactions that complete most of the time. Determinism is not going anywhere, my friends.

AI is not magic. This is still engineering. As Adam says, "it's still technology, and technology needs technologists." And I for one am looking forward to learning new and interesting engineering problems, reviewing different kinds of artifacts.

And _never_ doing another sticky, picky, two year long API rewrite or strangler fig migration, ever, _ever_ again.

_~charity_

P.S. Thanks to everyone who read a draft and gave me feedback: Dave Williams, Chad Fowler, Adam Jacob, Mark Ferlatte, Austin Parker, Erwin van der Koogh, Ankur Bhatt.

Seriously, that was our big pitch. Learn AI _so that_ you can complain more effectively.

I think those people are bad at math. The only thing we know for certain about exponential growth is that _it will end_. It always does. either in an S curve or a crash. (For a good time, google Heinz van Foerster and "our great-great grandchildren will be squeezed to death.")

I definitely think we will use machines to build the machines—duh, we already are—but that's about recursion and specialization. I think the exponential curve we are on the inside of now was created by sloshy free money chasing high returns, plus the properties of software as a function of language and logic, plus the biggest discoveries always happen in the early days of a technology boom, because low hanging fruit gets picked first.

My personal sense—and keep in mind that I am no kind of expert on AI—is that the exponential advancement in AI models leveled out a while ago, and gains are becoming harder to earn and more incremental in nature. I may turn out to be very wrong, of course. But even if there were no more AI innovations moving forwards, the past year has unleashed enough pent-up force to radically reshape the software industry as we know it. Like a pig in a python, we will be dealing with the consequences for a long time to come.

Hold your desire to jump in and berate me here, I beg you. Like I said, I will deal with the ethics and morality of using AI in my very next post. Be honest, your attention span is no more up for reading a 10,000-word essay than mine is up for writing one. (Can we blame AI for that too?)

[^1]: I was not _trying_ to be neutral or even-handed in my last piece, only to give a baseline of courtesy to everyone. But I think it's revealing how many times I was accused of being "so overly hard on skeptics", by skeptics, and "so overly hard on enthusiasts", by enthusiasts, and sometimes simply "It's sad how some people can't accept reality" with no indication which side they meant. Lord.
[^2]: Fred Hebert and I gave [the closing keynote at SRECon](https://www.usenix.org/conference/srecon25americas/presentation/majors) in March of 2025 where we told SREs they should get to know AI, [maybe even try vibe coding](https://charitydotwtf.substack.com/p/my-hypothetical-srecon26-keynote) (pause for laughs), because otherwise their critiques wouldn't land as well.
[^3]: Infrastructure, for example. I think this is true of a lot of engineers, btw. I just think it's really _really_ true of the type of engineer that signs up to be an SRE. Technological pessimism and ADHD, our two most defining traits.
[^4]: There is a segment of AI enthusiasts who believe we are entering an era of eternal exponential growth, in which the machines begin to build better and better machines, in ways we cannot understand.
[^5]: More on this coming EXTREMELY soon. Watch the [Honeycomb](http://honeycomb.io/blog) blog!
[^6]: The tech is cool, but as a thinking, feeling, breathing human who cares about other people, it can be hard to get excited about anything that so many people are this upset about. It's also hard to get excited about something when so many of the loudest voices are out there talking gleefully about putting everyone permanently out of work, and so many artists and writers and people from developing nations are talking openly about the impact on them.
[^7]: "The Other Fowler." I gather they've been making this joke for like.. fifty years.
[^8]: I share a longer version of this story in the second edition of "Observability Engineering, chapter 32, downloadable later _this week_!!"
[^9]: Adam is rarely wrong about technology, and I am 100% sure he is living and working in \_ _a_ \_ future of software engineering. I am less sure it is the future we will all be living in. If the hardest part of software has never been writing code—as is my belief—it logically follows that even if the economics of code production drop to zero, the hard parts will still be hard.
