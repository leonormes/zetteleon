---
aliases: []
confidence: 
created: 2025-10-22T08:34:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:14Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Re-Container-update Cleaned Email Thread
type:
uid: 
updated: 
version:
---

The conversation revolves around getting an updated container from The Hyve that can upload QA reports to an S3 bucket. This is a critical prerequisite for the HIE SDE Data Go Live project.

1. Initial Request: Your team (Weronika) requested an ETA for this container update from The Hyve, highlighting its importance.
2. The Hyve's Assumptions: The Hyve (Julia) initially assumed they would be provided with S3 access keys and that there would be one S3 bucket per site.
3. Change in Requirements: Your team (Ollie) later clarified that the client (Keiran) will not provide access keys. Instead, authentication must be done by assuming an IAM role.
4. The Hyve's Response: The Hyve (Jan) has acknowledged this change and agreed to investigate implementing the "Assume Role" functionality.

In short, the core of the discussion is a change in the authentication method for S3 access, from static credentials to a more secure IAM role-based approach.

Outstanding Actions

Based on the emails, here are the clear, actionable items that are still pending:

1. Get an ETA from The Hyve: This is the most critical outstanding action. Jan from The Hyve has only said he "will look into" the IAM role implementation. There is no confirmed delivery date for the updated container.
2. Clarify S3 Bucket Strategy with Keiran: The Hyve is working under the assumption of "one bucket per site". You need to confirm with Keiran if this is correct, or if a single bucket with different paths should be used, as Jan suggested.
3. Provide Necessary Information to The Hyve: Once the bucket strategy is clear, you need to provide The Hyve with the following details so they can complete their work:
    - The exact S3 bucket name(s).
    - The AWS region.
    - The site(s) that will be used for the initial test/demo.
4. Confirm Environment Variable for IAM Role: You need to confirm with The Hyve the exact environment variable they will use for the IAM role ARN (e.g., QCRAWSIAMROLE as Ollie suggested).

**Re-Container-update Cleaned Email Thread (Markdown)**

---

**From Oliver Rushton (FITFILE), 22 October 2025, 09:25**
To: Jan Blom
Cc: Julia Kurps, Weronika Jastrzebska, Susannah Thomas, Gareth Hailes, Leon Ormes, Robin Mofakham, Stefan Payralbe

> Hi Jan,
>
> Apologies for the delay. Keiran has just got back to us about the credentials for the S3 buckets. He does not want to provide ACCESSKEYID and SECRETACCESSKEY, but instead he wants to use an Assume Role. Is this alright for you to implement?
> I believe this will just mean instead of QCRACCESKEYID and QCRSECRETACCESSKEY, we will just set the QCRAWSIAMROLE environment variable, or something similar?
>
> Kind regards,
> Ollie

---

**From Jan Blom (The Hyve), 14 October 2025, 16:29**
To: Oliver Rushton
Cc: Julia Kurps, Weronika Jastrzebska, Susannah Thomas, Gareth Hailes, Leon Ormes, Robin Mofakham, Stefan Payralbe

> Hi Ollie, others,
>
> Gareth and I had discussed this previously. Yesterday, Stefan and I discussed how we would like to implement it. We will use a separate, simple script that runs after the QC reports have successfully completed.
> The script will upload the reports to the S3 bucket.
>
> To be able to do that, we will need the following pieces of information from your side:
>
> - The S3 bucket name
> - The S3 credentials
> - Maybe a region? (We could not yet make out if that is mandatory or useful)
> 
> We suggest the following variable names:
>
> - QCRBUCKET
> - QCRACCESKEYID
> - QCRSECRETACCESSKEY
> 
> If the reports for different sites go into the same bucket, we might also need a path.
>
> We already established a naming convention for the reports as a zip file with Keiran earlier. I will make sure that will be part of the specs we will make available for review.
>
> It would be handy for me to know for which site/sites we want to test/demo this.
>
> If there’s anything you’d like to discuss online, tomorrow would be good (except for 10:30-11:00 CEST), so feel free to plan a meeting.
>
> Kind regards,
> Jan

---

**From Oliver Rushton (FITFILE), 14 October 2025, 16:12**
To: Julia Kurps
Cc: Project team

> Hi Julia,
>
> Keiran has asked us to demonstrate The Hyve QA reports being uploaded to their S3, so we will test this first. This may require some pairing from both sides in case of needing to debug. Once this has been confirmed, we should be on track to meet the deadline.
>
> With regards to S3 configuration, I will ask Keiran what has been set up in our meeting tomorrow and get back to you. But yes, we should be supplying the credentials to your container – I’m not sure what has been agreed for this (environment variables or file mounts?).
>
> Kind regards,
> Ollie

---

**From Julia Kurps (The Hyve), 13 October 2025, 11:48**
To: Weronika Jastrzebska
Cc: Project team

> Hi Weronika,
>
> We will share an updated container mid next week. Does this still work with the expected timelines?
>
> **Assumptions:**
>
> - There will be one S3 bucket per site
> - The S3 credentials will be shared with us
> 
> We might come back with additional questions later this week.
>
> Best wishes,
> Julia Kurps

---

**From Weronika Jastrzebska (FITFILE), 13 October 2025, 11:21**
To: Julia Kurps
Cc: Project team

> Hi Julia,
>
> I just wanted to follow up on the update to your container. We received a confirmation from SDE that this is required to move to the live data stage 1.
>
> 1. Need to see the HyVE QC reports flowing into the nominated bucket
> 
> It would be great if you could confirm the ETA for those updates on your end.
>
> Many thanks,
> Weronika

---

**[End of cleaned message content. Footers and disclaimers removed.]**

[^1]:

    Re-Container-update.pdf

    Hi Ollie,

I will look into implementing the Assume Role. I will let you know if I run into any issues.

Kind regards, Jan

Of course. Here is a draft email you can send to your colleague to ensure you are both aligned on the implementation.

---

Hi Ollie,

an update on progress:

- I have finished debugging our implementation in a docker container using localstack (AWS services in a local container)
- In this setup, I noticed that I am required to provide a region name - I am unsure if this is a localstack requirement, or if it also will be a requirement when interaction with an AWS S3 bucket - I have therefore added an optional env.var. QCR_REGION_NAME
- I am currently building a fresh image which I will test once more
- I still need to add some airflow config - should be simple (or I jinxed it by typing this)
- I hope to upload the image today, but I am currently in the train heading home, hoping to stay ahead of the coming storm, so fingers crossed

I will let you know when the image is available for download.

Kind regards,

Jan Blom
