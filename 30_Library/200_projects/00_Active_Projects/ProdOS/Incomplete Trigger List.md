---
created: 2026-01-13T03:49:56+00:00
modified: 2026-04-08T18:01:13+00:00
title: Incomplete Trigger List
uuid: 1b4977b7-748f-4ccf-8d06-a688493b3b93
---

SoT - DevOps Trigger List (v1.0)

Protocol:

 - [ ] Set Timer: 5 Minutes. (Strict limit to prevent hyper-focus). ^2026-04-01T22-57-00
	- [📱 View in Todoist app](todoist://task?id=6gHHgQ8fhpPX8FQv) (Created: 📝 2026-04-01T22:57)
 - Scan Mode: Read the prompt. If your brain says "Oh yeah, that thing…"—CAPTURE IT.
 - Do Not Execute: Do not fix the code now. Do not open the console. Just capture the Starter Task.
 - Apply PINCH: If a task feels heavy, tag it with a PINCH driver (e.g., Challenge: Can I script this in under 10 mins?).
1. The Active Scope (Agile & Jira)
 - Fake Progress: Is there a ticket in "In Progress" that hasn't moved in 3 days? (Capture: Check in on Ticket-123).
 - The "Done" Lie: Did I finish a deployment but forget to move the ticket to "Done"?
 - Scope Creep: Am I working on a Terraform refactor that isn't on the board? (Capture: Create ticket for VPC refactor).
 - The Stand-up Debt: Did I promise a link, a doc, or a review during stand-up that I haven't sent yet?
1. Infrastructure as Code (Terraform)
 - The Monolith: Is there a.tf file that is frustratingly long to scroll through? (Capture: Split main.tf into modules).
 - Drift Anxiety: Is there an environment (Dev/Stage) I suspect has drifted from the code?
 - Hardcoded Shame: Did I hardcode an AMI ID or a variable "just for now" that needs to be parameterized?
 - Version Lag: Are we using a Terraform provider version that is spamming us with deprecation warnings?
 - Orphaned State: Are there resources we deleted manually that are still in the state file?
1. Kubernetes & Helm (The Deployment Layer)
 - Values Bloat: Is the values.yaml file for our main app becoming a confusing mess?
 - Image Hygiene: Are we deploying images tagged:latest or old SHAs that need pinning?
 - Chart Rot: Are we using a Helm chart with deprecated API versions (e.g., old Ingress or PDBs)?
 - Secret Sprawl: Do we have Secrets in the cluster that should be in the external Vault/Secret Manager?
 - Namespace Junk: Are there "test" namespaces from last month that need deleting?
1. The Cloud (AWS & Azure)
 - Zombie Resources: Are there EBS volumes, Load Balancers, or Elastic IPs unattached and costing money?
 - Security Doors: Did I leave a Security Group open to 0.0.0.0/0 for "debugging" purposes?
 - IAM Bloat: Does the CI/CD user have AdministratorAccess when it only needs specific permissions?
 - Backup Trust: When was the last time I actually checked if a backup was created successfully?
1. Observability (Grafana & Logging)
 - The "No Data" Graph: Is there a panel in Grafana that is broken/empty that I ignore every day? (Capture: Fix or Delete Panel X).
 - Alert Fatigue: Is there an alert channel that I have muted because it's too noisy? (Capture: Tune threshold for CPU alert).
 - Blind Spots: Is there a specific error I keep seeing in logs that we don't have a metric for?
1. The Human API (Manager & Team)
 - Status Update: Is there a "Win" or a "Blocker" my manager doesn't know about yet?
 - Documentation Debt: Did I figure out a weird fix for a deployment failure that is only in my head? (Capture: Write SoT for Deploy Fix).
 - Continuous Delivery: What is the one manual step I do every deployment that I hate? (Capture: Investigate automating step X).
End of Protocol
Action: Take your captured list.
 - Apply the Two-Minute Rule: If it takes < 2 mins, do it now.
 - For the rest, define the Starter Task (Action 3.1) for each.
 - If you are overwhelmed, use SAVESTATE to dump the list and return to your primary task.
Would you like me to help you define the "Starter Task" for one of the items you just uncovered?

Here is a comprehensive Mind Sweep Incompletion Trigger List derived directly from David Allen's _Getting Things Done_ and _Making It All Work_ methodologies [1, 2].

This list is designed to jog your memory and help you capture "open loops"—anything pulling at your attention that needs to be clarified, processed, or organized.

## I. Professional Triggers

Projects

- Projects started, not completed
- Projects that need to be started
- "Look into…" projects
- Status reporting

Commitments/Promises to Others

- Boss/Partners
- Colleagues/Subordinates
- Other professionals
- Customers/Clients
- Vendors/Other organizations

Communications to Make/Get

- Phone calls
- Voice mails
- E-mails/Texts
- Letters/Memos
- Social media postings

Writing to Finish/Submit

- Reports/Evaluations/Reviews
- Proposals
- Articles/Marketing materials
- Instructions/Manuals
- Summaries/Minutes
- Rewrites and edits

Meetings

- Upcoming meetings (preparation)
- Meetings needing to be set or requested
- Debriefing past meetings (minutes/actions)

Administration

- Legal issues
- Insurance
- Personnel/Staffing
- Policies/Procedures

Financial

- Cash/Budgets
- Forecasts/Projections
- Profit & Loss/Balance sheet
- Credit line
- Payables/Receivables/Petty cash
- Banks/Investors/Asset management

Planning/Organizing

- Goals and objectives (short & long term)
- Business/Marketing/Financial plans
- Upcoming events/Presentations/Conferences
- Travel/Vacation/Business trips

Organization Development

- Organizational chart/Restructuring
- Roles/Job descriptions
- Facilities/New systems
- Change initiatives/Succession planning
- Organizational culture

Staff

- Hiring/Firing/Promoting
- Reviews/Compensation
- Staff development/Training
- Feedback/Morale

Sales & Marketing

- Campaigns/Materials/Public Relations
- Customers/Prospects/Leads
- Sales process/Training
- Relationship building/Tracking
- Customer service

Systems & Equipment

- Phones/Mobile devices
- Computers/Software/Databases
- Telecommunications/Internet
- Filing/Reference/Inventories/Storage
- Office space/Furniture/Decorations
- Supplies/Maintenance/Security

Professional Development

- Training/Seminars
- Things to learn/Find out
- Skills to practice/develop
- Books to read/study
- Formal education (degrees, licensing)
- Resume/Career research
- Professional wardrobe

Waiting For…

- Information/Answers to questions
- Delegated tasks/projects
- Replies to communications (emails, letters, proposals)
- Reimbursements/Insurance claims
- Ordered items/Repairs/Tickets

---

## II. Personal Triggers

Projects

- Projects started, not completed
- Projects that need to be started
- Projects for other organizations (service, community, volunteer, spiritual)

Commitments/Promises to Others

- Spouse/Partner
- Children
- Parents/Relatives
- Friends
- Professionals

Communications to Make/Get

- Calls/E-mails/Texts
- Cards and letters
- Thank-yous
- Social media postings

Upcoming Events

- Birthdays/Anniversaries
- Weddings/Graduations
- Holidays/Travel/Vacations
- Dinners/Parties/Receptions
- Cultural/Sporting events

Home & Household

- Real estate/Landlords
- Repairs/Construction/Remodeling
- Heating/AC/Plumbing/Electricity/Roof
- Landscaping/Driveway/Garage
- Walls/Floors/Ceilings/Decor/Furniture
- Appliances/Light fixtures/Wiring
- Kitchen supplies/Equipment
- Laundry/Clothing storage
- Purging/Cleaning/Organizing

Administration

- Home office supplies/Equipment
- Phones/Computers/Software/Internet
- Filing/Records/Data storage

Financial

- Bills/Banks/Investments/Loans
- Taxes/Budget/Insurance/Mortgage
- Bookkeeping/Accountants

Health

- Doctors/Dentist/Optometrist/Specialists
- Checkups
- Diet/Food/Exercise

Personal Development

- Classes/Seminars/Education
- Coaching/Counseling
- Creative expressions (art, writing, etc.)

Leisure

- Books/Music/Video
- Places to visit/People to visit
- Web browsing/Photography
- Sports equipment/Hobbies

Transportation

- Motor vehicles/Bicycles
- Maintenance/Repair
- Commuting/Tickets/Reservations

Clothes

- Professional/Casual/Sports/Formal
- Accessories/Luggage
- Repairs/Tailoring

Pets

- Health/Training/Supplies

Errands/Shopping

- Hardware store/Pharmacy/Bank/Cleaners
- Groceries/Gifts/Stationery/Malls

Community

- Neighborhood/Neighbors
- Service work/Schools/Civic involvement
- Voting

Waiting For…

- Product orders/Repairs
- Reimbursements/Loaned items
- RSVPs/Information
