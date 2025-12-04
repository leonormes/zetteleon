---
aliases: []
confidence: 
created: 2025-10-22T08:41:18Z
epistemic: 
last_reviewed: 
modified: 2025-12-04T13:27:53Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Hutch Bunny Failing to Connect to OMOP Database
type:
uid: 
updated: 
version:
---

**Hutch Bunny Failing to Connect to OMOP Database: Cleaned Email Thread (Markdown)**

---

**From Oliver Rushton (FITFILE), 17 October 2025, 11:05**
To: Jakub Jaworski
Cc: Leon Ormes, Weronika Jastrzebska

> Hi Jakub,
>
> Has the SQL account for Bunny been disabled? We are seeing errors that imply this in our monitoring solution.
>
> Kind regards,
> Ollie
> Senior Software Engineer, FITFILE

---

**From Jakub Jaworski (Cambridge University Hospitals), 20 October 2025, 21:13**
To: Oliver Rushton
Cc: Leon Ormes, Weronika Jastrzebska

> Hi Ollie,
>
> Sorry, I have been away last week. Is this still a problem?
> Which SQL user is this for? *omopsynth* is enabled, *omopprd* is not.
>
> Best wishes,
> Jakub

---

**From Weronika Jastrzebska (FITFILE), 21 October 2025, 16:46**
To: Jakub Jaworski, Wai Keong Wong, Alexis McKenna
Cc: Leon Ormes, Oliver Rushton, Susannah Thomas, Mark Dines-Allen, Laura Clarke, Robin Mofakham, Helena Ahlfors

> Hi Jakub,
>
> I just wanted to share a quick update on the outstanding work on our end:
>
> 1. After uploading your Data Schema via the API and completing DNS networking configuration with Telefónica, we noticed an error in one of the OMOP tables (conceptrelationship). It is currently failing the schema validation; however, the schema definition was successful. This appears to be a bug on our side, which we are currently resolving.
> 2. We believe this issue should not prevent you from checking the classification for all OMOP tables and confirming whether you're happy with it—happy to discuss on the call if needed.
> 3. Once the schema issue is resolved, we will check the Bunny connection and confirm whether the problem with the SQL user still persists.
> In the meantime, we can proceed with the final configuration step—connecting your Data Source to the SDE Tenant.
> Could you please confirm who would be the best person to complete this with? Anyone who has access to the FITFILE application within your node would be suitable.
> Once confirmed, we can schedule a quick call to finalise this step as soon as possible.
> 
> Lastly, do you have a preferred method for sharing the Tenant ID with the person who will join the call? It isn't considered sensitive information, but if you'd prefer, we can share it live during the call instead. The Tenant ID is required to complete the connection between your Data Source and the SDE Tenant, and we will be providing it for you.
>
> Best regards,
> Weronika
> Product Manager, FITFILE

---

**From Jakub Jaworski (Cambridge University Hospitals), 22 October 2025, 08:30**
To: Weronika Jastrzebska
Cc: Leon Ormes, Oliver Rushton, Susannah Thomas, Mark Dines-Allen, Laura Clarke, Wai Keong Wong, Alexis McKenna, Robin Mofakham, Helena Ahlfors

> Hi Weronika,
>
> Thank you for the update. I am happy to help with finalising the connection.
> Can hop on a call tomorrow, Thursday 23rd, 8:30–12am or 3:15–4pm.
> Alternatively, Friday 24th, 11am–4pm.
> No problem with sharing the tenant id during the call.
>
> Please let me know if there is anything I can help with in the meantime.
>
> Best wishes,
> Jakub

---

**From Weronika Jastrzebska (FITFILE), 22 October 2025, 08:50**
To: Jakub Jaworski
Cc: Leon Ormes, Oliver Rushton, Susannah Thomas, Mark Dines-Allen, Laura Clarke, Wai Keong Wong, Alexis McKenna, Robin Mofakham, Helena Ahlfors

> Hi Jakub,
>
> Perfect, can we do 2:30 pm today if that works?
> If you could have a look at the email from Ollie regarding the SQL users that would be great.
>
> Many thanks,
> Weronika
> Product Manager, FITFILE

---

**From Jakub Jaworski (Cambridge University Hospitals), 22 October 2025, 09:36**
To: Weronika Jastrzebska
Cc: Leon Ormes, Oliver Rushton, Susannah Thomas, Mark Dines-Allen, Laura Clarke, Wai Keong Wong, Alexis McKenna, Robin Mofakham, Helena Ahlfors

> Hi Weronika,
>
> I am really sorry, but I am tied up all day today. However, please feel free to send a Teams request for the times indicated below.
>
> Best wishes,
> Jakub

---
