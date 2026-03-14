---
captured: "2026-02-26T09:28:59+00:00 2026-02-26T09:28:59+00:00"
created: 2026-02-26T09:29:02+00:00
modified: 2026-02-27T09:19:57+00:00
source: "https://gemini.google.com/app/447d4b0de6d73891"
status: "processing"
tags: ["input"]
title: HEAD You said review the azure portal docs. httpsazu...
type: "head"
---

## Raw Output / Content

review the azure portal docs. <https://azure.microsoft.com/en-gb/get-started/azure-portal/cloud-shell/?ef>\_id=\_k\_Cj0KCQiAtfXMBhDzARIsAJ0jp3DAX73iZQK4iNvz9j47yycIt-VsloQXEbapvtQOuNaIB1pkr5DpQqMaAhv1EALw\_wcB\_k\_&OCID=AIDcmm3bvqzxp1\_SEM\_\_k\_Cj0KCQiAtfXMBhDzARIsAJ0jp3DAX73iZQK4iNvz9j47yycIt-VsloQXEbapvtQOuNaIB1pkr5DpQqMaAhv1EALw\_wcB\_k\_&gad\_source=1&gad\_campaignid=23487475560&gbraid=0AAAAADcJh\_to5wdKvwYUYHj8GtVDaouH\_&gclid=Cj0KCQiAtfXMBhDzARIsAJ0jp3DAX73iZQK4iNvz9j47yycIt-VsloQXEbapvtQOuNaIB1pkr5DpQqMaAhv1EALw\_wcB

I am trying to see if we can use it for work. I currently have a bastion and jumpbox setup. From my machine I can ssh to the jumpbox in the private network. It requires its own subnet with the public IP access for the bastion. We want to minimise subnets. Does using this portal terminal avoid having to setup bastion and jumpbox

---

Yes, you can use the Azure Cloud Shell to bypass the need for a Bastion host and a jumpbox, but it will not help you minimise your subnets. In fact, it will likely increase them.

By default, the Azure Cloud Shell runs in a Microsoft-managed network and cannot access resources in your private virtual network. To allow it to SSH directly into your private virtual machines, you must configure a feature called Virtual Network Isolation (or VNet Integration).

While this setup entirely removes the need for your Bastion and jumpbox, the architecture required to securely bridge the browser-based terminal into your private network requires three dedicated subnets:

1. Container Subnet: To host the Azure Container Instances that run your ephemeral shell sessions.
2. Relay Subnet: To host the Azure Relay service, which handles the secure communication between your web browser and the isolated container.
3. Storage Subnet: To host the private endpoint connecting the Azure Storage account that persists your Cloud Shell files.

Currently, your Azure Bastion setup requires exactly one dedicated subnet (`AzureBastionSubnet`), and your jumpbox can either sit in its own subnet or share an existing management subnet (totalling one or two subnets). Migrating to an isolated Cloud Shell requires provisioning three dedicated subnets, which defeats your primary architectural goal of reducing subnet sprawl.

Additionally, it is worth noting that VNet-isolated Cloud Shell sessions generally take longer to start up than standard sessions and will introduce new costs for the required Azure Relay service. For your specific goal of keeping the network topology as flat and simple as possible, sticking with your current Bastion setup is the more efficient route.

---

can you show me the documentation refs for you claims

---

Here are the official Microsoft Azure documentation references that support those architectural requirements and constraints:

1\. Azure Cloud Shell Virtual Network Isolation Overview

- Link:[Use Cloud Shell in an Azure virtual network](https://learn.microsoft.com/en-us/azure/cloud-shell/vnet/overview)
- Key Claims Validated:
	- Default Isolation: "By default, Azure Cloud Shell sessions run in a container in a Microsoft network that's separate from your resources. Commands that run inside the container can't access resources in a private virtual network."
	- Azure Relay Requirement & Cost: "Virtual network isolation requires you to use Azure Relay, which is a paid service… you pay for network resources."
	- Performance Impact: "Starting Cloud Shell in a virtual network is typic ally slower than a standard Cloud Shell session."

2\. Deployment and Subnet Requirements

- Link:[Deploy Azure Cloud Shell in a virtual network with quickstart templates](https://learn.microsoft.com/en-us/azure/cloud-shell/vnet/deployment)
- Key Claims Validated:
	- Three Dedicated Subnets: Under the _Collect the required information_ section, the documentation specifies the network prerequisites: _"Subnet Address ranges - This deployment creates three subnets. You need to plan your address ranges for each subnet."_ \* The documentation goes on to define these as the Container subnet (for the ephemeral Azure Container Instances), the Relay subnet (for the Azure Relay private endpoint), and the Storage subnet (for the storage account that holds your Cloud Shell profile).

Because of these requirements, while VNet-integrated Cloud Shell works well for specific high-security environments, it is a heavier and more complex network deployment than a standard Azure Bastion subnet.
