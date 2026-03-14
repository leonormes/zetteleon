---
created: 2026-03-14T09:50:12+00:00
modified: 2026-03-14T11:09:28+00:00
tags: [articles]
title: Azure Private DNS FAQ
---

## Azure Private DNS FAQ

![rw-book-cover](https://learn.microsoft.com/en-us/media/open-graph-image.png)

### Metadata

- Author: [[asudbring]]
- Full Title: Azure Private DNS FAQ
- Category: articles
- Summary: Azure Private DNS lets you manage private domain names within and across virtual networks without needing internet access. You can link many virtual networks, even across subscriptions and regions, to a private DNS zone for easy name resolution. DNS records are automatically created and updated based on virtual machine status, but manual changes are also possible.
- URL: <https://learn.microsoft.com/en-us/azure/dns/dns-faq-private>

### Full Document

The following are frequently asked questions about Azure private DNS.

#### Does Azure DNS Support Private Domains?

Private domains are supported using the Azure Private DNS zones feature. Private DNS zones are resolvable only from within specified virtual networks. For more information, see the [overview](https://learn.microsoft.com/en-us/azure/dns/private-dns-overview).

For information on other internal DNS options in Azure, see [Name resolution for VMs and role instances](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-name-resolution-for-vms-and-role-instances).

#### Will Azure Private DNS Zones Work across Azure Regions?

Yes. Private Zones is supported for DNS resolution between virtual networks across Azure regions. Private Zones works even without explicitly peering the virtual networks. All the virtual networks must be linked to the private DNS zone.

#### Is Connectivity to the Internet from Virtual Networks Required for Private Zones?

No. Private zones work along with virtual networks. You use them to manage domains for virtual machines or other resources within and across virtual networks. Internet connectivity isn't required for name resolution.

#### Can the Same Private Zone Be Used for Several Virtual Networks for Resolution?

Yes. You can link a private DNS zone with thousands of virtual networks. For more information, see [Azure DNS Limits](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#azure-dns-limits)

#### Can a Virtual Network that Belongs to a Different Subscription Be Linked to a Private Zone?

Yes. You must have write operation permission on the virtual networks and the private DNS zone. The write permission can be granted to several Azure roles. For example, the Classic Network Contributor Azure role has write permissions to virtual networks and Private DNS zones Contributor role has write permissions on the private DNS zones. For more information on Azure roles, see [Azure role-based access control (Azure RBAC)](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview).

#### What Causes the Automatically Registered Virtual Machine DNS Records in a Private Zone Be Created or Deleted?

When you start a virtual machine within a linked virtual network with autoregistration enabled, DNS records are automatically created for that virtual machine. When you stop a virtual machine and it is deallocated, the autoregistered DNS records are removed.

#### I've Reconfigured the OS in My Virtual Machine to Have a New Host name or Static IP Address. Why Don't I See that Change Reflected in the Private Zone?

The private zone's records are populated by the Azure DHCP service; client registration messages are ignored. If you have disabled DHCP client support in the VM by configuring a static IP address, changes to the host name or static IP in the VM aren't reflected in the zone.

#### I Have Configured a Preferred DNS Suffix in My Windows Virtual Machine. Why Are My Records Still Registered in the Zone Linked to the Virtual Network?

The Azure DHCP service ignores any DNS suffix when it registers the private DNS zone. For example, if your virtual machine is configured for `contoso.com` as the primary DNS suffix, but the virtual network is linked to the `fabrikam.com` private DNS zone, the virtual machine's registration appears in the `fabrikam.com` private DNS zone.

#### Can an Automatically Registered Virtual Machine Record in a Private Zone from a Linked Virtual Network Be Deleted Manually?

Yes. You can overwrite the automatically registered DNS records with a manually created DNS record in the zone. The following question and answer address this topic.

#### What Happens when I Try to Manually Create a New DNS Record into a Private Zone that Has the Same Hostname as an Automatically Registered Existing Virtual Machine in a Linked Virtual Network?

You try to manually create a new DNS record into a private zone that has the same hostname as an existing, automatically registered virtual machine in a linked virtual network. When you do, the new DNS record overwrites the automatically registered virtual machine record. If you try to delete this manually created DNS record from the zone again, the delete succeeds. The automatic registration happens again as long as the virtual machine still exists and has a private IP attached to it. The DNS record is re-created automatically in the zone.

#### What Happens when We Unlink a Linked Virtual Network from a Private Zone? Will the Automatically Registered Virtual Machine Records from the Virtual Network Be Removed from the Zone Too?

Yes. To unlink a linked virtual network from a private zone, you update the DNS zone to remove the associated virtual network link. In this process, virtual machine records that were automatically registered are removed from the zone.

#### What Happens when We Delete a Linked Virtual Network That's Linked to a Private Zone? Do We Have to Manually Update the Private Zone to Unlink the Virtual Network as a Linked Virtual Network from the Zone?

No. When you delete a linked virtual network without unlinking it from a private zone first, your deletion operation succeeds and the links to the DNS zone are automatically cleared.

#### Will DNS Resolution by Using the Default FQDN (internal.cloudapp.net) Still Work even when a Private Zone (for Example, private.contoso.com) is Linked to a Virtual Network?

Yes. Private Zones don't replace the default Azure-provided internal.cloudapp.net zone. Whether you rely on the Azure-provided internal.cloudapp.net or on your own private zone, use the FQDN of the zone you want to resolve against.

#### Will the DNS Suffix on Virtual Machines within a Linked Virtual Network Be Changed to that of the Private Zone?

No. The DNS suffix on the virtual machines in your linked virtual network stays as the default Azure-provided suffix ("\*.internal.cloudapp.net"). You can manually change this DNS suffix on your virtual machines to that of the private zone. For guidance on how to change this suffix refer to [Use dynamic DNS to register hostnames in your own DNS server](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-name-resolution-ddns#windows-clients)

#### What Are the Usage Limits for Azure DNS Private Zones?

Refer to [Azure DNS limits](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/azure-subscription-service-limits#private-dns) for details on the usage limits for Azure DNS private zones.

#### Why Don't My Existing Private DNS Zones Show up in New Portal Experience?

If your existing private DNS zone were created using preview API, you must migrate these zones to new resource model. Private DNS zones created using preview API won't show up in new portal experience. See below for instructions on how to migrate to new resource model.

#### How Do I Migrate My Existing Private DNS Zones to the New Model?

We strongly recommend that you migrate to the new resource model as soon as possible. Legacy resource model will be supported, however, further features won't be developed on top of this model. In future, we intend to deprecate it in favor of new resource model. For guidance on how to migrate your existing private DNS zones to new resource model see [migration guide for Azure DNS private zones](https://learn.microsoft.com/en-us/azure/dns/private-dns-migration-guide).

#### Which One Takes Precedence, Azure Private DNS or a Custom DNS Server Setup on a VM?

That depends how you configured your Azure VMs or virtual network. If you specify custom DNS at the virtual-network or NIC level (by pointing to the IP address of the NIC of the VM running the DNS server), this will take precedence. If not, then the private DNS zone linked to the virtual network will apply.

##### Do Azure DNS Private Zones Store Any Customer Content?

No, Azure DNS private zones don't store any customer content.

#### Next Steps

- [Learn more about Azure Private DNS](https://learn.microsoft.com/en-us/azure/dns/private-dns-overview)
