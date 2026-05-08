---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-08T12:53:43+00:00
title: Representational state transfer (REST) means an API follows the REST architectural style, and wor
---

Representational state transfer (REST) means an API follows the [REST architectural style](https://ics.uci.edu/\~fielding/pubs/dissertation/rest_arch_style.htm), and works with REST (sometimes called RESTful) web services. This can make the API easier to use and faster to integrate with.

REST principles are widely adopted, which means developers will understand your API more quickly. It also means you can use industry-standard ways of documenting your API, and off-the-shelf testing software.

When you're using the REST API style, you should follow the REST design principles:

- uniform interface–all API requests for the same resource should have the same uniform resource identifier (URI)
- client and server–these must be independent of each other
- statelessness–this means that all requests and responses are self-contained and include all necessary information, and that no server-side sessions are required because all session state is kept on the client side
- cacheable–resources should be cached on the client side and server side, to improve performance and scalability
- layered system–allows for components such as proxies, gateways and firewalls to be placed between the client and the server, to make the service more reliable and secure

Using REST is a good way to design an API, but other approaches such as [GraphQL](https://www.gov.uk/guidance/using-graphql-for-your-api) or [gRPC](https://grpc.io/) may still be a better choice for specific projects. For example, GraphQL is useful for prototyping services, when you're not sure what views of the data other developers will need.
