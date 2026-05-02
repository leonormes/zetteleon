---
created: 2026-05-02T19:36:46+00:00
modified: 2026-05-02T20:40:35+00:00
title: Describe how controllers work abstractly and more ...
---

That's an excellent line of questioning\! Understanding controllers deeply is key to understanding Kubernetes, and the connection to cybernetics is quite insightful.
Let's break down how controllers work, both abstractly and more specifically, and then explore their relationship with cybernetics.

## How Kubernetes Controllers Work

1\. Abstractly: The Control Loop
At its core, every Kubernetes controller operates on a fundamental principle known as a control loop (or reconciliation loop). This can be summarised with three main phases:

- Observe: The controller continuously monitors the current state of the system for the specific resources it's responsible for. This "current state" is typically read from Kubernetes's central datastore, etcd (via the API server).
- Compare (or Diff): The controller compares this observed actual state against the desired state. The desired state is what you, the user (or another automated system), have specified in the object's spec field (e.g., "I want 3 replicas of this Pod," "This Service should point to Pods with label app=my-app").
- Act (or Reconcile): If there's a difference between the desired state and the actual state, the controller takes action to bring the actual state closer to the desired state. This might involve creating new objects, updating existing ones, deleting objects, or updating the status field of the object it's managing.

The goal is continuous convergence: to always drive the system towards the state you've declared. It's a declarative paradigm–you state _what_ you want, and the controllers figure out _how_ to achieve it and maintain it.
Think of it like a thermostat:

- Desired State (spec): You set the thermostat to 20°C.
- Observe: The thermostat measures the current room temperature (actual state).
- Compare: It compares the current temperature to 20°C.
- Act:
  - If too cold, it turns on the heating.
  - If too hot, it might turn on air conditioning (or in simpler systems, just turn off heating).
  - If just right, it does nothing. This loop runs continuously to maintain the desired temperature.

2\. Specifically: The Technical Implementation
Under the bonnet, the abstract control loop is implemented using several mechanisms, often facilitated by the client-go library:

- Watch Mechanism & Informers: Controllers don't constantly poll the API server for changes, as this would be inefficient and overload the API server. Instead, they use a "watch" mechanism.
  - Informers: An informer is a client-go component that watches for changes to specific resource Kinds (e.g., Pods, Deployments). When an object of that kind is created, updated, or deleted, the API server sends an event notification.
  - Shared Informers: Multiple controllers interested in the same resource Kind can use a shared informer. This means only one watch connection is established with the API server for that resource, and events are then distributed to all interested controllers.
  - Local Cache (Store): Informers maintain an in-memory cache of the objects they are watching. When a controller needs to get an object, it reads from this local cache, which is much faster and reduces load on the API server. The cache is kept synchronised with etcd by the watch events.
- Work Queues: When an informer receives an event (e.g., "Pod X was deleted," "Deployment Y's spec was updated"), it doesn't usually trigger the controller's reconciliation logic directly. Instead, it typically adds a key representing the affected object (e.g., "namespace/object-name") to a work queue.
  - Purpose of Work Queues:
    - Decoupling: Separates event detection from processing.
    - Rate Limiting: Prevents the controller from being overwhelmed by a flood of events.
    - Retries: If processing an item fails (e.g., due to a temporary network issue when trying to create a Pod), the item can be re-queued for a later attempt, often with exponential backoff.
    - Serialisation (per item): Ensures that changes related to a single object are processed one at a time, preventing race conditions for that specific object.
- Worker Routines & Reconciliation Logic: The controller has one or more worker routines (goroutines in Go) that continuously pull items from the work queue.
  - For each item (object key), the worker executes the controller's core reconciliation logic:
    1. Fetch the object: Get the latest version of the object from the informer's local cache using the key.
    2. Compare spec and status: Analyse the object's desired state (spec) and its current observed state (often reflected in its status or by querying related objects, like listing all Pods managed by a ReplicaSet).
    3. Perform actions:
       - If discrepancies are found, the controller makes API calls (e.g., create a new Pod, delete an old ReplicaSet, update a Service's endpoints).
       - It might also update the status subresource of the object it's managing (e.g., a Deployment controller updates status.availableReplicas).
  - This logic is highly specific to the controller's purpose. For example:
    - A ReplicaSet controller ensures the right number of Pods exist. If there are too few, it creates more. If too many, it deletes some.
    - A Deployment controller orchestrates ReplicaSets to achieve rolling updates or rollbacks.
    - A Node controller monitors node health and might evict Pods from failed nodes.
- Error Handling: Robust error handling is crucial. If an action fails, the item is usually re-queued. If an error is persistent, the controller might log it and move on, or give up after a certain number of retries.

Example Flow (Simplified ReplicaSet Controller):

1. Setup: ReplicaSet controller starts, creates an informer for ReplicaSet objects and Pod objects.
2. Event: User creates a ReplicaSet object with spec.replicas: 3\.
3. Informer: The ReplicaSet informer sees this new object and adds the key "\<namespace\>/my-replicaset" to the work queue.
4. Worker: A worker goroutine picks up the key.
5. Reconcile:
   - Fetches my-replicaset from its cache.
   - Lists all Pods that have my-replicaset as their ownerReference (also from its Pod cache). Let's say it finds 0 Pods.
   - Compares desired (3) vs. actual (0). Difference is \+3.
   - Makes API calls to create 3 new Pod objects, based on the template in my-replicaset.spec.
   - Updates my-replicaset.status.replicas to reflect the current state (e.g., 0 ready, 3 desired).
6. Later Event: One of the created Pods crashes.
7. Informer: The Pod informer sees the Pod deletion/failure event. Since the ReplicaSet controller is also watching Pods (especially those it owns), it might get an event for the Pod, or it will re-evaluate its ReplicaSets periodically or when they change. It adds "\<namespace\>/my-replicaset" to the work queue (because one of its managed Pods changed state).
8. Worker: Picks up "\<namespace\>/my-replicaset".
9. Reconcile:
   - Fetches my-replicaset.
   - Lists Pods–finds only 2 running.
   - Compares desired (3) vs. actual (2). Difference is \+1.
   - Makes an API call to create 1 new Pod.

This loop ensures that, over time, the actual state converges towards the desired state.

## Are Kubernetes Controllers Related to Cybernetics?

Yes, absolutely. Kubernetes controllers are a fantastic practical application of cybernetic principles.
Cybernetics, in essence, is the study of control and communication in complex systems, whether they are animals, organisations, or machines. It focuses on:

1. Goal-Oriented Behaviour: Systems that strive to achieve or maintain a specific goal or state.
2. Feedback Loops: The mechanism by which a system receives information about its current state or the effects of its actions, and uses this information to adjust its future behaviour.
3. Self-Regulation: The ability of a system to maintain stability and its desired state despite external disturbances.
4. Control Mechanisms: The components or processes within a system that exert influence to achieve the goal.
5. Communication: The flow of information necessary for feedback and control.

How Kubernetes Controllers Embody Cybernetic Principles:

- Goal-Oriented: Each Kubernetes controller has a clearly defined goal–to make the actual state of the resources it manages match the desired state (spec) defined by the user. The Deployment controller's goal is to have a certain number of application replicas running with a specific version.
- Feedback Loop: This is central to controller operation:
  - Sensor/Observation: The controller "senses" the actual state of the cluster by watching resources and reading their status fields.
  - Comparator: It compares this observed state with the desired state (spec).
  - Effector/Action: If there's a discrepancy, the controller takes corrective action (creates/updates/deletes resources).
  - The results of these actions (e.g., a new Pod becoming Ready, an old one being deleted) feed back into the "observed state," closing the loop. The status subresource of an object is a key part of this feedback.
- Self-Regulation/Homeostasis: Controllers work to maintain the system's equilibrium around the desired state. If a Pod dies unexpectedly (an external disturbance), the relevant controller (e.g., ReplicaSet) detects this and automatically creates a new one, restoring the desired number of replicas. This is akin to biological homeostasis, like the body maintaining a constant internal temperature.
- Control Mechanisms: The controllers themselves _are_ the control mechanisms of Kubernetes. They actively manipulate cluster resources to enforce the desired configurations.
- Communication: Controllers communicate extensively with the API server, which acts as the central nervous system and source of truth for the cluster. They send requests to modify resources and receive information about the current state.

So, the entire "observe \-\> compare \-\> act" reconciliation loop is a classic cybernetic control loop. Kubernetes uses these principles to automate the management of complex distributed applications, making them more resilient and self-healing. Norbert Wiener, one of the founders of cybernetics, would likely find Kubernetes a fascinating example of his theories in action in the digital realm.
