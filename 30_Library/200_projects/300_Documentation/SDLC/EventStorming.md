---
aliases: []
confidence: 
created: 2025-02-20T02:46:46Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:43Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ddd, SDLC]
title: EventStorming
type: 
uid: 
updated: 
version: 
---

![EventStorming in Detail](EventStorming%20in%20Detail.md)

User Story Mapping in Detail

User story mapping is a technique for visualising a product backlog in a way that shows both the big picture and the individual details. It helps teams to organise and prioritise user stories, ensuring that they are aligned with the overall user experience.

1. Building Shared Understanding: User story mapping helps teams build shared understanding by visually laying out the user's journey and the tasks a user does. This helps everyone to see how the different pieces of the product fit together and how they contribute to the overall user experience.
2. Spotting Holes: By mapping out the user's journey, it becomes easier to identify gaps in the product backlog. The team can then add new user stories to address these gaps, ensuring that the product is complete and meets the needs of its users.
3. Prioritisation: User story mapping provides a framework for prioritising user stories based on their importance to the user experience. This helps the team to focus on building the most valuable features first.
4. Visualising the User Interface: Visualising the user interface and the whole experience helps to build shared understanding of the solution.
5. Challenges to user story mapping:
	- Because stories let you focus on building small things, it’s easy to lose sight of the big picture.
	- Because stories are about conversations, people use that idea to avoid writing anything down.
	- Because good stories are supposed to be written from a user’s perspective, and there are lots of parts that users never see, team members argue that "our product doesn’t have users, so user stories won’t work here".

Combining EventStorming and User Story Mapping

While both EventStorming and user story mapping can be used independently, they are even more effective when combined. EventStorming can be used to model the overall business process, while user story mapping can be used to zoom in on specific parts of the process and define the user stories needed to support them. This combined approach ensures that the product backlog is aligned with the business goals and that the user stories are well-defined and prioritised.

- Both techniques may be used to map in narrative flow across many users and systems.
- Both techniques can be used to build shared understanding.

Reasoning

The reason these techniques are so effective is that they address the root causes of misunderstandings and misinterpretations. By bringing together diverse perspectives, visualising the process, and encouraging open communication, they help to surface hidden assumptions and ensure that everyone is on the same page.

Moreover, these techniques promote a collaborative and iterative approach to software development. Instead of relying on a single person to define the requirements upfront, the team works together to discover and refine them over time. This leads to a more flexible and adaptive process, which is better able to respond to changing customer needs.

To run an effective EventStorming session remotely for a small team, it's important to adapt the in-person collaborative approach to a virtual environment. The key is to maintain engagement, facilitate clear communication, and ensure everyone can contribute effectively. Here’s a detailed guide, incorporating best practices and addressing potential challenges:

1. Preparation and Setup

- Choose the Right Tooling:
    - Virtual Whiteboard: Select a virtual whiteboard tool like Miro or Mural. These platforms allow real-time collaboration with features such as sticky notes, drawing tools, and templates. Ensure everyone on the team is comfortable with the basics of the chosen tool, such as navigation, adding and moving stickies, and using the drawing functions.
    - Video Conferencing: Use a video conferencing tool that supports breakout sessions, such as Zoom, Google Meet, or Microsoft Teams. Breakout rooms enable smaller groups to have focused discussions, mirroring the dynamics of in-person workshops.
- Prepare the Virtual Board:
    - Set up the Board: Before the session, prepare the virtual whiteboard with all necessary instructions and a basic timeline structure. Lock all background elements to prevent accidental movement or changes.
    - Create a Legend: Develop a visual legend for the sticky note grammar, including colours for events, actors, systems, and other elements. Ensure this legend is clearly visible on the board. For example, orange stickies for events, yellow for systems, and so on.
    - Provide a Tutorial: Offer a quick tutorial on how to use the virtual whiteboard tool, either ahead of time or at the start of the session. Show participants how to hide collaborators’ cursors to reduce visual clutter.
- Communicate Expectations:
    - Send a Meeting Invite: Clearly state the business goals of the workshop in the meeting invite. Emphasise that the session will be hands-on, engaging, and participatory.
    - Set the Stage: At the beginning of the session, review the agenda and expected outcomes. Provide a high-level overview of the steps involved, such as identifying events, emergent structure, actors, systems, value, and opportunities.
- Gather Materials:
    - Virtual Stickies: Ensure everyone has access to virtual sticky notes in various colours.
    - Templates: Prepare templates for personas, if needed, to help participants focus on specific user roles during the session.

1. Facilitating the Session

- Icebreaker Activity: Start with a quick icebreaker activity to introduce the basics of EventStorming in a fun and engaging way. For example, model a well-known story like Cinderella or Lion King. Ask everyone to write down events from the story on sticky notes individually.
- Brainstorming Events:
    - Individual Brainstorming: Begin by having each participant brainstorm events individually for a few minutes. This divergent stage is about generating as many ideas as possible without critique.
    - Sequencing Events: After the brainstorming, have the team sequence the events into a timeline from left to right. This can be done collaboratively, with participants moving stickies around to refine the sequence.
- Enriching the Timeline:
    - Add Key Information: Layer more information onto the timeline, such as questions, pain points, risks, actors, systems, and business rules. Use different coloured stickies to represent different types of information.
    - Identify Actors and Systems: Determine the key actors involved in the process and the systems they interact with. Use a specific colour (e.g. yellow) for actors and another (e.g. gold) for systems.
    - Walk the Narrative: Regularly walk the narrative to ensure everyone understands the flow and can identify any gaps or inconsistencies.
- Managing the Flow
    - Timeboxing: Strictly timebox each activity to maintain focus and prevent discussions from dragging on. Use the timer function in your virtual whiteboard tool to keep track of time.
    - Encourage Participation: Ensure that everyone participates by actively soliciting input and asking open-ended questions. Create a safe environment where participants feel comfortable sharing their ideas.
    - Use Breakout Rooms: For detailed process modelling or to address conflicts, divide the participants into smaller breakout groups. This allows for deeper conversations and more focused exploration.
    - Regular Breaks: Schedule regular breaks (e.g. every 30 minutes) to help participants stay relaxed and engaged. Encourage stretching or short physical activities during breaks.
- Visual Unification Tools:
    - Visualisation: EventStorming provides a practical way for teams to understand the presence and negative impact of queues on your work, so they can start to manage them more effectively.
- Asyncronous Updates:
    - Flexibility: Embrace asynchronous updates when appropriate, allowing people to update the board with events outside of the scheduled sessions, so long as they walk through their changes with everyone in the next session.
- Scaling Techniques:
    - Breakout Groups: Create working groups to work in parallel on either the same problem, or different important parts of the domain/subdomains.
    - Timebox: Assign breakout groups a timebox (perhaps only 20 minutes) to Event Storm, then do a quick (maybe 3-5 minutes) walkthrough of each model together.

1. Post-Session Activities

- Document the Outcome:
    - Take Photos: Capture the final timeline by taking photos or screenshots of the virtual board.
    - Record a Walkthrough: Video record a walkthrough of the timeline for future reference. This helps to preserve the context and insights gained during the session.
- Identify Next Steps:
    - Follow-Up Items: Identify items for further follow-up and investigation based on any questions or hot spots that were identified.
    - Action Items: Create a list of action items and assign owners for each. This ensures that the insights from the session are translated into concrete actions.
- Retrospective:
    - Conduct a Retrospective: At the end of the session, conduct a quick retrospective to gather feedback on what worked well and what could be improved. Ask participants what they liked, what was missing, what they learned, and what they still longed for.

1. Addressing Remote-Specific Challenges

- Technical Difficulties:
    - Co-Facilitator: Have a co-facilitator who can focus on the technology and provide support to participants experiencing technical difficulties.
    - Backup Plans: Have backup plans in case of technical issues, such as alternative communication channels or pre-recorded tutorials.
- Maintaining Engagement:
    - Keep it Interactive: Use interactive elements such as voting, emojis, and images to spice up the workshop.
    - Breaks and Energisers: Incorporate short energiser activities or games to keep participants engaged and prevent Zoom fatigue.
- Communication Barriers:
    - Clear Instructions: Provide clear and concise instructions for each activity.
    - Encourage Active Listening: Encourage participants to actively listen to one another and ask clarifying questions.
    - Address Technical Jargon: Be mindful of using technical jargon and ensure that everyone understands the terms being used. Ask "what happened here?" rather than describing how it happened in terms of purely technical implementation details.

By following these steps, you can create a remote EventStorming session that is engaging, productive, and effective in building shared understanding within your team. These sessions can help you to improve your business processes, enable software teams to be more productive, and ensure that everyone is aligned on the goals and priorities of your projects.

To run an effective EventStorming session remotely for a small team, it's important to adapt the in-person collaborative approach to a virtual environment. The key is to maintain engagement, facilitate clear communication, and ensure everyone can contribute effectively. Here’s a detailed guide, incorporating best practices and addressing potential challenges:

1. Preparation and Setup

- Choose the Right Tooling:
    - Virtual Whiteboard: Select a virtual whiteboard tool like Miro or Mural. These platforms allow real-time collaboration with features such as sticky notes, drawing tools, and templates. Ensure everyone on the team is comfortable with the basics of the chosen tool, such as navigation, adding and moving stickies, and using the drawing functions.
    - Video Conferencing: Use a video conferencing tool that supports breakout sessions, such as Zoom, Google Meet, or Microsoft Teams. Breakout rooms enable smaller groups to have focused discussions, mirroring the dynamics of in-person workshops.
- Prepare the Virtual Board:
    - Set up the Board: Before the session, prepare the virtual whiteboard with all necessary instructions and a basic timeline structure. Lock all background elements to prevent accidental movement or changes.
    - Create a Legend: Develop a visual legend for the sticky note grammar, including colours for events, actors, systems, and other elements. Ensure this legend is clearly visible on the board. For example, orange stickies for events, yellow for systems, and so on.
    - Provide a Tutorial: Offer a quick tutorial on how to use the virtual whiteboard tool, either ahead of time or at the start of the session. Show participants how to hide collaborators’ cursors to reduce visual clutter.
- Communicate Expectations:
    - Send a Meeting Invite: Clearly state the business goals of the workshop in the meeting invite. Emphasise that the session will be hands-on, engaging, and participatory.
    - Set the Stage: At the beginning of the session, review the agenda and expected outcomes. Provide a high-level overview of the steps involved, such as identifying events, emergent structure, actors, systems, value, and opportunities.
- Gather Materials:
    - Virtual Stickies: Ensure everyone has access to virtual sticky notes in various colours.
    - Templates: Prepare templates for personas, if needed, to help participants focus on specific user roles during the session.

1. Facilitating the Session

- Icebreaker Activity: Start with a quick icebreaker activity to introduce the basics of EventStorming in a fun and engaging way. For example, model a well-known story like Cinderella or Lion King. Ask everyone to write down events from the story on sticky notes individually.
- Brainstorming Events:
    - Individual Brainstorming: Begin by having each participant brainstorm events individually for a few minutes. This divergent stage is about generating as many ideas as possible without critique.
    - Sequencing Events: After the brainstorming, have the team sequence the events into a timeline from left to right. This can be done collaboratively, with participants moving stickies around to refine the sequence.
- Enriching the Timeline:
    - Add Key Information: Layer more information onto the timeline, such as questions, pain points, risks, actors, systems, and business rules. Use different coloured stickies to represent different types of information.
    - Identify Actors and Systems: Determine the key actors involved in the process and the systems they interact with. Use a specific colour (e.g. yellow) for actors and another (e.g. gold) for systems.
    - Walk the Narrative: Regularly walk the narrative to ensure everyone understands the flow and can identify any gaps or inconsistencies.
- Managing the Flow
    - Timeboxing: Strictly timebox each activity to maintain focus and prevent discussions from dragging on. Use the timer function in your virtual whiteboard tool to keep track of time.
    - Encourage Participation: Ensure that everyone participates by actively soliciting input and asking open-ended questions. Create a safe environment where participants feel comfortable sharing their ideas.
    - Use Breakout Rooms: For detailed process modelling or to address conflicts, divide the participants into smaller breakout groups. This allows for deeper conversations and more focused exploration.
    - Regular Breaks: Schedule regular breaks (e.g. every 30 minutes) to help participants stay relaxed and engaged. Encourage stretching or short physical activities during breaks.
- Visual Unification Tools:
    - Visualisation: EventStorming provides a practical way for teams to understand the presence and negative impact of queues on your work, so they can start to manage them more effectively.
- Asyncronous Updates:
    - Flexibility: Embrace asynchronous updates when appropriate, allowing people to update the board with events outside of the scheduled sessions, so long as they walk through their changes with everyone in the next session.
- Scaling Techniques:
    - Breakout Groups: Create working groups to work in parallel on either the same problem, or different important parts of the domain/subdomains.
    - Timebox: Assign breakout groups a timebox (perhaps only 20 minutes) to Event Storm, then do a quick (maybe 3-5 minutes) walkthrough of each model together.

1. Post-Session Activities

- Document the Outcome:
    - Take Photos: Capture the final timeline by taking photos or screenshots of the virtual board.
    - Record a Walkthrough: Video record a walkthrough of the timeline for future reference. This helps to preserve the context and insights gained during the session.
- Identify Next Steps:
    - Follow-Up Items: Identify items for further follow-up and investigation based on any questions or hot spots that were identified.
    - Action Items: Create a list of action items and assign owners for each. This ensures that the insights from the session are translated into concrete actions.
- Retrospective:
    - Conduct a Retrospective: At the end of the session, conduct a quick retrospective to gather feedback on what worked well and what could be improved. Ask participants what they liked, what was missing, what they learned, and what they still longed for.

1. Addressing Remote-Specific Challenges

- Technical Difficulties:
    - Co-Facilitator: Have a co-facilitator who can focus on the technology and provide support to participants experiencing technical difficulties.
    - Backup Plans: Have backup plans in case of technical issues, such as alternative communication channels or pre-recorded tutorials.
- Maintaining Engagement:
    - Keep it Interactive: Use interactive elements such as voting, emojis, and images to spice up the workshop.
    - Breaks and Energisers: Incorporate short energiser activities or games to keep participants engaged and prevent Zoom fatigue.
- Communication Barriers:
    - Clear Instructions: Provide clear and concise instructions for each activity.
    - Encourage Active Listening: Encourage participants to actively listen to one another and ask clarifying questions.
    - Address Technical Jargon: Be mindful of using technical jargon and ensure that everyone understands the terms being used. Ask "what happened here?" rather than describing how it happened in terms of purely technical implementation details.

By following these steps, you can create a remote EventStorming session that is engaging, productive, and effective in building shared understanding within your team. These sessions can help you to improve your business processes, enable software teams to be more productive, and ensure that everyone is aligned on the goals and priorities of your projects.

Would you like me to elaborate on any of these steps further, or perhaps provide some examples of how to apply these techniques in practice? I can also offer to review the material with you using some quizzes.
