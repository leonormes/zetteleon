**Traffic routing**

Any traffic sent to this IP (from other instances, services, etc.) will first pass through the VPC’s internal routing and eventually land at the ENI. 

The ENI, in turn, delivers this traffic to its attached resource (e.g., EC2 instance). 

Outgoing traffic from the instance also passes through this ENI.