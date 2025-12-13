---
aliases: []
confidence: 
created: 2025-04-02T03:12:13Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, FFAPP-3588, gateway, lattice, networking]
title: VPC Lattice Service Network
type: 
uid: b0b32806-0e2f-4a1a-929f-d2b6855af996
updated: 
version: 
---

## Current Setup Documentation

### Architecture Overview

```sh
[EKS Cluster (AWS)]
├── VPC Lattice Service Network
│   └── Service: echo-server-service
│       └── Target Group: echo-server-target-group
├── Gateway API Controller
│   └── Gateway: default
│       └── HTTP Route: echo-server-route
└── Echo Server
    └── Pod: echo-server-84f9549498-65pql
```

### Components

#### 1. VPC Lattice Service Network
- Name: "default"
- ARN: `arn:aws:vpc-lattice:eu-west-2:592527451415:servicenetwork/sn-0c7635717d4e989b1`
- Associated VPC: `vpc-0e86d4ca9eb77129d`

#### 2. Gateway API Controller
- Namespace: `aws-application-networking-system`
- Service Account: `gateway-api-controller`
- IAM Role: `ff-test-ingress-vpc-lattice-controller-role`
- Environment Variables:

```sh
REGION=eu-west-2
AWS_ACCOUNT_ID=592527451415
CLUSTER_VPC_ID=vpc-0e86d4ca9eb77129d
CLUSTER_NAME=ff-test-ingress
LATTICE_ENDPOINT=https://vpc-lattice.eu-west-2.amazonaws.com
DEFAULT_SERVICE_NETWORK=default
```

#### 3. Gateway Configuration

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: Gateway
metadata:
  name: default
  namespace: aws-application-networking-system
spec:
  gatewayClassName: amazon-vpc-lattice
  listeners:
    - name: http
      port: 80
      protocol: HTTP
      allowedRoutes:
        namespaces:
          from: Same
```

#### 4. HTTP Route Configuration

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: echo-server-route
  namespace: aws-application-networking-system
spec:
  parentRefs:
    - name: default
      kind: Gateway
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /echo
      backendRefs:
        - name: echo-server
          port: 80
```

#### 5. Echo Server Service
- Name: `echo-server`
- Type: `ClusterIP`
- Port: 80
- Pod: `echo-server-84f9549498-65pql`

### Current Access
- The echo server is accessible via:

```sh
http://echo-server-route-aws-application-ne-062d9f25affefff2a.7d67968.vpc-lattice-svcs.eu-west-2.on.aws/echo
```

- Currently only accessible from within the VPC

## Demonstrating Secure Routing from Azure AKS

To demonstrate secure routing from Azure AKS, we need to:

1. Set up VPC Lattice Service Network Access:

```bash
# Create a VPC Lattice auth policy
aws vpc-lattice create-auth-policy \
  --resource-identifier arn:aws:vpc-lattice:eu-west-2:592527451415:servicenetwork/sn-0c7635717d4e989b1 \
  --policy '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "AWS": "arn:aws:iam::AZURE_ACCOUNT_ID:root"
        },
        "Action": "vpc-lattice-svcs:InvokeService",
        "Resource": "arn:aws:vpc-lattice:eu-west-2:592527451415:service/svc-062d9f25affefff2a"
      }
    ]
  }'
```

2. Create a Service Network VPC Association for Azure:

```bash
aws vpc-lattice create-service-network-vpc-association \
  --service-network-identifier sn-0c7635717d4e989b1 \
  --vpc-identifier AZURE_VPC_ID
```

3. Set up Azure AKS:

```bash
# Create Azure AKS cluster
az aks create \
  --resource-group myResourceGroup \
  --name myAKSCluster \
  --node-count 1 \
  --enable-addons monitoring \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group myResourceGroup --name myAKSCluster
```

4. Create a test client in Azure AKS:

```yaml
# test-client.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: test-client
spec:
  replicas: 1
  selector:
    matchLabels:
      app: test-client
  template:
    metadata:
      labels:
        app: test-client
    spec:
      containers:
      - name: test-client
        image: curlimages/curl
        command: ['/bin/sh', '-c']
        args:
        - |
          while true; do
            curl -v http://echo-server-route-aws-application-ne-062d9f25affefff2a.7d67968.vpc-lattice-svcs.eu-west-2.on.aws/echo
            sleep 30
          done
```

5. Deploy the test client:

```bash
kubectl apply -f test-client.yaml
```

6. Monitor the test client:

```bash
kubectl logs -f deployment/test-client
```

### Security Considerations

1. Network Security:
   - VPC Lattice provides secure, private connectivity
   - Traffic is encrypted in transit
   - Access is controlled via IAM policies

2. Authentication:
   - Azure AKS cluster must have proper IAM roles
   - Service Network auth policy controls access
   - VPC associations ensure network isolation

3. Monitoring:
   - Enable CloudWatch logging for VPC Lattice
   - Monitor Azure AKS logs
   - Set up alerts for unauthorized access attempts

Would you like me to provide more details about any of these aspects or help you set up the Azure AKS integration?
