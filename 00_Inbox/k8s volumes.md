---
created: 2026-01-24T09:33:17+00:00
modified: 2026-01-24T09:33:25+00:00
title: k8s volumes
---

In Kubernetes, volumes provide a way for containers within a pod to access shared storage, ensuring data persistence across container restarts and facilitating data sharing between containers. Kubernetes supports various volume types, each tailored to specific use cases:

1. emptyDir

An emptyDir volume is created when a pod is assigned to a node and exists as long as that pod is running on that node. It's initially empty and is often used for temporary storage needs, such as caching or scratch space. The data in an emptyDir volume is deleted permanently when the pod is removed from the node.

Example configuration:

apiVersion: v1

kind: Pod

metadata:

  name: example-pod

spec:

  containers:

  - name: app-container
    image: nginx
    volumeMounts:
    - mountPath: /tmp
      name: temp-storage
  volumes:
  - name: temp-storage
    emptyDir: {}

1. hostPath

A hostPath volume mounts a file or directory from the host node's filesystem into a pod. This is useful for scenarios where containers need access to specific files or directories on the host machine. However, using hostPath requires caution, as it can expose the host filesystem to the pod, potentially leading to security risks.

Example configuration:

apiVersion: v1

kind: Pod

metadata:

  name: hostpath-pod

spec:

  containers:

  - name: app-container
    image: nginx
    volumeMounts:
    - mountPath: /host-data
      name: host-storage
  volumes:
  - name: host-storage
    hostPath:
      path: /data
      type: Directory

1. nfs

An nfs (Network File System) volume allows an existing NFS share to be mounted into a pod. This is beneficial for sharing data across multiple pods or even across different nodes. The data in an nfs volume is not erased when the pod is removed, as it resides on the NFS server.

Example configuration:

apiVersion: v1

kind: Pod

metadata:

  name: nfs-pod

spec:

  containers:

  - name: app-container
    image: nginx
    volumeMounts:
    - mountPath: /mnt/nfs
      name: nfs-storage
  volumes:
  - name: nfs-storage
    nfs:
      server: nfs-server.example.com
      path: /exported/path

1. configMap

A configMap volume is used to inject configuration data into pods. This allows you to decouple configuration artifacts from image content, making applications more portable.

Example configuration:

apiVersion: v1

kind: Pod

metadata:

  name: configmap-pod

spec:

  containers:

  - name: app-container
    image: nginx
    volumeMounts:
    - mountPath: /etc/config
      name: config-volume
  volumes:
  - name: config-volume
    configMap:
      name: my-config

1. secret

A secret volume is similar to a configMap but is specifically designed to hold sensitive information, such as passwords or tokens. Kubernetes ensures that secret data is stored securely and is only accessible to authorized pods.

Example configuration:

apiVersion: v1

kind: Pod

metadata:

  name: secret-pod

spec:

  containers:

  - name: app-container
    image: nginx
    volumeMounts:
    - mountPath: /etc/secret
      name: secret-volume
  volumes:
  - name: secret-volume
    secret:
      secretName: my-secret

1. persistentVolumeClaim

A persistentVolumeClaim (PVC) is a request for storage by a user. It abstracts the underlying storage implementation, allowing users to request storage resources without needing to know the details of the storage provider. PVCs are used in conjunction with persistentVolume (PV) resources, which represent actual storage volumes in the cluster.

Example configuration:

apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-example
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 10Gi
---

apiVersion: v1

kind: Pod

metadata:

  name: pvc-pod

spec:

  containers:

  - name: app-container
    image: nginx
    volumeMounts:
    - mountPath: /mnt/storage
      name: pvc-storage
  volumes:
  - name: pvc-storage
    persistentVolumeClaim:
      claimName: pvc-example

In this example, a PVC named pvc-example requests 10Gi of storage. The pod pvc-pod then mounts this storage at /mnt/storage.

When configuring volumes in Kubernetes manifests, it's essential to choose the appropriate volume type based on your application's requirements, considering factors like data persistence, security, and scalability.
