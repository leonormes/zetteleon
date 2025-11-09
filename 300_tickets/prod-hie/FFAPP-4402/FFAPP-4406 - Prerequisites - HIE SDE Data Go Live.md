---
aliases: []
assignee: Leon Ormes
confidence: 
created: 2025-10-14T13:48:34Z
epic: FFAPP-4402
epic_name: HIE SDE Data Go Live
epistemic: 
issue_id: 22208
issue_key: FFAPP-4406
issue_type: Task
jira_link: https://fitfile.atlassian.net/browse/22208
last_reviewed: 
modified: 2025-11-03T13:48:14Z
priority: High
project: FITFILE Application (FFAPP)
purpose: 
reporter: Robin Mofakham
review_interval: 
see_also: []
source_of_truth: []
status: In Progress
tags: []
title: FFAPP-4406 - Prerequisites - HIE SDE Data Go Live
type:
uid: 
updated: 2025-10-22 08:20:12 UTC
version:
---

## Epic: FFAPP-4402 - HIE SDE Data Go Live

**Status**: ⚪ To Do | **Priority**: ⚠️ Medium | **Assignee**: Robin Mofakham

[View Epic in Jira](https://fitfile.atlassian.net/browse/22200)

### Epic Description

The required tasks for the main HIE SDE node to connect to production services and processing of real patient data.

**Created**: 2025-10-14 13:25:02 UTC | **Updated**: 2025-10-14 16:47:24 UTC

### Child Tasks (9 total)

#### 🔵 In Progress (1)

- **FFAPP-4406**: Prerequisites - HIE SDE Data Go Live (🔺 High) - Leon Ormes *(this ticket - see details below)*

#### ⚫ Ready (2)

- **FFAPP-4407**: Testing Data Export to S3 (⚠️ Medium) - Unassigned
- **FFAPP-4352**: Clean up SDE Node (⚠️ Medium) - Unassigned

#### ⚫ Refinement (5)

- **FFAPP-4403**: Connect RES Production (and disconnect RES Test) (⚠️ Medium) - Unassigned
- **FFAPP-4404**: HDRUK - Upgrade Relay and Bunny (⚠️ Medium) - Unassigned
- **FFAPP-4405**: HDRUK - Production access (⚠️ Medium) - Unassigned
- **FFAPP-4408**: Testing The Hyve -> SDE S3 reports upload (⚠️ Medium) - Unassigned
- **FFAPP-4409**: Check CUH live data connection in SDE Node (⚠️ Medium) - Unassigned

#### ⚫ Parking Lot (1)

- **FFAPP-4410**: Implement CUH data backup (⚠️ Medium) - Unassigned

---

## FFAPP-4406: Prerequisites - HIE SDE Data Go Live

### Status

🔵 **In Progress** | 🔺 **High Priority**

### Description

#### RES Production

- @<Gareth.hailes@fitfile.com> to confirm what is needed to connect their RES production to our VPC.

#### HDRUK Bunny Requirements

- List of users from SDE
- Size of the dataset from SDE for HDRUK
- Test cases from the EoE

#### The Hyve QA Reports

- The Hyve to release the new container - Julia said sometime around the week of the 20th October
- What is the interface (environment or file mount) for supplying the S3 credentials to The Hyve container - @Ollie Rushton has asked julia.
- Can keiran supply us the S3 credentials for us to store in Hashicorp Vault - we will talk to Keiran tomorrow.
- We need to ask keiran whether there will be a bucket per site - as the hyve have assumed.
- Ask keiran whether there is a staging S3 bucket we can use for the Hyve test.
- Confirm with keiran what type of credentials will be provided for access to the S3 bucket for the hyve.

#### Connecting Real Patient Data

- CUH to connect the live data source to the Node and connect it to the SDE Tenant (or project, depending on what has been agreed).

### Action Plan

#### 1. Chase The Hyve for Container Release ETA (High Priority)

- **Action:** Draft and send an email to Jan Blom at The Hyve to get a firm ETA for the container release with IAM role support.
- **To:** Jan Blom (The Hyve)
- **Cc:** Julia Kurps, Weronika Jastrzebska, Susannah Thomas, Gareth Hailes, Leon Ormes, Robin Mofakham, Stefan Payralbe, Ollie Rushton
- **Subject:** URGENT: ETA for container release with IAM role support (FFAPP-4406)
- **Key Points for Email:**
  - Acknowledge his last email about implementing the Assume Role.
  - Emphasize that this is a critical blocker for the HIE SDE Data Go Live project (FFAPP-4402).
  - Request a specific delivery date for the new container.
  - Offer a meeting to resolve any issues.

#### 2. Connect RES Production to VPC

- **Action:** Identify the contact person "Kieran" and their contact details.
- **Action:** Identify the VPC ID for the RES production environment.
- **Action:** Draft an email to Kieran to request the VPC connection.
- **To:** Kieran
- **Cc:** Robin Mofakham, Gareth Hailes
- **Subject:** Request to connect RES production to VPC for HIE SDE project (FFAPP-4406)
- **Key Points for Email:**
  - State the request to connect the RES production environment to your VPC.
  - Provide the VPC ID.
  - Ask for confirmation and if any further information is needed.

#### 3. Gather HDRUK Bunny Requirements

- **Action:** Identify the appropriate contacts at SDE and EoE for the required information.
- **Action:** Draft an email to these contacts.
- **Subject:** Request for HDRUK Bunny requirements for HIE SDE project (FFAPP-4406)
- **Key Points for Email:**
  - Request the following information:
    - List of users from SDE.
    - Size of the dataset from SDE for HDRUK.
    - Test cases from the EoE.
  - Ask them to provide the information or direct you to the right person.

#### 4. Finalize S3 Bucket Strategy with Keiran

- **Action:** Schedule a meeting with Keiran.
- **Attendees:** Keiran, Leon Ormes, Ollie Rushton, Robin Mofakham
- **Agenda:**
  - S3 bucket strategy for The Hyve QA reports.
  - Clarify if there will be a bucket per site.
  - Request a staging S3 bucket for testing.
  - Confirm the type of credentials to be provided for S3 access.

#### 5. Follow up on CUH Live Data Connection

- **Action:** Check with Weronika on the status of her meeting with Jakub from CUH.
- **Action:** Ask Weronika if there are any action items for you resulting from that meeting.

### People

- **Assignee**: Leon Ormes
- **Reporter**: Robin Mofakham

### Linked Issues

#### Blocks

- **FFAPP-4403**: Connect RES Production (and disconnect RES Test)
- **FFAPP-4404**: HDRUK - Upgrade Relay and Bunny

### Comments

#### Gareth Hailes - 2025-10-15 08:52:18 UTC

**_ to confirm what is needed to connect their RES production to our VPC._**
Essentially we have to notify Kieran and he will undertaken the changes in LZA once we provide the VPC ID @Robin Mofakham

---

#### Ollie Rushton - 2025-10-15 09:04:45 UTC

Jan responded with this:

> Hi Ollie, others,
>
> Gareth and I had discussed this previously. Yesterday, Stefan and I discussed how we would like to implement it.
>
> We will use a separate, simple script that runs after the QC reports have successfully completed. The script will upload the reports to the S3 bucket.
>
> To be able to do that we will need the following pieces of information from your side: the S3 bucket name, the S3 credentials (and maybe a region? We could not yet make out if that is mandatory or useful.)
>
> We suggest the following names:
>
> - QCR_BUCKET
> - QCR_ACCES_KEY_ID
> - QCR_SECRET_ACCESS_KEY
> 
> If the reports for different sites go into the same bucket, we might also need a path. We already established a naming convention for the reports as a zip file with Keiran earlier. I will make sure that that will be part of the specs we will make available for review.
>
> It would be handy for me to know for which site/sites we want to test/demo this.
>
> If there's anything you'd like to discuss online, tomorrow would be good, except for 10:30-11:00 (CEST), so feel free to plan a meeting.
>
> Kind regards,
>
> Jan

---

#### Robin Mofakham - 2025-10-21 14:52:39 UTC

S3 information has been requested in the shared teams channel

---

#### Robin Mofakham - 2025-10-22 08:07:04 UTC

@Leon Ormes is this sufficient?

**From Easwaran @ HIE**

We have the S3 bucket created in our Data landing zone account.

Single bucket for all the site per environment:

- **DEV**: `eoe-sde-dev-dqr-905418144317`
- **TEST/STG**: `eoe-sde-tst-dqr-339713007003/eoe-sde-stg-dqr-339713007003`
- **PROD**: `eoe-sde-prd-dqr-381492210920`

For test account, please use the tst bucket.

We have given access to the IAM role: `arn:aws:iam::339713007003:role/dlz-tst-writer-codisc` from codisc account

If the role is assumed we should not need S3 credentials, please let me know if that works

---

```sh
vault kv patch admin/deployments/hie-prod-34/secrets/thehyve \
  qcr_bucket="qa-reports-bucket" \
  qcr_access_key_id="AKIA..." \
  qcr_secret_access_key="secret..." \
  qcr_iam_role=" arn:aws:iam::339713007003:role/dlz-tst-writer-codisc"
```

#### Ollie Rushton - 2025-10-22 08:19:14 UTC

@Robin Mofakham - This is not what the hyve were expecting - they were expecting plain ACCESS_KEY_ID and SECRET_ACCESS_KEY, but it looks like Kieran has provided a IAM role - which implies AWS Assume Role behaviour (this is what he provided us for our bespoke S3 export CLI)

---

#### Ollie Rushton - 2025-10-22 08:20:12 UTC

@Robin Mofakham - So we need to get back to the hyve with this information so they can implement it - it isn't much work

---

### Summary

This ticket tracks prerequisites for the HIE SDE data go live, including:

1. RES production VPC connection setup
2. HDRUK Bunny requirements gathering
3. The Hyve QA reports S3 integration (now using IAM role instead of access keys)
4. Real patient data connection from CUH

**Latest Update**: HIE has provided IAM role-based S3 access instead of access keys. The Hyve team needs to be informed to implement AWS Assume Role behavior.

---

## Related Epic Child Tasks - Details

### FFAPP-4407: Testing Data Export to S3

**Status**: ⚫ Ready | **Priority**: ⚠️ Medium | **Assignee**: Unassigned

[View in Jira](https://fitfile.atlassian.net/browse/22210)

#### Description

Internal then External testing of the process of the CLI tool (S3FITFILE-CLI) that exports to S3.

**Created**: 2025-10-14 14:01:10 UTC | **Updated**: 2025-10-15 14:24:48 UTC | **Reporter**: Robin Mofakham

---

### FFAPP-4352: Clean up SDE Node

**Status**: ⚫ Ready | **Priority**: ⚠️ Medium | **Assignee**: Unassigned

[View in Jira](https://fitfile.atlassian.net/browse/21876)

#### Description

While testing, SDE raised a point they are seeing a lot of legacy data sources configured in the past for Milestone presentation. We should help them and guide them how to delete and clean up their environment once CUH data source will be available.

**Created**: 2025-10-07 13:03:21 UTC | **Updated**: 2025-10-15 14:24:48 UTC | **Reporter**: Weronika Jastrzebska

---

### FFAPP-4403: Connect RES Production (and Disconnect RES Test)

**Status**: ⚫ Refinement | **Priority**: ⚠️ Medium | **Assignee**: Unassigned

[View in Jira](https://fitfile.atlassian.net/browse/22202)

#### Description

Notes - @<Gareth.hailes@fitfile.com> to fill out, but essentially involves VPC peering, accepting the connection of either side

Please provide simple documentation on RES connections.

#### Dependencies

- **Blocked by**: FFAPP-4406 (Prerequisites ticket)

**Created**: 2025-10-14 13:29:45 UTC | **Updated**: 2025-10-15 09:45:56 UTC | **Reporter**: Robin Mofakham

---

### FFAPP-4404: HDRUK - Upgrade Relay and Bunny

**Status**: ⚫ Refinement | **Priority**: ⚠️ Medium | **Assignee**: Unassigned

[View in Jira](https://fitfile.atlassian.net/browse/22204)

#### Description

We have been asked by Charlotte from HDRUKL to upgrade to the latest software versions of the relay and bunny hutch solution.

Also, we need to reconfigure relay to use the production HDRUK BC RQuest API.

#### Dependencies

- **Blocked by**: FFAPP-4406 (Prerequisites ticket)
- **Blocked by**: FFAPP-4405 (HDRUK - Production access)

**Created**: 2025-10-14 13:33:56 UTC | **Updated**: 2025-10-15 09:45:57 UTC | **Reporter**: Robin Mofakham

---

### FFAPP-4405: HDRUK - Production Access

**Status**: ⚫ Refinement | **Priority**: ⚠️ Medium | **Assignee**: Unassigned

[View in Jira](https://fitfile.atlassian.net/browse/22206)

#### Description

We require access to the production HDRUK portal. This involves:

- HDRUK - create collection
- HDRUK - supply collection connection details
- FITFILE - to provide outbound IP to HDRUK of the current HIE cluster.
- HDRUK - to grant FITFILE operators access to the production portal

We're waiting on:

- List of users from SDE
- Size of the dataset
- Test cases from the EoE

#### Dependencies

- **Blocks**: FFAPP-4404 (HDRUK - Upgrade Relay and Bunny)

**Created**: 2025-10-14 13:35:01 UTC | **Updated**: 2025-10-15 09:45:57 UTC | **Reporter**: Robin Mofakham

---

### FFAPP-4408: Testing The Hyve -> SDE S3 Reports Upload

**Status**: ⚫ Refinement | **Priority**: ⚠️ Medium | **Assignee**: Unassigned

[View in Jira](https://fitfile.atlassian.net/browse/22212)

#### Description

The Hyve will release a container during the week of the 20th October, with the changes to upload reports to an S3 bucket.

Keiran has asked us to test this capability to prove that we are ready to connect to the RES production environment.

#### Prerequisites

- What is the interface (environment or file mount) for supplying the S3 credentials to The Hyve container - @Ollie Rushton has asked julia.
- Can keiran supply us the S3 credentials for us to store in Hashicorp Vault - we will talk to Keiran tomorrow.
- We need to ask keiran whether there will be a bucket per site - as the hyve have assumed.
- Ask keiran whether there is a staging S3 bucket we can use for the Hyve test.
- Confirm with keiran what type of credentials will be provided for access to the S3 bucket for the hyve.

#### Test

- Store the S3 credentials in Hashicorp Vault.
- Modify the Hyve helm chart to deploy the vaultstaticsecret and configure the container's env.
- Upgrade The Hyve container in the FF Demo nodes
- Run the ETL pipeline, monitor for any pipeline failures and check whether the files have been stored in S3 (may need keiran to check this)

**Created**: 2025-10-14 14:12:52 UTC | **Updated**: 2025-10-15 09:45:57 UTC | **Reporter**: Ollie Rushton

---

### FFAPP-4409: Check CUH Live Data Connection in SDE Node

**Status**: ⚫ Refinement | **Priority**: ⚠️ Medium | **Assignee**: Unassigned

[View in Jira](https://fitfile.atlassian.net/browse/22214)

#### Description

Once CUH have connected the live data to the CUH Node, we should inform the SDE to perform tests using Query Plans against the live data source

**Created**: 2025-10-14 14:41:47 UTC | **Updated**: 2025-10-15 09:45:58 UTC | **Reporter**: Ollie Rushton

---

### FFAPP-4410: Implement CUH Data Backup

**Status**: ⚫ Parking Lot | **Priority**: ⚠️ Medium | **Assignee**: Unassigned

[View in Jira](https://fitfile.atlassian.net/browse/22216)

#### Description

Currently, for the CUH node, [Description appears incomplete in Jira]

**Created**: 2025-10-14 14:51:03 UTC | **Updated**: 2025-10-15 09:45:58 UTC | **Reporter**: Ollie Rushton

Keiran Raine | Health Innovation East - apologies, but I'm still unsure what you mean by "this" - I assume you are referring to the bucket being different per project as we discussed a long time ago, but I need to know whether the iam-role will be the same for all projects within the same environment? The iam-role will be different per environment, that makes perfect sense, but if the iam-role changes per bucket, then it will affect our implementation. Yes, the IAM user is `arn:aws:iam::135808916559:user/fitfile-s3` which has permission to write to any bucket following the conventions described above.  We will want to designate a different one for `live` data into the production env though, but we really need to see this working on our end as we're not aware of it being tested so far.

Oliver Rushton22/10/2025 18:38Keiran Raine | Health Innovation East - I understand that Robin Mofakham is working with Easwaran Chandrasekaran | Health Innovation East to get The Hyve S3 credentials for the testing bucket for the QA reports. On a separate note, I am working on getting the test ready for the data export from…

For each environment this is different, additionally for each project it is different

- dlz-tst-s3-fitfile-ff2504-339713007003

Structure `dlz-{env}-s3-fitfile-{sde_project}-{account_id}`.  There is only one project configured for testing, unless we include the `dev` one.

Keiran Raine | Health Innovation East - I understand that Robin Mofakham is working with Easwaran Chandrasekaran | Health Innovation East to get The Hyve S3 credentials for the testing bucket for the QA reports.

On a separate note, I am working on getting the test ready for the data export from FITFILE to the SDE Project S3 bucket(s). We are hoping to implement the existing CLI inside our data pipeline, and by adding a button to the frontend to export Query Plan results, we believe this will reduce any user errors that may have happened with the existing CLI.

You previously gave me credentials which I ran a data export test with. The IAM role includes "arn:aws.......staticinfra-eoe-automatio-dlzinfradevs3fitfile.....". Is this still the same IAM role we will use for the data export test to S3. And is this still the bucket: "dlz-dev-s3-fitfile-ff2502-905418144317" to use for the test?

In your last email, you mentioned testing export from 2 FITFILE Projects into 2 different buckets. Could you provide us with those 2 buckets?

Also I am assuming the iam role will be the same for all test cases, and will not change per SDE project context?

Oh, I've just spotted an error in the cloud formation bucket policy though which we'll need to push out, but trivial so will get that sorted immediately One last thing, can you send the iam role-arn for the assume role for the FITFILE -> S3 export?

Found them:

- dev - `arn:aws:iam::905418144317:role/staticinfra-eoe-automatio-dlzinfradevs3fitfile7AC5B-StRCYN1gshNG`
- tst - `arn:aws:iam::339713007003:role/staticinfra-eoe-automatio-dlzinfratsts3fitfile81AED-U8E5ngxEE2Sr`

> **Keiran Raine | Health Innovation East**
>
> Policy against TST is now corrected. LZA deploy is pending for: STG role assume permissions link to userfitfile-s3-prd user + role assume permissions Easwaran Chandrasekaran | Health Innovation East has been briefed.

This user has been created and credentials shared to Helana For the Hyve bucket Option 1 works for us:

1. fitfile-s3 can be used for DEV/TEST with the credentials shared. I will implement the LZA changes for this user to assume role dlz-dev-writer-codisc/dlz-tst-writer-codisc
2. For PROD we can use this new user fitfile-s3-prd with assume role access to dlz-prd-writer-codisc

Please let me know if my understanding is correct and this is an expected solution

Hi Easwaran Chandrasekaran | Health Innovation East, so from our perspective, there are two requirements we are trying to meet:

1 - FITFILE SDE Project Extract export to SDE S3 project bucket.

2FITFILE Data Provider export The Hyve QA reports to a different SDE S3 bucket.

For the first, we need these users:

1. fitfile-s3 (dev/test) -  (Keiran provided credentials for the fitfile-s3 user and has configured assume role policy for pushing to the test project bucket).
2. fitfile-s3-prd - The same as above but for the prod environment (as you have mentioned)

For the second, we need these users:

1. one user for testing the Hyve QA reports push to S3 - the bucket Keiran provided is this: `eoe-sde-tst-dqr-339713007003`  
   we believe for the test we can just use the fitfile-s3 user again if it has assume role policy to push to that test bucket.
2. one production user **per data provider using The Hyve** (so one for MKUH and one for NNUH) for pushing the OMOP QA reports to the SDE production environment QA report bucket.

   As we have not deployed to MKUH or NNUH yet, we do not need these users yet.

So in summary, we think we can just use the fitfile-s3 user for both tests which we will run today. Please let us know if this is aligned to what you expect as well.

Hi Oliver, Yes we are aligned:

1. **fitfile-s3** user can be used for Project Extract export to SDE S3 project bucket >> Using assume role: staticinfra-eoe-automatio-dlzinfra**dev**s3fitfile7AC5B-StRCYN1gshNG / staticinfra-eoe-automatio-dlzinfra**tst**s3fitfile81AED-U8E5ngxEE2Sr / staticinfra-eoe-automatio-dlzinfra**stg**s3fitfileB175A-xCvgDbEsdBgx (Non - PROD)
    - **fitfile-s3-prd** user can assume staticinfra-eoe-automatio-dlzinfra**prd**s3fitfile199DD-QdfxpM5Amoy1 for PROD testing

    > > Both ready to test

2.  For the Hyve QA reports to DQR bucket: >> In Progress, will be ready to test today   1. **fitfile-s3** user can assume dlz-dev-writer-codisc to access eoe-sde-dev-dqr-905418144317 bucket 2. **fitfile-s3** user can assume dlz-tst-writer-codisc to access eoe-sde-tst-dqr-339713007003 bucket 3. **fitfile-s3** user can assume dlz-stg-writer-codisc to access eoe-sde-stg-dqr-339713007003 bucket 4. **fitfile-s3-prd** user assume dlz-prd-writer-codisc to access eoe-sde-prd-dqr-381492210920 bucket
    Once the hyve QA reporting with fitfile-s3 user goes well in non-prod, I will work on created separate users for each data provider instead of **fitfile-s3-prd**

> **Oliver Rushton (Guest)**
>
> brilliant, thanks - let us now when the fitfile-s3 user can assume the roles to access the Hyve QA report buckets 🙂

We are ready to test the Hyve QA Bucket now Please let me know if you are facing any issues Hi Easwaran Chandrasekaran | Health Innovation East, Could you check 2 things for us:

1. Can you see the Hyve QA reports in the `eoe-sde-tst-dqr-339713007003` bucket?  
2. Can you see 2 files in the `dlz-tst-s3-fitfile-ff2504-339713007003` bucket - one called `CUH-NNUH-and-MKUH-project-extract-synth-0-3.json.gz` and the other called `manifest.csv`?

If they are both there, then we can say the tests were successful we got this, but the hyve bucket is empty:

we got this, but the hyve bucket is empty:  We have enforced encryption for Putobject action - should that be removed

![[Pasted image 20251024134340.png]]

![[Pasted image 20251024134347.png]]

Hi Oliver Rushton you will need to add the below headers when writing to the Hyve bucket:

```sh
"s3:x-amz-server-side-encryption-aws-kms-key-id": "arn:aws:kms:eu-west-2:339713007003:key/3d6bbd7c-1a80-432d-830b-9df6b11e1130"  
"s3:x-amz-server-side-encryption": "aws:kms"
```
