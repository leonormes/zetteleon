---
captured: "2026-03-07T16:51:47+00:00 2026-03-07T16:51:47+00:00"
created: 2026-03-07T16:51:49+00:00
modified: 2026-03-14T11:10:46+00:00
source: "https://claude.ai/chat/773d43db-8b46-42b5-b430-a870bcd4723c"
status: "processing"
tags: ["input", 1, 1/2, 2]
title: HEAD AWS VPC peering and DNS resolver configuration
type: "head"
---

## Raw Output / Content

Help me complete these steps in the aws portal. I have to do the things marked CODISC: RES: VPC -> Route tables -> Edit Route table "eoe-sde-re-{env}-rt-res" Add route 10.65.6.0/23 (or specified FITFILE CIDRs) Get subnet CIDRs for eoe-sde-re-{env}-sub-res-{a,b} from RES account CODISC: VPC -> Route tables -> Edit Edit routes: eoe-sde-codisc-private-Eks\_az\_2-eu-west-2b (2a later?) NOTE: this route table is also managed by Terraform Subnet CIDR -> Peering connection, items: dev - 10.64.11.0/25 dev - 10.64.11.128/25 tst - 10.64.14.0/25 tst - 10.64.14.128/25 prd - 10.64.48.0/22 prd - 10.64.52.0/22 CODISC: VPC -> Security -> Security Groups -> Create (edit if adding env) Name: codisc-from-sde-multi (as can only have one to link to VPC) Inbound: HTTPS & DNS (UDP) for each RES subnet CIDR range (eu-west-2a/b for each env) Outbound: IPv4, all traffic, 0.0.0.0/0 CODISC: Route53 -> Resolver -> Inbound Endpoints (if not created) Name: SDE to CODISC VPC: eoe-sde-codisc Security group: codisc-from-sde-multi Endpoint type: IPv4 Protocols: Do53 IP addresses: eu-west-2a/b subnets for CODISC deployment RES: Security group to attach to Outbound endpoint: Name: res-to-codisc Outbound rules: HTTPS -> 10.65.6.0/23 DNS (UDP) -> 10.65.0.0/20 RES: Route 53 -> Resolver -> Outbound endpoint -> Create Name: eoe-sde-codisc VPC in the Region: eoe-sde-re-{env}-vpc-res Security group: res-to-codisc Endpoint type: IPv4 Protocols: Do53 IP addresses 1/2: eu-west-2a/b, eoe-sde-re-{env}-sub-res-a/b RES: Route 53 -> Resolver -> Rules -> Create Name: eoe-sde-dev-to-codisc Rule type: Forward Domain name: fitfile.net VCPs: eoe-sde-re-{env}-vpc-res Outbound endpoint: eoe-sde-codisc Targets: 10.65.5.106 & 10.65.7.33, port 53

---

Right, Leon—here are your three CODISC tasks broken into portal-clickable micro-steps. I've stripped out the RES steps entirely so you can focus.

---

## CODISC Task 1: Route Table—Add Peering Routes

Where: VPC → Route Tables

1. Open the VPC console in `eu-west-2`
2. Click Route tables in the left nav
3. Search for `eoe-sde-codisc-private-Eks_az_2-eu-west-2b`
4. Select it → Routes tab → Edit routes
5. Add these 6 routes, each pointing to the VPC Peering Connection as the target:

| CIDR | Env |
| --- | --- |
| `10.64.11.0/25` | dev |
| `10.64.11.128/25` | dev |
| `10.64.14.0/25` | tst |
| `10.64.14.128/25` | tst |
| `10.64.48.0/22` | prd |
| `10.64.52.0/22` | prd |

1. For each row: Add route → paste CIDR → Target dropdown → Peering Connection → select the relevant peering connection
2. Click Save changes

> ⚠️ Your note says this route table is also Terraform-managed. These manual additions will drift. You'll want to backport them into your Terraform config after validation, or they'll get wiped on the next apply.

---

## CODISC Task 2: Security Group—codisc-from-sde-multi

Where: VPC → Security Groups

If creating new:

1. Click Security Groups → Create security group
2. Name:`codisc-from-sde-multi`
3. Description: something like `Allow HTTPS and DNS from SDE RES subnets`
4. VPC: select `eoe-sde-codisc`

If the SG already exists (adding a new env): find it and click Edit inbound rules.

Inbound rules—for each RES subnet CIDR (the 2a and 2b subnet for each env), add two rules:

| Type | Protocol/Port | Source (CIDR) | Note |
| --- | --- | --- | --- |
| HTTPS | TCP / 443 | `{env}-sub-res-a CIDR` | One per env per AZ |
| DNS (UDP) | UDP / 53 | `{env}-sub-res-a CIDR` | One per env per AZ |
| HTTPS | TCP / 443 | `{env}-sub-res-b CIDR` |  |
| DNS (UDP) | UDP / 53 | `{env}-sub-res-b CIDR` |  |

That's 4 rules per environment × 3 environments = 12 inbound rules (assuming dev, tst, prd each have 2a and 2b subnets).

> You need the actual subnet CIDRs from the RES account for `eoe-sde-re-{env}-sub-res-a` and `eoe-sde-re-{env}-sub-res-b`. These come from the RES step you've marked—grab those first.

Outbound rule:

1. Single rule: All traffic → `0.0.0.0/0`
2. Click Create security group (or Save rules if editing)

---

## CODISC Task 3: Route53 Resolver Inbound Endpoint

Where: Route 53 → Resolver → Inbound endpoints

1. Open Route 53 console
2. Left nav → Resolver → Inbound endpoints
3. Check if one already exists—if yes, skip this task
4. If not: Create inbound endpoint
5. Name:`SDE to CODISC`
6. VPC:`eoe-sde-codisc`
7. Security group:`codisc-from-sde-multi` (the one you just created)
8. Endpoint type: IPv4
9. Protocols: Do53
10. IP address 1: select eu-west-2a subnet from the CODISC deployment, leave IP as auto-assign (or specify if you have one)
11. IP address 2: select eu-west-2b subnet from the CODISC deployment
12. Click Submit

> 📝 Once created, note down the two resolver IP addresses assigned—those are the `10.65.5.106` and `10.65.7.33` values referenced in your RES forwarding rule targets. If they don't match, update the RES rule targets accordingly.

---

### Suggested order of Attack

1. Get the RES subnet CIDRs first (you need them for Task 2)
2. Task 2—Create the Security Group (Task 3 depends on it)
3. Task 3—Create the Inbound Endpoint (needs the SG)
4. Task 1—Route table (independent, but do last so you can validate connectivity end-to-end)

What's your first blocker—do you have the RES subnet CIDRs to hand?

---

There was an error editing routes. All changes have been reverted. Details \* Creating a route route table rtb-0c3588944a5ce5db3 and network gateway pcx-0bad62f5b3944d3fd belong to different networks aws ec2 describe-vpc-peering-connections \\ --region eu-west-2 \\ --query "VpcPeeringConnections\[\*\].{ID:VpcPeeringConnectionId, Status:Status.Code, Requester:RequesterVpcInfo.VpcId, Accepter:AccepterVpcInfo.VpcId}" \\ --output table --------------------------------------------------------------------------------------- | DescribeVpcPeeringConnections | +-----------------------+-------------------------+-------------------------+---------+ | Accepter | ID | Requester | Status | +-----------------------+-------------------------+-------------------------+---------+ | vpc-04df2a335adf1ed10| pcx-0bad62f5b3944d3fd | vpc-0d6d00e165c25ee24 | active | | vpc-0aabc42188b2162bf| pcx-04ddc53b9ff3e005f | vpc-04add8e5b1b8156c2 | active | +-----------------------+-------------------------+-------------------------+---------+ The test vpc we are configuring is vpc-04df2a335adf1ed10

---

The error is clear: the route table isn't in a VPC that's part of that peering connection.

Quick diagnosis: You need to confirm which VPC the route table `rtb-0c3588944a5ce5db3` actually belongs to.

### Micro-step Right now

In the VPC console → Route Tables → select `rtb-0c3588944a5ce5db3` → look at the Details tab → note the VPC field.

Two possibilities:

1. Route table is in `vpc-04df2a335adf1ed10` (your CODISC VPC) → then `pcx-0bad62f5b3944d3fd` _should_ work since that VPC is the accepter. Something else is off—double-check you selected the right peering connection from the dropdown.
2. Route table is in a different VPC (e.g. `vpc-0aabc42188b2162bf` or `vpc-04add8e5b1b8156c2`) → you need the _other_ peering connection `pcx-04ddc53b9ff3e005f`, or you're editing the wrong route table entirely.

Given the route table name includes `codisc`, my hunch is it might actually sit in a secondary/EKS-managed VPC that's peered differently—EKS sometimes creates its own VPC for pod networking.

What VPC ID does the route table show?

---

The instructions they gave us seem a bit confused. Here are all the messages about it yes, only the last 3 steps were already set so didn't create Great, so hopefully the firewall update will be the last step (sid collision stopped the deploy) sure Looks like there is more to do here - the firewall update doesn't help. Stil could not resolve host and `dig` can't get any details of a route. One for tomorrow though Will revisit the steps Need to work in tandem with someone at FITFILE Should be noted that we need to separate out dev/tst/stg/prd - there is only a prd and tst stack for FITFILE Prd shouldn't be accessible anywhere other than RES-PRD, technically Test can be in all other RES networks but getting it working on TST is the priority Hi Keiran Raine | Health Innovation East, what do you need from the FITFILE team to assist with this? Easwaran Chandrasekaran | Health Innovation East have you looked at this today? Oliver Rushton the main thing is to check what the VPC route table for the test stack points to the values indicated against CODISC in the block above - and check that there isn't a collision from the prod stack. We only need the TST & PRD sets on the peering between accounts, but DEV,TST,STG could all route app.eoe-test-codisc. Keiran Raine | Health Innovation East Easwaran Chandrasekaran | Health Innovation East have you looked at this today? Oliver Rushton the main thing is to check what the VPC route table for the test stack points to the values indicated against CODISC in the block above - and check that there isn't a collision from the prod stack. W… Leon Ormes could you have a look at this please? l will check and get back on the route tables Peering Connection Setup: Requestor: vpc-0d6d00e165c25ee24 Acceptor: vpc-04df2a335adf1ed10 / eoe-test-codisc (10.66.0.0/20) From RES - tst - route table -- There is a route to 10.66.0.0/20 Security Group: res-to-codisc: Outbound rules: 10.65.6.0/23; 10.65.0.0/20 (current setup) Should this security group has the outbound to 10.66.0.0/23(HTTPS); 10.66.0.0/20 DNS (UDP)? Yes the 10.65 ranges are for Prod CODISC. The test uses 10.66.0.0/20 Updated will test and get back On the VPC resolver rules for domain fitfile.net currently I have target IPs as 10.65.5.106; 10.65.7.33 port:53 what should be the updated for TST DNS IPs Hi Easwaran, just looking at the different in the VPC resolver setup between our prod VPC and the new test VPC, we can see there is no configured input endpoints for the test VPC. The IPs you've listed in your last message are the ones we see as configured inbound endpoints for the prod VPC. As it's been a while since the last deployment, I cannot remember whether FITFILE need to set this up, or whether this is something that you would set up? There is also no DNS Firewall rule group configured on the VPC resolver for vpc-0aabc42188b2162bf I believe everything we did is in that plain text panel above - it scrolls, anything indented by CODISC has to be done by FITFILE. At one time our TST pointed to the production stack, it was promoted up and we dropped the peering connections from the other accounts. Hi Keiran, we understand now. We will complete those CODISC actions and get back to you when complete. Thanks Where is the fitfile.net domain hosted, this last step I believe should be from RES but the target should be set for tst domain: RES: Route 53 -> Resolver -> Rules -> Create   Name: eoe-sde-dev-to-codisc   Rule type: Forward   Domain name: fitfile.net   VCPs: eoe-sde-re-{env}-vpc-res   Outbound endpoint: eoe-sde-codisc   Targets: 10.65.5.106 & 10.65.7.33, port 53

---

Right, this thread clears up a lot. The original instructions were written against the prod stack and haven't been properly adapted for test. Here's what I've extracted:

---

## Key Revelation: Two Different CIDR Ranges

|  | Prod CODISC | Test CODISC |
| --- | --- | --- |
| VPC | `vpc-0aabc42188b2162bf` | `vpc-04df2a335adf1ed10` |
| CIDR | `10.65.0.0/20` | `10.66.0.0/20` |
| Peering | `pcx-04ddc53b9ff3e005f` | `pcx-0bad62f5b3944d3fd` |

The original step sheet has `10.65.x.x` CIDRs baked in everywhere—those are prod. Your test environment is `10.66.0.0/20`.

---

## Your Route Table Error—Explained

The route table `eoe-sde-codisc-private-Eks_az_2-eu-west-2b` likely lives inside an EKS-managed VPC that's separate from `vpc-04df2a335adf1ed10`. EKS frequently creates its own VPC for pod networking. The peering connection `pcx-0bad62f5b3944d3fd` only connects the RES and the main CODISC VPCs—not the EKS VPC.

Immediate check: Go to VPC → Route Tables → select that route table → Details tab → note the VPC ID. If it's _not_ `vpc-04df2a335adf1ed10`, that confirms it.

You may need to either:

- Find the correct route table within `vpc-04df2a335adf1ed10`, or
- Ask FITFILE whether there's additional peering needed for the EKS VPC

---

## Corrected CODISC Tasks for Test

### Task 1: Route Table

The CIDRs to add should be the RES-TST subnet CIDRs (not dev/prd). From your original list, that's:

| CIDR | Env |
| --- | --- |
| `10.64.14.0/25` | tst |
| `10.64.14.128/25` | tst |

Only these two for now—Keiran confirmed getting it working on TST is the priority.

But first you need to find the right route table in the correct VPC.

### Task 2: Security Group Codisc-from-sde-multi

Inbound rules should reference the RES-TST subnet CIDRs (same two above), with HTTPS (443/TCP) and DNS (53/UDP) for each.

### Task 3: Route53 Inbound Endpoint

Same as before, but the IPs it assigns will be in the `10.66.x.x` range, not `10.65.x.x`. Once created, you need to tell Keiran/RES team those IPs so they can update their forwarding rule targets.

### Task 4 (Keiran's Question at the end)

The resolver rule targets `10.65.5.106` & `10.65.7.33` are the prod inbound endpoint IPs. For test, Keiran needs the new IPs from your Task 3. This is an RES-side task but they're blocked on you completing Task 3 first.

---

## Your next Physical Action

Check the VPC ID on that route table—that'll tell us whether you're editing the wrong route table or need to escalate the EKS VPC question to FITFILE.

---

These are the routetables

---

There's the problem. Look at the VPC column:

| Route Table | VPC |
| --- | --- |
| `eoe-sde-codisc-private-Eks_az_2-eu-west-2b` (selected) | `vpc-0aabc42188b2162bf` |
| `eoe-test-codisc-private-Eks_az_2-eu-west-2b` | `vpc-04df2a335adf1ed10` |

You were editing the prod route table. The original instructions used `eoe-sde-codisc` naming, which is the prod stack.

## The Fix

You need the test equivalent, which is right there in your list:

> `eoe-test-codisc-private-Eks_az_2-eu-west-2b` `rtb-0e65c7e4b158905f9` VPC: `vpc-04df2a335adf1ed10 | eoe-test-codisc`

### Next Physical Action

1. Deselect the current route table
2. Select `eoe-test-codisc-private-Eks_az_2-eu-west-2b`
3. Routes tab → Edit routes
4. Add the TST CIDRs pointing to peering connection `pcx-0bad62f5b3944d3fd`:
	- `10.64.14.0/25`
	- `10.64.14.128/25`

This should work now because the route table and peering connection are both associated with `vpc-04df2a335adf1ed10`.

---

looks like they were already correct

---

That's already set up. Those two TST peering routes are spot on. Hit Cancel—nothing to change here.

Task 1: ✅ Done (already configured)

### On to Task 2: Security Group

VPC → Security Groups → search for `codisc-from-sde-multi`

Check if it already exists in `vpc-04df2a335adf1ed10` (eoe-test-codisc). Given the routes were already there, there's a decent chance the security group might be too.

---

no

---

That one's in `vpc-0aabc42188b2162bf`—prod again. You need to create one for test.

### Create Security Group

1. Click Create security group
2. Name tag:`codisc-from-sde-multi` (or consider `test-codisc-from-sde-multi` to avoid confusion with the prod one)
3. Description:`Allow HTTPS and DNS from SDE-TST subnets`
4. VPC:`vpc-04df2a335adf1ed10 | eoe-test-codisc`

Inbound rules—you need the RES-TST subnet CIDRs for `eoe-sde-re-tst-sub-res-a` and `eoe-sde-re-tst-sub-res-b`. Do you have those to hand? They're the `10.64.14.0/25` and `10.64.14.128/25` from your original list.

If so, add 4 inbound rules:

| Type | Port | Source |
| --- | --- | --- |
| HTTPS | 443 | `10.64.14.0/25` |
| DNS (UDP) | 53 | `10.64.14.0/25` |
| HTTPS | 443 | `10.64.14.128/25` |
| DNS (UDP) | 53 | `10.64.14.128/25` |

Outbound rule:

- All traffic → `0.0.0.0/0`
1. Click Create security group

---

this step is done. Is the all traffic sg outbound rule dangerous?

---

Task 2: ✅ Done—looks perfect.

On the outbound rule: no, it's fine here. Outbound "all traffic 0.0.0.0/0" is standard practice for security groups that protect inbound endpoints like DNS resolvers. The security posture is controlled by the inbound rules (which you've locked down to specific CIDRs and ports). The outbound rule just allows the resolver to send responses back—restricting it could break DNS replies taking unexpected return paths.

The prod SG has the same pattern. You're good.

---

### On to Task 3: Route53 Inbound Endpoint

1. Open Route 53 console
2. Left nav → Resolver → Inbound endpoints
3. Click Create inbound endpoint
4. Name:`SDE to test CODISC` (differentiate from the prod one)
5. VPC:`vpc-04df2a335adf1ed10 | eoe-test-codisc`
6. Security group:`sg-075f76604d63eace1 | test-codisc-from-sde-multi`
7. Endpoint type: IPv4
8. Protocols: Do53
9. IP address 1: pick an eu-west-2a subnet from the test CODISC VPC
10. IP address 2: pick an eu-west-2b subnet
11. Leave IPs as auto-assign
12. Click Submit

Once created, note the two assigned IP addresses—Keiran's team needs those to configure their RES-side forwarding rule targets (replacing the `10.65.x.x` prod IPs).

---

So where he is asking about targets should that be the 2 ips we now have in the endpoints RES: Route 53 -> Resolver -> Rules -> Create  Name: eoe-sde-dev-to-codisc  Rule type: Forward  Domain name: fitfile.net  VCPs: eoe-sde-re-{env}-vpc-res  Outbound endpoint: eoe-sde-codisc  Targets: 10.65.5.106 & 10.65.7.33, port 53

---

Task 3: ✅ Done

And yes, exactly. The targets in that RES forwarding rule need to be your new test IPs:

| Prod (original instructions) | Test (what Keiran's team should use) |
| --- | --- |
| `10.65.5.106` | `10.66.8.199` (eu-west-2a) |
| `10.65.7.33` | `10.66.7.215` (eu-west-2b) |

That's an RES-side task, so send Keiran/Easwaran those two IPs and let them know all three CODISC tasks are complete. Their remaining steps are:

1. Update the RES security group `res-to-codisc` outbound rules to use `10.66.x.x` ranges (not the `10.65.x.x` prod ranges—Easwaran flagged this earlier in the thread)
2. Create the Route53 forwarding rule with targets `10.66.8.199` and `10.66.7.215` on port 53
3. DNS Firewall rule group on the test VPC (Oliver mentioned this was missing)

All three CODISC tasks are done on your side. Nice one. 🎯

---

create the jira ticket details so I can add the work to jira

---

No need for a docx here—I'll create a clean markdown you can copy from.

---

my routing has broken for the prod frontend although I can dig dig app.eoe-sde-codisc.privatelink.fitfile.net; <<>> DiG 9.18.39-0ubuntu0.24.04.2-Ubuntu <<>> app.eoe-sde-codisc.privatelink.fitfile.net;; global options: +cmd;; Got answer:;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 7800;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1;; OPT PSEUDOSECTION:; EDNS: version: 0, flags:; udp: 65494;; QUESTION SECTION:;app.eoe-sde-codisc.privatelink.fitfile.net. IN A;; ANSWER SECTION: app.eoe-sde-codisc.privatelink.fitfile.net. 60 IN A 10.65.7.184 app.eoe-sde-codisc.privatelink.fitfile.net. 60 IN A 10.65.4.210;; Query time: 2 msec;; SERVER: 127.0.0.53#53(127.0.0.53) (UDP);; WHEN: Thu Feb 26 16:00:15 UTC 2026;; MSG SIZE rcvd: 103 The browser times out

---

DNS works but HTTPS times out—so the issue is in the network path, not name resolution. Let's narrow it down quickly.

Where are you running this from? I'm assuming a jumpbox/bastion in a RES VPC.

### Immediate diagnostic—run These

If `nc` times out too, it's a routing or security group issue between your box and the prod CODISC IPs. If `nc` connects but curl hangs, it's TLS/application-level.

### Did Today's Work Break Prod?

Almost certainly no—everything you touched was in the test VPC (`vpc-04df2a335adf1ed10`):

- Route table edit errored and reverted
- Security group was created in the test VPC
- Resolver endpoint was created in the test VPC

None of that touches the prod VPC (`vpc-0aabc42188b2162bf`). This is likely either coincidental timing or was already broken. Worth checking—was prod working before you started today?

---

\# Can you actually reach the port? nc -zv 10.65.7.184 443 -w 5 nc -zv 10.65.4.210 443 -w 5 # Does curl show where it hangs? curl -vk --connect-timeout 10 [https://app.eoe-sde-codisc.privatelink.fitfile.net](https://app.eoe-sde-codisc.privatelink.fitfile.net/) zsh: no matches found: port? nc: connect to 10.65.7.184 port 443 (tcp) timed out: Operation now in progress nc: connect to 10.65.4.210 port 443 (tcp) timed out: Operation now in progress zsh: no matches found: hangs? \* Host app.eoe-sde-codisc.privatelink.fitfile.net:443 was resolved. \* IPv6: (none) \* IPv4: 127.0.0.1 \* Trying 127.0.0.1:443… \* connect to 127.0.0.1 port 443 from 127.0.0.1 port 56530 failed: Connection refused \* Failed to connect to app.eoe-sde-codisc.privatelink.fitfile.net port 443 after 0 ms: Couldn't connect to server \* Closing connection curl: (7) Failed to connect to app.eoe-sde-codisc.privatelink.fitfile.net port 443 after 0 ms: Couldn't connect to server ip-10-65-2-8%

---

Two separate issues here:

### Issue 1: Curl Resolves to 127.0.0.1 (not Dig's result)

`dig` queries DNS directly, but `curl` (and browsers) use the system resolver which checks `/etc/hosts` first. Something is overriding the DNS response.

If there's a `127.0.0.1` entry in `/etc/hosts`, that's your browser timeout explained.

### Issue 2: Nc to the Prod IPs times out

Your prompt shows `ip-10-65-2-8`—you're on a box inside the prod CODISC VPC (`10.65.0.0/20`). So this isn't a peering/routing issue, it's traffic within the same VPC timing out.

Check these in order:

1. `/etc/hosts`—most likely the browser problem
2. Security groups on whatever sits behind `10.65.7.184` / `10.65.4.210`—explains the `nc` timeout

Start with the `grep`—that's the quickest win.

---

\# Check for a hosts file override grep -i fitfile /etc/hosts # Check what the system resolver actually returns getent hosts app.eoe-sde-codisc.privatelink.fitfile.net zsh: command not found: # 127.0.0.1 app.eoe-sde-codisc.privatelink.fitfile.net zsh: command not found: # 127.0.0.1 app.eoe-sde-codisc.privatelink.fitfile.net ip-10-65-2-8%

---

There's your browser problem. Someone added a hosts file entry pointing the domain to localhost.

### Fix

Then verify:

Should now return `10.65.7.184` / `10.65.4.210` instead of `127.0.0.1`.

The `nc` timeout to the actual IPs is still a concern though—once the hosts fix is in, try `curl` again. If it still times out, we'll need to look at the security groups on the target endpoints.

---

how can I check the aws config

---

That'll show you the account ID, IAM role/user, and active region/profile.

---

\# Who am I and what account? aws sts get-caller-identity # What region am I defaulting to? aws configure list zsh: no matches found: account? { "UserId": "AROAR7HWXTRH3OS4DQURH:leon.ormes@fitfile.com", "Account": "135808916559", "Arn": "arn:aws:sts::135808916559:assumed-role/AWSReservedSSO\_DiscoveryEngineeringAccess\_b38ff0a73dfb5f6d/leon.ormes@fitfile.com" } zsh: no matches found: to? NAME: VALUE: TYPE: LOCATION profile: <not set>: None: None access\_key: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*BFXA: env: secret\_key: \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*PItW: env: region: eu-west-2: config-file: ~/.aws/config How can we check the routing config

---

You're in the right account (`135808916559`—the CODISC account). Let's trace the network path:

The ENI lookup is the key one—it'll tell us what's behind those IPs and which security groups are attached, so we can see if port 443 inbound is actually allowed from `10.65.2.8`.

---

Here are the outputs

---

Good news: both IPs are NLB ENIs in the same VPC—so this isn't a peering/routing problem. It's traffic within the prod CODISC VPC being blocked.

I notice there's a Firewall subnet (`eoe-sde-codisc-private-Firewall-eu-west-2a`)—this VPC likely routes traffic through AWS Network Firewall. Let's check:

The firewall route table is the most likely culprit—if the jumpbox routes local VPC traffic through the Network Firewall, a firewall rule change could explain the timeout.

---

aws ec2 describe-route-tables --region eu-west-2 \\ --route-table-ids rtb-0c1cdd9adc08a70cd \\ --query "RouteTables\[0\].Routes\[\*\].{Dest:DestinationCidrBlock,Target:GatewayId,NAT:NatGatewayId,FW:VpcEndpointId,Peer:VpcPeeringConnectionId}" \\ --output table -------------------------------------------------------------------- | DescribeRouteTables | +--------------+-------+-------+-------+---------------------------+ | Dest | FW | NAT | Peer | Target | +--------------+-------+-------+-------+---------------------------+ | 10.65.0.0/20| None | None | None | local | | 0.0.0.0/0 | None | None | None | vpce-031bfaf1e2ee877ca | +--------------+-------+-------+-------+---------------------------+ ip-10-65-2-8% aws ec2 describe-network-interfaces --region eu-west-2 \\ --filters "Name=addresses.private-ip-address,Values=10.65.7.184" \\ --query "NetworkInterfaces\[\*\].Groups\[\*\].{ID:GroupId,Name:GroupName}" \\ --output table --------------------------- |DescribeNetworkInterfaces| ip-10-65-2-8% aws ec2 describe-network-acls --region eu-west-2 \\ --filters "Name=association.subnet-id,Values=subnet-089c457b2998ff843" \\ --query "NetworkAcls\[\*\].{ID:NetworkAclId,Entries:Entries\[\*\].{Rule:RuleNumber,Allow:RuleAction,CIDR:CidrBlock,Port:PortRange.From,Egress:Egress}}" \\ --output table ----------------------------------------------------- | DescribeNetworkAcls | +---------------------------------------------------+ | ID | +---------------------------------------------------+ | acl-0b059cc861528dc9f | +---------------------------------------------------+ || Entries || |+-------+-------------+---------+-------+---------+| || Allow | CIDR | Egress | Port | Rule || |+-------+-------------+---------+-------+---------+| || allow| 0.0.0.0/0 | True | None | 100 || || deny | 0.0.0.0/0 | True | None | 32767 || || allow| 0.0.0.0/0 | False | None | 100 || || deny | 0.0.0.0/0 | False | None | 32767 || |+-------+-------------+---------+-------+---------+|

---

NACLs are wide open, local VPC traffic goes direct (not through the firewall), and NLBs don't have security groups attached. So the network path is clear.

This points to the NLB itself—NLBs silently drop TCP SYNs when they have no healthy targets, which looks exactly like a timeout.

Then once we have the ARN:

My bet: the targets behind the NLB are unhealthy—likely the pods or nodes have restarted or the deployment is broken. That would explain why DNS works fine but connections time out.

---

\# Get the NLB ARN from the description we saw earlier aws elbv2 describe-load-balancers --region eu-west-2 \\ --query "LoadBalancers\[?LoadBalancerName=='a09b6c067806443db8a14d79fbd6a2ac'\].{ARN:LoadBalancerArn,State:State.Code,Scheme:Scheme}" \\ --output table # If that doesn't match by name, find it by the ENI description aws elbv2 describe-load-balancers --region eu-west-2 \\ --query "LoadBalancers\[\*\].{Name:LoadBalancerName,ARN:LoadBalancerArn,State:State.Code,VPC:VpcId}" \\ --output table quote> ip-10-65-2-8% aws elbv2 describe-load-balancers --region eu-west-2 \\ --query "LoadBalancers\[?LoadBalancerName=='a09b6c067806443db8a14d79fbd6a2ac'\].{ARN:LoadBalancerArn,State:State.Code,Scheme:Scheme}" \\ --output table -------------------------------------------------------------------------------------------------------------------------------------------------- | DescribeLoadBalancers | +--------------------------------------------------------------------------------------------------------------------------+-----------+---------+ | ARN | Scheme | State | +--------------------------------------------------------------------------------------------------------------------------+-----------+---------+ | arn:aws:elasticloadbalancing:eu-west-2:135808916559:loadbalancer/net/a09b6c067806443db8a14d79fbd6a2ac/3d6a600ba7023f54 | internal | active | +--------------------------------------------------------------------------------------------------------------------------+-----------+---------+ ip-10-65-2-8% aws elbv2 describe-load-balancers --region eu-west-2 \\ --query "LoadBalancers\[\*\].{Name:LoadBalancerName,ARN:LoadBalancerArn,State:State.Code,VPC:VpcId}" \\ --output tableCopy And SaveShareAsk Copilot aws: \[ERROR\]: argument --output: Found invalid choice 'tableCopy' usage: aws \[options\] <command> <subcommand> \[<subcommand>…\] \[parameters\] To see help text, you can run: aws help aws <command> help aws <command> <subcommand> help

---

---

aws elbv2 describe-target-groups --region eu-west-2 \\ --load-balancer-arn "arn:aws:elasticloadbalancing:eu-west-2:135808916559:loadbalancer/net/a09b6c067806443db8a14d79fbd6a2ac/3d6a600ba7023f54" \\ --query "TargetGroups\[\*\].{Name:TargetGroupName,ARN:TargetGroupArn,Port:Port,Protocol:Protocol}" \\ --output table -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | DescribeTargetGroups | +--------------------------------------------------------------------------------------------------------------------+-----------------------------------+--------+------------+ | ARN | Name | Port | Protocol | +--------------------------------------------------------------------------------------------------------------------+-----------------------------------+--------+------------+ | arn:aws:elasticloadbalancing:eu-west-2:135808916559:targetgroup/k8s-ingressn-ingressn-c88724a983/bf3828527adf2bd5 | k8s-ingressn-ingressn-c88724a983 | 31139 | TCP | | arn:aws:elasticloadbalancing:eu-west-2:135808916559:targetgroup/k8s-ingressn-ingressn-cae3d9a7ff/97442ac3a7af494a | k8s-ingressn-ingressn-cae3d9a7ff | 32623 | TCP | +--------------------------------------------------------------------------------------------------------------------+-----------------------------------+--------+------------+ ip-10-65-2-8%

---

Two target groups on NodePorts. Let's check if they're healthy:

If they show `unhealthy` or `unused`—that's your answer. The NLB has nowhere to send traffic.

---

aws elbv2 describe-target-health --region eu-west-2 \\ --target-group-arn "arn:aws:elasticloadbalancing:eu-west-2:135808916559:targetgroup/k8s-ingressn-ingressn-c88724a983/bf3828527adf2bd5" \\ --query "TargetHealthDescriptions\[\*\].{IP:Target.Id,Port:Target.Port,State:TargetHealth.State,Reason:TargetHealth.Reason}" \\ --output table aws elbv2 describe-target-health --region eu-west-2 \\ --target-group-arn "arn:aws:elasticloadbalancing:eu-west-2:135808916559:targetgroup/k8s-ingressn-ingressn-cae3d9a7ff/97442ac3a7af494a" \\ --query "TargetHealthDescriptions\[\*\].{IP:Target.Id,Port:Target.Port,State:TargetHealth.State,Reason:TargetHealth.Reason}" \\ --output table ---------------------------------------------------------------------------- | DescribeTargetHealth | +----------------------+--------+-----------------------------+------------+ | IP | Port | Reason | State | +----------------------+--------+-----------------------------+------------+ | i-00776004ccc46fa33 | 31139 | None | healthy | | i-0009d024971f5a3ae | 31139 | None | healthy | | i-0672296a6bfb87a92 | 31139 | Target.FailedHealthChecks | unhealthy | | i-0cdbfe365293d168b | 31139 | None | healthy | | i-0964d2c6fd0d4f6b0 | 31139 | None | healthy | +----------------------+--------+-----------------------------+------------+ ---------------------------------------------------------------------------- | DescribeTargetHealth | +----------------------+--------+-----------------------------+------------+ | IP | Port | Reason | State | +----------------------+--------+-----------------------------+------------+ | i-00776004ccc46fa33 | 32623 | None | healthy | | i-0672296a6bfb87a92 | 32623 | Target.FailedHealthChecks | unhealthy | | i-0cdbfe365293d168b | 32623 | None | healthy | | i-0964d2c6fd0d4f6b0 | 32623 | None | healthy | | i-0009d024971f5a3ae | 32623 | None | healthy | +----------------------+--------+-----------------------------+------------+ ip-10-65-2-8%

---

One node unhealthy, but 4/5 are healthy on both target groups—the NLB should still be serving traffic fine. That's not your problem.

Let's check what the NLB is actually listening on:

If there's no listener on port 443, that explains the `nc` timeout—the NLB silently drops SYNs on ports with no listener, which looks identical to a routing/firewall issue.

Also—did you run the `/etc/hosts` fix? That's still the most likely cause of the browser timeout:

---

aws elbv2 describe-listeners --region eu-west-2 \\ --load-balancer-arn "arn:aws:elasticloadbalancing:eu-west-2:135808916559:loadbalancer/net/a09b6c067806443db8a14d79fbd6a2ac/3d6a600ba7023f54" \\ --query "Listeners\[\*\].{Port:Port,Protocol:Protocol,TargetGroup:DefaultActions\[0\].TargetGroupArn}" \\ --output table ------------------------------------------------------------------------------------------------------------------------------------------- | DescribeListeners | +------+-----------+----------------------------------------------------------------------------------------------------------------------+ | Port | Protocol | TargetGroup | +------+-----------+----------------------------------------------------------------------------------------------------------------------+ | 443 | TCP | arn:aws:elasticloadbalancing:eu-west-2:135808916559:targetgroup/k8s-ingressn-ingressn-cae3d9a7ff/97442ac3a7af494a | | 80 | TCP | arn:aws:elasticloadbalancing:eu-west-2:135808916559:targetgroup/k8s-ingressn-ingressn-c88724a983/bf3828527adf2bd5 | +------+-----------+----------------------------------------------------------------------------------------------------------------------+ ip-10-65-2-8% cat /etc/hosts 127.0.0.1 localhost # The following lines are desirable for IPv6 capable hosts::1 ip6-localhost ip6-loopback fe00::0 ip6-localnet ff00::0 ip6-mcastprefix ff02::1 ip6-allnodes ff02::2 ip6-allrouters ff02::3 ip6-allhosts

---

Hosts file is clean now, NLB is listening on 443 with healthy targets. Everything checks out infrastructure-wise.

Try again:

If `nc` still times out, this is weird territory—we'd need to check whether the jumpbox subnet routes through the Network Firewall for intra-VPC traffic. That `vpce-031bfaf1e2ee877ca` in the default route could be an AWS Network Firewall endpoint, and it might be inspecting/blocking even local VPC traffic.

---

nc -zv 10.65.7.184 443 -w 5 curl -vk --connect-timeout 10 [https://app.eoe-sde-codisc.privatelink.fitfile.net](https://app.eoe-sde-codisc.privatelink.fitfile.net/) nc: connect to 10.65.7.184 port 443 (tcp) timed out: Operation now in progress \* Host app.eoe-sde-codisc.privatelink.fitfile.net:443 was resolved. \* IPv6: (none) \* IPv4: 10.65.4.210, 10.65.7.184 \* Trying 10.65.4.210:443… \* ipv4 connect timeout after 4999ms, move on! \* Trying 10.65.7.184:443… \* ipv4 connect timeout after 4997ms, move on! \* Failed to connect to app.eoe-sde-codisc.privatelink.fitfile.net port 443 after 10002 ms: Timeout was reached \* Closing connection curl: (28) Failed to connect to app.eoe-sde-codisc.privatelink.fitfile.net port 443 after 10002 ms: Timeout was reached

---

DNS fix worked (curl now resolves correctly), but TCP is still dead. Since NLB, listeners, targets, NACLs, and routing all look fine, the prime suspect is that Network Firewall endpoint (`vpce-031bfaf1e2ee877ca`).

Even though `10.65.0.0/20 → local` should handle intra-VPC traffic, let's check if the NLB's subnets route return traffic through the firewall:

If the firewall is inspecting intra-VPC traffic, a rule change or a "sid collision" (which was mentioned in the Slack thread!) could be silently dropping the packets.

---

aws ec2 describe-route-tables --region eu-west-2 \\ --route-table-ids rtb-010658b9d1ef194c6 \\ --query "RouteTables\[0\].Routes\[\*\].{Dest:DestinationCidrBlock,Target:GatewayId,FW:VpcEndpointId,NAT:NatGatewayId}" \\ --output table ----------------------------------------------------------------------------- | DescribeRouteTables | +--------------+-------+-------------------------+--------------------------+ | Dest | FW | NAT | Target | +--------------+-------+-------------------------+--------------------------+ | 10.65.0.0/20| None | None | local | | 0.0.0.0/0 | None | nat-02c1a6d832f6683e5 | None | | None | None | None | vpce-0b384c673bc88e44f | +--------------+-------+-------------------------+--------------------------+ ip-10-65-2-8% aws ec2 describe-route-tables --region eu-west-2 \\ --route-table-ids rtb-0c3588944a5ce5db3 \\ --query "RouteTables\[0\].Routes\[\*\].{Dest:DestinationCidrBlock,Target:GatewayId,FW:VpcEndpointId,NAT:NatGatewayId}" \\ --output table ------------------------------------------------------------------------------ | DescribeRouteTables | +---------------+-------+-------------------------+--------------------------+ | Dest | FW | NAT | Target | +---------------+-------+-------------------------+--------------------------+ | 10.64.48.0/22| None | None | None | | 10.64.52.0/22| None | None | None | | 10.65.0.0/20 | None | None | local | | 0.0.0.0/0 | None | nat-02c1a6d832f6683e5 | None | | None | None | None | vpce-0b384c673bc88e44f | +---------------+-------+-------------------------+--------------------------+ ip-10-65-2-8% aws network-firewall describe-firewall --region eu-west-2 \\ --vpc-id vpc-0aabc42188b2162bf \\ --query "Firewall.{Name:FirewallName,Policy:FirewallPolicyArn}" \\ --output table usage: aws \[options\] <command> <subcommand> \[<subcommand>…\] \[parameters\] To see help text, you can run: aws help aws <command> help aws <command> <subcommand> help Unknown options: --vpc-id, vpc-0aabc42188b2162bf

---

NLB subnets route intra-VPC via `local`—firewall isn't in the path. This is puzzling.

Let me try a different angle. NLBs now support security groups, and the node security groups need to allow traffic from the jumpbox. Let's check both:

If port 80 works but 443 doesn't, it's TLS-related. If both timeout, it's likely a security group on the NLB or nodes blocking the jumpbox IP (`10.65.2.8`).

---

ip-10-65-2-8% aws elbv2 describe-load-balancers --region eu-west-2 \\ --load-balancer-arns "arn:aws:elasticloadbalancing:eu-west-2:135808916559:loadbalancer/net/a09b6c067806443db8a14d79fbd6a2ac/3d6a600ba7023f54" \\ --query "LoadBalancers\[0\].SecurityGroups" \\ --output table ip-10-65-2-8% aws ec2 describe-instances --region eu-west-2 \\ --instance-ids i-00776004ccc46fa33 \\ --query "Reservations\[0\].Instances\[0\].{SGs:SecurityGroups\[\*\].GroupId,Subnet:SubnetId,IP:PrivateIpAddress}" \\ --output table -------------------------------------------- | DescribeInstances | +-------------+----------------------------+ | IP | Subnet | +-------------+----------------------------+ | 10.65.5.32 | subnet-02b4bec3447cbbf9e | +-------------+----------------------------+ || SGs || |+----------------------------------------+| || sg-02dcb1a5bbe8844b8 || |+----------------------------------------+| ip-10-65-2-8% nc -zv 10.65.7.184 80 -w 5 nc: connect to 10.65.7.184 port 80 (tcp) timed out: Operation now in progress ip-10-65-2-8%

---

Both ports timeout. No security groups on the NLB (so it passes all traffic). The key insight: NLBs preserve the client's source IP. So the EKS nodes see traffic arriving from `10.65.2.8` on the NodePorts—and the node security group needs to allow that.

If the inbound rules only allow traffic from other EKS nodes or specific security groups (not the jumpbox subnet `10.65.2.x`), that's your timeout. The NLB forwards the packet but the node drops it because the source IP isn't permitted.

---

aws ec2 describe-security-groups --region eu-west-2 \\ --group-ids sg-02dcb1a5bbe8844b8 \\ --query "SecurityGroups\[0\].IpPermissions\[\*\].{Proto:IpProtocol,From:FromPort,To:ToPort,CIDRs:IpRanges\[\*\].CidrIp,SGs:UserIdGroupPairs\[\*\].GroupId}" \\ --output json \[{ "Proto": "tcp", "From": 32623, "To": 32623, "CIDRs": \["217.38.237.128/26" \], "SGs": \[\] }, { "Proto": "tcp", "From": 32082, "To": 32082, "CIDRs": \[\], "SGs": \["sg-06a3ef4dc97a131f1" \] }, { "Proto": "-1", "From": null, "To": null, "CIDRs": \[\], "SGs": \["sg-02dcb1a5bbe8844b8", "sg-06a3ef4dc97a131f1" \] }, { "Proto": "tcp", "From": 31139, "To": 31139, "CIDRs": \["217.38.237.128/26" \], "SGs": \[\] }, { "Proto": "tcp", "From": 32080, "To": 32080, "CIDRs": \["10.65.2.8/32" \], "SGs": \["sg-06a3ef4dc97a131f1" \] }, { "Proto": "icmp", "From": 3, "To": 4, "CIDRs": \["0.0.0.0/0" \], "SGs": \[\] }, { "Proto": "tcp", "From": 31835, "To": 31835, "CIDRs": \["10.65.4.0/23", "10.65.6.0/23" \], "SGs": \[\] }, { "Proto": "tcp", "From": 443, "To": 443, "CIDRs": \[\], "SGs": \["sg-02dcb1a5bbe8844b8" \] } \]

---

Found it. The NodePorts `31139` and `32623` only allow inbound from `217.38.237.128/26`—that's an external CIDR (office/VPN range?). Your jumpbox `10.65.2.8` isn't permitted.

| NodePort | Allowed Sources | Your IP |
| --- | --- | --- |
| 31139 (HTTP) | `217.38.237.128/26` | ❌ `10.65.2.8` |
| 32623 (HTTPS) | `217.38.237.128/26` | ❌ `10.65.2.8` |
| 32080 | `10.65.2.8/32` ✅ | ✅ |

Interestingly, `10.65.2.8` is explicitly allowed on port `32080`—so someone's set up jumpbox access on a different NodePort before, but not for the NLB-fronted ones.

### The Question Is: Was This Ever Working from the Jumpbox?

That `/etc/hosts` entry pointing to `127.0.0.1` suggests the previous approach may have been a kubectl port-forward or SSH tunnel rather than hitting the NLB directly. That would explain why it "broke"—the port-forward session ended.

### Two Options

1. If you just need to test from the jumpbox: restart the port-forward to the ingress controller or the app service directly
2. If the jumpbox should route through the NLB: add `10.65.2.0/24` (or `/32`) to the SG on ports 31139 and 32623—but check with Keiran first since this is the prod node SG and it's likely Terraform-managed

Which approach makes sense for your use case?

---

the jumpbox should route through the NLB

---

Right. You need to add the jumpbox to the node SG on both NodePorts. Since this is the prod node SG and likely Terraform-managed, I'd recommend a narrow `/32` rule like the existing `32080` entry.

### Steps

1. VPC → Security Groups → `sg-02dcb1a5bbe8844b8`
2. Inbound rules tab → Edit inbound rules
3. Add two rules:

| Type | Port | Source | Description |
| --- | --- | --- | --- |
| Custom TCP | 31139 | `10.65.2.8/32` | Jumpbox HTTP via NLB |
| Custom TCP | 32623 | `10.65.2.8/32` | Jumpbox HTTPS via NLB |

1. Save rules

Then test:

> ⚠️ Terraform drift warning: This is the same situation as the route tables—backport these rules or they'll get wiped on the next apply. Also worth flagging to Keiran that the existing `217.38.237.128/26` rule only covers external access, not internal VPC access to the NLB.

---

why are those specific ports used? Where can I find the config that sets

---

Those are Kubernetes NodePorts—when you create a `Service` of type `LoadBalancer` or `NodePort`, Kubernetes assigns (or you specify) a port in the 30000–32767 range on every node. The NLB then forwards traffic to those NodePorts.

The chain is:

### Where the Config Lives

The NodePort assignment is on the Kubernetes Service for the ingress controller. Since the NLB target groups have `ingressn` in the name, it's likely an nginx ingress controller.

If you have `kubectl` access to the prod cluster:

You'll see something like:

The security group rules are likely managed by the AWS Load Balancer Controller running in the cluster—it automatically reconciles NLB config and SG rules based on Service annotations. That's why the SG rules are so specific. If it's reconciling, your manual SG addition might get reverted by the controller too, not just Terraform.

---

kubectl get svc -A | grep -i ingress ingress-nginx ingress-nginx-controller LoadBalancer 172.20.48.18 a09b6c067806443db8a14d79fbd6a2ac-3d6a600ba7023f54.elb.eu-west-2.amazonaws.com 80:31139/TCP,443:32623/TCP 303d ingress-nginx ingress-nginx-controller-admission ClusterIP 172.20.30.12 <none> 443/TCP 303d

---

That confirms it—`80:31139` and `443:32623` match exactly.

Check the annotations to see how the NLB and SG rules are managed:

Look for annotations like:

- `service.beta.kubernetes.io/aws-load-balancer-security-groups`—specifies which SG to use
- `service.beta.kubernetes.io/aws-load-balancer-additional-resource-tags`—tagging
- `service.beta.kubernetes.io/aws-load-balancer-scheme`—internal/internet-facing
- `service.beta.kubernetes.io/aws-load-balancer-target-group-attributes`—target group config

If the AWS Load Balancer Controller is managing the SG, your manual rule addition will get reverted. The proper fix would be adding the jumpbox CIDR to the annotation or to a Helm values file for the ingress-nginx chart.

Did you add the SG rules yet? Worth testing first, then figuring out the permanent fix.

---

kubectl get svc -n ingress-nginx ingress-nginx-controller -o yaml | grep -A 30 annotations annotations: meta.helm.sh/release-name: ingress-nginx meta.helm.sh/release-namespace: ingress-nginx service.beta.kubernetes.io/aws-load-balancer-backend-protocol: tcp service.beta.kubernetes.io/aws-load-balancer-cross-zone-load-balancing-enabled: "true" service.beta.kubernetes.io/aws-load-balancer-internal: "true" service.beta.kubernetes.io/aws-load-balancer-private-ipv4-addresses: 10.65.4.6,10.65.6.6 service.beta.kubernetes.io/aws-load-balancer-scheme: internal service.beta.kubernetes.io/aws-load-balancer-type: nlb creationTimestamp: "2025-04-29T14:01:06Z" finalizers: - service.kubernetes.io/load-balancer-cleanup labels: app.kubernetes.io/component: controller app.kubernetes.io/instance: ingress-nginx app.kubernetes.io/managed-by: Helm app.kubernetes.io/name: ingress-nginx app.kubernetes.io/part-of: ingress-nginx app.kubernetes.io/version: 1.12.1 helm.sh/chart: ingress-nginx-4.12.1 name: ingress-nginx-controller namespace: ingress-nginx resourceVersion: "133573787" uid: 09b6c067-8064-43db-8a14-d79fbd6a2ac7 spec: allocateLoadBalancerNodePorts: true clusterIP: 172.20.48.18 clusterIPs: - 172.20.48.18 externalTrafficPolicy: Local healthCheckNodePort: 31835

---

Good news—this uses the in-tree cloud provider (`nlb`), not the AWS Load Balancer Controller (`nlb-ip`). The in-tree provider doesn't actively reconcile security group rules, so your manual SG addition should stick. Only Terraform would revert it.

Also worth noting: the annotation specifies `private-ipv4-addresses: 10.65.4.6,10.65.6.6` but the actual NLB ENIs are on `10.65.4.210` and `10.65.7.184`. Those don't match—the NLB may have been recreated at some point. Not urgent but worth a mental note.

### Next Action

Go ahead and add those two SG rules:

1. VPC → Security Groups → `sg-02dcb1a5bbe8844b8`
2. Edit inbound rules → add:
	- Custom TCP / `31139` / `10.65.2.8/32`
	- Custom TCP / `32623` / `10.65.2.8/32`
3. Save

Then test:

---

the res prod can not reach our cluster now. I need to add 10.64.48.0/21, 10.64.40.128/26 to the sg to allow that traffic in. what are my instructions for the aws portal

---

Same security group, same process:

1. VPC → Security Groups → `sg-02dcb1a5bbe8844b8`
2. Inbound rules tab → Edit inbound rules
3. Add four rules:

| Type | Port | Source | Description |
| --- | --- | --- | --- |
| Custom TCP | 31139 | `10.64.48.0/21` | RES-PRD HTTP via NLB |
| Custom TCP | 32623 | `10.64.48.0/21` | RES-PRD HTTPS via NLB |
| Custom TCP | 31139 | `10.64.40.128/26` | RES-PRD HTTP via NLB |
| Custom TCP | 32623 | `10.64.40.128/26` | RES-PRD HTTPS via NLB |

1. Save rules

> Same Terraform drift caveat applies—add these to the backport list along with the jumpbox rules.
