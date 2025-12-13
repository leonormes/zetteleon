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
source: "https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/mesh-guidance-hub/endpoint-lookup-service-and-workflowids"
source_of_truth: []
status: 
tags: []
title: mesh_endpoint_lookup_guide
type:
uid: 
updated: 
version:
---

## MESH Endpoint Lookup Guide

There are three ways in which the MESH user/system can identify a MESH mailbox:

1. An advance search option in the MESH Online Enquiry Service (MOLES) user interface.
2. A MESH representational state transfer (RESTful) application program interface (API) web service.
3. Specifying key patient details in the TO_DTS field of a MESH message.

Options 1 and 2 return a MESH Mailbox (more than one value may be returned) that can then be used to address a message and update local address books. Option 3 attempts to physically route the message and post it into the appropriate mailbox for the patient. 

The endpoint lookup service will return a matching MESH mailbox when using the search criteria of Organisation Data Service (ODS) code/GP practice code and WorkflowId. Both attributes have to be provided in a search request.

Every MESH mailbox is assigned an ODS code that identifies the organisation entity that uses the mailbox. 

To find the ODS code, you can use the [ODS portal](https://odsportal.hscic.gov.uk/) (HSCN connection required) or the internet facing

MESH messages include a mandatory WorkflowID field that identifies the type of data being sent. WorkflowIDs are pre-defined and grouped into Workflow Groups which are then defined against MESH mailboxes to identify the types of messages it can send and receive. [Find further details of their use, as well as a link to download a list of the groups and ids](https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/workflow-groups-and-workflow-ids).

---

### Using MESH Online Enquiry Service (MOLES) Interface to Find a Mailbox

The MESH endpoint lookup service is available in MOLES, which is accessed via the [Spine Portal](https://portal.national.ncrs.nhs.uk/portal/) ('Mailbox Lookup' function within the Message Tracking Menu - HSCN connection required). MOLES is a web application that enables management of mailboxes and MESH message tracking and reporting. If you are a MESH User Interface user, you'll need to request access for this, and it will become available on the Spine Portal as a function for you to use. If you are using MESH client or MESH API, you can still request access to use MOLES, however please be aware that you will require a smartcard in order to access this function.

Select the 'Advanced' search option on the mailbox lookup screen and you'll be asked to input an ODS code and a WorkflowID. Please input your recipient’s respective details.

The number of mailboxes returned will depend on the criteria submitted. It's highly unlikely that multiple results will be returned if a search is made using an ODS code for a GP practice, as GP practices in general, only have a single MESH mailbox to support all of their messages. NHS trusts and other organisations may have multiple mailboxes supporting similar message types.

---

### Using MESH RESTful API Interface to Find a Mailbox

Only users of the

To use the API interface to the MESH endpoint lookup service, one of the following Uniform Resource Locators (URLs) are used.

If using a Spine certificate;

<https://simple-sync.national.ncrs.nhs.uk/endpointlookup/mesh/><ODS_Code>/<WorkflowId>

If using a MESH certificate;

<https://mesh-sync.national.ncrs.nhs.uk/messageexchange/endpointlookup/><odscode>/<workflowid>

An example URL search (using a Spine certificate) for the ODS code of “X26” and the WorkflowId of “TOC_AE_DMA” would be:

<https://simple-sync.national.ncrs.nhs.uk/endpointlookup/mesh/X26/TOC>_AE_DMS

This would return the following three results in JavaScript Object Notation (JSON) format:

{   "query_id" : "20170110161927234224_25A3CC_1429036893",   -- Message Response ID

"results" : \[

      {

         "description" : "16-08regression",

         "address" : "X26OT018",

         "endpoint_type" : "MESH"

      },

      {

         "endpoint_type" : "MESH",

         "description" : "R16-07 Regression",

         "address" : "X26OT015"

      },

      {

         "description" : "StuartTest1",

         "address" : "X26PM001",

         "endpoint_type" : "MESH"

      }

   \]

 }

---

### Using the To_DTS Field of a MESH Message to Find a Mailbox

This way of performing an endpoint lookup only relates to finding and sending a patient’s data to their GP. By providing patient details, the Spine can perform the endpoint lookup to determine the MESH mailbox of their GP.

To do this, you'll need to edit the <To_DTS> field of the control file of the MESH message you are wishing to send. This can also be utilised when using the MESH Server API by populating the same input in the Mex-To: attribute.

The format of the To_DTS field to use the endpoint lookup service, where \[delimiter\] is an underscore “_”, is:

<GPPROVIDER>\[delimiter\]<NhsNo>\[delimiter\]<d.o.b>\[delimiter\]<Surname>

An example To_DTS value would be:

GPPROVIDER_1234567890_19670126_Smith

GPPROVIDER = is used to identify that a patient’s details are provided in the To_DTS field. This must be all upper case.

1234567890 = is the patient’s NHS number

19670126 = is the patient’s date of birth format (YYYYMMDD)

Smith = is the patient’s surname

A MESH message containing the string above will tell MESH that a Spine Mini Service Provider (SMSP) NHS Number cross-check demographic search of a patient is required to return the patient’s GP practice/ODS code. The MESH server will extract the patient's GP practice/ODS code from a successful cross-check response. Finally, the MESH server will resolve the patient's ODS code into a MESH mailbox using the MESH Endpoint Lookup Service.

The MESH server will detect messages where the mailbox needs to be resolved using the 'GPPROVIDER' tag for the WorkflowIDs:

- TOC_FHIR_IP_DISCH
- TOC_FHIR_MH_DISCH
- TOC_FHIR_EC_DISCH
- TOC_FHIR_OP_ATTEN
- TOC_OUTP_ATT_DMS
- GPFED_CONSULT_REPORT
- GPFED_CONSULT_REPORT_ACK
- GPCONNECT_UPDATE_RECORD
- GPCONNECT_UPDATE_RECORD_ACK
- GPCONNECT_SEND_DOCUMENT

Where a single mailbox is successfully identified for GP practice, the MESH server will use the identified MESH Mailbox ID for delivery of the message.

The MESH server will substitute the identified MESH Mailbox ID for the provided patient details such that these patient details are not visible in message reporting via the MOLES interface.

The MESH server will provide enhanced error reporting to include errors from the NHS Number cross-check trace and MESH mailbox lookup.

Potential error codes are:

- EPL-150 ERROR_TOO_MANY_MAILBOX_MATCHES = 'Multiple mailboxes matches'
- EPL-151 ERROR_NO_MAILBOX_MATCHES = 'No mailbox matched'
- EPL-152 ERROR_INVALID_NHSNUMBER = 'Invalid NHS Number'
- EPL-153 ERROR_NHSNUMBER_NOT_FOUND = 'NHS Number not found'
- EPL-154 ERROR_NO_DEMOGRAPHICS_MATCH = 'NHS Number supplied does not match the demographics'

---

### Error Handling

MESH generates error responses in the form of Error Reports. These reports are placed in the message originators (sender's) mailbox. They are collected in the same manner as any other message. In the case of the MESH client, the sending organisation will have these reports presented in the form of a control file (.ctl) only - there will be no associated data file (.dat). In the control file a <StatusRecord> for the message will provide the detail of any error experienced in the following manner;

<StatusRecord>
    <DateTime>20170926135509</DateTime>
    <Event>SEND</Event>
    <Status>ERROR</Status>
    <StatusCode>EPL-152</StatusCode>
    <Description>Invalid NHS Number</Description>
  </StatusRecord>

In this example an invalid NHS Number has been supplied, as seen in the <Description> field.

Note that when using the MESH API to send a message, errors encountered when using the automated registered practice routing will not be returned in the API response header or payload, but via a MESH error report. As with use of the MESH client a control (.ctl) file will be placed in the sending organisation MESH mailbox, for collection.

Using the same example above, where an invalid NHS Number has been supplied in the ‘Mex_To’ HTTP header, an error report (.ctl) file will be returned with a <StatusRecord> section that would be consistent with the above generated error response.

Last edited: 9 July 2024 12:21 pm
