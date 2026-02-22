# Private DNS options for AKS

![rw-book-cover](https://i.ytimg.com/vi/1_iFSg9Roeg/maxresdefault.jpg?v=668537ec)

## Metadata
- Author: [[Houssem Dellai]]
- Full Title: Private DNS options for AKS
- Category: #articles
- Summary: There are two main DNS options for private AKS clusters: disabling public FQDN with a private DNS zone, or enabling public FQDN without a private DNS zone. Using a private DNS zone is more secure but requires managing DNS records carefully, especially in shared environments. Teams must decide between trusting AKS to manage DNS records or using automation to control changes for security.
- URL: https://www.youtube.com/watch?v=1_iFSg9Roeg

## Full Document
let's learn in this SLB session how to configure a private D Zone with a private AK cluster for that we'll explore the options for configuring DNS with a private AKs cluster during the creation so typically you would have two options which are two feature plags that you can enable or disable when creating your AKs cluster first of all is disable public fqdn so this value could be either true or false we'll see what is the impact of using this Fe feature and 

then we have a second option that is called private DNS Zone private DNS Zone takes three options first option is none it means that here I don't want to use a private DNS zone or system it means that the private DNS Zone will be created and managed by the AKs cluster or it could also be the resource ID and this is the use case for using bring your own uh private DNS Zone that you re that you manage yourself let's take this first 

use case where here we have a Nas cluster that is attached to a customer virtal network using private endpoint private DNS Zone will be us it to resolve access to the control plane of the cluster here because we have one single virtual Network then any VM or any workload within that virtual network will be able to resolve access to that control plane this is the typical configuration where we use disabled public fqdn to be true and at the same 

time private DNS Zone will be either equal to system or to will use bring your own DNS Zone in both cases the AKs cluster will create the a record but now for organizations that are using H and spoke models they will have the AKs cluster attached to the spoke virtal Network and then they would have a her that is imping with that spoke and the her itself might be also imping with with other Spokes and it might be also 

imping with on premise veral networks and here we want to be able to resolve access to the AKs cluster from any workload or VM from within the spoke virtal Network and also from any VM that is within the Hub virtual Network so again here we can rely on the private DNS Zone to achieve that domain name resolution but actually there is a more easy solution the solution 

is to enable the public fqdn so this means that here when creating the cluster we set up the disabled public fqdn to be false and then we don't need to create a private DNS zone so we'll set private DNS Zone to be equal none so this means here we'll go will not create this private DN zone won't be created and by setting public fqdn to be equal false this means that here the fqdn of 

the control plane of the cluster will be resolved not through that private DNS Zone because it's not created but it will be resolved through Azure DNS so this means that here within Azure DNS we will have a record that is the fqdn of our cluster that will point to the private IP of our cluster and this fqdn will be reservable publicly from the internet this means that also our 

virtual networks including the Hub and this spook will be able to resolve that fqdn publicly to get that private IP to access the control plane of the cluster now the fact that this fqdn can resolve the private endpoint private IP address publicly on the internet this could be acceptable by some organizations because they will consider that the AKs control plane is still secured because you have airback access control and the only way to access that control plane is from 

within the virtual network if you belong to those people then this architecture would be the simplest for you to implement however for some other companies that will consider that public fqdn is a security threat and they don't accept that will be will resolve to a private IP address because they consider that if an attacker within the virtal network knows that private IP address that will will be considered as a threat to uh the control plane so for this people we have other options to consider 

so they will need to use the private DNS Zone this means that they will have their AKs cluster control plane exposed through a public or private endpoint that we leave within a virtual Network that is the spoke virtual Network that will be paed with Hub virtual Network so here they will go to disable that public fqdn it will be disabled by setting disable public fq dn2 true this means 

that they should use or they should rely on a private DNS Zone that they will set up right here and to create that private DNS Zone they have two options system or resource ID or bring your own DNS zone so with system it means that they will allow Azure or AKs to create that private DNS Zone and manage that private DNS Zone by creating the a records with resource ID or if you use bring your own DNS Zone this means that it's up to you 

to create the private DNS Zone before creating the cluster and then when you create the cluster you specify private DNS Zone to the resource ID of the private DNS Zone and in this case the AKs through its identity whether that is managed Identity or service principle it will go to it will go ahead to connect to that private DNS Zone and it will go to create an N record and here this private DS Zone will be of course linked to the hub virtual Network the this means that any virtual machine inside 

here will be able to resolve that private endpoint in addition to that actually a new link should be created here from the spoke to the private DNS Zone this might change in the future but today this is um needed for the AKs to function uh correctly and this link will be used by the nodes of the cluster that are within the spoke vet to be able to resolve the um IP address of the cluster now if we have multiple AKs clusters 

with multiple virtual networks we can still use private DNS Zone but we can leverage also the subdomain name through creating a child private DNS Zone a child private DNS zone is actually a private DNS Zone that will use the same prefix for the fqdn that is used by the DNS Zone and it will be attached to the this parent DNS zone so this model could be used and leveraged by the additional DNS or the additional virtual networks 

and the AKs clusters in order to instead accessing the private DNS Zone and creating a records there they can do that at this level at the child d zone that could be leveraged by uh using another flag when creating the AKs cluster that is the fqdn subdomain let's now analyze these Solutions in terms of operating model so for the first model here this will be typically used by the application team who will own their own 

infrastructure so they will own their own a cluster their vet and their private DNS zone so they can write write records within that DNS Zone and that should be feasible Second Use case here this part here is owned by the application team or the project team and this part here will be owned by platform team the project team will typically create its own resources for within their own spoke virtual Network and also the project team or the platform team 

they will create the Hub Network with the DNS components and so on and here we don't have private DNS zone so there is no interference between the responsibilities of the two teams however in this model we have an issue here so the AKs and the vnet will be owned here by the application team or by the project team typically within most of the cases however this part here that is the Hub and the private DNS zones will be owned by by the operation or by 

the platform team sometimes we call them the Ops Team or the anra team or the security team or the network team whatever you want to name it it's another team it's a different team than the project team the issue here will be at the level of the private DNS zone so the private DNS Zone if it's Central private DNS Zone it means that we will create only one single private DNS Zone attached to the hub virtual Network that will be managed by the platform team however here the AKs cluster using its 

identity needs to go to connect to that private d zone and create a n record and the fact that it could create that a record this means that the platform team will be afraid from that operation because that identity of the cluster that have the right airback role to do that change within the private DNS Zone could be altered and it could be used to add or delete or edit some a some existing a records for the other teams 

so they don't want really to trust this operation in this case they have two options first option is to just accept that risk because this risk of using this identity is the same risk as using another identity that is managed by this platform team to do the same operations on the private DNS Zone second option is to not allow the project team to do this operation and instead they can do that 

either manually or using automation tools like the devops pipelines or automated scripts that will go to be triggered on the creation on each new AKs cluster and private endpoint that will go to look for the fqdn and then that script will go to write the a record within the private DNS Zone the issue again with this is that that fqdn should be created before creating the AKs cluster and we don't know which fqdn will be used by the AKs cluster because 

part of that fqdn is a prefix that is randomly generated so this will leave you with one single option which is the first option which is to accept that the identity of the cluster creates that a record this might change in the future so keep an eye on the AKs updates I hope this was helpful thank you
