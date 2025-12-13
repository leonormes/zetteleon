---
aliases: []
author:
confidence: 
created: 2025-02-07T12:57:56Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source: "https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/mesh-guidance-hub/client-user-guide#how-to-send-a-mesh-message"
source_of_truth: []
status: 
tags: []
title: mesh_client_user_guide
type:
uid: 
updated: 
version:
---

## MESH Client User Guide

The MESH 'client' is a piece of software installed onto your server. It allows you to send large electronic files between a MESH mailbox at one organisation to a MESH mailbox at another organisation in a secure environment.

There are three different types of MESH, so please check with your IT administrators or systems suppliers if you are unsure which type of MESH you have. This guidance is for MESH client users only.

Files up to a maximum of 20Gb can be sent. To send larger than 75Mb (compressed) the AllowChunking flag must be set. The file size for transmission is calculated by the client after compression by gzip, if this exceeds 75Mb the file will not be sent, and the chunking (AllowChunking flag) must be used.

---

### Apply for a MESH Mailbox

To send and receive files, you'll need a MESH mailbox. During the installation of the MESH client, your organisation will have created a mailbox, however you may require several mailboxes to be associated with one organisation. 

There are many services and types of data that MESH can facilitate. We recommend you have separate mailboxes for the different services you may be using. For example, you may have one mailbox for data concerning the [national data opt-out (NDOP)](https://digital.nhs.uk/services/national-data-opt-out) and one for [Child Protection Information Sharing (CP-IS)](https://digital.nhs.uk/services/child-protection-information-sharing-service) data. 

Whilst waiting for NHS Digital to approve your new mailbox request, you can also check that your organisation has the MESH client set up on the server. The MESH client is responsible for the actual sending and receiving of messages and data via the MESH system. We recommend requesting your IT department or systems suppliers to complete this task for you, if you do not already have MESH client.

Please refer to our [MESH client installation guidance](https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/mesh-guidance-hub/client-installation-guidance) for assistance with installing and configuring MESH client.

---

### Configure Your MESH Mailbox

If the MESH mailbox request form is correctly completed, we'll reply to you within 10 days. You'll receive two emails from NHS Digital once your MESH mailbox application has been processed and approved:

1. Will give all the configuration information for your mailbox, as well as the workflow IDs for the messages you have indicated the mailbox will be used for. You will need the Workflow ID for sending a MESH message.
2. Will contain your MESH mailbox password.

Please email the configuration information to your IT contact, so they may configure your MESH mailbox to send and receive messages. As part of this configuration process, you should be granted access and permission to a number of folders set up on a shared folder.

These folders will act as your mailbox. The next section will cover these folders in more detail.

---

### Your MESH Mailbox

Congratulations, your mailbox is set up and ready to use.

You should now have access to your mailbox which will look like several folders. The number and names of the folders can differ depending upon how your MESH client is configured; the default set up is to have a main folder called “MESH-DATA-HOME” which holds the folders “failed”, “in”, “out” “sent” and “temp”.

#### Folder Functions

All messages you wish to send to another MESH mailbox should be put in the "out" folder.

Messages that have been successfully processed will be automatically moved to the “sent” folder.

Messages that have been unsuccessfully processed from the “out” folder will be automatically moved to the “failed” folder.

Messages that are received from another mailbox will appear within the “in” folder

---

### How to Send a MESH Message

Each MESH message to send is comprised of:

- a .dat file - this is the data file (payload) and contains the data you wish to send
- a .ctl file - this is the control file and provides the required information for MESH to route the message to the correct recipient

Both files must have the same name for the message to send correctly (and the given .dat or .ctl file extension at the end). For example, to send a file, you would need both a NHSD_26092019_1120.ctl and a NHSD_26092019_1120.dat file.

---

A suggested file name format, as used above, is: “Organisation_Date_Time”. This ensures there are no duplicates on MESH.

You can use any text editor, including Notepad or Wordpad, to create or edit the .dat and .ctl files.

#### Create the .dat (data) File

MESH can send all types of data. 

Rename the data you wish to send as a .dat file. This can be done in two ways: adding on the “.dat” extension after the original file type or removing the original file type extension and replacing with “.dat”.

For example, you may have a xxxx.csv file that you wish to send. You can either add the file type to the end (rename the file xxxx.csv.dat) or change the file type (rename the file xxxx.dat). With the former option, your recipient will need to remove the “.dat” from the file name to view, and with the latter, the recipient will need to know what programme to open the data file with, as there is no indication from the file name what type of data is contained. Choose the option most suitable for you and your recipient.

#### Create the .ctl File (also Known as the Control file)

This is the companion to the .dat file and contains all message meta-data in an XML file. 

The structure of the file must match the format of the example below. The text highlighted in bold should be replaced with your own organisation’s details. Without these changes, your file will not successfully be delivered and processed.

<DTSControl>
<Version>1.0</Version>
<AddressType>DTS</AddressType>
<MessageType>Data</MessageType>            
<WorkflowId>XXXXXXXXXXX</WorkflowId>
<To_DTS>XXXXXXXX</To_DTS>
<From_DTS>XXXXXXX</From_DTS> 
<Subject>XXXSubjectHeaderXXX</Subject>
 <LocalId>XXXXXXXX</LocalId> 
<Compress>Y</Compress>
<AllowChunking>Y</AllowChunking>
<Encrypted>N</Encrypted>
</DTSControl>

The <WorkflowID> section should be the name of the correct [workflow ID](https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/mesh-guidance-hub/endpoint-lookup-service-and-workflowids) described in the email received when your mailbox was first created.

The <ToDTS> section should be the name of your recipient’s mailbox. If you do not know what this is already, it's usually easiest to ask your recipient directly for their MESH mailbox name. Otherwise, please refer to the [MESH endpoint lookup service page](https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/mesh-guidance-hub/endpoint-lookup-service-and-workflowids) for further guidance on finding a mailbox name.

The <FromDTS> section should be the name of your mailbox ID, included on the email received when your mailbox was first created.

The <Subject> section is optional and acts like an email subject header, so you may use this as an opportunity to explain to the recipient what the message is about, name a specific member of staff for the recipient mailbox’s information, or what the message contains. You may leave blank if you wish. 

The <LocalId> section is an optional field. You can specify any reference or information which is useful to you, such as which clinician sent the file. You may leave blank if you wish.

The <Compress> section is to indicate that the data file can be compressed by the MESH client. Put “Y” if you wish for this, and a “N” if you do not want it compressed.

The <AllowChunking> section is to indicate that the data file can be chunked by the MESH client.

To support the transfer of files in excess of 75Mb (compressed). If set to “Y” the client will support the transfer of files up to a maximum of 20Gb. Failure to set this flag when attempting to transfer files with a size in excess of 75Mb will result in a failed transfer. To support the transfer, the client will process large files in 20Mb chunks. 

#### Send both the .dat and .ctl Files as a Message

Once you’ve created the .dat and .ctl files, place these in the “out” folder in your mailbox. If you're moving the files individually into this folder, please ensure you put the .dat file in first. 

The timing of the message being sent will depend upon how the MESH client is configured to connect to the mailbox – this is referred to as “polling”. This is automatically set up to be every 30 minutes, however your MESH client installer may have altered the configuration of your MESH client for specific needs. When your mailbox has polled, your messages will then automatically be moved to your “sent” folder and get sent through to the “in” folder of your recipient’s mailbox.

The .ctl file will be altered when moved from your “out” folder to your “sent” folder. The new structure of the .ctl file will be:

<DTSControl>
<Version>1.0</Version>
<AddressType>DTS</AddressType>
<MessageType>Data</MessageType>
<From_DTS>xxxxxxxx</From_DTS>
<To_DTS>xxxxxxxx</To_DTS>
<Subject>xxxxxxxx</Subject>
<LocalId>xxxxxxxx</LocalId>
<DTSId>DTS–20101216101210-927652</DTSId>
<PartnerId></PartnerId>
<Compress>Y</Compress>
<Encrypted>N</Encrypted>
<WorkflowId>PATH_MEDRPT_V3</WorkflowId>
<ProcessId></ProcessId>
<DataChecksum></DataChecksum>
<IsCompressed >Y</IsCompressed >
<StatusRecord>
<DateTime>20101216102012</DateTime>
<Event>Transfer to DTS Server</Event>
<Status>Success</Status>
<StatusCode>0</StatusCode>
<Description></Description>
</StatusRecord>
</DTSControl>

To check that your message has been sent correctly, the <Status> field of the returned .ctl file should read “Success”. 

It's up to your organisation to manage the “sent” folder and archive/delete files as necessary.

---

### Error Messages and Failure to Send

If the file you submitted cannot be sent, you will receive a .ctl file to the “in” folder. To know why your message did not send correctly, refer to the <Event>, <Status> and <StatusType> fields of the .ctl file received to the “in” folder.

The common types of error you may receive in your “in” folder, and how to resolve them, are listed below.

|  |  |  |  |  |
| --- | --- | --- | --- | --- |
| Collect report | COLLECT | SUCCESS | 00 | Data collect success confirmation |
| Collect error | COLLECT | ERROR | 01 | .ctl file is missing or inaccessible |
| Collect error | COLLECT | ERROR | 02 | .dat file is missing or inaccessible |
| Server authentication error | TRANSFER | ERROR | 03 | Server authentication failure caused by an invalid certificate, unreachable certificate or path problem |
| Transfer report | TRANSFER | SUCCESS | 00 | Data transfer success confirmation |
| Client authentication error | TRANSFER | ERROR | 04 | Client authentication failure caused by invalid MESH username or authentication string |
| Delay report | TRANSFER | SUCCESS | 05 | The MESH client has failed to transfer the data file to the MESH server. The MESH client will try again |
| Transfer fail | TRANSFER | ERROR | 06 | The MESH client has failed to transfer the data file to the MESH server - the maximum attempts to retry have been reached |
| Server fail | SEND | ERROR | 07 | Invalid <FromDTS> address in .ctl file |
| Server fail | SEND | ERROR | 08 | Invalid <ToDTS> address in .ctl file |
| Server fail | SEND | ERROR | 12 | Unregistered <ToDTS> address |
| Non delivery | SEND | ERROR | 13 | SMPT delivery failure |
| Non delivery | SEND | ERROR | 14 | MESH delivery failure |
| Poll report | RECEIVE | SUCCESS | 00 | Poll report success confirmation |
| Poll fail | RECEIVE | ERROR | 15 | Check the MESH client log file for more information |
| Server authentication error | RECEIVE | ERROR | 16 | Invalid server certificate |
| Client authentication error | RECEIVE | ERROR | 17 | Invalid MESH username or authentication string |

- Status typeCollect report
- <Event>COLLECT
- <Status>SUCCESS
- <StatusType>00
- DescriptionData collect success confirmation
- Status typeCollect error
- <Event>COLLECT
- <Status>ERROR
- <StatusType>01
- Description.ctl file is missing or inaccessible
- Status typeCollect error
- <Event>COLLECT
- <Status>ERROR
- <StatusType>02
- Description.dat file is missing or inaccessible
- Status typeServer authentication error
- <Event>TRANSFER
- <Status>ERROR
- <StatusType>03
- DescriptionServer authentication failure caused by an invalid certificate, unreachable certificate or path problem
- Status typeTransfer report
- <Event>TRANSFER
- <Status>SUCCESS
- <StatusType>00
- DescriptionData transfer success confirmation
- Status typeClient authentication error
- <Event>TRANSFER
- <Status>ERROR
- <StatusType>04
- DescriptionClient authentication failure caused by invalid MESH username or authentication string
- Status typeDelay report
- <Event>TRANSFER
- <Status>SUCCESS
- <StatusType>05
- DescriptionThe MESH client has failed to transfer the data file to the MESH server. The MESH client will try again
- Status typeTransfer fail
- <Event>TRANSFER
- <Status>ERROR
- <StatusType>06
- DescriptionThe MESH client has failed to transfer the data file to the MESH server - the maximum attempts to retry have been reached
- Status typeServer fail
- <Event>SEND
- <Status>ERROR
- <StatusType>07
- Description

Invalid <FromDTS> address in .ctl file

- Status typeServer fail
- <Event>SEND
- <Status>ERROR
- <StatusType>08
- DescriptionInvalid <ToDTS> address in .ctl file
- Status typeServer fail
- <Event>SEND
- <Status>ERROR
- <StatusType>12
- DescriptionUnregistered <ToDTS> address
- Status typeNon delivery
- <Event>SEND
- <Status>ERROR
- <StatusType>13
- DescriptionSMPT delivery failure
- Status typeNon delivery
- <Event>SEND
- <Status>ERROR
- <StatusType>14
- DescriptionMESH delivery failure
- Status typePoll report
- <Event>RECEIVE
- <Status>SUCCESS
- <StatusType>00
- DescriptionPoll report success confirmation
- Status typePoll fail
- <Event>RECEIVE
- <Status>ERROR
- <StatusType>15
- DescriptionCheck the MESH client log file for more information
- Status typeServer authentication error
- <Event>RECEIVE
- <Status>ERROR
- <StatusType>16
- DescriptionInvalid server certificate
- Status typeClient authentication error
- <Event>RECEIVE
- <Status>ERROR
- <StatusType>17
- DescriptionInvalid MESH username or authentication string

---

### Receive MESH Messages to Your MESH Mailbox

If another organisation has sent your mailbox a message, it will be saved to your “in” folder. There may be a delay in between the sending and receiving of a file, depending upon the configuration of your MESH client, and the sender’s.

To access the message, double click on the file to open it. If the data file has the equivalent of two file extensions (such as xxxx.csv.dat), rename the file to remove the .dat, and the file will open automatically with the correct programme.

MESH will delete messages that haven't been downloaded 5 days after they have been sent, as the default configuration of MESH client does not send a notification of receiving a new message. If you fail to collect a message after 5 days, and it has been deleted, it is possible for us to resend this message within 30 days of being sent if you contact the National Service Desk at [support.digitalservices@nhs.net](https://digital.nhs.uk/). We recommend that you have monitoring in place to ensure the MESH client is running.

---

### Simplify MESH

There are some ways to make the use of MESH mailbox more efficient. These changes require someone to edit the configuration of the MESH client, so please ask your IT department about implementing the items below.

Message received notification - create a script that monitors the “in” folder for new files and sends an email to select people who need to know a new file has been received.

Automatically send a message from the .dat file only - create a folder where you can save .dat files you wish to send. A script could then be created that detects the new .dat file, uses the MESH mailbox ID used in the.dat file’s name and automatically creates the .CTL file required, before copying both files to the MESH Mailbox “out” folder.

Last edited: 21 May 2024 2:15 pm
