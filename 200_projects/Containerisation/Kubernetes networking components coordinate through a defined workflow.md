---
aliases: []
confidence: 
created: 2025-10-26T17:22:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:27Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [cni, container-runtime, coordination, kube-proxy, kubelet, topic/technology/containers, topic/technology/kubernetes, type/fact, workflow]
title: Kubernetes networking components coordinate through a defined workflow
type: Fact
uid: 
updated: 
version: 1
---

## Summary

Kubernetes networking components follow a coordinated workflow where kubelet, container runtime, CNI plugins, and kube-proxy work together to configure pod networking and maintain service connectivity throughout the cluster.

## Details

### Pod Creation Workflow

1. **API Request**: Pod creation request received by kube-apiserver
2. **Scheduling**: kube-scheduler assigns pod to specific node
3. **kubelet Action**: kubelet on target node receives pod specification
4. **Container Runtime**: kubelet instructs container runtime to create containers
5. **Container Startup**: Runtime starts containers and reports readiness
6. **CNI Invocation**: kubelet calls CNI plugin to configure pod network
7. **Network Setup**: CNI plugin assigns IP, creates interfaces, sets up routing

### Service Configuration Workflow

1. **Service Creation**: Service definition stored in etcd via apiserver
2. **Endpoint Discovery**: Endpoint controller creates endpoint objects
3. **kube-proxy Watch**: kube-proxy on all nodes watches for service/endpoint changes
4. **Rule Generation**: kube-proxy generates iptables/IPVS rules for service routing
5. **Load Balancing**: Rules distribute traffic to healthy pod endpoints
6. **Dynamic Updates**: Rules update automatically when pods/services change

### Component Coordination Points

**kubelet Responsibilities:**

- Pod lifecycle management
- CNI plugin invocation
- Container runtime coordination
- Network readiness verification

**Container Runtime Role:**

- Container creation and management
- Network namespace preparation
- CNI plugin coordination
- Status reporting to kubelet

**CNI Plugin Functions:**

- Network namespace configuration
- IP address assignment (IPAM)
- Interface creation (veth, bridge)
- Routing and rule setup

**kube-proxy Operations:**

- Service/endpoint monitoring
- Load balancing rule generation
- Traffic redirection implementation
- Health checking integration

**etcd Integration:**

- Configuration storage
- State consistency maintenance
- Change notification distribution
- Recovery and backup source

### Error Handling and Recovery

- **Network Failures**: CNI plugin retry mechanisms
- **Pod Restarts**: Automatic network reconfiguration
- **Node Failures**: Service endpoint updates and traffic rerouting
- **Configuration Drift**: Reconciliation loops ensure desired state

## Related

- [[Container runtime configures pod networking through CNI plugins]] - Runtime responsibilities
- [[kube-proxy implements Services using iptables or IPVS]] - Service implementation
- [[etcd stores cluster network state and service configuration]] - State management
- [[MOC - Container Runtime & Orchestration]] - Complete orchestration picture
