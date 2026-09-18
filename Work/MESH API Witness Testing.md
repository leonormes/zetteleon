---
aliases: [MESH Compliance Testing, MESH Witness Test, NHS MESH Accreditation]
created: 2026-09-16T00:00:00+00:00
modified: 2026-09-16T10:42:03+00:00
permalink: llmeon/30-library/200-projects/mesh-api-witness-testing
project_category: refined_deployment
project_name: Refined Deployment
project_status: reference
tags: [compliance, fitfile, healthcare, mesh, nhs, witness-testing]
title: MESH API Witness Testing
type: null
---

## Summary

FITFILE's connection to the NHS MESH API (Message Exchange for Social Care and Health) required NHS England assurance via a formal witness test before live operational credentials were issued. This note is the full context record: the NHS process and requirements, the official test-case spec, the defects found during pre-witness evidence review, the outcome, and pointers into the actual codebase and test files that implement/exercise this.

Outcome: PASSED. Per `Plan for application of fixed IG rules and guidelines` (Confluence): _"FITFILE has been granted live operational credentials for MESH API access after successfully completing the witness test and obtaining an accreditation certificate confirming compliance."_

> [!note] Not to be confused with…
> FITFILE ran a separate, unrelated witness test for the TPP SystmOne SCAL/IM1 submission (data extraction via TPP's dev environment, NHS England IM1 team, Joanne Maw/Caroline Holmes, 2024–2025). That is a different assurance track with a different NHS team and different test scope. This note is MESH-specific only (NHS England Solution Assurance / Citizen and Interoperability Cell, Nigel Watts).

---

## 1. Timeline (From Email: "MESH API for FITFILE Group Limited - FITFILE")

Correspondence between Nigel Watts (Senior Practitioner–Senior Test and Assurance Analyst, Transformation Directorate / Solution Assurance / Citizen and Interoperability Cell, NHS England) and FITFILE (Annabel Flinn—Project Manager, Leon Ormes—Software Engineer, cc Petros Kotsidis, Paddy Yung NHS England).

| Date | From → To | Content |
|---|---|---|
| 3 Nov 2023 | Nigel Watts → Annabel Flinn, Ian Whitney, Jon Bradshaw, Petros Kotsidis | Kickoff email. Explains the full assurance process (see §2), attaches the test-case spreadsheet, asks FITFILE to request 3 test mailboxes in INT via ITOC Support Desk. |
| 16 Feb 2024 | Annabel → Nigel | Ran sending (201/202) and receiving (401/402) compliance tests; asks about the DAT file and requests witness-test scope details. Provides mailbox ID `8KM90OT001`, config constants (`MESH_URI_INTEGRATION`, `OPT_OUT_WORKFLOW_ID='SPINE_NTT_UPHOLDING'`, `OPT_OUT_MAILBOX_ID='X26OT154'`). |
| 20 Feb 2024 | Nigel → Annabel | DAT file = just the payload, arbitrary content. Confirms once Sending/Receiving evidence is accepted, Witness Test is booked (allowing lead time for test 703's 5-day wait). Asks if chunking will be supported. |
| 4–5 Mar 2024 | Annabel ↔ Nigel | Nigel reviews evidence: no Handshake message found, List not called immediately after Send (5 min delay instead), message retrieved twice before Acknowledge (duplicate-download risk). Confirms compression/chunking are optional—skipped tests just get a caveat on the Technical Conformance Certificate. |
| 7–13 Mar 2024 | Annabel ↔ Nigel | Handshake issue reportedly fixed. Nigel re-reviews: Handshake done 4× in a burst on 07/03 but not since; two messages retrieved multiple times before ack. Confirms compression/chunking not mandatory. |
| 28 Mar 2024 | Annabel → Nigel | All outstanding issues resolved and tests re-run; asks to schedule the witness test (5 working days notice previously cited). |
| 4 Apr 2024 | Nigel → Leon/Annabel | Still an issue: message `20240329012613692574_1F60C3` retrieved dozens of times (66× on one day alone) before being acknowledged—must Ack immediately after Retrieve to clear it from the next List. |
| 4 Apr 2024 | Leon → Nigel | Root cause = FITFILE's opt-out logic re-sending stale requests, not the core MESH client (`mesh-proxy.ts` / `Mailbox.ts`); will disable that path to get clean logs. Proposes validating the Non-Delivery Report test (703) via a local Docker MESH sandbox (fabricated dates) instead of waiting the real 5 days, since the code path can be exercised identically. |
| 4 Apr 2024 | Nigel → Leon | Wants to see the sandbox-based Non-Delivery Report evidence, and will compare it against a real 5-day-aged report he generated himself as a sanity check. Will book the witness test once a clean set of Send/Receive logs is confirmed. |

_(Thread ends here in the available correspondence—the actual witness test call itself, and its outcome, are not present in the email record. The accreditation confirmation comes from Confluence—see §5.)_

---

## 2. NHS Assurance Process (From Nigel Watts' Original Email + Confluence)

1. Evidence must show conformance to the [MESH API spec](https://digital.nhs.uk/developer/api-catalogue/message-exchange-for-social-care-and-health-api), tracked against the official test-case spreadsheet (`MESH API Compliance Test.xlsx`, v1.6—attached to the Confluence page below).
2. Sending (201, 202) and Receiving (401, 402)—self-tested first, evidence submitted by email.
3. Everything else—live Witness Test: Teams call, screen-shared, ~2 hours, run against NHS's integration environment (INT).
4. 3 test mailboxes needed in INT (requested via `itoc.supportdesk@nhs.net`):
   - Mailbox for the system under development (send/receive).
   - Independent mailbox using the [MESH Java Client](https://digital.nhs.uk/services/message-exchange-for-social-care-and-health-mesh/compare-mesh-services#mesh-client), to send/receive against FITFILE's system.
   - Dormant/dead-letter mailbox for test cases 703/705 (message must expire after 5 days).
5. Witness test only booked once 201/202/401/402 evidence accepted—with lead time for the 703 5-day wait.

---

## 3. Full Official Test-case Catalogue (Spec V1.6)

Source: `MESH API Compliance Test.xlsx`, attached to Confluence page _"NHS National Data Opt Out Test Spec & Instructions"_.

| Set | Case | What it checks | Pass criteria |
|---|---|---|---|
| 2–Sending | 201 | Send uncompressed | Msg arrives unaltered; pattern Authenticate→Send→Check Inbox; mandatory headers (`Authorization`, `Mex-From`, `Mex-To`, `Mex-WorkflowID`, `Content-Type: application/octet-stream`) |
| 2–Sending | 202 | Send compressed (`Content-Encoding: GZIP`) | Same, `Mex-Content-Compressed=Y`/`Mex-Content-Compress=Y` |
| 4–Receiving | 401 | Receive uncompressed | Pattern Authenticate→Check Inbox→Download→Acknowledge; DAT matches original |
| 4–Receiving | 402 | Receive compressed | Same + GZIP `Content-Encoding`/`Accept-Encoding` |
| 5–Chunking _(optional)_ | 501 | Receive chunked >200MB | Repeated `Download message block` calls; MD5 of reassembled file matches |
| 5–Chunking _(optional)_ | 502 | Send chunked >200MB | `Allow-Chunking` header, `Mex-Chunk-Range`, final block marker MEX0178 |
| 6–High volume | 601 | 600 messages waiting | Pattern: Check Inbox → 500×(Download+Ack) → Check Inbox → 100×(Download+Ack)—List batches cap at 500 |
| 7–Error handling | 701 | Auth failure (mailbox disabled) | Handles `403 Authentication Failed` gracefully |
| 7–Error handling | 702 | Invalid recipient mailbox ID | Handles `417 Invalid Recipient` gracefully |
| 7–Error handling | 703 | Undelivered message | `202 Accepted` initially; after 5 days marked "Undelivered"; must handle the report |
| 7–Error handling | 704 | Download non-existent message ID | Handles `404 Message Does Not Exist` |
| 7–Error handling | 705 | Re-download an already-downloaded message (uses 703's message) | Handles `410 Gone` |
| 8–Self-certification | 801 | Max 1 thread per mailbox (declared, not live-tested) |
| 8–Self-certification | 802 | Adherence to published API spec (declared) |
| 8–Self-certification | 803 | Will handle undelivered-message notifications appropriately (declared) |

Compression (202) and chunking (501/502) are optional—if unsupported, those tests are skipped and a caveat is added to the Technical Conformance Certificate instead (confirmed twice by Nigel Watts).

---

## 4. Defects Found against FITFILE's Implementation (Pre-witness Evidence Review)

From the email review cycle (Feb–Apr 2024):

- Handshake (Authenticate / MEX0033) must run once every 24h—was missing, then only firing in bursts.
- Check Inbox must fire immediately after Send—was waiting for the next scheduled poll (~5–20 min later).
- Acknowledge promptly—message must be Acked right after Download, not retrieved repeatedly first. NHS logs showed a message retrieved 66+ times in one day before being acked. Root cause traced by Leon Ormes to the opt-out logic re-processing the same message, not the core MESH client.
- Non-Delivery Report (703) validated via local sandbox—Leon used the NHS Digital `mesh-sandbox` Docker Compose locally with fabricated message dates to avoid the real 5-day wait; Nigel accepted comparing this against a real aged report as validation.

---

## 5. Outcome & Current Live Config

Per Confluence _"Plan for application of fixed IG rules and guidelines"_:

> "FITFILE has been granted live operational credentials for MESH API access after successfully completing the witness test and obtaining an accreditation certificate confirming compliance."

- Organisation: FITFILE Group Ltd, ODS Code `8KM90`
- Production Mailbox ID: `8KM90HC001`
- Production MESH API Base URL: `https://mesh-sync.spineservices.nhs.uk`

NDOO business-rule context (Confluence _"National Data Opt-Out"_ + _"Plan for application of fixed IG rules and guidelines"_):

- NDOO checks must be applied within 20–21 days of registration (regulatory limit); FITFILE's ETL cadence is currently ~22 days—worth re-checking this margin.
- MESH "Check for Opt-outs" response can take up to ~1 hour, sometimes up to a day.
- Env vars in use: `MESH_PYTHON_FILE_PATH`, `MESH_CLIENT_CERT`, `MESH_CLIENT_KEY`, `MESH_MAILBOX_PASSWORD`, `MESH_HASH_SECRET`, `MESH_MAILBOX_ID`, `MESH_BASE_URL`, `MESH_OPTOUT_MAILBOX_ID`, `MESH_OPTOUT_WORKFLOW_ID`, `MESH_POLLING_INTERVAL_MS`.

---

## 6. Codebase—implementation

Repo: `InsightFILE` (path: `/Volumes/DAL/Fitfile/gitlab/FITFILE/Application/InsightFILE`)

All MESH code lives under `apps/fitconnect/src/services/optout/MeshService/`:

| File | Role |
|---|---|
| `Mailbox.ts` | Core MESH REST client: `sendMessageToMesh` (outbox POST), `getListOfMessageId` (paginated inbox list via `links.next`), `getMessageWithId` (download + chunk reassembly via `mex-total-chunks`), `getMessageChunk`, `ackMessage` (PUT `…/status/acknowledged`), `validateMailbox`, `mailboxMonitor` (compliance-test-only helper) |
| `axiosClient.ts` | `HttpClient` impl—get/post/put over TLS (`https.Agent`); maps Axios errors → `Result<Err>` with `{status, data}` cause |
| `generate-auth-token.ts` | Builds `NHSMESH <mailbox>:<nonce>:<count>:<timestamp>:<hmac-sha256>` Authorization header |
| `construct-message-headers.ts` | Builds client/send headers (`Mex-ClientVersion`, `Mex-From`, `Mex-To`, `Mex-WorkflowID`, `Mex-LocalId`) + `generateOptoutRequestId` |
| `checkForReportMessage.ts` | Flags `mex-messagetype: REPORT` (non-delivery report); logs error if type header missing entirely |
| `constants.ts` | Auth schema name, timestamp format, NHS PTL Root CA cert |
| `types.ts` | `MailboxConfig`, `MeshMessage`, `InboxMessageList`, `MeshError`, `HttpClient` interface |
| `MessageHeaders.ts` | `parseHeaders`—strips down to `mex-*` headers |
| `MeshOptoutSource.ts` | Higher-level `OptoutSource` impl: `submitOptoutRequest`, `listOptoutResponses`, `ingestNewMessages` (the list→download→checkReport→ack loop) |

Manual/local test tooling:

- `docs/mesh-sandbox.md`—spins up a local `mesh-mailbox` Helm chart (port-forwarded to `localhost:8700`); this is what the skipped integration tests below target. Also documents the staging-environment SpiceDB/relationship setup for simulating opt-out end-to-end.
- `scripts/post-mesh-optout-response.sh` + `scripts/mocks/mesh_mailbox_response_message.txt`—generates valid mock NHS numbers and posts a simulated MESH mailbox response via curl.

---

## 7. Codebase—tests, Mapped to the Official NHS Test Cases

`apps/fitconnect/src/services/optout/MeshService/__tests__/Mailbox.test.ts`:

- Unit (always run): header parsing, auth-token structure/HMAC, single-message download, chunked-message download & reassembly, outbox POST header correctness.
- `describe.skip(TestTypes.Integration)` (manual only, needs local MESH sandbox on `localhost:8700`):
  - Empty inbox → `[]`
  - Single message in inbox → returned in list
  - Invalid mailbox → `403` handled
  - Pagination: 600-message inbox → all 600 IDs retrieved across paginated List calls _(≈ case 601)_
  - Download non-existent message → `404` _(= case 704)_
  - Full round-trip: send → list → download (asserts exact `mex-*` headers) → ack → confirms removed from list _(≈ cases 401/402)_
  - Outbox POST to invalid recipient → `403` _(partial—NHS's real case 702 expects `417`, not `403`)_

`apps/fitconnect/src/services/optout/MeshService/__tests__/ingestMessages.test.ts`:

- Unit: `MeshOptoutSource` correctly separates a `REPORT`-type message from a `DATA`-type message; `checkForReportMessage` logs on REPORT, silent on DATA, logs separately if `mex-messagetype` is missing _(≈ case 703)_.
- `describe.skip(TestTypes.Integration)`: high-volume ingestion—600 messages, all downloaded+acked (599 processed, 1 deliberately missing), second call confirms mailbox now empty _(= case 601, idempotency of ack)_.

`apps/fitconnect/src/services/optout/__tests__/OptoutService.integration.test.ts`—despite the name, `MeshOptoutSource` is fully mocked here; this tests `OptoutResponseProcessorService`'s message-ID→tracking mapping and S3 storage, not the MESH wire protocol.

### Coverage Gap Summary

| NHS case | Repo coverage |
|---|---|
| 201/202 Send | ✅ unit + skipped integration |
| 401/402 Receive | ✅ |
| 501 Receive chunked | ✅ (reassembly unit test) |
| 502 Send chunked | ❌ not implemented—`sendMessageToMesh` has no chunk-splitting logic at all |
| 601 High volume | ✅ |
| 701 Auth failure (403) | ✅ (via generic invalid-mailbox 403, not the specific disabled-mailbox scenario) |
| 702 Invalid recipient (417) | ⚠️ partial—existing test only asserts a `403`, not `417` |
| 703 Undelivered report | ✅ (unit test + local sandbox validation approach) |
| 704 Message doesn't exist (404) | ✅ |
| 705 Already downloaded (410 Gone) | ❌ not tested |
| 801/802/803 | N/A—declarative, not code-tested |

If touching `Mailbox.ts` or `axiosClient.ts`, the three gaps above (502, 702's 417, 705's 410) are exactly the places where a regression could slip past the existing test suite despite being part of what NHS's official spec expects.

---

## 8. Source Documents

Confluence (space `FITFILE`, `fitfile.atlassian.net/wiki`):

- [NHS National Data Opt Out Test Spec & Instructions](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1621032961) (id `1621032961`)—original NHS process email + attached `MESH API Compliance Test.xlsx` v1.6 (full test spec, §3 above)
- [NHS MESH API](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1678737410) (id `1678737410`)—FITFILE's internal notes mapping test 201/202 to `mesh-proxy.ts`
- [MESH API Documentation](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/1678868496) (id `1678868496`)—Swagger/OpenAPI link
- [Understanding the NHS Opt-Out Process for Research Data](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2096726017) (id `2096726017`)—sandbox testing narrative, NHS Digital approval confirmation
- [Plan for application of fixed IG rules and guidelines](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2098167827) (id `2098167827`)—confirms accreditation obtained; NDOO implementation detail (source-vs-ETL opt-out, cadence)
- [National Data Opt-Out](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2247655425) (id `2247655425`)—current live NDOO design, requirements table (NHS Digital Operational Policy Guidance refs), env var interface, mesh-sandbox stub reference

Email threads (as pasted into chat, not separately archived):

- _"MESH API for FITFILE Group Limited - FITFILE"_—Nigel Watts (NHS England) ↔ Annabel Flinn / Leon Ormes / Petros Kotsidis, 3 Nov 2023–4 Apr 2024. This is the primary MESH witness-testing thread (§1 above).
- _"Test Environment Extract Setup"_—Annabel Flinn ↔ TPP Integration team (Bridie Haworth, Lauren Nightingale), May 2024. Related to the TPP SCAL track, not MESH—kept separate per the disambiguation note above.
- _"FITFILE - SCAL Submission"_—Susannah Thomas/Petros Kotsidis ↔ NHS England IM1 team (Joanne Maw, Caroline Holmes) and TPP, Nov 2024–Jun 2025. Also the TPP SCAL/IM1 track, not MESH.

Codebase: `InsightFILE` repo, `apps/fitconnect/src/services/optout/MeshService/` (see §6–7).
