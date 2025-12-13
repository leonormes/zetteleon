---
aliases: []
confidence: 
created: 2025-03-11T10:24:58Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:39Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [azure, IAM]
title: Roles Assigned to Gareth Hailes and Why They Are Problematic
type: plan
uid: 
updated: 
version:
---

gareth.hailes@fitfile.com = no roles

ghailes@fitfile.com = Multiple privileged roles

![[Screenshot 2025-03-11 at 10.16.31.jpg]]

Yes, **this screenshot definitely raises red flags for a security expert**, and confirms your concerns about excessive access for this colleague, Gareth Hailes. Let's break down why these assigned roles are a significant security concern:

**Roles Assigned to Gareth Hailes and Why They Are Problematic:**

1. **Global Administrator:**

    - **Description:** "Can manage all aspects of Microsoft Entra ID and Microsoft services that use Microsoft Entra identities."
    - **Severity: CRITICAL RED FLAG.** This is the **highest privilege role in Azure AD.** A Global Administrator has effectively "god mode" access to *everything* within your Azure Tenant. They can:
        - Manage all users, groups, and administrators, including resetting passwords, deleting accounts, and assigning roles (even to themselves, including Global Administrator again if removed).
        - Configure all Azure AD settings, including security policies (like MFA, Conditional Access), domain names, branding, and integration with other services.
        - Access data in *almost all* Microsoft 365 services, including SharePoint, Exchange, Teams, and potentially even some Azure resources depending on configuration and delegated permissions.
        - Effectively control the entire identity layer of your organization's cloud presence.
    - **Why it's a Red Flag:** **Granting Global Administrator to a *consultant*, especially for day-to-day activities, is an extremely dangerous practice.** It violates the principle of least privilege and creates a massive single point of failure and potential for abuse. It's seldom justified for routine tasks and should be *extremely* limited to dedicated administrative accounts used in tightly controlled emergency or setup scenarios.

2. **Privileged Role Administrator:**

    - **Description:** "Can manage role assignments in Microsoft Entra ID, and all aspects of Privileged Identity Management."
    - **Severity: HIGH RED FLAG.** This role is *specifically for managing access control* itself within Azure AD. A Privileged Role Administrator can:
        - Manage role assignments to *any* Azure AD role, including other administrative roles (except Global Administrator in some scenarios, but still significant power).
        - Activate and configure Privileged Identity Management (PIM), which controls Just-In-Time access.
        - Essentially, they control *who has what permissions* within your Azure AD environment.
    - **Why it's a Red Flag:** Giving this role to the same consultant who already has Global Administrator **compounds the problem.** It means they not only have ultimate power but also the *power to delegate and control* who else has power. This further solidifies the "single point of control" issue and increases the risk of unauthorized privilege escalation or manipulation of access controls.

3. **Reports Reader:**

    - **Description:** "Can read sign-in and audit reports."
    - **Severity: Low Concern (in isolation), but relevant in context.** This role itself is less powerful. It allows viewing sign-in and audit logs.
    - **Why it's relevant in context:** While reading reports isn't inherently dangerous, *in combination* with Global Administrator and Privileged Role Administrator, it means Gareth Hailes has full visibility into all user activity and security events, and *also* the power to control and change anything without oversight. He is essentially monitoring his own potentially excessive actions.
4. **Security Administrator:**

    - **Description:** "Can read security information and reports, and manage configuration in Microsoft Entra ID and Office 365."
    - **Severity: HIGH RED FLAG.** This role is designed for security operations and configuration. A Security Administrator can:
        - Manage security-related configurations in Azure AD and Office 365, such as security policies, MFA settings, threat management, and data governance settings.
        - Access security reports and dashboards.
        - Potentially respond to security alerts.
    - **Why it's a Red Flag:** While a Security Administrator role is needed in a security team, granting it to the same person with Global Administrator and Privileged Role Administrator is **grossly excessive and unnecessary.** It gives them overlapping and redundant security management capabilities, again further concentrating power and blurring lines of responsibility and oversight. It's like giving the bank vault manager also control of the security cameras and alarm system with no independent checks.

5. **Security Reader:**

    - **Description:** "Can read security information and reports in Microsoft Entra ID and Microsoft 365."
    - **Severity: Low Concern (in isolation), but redundant in context.** Similar to Reports Reader, in isolation, this is a read-only role for security information.
    - **Why it's redundant in context:** With Global Administrator and Security Administrator roles, the Security Reader role is completely unnecessary. They already have far more than read-only access to security information.

**Overall Assessment and Red Flags to a Security Expert:**

- **Massive Red Flag:** The assignment of **Global Administrator, Privileged Role Administrator, and Security Administrator** roles to a *single consultant account* is a **massive security red flag**. It screams "violation of least privilege," "single point of failure," and "poor security architecture."
- **Violation of Least Privilege:** These roles grant far, far more permissions than any consultant should typically need for security and compliance *expertise*. Security expertise involves *advising* and *configuring*, not typically requiring the highest level of operational control on a daily basis.
- **Single Point of Failure/Abuse:** Concentrating this level of power in one account is incredibly risky. If this account is compromised, or if the consultant acts maliciously or makes a serious error, the impact could be catastrophic for your Azure environment and sensitive NHS data.
- **Lack of Segregation of Duties:** The consultant is essentially given responsibility for *everything* security-related and has the power to monitor and control his own actions. There are no checks and balances, which is a core principle of security and compliance (the "four-eyes principle" we discussed).
- **Non-Compliant and Unprofessional:** This setup is highly unlikely to meet NHS DSPT requirements or UK GDPR Article 32 for security and access control. As you correctly identified, it's also highly unprofessional and not aligned with industry best practices for cloud security.
- **Undermines Trust and Transparency:** It creates a lack of transparency and trust within the team. As you experienced, raising concerns about workstation differences is deflected, and the concentration of power makes it difficult for others to question or audit effectively.

**Presenting this Information:**

When you present this to the company owner, show this screenshot and explain in simple terms:

- "This screenshot shows the roles assigned to [Consultant Name]. The role marked 'Global Administrator' is like having the ultimate master key to our entire Azure system – everything we have. The role 'Privileged Role Administrator' means they also control *who else* gets access to important areas."
- "Having one person, especially an external consultant, with this level of access is like giving them complete control over our bank vault. It's a huge risk, not just technically, but for our business and our responsibility to protect patient data."
- "Security best practices and NHS guidelines strongly advise *against* this. We need to move to a system where access is granted based on 'least privilege,' where changes are reviewed, and where no single person has this level of unchecked power."

**In conclusion, yes, this screenshot is a significant red flag.** It visually confirms your concerns and provides concrete evidence of a highly insecure and non-compliant access model. It strengthens your argument for urgently implementing the GitOps and least privilege IAM plan we've been discussing. Use this visual evidence to clearly communicate the severity of the situation to your company owner.

That's a common tactic to deflect scrutiny, but easily verifiable with Azure's built-in audit logs! His claim that he uses a separate, unprivileged account for day-to-day activities is testable. Here's how you can check which user account has the most activity:

**Methods to Check User Activity in Azure:**

You'll primarily use **Azure Monitor's Log Analytics** and **Azure Activity Log** to investigate this. Here's a breakdown using both Azure Portal (for ease of use) and Azure CLI/PowerShell (for more programmatic analysis):

**1. Using Azure Portal - Azure Activity Log:**

- **Pros:** Quick for a general overview, user-friendly interface.
- **Cons:** Less powerful for detailed analysis, limited filtering and aggregation.

**Steps:**

1.  **Navigate to Azure Monitor:** In the Azure portal, search for and select "Monitor."
2.  **Go to Activity Log:** In the Monitor blade, select "Activity log."
3.  **Filter by User:**
    -   Click the "Add filter" button.
    -   Choose "Category" and select "Administrative". (This will focus on management operations, not just read actions).
    -   Click "Add filter" again.
    -   Choose "Initiated by (actor)" and enter the User Principal Name (UPN) of his **privileged account** (the one with all the roles, e.g., `gareth.hailes@yourcompanydomain.com`). Click "Apply".
    4.  **Set Time Range:** Adjust the "Time range" at the top to a relevant period (e.g., "Last 7 days," "Last 30 days").
    5.  **Note the Number of Events:** Look at the total number of events displayed in the Activity Log for his privileged account within the chosen time range. Make a mental note or write it down.
4.  **Repeat for Day-to-Day Account:**
    -   Click "Edit filters".
    -   Change the "Initiated by (actor)" filter to his **claimed day-to-day account** (e.g., `gareth.hailes.daytoday@yourcompanydomain.com`). Click "Apply".
    -   Note the total number of events for this account in the same time range.
5.  **Compare Event Counts:** Compare the number of events for both accounts. If the privileged account shows significantly *more* administrative activity than the day-to-day account, his claim is questionable.

**2. Using Azure Portal - Log Analytics Workspace (Recommended for Deeper Analysis):**

- **Pros:** Powerful querying with Kusto Query Language (KQL), detailed analysis, aggregation, and visualization possible.
- **Cons:** Requires some familiarity with KQL. You need to have Azure Activity Logs being sent to a Log Analytics Workspace (which is good practice anyway and should be set up as part of the security plan).

**Steps:**

1.  **Navigate to your Log Analytics Workspace:** In the Azure portal, search for and select "Log Analytics workspaces" and choose your workspace.
2.  **Go to "Logs":** In your Log Analytics Workspace blade, select "Logs".
3.  **Run Kusto Query to Check Activity Log for Privileged Account:** Paste and run the following KQL query, replacing placeholders with the correct User Principal Names and Time Range:

```kusto
AzureActivity
| where TimeGenerated >= ago(30d) // Adjust time range as needed (e.g., ago(7d) for last 7 days)
| where Caller =~ "gareth.hailes@yourcompanydomain.com" // Replace with his privileged account UPN
| summarize count() by OperationNameValue, CategoryValue
| order by count_ desc
```

-   **Explanation of Query:**
        * `AzureActivity`: Specifies the table to query (Azure Activity Logs).
        * `where TimeGenerated >= ago(30d)`: Filters for logs within the last 30 days. Adjust `30d` to your desired time range (e.g., `7d` for 7 days).
        * `where Caller =~ "gareth.hailes@yourcompanydomain.com"`: Filters for events where the "Caller" (user who initiated the action) matches his privileged account UPN. `~=` is case-insensitive match. **Replace `"gareth.hailes@yourcompanydomain.com"` with the *actual* UPN.**
        * `summarize count() by OperationNameValue, CategoryValue`: Aggregates the results, counting the number of operations by "Operation Name" (what action was performed) and "Category" (e.g., Administrative, Security, Alert).
        * `order by count_ desc`: Orders the results by the count in descending order, showing the most frequent operations first.

    4.  **Review Results for Privileged Account:** Examine the query results. Note the total `count` of operations and the types of `OperationNameValue` and `CategoryValue` listed. Look for administrative operations (e.g., `Write`, `Create`, `Update`, `Delete`, `Action`).
    5.  **Run Kusto Query for Day-to-Day Account:** Modify the query by changing the `Caller =~ "..."` filter to his claimed **day-to-day account UPN** (e.g., `gareth.hailes.daytoday@yourcompanydomain.com`). Run the modified query:

```kusto
    AzureActivity
    | where TimeGenerated >= ago(30d)
    | where Caller =~ "gareth.hailes.daytoday@yourcompanydomain.com" // Replace with his day-to-day account UPN
    | summarize count() by OperationNameValue, CategoryValue
    | order by count_ desc
```

6.  **Compare Results:** Compare the results from both queries.
-   **High Activity on Privileged Account, Low on Day-to-Day Account:** This strongly suggests he is *not* primarily using the day-to-day account for Azure management and his claim is likely untrue. Focus on the *types* of operations - if the privileged account shows many "Write," "Create," "Update," "Delete" operations, it indicates administrative work.
-   **Similar or Higher Activity on Day-to-Day Account:** This would be unexpected given the role assignments you've shown. Investigate further. It's still concerning if the "day-to-day" account is doing significant administrative work if it's *not* supposed to have those permissions.
        * **Very Low Activity on Both:** This is less likely but possible if he hasn't been very active in Azure recently *within the chosen time range*. Extend the time range in the query (e.g., `ago(90d)`) and re-run the analysis.

**3. Using Azure CLI/PowerShell (for Scripting and Automation):**

- **Pros:** Scriptable, can automate data collection, export to files, integrate with reporting.
- **Cons:** Requires more technical skill, output might need further processing for easy comparison.

**Example Azure CLI:**

Bash

```sh
# Privileged Account Activity
privilegedUPN="gareth.hailes@yourcompanydomain.com" # Replace
echo "Activity for Privileged Account: $privilegedUPN"
az monitor activity-log list --caller $privilegedUPN --max-records 100 --query "[].operationName" -o table

# Day-to-Day Account Activity
dayToDayUPN="gareth.hailes.daytoday@yourcompanydomain.com" # Replace
echo "\nActivity for Day-to-Day Account: $dayToDayUPN"
az monitor activity-log list --caller $dayToDayUPN --max-records 100 --query "[].operationName" -o table
```

- **Explanation:** These scripts use Azure CLI (`az`) or PowerShell (`Get-AzActivityLog`) to fetch Activity Logs, filter by "Caller" (user), and group/count operations to show the most frequent actions. *Replace the placeholder UPNs.*

**Important Considerations:**

- **Time Range:** Analyse activity over a sufficiently representative time period (at least a week, preferably a month) to account for variations in workload.
- **Operation Types:** Focus on *administrative* operations (Create, Update, Delete, Write, Action) in the Activity Logs. Read-only operations are less indicative of privileged activity.
- **Log Retention:** Ensure your Azure Activity Logs are retained for a sufficient period to cover your analysis timeframe. Log Analytics workspaces allow for longer retention.
- **"Noise" in Logs:** Azure Activity Logs can be verbose. Focus on patterns and significant administrative operations. Don't get bogged down in every single log entry.
- **Present Findings Objectively:** When presenting your findings to the company owner, present the *data* from the logs (counts of operations, types of operations) in a clear and objective way. Let the data speak for itself. If the privileged account clearly shows more administrative activity, the data will contradict the consultant's claim and strengthen your case for change.

By using these methods to analyse Azure Activity Logs, you can gather concrete evidence to verify or refute the consultant's claim about using a separate, less privileged account, and build a stronger, data-driven argument for implementing a more secure and compliant Azure access model.

It's understandable to feel frustrated when faced with resistance to modern security best practices, especially from someone who is supposed to be the expert. Instead of directly challenging his stance, let's approach this diplomatically by trying to understand his perspective first and then gently guiding him towards better practices.

Here's a strategy for learning about his views and gently nudging him towards best practices, framed as seeking his expert opinion and understanding his rationale:

**Approach: "The Curious Learner" - Seeking Expert Insights**

Instead of being confrontational, adopt a posture of genuine curiosity and a desire to learn from his experience. Frame your questions as wanting to understand his thinking process and learn from his 20 years in tech.

**Conversation Starters & Questions:**

1. **Acknowledge His Experience and Expertise (Start Positive):**

    - "Gareth, you've been in tech for 20 years, which is fantastic experience. I'm really keen to tap into your deep knowledge, especially as we're refining our Azure security approach."
    - "With your extensive background, you've likely seen many different approaches to system administration. I'd really value your perspective on our current Azure setup."
2. **Open-Ended Question about Current Admin Role Status:**

    - "Looking at the admin roles assigned to your account, they're quite comprehensive. Could you walk me through your thinking behind this particular role setup? What's the rationale for having this level of access consolidated in one place in our current environment?"
    - "Given your security background, I'm interested to understand your approach to managing administrative access in Azure. Can you share your overall philosophy on how you typically handle privileged roles in cloud environments?"
    - "From your experience, what are the key benefits and considerations, in your opinion, when structuring administrative access like this in a cloud environment like Azure?"
3. **Address the "Two Accounts" Claim and Activity Logs (Indirectly, Fact-Based):**

    - "You mentioned having two accounts, and using the non-admin one for day-to-day. To help me understand the activity patterns, I've been reviewing the Azure Activity Logs. [Optionally, *if comfortable, you can subtly share data without being accusatory*:] I've noticed most of the administrative actions seem to be originating from the account with the assigned admin roles. Could you help me understand how you typically separate your tasks between these accounts in practice? Perhaps I'm not interpreting the logs correctly."
    - **(If he denies significant activity on the admin account):** "That's interesting, because when I looked at the Azure Activity Logs for the past month, I seemed to see quite a bit of administrative activity logged against [his admin account UPN]. Perhaps there's something I'm misunderstanding about how those logs work? Could you maybe help me interpret them correctly in the context of how you use the accounts?" *This is a gentle way to present the data without directly accusing him of lying.*
4. **Introduce "Modern Cloud Security Best Practices" as an Evolving Field (Not as Criticism):**

    - "Cloud security has evolved so rapidly, especially with things like zero trust and least privilege becoming really central. From your experience, how have you seen best practices around administrative access change over the past few years, particularly with the move to cloud platforms like Azure?"
    - "I've been reading a lot about 'least privilege' and 'Just-in-Time access' in cloud environments, driven by frameworks like Zero Trust and recommendations from organizations like NCSC and NIST. I'm curious about your thoughts on how these modern approaches compare to more traditional admin models, especially in terms of practical implementation in Azure."
    - "With the increasing focus on compliance and data protection, especially in sectors like healthcare and with regulations like GDPR and DSPT, are you seeing any shifts in how organizations are structuring administrative access in cloud environments to meet these stricter requirements?"
5. **Focus on NHS Data Compliance and Business Risk (Relate to Company Goals):**

    - "For us, with NHS patient data, compliance and security are absolutely paramount. From your perspective, how confident are you that our *current* administrative access model aligns with the stringent requirements of the NHS DSPT and UK GDPR, specifically in areas like access control and audit logging?"
    - "What are your thoughts on the *business risks* associated with concentrating administrative access in a single account, especially if that account were ever compromised? How do you see that balancing against the convenience of a centralized approach?"
    - "Given our responsibility to the NHS, what would you consider the *strongest* approach to demonstrate to them that we are taking every possible measure to secure patient data, particularly concerning privileged access management?"
6. **"Curiosity-Driven" Questions to Prompt Self-Reflection:**

    - "What are some potential *downsides* or limitations, in your view, of relying heavily on a single administrator account with broad permissions in the long run, especially as our Azure environment grows more complex and our team expands?"
    - "If we were to aim for an even *more* secure setup, building on our current approach, what would be the *first couple of things* you might consider changing or refining about our administrative access model?"
    - "Thinking about 'auditability' and 'accountability,' if we needed to quickly investigate a security incident or demonstrate compliance, how easy or difficult do you think it would be with our *current* administrative access setup compared to a more granular, GitOps-based approach?"

**Active Listening and Gentle Guidance:**

- **Listen Carefully:** Pay close attention to his responses. Try to understand his underlying assumptions and reasoning, even if you disagree.
- **Validate Experience (Where Appropriate):** Acknowledge his experience, even if you challenge his conclusions. "I understand you've used this approach successfully in the past..."
- **Be Respectful but Firm:** Don't be confrontational, but don't back down from your concerns about security and compliance.
- **Be Prepared to Counter Weak Arguments (Gently):** If his justifications seem weak or outdated, be prepared to gently introduce counterpoints based on best practices, security frameworks, and the specific risks associated with NHS data. Example: "I understand the convenience aspect, but I'm also concerned about the NCSC guidelines that strongly recommend against broad, standing admin access, especially for critical systems."
- **Focus on Solutions (The GitOps Plan):** After understanding his perspective, subtly steer the conversation back to the *solution* – the GitOps and improved IAM plan you've developed. Highlight how it addresses the limitations of the current approach while still being practical and efficient for your team.

**Goal:**

The aim of this approach is *not* to win an argument or make him feel defensive. The goal is to:

- **Understand his perspective and thought process.**
- **Gently introduce modern security best practices as relevant and valuable in the cloud context.**
- **Highlight the business and compliance drivers for change, especially concerning NHS data.**
- **Guide him towards recognizing the limitations of the current approach and the benefits of adopting a more secure and GitOps-driven model.**
- **Open a dialogue, not shut it down.** You want to create an environment where he can re-evaluate his approach without feeling personally attacked.

By taking this "curious learner" approach, you can have a more productive conversation and increase the likelihood of influencing him to embrace more secure and compliant practices, while still respecting his experience and expertise. Good luck! Let me know how the conversation goes.
