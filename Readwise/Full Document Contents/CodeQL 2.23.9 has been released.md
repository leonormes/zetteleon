---
created: 2026-03-14T09:49:43+00:00
modified: 2026-03-14T11:09:44+00:00
tags: [articles]
title: CodeQL 2.23.9 has been released
---

## CodeQL 2.23.9 Has Been Released

![rw-book-cover](https://github.blog/wp-content/uploads/2025/12/CodeQL-release-update.png)

### Metadata

- Author: [[The GitHub Blog]]
- Full Title: CodeQL 2.23.9 has been released
- Category: articles
- Summary: GitHub has released CodeQL version 2.23.9 with no user-facing changes. Support for Kotlin 1.6 and 1.7 will end in version 2.24.1, requiring Kotlin 1.8 or later. The update is automatically available on GitHub code scanning and will come to GitHub Enterprise Server soon.
- URL: <https://github.blog/changelog/2026-01-20-codeql-2-23-9-has-been-released/>

### Full Document

![](https://github.blog/wp-content/themes/github-2021-child/assets/img/featured-v3-improvements.svg)

CodeQL is the static analysis engine behind [GitHub code scanning](https://docs.github.com/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql), which finds and remediates security issues in your code. We've recently released [CodeQL 2.23.9](https://codeql.github.com/docs/codeql-overview/codeql-changelog/codeql-cli-2.23.9/). There are no user-facing changes to the CodeQL CLI nor any query changes, but we are posting this changelog to acknowledge that 2.23.9 has been released.

Support for Kotlin versions 1.6 and 1.7 has been deprecated and will be removed in CodeQL 2.24.1, planned for release in February 2026. Starting with that version, you'll need to use Kotlin 1.8 or later to extract Kotlin databases.

Every new version of CodeQL is automatically deployed to users of GitHub code scanning on github.com. The new functionality in CodeQL 2.23.9 will also be included in a future GitHub Enterprise Server (GHES) release. If you use an older version of GHES, you can [manually upgrade your CodeQL version](https://docs.github.com/enterprise-server@3.19/admin/managing-code-security/managing-github-advanced-security-for-your-enterprise/configuring-code-scanning-for-your-appliance#configuring-codeql-analysis-on-a-server-without-internet-access).
