---
aliases: []
confidence: 
created: 2025-02-07T12:57:56Z
epistemic: 
id: Cert Handling in Mesh
ID: 12a
last_reviewed: 
modified: 2025-12-13T11:39:49Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy]
title: cert_handling_in_mesh
type: 
uid: 
updated: 
version: 
---

## Cert Handling in Mesh

How the service handles the certificates needed to communicate with the

### Configuration Loading

The service loads the necessary certificate information from environment variables or configuration files. This is evident in the config-loader.ts file, which includes entries for:

- meshClientCert
- meshClientKey
- meshHashSecret

### HTTPS Agent Configuration

In the server.ts file, an HTTPS agent is created with the loaded certificate information:

```javascript
const mailboxConfig = {
   httpClient: new AxiosClient({
      MESH_URI_INTEGRATION,
      MESH_BASE_URL,
      agent: new https.Agent({
	 cert: config.meshClientCert,
	 key: config.meshClientKey,
	 ca: NHS_PTL_ROOTCA_DATA,
	 rejectUnauthorized: false,
      }),
   }),
   headers: { Accept: 'application/vnd.mesh.v2+json' },
};
```

This agent is used to configure the HTTPS requests made to the MESH API.

Root CA Certificate:

   The service includes a root CA certificate (NHS_PTL_ROOTCA_DATA) which is loaded from a file:

```javascript
export const NHS_PTL_ROOTCA_DATA = fs.readFileSync(__dirname + '/../config/nhs-ptl-rootca.pem', 'utf8');
```

This root CA is used to verify the MESH API's server certificate.

### Request Configuration

When making requests to the MESH API, the service uses the configured HTTPS agent with the certificates. For example, in the send-request.ts file:

```javascript
const httpsAgent = new https.Agent({
   cert: config.meshClientCert,
   key: config.meshClientKey,
   ca: NHS_PTL_ROOTCA_DATA,
   rejectUnauthorized: false,
});
```

Axios, like many HTTP clients, uses the `https.Agent` in Node.js to manage HTTPS connections. The `https.Agent` is responsible for handling the details of the TLS/SSL connection, which includes managing certificates for secure communication. Here's why it's needed:

1. Certificate Management: When making HTTPS requests, the client needs to present a client certificate to authenticate itself to the server. The `https.Agent` allows you to specify the client certificate (`cert`), the private key (`key`), and any Certificate Authority (CA) certificates (`ca`) needed to establish a secure connection.
2. Secure Communication: HTTPS ensures that the data sent between the client and server is encrypted. The `https.Agent` handles the encryption and decryption of data, ensuring that the communication remains secure.
3. Verification of Server Identity: The `https.Agent` can be configured to verify the server's certificate against a list of trusted CAs. This helps prevent man-in-the-middle attacks by ensuring that the client is communicating with the legitimate server.
4. Connection Reuse: The `https.Agent` manages connection pooling and reuse, which can improve performance by reusing existing connections rather than establishing new ones for each request.

By configuring an `https.Agent` with the necessary certificates and keys, Axios can securely communicate with servers over HTTPS, ensuring both the integrity and confidentiality of the data being exchanged.

Setting `rejectUnauthorized` to `false` in an HTTPS agent configuration means that the client will not verify the server's SSL/TLS certificate against the list of trusted Certificate Authorities (CAs). This effectively disables the security feature that prevents man-in-the-middle attacks by ensuring the server is who it claims to be.

Here are some reasons why `rejectUnauthorized` might be set to `false`:

1. Development and Testing: During development or testing, developers might use self-signed certificates or work in environments where the server's certificate is not signed by a trusted CA. Disabling certificate verification can simplify testing in such scenarios.
2. Internal Networks: In some cases, within a secure internal network, the risk of man-in-the-middle attacks might be considered low, and certificate verification might be disabled for convenience.
3. Misconfiguration: Sometimes, it might be set to `false` due to oversight or misconfiguration, which can introduce security vulnerabilities.
4. Legacy Systems: Some legacy systems might not support proper certificate verification, leading developers to disable it to maintain compatibility.

However, it's important to note that setting `rejectUnauthorized` to `false` is generally not recommended for production environments, as it exposes the application to potential security risks. It's advisable to ensure that the server's certificate is properly signed by a trusted CA and to enable certificate verification by setting `rejectUnauthorized` to `true`.

### Local Development

For local development, the README file suggests setting environment variables for the certificate information:

```sh
export MESH_CLIENT_CERT=`cat ./mesh-client-cert.pem`
export MESH_CLIENT_KEY=`cat ./mesh-client-key.pem`
```

### Production Configuration

In a production environment, the service attempts to load the certificate information from specific file paths:

```json
{ filePath: '/certs/mesh-client-cert.pem', configType: 'text', propertyName: 'meshClientCert' },
{ filePath: '/certs/mesh-client-key.pem', configType: 'text', propertyName: 'meshClientKey' },
```

By handling the certificates in this manner, the service ensures secure communication with the MESH API while allowing for flexible configuration across different environments (local development, testing, production).

---

[12 MESH Service](<./12 MESH Service.md>)
