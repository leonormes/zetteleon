---
aliases: []
confidence:
created: 2025-10-06T09:12:43Z
epistemic:
last_reviewed:
modified: 2025-12-04T13:27:53Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [nnuh]
title: NNUH data meeting
type:
uid:
updated:
version:
---

Of course. Based on the meeting transcript and your Jira ticket, your task is to update the NNUH network diagram to reflect a significant potential change in the data architecture, specifically concerning where the source and harmonised data will be stored and how it will be accessed. The current diagram is now likely incorrect based on the discussion.

Here is a breakdown of the work you need to do, framed as a step-by-step plan.

---

## 1. Clarify Key Architectural Decisions

Before you can accurately update the diagram, you need confirmed answers to the pivotal questions raised in the meeting. The current diagram is ambiguous until these points are resolved.

- **Data Storage Method:** NNUH must decide whether they will provide the data as **flat files (CSVs)** or in a **PostgreSQL database**. Mike Shemko is the key contact for this decision. This choice fundamentally changes the components and data flow lines in the diagram.
- **Location of Harmonised (OMOP) Data:** It was discussed that NNUH may require direct access to the final, harmonised OMOP data. If so, the plan is for **NNUH to host this database** themselves and provide Fitfile with access credentials. This is a major architectural shift, moving a core component from the "Fitfile Node" in Azure to the NNUH on-premise environment.
- **Confirm Ben's Specific Feedback:** The meeting notes state that "we're waiting for a little bit of information to come from Ben following the call yesterday" and that this may lead to updates to the diagram. You must get these specific points from Susannah or your internal team to ensure they are incorporated.

---

## 2. Draft the Updated Network Diagram

Once you have the clarifications from Step 1, you can modify the diagram. Your key changes will be:

- **Modify the NNUH On-Premise Section:**
  - Based on the decision, add an icon for either a **File Store** or a **PostgreSQL Database** to represent the source data extract.
  - If NNUH is hosting the harmonised data, add a second **PostgreSQL Database icon** in this section, clearly labelled "Harmonised OMOP Data".
- **Update the Data Flow and Connections:**
  - Redraw the connection from the "FITFILE NODE" to the NNUH environment.
  - If NNUH provides a database, this line will represent a secure database connection (e.g., over a VPN) from the Fitfile components to the NNUH-hosted source *and* harmonised databases.
  - If they provide flat files, the flow might be an SFTP transfer or an API upload into the Fitfile Node. The current diagram's use of a "Reverse Proxy" may still be relevant here.
- **Adjust the "FITFILE NODE" (Azure Cloud) Section:**
  - If the harmonised OMOP database is moved to NNUH's environment, **remove it** from the Azure diagram. The Fitfile Node's role becomes more focused on processing and ETL (The Hyve's components) rather than data storage.
- **Add Annotation for Security and Access Control:**
  - Add a text note specifying that Fitfile will require **separate credentials for synthetic and live data access**. This is a critical detail for the RITS security process.
  - Update any notes regarding firewalls or network rules to reflect the new connection type (e.g., rules for Postgres traffic on port 5432 vs. SFTP on port 22).
- **Review and Reconcile Sticky Notes:**
  - Go through the yellow sticky notes on the current diagram. Many of the questions they pose (e.g., "if true, stands up in on-premise") are precisely what was discussed in the meeting.
  - Remove notes that are now resolved by the new design and update any that are still relevant.

---

## 3. Update Supporting Documentation

The RITS process requires more than just a diagram. You should also:

- **Write a Narrative Description:** Briefly describe the updated data flow. Explain *why* the architecture has changed (i.e., to meet NNUH's requirement for direct data access and to clarify the audit trail process).
- **List Stakeholders:** Ensure the contact list on the diagram (Mike, Jeffrey, Mark, Ben, Nick) is still correct.

---

## 4. Distribute for Review and Sign-Off

Once the draft is complete, circulate the updated diagram and its description to all relevant stakeholders for confirmation before formal submission.

- **Internal:** Susannah Thomas, Oliver Rushton, Weronika Jastrzebska.
- **NNUH:** Mike Shemko, Ben Goss.
- **Partner:** Liam Glueck & Stefan from The Hyve (to ensure the access method works for their ETL process).

---

### Summary To-Do List

1. [ ] **Contact Mike Shemko (NNUH)** to confirm the data storage decision (Flat Files vs. Postgres DB) and the location of the harmonised OMOP database.
2. [ ] **Check with Susannah/Oliver** for the specific feedback points from Ben Goss.
3. [ ] **Modify the diagram** to move the OMOP database to NNUH on-premise (if confirmed).
4. [ ] **Update the diagram** to show the correct source data component (File Store or DB).
5. [ ] **Redraw connection lines** to reflect the new data access method.
6. [ ] **Add a text annotation** regarding separate credentials for live/synthetic data.
7. [ ] **Clean up the old sticky notes.**
8. [ ] **Write a brief narrative** explaining the changes.
9. [ ] **Send the updated package for review** before finalising for the RITS submission.

## NNUH/FITFILE/The Hyve Re: Data Update Meeting - August 19

[**VIEW RECORDING - 33 mins (No highlights)**](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_)

![[EoE - HIE&NNUH Network Diagram.jpg]]

### Meeting Purpose

[Discuss data update and technical requirements for transitioning from synthetic to live data in the NNUH/Fitfile/The Hyve project.](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=4.0 "PLAY @0:04")

### Key Takeaways

- [The live data format will largely resemble the synthetic data, allowing for reuse of existing ETL processes](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=147.0 "PLAY @2:27")
- [NHS numbers are required for national opt-out and data linkage, but will be handled securely within the Fitfile node](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=665.0 "PLAY @11:05")
- [Infrastructure decisions are needed regarding data storage (flat files vs. database) and access methods](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1175.0 "PLAY @19:35")
- [Further discussions needed on national opt-out implementation and audit trail requirements](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1121.0 "PLAY @18:41")

### Topics

#### Data Format and Content

- [ICD-10 codes will continue to be used for diagnoses](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=261.0 "PLAY @4:21")
- [Potential improvements in medication data quality due to new EPMA system](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=492.0 "PLAY @8:12")
- [Full date of birth (not just year) will be provided in the updated data extract](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1127.0 "PLAY @18:47")
- [NHS numbers will be included in the person_source_value field for opt-out and linkage purposes](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=665.0 "PLAY @11:05")

#### Data Storage and Access

- [Options discussed: flat files (CSV) vs. PostgreSQL database](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1194.0 "PLAY @19:54")
- [Flat files are simpler but may complicate audit trail creation](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1197.0 "PLAY @19:57")
- [Database approach offers easier auditing but requires more setup](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1200.0 "PLAY @20:00")
- [Decision needed on whether NNUH requires direct access to harmonized OMOP data](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1509.0 "PLAY @25:09")

#### Data Linkage and Opt-out

- [Fitfile to use NHS numbers for national opt-out via Mesh API](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=774.0 "PLAY @12:54")
- [Linkage methodology produces non-deterministic tokens for cross-site data matching](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=861.0 "PLAY @14:21")
- [Potential use case for linking primary care (TPP) and secondary care data](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=947.0 "PLAY @15:47")
- [Further discussion needed on opt-out implementation specifics for NNUH](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1786.0 "PLAY @29:46")

#### Technical Infrastructure

- [Authentication and credential format for database access to be determined](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1619.0 "PLAY @26:59")
- [Separate credentials required for synthetic and live data access](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1753.0 "PLAY @29:13")
- [Consideration needed for storing synthetic and live data (labeled separately or in distinct areas)](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1691.0 "PLAY @28:11")

### Next Steps

- [Mike to verify any changes in medication data format with the pharmacy team](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=609.0 "PLAY @10:09")
- [Discuss primary care data linkage use case with Danielle and Henri](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1023.0 "PLAY @17:03")
- [NNUH to decide on audit trail requirements and data storage approach (flat files vs. database)](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1716.0 "PLAY @28:36")
- [Mike to consult with security team on database credential provisioning](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1654.0 "PLAY @27:34")
- [Fitfile to update network document and share with stakeholders](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1888.0 "PLAY @31:28")
- [Further discussion needed on national opt-out implementation for NNUH](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1786.0 "PLAY @29:46")
- [Await DPIA feedback and proceed with installation planning](<https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_?tab=summary&timestamp=1943.0> "PLAY @32:23

## NNUH/FITFILE/The Hyve Re: Data Update Meeting - August 19

[**VIEW RECORDING - 33 mins (No highlights)**](https://fathom.video/share/2V2Pp4f7kqHs4FVT_NU8ptELTMw9ZDB_)

[@0:04](https://fathom.video/calls/383536653?timestamp=4.1) - **Susannah Thomas (Fitfile)**

Hi, Liam, hi, Stefan. Hi, everyone. Mike, have you met Liam and Stefan before? I can't remember. think it was a while back.

Definitely met Stefan a while back.

[@0:20](https://fathom.video/calls/383536653?timestamp=20.96) - **Shemko, Mike (NNUHFT) (Nnuh)**

It was back in January, I think. Okay, yeah. It has been a while indeed. It has.

[@0:28](https://fathom.video/calls/383536653?timestamp=28.34) - **Susannah Thomas (Fitfile)**

We also have Mark on the call. Have you met Mark before as well from HAE? So Mark is working on the project management side with Laura, and I'll let Mark explain a bit further what he's doing.

Sure. Excellent. Yeah, nice to meet you all.

[@0:45](https://fathom.video/calls/383536653?timestamp=45.82) - **Mark Dines-Allen | Health Innovation East (Health Innovation East)**

So Mark Aver has brought me in to sort of give more support to how we onboard new sites from that initial engagement right through to delivery.

So I'm to be supporting Laura and the rest of the team. So nice to meet

[@1:03](https://fathom.video/calls/383536653?timestamp=63.252) - **Susannah Thomas (Fitfile)**

And I guess you haven't met anyone from our side either, Mark, so if we, I know we've only got a half an hour, so if just want to do a quick run through, and starting with Oli on our side.

[@1:16](https://fathom.video/calls/383536653?timestamp=76.592) - **Oliver Rushton**

Do you think we could, I know we've got half an hour and I think that the other guys have got lots of questions, so if you wouldn't mind, if we would just crack on.

Can we put just something in the message, in the chat?

[@1:28](https://fathom.video/calls/383536653?timestamp=88.612) - **Susannah Thomas (Fitfile)**

Yeah, that's right, just do it in the chat, that would be great, yeah, okay, no problem, so we, we've gone through, we had, we've had some discussion, and I know that the last time we probably talked about the data side was probably back in January, and so in terms of, we've got some questions, the Hyve, we've got some questions regarding just the data and moving from live, synthetic data to live data, and I know that Oli has some of the technical questions.

So Oli, do you want to start off on the technical questions that we have? technical questions? Yeah. In relation, and I know Veronica has a couple of questions on the opt-out as well.

[@2:05](https://fathom.video/calls/383536653?timestamp=125.684) - **Oliver Rushton**

I would love to, but I really feel like the Hive need to probably ask their questions first, and then we'll go on from there.

[@2:16](https://fathom.video/calls/383536653?timestamp=136.264) - **Liam Glueck (The Hyve)**

Yeah, mean, if that's okay with you guys, I think we can get through ours relatively quick, to give you enough time at least.

[@2:24](https://fathom.video/calls/383536653?timestamp=144.144) - **Oliver Rushton**

So, Mike and Mark.

[@2:25](https://fathom.video/calls/383536653?timestamp=145.764) - **Liam Glueck (The Hyve)**

Hope you're both doing well. So, yeah, I mean, for us, we focused on the transforming of the data, right, into the OMOP standards.

So, we've gotten used to the synthetic data and the format that's in, and the tables. And so, more or less, our questions are, how different will it be?

But if I am, and in doing so, if I need to specify exactly what we're used to with the synthetic data, for example, that the diagnoses come with ICD-10 codes.

Will this be different? Are you using another coding system? Sort of, I have to admit those were probably the main source codings we had.

Otherwise, we also have specific string terms or like how the text occurs when it comes to race mappings or drugs.

Okay.

[@3:22](https://fathom.video/calls/383536653?timestamp=202.456) - **Shemko, Mike (NNUHFT) (Nnuh)**

So, it's a complicated answer, maybe. And I don't know if you've already looked at new releases of ICD, you know, how they get republished from TRUD every so often.

There's country level standards and NHS standards, but I can pull off some reference information from you. And the ICD codes in general internationally gets refreshed and modified all the time, right?

I don't know how that fits in with OMOP, or does it, necessarily? Well, it's more so that it's the source terminology that we saw.

[@4:10](https://fathom.video/calls/383536653?timestamp=250.848) - **Liam Glueck (The Hyve)**

So in the end, we're going to use SNOMED terms, realistically, right? The SNOMED ontology for actually representing the concepts in the OMOP tables.

We just use the ICT-10 vocabulary then to sort of automatically do that, right? Because OMOP and Odyssey have the mapping tables.

So it's not that we need to know what's in there in terms of the actual codes. It's just knowing whether or not ICD-10 will still be used.

Okay. Yes, it will still be used.

[@4:40](https://fathom.video/calls/383536653?timestamp=280.508) - **Shemko, Mike (NNUHFT) (Nnuh)**

There will be differences, though, once we get the EPR live. So what we produce now is going to change in March of next year, anyhow.

Okay. Okay.

[@4:51](https://fathom.video/calls/383536653?timestamp=291.728) - **Susannah Thomas (Fitfile)**

I think for the purpose of – well, I know that there's going to be quite a lot of change because there will be a lot more data available in March next year.

At the moment, in terms of this project, because we have our, the project has been extended to the end of January, so I think for the purpose of moving over, it's just concentrating on the data that you've got available at the moment, Mike, in terms of moving over to live data.

Obviously, depending on how far this project goes and whether there'll be a new contract coming in for next year, which we hope will be the case, then we'll be looking at that change to, you know, the expansion of the data with the extra three hospitals data and all the other data that you're working on in the EPR, but I think for the moment, it's just going to be concentrating on what live data you have available right now.

Okay.

[@5:44](https://fathom.video/calls/383536653?timestamp=344.14) - **Shemko, Mike (NNUHFT) (Nnuh)**

I guess I will reiterate that from our previous discussions as well, what we, what we designed is, you know, Python data pipelines that are sucking the data out of live systems and then, for lack of a better term,

We into staging tables and environments for the SDE to pick up, so it's not like it's live data. I just want to make that distinction, especially with Information Governance colleagues.

Whenever we talk about something being live, to them it means a little bit something different, right? So in a partial answer to, I think the first bit of your question, Liam, is that we can produce that and modify the pipeline.

The data can flow, but we can do a pre-processing step if required to transform it in any way that's better for you to receive, if that makes sense?

Will this still be the same pipeline that was used to make the previous set of synthetic data?

[@6:44](https://fathom.video/calls/383536653?timestamp=404.412) - **Liam Glueck (The Hyve)**

Yes, for now, yeah. Okay, then my assumption is that it shouldn't be so much of an issue, right? If it's still being generated the same way, then we can hopefully just have the same assumptions for what we saw in this synthetic data.

And our ETL is anyways curated to work with that.

[@7:03](https://fathom.video/calls/383536653?timestamp=423.384) - **Shemko, Mike (NNUHFT) (Nnuh)**

And I think we are still talking about the MVP corpus of data for cardiovascular, extending that, and then the NOFORC arthritis registry as well as a secondary data, so which you don't have any data on yet.

But that's the second one that we've vetted as an additional data source at this moment in time.

[@7:30](https://fathom.video/calls/383536653?timestamp=450.224) - **Liam Glueck (The Hyve)**

Yeah, it'll be very similar anyhow, though, generally speaking. okay. So that's good to know. It's just that, so for example, in my mind, it just sounds like if you're going to have two different disease areas of focus, then a lot of the drugs that have been used might differ, right?

So for example, we have a lot of like string text, so text fields for the drugs, and we've mapped those, and in combinations with the form and dose that we saw.

So that brings me up to another question then on the drug format. So it's just making sure that if we get string values again, but there will be some new drugs, in order to map those, we have to know what they are, right?

Yeah, that's a very messy data.

[@8:12](https://fathom.video/calls/383536653?timestamp=492.876) - **Shemko, Mike (NNUHFT) (Nnuh)**

think there, since we last spoke as well, I think they've either about to launch a new EPMA system or have already, in which case the data might be a lot cleaner on the medication side.

But I have, I'll have to verify that statement. Okay, no problem.

[@8:35](https://fathom.video/calls/383536653?timestamp=515.316) - **Liam Glueck (The Hyve)**

So, but at least it's good to know that, in theory, they should come with the same format as what we saw, right?

Also with sort of each relevant table on their own, right? There'd be a diagnoses table, a medications table, a patient data table.

Yeah. Okay, great. Okay. Well, then the assumptions would stay the same, guess, right? Unless Stefan sees any other points that we might be missing.

Bye. But if it's being generated the same way, then we should be able to rely on the ETL to a good extent.

Yeah, I agree.

[@9:09](https://fathom.video/calls/383536653?timestamp=549.208) - **Stefan**

mean, the more it resembles the format of the synthetic data that we've already seen, the better, I would say, because then we can reuse lots of what we already have now designed with regards to the mapping scripts.

Yeah, so for the semantic mappings where we can use the OMO vocabularies, for example mapping the ICD-10 codes, then we can easily reuse that.

It doesn't really require any modifications. But for the drugs where we mapped actual strings, yeah, we do need to get them a unique list of all the values that occur in the data.

Because we cannot have automated mappings for that.

[@10:09](https://fathom.video/calls/383536653?timestamp=609.02) - **Shemko, Mike (NNUHFT) (Nnuh)**

I'll ask the pharmacy team about any changes because I haven't linked in with them for a while and let me get back to you on the medications one to see if things have shifted at all there.

Hopefully in the right direction of making it more cleaner and actual names rather than just strings. Yeah, it's messy.

Great. Okay.

[@10:35](https://fathom.video/calls/383536653?timestamp=635.86) - **Stefan**

But then in that case, also for the sake of time, I think then that should be good for us for now.

[@10:42](https://fathom.video/calls/383536653?timestamp=642.02) - **Liam Glueck (The Hyve)**

Thank you.

[@10:42](https://fathom.video/calls/383536653?timestamp=642.96) - **Oliver Rushton**

Thanks.

[@10:44](https://fathom.video/calls/383536653?timestamp=644.04) - **Weronika Jastrzebska**

From the Fitfile side, sorry Oli, before we're going to move on to our question around the database, I just want to say like when we were running some example queries on the synthetic data, were two matters that we wanted to bring up.

The first one was, I'm not sure if that's already been said. But the NHS numbers, I think that's been done as part of the synthetic data.

We, as Fitfile, we need NHS numbers to run the national opt-out on. So what we've done with synthetic data, they were added to the person source value.

think field, that was the name of the field that they were mapped to. And I think that's still the desire moving forward.

I just wanted to bring it up in the forum in case it is a problem or we've not flagged this properly before.

[@11:30](https://fathom.video/calls/383536653?timestamp=690.352) - **Shemko, Mike (NNUHFT) (Nnuh)**

Sorry, are you saying that from, we didn't put NHS numbers in the synthetic data, even synthetic NHS numbers, right?

Uh, and do you mean for the, the linkage part or opt-out tracing you will need them at some level?

Um, well, all I can, all I can say is that in the EPR program, we've just finished, um, construction in the master patient index section.

you. Across all three hospitals, and I think we're at 86% of the DBS-traced NHS numbers, so the confidence in the data quality of the demographic data, including the NHS number against the spine, is quite high at the moment, and that will obviously feed into the mapping of the opt-outs.

So I don't understand how the whole mechanics of that will work yet on the SDE, but yeah, hopefully that gives you some confidence in that we've got, you know, reliable figures there, and will you have a separate PDS interface, API, on the SDE, is that the idea, or how would you?

[@12:54](https://fathom.video/calls/383536653?timestamp=774.084) - **Weronika Jastrzebska**

Sorry, no, I think in terms of, it won't be surfaced in the SDE at all. So we, as Fitfile, we will use it predominantly to link the data across different sites, but for the opt-out specifically, if we are tasked with basically removing opt-out patients, that is through the Mesh API integration, which requires the NHS numbers for us to filter out.

So that's the prime reason why we need those NHS numbers to be part of the data that will then be harmonized instead of the Fitfile node, instead of the Nnuh.

So it won't be leaving the perimeter, if that makes sense. Yeah, that makes sense.

[@13:40](https://fathom.video/calls/383536653?timestamp=820.476) - **Shemko, Mike (NNUHFT) (Nnuh)**

Mesh is part of, you can do PDS on Mesh as a message. Yeah, that I understand. Okay, thanks. That makes sense.

I think you might want to add more there.

[@13:50](https://fathom.video/calls/383536653?timestamp=830.196) - **Oliver Rushton**

No, was just going to say that the, obviously Fitfile for the linkage methodology would run our kind of algorithm to produce a linkage token.

Based on the NHS numbers, that's what we've been doing across, well, that's the plan to do that across the three sites so that we can all produce, you know, tokens that can be matched.

I see.

[@14:13](https://fathom.video/calls/383536653?timestamp=853.328) - **Shemko, Mike (NNUHFT) (Nnuh)**

So you just created another unique identifier and then a map in behind the scenes which maps it out, right?

Identifies.

[@14:21](https://fathom.video/calls/383536653?timestamp=861.688) - **Oliver Rushton**

The linkage methodology that we use produces a non-deterministic kind of token that can be not matched but verified, kind of like using mathematical proofs, if that makes sense, zero-match proofs.

So it's not like we're keeping a mapping, if that makes sense. It's kind of like verified at, for that particular query, and every time you run the query it produces a different token based on that original NHS number.

Okay.

[@14:51](https://fathom.video/calls/383536653?timestamp=891.628) - **Weronika Jastrzebska**

So the assumption is the SD manager will only run the pseudonymized or anonymized queries, so exactly what Oli said, that...

have or let's Well, hold that a Después We will transform the NHS number before it's being returned to the end-user.

I've got a call.

[@15:09](https://fathom.video/calls/383536653?timestamp=909.38) - **Oliver Rushton**

Yeah, sorry, go ahead.

[@15:11](https://fathom.video/calls/383536653?timestamp=911.24) - **Weronika Jastrzebska**

Just go ahead. ahead. In terms of the opt-out, this is something that we wanted to discuss in scope of you as well, because it's almost like each site has slightly different requirements on the opt-out.

As far as I remember with Nnuh that Fitfile is the only party running the opt-out, so that's why we might have to spend a little bit more time and map something.

How would this run inside of the node? And with the Mesh API, we have some options that we can take you through in a separate call.

Okay, thank you.

[@15:46](https://fathom.video/calls/383536653?timestamp=946.46) - **Shemko, Mike (NNUHFT) (Nnuh)**

Yeah, that sounds good. I was going to ask the question around linkage of, um, have you have you got any use cases or data sets for linking the primary care data with secondary care as of yet?

Using NHS number of the mesh kind of methodology, one of the projects that we want to get off the ground is with a set of GP practices in Norfolk, and we want to link the data between the primary care, the GP practices, and the acute setting.

Of course, I guess, deterministically, if they have data sharing agreements and we can do that behind the scenes, that's great, but I really want to prove the utility maybe of doing it on the SDE.

So we haven't got approval to run that project yet, but in September, Data Access Committee will be putting an application into the SDE to do that.

I just wonder if anyone else has talked through how that might work, linking primary care data with...

[@17:03](https://fathom.video/calls/383536653?timestamp=1023.44) - **Oliver Rushton**

I believe we have come across a use case like this, but I think this is not for the people probably on this call.

think this is like Danielle, think Veronica we could bring in as a separate chat and Henri possibly as well.

Yes, think that they too will serve that.

[@17:19](https://fathom.video/calls/383536653?timestamp=1039.02) - **Weronika Jastrzebska**

We have some projects scoped with the primary care data with Enos specifically. But yeah, I think that there are other people who will be able to tell you a little bit more on that.

The other use case was linking the data across different SDE sites and obviously that's together with the pseudonyms from PET as well.

That's another use case that is being brought to the table as well.

[@17:45](https://fathom.video/calls/383536653?timestamp=1065.4) - **Susannah Thomas (Fitfile)**

Yeah, and this is something that IM1, which is run by NHSE England, their IM1 team is looking at doing this as well.

And we have, as the guys have said, we've worked with Enos. Enos. like focus on that as as we are alter idea In.

We on doing this previously in the past, but to go, let's have a chat when Danielle's back next week maybe, and we can kind of delve into that in a bit more detail.

Yeah, that's great.

[@18:13](https://fathom.video/calls/383536653?timestamp=1093.94) - **Shemko, Mike (NNUHFT) (Nnuh)**

And just so you know, Norfolk is almost entirely TPP. Okay. That's fine, because we're also looking at TPP.

[@18:23](https://fathom.video/calls/383536653?timestamp=1103.66) - **Susannah Thomas (Fitfile)**

Yeah.

[@18:25](https://fathom.video/calls/383536653?timestamp=1105.42) - **Weronika Jastrzebska**

It's almost 98% or something, System 1 up here.

[@18:29](https://fathom.video/calls/383536653?timestamp=1109.42) - **Oliver Rushton**

Yeah.

[@18:30](https://fathom.video/calls/383536653?timestamp=1110.38) - **Shemko, Mike (NNUHFT) (Nnuh)**

Right. That's good to know. We're also looking at the TPP as a, as a, as a second primary provider.

[@18:38](https://fathom.video/calls/383536653?timestamp=1118.12) - **Weronika Jastrzebska**

Exactly. Yeah, it's small. Absolutely. I'm very sorry. Can I just ask the second question? Just going back to the data.

So that was the conversation about the NHS number. And the second thing that came out during the testing was the fact that we've only been given year of birth, as opposed to the date of birth.

And I think as the team raised it with us at the time that this might be a real requirement.

While we're talking to the sites, because obviously that means the user won't be able to filter by age in the national portal while they're running the cohort discovery.

So is that something that maybe we can pick up as well with somebody from the NNUH team? Yeah, sure.

[@19:18](https://fathom.video/calls/383536653?timestamp=1158.71) - **Shemko, Mike (NNUHFT) (Nnuh)**

We can correct that or update the files and resend them. That's fine. Okay.

[@19:26](https://fathom.video/calls/383536653?timestamp=1166.35) - **Weronika Jastrzebska**

Perfect. That was everything I had, Oli. Maybe you have some more questions.

[@19:30](https://fathom.video/calls/383536653?timestamp=1170.41) - **Oliver Rushton**

Yeah, I've got some more infrastructure-specific questions. So I think this has been discussed before, but what's the data source technology that we're expecting to kind of be able to, you know, connect to, to get the extract for the Hive guys to then harmonize?

I mean, it's really open.

[@19:52](https://fathom.video/calls/383536653?timestamp=1192.91) - **Shemko, Mike (NNUHFT) (Nnuh)**

I mean, how do you want to resend? We could store everything as a flat file. We've got a really big kind of data science server.

wait. lots the water. With file stores, that's how we're organizing everything, our site anyhow, or we could put it into Mongo or Postgres or something.

I don't know if that's required.

[@20:16](https://fathom.video/calls/383536653?timestamp=1216.32) - **Oliver Rushton**

I think, like Liam and Stefan, I think you've said before that there's options, essentially, for the Hyve technology to connect to these different data sources.

Yeah, mean, Postgres is what we're most used to, otherwise CSV.

[@20:32](https://fathom.video/calls/383536653?timestamp=1232.0) - **Liam Glueck (The Hyve)**

Yeah, both would be fine for us.

[@20:35](https://fathom.video/calls/383536653?timestamp=1235.06) - **Stefan**

If it also doesn't make any difference for you, then I think the easiest would be to provide them a CSV files on the node, because then we can directly ingest them into our database and then do further processing there.

[@20:52](https://fathom.video/calls/383536653?timestamp=1252.04) - **Shemko, Mike (NNUHFT) (Nnuh)**

Yeah, so basically, it would be really simple, like just storage of flat files on our site in an organized way.

That'll... We'll be able to track longitudinal, you know, changes to data, updates to data, and then additional data sets.

So we can just pull it directly from there. And one of the questions that we had in just going through the DPIA, which we've been able to progress a little bit, is around the audit trail and how we keep track of it all.

So we're putting some thought into, A, how we store it, and then B, how we monitor that and keep a record of whatever goes into the SD or is queried, that sort of thing.

Mm-hmm. Sorry, Liam and Stefan, I just want to check around that as well.

[@21:47](https://fathom.video/calls/383536653?timestamp=1307.11) - **Oliver Rushton**

So with, obviously, the Hype being hosted inside the Fitfile node, how do we envision, like, you know, access to these files?

Is it, you know, is it an SFTP transfer? Is it something...? Like that, do you have support for that, inherently, in the Hyve system?

Is that a question?

[@22:10](https://fathom.video/calls/383536653?timestamp=1330.1) - **Shemko, Mike (NNUHFT) (Nnuh)**

Oh, sorry. That's for the Hyve.

[@22:13](https://fathom.video/calls/383536653?timestamp=1333.92) - **Stefan**

Yeah, I'm afraid that question is best asked to Jan as he picks up that part.

[@22:25](https://fathom.video/calls/383536653?timestamp=1345.42) - **Oliver Rushton**

I know that we've proven that, obviously, we've done this with a Postgres database before. I just don't want to make the assumption that the access to the files is, I suppose, trivial.

Like, I'd rather go to something that we know works. But, Mike, from your side, if it was like a Postgres database, is that difficult for you guys to set up?

It's more work than flat files.

[@22:51](https://fathom.video/calls/383536653?timestamp=1371.06) - **Shemko, Mike (NNUHFT) (Nnuh)**

Definitely. And that's how we're organising it locally. Which would be, if you need it in Postgres... We can do that.

I don't know. Sorry, jumping in.

[@23:09](https://fathom.video/calls/383536653?timestamp=1389.52) - **Helena Ahlfors**

The only benefit of the database approach might be that it is more straightforward to create the audit trail of when things have been pulled from that database or queried access.

So that might be a benefit of that. But I understand otherwise the flat file option is more straightforward and less initial work.

So it sounds like that it might be useful for Mike, for your site to think about what is the audit trail requirement, what you want to essentially implement.

And then for our site, discuss with Hype what is the method that we need to use in the background to be able to access that data and process it and do the magic there.

Yeah. sounds right.

[@23:57](https://fathom.video/calls/383536653?timestamp=1437.18) - **Oliver Rushton**

I think obviously like Fitfile has upload capability of CSP. So that is an option. I'm not sure about the data, the size of the data that we're going to be dealing with, and therefore what constraints our API might have.

But we can look around that, and then that might be the simplest option. Just post them to the API, they'll be available for the Hyve to then consume from a local Postgres in the node.

But yeah, we'll pencil that for now. So is there any requirements on where the Hyve kind of output data is stored?

Are you very happy for it to be within the Fitfile node, within the infrastructure of Fitfile control, essentially? Otherwise, you could provide a database in your own premise.

to me. Yes, Mike. it's you, Mike. I don't think I understood your question. More about like where the output, so the OMOP data, the harmonized kind of data that Hyve will produce, where that is stored and whether there's any requirements around where it is stored.

So can it be in the Fitfile node, which would be the simplest for us, or would you provide a database where the output goes, which is something under your control?

Right.

[@25:21](https://fathom.video/calls/383536653?timestamp=1521.64) - **Shemko, Mike (NNUHFT) (Nnuh)**

I guess the only thing I would say is if we retained access to that, so if we have it on the Fitfile node and retain access to it, that's fine, but we'd probably, if not, then we'd probably want to also store it in our own environment for other uses, and, you know, this is going to be a gradual progression in data sources over time once we get the EPR up and running a new data sources, and just to make sure that we, we can include that in the future exercises easily.

And not start to build silos, right?

[@26:04](https://fathom.video/calls/383536653?timestamp=1564.03) - **Oliver Rushton**

Yeah, I think that the current solution that we have when we are hosting the data, it wouldn't necessarily be accessible to you.

So if it's a requirement that you guys have access, then it may be something that you would have to provision and then give us access to.

And in which case, if we're doing that, then maybe there is some sense in having the source data provided in a similar way if you have to set up a Postgres server.

Yeah. Yeah, okay. Okay, that's good to know. Just conscious of the time.

[@26:45](https://fathom.video/calls/383536653?timestamp=1605.91) - **Susannah Thomas (Fitfile)**

Mike, do you have time to go over a few minutes? A few minutes, yeah.

[@26:50](https://fathom.video/calls/383536653?timestamp=1610.57) - **Shemko, Mike (NNUHFT) (Nnuh)**

Okay.

[@26:52](https://fathom.video/calls/383536653?timestamp=1612.59) - **Susannah Thomas (Fitfile)**

Okay. There's not many, there's not many more questions left.

[@26:59](https://fathom.video/calls/383536653?timestamp=1619.67) - **Oliver Rushton**

So, no, no, We're kind of figuring out the solution as we kind of go along, but is there any, like, format of authentication credentials for this database that we're now going to have that, like, is there any specific format of the credentials that we would expect?

I mean, at the moment, the Fitfile application, normally a user would go into the UI and they would add the database kind of connection string credentials, you know, username, password, host port, database name, and then certificates.

But is there any, you know, requirements that you have around how the credentials are provided to Fitfile?

[@27:34](https://fathom.video/calls/383536653?timestamp=1654.58) - **Shemko, Mike (NNUHFT) (Nnuh)**

Well, I'll have to ask our security network people how to provision that, I guess, and it's good we have the conversation now about what we're going to do our side, and then I'll just ask them how we plan to provision it.

Yes.

[@27:53](https://fathom.video/calls/383536653?timestamp=1673.9) - **Oliver Rushton**

Okay, that's great. But if you could, I don't know, at least let them, you know, when asking them, let them know that.

What the platform currently supports, and then if that's not acceptable, then obviously we can develop a new authentication, you know, connection mechanism.

[@28:11](https://fathom.video/calls/383536653?timestamp=1691.78) - **Weronika Jastrzebska**

Can I also ask, is it decided to have like synthetic and then live data separate, like sitting in a separate potentially databases?

This is something that we worked in the past, and now how we envision it, obviously with the SD manager querying the data, we need to have this, like, we need to distinguish between synthetic and live for them.

[@28:36](https://fathom.video/calls/383536653?timestamp=1716.74) - **Shemko, Mike (NNUHFT) (Nnuh)**

I don't see, I mean, I don't see why we would store them in completely separate areas. We just label them because we start to produce additional synthetic data sets 4ML experiments or something that might be a detractive product in its own right to the SDE customers downstream.

stream. So I would be tempted to keep it all in the same area, but label the data sources basically on our side, that's live data, and this is synthetic data, if that makes sense.

That does make sense.

[@29:13](https://fathom.video/calls/383536653?timestamp=1753.35) - **Oliver Rushton**

I think that the main requirement that Weronika is talking about for Fitfile is to have separate credentials at least.

So it isn't normally other stored, as long as there's two different access points, one that can only access synthetic and one that can only access live.

Okay. Okay, that should be good then. I think that's all I've got, because if you want to pencil the...

I think we need a little bit more time for NDOO. NDOO, yeah.

[@29:41](https://fathom.video/calls/383536653?timestamp=1781.69) - **Weronika Jastrzebska**

Yeah, so we can run through some options and then see what's possible. But just to confirm, Mike, is this still a desire for Fitfile to run opt-out, and you're not going to be running any opt-out on the data that you'll be providing?

I think there's probably...

[@30:00](https://fathom.video/calls/383536653?timestamp=1800.71) - **Shemko, Mike (NNUHFT) (Nnuh)**

Because... We're redesigning everything to do with our PaaS and the interface with the spine right now, anyhow. Let me take that question back and see, you know, if, I don't know what the plans currently are locally, so I'll go back and verify.

Perfect, thank you.

[@30:21](https://fathom.video/calls/383536653?timestamp=1821.4) - **Stefan**

Okay. I think that's it from our end, Susannah.

[@30:24](https://fathom.video/calls/383536653?timestamp=1824.54) - **Weronika Jastrzebska**

Is there anything else that we wanted to go over?

[@30:28](https://fathom.video/calls/383536653?timestamp=1828.38) - **Susannah Thomas (Fitfile)**

Um, no, I think, um, do you know who the other user is going to be at the moment yet, Mike?

And, um, not yet. That's fine, we've still got time.

[@30:42](https://fathom.video/calls/383536653?timestamp=1842.32) - **Shemko, Mike (NNUHFT) (Nnuh)**

Yeah, we're, no, we're hiring some new posts in September, um, so it'll be those people. I don't know who they are yet.

Okay.

[@30:50](https://fathom.video/calls/383536653?timestamp=1850.94) - **Susannah Thomas (Fitfile)**

I think you said last, last week that there's going to be one other user at the moment with you, um, uh, just in terms of the data.

I mean, I guess at the moment we would have you embed. Ben potentially as users on the platform?

[@31:04](https://fathom.video/calls/383536653?timestamp=1864.79) - **Shemko, Mike (NNUHFT) (Nnuh)**

Ben Goss, is. Yes, Ben Goss, yeah.

[@31:07](https://fathom.video/calls/383536653?timestamp=1867.93) - **Susannah Thomas (Fitfile)**

And you mentioned briefly earlier, just on the DPIA, is there anything further that we can help with on that or any other information that you need from us?

[@31:18](https://fathom.video/calls/383536653?timestamp=1878.89) - **Shemko, Mike (NNUHFT) (Nnuh)**

Not as of yet. I've asked the question this morning and I haven't got a response yet, so I will let you know.

[@31:28](https://fathom.video/calls/383536653?timestamp=1888.45) - **Susannah Thomas (Fitfile)**

One of the things as well, when we were talking to Ben yesterday, and obviously just from the update from this call as well, is that we might need to do a few minor changes to the network document as well.

So what I will do is I will ping a message back to Geoffrey and all of the other people on the email list just to advise that because I want to make sure that they have the most up-to-date information on that networking document.

And we're waiting for a little bit of information to come from Ben following the call yesterday. bit. Which may mean that we will make some updates as well to the diagram that we put into that document as well.

Because I just want to make sure that they have signed off on that final version from the RITS perspective as well.

Okay, thanks. There's an email trail with all the stakeholders, so just use that one and thank you.

[@32:18](https://fathom.video/calls/383536653?timestamp=1938.68) - **Shemko, Mike (NNUHFT) (Nnuh)**

Just so that you're aware of that. Okay. All right.

[@32:23](https://fathom.video/calls/383536653?timestamp=1943.22) - **Susannah Thomas (Fitfile)**

So I think at the moment we'll just wait to hear back from you. I'll do the notes from this session and send that out to you later on.

And we'll wait to hear back from you on some of those issues and some of those items just to go back on.

[@32:36](https://fathom.video/calls/383536653?timestamp=1956.32) - **Oliver Rushton**

And then just wait to hear from you as well.

[@32:38](https://fathom.video/calls/383536653?timestamp=1958.66) - **Susannah Thomas (Fitfile)**

And just regarding the DPIA, we'll wait to hear back from Ben as well. And then we can make sure that that networking document's updated and then we'll go from there.

But hopefully getting closer to moving forward into getting started with the installation. Yep. Onwards and upwards.

[@32:58](https://fathom.video/calls/383536653?timestamp=1978.54) - **Shemko, Mike (NNUHFT) (Nnuh)**

Thank you very much. Thank you so much. Thank you so much. And if you've got any questions, Mike, just please let us know.

Thank you. OK, take care. Thanks, everybody.

[@33:06](https://fathom.video/calls/383536653?timestamp=1986.78) - **Oliver Rushton**

Thank you, everyone. Bye-bye. you. Bye.

[@33:09](https://fathom.video/calls/383536653?timestamp=1989.28) - **Mark Dines-Allen | Health Innovation East (Health Innovation East)**

Suzanne, you've got two seconds.
