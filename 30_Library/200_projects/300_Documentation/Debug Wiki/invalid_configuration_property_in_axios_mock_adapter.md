---
aliases: []
confidence: 
created: 2025-02-07T12:57:53Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:42Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: invalid_configuration_property_in_axios_mock_adapter
type:
uid: 
updated: 
version:
---

## Configuration Error: Invalid Configuration Property in Axios Mock Adapter

### Error Classification

- Primary Category: Configuration Errors
- Subcategory: Invalid settings or parameters
- Severity Level: High
- Impact Scope: Local

### Description

The error message "Invalid config property 'Authorization' provided to onGet/onPost" indicates an issue with how the `Authorization` header is being set in the test setup using the `axios-mock-adapter` library. This library is designed to intercept and mock Axios requests within tests, but it has strict validation rules for the configuration properties allowed when defining mock responses.

The `Authorization` header is typically used for authentication purposes, and including it within the `config` object passed to `onGet` or `onPost` is not the correct approach with this library.

### Technical Details

- Error message: "Invalid config property 'Authorization' provided to onGet/onPost"
- Library: axios-mock-adapter
- Affected tests:
    - `src/infra/elasticsearch/__tests__/elasticsearch-client.test.ts`
    - `src/infra/elasticsearch/__tests__/ElasticSearchConnectionAdaptor.test.ts`

### Root Cause

The root cause is providing the `Authorization` header within the configuration object of the `onGet` or `onPost` methods of `axios-mock-adapter`. This library expects specific properties within this object, and `Authorization` is not one of them.

### Resolution

To resolve this, the `Authorization` header should be set as part of the mock request headers instead of the configuration object. Here's an example of how to correct this:

TypeScript

```sh
// Incorrect:
axiosAdaptor.onGet(getIndicesServiceUrl, {
    Authorization: 'Basic Y2xpbmljYWxVc2VyMTphYmNkMTIzNA==',
    Accept: 'application/json, text/plain, /',
    'Content-Type': 'application/json',
}).reply(200, mockGetIndicesResponse);

// Correct:
axiosAdaptor.onGet(getIndicesServiceUrl, undefined, {
    headers: {
        Authorization: 'Basic Y2xpbmljYWxVc2VyMTphYmNkMTIzNA==',
        Accept: 'application/json, text/plain, /',
        'Content-Type': 'application/json',
    },
}).reply(200, mockGetIndicesResponse);
```

By making this adjustment in the affected test files, the error should be resolved, and the tests should run as expected.

### Validation Checklist
