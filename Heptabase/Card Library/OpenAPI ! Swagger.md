## OpenAPI / Swagger

![](https://user-images.githubusercontent.com/20847995/79218686-7ba7b900-7e59-11ea-8a5e-676a83b9f86e.png)

This handler allows you to load remote or local [OpenAPI (2/3) and Swagger](https://swagger.io/) schemas. This work originated from IBM Research, and is currently maintained by GraphQL Mesh.

For migrating from version `< 0.32` see [migration guide](https://the-guild.dev/graphql/mesh/docs/migration/openapi-0.31-0.32)

You can import it using remote/local `.json` or `.yaml`.

To get started, install the handler library:

Now, you can use it directly in your Mesh config file / URL:

.meshrc.yaml

```
sources:
  - name: MyOpenapiApi
    handler:
      openapi:
        source: ./my-schema.json
```

Note that this handler is based on the [JSON Schema handler](https://the-guild.dev/graphql/mesh/docs/handlers/json-schema) - so it’s configurations will apply here as well.

## Overriding default Query/Mutation operations classification

By default, all GET operations will be placed into Query fields and all other operations into Mutation fields. with this option, you can manually override this process. To switch between Query and Mutation operations, and vice versa, you need to define a rule per override, consisting of the OAS title, the path of the operation, the method of the operation and finally, the destination type (e.g., Query or Mutation). See the example below:

.meshrc.yaml

```
sources:
  - name: MyOpenapiApi
    handler:
      openapi:
        source: ./my-schema.json
        selectQueryOrMutationField:
          - fieldName: 'add_weather_forecast' # OAS field name
            type: Query # switch method POST from default Mutation into Query
          - fieldName: 'get_weather_forecast' # OAS field name
            type: Mutation # switch method GET from default Query into Mutation
```

## Naming convention

We use `operationId` for the names, and aim to keep it as close as possible to origin.

### Type naming

We adjust `operationId` only when necessary according to the GraphQL spec: - Chars (white space), `.`, `/`, `:` and `-` are replaced with `_` (underscore) - Other chars which are not latin/digits are replaced with their char codes - If first char of the name is a digit, we prefix it with `_` (GraphQL spec doesn’t allow that)

### Unnamed types

We use path-based naming. So names could be structured like, for example,`query_getUsers_items_firstName`

## Headers

[Read about configuration and examples](https://the-guild.dev/graphql/mesh/docs/guides/headers)

## Advanced cookies handling

When building a web application, cookies are often used for authentication for security reasons. On the other end, mobile applications tend to use an HTTP header.

This section shows how to configure GraphQL Mesh to accept either and use GraphQL Mesh to set/unset cookies on the login & logout mutations.

### Accepting one of the cookies, header, or context value

We want to accept one of the following:

- an `accessToken` cookie

- an `Authorization` header

- an authorization value available in context (e.g. set by a GraphQL auth plugin)

And transmit it to the Rest API as an `Authorization` header. GraphQL Mesh does not allow dynamic selection in the `meshrc.yaml` file, but that’s fine! We can use a bit of trickery.

Here in the `meshrc.yaml` configuration we store the cookie in `Authorization-Cookie`, and the header in `Authorization-Header`. To introduce the logic needed to generate the proper `Authorization` header for the Rest API, we need to implement a `customFetch`. It will replace the `fetch` used by GraphQL Mesh to call the Rest API.

### Setting / Unsetting the cookie

Of course, using GraphQL Mesh as a Gateway for both the mobile application and web application is excellent. Still, there’s one thing missing: the setting of the cookie for the web application.

We need to access the HTTP response that is sent back to the client. Luckily, we can do so in `additionalResolvers`. So we need to create two new resolvers, one for login and one for logout, and manage the cookie in their code.

The first step is to edit the `meshrc.yaml` file, add this at the end:

Then manage the cookie in the new resolvers:

resolvers.ts

```
// lifespan of our cookie
const oneYear = 365 * 24 * 3600
 
const resolvers = {
  Mutation: {
    async login(root, args, context, info) {
      // Call the Rest API's login operation
      const result = await context.Rest.Mutation.accountLogin({
        root,
        args: {
          credentials: args.credentials
        },
        context,
        info
      })
      // if \`result\` contains a JWT token, you could instead decode it and set \`Expires\`
      // to the JWT token's expiration date
      context.res.set(
        'Set-Cookie',
        \`accessToken=${result}; Path=/; Secure; HttpOnly; Max-Age=${oneYear};\`
      )
 
      return result
    },
    logout(root, args, { res }) {
      // use old date to unset cookie
      res.set(
        'Set-Cookie',
        \`accessToken=logout; Path=/; Secure; HttpOnly; Expires=Thu, 1 Jan 1970 00:00:00 GMT;\`
      )
 
      return true
    }
  }
}
 
module.exports = { resolvers }
```

## Callbacks as Subscriptions

OpenAPI handler is able to process OAS Callbacks as GraphQL Subscriptions. It uses your PubSub implementation to consume the data. But you have to define webhooks for individual callbacks to make it work.

See [Subscriptions & Webhooks](https://the-guild.dev/graphql/mesh/docs/guides/subscriptions-webhooks) to create an endpoint to consume a webhook. You should use the callback url as `pubSubTopic` in the webhook configuration.

Also see our example;[Subscriptions Example with Webhooks](https://codesandbox.io/s/github/ardatan/graphql-mesh/tree/master/examples/openapi-subscriptions).

GraphQL Mesh supports loading the sources from a CDN or schema registry. You can use the `source` property to load the schema from a CDN or schema registry.

## Examples

We have a lot of examples for OpenAPI Handler;

- [JavaScript Wiki](https://codesandbox.io/s/github/ardatan/graphql-mesh/tree/master/examples/openapi-javascript-wiki)

- [Location Weather](https://codesandbox.io/s/github/ardatan/graphql-mesh/tree/master/examples/openapi-location-weather)

- [StackExchange](https://codesandbox.io/s/github/ardatan/graphql-mesh/tree/master/examples/openapi-stackexchange)

- [Stripe](https://codesandbox.io/s/github/ardatan/graphql-mesh/tree/master/examples/openapi-stripe)

- [Subscriptions Example with Webhooks](https://codesandbox.io/s/github/ardatan/graphql-mesh/tree/master/examples/openapi-subscriptions)

- [YouTrack](https://codesandbox.io/s/github/ardatan/graphql-mesh/tree/master/examples/openapi-youtrack)

## Config API Reference

- `source` (type: `String`, required) - A pointer to your API source (Support both JSON and YAML) - could be a local file, remote file or url endpoint

- `fallbackFormat` (type: `String (json | yaml | js | ts)`) - Format of the files referenced from the source file, for cases content type isn’t detected automatically

- `endpoint` (type: `String`) - Specifies the URL on which all paths will be based on. Overrides the server object in the OAS.

- `schemaHeaders` (type: `JSON`) - If you are using a remote URL endpoint to fetch your schema, you can set headers for the HTTP request to fetch your schema.

- `operationHeaders` (type: `JSON`) - JSON object representing the Headers to add to the runtime of the API calls

- `ignoreErrorResponses` (type: `Boolean`) - Responses are converted to a Union type grouping all possible responses. Applying this will ignore all responses with status code other than 2xx, resulting in simpler response types, usualy regular object type instead of union. Default: false

- `selectQueryOrMutationField` (type: `Array of Object`) - Allows to explicitly override the default operation (Query or Mutation) for any OAS operation:

   - `type` (type: `String (query | mutation | Query | Mutation)`, required)

   - `fieldName` (type: `String`, required)

- `queryParams` (type: `JSON`) - JSON object representing the query search parameters to add to the API calls

- `timeout` (type: `Int`) - Timeout for the HTTP request in milliseconds

Last updated on

[GraphQL](https://the-guild.dev/graphql/mesh/docs/handlers/graphql "GraphQL") [Federation Supergraph](https://the-guild.dev/graphql/mesh/docs/handlers/supergraph "Federation Supergraph")

The action has been successful

Questions? Chat with us!Support is online Chat with The Guild