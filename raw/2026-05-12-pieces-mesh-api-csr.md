---
created: 2026-05-12T22:06:30+00:00
modified: 2026-05-26T11:43:43+00:00
pieces_ids: ["01b4c4df-6703-44a5-927c-e2569d8faea4", "880f648a-a7ac-4f9d-983d-0efc9e0ed0e8", "89eefa6a-2342-4bfc-8470-6c6e2673a7af", "97548f1b-28de-4b46-8c32-832157f94f57", "e69b17ef-cbec-44d6-9e4e-f471c5b8ee68", "ffe79b06-86f9-4c29-9177-3fa72c84563a"]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-12-pieces-mesh-api-csr
---

## Pieces LTM Ingest—MESH API CSR

Ingestion window: Last 24 hours (4-hour window returned 0 new assets; extended per skill instructions)

Summary: 6 assets captured for MESH API CSR.

---

### Asset 1 (Pieces: 880f648a-a7ac-4f9d-983d-0efc9e0ed0e8)

Captured: 2026-05-12T14:41:08.973413Z

The CSR generated successfully—no error, just an informational warning. Here's what you need to know:

### The Warning—You Can Ignore It

The `JKS keystore uses a proprietary format` warning is cosmetic. It's a standard Java 9+ advisory nudging you toward PKCS12. Your `MESH.keystore` already works, and the CSR (`mesh-api.csr`) was written correctly. Do not run the migration command—it would overwrite your existing keystore in place and isn't necessary for submitting to the NHS.

### The CSR is Ready

Your new CSR is at:

```
/Volumes/DAL/Fitfile/meshCerts/mesh-api.csr
```

With CN: `8KM90HC001.8KM90.api.mesh-client.nhs.uk`

### Next Step—Send to the NHS National Service Desk

Reply to Peter Begg's email (CS1446557) with:

- The `mesh-api.csr` file attached
- The draft reply above (confirm you're API-based, replacing expired cert, new CSR uses the correct API FQDN)
- The URID reference number from the ticket (required for validation per the NHS guidance)
- Your MESH API Conformance Certificate if you have it—the manual application guidance requires it for API users

You can verify the CN in the CSR is correct before sending with:

```bash
openssl req -noout -text -in /Volumes/DAL/Fitfile/meshCerts/mesh-api.csr | grep Subject
```

It should show `CN = 8KM90HC001.8KM90.api.mesh-client.nhs.uk`.

---

### Asset 2 (Pieces: 97548f1b-28de-4b46-8c32-832157f94f57)

Captured: 2026-05-12T14:40:58.030198Z

The user has run the keytool command and it generated the CSR successfully (no error output, just a warning about the keystore format). The warning is about the JKS (Java KeyStore) format being proprietary and recommending migration to PKCS12. This is a standard Java keytool warning.

The key question here is: did the CSR generate successfully? Yes - the command completed without an error, only a warning. The warning is non-critical for their use case.

They need to know:

1. The CSR was generated successfully at `/Volumes/DAL/Fitfile/meshCerts/mesh-api.csr`
2. The JKS warning is non-critical - they don't need to migrate for this purpose
3. Now they're ready to submit the CSR to the NHS National Service Desk for certificate signing.

---

### Asset 3 (Pieces: e69b17ef-cbec-44d6-9e4e-f471c5b8ee68)

Captured: 2026-05-12T14:40:52.511394Z

keytool -certreq -alias meshclient \
  -keystore /Volumes/DAL/Fitfile/meshCerts/MESH.keystore \
  -file /Volumes/DAL/Fitfile/meshCerts/mesh-api.csr \
  -dname "CN=8KM90HC001.8KM90.api.mesh-client.nhs.uk"

Enter keystore password:

Warning:

The JKS keystore uses a proprietary format. It is recommended to migrate to PKCS12 which is an industry standard format using "keytool -importkeystore -srckeystore /Volumes/DAL/Fitfile/meshCerts/MESH.keystore -destkeystore /Volumes/DAL/Fitfile/meshCerts/MESH.keystore -deststoretype pkcs12".

---

### Asset 4 (Pieces: 89eefa6a-2342-4bfc-8470-6c6e2673a7af)

Captured: 2026-05-12T14:39:27.853758Z

I have a rich picture of your work today. Here's a draft reply to Peter Begg at the NHS National Service Desk that addresses his two questions directly, grounded in what I can see you worked on this morning.

---

### Draft Reply—CS1446557

To: ssd.nationalservicedesk@nhs.net

Subject: RE: CS1446557 | Request for Information

---

Dear Peter,

Thank you for coming back to me on this.

To answer your questions directly:

We are using the MESH API (not the MESH client), and this is to replace an existing, expired certificate. We use the MESH API programmatically via a Python client (`nhs_client.py`) to access the NHS Data Opt-Out service, using a certificate and private key for TLS authentication.

Understood—I will regenerate a new CSR using the API naming convention with the FQDN:

`8KM90HC001.8KM90.api.mesh-client.nhs.uk`

I will send the new CSR across to you as soon as it has been generated.

Kind regards,

Leon Ormes

FITFILE Group Ltd (ODS: 8KM90)

---

### Context from Your Work Today

Here's what I can see from your LTM to confirm the above is accurate:

- The original CSR you generated and attached had the CN `optout-8KM90.fitfile.thirdparty.nhs.uk`—this is the MESH client naming format (the `thirdparty` domain), which is why Peter flagged it as unsuitable for API use.
- The API FQDN format the NHS requires is `<Identifier>.<ODScode>.api.mesh-client.nhs.uk`. Peter has confirmed your existing record already has `8KM90HC001.8KM90.api.mesh-client.nhs.uk`.
- Your [`meshCerts` directory](file:///Volumes/DAL/Fitfile/meshCerts) at `/Volumes/DAL/Fitfile/meshCerts` contains `mesh.csr`, `mesh2.csr`, `MESH.keystore`, `keystore.p12`, and `mesh-client-key.pem`—the keystore is already set up, you just need to regenerate a CSR with the correct CN.
- You were working with Oliver Rushton and Susannah Thomas on this in Teams around 12:05 PM today, and the context was that the existing certificate had expired, causing connection errors.
- In a recorded conversation around 12:46 PM you noted the discrepancy between the certificate common name on the guidance page vs. what you had previously generated.

### To Generate the New CSR with the Correct FQDN

Run this from your `meshCerts` directory (the keystore password you used previously was `fitfile_nhs`):

```bash
keytool -certreq -alias meshclient \
  -keystore /Volumes/DAL/Fitfile/meshCerts/MESH.keystore \
  -file /Volumes/DAL/Fitfile/meshCerts/mesh-api.csr \
  -dname "CN=8KM90HC001.8KM90.api.mesh-client.nhs.uk"
```

Then attach `mesh-api.csr` in your reply to Peter. You may also want to include a copy of the MESH API Conformance Certificate if you have it—the NHS guidance notes this is required for Step 5 of the manual application process ([MESH certificate guidance](https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/mesh-guidance-hub/certificate-guidance#manually-apply-for-a-mesh-certificate-hscn-n3-internet-access-)).

---

### Asset 5 (Pieces: ffe79b06-86f9-4c29-9177-3fa72c84563a)

Captured: 2026-05-12T14:38:56.111893Z

The user wants me to look at their work today about the mesh API certificates, and they've received a reply email from the National Service Desk. They want me to search their memory for context about this work today. Let me search for relevant information about mesh API certificates from today.

---

### Asset 6 (Pieces: 01b4c4df-6703-44a5-927c-e2569d8faea4)

Captured: 2026-05-12T14:38:49.622425Z

Look at my work today about the mesh api certificates. Here is the reply email

Thank you for contacting the National Service Desk.

In order for us to investigate CS1446557 further, please can you provide us with the following information.

The information we require is:

Hi Leon,

is this to replace the existing certificate? oe ar you planning on using the NHS MESH client.

If you are using your API and replacing the existing certificate, can you regenerate a new CSR with the FQDN of 8KM90HC001.8KM90.api.mesh-client.nhs.uk as this is what we already have, and it has the API in it to show that it is being used solely for an API, whereas the CSR you have attached is suitable only for use with the NHS MESH client.

Kind Regards

---
