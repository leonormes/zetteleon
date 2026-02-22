# Fermyon Built a WebAssembly Cloud to Push Serverless Microservices Beyond Containers

![rw-book-cover](https://cdn.infoq.com/statics_s2_20221117075519/styles/static/images/logo/logo-big.jpg)

## Metadata
- Author: [[InfoQ]]
- Full Title: Fermyon Built a WebAssembly Cloud to Push Serverless Microservices Beyond Containers
- Category: #articles
- Summary: InfoQ's newsletter highlights trends in architecture, team design, and scaling engineering orgs. Podcasts and talks cover DDD, Team Topologies, hybrid leadership, and the engineer/manager tradeoffs. Resources and events help teams learn about scalable systems and migrations like SQL→NoSQL.
- URL: infoq.com

## Full Document
[![InfoQ .NET Trends Report 2022](https://cdn.infoq.com/statics_s2_20221117075519/experiments/homepage_trend_reports/styles/img/NET-2022-thumb.jpg)](https://www.infoq.com/articles/dotnet-trends-2022/)[InfoQ .NET Trends Report 2022](https://www.infoq.com/articles/dotnet-trends-2022/)
[![How To Build Payment Systems That Scale to Infinity (Live Webinar Dec 13th, 2022) - Save Your Seat](https://imgopt.infoq.com/fit-in/150x192/filters:quality(80)/sponsorship/rsc/a2e9cdbe-ebe9-42e3-9046-041d6565a5bd/cover/CLRSC-1667905227050.jpg)](https://www.infoq.com/vendorcontent/show.action?vcr=a2e9cdbe-ebe9-42e3-9046-041d6565a5bd&itm_source=infoq&itm_medium=VCR&itm_campaign=vcr_homePage_click&itm_content=bottom&vcrPlace=RVC&pageType=HOMEPAGE)
 

|  |  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 

|  |  |  |  |  |  |  |
| --- | --- | --- | --- | --- | --- | --- |
| Welcome to the InfoQ Software Architects' Newsletter! Each month, we bring you essential news and experience from industry peers on emerging patterns and technologies. This month, we focus on "From One to Many: Architects, Staff Plus Engineering, and Optimizing Teams". These core topics currently span the entire "diffusion of innovation" graph in this year's [Architecture and Design InfoQ Trends Report](https://www.infoq.com/articles/architecture-trends-2022/?utm_source=infoqEmail&utm_medium=editorial&utm_campaign=ArchitectNL&utm_content=11252022). We see increasing adoption of architecture decision records (ADRs), senior individual contributor (IC) career tracks, and team topologies. Key challenges remain in this space, including being conscious about how architecture decisions are made at scale (and with the required speed) and bringing the social element into the sociotechnical systems in which we all now work. Susanne Kaiser is a software consultant working with teams on microservice adoption. Recently, she's brought together [Domain-Driven Design, Wardley Mapping, and Team Topologies](https://www.infoq.com/podcasts/ddd-wardley-mapping-team-topologies-2/?utm_source=infoqEmail&utm_medium=editorial&utm_campaign=ArchitectNL&utm_content=11252022) into a conversation about helping teams adopt a fast flow of change. In this InfoQ podcast, Wes Reisz speaks with Susanne about why she feels these three approaches to dealing with software complexity are so complementary. The two then work through some of the patterns she’s seen in her consulting work and discuss how to get started, the most effective sequencing of the patterns, and the effect of overall team size in applying these patterns. [Jesse McGinnis](https://twitter.com/elsom25) spoke at [QCon San Francisco](https://qconsf.com/) on [building high-trust and high-performing teams at Shopify](https://www.infoq.com/news/2022/10/high-trust-performing-teams/?utm_source=infoqEmail&utm_medium=editorial&utm_campaign=ArchitectNL&utm_content=11252022) in a remote world. His talk covered three main concepts. First, focus on trust. Second, first impressions matter. And third, have effective digital conversations. Having capable humans with the proper focus helps them to achieve high confidence. According to McGinnis, and based on the two-and-a-half years of transformation to fully remote at Shopify, it evolves around one core idea: "Intentionality".  [Lena Reinhard](https://www.linkedin.com/in/lenareinhard/) spoke at [QCon San Francisco](https://qconsf.com/) on [Successful Leadership in Hybrid Environments](https://www.infoq.com/news/2022/10/hybrid-leadership-success/?utm_source=infoqEmail&utm_medium=editorial&utm_campaign=ArchitectNL&utm_content=11252022). She explored why hybrid working is attractive for companies and employees, the risks and challenges associated with hybrid working, and why leadership in hybrid environments is fundamentally an issue of equity and inclusion. She discussed a set of guiding principles for hybrid leadership and ways to unleash your team’s potential and ended with advice on changing your organization for the better. Scaling challenges look different for every company, and facing them means that you've found a market fit with a product that's ready to take the next step into a much larger pool of potential customers. But, while the importance of planning for growth and focusing on your customers is apparent for any organization, the methodology behind how and when to scale your engineering org is less clear. Shailesh Kumar, Sr. Vice President of Engineering at ClickUp, argues that there are [four key focus areas when pragmatically scaling an organization](https://www.infoq.com/articles/pragmatically-scale-engineering-organization/?utm_source=infoqEmail&utm_medium=editorial&utm_campaign=ArchitectNL&utm_content=11252022) through hyper-growth: people, process, product, and platform.

|  |  |  |
| --- | --- | --- |
| 

|  |
| --- |
| [Systems That Scale](https://www.infoq.com/vendorcontent/show.action?vcr=a7be77d5-8d3a-4f91-b5ac-d7cb08cff46c&medium=ArchNL&customerParameters=utm_source%3Dinfoq%26utm_medium%3Dsponsor%26utm_campaign%3Dtofu-pipe-oreilly-foundations-of-scalable-systems%26utm_content%3Dguide-static-oreilly-foundations-of-scalable-systems-free-book-newsletter-1125%26utm_term%3Dprosp-infoq-rsc) |
| Scale has become mandatory for apps and services with users spread out all over the globe. But that doesn't mean everyone is ready for it! *Download these free chapters from O'Reilly's [Foundations of Scalable Systems](https://www.infoq.com/vendorcontent/show.action?vcr=a7be77d5-8d3a-4f91-b5ac-d7cb08cff46c&medium=ArchNL&customerParameters=utm_source%3Dinfoq%26utm_medium%3Dsponsor%26utm_campaign%3Dtofu-pipe-oreilly-foundations-of-scalable-systems%26utm_content%3Dguide-static-oreilly-foundations-of-scalable-systems-free-book-newsletter-1125%26utm_term%3Dprosp-infoq-rsc) to learn the essential principles for designing scalable systems. Courtesy of CockroachDB.* |

 |

  We have a small favour to ask. The InfoQ team would like to better understand which technologies and software products are currently on your radar. Your responses will help us create more topically relevant and useful content for the InfoQ community. Complete the survey for **a chance to win 1 of 5 complimentary all-access tickets to QCon Plus (Nov 29 - Dec 9) worth $599.** [**Take the 3 minute survey**](https://www.surveymonkey.com/r/6TN29Q5).  [Charity Majors](https://qconsf.com/speakers/charitymajors), founder and CTO of Honeycomb.io, talked at QCon San Francisco about the [pendulum of being a senior engineer and manager](https://www.infoq.com/news/2022/11/engineer-manager-pendulum/?utm_source=infoqEmail&utm_medium=editorial&utm_campaign=ArchitectNL&utm_content=11252022). She discussed the need for managers in technical teams to have engineering credibility and also the value of deliberately embracing both senior technologist and manager roles in your career, but not both at the same time. Majors explained that management is often seen as an alternative to progressing as an engineer and that technologists have to choose to move away from their technical focus if they want to advance in their careers. She pointed to some assumptions often held about management roles: * It is a one-way trip.
* It's more prestigious than engineering.
* It's the only way to have influence.
* All managers want to be directors or VPs.

She went on to debunk all of these assumptions and explain why the manager and the engineer roles are not incompatible. She advised senior leaders looking to establish a culture where moving between management and technology is accepted and seen as healthy: * Don't build a system where people have to be a manager if they want to be in the loop or have a seat at the table.
* Drain authoritarianism out of your hierarchy. Command-and-control management is toxic to any kind of creative flourishing.
* Management is overhead, management is a support function. Visualize your hierarchy upside down; support system, not dominance.
* If you're unhappy as a manager, don't do it. Your sacrifice will only hurt yourself and those around you.
* Build a long, healthy, flourishing career by leaning into curiosity, love of learning, and surrounding yourself with amazing people.

*This content is an excerpt from a recent InfoQ article by Shane Hasti,"[The Engineer/Manager Pendulum: Charity Majors at QCon SF](https://www.infoq.com/news/2022/11/engineer-manager-pendulum/?utm_source=infoqEmail&utm_medium=editorial&utm_campaign=ArchitectNL&utm_content=11252022)".* To get notifications when InfoQ publishes content on these topics, follow "[architecture and design](https://www.infoq.com/architecture-design/?utm_source=infoqEmail&utm_medium=editorial&utm_campaign=ArchitectNL&utm_content=11252022)", "[leadership](https://www.infoq.com/leadership/?utm_source=infoqEmail&utm_medium=editorial&utm_campaign=ArchitectNL&utm_content=11252022)", and "[team collaboration](https://www.infoq.com/team-collaboration/?utm_source=infoqEmail&utm_medium=editorial&utm_campaign=ArchitectNL&utm_content=11252022)" on InfoQ.

|  |  |  |
| --- | --- | --- |
| 

|  |
| --- |
| [SQL to NoSQL Architectural Differences](https://www.infoq.com/vendorcontent/show.action?vcr=313aa373-4c75-4cdb-ad09-0b55d5789258&utm_source=email&utm_medium=VendorContent&utm_campaign=ArchitectNL&utm_content=11252022) |
| When and how to migrate data from SQL to NoSQL are matters of much debate. It can certainly be a daunting task, but when your SQL systems hit architectural limits or your cloud provider expenses skyrocket, it’s probably time to consider a move. Read this white paper to learn about the architectural differences Between SQL and NoSQL, the tradeoffs between flexibility, scale and cost, and considerations for successful SQL to NoSQL migrations. *Learn more about this topic in the eBook "[SQL to NoSQL: Architecture Differences and Considerations for Migration](https://www.infoq.com/vendorcontent/show.action?vcr=313aa373-4c75-4cdb-ad09-0b55d5789258&utm_source=email&utm_medium=VendorContent&utm_campaign=ArchitectNL&utm_content=11252022)", sponsored by ScyllaDB.* |

 |

Upcoming events   **[QCon Plus online - Nov 30-Dec 8, 2022](https://plus.qconferences.com/?utm_source=infoq&utm_medium=newsletter&utm_campaign=architectsnewsletter_nov25_qplusnov22)** Last chance to join 90+ technical talks from leading early adopter companies including; Microsoft, Doordash, Netflix, Adidas, Stripe, Shopify, Lyft, Google, Linkedin, Amazon, Slack, Vanguard Group and more. [Register now](https://plus.qconferences.com/registration/event/1?utm_source=infoq&utm_medium=newsletter&utm_campaign=architectsnewsletter_nov25_qplusnov22)!   **[QCon London - March 27-29, 2023](https://qconlondon.com/?utm_source=infoq&utm_medium=newsletter&utm_campaign=architectsnewsletter_nov25_qconlondon23)** At QCon London maximize insights from the world’s most innovative senior practitioners and get answers to your software challenges from real-world technical talks. Bring new ideas back to your team to shape your software decisions, workflows, and roadmap. [Book your seat and save with early bird tickets](https://qconlondon.com/registration/event/1?utm_source=infoq&utm_medium=newsletter&utm_campaign=architectsnewsletter_nov25_qconlondon23)!  Senior software developers rely on the InfoQ community to keep ahead of the adoption curve. One of the main reasons software architects and engineers tell us they keep coming back to InfoQ is because they trust the information provided and selected by their peers. We’ve been helping software development teams adopt new technologies and practices for over 15 years through InfoQ articles, news items, podcasts, tech talks, trends reports, and QCon software development conferences. We hope you find this newsletter useful. If not, you can unsubscribe using the link below. Forwarded email? Subscribe and get your own copy. |

 |

|  |
| --- |
|  You have received this email because you subscribed to "The Architects' Newsletter". To stop receiving the Architects' Newsletter, please click the following link: [Unsubscribe](javascript:void(0)) - - -  C4Media Inc. (InfoQ.com), 705-2267 Lake Shore Blvd. West,  Toronto, Ontario, Canada, M8V 3X2 |

 |
