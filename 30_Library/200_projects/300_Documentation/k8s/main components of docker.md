---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:42Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [containers]
title: main components of docker
type:
uid: 
updated: 
version:
---

what are the main components of docker

Docker is composed of several key components that work together to create and manage containerized applications. The main components of Docker are:

## Docker Engine

The Docker Engine is the core of the Docker platform, consisting of three primary elements:

1. Docker Daemon (dockerd): This is the background service that manages Docker objects such as images, containers, networks, and volumes[1][4].
2. Docker Client: The command-line interface (CLI) that allows users to interact with Docker through commands like `docker build`, `docker pull`, and `docker run`[1][5].
3. REST API: Enables communication between the Docker client and the Docker daemon[4][7].

## Docker Objects

Docker utilizes various objects to run applications:

1. Docker Images: Read-only templates used to create containers. They contain the application code, runtime, libraries, and dependencies needed to run an application[5][7].
2. Docker Containers: Runnable instances of Docker images. They are isolated environments that encapsulate the application and its dependencies[1][5].
3. Docker Networks: Allow containers to communicate with each other and with the external world[5][8].
4. Docker Volumes: Provide persistent storage for data generated and used by Docker containers[5][8].

## Docker Registry

The Docker Registry is a storage and distribution system for Docker images:

1. Docker Hub: The default public registry where Docker looks for images[5][6].
2. Private Registries: Can be set up to store and share images within an organization[6].

## Additional Components

1. Docker Compose: A tool for defining and running multi-container Docker applications[4].
2. Docker Host: The machine on which the Docker daemon runs and containers are executed[5][6].
3. Container Runtime: The software responsible for running containers. Docker uses containerd by default[3].

These components work together to provide the full Docker experience, from building and sharing images to running and managing containers across various environments.

Citations:

[1] Docker 101: The Docker Components - Sysdig <https://sysdig.com/learn-cloud-native/docker-101-the-docker-components/>

[2] Docker Architecture - Javatpoint <https://www.javatpoint.com/docker-architecture>

[3] Docker Architecture Overview - Structure & Components - Spacelift <https://spacelift.io/blog/docker-architecture>

[4] What is Docker? <https://docs.docker.com/get-started/docker-overview/>

[5] Understanding Docker Components :Complete Guide 2025 <https://thinksys.com/devops/docker-components/>

[6] DOCKER AND ITS COMPONENTS - LinkedIn <https://www.linkedin.com/pulse/docker-its-components-bhavishay-sikka>

[7] What is Docker architecture? | Sysdig <https://sysdig.com/learn-cloud-native/what-is-docker-architecture/>

[8] Docker Architecture | Docker Resource Isolation | Lifecycle <https://k21academy.com/docker-kubernetes/docker-architecture-docker-engine-components-container-lifecycle/>

[9] Architecture of Docker - GeeksforGeeks <https://www.geeksforgeeks.org/architecture-of-docker/>

can I call the rest API directly using other tools like curl or postman

Yes, you can call Docker's REST API directly using tools like cURL or Postman. This provides a way to interact with Docker without using the Docker CLI, which can be useful for debugging, automation, or learning about Docker's internals.

## Using cURL

To use cURL with Docker's API:

1. Ensure you have cURL version 7.40 or later, which supports the `--unix-socket` flag[4].
2. Use the following command structure:

```bash
curl --unix-socket /var/run/docker.sock http:/v1.41/<endpoint>
```

   Replace `<endpoint>` with the specific API endpoint you want to access[1][5].

3. For example, to get Docker version information:

```bash
curl --silent --unix-socket /var/run/docker.sock http://v1.41/version
```

## Using Postman

Postman can also be used to interact with Docker's API:

1. Import the cURL command into Postman:
   - Open Postman and select "Import"
   - Paste your cURL command
   - Postman will automatically convert it to a request[2]

2. Alternatively, you can manually set up the request in Postman:
   - Set the request type (GET, POST, etc.)
   - Enter the API endpoint URL
   - Add necessary headers and body content

3. For Docker API requests, you'll need to use Postman's socket connection feature, which may require additional configuration.

## Important Considerations

- The Docker API version may change. Use the appropriate version in your requests (e.g., v1.41)[5].
- When using cURL, the hostname in the URL (e.g., `http://localhost`) is not important for Unix socket connections[1].
- For security reasons, the Docker API is often only accessible via a Unix socket by default. Exposing it over TCP requires additional configuration and security measures.

By using these tools, you can directly interact with Docker's API, providing more flexibility and control over your Docker environment compared to using the standard Docker CLI.
