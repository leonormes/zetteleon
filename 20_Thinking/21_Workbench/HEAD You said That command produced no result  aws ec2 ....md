---
captured: "2026-03-07T16:50:30+00:00 2026-03-07T16:50:30+00:00"
created: 2026-03-07T16:50:31+00:00
modified: 2026-03-14T11:10:32+00:00
source: "https://gemini.google.com/app/ed22d10af3b11070"
status: "processing"
tags: ["input"]
title: HEAD You said That command produced no result  aws ec2 ...
type: "head"
---

## Raw Output / Content

That command produced no result

aws ec2 describe-security-group-rules \\

\--region eu-west-2 \\

\--query "SecurityGroupRules\[?IsEgress==\\\`false\\\` && ToPort==\\\`8080\\\` && IpProtocol==\\\`tcp\\\`\].\[GroupId, ReferencedGroupInfo.GroupId, CidrIpv4\]" \\

\--output table

awsadmin@ip-10-66-2-4:~$

---

That blank output is the smoking gun! It confirms exactly why your browser connection is failing.

Because the query returned absolutely nothing, it means there is currently no Security Group rule in your entire `eu-west-2` region that allows inbound TCP traffic on port 8080. Your SSM session successfully reaches the jumpbox, but the moment the jumpbox tries to route that traffic to the Pod IP (`10.66.4.146`), the AWS network quietly drops it at the EKS worker node's elastic network interface.

To fix this and get your webpage loading, we need to explicitly authorise your jumpbox (`sg-01e72a1acfcb7571b`) to speak to your EKS worker nodes on port 8080.

### The Fix: Authorise the Ingress Traffic

You will need the Security Group ID of your EKS worker nodes (or the cluster security group, depending on your EKS setup). Once you have that target ID, you can run this command on your jumpbox to instantly open the network path:

Once that rule is applied, your existing SSM port-forwarding command from your local machine will immediately start working, and `http://localhost:8080` will load the application.

Would you like me to provide a quick `kubectl` and `aws` combined command to automatically fetch the correct `<TARGET_EKS_NODE_SG>` if you aren't sure what your EKS node's Security Group ID is?

---

yes

---

Here is a quick script you can run directly on your jumpbox to trace the pod's IP back to the underlying EC2 instance and extract its Security Group ID.

This works by querying the Kubernetes API to find which worker node is hosting the pod, extracting that node's AWS instance ID, and then querying the AWS API to find its attached Security Groups.

### Step 1: Find the Target EKS Node Security Group

Copy and paste this entire block into your jumpbox terminal:

### Step 2: Authorise the Ingress Traffic

The output from the script above will present a table with a Group ID (e.g., `sg-0abc123…`) and a Group Name (usually something like `eks-cluster-sg-…` or `eks-node-group-…`).

Copy that target Group ID and insert it into this final command, running it on the jumpbox:

Once this rule successfully executes, the AWS network will instantly allow the traffic to flow. Your pending local SSM session will be able to route traffic through the jumpbox straight to the pod, and navigating to `http://localhost:8080` in Chrome should immediately load the webpage.

Would you like me to walk you through how to verify the connection is active locally once you have applied the rule?

---

we are using the test-codisc cluster

\# 1. Get the Node Name running the specific Pod IP

NODE\_NAME=$(kubectl get pods -n thehyve -o jsonpath="{.items\[?(@.status.podIP=='10.66.4.146')\].spec.nodeName}")

\# 2. Extract the underlying EC2 Instance ID for that Node

INSTANCE\_ID=$(kubectl get node $NODE\_NAME -o jsonpath='{.spec.providerID}' | awk -F/ '{print $NF}')

\# 3. Fetch and display the Security Groups attached to that EKS Node

aws ec2 describe-instances \\

\--instance-ids $INSTANCE\_ID \\

\--region eu-west-2 \\

\--query "Reservations\[\*\].Instances\[\*\].SecurityGroups\[\*\].\[GroupId, GroupName\]" \\

\--output table

\-----------------------------------------------------------------------

| DescribeInstances |

+-----------------------+---------------------------------------------+

| sg-0c25c161ce4a58b4b | eoe-sde-codisc-jumpbox-sg |

| sg-0c25c161ce4a58b4b | eoe-sde-codisc-jumpbox-sg |

| sg-02dcb1a5bbe8844b8 | eks-cluster-sg-eoe-sde-codisc-1541232588 |

| sg-02dcb1a5bbe8844b8 | eks-cluster-sg-eoe-sde-codisc-1541232588 |

| sg-01e72a1acfcb7571b | eoe-test-codisc-jumpbox-sg |

| sg-07d4303ad17faa6f9 | eks-cluster-sg-eoe-test-codisc-1471888330 |

| sg-07d4303ad17faa6f9 | eks-cluster-sg-eoe-test-codisc-1471888330 |

| sg-02dcb1a5bbe8844b8 | eks-cluster-sg-eoe-sde-codisc-1541232588 |

| sg-02dcb1a5bbe8844b8 | eks-cluster-sg-eoe-sde-codisc-1541232588 |

| sg-02dcb1a5bbe8844b8 | eks-cluster-sg-eoe-sde-codisc-1541232588 |

| sg-07d4303ad17faa6f9 | eks-cluster-sg-eoe-test-codisc-1471888330 |

+-----------------------+---------------------------------------------+

---

This output perfectly isolates the target we need.

Because you are using the `test-codisc` cluster, the relevant Security Group protecting your EKS worker nodes is `sg-07d4303ad17faa6f9` (`eks-cluster-sg-eoe-test-codisc-1471888330`).

We now have both pieces of the puzzle:

- Source (Your Jumpbox):`sg-01e72a1acfcb7571b`
- Target (Your EKS Nodes):`sg-07d4303ad17faa6f9`

### The Final Authorisation Command

To allow the network traffic through, run the following command directly on your jumpbox. _(Note: The AWS CLI requires the American spelling `authorize-security-group-ingress` for the command itself)._

Once this command successfully executes, the AWS network will instantly authorise the route.

### Testing the Connection

1. Leave the jumpbox terminal as it is.
2. Go back to your local machine's terminal and re-run your original SSM port-forwarding command (pointing to the Pod IP `10.66.4.146`):
3. Open Chrome on your local machine and navigate to `http://localhost:8080`.

Would you like me to walk you through setting up an EKS network policy just in case the cluster itself is restricting ingress traffic at the pod level?

---

this worked and I saw the login page I was after. But the pod crashed! obviously now there is a new pod with a new ip. Give me the commands to debug why it crashed when I accessed it and if we can use the svc instead

---

It is incredibly frustrating to finally get the network path clear only for the application to immediately fall over! However, the fact that you saw the login page means our AWS routing is flawless. The issue now lies entirely within the application or the pod's resources.

Here is how we can diagnose the crash, followed by the setup to use the Kubernetes Service so you never have to hunt down a Pod IP again.

### Part 1: Debugging the Crash

When a pod crashes in Kubernetes, the container runtime usually restarts it. If it restarts within the same pod shell, the previous logs are preserved. If the ReplicaSet spun up an entirely new pod, we have to look at the cluster events.

Run these commands from your jumpbox:

1\. Check the previous container's logs:If the pod kept its name but the container inside restarted, you can pull the logs from the dead container using the `--previous` flag.

_(Look for fatal errors, out-of-memory (OOM) exceptions, or database connection timeouts right at the end of the log output)._

2\. Check the cluster events:If the pod was completely evicted or deleted and a brand new one was created, the `--previous` flag will not work. Instead, check the recent events in the namespace to see exactly what the Kubernetes control plane did:

_(Scan the bottom of this list for warnings like `OOMKilled`, `Liveness probe failed`, or `FailedScheduling`)._

---

### Part 2: Bypassing Pod IPs (Using the Service)

You are absolutely right to want to use the Service (`svc/thehyve`). Services exist specifically to abstract away ephemeral Pod IPs.

Because the Service `ClusterIP` is a virtual IP that only exists inside the EKS nodes, your jumpbox cannot route to it directly using the AWS SSM remote-host document. Instead, we have to use `kubectl` on the jumpbox to bridge the gap.

Since you already have your SSH config (`hie-jmp-test`) perfectly set up to proxy through SSM, this is surprisingly easy and requires two steps.

Step 1: Start the SSH Tunnel & Kubectl Relay Open a terminal on your local machine and run this command. It uses your SSH config to log into the jumpbox while simultaneously forwarding your local port 8080 to the jumpbox's local port 8080.

Step 2: Bind the Service Once that SSH session connects and you are logged into the jumpbox, run the native Kubernetes port-forward command:

Leave this running in your terminal. You can now open your Chrome browser and navigate to `http://localhost:8080`.

Because `kubectl` is attached directly to the Service, it will automatically route your traffic to healthy pods. If the pod crashes and gets a new IP, Kubernetes updates the Service endpoints, and your browser connection will seamlessly flow to the new pod without you having to change a single command.

Would you like me to help you interpret the output of those debug logs once you pull them?

---

kubectl get pods -n thehyve

NAME READY STATUS RESTARTS AGE

thehyve-67956b8dc-f5vf7 2/2 Running 0 2m48s

thehyve-postgresql-0 1/1 Running 0 2d22h

awsadmin@ip-10-66-2-4:~$ kubectl logs -n thehyve thehyve-67956b8dc-f5vf7 --previous

Defaulted container "webserver" out of: webserver, scheduler, thehyve-init (init)

Error from server (BadRequest): previous terminated container "webserver" in pod "thehyve-67956b8dc-f5vf7" not found

---

Ah, I see exactly what happened here. The reason that command failed is because the `--previous` flag only works when a container crashes and restarts _inside the exact same pod_ (which would show up in your output as `RESTARTS: 1` or higher).

Because your pod has an `AGE` of `2m48s` and `0` `RESTARTS`, it means Kubernetes didn't just restart the application container; the ReplicaSet entirely deleted the old pod and replaced it with a brand new one. Since this is a fresh pod shell, it has no "previous" container memory to pull logs from.

When an application crashes so hard that the entire pod is evicted or replaced, the local logs die with the pod.

Here is how we can find out what killed it, and how to set up the Service connection so your browser survives any future pod swaps.

### Part 1: Debugging the Crash

Since the pod itself is gone, we have to look at the Kubernetes event trail to see why the control plane decided to replace it.

Run this command on your jumpbox to print the namespace events chronologically:

Scroll to the bottom of the output and look for the events right around the time the old pod died (about 3 minutes ago). You are looking for red flags such as:

- `OOMKilled` or `Evicted`: The application tried to use more memory than the EKS node had available, or it breached its configured memory limits.
- `Killing`: This is usually triggered if the application locked up and failed its Kubernetes Liveness probe.
- `NodeNotReady`: The underlying EC2 instance temporarily lost connection to the cluster.

_Note: If you need the actual application logs from the dead pod to see the exact code exception, you will need to check AWS CloudWatch (assuming Container Insights or Fluent Bit logging is enabled on this EKS cluster), as the cluster nodes no longer hold those text files._

---

### Part 2: Bypassing Pod IPs with the Service

You are absolutely right to want to use the Service (`svc/thehyve`). Services exist specifically to abstract away these ephemeral Pod IPs. If a pod crashes, the Service automatically updates its internal routing table to point to the new pod, meaning your browser connection can recover without you needing to type out new IPs.

Because the Service `ClusterIP` is a virtual IP that only exists inside the EKS network, your jumpbox cannot route to it directly using the raw AWS SSM network document we used earlier. Instead, we use `kubectl` on the jumpbox to bridge the gap using your SSH configuration.

Step 1: Start the SSH Tunnel Open a terminal on your local machine and run this command. It uses your SSH config to log into the jumpbox while simultaneously forwarding your local port 8080 to the jumpbox's local port 8080.

Step 2: Bind the Service Once that SSH session connects and you are at the jumpbox terminal prompt, run the native Kubernetes port-forward command:

Leave this running in your terminal. You can now open your Chrome browser and navigate to `http://localhost:8080`.

Because `kubectl` is attached directly to the Service, it will automatically route your traffic to the healthy `thehyve-67956b8dc-f5vf7` pod.

Would you like me to help you interpret the output of the `kubectl get events` command once you have run it to pinpoint the exact reason for the crash?

---

kubectl get events -n thehyve --sort-by='.metadata.creationTimestamp'

LAST SEEN TYPE REASON OBJECT MESSAGE

5m26s Normal RolloutRestartTriggered vaultstaticsecret/thehyve Rollout restart triggered for {Deployment thehyve}

13m Normal SecretRotated vaultstaticsecret/thehyve Secret synced

5m26s Normal ScalingReplicaSet deployment/thehyve (combined from similar events): Scaled down replica set thehyve-795c79cc97 from 1 to 0

57m Normal SuccessfulDelete replicaset/thehyve-69cf74fb8f Deleted pod: thehyve-69cf74fb8f-kptdn

57m Normal Killing pod/thehyve-69cf74fb8f-kptdn Stopping container scheduler

57m Normal Killing pod/thehyve-69cf74fb8f-kptdn Stopping container webserver

57m Warning Unhealthy pod/thehyve-69cf74fb8f-kptdn Readiness probe failed: Get "http://10.66.5.156:8080/": context deadline exceeded (Client.Timeout exceeded while awaiting headers)

56m Normal SuccessfulCreate replicaset/thehyve-86bcb4d895 Created pod: thehyve-86bcb4d895-4gk4b

56m Normal Scheduled pod/thehyve-86bcb4d895-4gk4b Successfully assigned thehyve/thehyve-86bcb4d895-4gk4b to ip-10-66-5-187.eu-west-2.compute.internal

56m Normal Created pod/thehyve-86bcb4d895-4gk4b Created container: thehyve-init

56m Normal Pulled pod/thehyve-86bcb4d895-4gk4b Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 413ms (413ms including waiting). Image size: 3751176217 bytes.

56m Normal Pulling pod/thehyve-86bcb4d895-4gk4b Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

56m Normal Started pod/thehyve-86bcb4d895-4gk4b Started container thehyve-init

56m Normal Started pod/thehyve-86bcb4d895-4gk4b Started container webserver

56m Normal Pulling pod/thehyve-86bcb4d895-4gk4b Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

56m Normal Pulled pod/thehyve-86bcb4d895-4gk4b Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 194ms (194ms including waiting). Image size: 3751176217 bytes.

56m Normal Created pod/thehyve-86bcb4d895-4gk4b Created container: webserver

56m Normal Created pod/thehyve-86bcb4d895-4gk4b Created container: scheduler

56m Normal Started pod/thehyve-86bcb4d895-4gk4b Started container scheduler

56m Normal Pulled pod/thehyve-86bcb4d895-4gk4b Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 199ms (199ms including waiting). Image size: 3751176217 bytes.

56m Normal Pulling pod/thehyve-86bcb4d895-4gk4b Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

56m Warning Unhealthy pod/thehyve-86bcb4d895-4gk4b Readiness probe failed: Get "http://10.66.5.210:8080/": dial tcp 10.66.5.210:8080: connect: connection refused

56m Warning Unhealthy pod/thehyve-86bcb4d895-4gk4b Liveness probe failed: Get "http://10.66.5.210:8080/": dial tcp 10.66.5.210:8080: connect: connection refused

48m Normal Killing pod/thehyve-86bcb4d895-4gk4b Stopping container webserver

48m Normal Killing pod/thehyve-86bcb4d895-4gk4b Stopping container scheduler

48m Normal SuccessfulDelete replicaset/thehyve-86bcb4d895 Deleted pod: thehyve-86bcb4d895-4gk4b

48m Warning Unhealthy pod/thehyve-86bcb4d895-4gk4b Readiness probe failed: Get "http://10.66.5.210:8080/": context deadline exceeded (Client.Timeout exceeded while awaiting headers)

48m Normal SuccessfulCreate replicaset/thehyve-59867dc8b9 Created pod: thehyve-59867dc8b9-sh2rz

48m Normal Scheduled pod/thehyve-59867dc8b9-sh2rz Successfully assigned thehyve/thehyve-59867dc8b9-sh2rz to ip-10-66-5-187.eu-west-2.compute.internal

48m Normal Pulling pod/thehyve-59867dc8b9-sh2rz Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

48m Normal Pulled pod/thehyve-59867dc8b9-sh2rz Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 209ms (209ms including waiting). Image size: 3751176217 bytes.

48m Normal Created pod/thehyve-59867dc8b9-sh2rz Created container: thehyve-init

48m Normal Started pod/thehyve-59867dc8b9-sh2rz Started container thehyve-init

48m Normal Pulling pod/thehyve-59867dc8b9-sh2rz Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

48m Normal Pulled pod/thehyve-59867dc8b9-sh2rz Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 192ms (192ms including waiting). Image size: 3751176217 bytes.

48m Normal Started pod/thehyve-59867dc8b9-sh2rz Started container scheduler

48m Normal Started pod/thehyve-59867dc8b9-sh2rz Started container webserver

48m Normal Pulling pod/thehyve-59867dc8b9-sh2rz Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

48m Normal Pulled pod/thehyve-59867dc8b9-sh2rz Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 178ms (178ms including waiting). Image size: 3751176217 bytes.

48m Normal Created pod/thehyve-59867dc8b9-sh2rz Created container: scheduler

48m Normal Created pod/thehyve-59867dc8b9-sh2rz Created container: webserver

39m Warning Unhealthy pod/thehyve-59867dc8b9-sh2rz Readiness probe failed: Get "http://10.66.4.119:8080/": dial tcp 10.66.4.119:8080: connect: connection refused

47m Warning Unhealthy pod/thehyve-59867dc8b9-sh2rz Liveness probe failed: Get "http://10.66.4.119:8080/": dial tcp 10.66.4.119:8080: connect: connection refused

40m Normal Killing pod/thehyve-59867dc8b9-sh2rz Stopping container webserver

40m Normal Killing pod/thehyve-59867dc8b9-sh2rz Stopping container scheduler

40m Normal SuccessfulDelete replicaset/thehyve-59867dc8b9 Deleted pod: thehyve-59867dc8b9-sh2rz

39m Normal SuccessfulCreate replicaset/thehyve-59b7658796 Created pod: thehyve-59b7658796-h7sp4

39m Normal Scheduled pod/thehyve-59b7658796-h7sp4 Successfully assigned thehyve/thehyve-59b7658796-h7sp4 to ip-10-66-5-187.eu-west-2.compute.internal

39m Normal Pulling pod/thehyve-59b7658796-h7sp4 Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

39m Normal Started pod/thehyve-59b7658796-h7sp4 Started container thehyve-init

39m Normal Pulled pod/thehyve-59b7658796-h7sp4 Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 387ms (387ms including waiting). Image size: 3751176217 bytes.

39m Normal Created pod/thehyve-59b7658796-h7sp4 Created container: thehyve-init

39m Normal Created pod/thehyve-59b7658796-h7sp4 Created container: webserver

39m Normal Pulling pod/thehyve-59b7658796-h7sp4 Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

39m Normal Pulled pod/thehyve-59b7658796-h7sp4 Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 185ms (185ms including waiting). Image size: 3751176217 bytes.

39m Normal Started pod/thehyve-59b7658796-h7sp4 Started container webserver

39m Normal Pulling pod/thehyve-59b7658796-h7sp4 Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

39m Normal Pulled pod/thehyve-59b7658796-h7sp4 Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 188ms (188ms including waiting). Image size: 3751176217 bytes.

39m Normal Created pod/thehyve-59b7658796-h7sp4 Created container: scheduler

39m Normal Started pod/thehyve-59b7658796-h7sp4 Started container scheduler

31m Warning Unhealthy pod/thehyve-59b7658796-h7sp4 Readiness probe failed: Get "http://10.66.4.174:8080/": dial tcp 10.66.4.174:8080: connect: connection refused

39m Warning Unhealthy pod/thehyve-59b7658796-h7sp4 Liveness probe failed: Get "http://10.66.4.174:8080/": dial tcp 10.66.4.174:8080: connect: connection refused

31m Normal SuccessfulDelete replicaset/thehyve-59b7658796 Deleted pod: thehyve-59b7658796-h7sp4

31m Normal Killing pod/thehyve-59b7658796-h7sp4 Stopping container webserver

31m Normal Killing pod/thehyve-59b7658796-h7sp4 Stopping container scheduler

31m Warning Unhealthy pod/thehyve-59b7658796-h7sp4 Readiness probe failed: Get "http://10.66.4.174:8080/": context deadline exceeded (Client.Timeout exceeded while awaiting headers)

31m Normal Scheduled pod/thehyve-66c5b765f8-nprpb Successfully assigned thehyve/thehyve-66c5b765f8-nprpb to ip-10-66-5-187.eu-west-2.compute.internal

31m Normal SuccessfulCreate replicaset/thehyve-66c5b765f8 Created pod: thehyve-66c5b765f8-nprpb

30m Normal Started pod/thehyve-66c5b765f8-nprpb Started container thehyve-init

30m Normal Pulled pod/thehyve-66c5b765f8-nprpb Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 228ms (228ms including waiting). Image size: 3751176217 bytes.

30m Normal Created pod/thehyve-66c5b765f8-nprpb Created container: thehyve-init

30m Normal Pulling pod/thehyve-66c5b765f8-nprpb Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

30m Normal Created pod/thehyve-66c5b765f8-nprpb Created container: webserver

30m Normal Pulled pod/thehyve-66c5b765f8-nprpb Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 232ms (232ms including waiting). Image size: 3751176217 bytes.

30m Normal Pulling pod/thehyve-66c5b765f8-nprpb Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

30m Normal Started pod/thehyve-66c5b765f8-nprpb Started container webserver

30m Normal Pulling pod/thehyve-66c5b765f8-nprpb Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

30m Normal Pulled pod/thehyve-66c5b765f8-nprpb Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 176ms (176ms including waiting). Image size: 3751176217 bytes.

30m Normal Started pod/thehyve-66c5b765f8-nprpb Started container scheduler

30m Normal Created pod/thehyve-66c5b765f8-nprpb Created container: scheduler

30m Warning Unhealthy pod/thehyve-66c5b765f8-nprpb Readiness probe failed: Get "http://10.66.5.210:8080/": dial tcp 10.66.5.210:8080: connect: connection refused

30m Warning Unhealthy pod/thehyve-66c5b765f8-nprpb Liveness probe failed: Get "http://10.66.5.210:8080/": dial tcp 10.66.5.210:8080: connect: connection refused

22m Normal Killing pod/thehyve-66c5b765f8-nprpb Stopping container scheduler

22m Normal Killing pod/thehyve-66c5b765f8-nprpb Stopping container webserver

22m Normal SuccessfulDelete replicaset/thehyve-66c5b765f8 Deleted pod: thehyve-66c5b765f8-nprpb

22m Warning Unhealthy pod/thehyve-66c5b765f8-nprpb Readiness probe failed: Get "http://10.66.5.210:8080/": read tcp 10.66.5.187:57428->10.66.5.210:8080: read: connection reset by peer

22m Normal SuccessfulCreate replicaset/thehyve-764d6f8c8 Created pod: thehyve-764d6f8c8-kb8nf

22m Normal Scheduled pod/thehyve-764d6f8c8-kb8nf Successfully assigned thehyve/thehyve-764d6f8c8-kb8nf to ip-10-66-5-187.eu-west-2.compute.internal

22m Normal Pulling pod/thehyve-764d6f8c8-kb8nf Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

22m Normal Pulled pod/thehyve-764d6f8c8-kb8nf Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 358ms (358ms including waiting). Image size: 3751176217 bytes.

22m Normal Started pod/thehyve-764d6f8c8-kb8nf Started container thehyve-init

22m Normal Created pod/thehyve-764d6f8c8-kb8nf Created container: thehyve-init

21m Normal Created pod/thehyve-764d6f8c8-kb8nf Created container: scheduler

21m Normal Started pod/thehyve-764d6f8c8-kb8nf Started container scheduler

21m Normal Pulling pod/thehyve-764d6f8c8-kb8nf Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

21m Normal Pulled pod/thehyve-764d6f8c8-kb8nf Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 204ms (204ms including waiting). Image size: 3751176217 bytes.

21m Normal Created pod/thehyve-764d6f8c8-kb8nf Created container: webserver

21m Normal Started pod/thehyve-764d6f8c8-kb8nf Started container webserver

21m Normal Pulling pod/thehyve-764d6f8c8-kb8nf Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

21m Normal Pulled pod/thehyve-764d6f8c8-kb8nf Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 194ms (194ms including waiting). Image size: 3751176217 bytes.

21m Warning Unhealthy pod/thehyve-764d6f8c8-kb8nf Readiness probe failed: Get "http://10.66.4.146:8080/": dial tcp 10.66.4.146:8080: connect: connection refused

21m Warning Unhealthy pod/thehyve-764d6f8c8-kb8nf Liveness probe failed: Get "http://10.66.4.146:8080/": dial tcp 10.66.4.146:8080: connect: connection refused

13m Normal SuccessfulDelete replicaset/thehyve-764d6f8c8 Deleted pod: thehyve-764d6f8c8-kb8nf

13m Normal Killing pod/thehyve-764d6f8c8-kb8nf Stopping container scheduler

13m Normal Killing pod/thehyve-764d6f8c8-kb8nf Stopping container webserver

13m Warning Unhealthy pod/thehyve-764d6f8c8-kb8nf Readiness probe failed: Get "http://10.66.4.146:8080/": read tcp 10.66.5.187:54236->10.66.4.146:8080: read: connection reset by peer

13m Normal SuccessfulCreate replicaset/thehyve-795c79cc97 Created pod: thehyve-795c79cc97-7z6s7

13m Normal Scheduled pod/thehyve-795c79cc97-7z6s7 Successfully assigned thehyve/thehyve-795c79cc97-7z6s7 to ip-10-66-5-187.eu-west-2.compute.internal

13m Normal Started pod/thehyve-795c79cc97-7z6s7 Started container thehyve-init

13m Normal Created pod/thehyve-795c79cc97-7z6s7 Created container: thehyve-init

13m Normal Pulled pod/thehyve-795c79cc97-7z6s7 Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 270ms (270ms including waiting). Image size: 3751176217 bytes.

13m Normal Pulling pod/thehyve-795c79cc97-7z6s7 Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

13m Normal Pulling pod/thehyve-795c79cc97-7z6s7 Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

13m Normal Pulled pod/thehyve-795c79cc97-7z6s7 Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 178ms (178ms including waiting). Image size: 3751176217 bytes.

13m Normal Pulled pod/thehyve-795c79cc97-7z6s7 Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 204ms (204ms including waiting). Image size: 3751176217 bytes.

13m Normal Created pod/thehyve-795c79cc97-7z6s7 Created container: webserver

13m Normal Started pod/thehyve-795c79cc97-7z6s7 Started container webserver

13m Normal Pulling pod/thehyve-795c79cc97-7z6s7 Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

13m Normal Started pod/thehyve-795c79cc97-7z6s7 Started container scheduler

13m Normal Created pod/thehyve-795c79cc97-7z6s7 Created container: scheduler

13m Warning Unhealthy pod/thehyve-795c79cc97-7z6s7 Readiness probe failed: Get "http://10.66.5.101:8080/": dial tcp 10.66.5.101:8080: connect: connection refused

13m Warning Unhealthy pod/thehyve-795c79cc97-7z6s7 Liveness probe failed: Get "http://10.66.5.101:8080/": dial tcp 10.66.5.101:8080: connect: connection refused

5m26s Normal SuccessfulDelete replicaset/thehyve-795c79cc97 Deleted pod: thehyve-795c79cc97-7z6s7

5m26s Normal Killing pod/thehyve-795c79cc97-7z6s7 Stopping container webserver

5m26s Normal Killing pod/thehyve-795c79cc97-7z6s7 Stopping container scheduler

5m22s Warning Unhealthy pod/thehyve-795c79cc97-7z6s7 Readiness probe failed: Get "http://10.66.5.101:8080/": context deadline exceeded (Client.Timeout exceeded while awaiting headers)

5m15s Normal SuccessfulCreate replicaset/thehyve-67956b8dc Created pod: thehyve-67956b8dc-f5vf7

5m14s Normal Scheduled pod/thehyve-67956b8dc-f5vf7 Successfully assigned thehyve/thehyve-67956b8dc-f5vf7 to ip-10-66-5-187.eu-west-2.compute.internal

5m4s Normal Pulling pod/thehyve-67956b8dc-f5vf7 Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

5m4s Normal Pulled pod/thehyve-67956b8dc-f5vf7 Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 351ms (351ms including waiting). Image size: 3751176217 bytes.

5m4s Normal Created pod/thehyve-67956b8dc-f5vf7 Created container: thehyve-init

5m4s Normal Started pod/thehyve-67956b8dc-f5vf7 Started container thehyve-init

4m43s Normal Pulled pod/thehyve-67956b8dc-f5vf7 Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 197ms (197ms including waiting). Image size: 3751176217 bytes.

4m43s Normal Created pod/thehyve-67956b8dc-f5vf7 Created container: webserver

4m43s Normal Pulling pod/thehyve-67956b8dc-f5vf7 Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

4m42s Normal Started pod/thehyve-67956b8dc-f5vf7 Started container webserver

4m42s Normal Pulling pod/thehyve-67956b8dc-f5vf7 Pulling image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1"

4m42s Normal Pulled pod/thehyve-67956b8dc-f5vf7 Successfully pulled image "fitfileregistry.azurecr.io/thehyve/fitfile\_etl\_container\_cuh:0.4.1" in 231ms (231ms including waiting). Image size: 3751176217 bytes.

4m42s Normal Created pod/thehyve-67956b8dc-f5vf7 Created container: scheduler

4m42s Normal Started pod/thehyve-67956b8dc-f5vf7 Started container scheduler

4m21s Warning Unhealthy pod/thehyve-67956b8dc-f5vf7 Readiness probe failed: Get "http://10.66.5.210:8080/": dial tcp 10.66.5.210:8080: connect: connection refused

4m24s Warning Unhealthy pod/thehyve-67956b8dc-f5vf7 Liveness probe failed: Get "http://10.66.5.210:8080/": dial tcp 10.66.5.210:8080: connect: connection refused

---

This event log tells a fantastic story, and I have some brilliant news for you: your pod did not crash, and your web request had absolutely nothing to do with it dying!

The log reveals exactly what is happening, and it is a completely automated, deliberate process triggered by your secrets management.

Here is the breakdown of the "crash" and why you are seeing those errors.

### The Culprit: Aggressive Vault Secret Rotation

If you look closely at the timestamps, this pod is not crashing randomly; it is being systematically replaced by Kubernetes every 8 to 9 minutes (57m, 48m, 39m, 31m, 22m, 13m, and 5m ago).

The smoking gun is right at the top of your event log:

You have a HashiCorp Vault integration (or similar secret operator) running in the cluster. Every time the Vault operator rotates or syncs the secret, it is configured to deliberately trigger a `RolloutRestart` on your `thehyve` Deployment so the application can pick up the new credentials.

Because this rotation is happening so frequently (roughly every 8 minutes), the Deployment is constantly spinning up a brand new ReplicaSet, waiting for the new pod to start, and then deleting the old one. You simply happened to access the webpage exactly when the 8-minute timer hit!

### The "Unhealthy" Errors Are Red Herrings

You might be looking at the `Unhealthy` warnings and thinking the application is failing:

These are actually normal symptoms of a pod shutting down. When the Deployment rollout triggers, Kubernetes sends a termination signal to your old pod. The `webserver` container immediately stops accepting traffic to shut down gracefully. However, the Kubernetes health probes keep checking the pod for a few more seconds. Because the web server has already turned off, the probes get a `connection refused` or `context deadline exceeded` error right before the pod is fully deleted.

### Why the Service Tunnel is Essential

This event log perfectly highlights why connecting to a direct Pod IP is dangerous in this environment. Because your Vault secrets are forcing a pod rotation every 8 minutes, your Pod IP will change every 8 minutes.

If you use the Service connection method we discussed previously:

Kubernetes will automatically handle the Vault rollouts for you. The Service acts as a stable anchor. When Vault triggers the restart and the old pod dies, `kubectl` will seamlessly route your `localhost:8080` traffic to the newly created pod without dropping your browser session or requiring you to run a new command.

Would you like me to help you check the configuration of that `vaultstaticsecret/thehyve` object to see if we can extend that 8-minute rotation timer to something less aggressive, or are you happy to proceed with the Service port-forwarding?

---

terminal 1: ssh -L 8080:localhost:8080 hie-jmp-test

Welcome to Ubuntu 24.04.1 LTS (GNU/Linux 6.8.0-1016-aws x86\_64)

\* Documentation: <https://help.ubuntu.com>

\* Management: <https://landscape.canonical.com>

\* Support: <https://ubuntu.com/pro>

System information as of Fri Feb 20 10:14:25 UTC 2026

System load: 0.05 Temperature: -273.1 C

Usage of /: 28.0% of 29.95GB Processes: 156

Memory usage: 6% Users logged in: 1

Swap usage: 0% IPv4 address for ens5: 10.66.2.4

\* Ubuntu Pro delivers the most comprehensive open source security and

compliance features.

<https://ubuntu.com/aws/pro>

Expanded Security Maintenance for Applications is not enabled.

116 updates can be applied immediately.

To see these additional updates run: apt list --upgradable

Enable ESM Apps to receive additional future security updates.

See <https://ubuntu.com/esm> or run: sudo pro status

\*\*\* System restart required \*\*\*

Last login: Fri Feb 20 10:13:24 2026 from 127.0.0.1

awsadmin@ip-10-66-2-4:~$

Term2:

kubectl port-forward -n thehyve svc/thehyve 8080:8080

Unable to listen on port 8080: Listeners failed to create with the following errors: \[unable to create listener: Error listen tcp4 127.0.0.1:8080: bind: address already in use unable to create listener: Error listen tcp6 \[::1\]:8080: bind: address already in use\]

error: unable to listen on any of the requested ports: \[{8080 8080}\]

---

Ah, the classic "address already in use" error! This simply means that port `8080` is currently occupied by another process and cannot accept a new binding.

Given all the excellent debugging we did earlier, there are two highly probable reasons for this:

1. A Ghost Process on the Jumpbox: There is a "zombie" `kubectl` process or AWS SSM agent still running in the background of your jumpbox from our earlier tests.
2. Terminal Confusion: If you accidentally ran Terminal 2 on your _local machine_ instead of the jumpbox, the port will be blocked because Terminal 1's SSH tunnel is already actively listening on your local port `8080`.

Because you are already successfully logged into the jumpbox in Terminal 1 (sitting at the `awsadmin@ip-10-66-2-4:~$` prompt), you can actually execute everything right there without needing a second terminal.

Here is how to clear the blockage and get the tunnel running seamlessly:

### Step 1: Terminate the Ghost Process

In Terminal 1 (on your jumpbox), run this command to force-close anything currently clinging to port `8080`:

_(If it outputs a process ID and kills it, you know we found the culprit. You can also run `killall kubectl` just to be completely certain)._

### Step 2: Start the Kubernetes Relay

Still in Terminal 1 on the jumpbox, run your port-forward command again:

As soon as that command outputs `Forwarding from 127.0.0.1:8080`, the connection is live. Your SSH tunnel (which is running concurrently because you used `-L 8080:localhost:8080` to connect) will securely pipe the traffic from your local machine directly into the Service.

Open Chrome on your local machine and navigate to `http://localhost:8080`.

Would you like me to show you how to wrap this entire workflow into a single, automated bash alias on your local machine so you never have to memorise these commands or manually clear stuck ports again?

---

kubectl port-forward -n thehyve svc/thehyve 8080:8080

Forwarding from 127.0.0.1:8080 -> 8080

Forwarding from \[::1\]:8080 -> 8080

Handling connection for 8080

Handling connection for 8080

Handling connection for 8080

Handling connection for 8080

Handling connection for 8080

Handling connection for 8080

Handling connection for 8080

Handling connection for 8080

Handling connection for 8080

Handling connection for 8080

Handling connection for 8080

Handling connection for 8080

Handling connection for 8080

Handling connection for 8080

E0220 10:23:01.939481 239858 portforward.go:424\] "Unhandled Error" err="an error occurred forwarding 8080 -> 8080: error forwarding port 8080 to pod 9be4f975269d42b44c068fac7da3ad33672a2f6c868aec10a48b871f86c32a98, uid: network namespace for sandbox \\"9be4f975269d42b44c068fac7da3ad33672a2f6c868aec10a48b871f86c32a98\\" is closed"

error: lost connection to pod

awsadmin@ip-10-66-2-4:~$ channel 4: open failed: connect failed: Connection refused

channel 5: open failed: connect failed: Connection refused

channel 3: open failed: connect failed: Connection refused

channel 4: open failed: connect failed: Connection refused

channel 3: open failed: connect failed: Connection refused

channel 4: open failed: connect failed: Connection refused

channel 3: open failed: connect failed: Connection refused

channel 4: open failed: connect failed: Connection refused

channel 3: open failed: connect failed: Connection refused

channel 4: open failed: connect failed: Connection refused

^C

awsadmin@ip-10-66-2-4:~$ kubectl port-forward -n thehyve svc/thehyve 8080:8080

Forwarding from 127.0.0.1:8080 -> 8080

Forwarding from \[::1\]:8080 -> 8080

Handling connection for 8080

Handling connection for 8080

E0220 10:23:28.882529 239935 portforward.go:424\] "Unhandled Error" err="an error occurred forwarding 8080 -> 8080: error forwarding port 8080 to pod 004bb2c4cc13f1cb6da6b1eee5354f51799c5b98f82a83dc832f4b0eedba5cb8, uid: failed to execute portforward in network namespace \\"/var/run/netns/cni-f646250f-4bde-9cf4-897a-c088eade78b2\\": failed to connect to localhost:8080 inside namespace \\"004bb2c4cc13f1cb6da6b1eee5354f51799c5b98f82a83dc832f4b0eedba5cb8\\", IPv4: dial tcp4 127.0.0.1:8080: connect: connection refused IPv6 dial tcp6: address localhost: no suitable address found "

error: lost connection to pod

awsadmin@ip-10-66-2-4:~$ channel 3: open failed: connect failed: Connection refused

channel 5: open failed: connect failed: Connection refused

channel 3: open failed: connect failed: Connection refused

channel 4: open failed: connect failed: Connection refused

channel 3: open failed: connect failed: Connection refused

channel 4: open failed: connect failed: Connection refused

---

This exposes a notorious quirk in how Kubernetes handles Service port-forwarding, and it ties directly back to that 8-minute Vault secret rotation cycle we discovered!

When you run `kubectl port-forward svc/thehyve`, Kubernetes is slightly deceptive. It does not actually route traffic dynamically through the Service load balancer. Instead, it queries the Service _once_, picks a single active Pod IP from the list, and binds your tunnel directly to that specific pod.

When the Vault operator inevitably triggers the rollout and deletes that exact pod, the `network namespace for sandbox… is closed` error occurs because the underlying container literally ceases to exist. `kubectl` then exits completely instead of gracefully failing over to the new pod.

Those `channel X: open failed` errors following the crash are simply your local Chrome browser trying to fetch background assets through the SSH tunnel, but hitting a dead end because `kubectl` has stopped listening on the jumpbox.

### The Fix: The Auto-Reconnect Loop

Because `kubectl port-forward` cannot handle pod rotation natively, the standard industry workaround is to wrap the command in a simple bash loop. When the pod dies and `kubectl` drops the connection, the loop will instantly catch it and establish a fresh tunnel to the newly spun-up pod.

Run this continuous loop command in your jumpbox terminal (Terminal 1):

### How to Use it

1. Leave that loop running in the jumpbox terminal.
2. Because your SSH tunnel (`ssh -L 8080:localhost:8080`) is still active in the background, just go back to Chrome on your local machine.
3. Refresh `http://localhost:8080`.

The webpage will load normally. Whenever Vault kills the pod, your browser might hang for about 2 to 3 seconds while the script reconnects to the new pod, but it will automatically recover without you having to touch the terminal again.

Would you like me to show you how to inspect the Vault `StaticSecret` object to see if we can safely increase that aggressive 8-minute rotation interval to something more stable, like 24 hours?

---

I need a wiki playbook for the issues we solved here so that I can quickly repeat this and get a working connection, both for this and a more generic for any other pods I want to access via the web browser in a private cluster

---

This is a brilliant idea. After navigating the quirks of AWS network routing, Kubernetes service behaviours, and aggressive Vault secret rotations, capturing this in a playbook will save you and your team hours of future debugging.

Here is a structured, copy-pasteable wiki playbook written specifically for your architecture. It covers the bulletproof method for volatile pods, the direct network method, and a troubleshooting matrix based on exactly what we solved today.

---

## Playbook: Accessing Private EKS Web Apps via SSM Jumpbox

Architecture Overview This guide details how to securely route web traffic from your local browser (`localhost`) into a private EKS cluster. The connection flows from your local machine, through an AWS Systems Manager (SSM) tunnel to a jumpbox inside the VPC, and finally to the internal Kubernetes pods.

---

## Method 1: The "Bulletproof" SSH + Kubectl Relay (Recommended)

Best for: Standard usage, long-running sessions, and applications where pods restart frequently (e.g., triggered by HashiCorp Vault secret rotations).

Because `kubectl port-forward` binds to a single backend Pod IP even when pointed at a Service, the connection will drop if the pod rotates. This method uses an auto-healing loop to instantly restore the connection.

### Step 1: Establish the Local SSH Tunnel

On your local machine, open a terminal and use your configured SSH-over-SSM alias to bind your local port to the jumpbox port.

_Leave this terminal open and running._

### Step 2: Start the Auto-Healing Kubectl Loop

Once logged into the jumpbox (in the terminal you just opened), set your AWS environment variables to authenticate with the cluster. Then, run this loop to attach to the Kubernetes Service. If the pod dies, the loop automatically catches the error and reconnects.

### Step 3: Access the Application

Open your local web browser and navigate to: `http://localhost:8080`

---

## Method 2: Direct SSM to Pod IP Routing (Network Layer)

Best for: Bypassing `kubectl` entirely, or when you only want to use the AWS CLI._Warning: This will fail if the pod restarts, as the IP will change. It also requires specific Security Group ingress rules._

### Step 1: Get the Pod's VPC IP Address

Log into your jumpbox and fetch the routable VPC IP address of the target pod.

### Step 2: Verify and Authorise Security Groups

The AWS network will silently drop the connection if the EKS worker nodes do not allow ingress from the jumpbox.

Run this script on the jumpbox to find the necessary Security Group IDs and authorise the traffic:

### Step 3: Start the SSM Remote Host Session

On your local machine, open a terminal and run the SSM port-forwarding document, pointing it directly to the Pod IP.

Open your local web browser and navigate to: `http://localhost:8080`

---

## Troubleshooting Matrix

| Error / Symptom | Root Cause | The Fix |
| --- | --- | --- |
| `TargetNotConnected` when running `aws ssm start-session` | The AWS CLI is using the wrong default region or profile, so it cannot "see" the jumpbox. | Append `--region eu-west-2 --profile <your-profile>` to the command. |
| Browser times out / Endless spinning (when using Direct Pod IP method) | The EKS Node Security Group is blocking inbound traffic from the jumpbox instance. | Follow Step 2 in Method 2 to authorise the jumpbox SG to reach the EKS Node SG on the target port. |
| `bind: address already in use` when running `kubectl port-forward` | A previous crashed session or background process is still clinging to port 8080 on the jumpbox. | Run `fuser -k 8080/tcp` on the jumpbox to force-kill the ghost process. |
| `network namespace closed` or `lost connection to pod` | The specific pod your session was bound to was deleted (e.g., Vault secret rotation, OOM kill, or deployment rollout). | Wrap your `kubectl port-forward` command in the `while true` loop shown in Method 1 so it reconnects automatically. |
| Cannot route to ClusterIP via AWS SSM Document | SSM `AWS-StartPortForwardingSessionToRemoteHost` only understands real VPC IPs, not Kubernetes virtual IPs. | Use Method 1 (SSH Tunnel + native Kubectl), or point the SSM document to a real Pod IP (Method 2). |

---

Would you like me to generate a simple bash script that you can save on your local machine to fully automate Method 1 so you only ever have to type one command to launch both the tunnel and the loop?

---

yes

---

Here is the automation script. It elegantly combines the local SSH tunnel, remote ghost-process cleanup, and the auto-healing `kubectl` loop into a single executable file.

It also uses a neat SSH trick (`bash -l -c`) to ensure that when it connects to the jumpbox, it executes as a "login shell". This ensures your jumpbox's `.bash_profile` or `.bashrc` runs first, automatically loading any necessary AWS environment variables before attempting to run `kubectl`.

### The Automation Script

1. On your local machine, create a new file named `connect-thehyve.sh`:
2. Copy and paste the following code into the file:
	Bash

	```
	#!/bin/bash
	# --- Configuration ---
	JUMPBOX_HOST="hie-jmp-test"
	NAMESPACE="thehyve"
	TARGET="svc/thehyve"
	PORT="8080"
	# ---------------------
	echo "Initialising secure tunnel to ${JUMPBOX_HOST} for ${NAMESPACE}/${TARGET}..."
	echo "The web application will be available at: http://localhost:${PORT}"
	echo "Press Ctrl+C at any time to cleanly terminate the connection."
	echo "-------------------------------------------------------------------"
	# Execute SSH with Local Forwarding (-L) and pseudo-terminal allocation (-t)
	# The remote command is wrapped in a login shell to ensure AWS environment variables load
	ssh -t -L ${PORT}:localhost:${PORT} "${JUMPBOX_HOST}" \
	  "bash -l -c '
	    echo \"Checking for and clearing any ghost processes on port ${PORT}...\"
	    fuser -k ${PORT}/tcp 2>/dev/null
	    echo \"Starting auto-healing kubectl port-forward loop...\"
	    while true; do
	      kubectl port-forward -n ${NAMESPACE} ${TARGET} ${PORT}:${PORT}
	      echo \"[Warning] Connection dropped (pod likely rotated). Reconnecting in 2 seconds...\"
	      sleep 2
	    done
	  '"
	```

3. Save the file and make it executable:

### How to Use It

Whenever you need to access the application, simply open your local terminal and run:

The script will handle the port binding, log into the jumpbox, clear any stuck connections from previous sessions, and start the resilient loop. Once you see the `Forwarding from 127.0.0.1:8080` message, you can open Chrome and head straight to `http://localhost:8080`.

When you are finished working, just press `Ctrl+C`. The script will gracefully kill the remote `kubectl` loop and close the SSH tunnel in one go.

Would you like me to show you how to move this script into your local machine's `bin` directory so you can type `connect-thehyve` from any folder without needing the `./` prefix?
