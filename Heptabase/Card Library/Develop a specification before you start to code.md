### Develop a specification before you start to code

The [OpenAPI Specification](https://swagger.io/specification/) is a standardised way of describing RESTful web APIs, and [is recommended](https://www.gov.uk/government/publications/recommended-open-standards-for-government/describing-restful-apis-with-openapi-3) by the government Open Standards Board.

It allows you to produce a file (the OpenAPI document) which is both machine and human readable, and which describes the format and responses of your API.

A good principle is to produce an OpenAPI document as the first output of your design process, and then develop the document along with the API design.

This will help to:

- show the API has been developed consistently with others from your organisation

- test the API against rules and for security issues [using a software linter](https://owasp.org/www-project-devsecops-guideline/latest/01b-Linting-Code#:\~:text=Linting%20is%20the%20automated%20checking,\\(otherwise%20known%20as%20linter\\).)

- generate reference documentation automatically – documentation generated in this way should be [supported by further resources](https://www.gov.uk/guidance/how-to-document-apis)

For non-REST APIs like GraphQL, you should still look to produce a specification during the design process. For example, for GraphQL this would be a GraphQL schema specification defining the types available, queries, mutations and the relationships between them.