---
captured: "2026-03-02T13:58:17+00:00 2026-03-02T13:58:17+00:00"
created: 2026-03-02T13:58:20+00:00
modified: 2026-03-14T11:10:39+00:00
source: "https://claude.ai/chat/4f532e64-bf46-4818-9ac6-8d2f7ed9bf35"
status: "processing"
tags: ["input"]
title: HEAD GitLab CLI authentication with expired token
type: "head"
---

## Raw Output / Content

I am trying to authenticate to gitlab with the cli GET [https://gitlab.com/api/v4/user](https://gitlab.com/api/v4/user): 401 {error: invalid\_token}, {error\_description: Token is expired. You can either do re-authorization or token refresh.} │ │ with provider\["registry.terraform.io/gitlabhq/gitlab"\], │ on providers.tf line 5, in provider "gitlab": │ 5: provider "gitlab" { │ ╵ …/mkuh-prod-2 on  main!? on ⛵ fitfile-cloud-prod-1-aks-cluster-admin () on ☁️ FitFileLZ on 🅰 (eu-west-2) at 15:35:12 ❯ glab auth Manage glab's authentication state. USAGE glab auth <command> \[command\] \[--flags\] COMMANDS configure-docker Register glab as a Docker credential helper docker-helper A Docker credential helper for GitLab container registries dpop-gen \[--flags\] Generates a DPoP (demonstrating-proof-of-possession) proof JWT. (EXPERIMENTAL) login \[--flags\] Authenticate with a GitLab instance. logout \[--flags\] Logout from a GitLab instance. status \[--flags\] View authentication status. FLAGS -h --help Show help for this command. …/mkuh-prod-2 on  main!? on ⛵ fitfile-cloud-prod-1-aks-cluster-admin () on ☁️ FitFileLZ on 🅰 (eu-west-2) at 15:35:23 ❯ glab auth login --hostname gitlab.com - Signing into gitlab.com WARNING: One of GITLAB\_TOKEN, GITLAB\_ACCESS\_TOKEN, OAUTH\_TOKEN environment variables is set. If you don't want to use it for glab, unset it. The minimum required scopes are 'api' and 'write\_repository'. Generate a personal access token at [https://gitlab.com/-/user\_settings/personal\_access\_tokens?scopes=api,write\_repository](https://gitlab.com/-/user_settings/personal_access_tokens?scopes=api,write_repository) ┃ Paste your authentication token: Cancelled. ERROR Could not prompt: user cancelled. …/mkuh-prod-2 on  main!? on ⛵ fitfile-cloud-prod-1-aks-cluster-admin () on ☁️ FitFileLZ on 🅰 (eu-west-2) at 15:35:45 ❯ glab auth login --hostname gitlab.com - Signing into gitlab.com WARNING: One of GITLAB\_TOKEN, GITLAB\_ACCESS\_TOKEN, OAUTH\_TOKEN environment variables is set. If you don't want to use it for glab, unset it. - glab config set -h gitlab.com git\_protocol ssh ✓ Configured Git protocol. - glab config set -h gitlab.com api\_protocol https ✓ Configured API protocol. ERROR Error using API: GET [https://gitlab.com/api/v4/user](https://gitlab.com/api/v4/user): 401 {error: invalid\_token}, {error\_description: Token is expired. You can either do re-authorization or token refresh.}. What am I doing wrong? I want to get the token to use

---

The issue is clear from the warning message: an environment variable (`GITLAB_TOKEN`, `GITLAB_ACCESS_TOKEN`, or `OAUTH_TOKEN`) is set with an expired token, and it's taking precedence over whatever glab is trying to do.

---

This is not working and the var is empty export GITLAB\_TOKEN=$(glab auth status -t 2>/dev/null || echo "YOUR\_GITLAB\_TOKEN\_HERE") How do I get the token now it worked

---

---

export GITLAB\_TOKEN=$(glab auth status -t 2>&1 | grep "Token:" | awk '{print $NF}') …/mkuh-prod-2 on  main!? on ⛵ fitfile-cloud-prod-1-aks-cluster-admin () on ☁️ FitFileLZ on 🅰 (eu-west-2) at 15:39:27 ❯ echo $GITLAB\_TOKEN …/mkuh-prod-2 on  main!? on ⛵ fitfile-cloud-prod-1-aks-cluster-admin () on ☁️ FitFileLZ on 🅰 (eu-west-2) at 15:39:30 ❯ glab auth status -t 2>&1 | grep "Token:" | awk '{print $NF}' …/mkuh-prod-2 on  main!? on ⛵ fitfile-cloud-prod-1-aks-cluster-admin () on ☁️ FitFileLZ on 🅰 (eu-west-2) at 15:39:40 ❯ cat ~/.config/glab-cli/config.yml # What protocol to use when performing Git operations. Supported values: ssh, https. git\_protocol: ssh # What editor glab should run when creating issues, merge requests, etc. This global config cannot be overridden by hostname. editor: # What browser glab should run when opening links. This global config cannot be overridden by hostname. browser: # Set your desired Markdown renderer style. Available options are \[dark, light, notty\]. To set a custom style, refer to [https://github.com/charmbracelet/glamour#styles](https://github.com/charmbracelet/glamour#styles) glamour\_style: dark # Allow glab to automatically check for updates and notify you when there are new updates. check\_update: true # Whether or not to display hyperlink escape characters when listing items like issues or merge requests. Set to TRUE to display hyperlinks in TTYs only. Force hyperlinks by setting FORCE\_HYPERLINKS=1 as an environment variable. display\_hyperlinks: false # Default GitLab hostname to use. host: gitlab.com # Set to true (1) to disable prompts, or false (0) to enable them. no\_prompt: false # Configuration specific for GitLab instances. hosts: gitlab.com: # What protocol to use to access the API endpoint. Supported values: http, https. api\_protocol: https # Configure host for API endpoint. Defaults to the host itself. api\_host: gitlab.com # Your GitLab access token. To get one, read [https://docs.gitlab.com/ee/user/profile/personal\_access\_tokens.html](https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html) token:!!null 0577c55051464a9ba066a9459b6… git\_protocol: ssh user: leontormes container\_registry\_domains: gitlab.com,gitlab.com:443,registry.gitlab.com is\_oauth2: "true" oauth2\_refresh\_token: 8489d16f43f8a93e5… oauth2\_expiry\_date: 23 Feb 26 17:38 GMT last\_update\_check\_timestamp: "2026-02-23T15:16:02Z" I have redacted the actual tokens.

---

The token is there but stored with `!!null` prefix which is weird. But the key issue is that `is_oauth2: "true"`—this is an OAuth2 token that expires (expiry is `23 Feb 26 17:38 GMT`—that's today, about 2 hours from now). The grep didn't work because the output format doesn't match "Token:".

Let me help them extract the token properly.

---

echo $GITLAB\_TOKEN 0577c55051464a9ba066a9459b6370b80….. 8489d16f43f8a93e5162d2c712548ccb….. Has 2 tokens in it

---

The grep is picking up both the `token:` and `oauth2_refresh_token:` lines. Need to be more specific.

---

---
