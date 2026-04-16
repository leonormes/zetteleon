---
title: "martinbaillie/vault-plugin-secrets-github: Create ephemeral, finely-scoped @github access tokens using @hashicorp Vault."
source: "https://github.com/martinbaillie/vault-plugin-secrets-github"
captured: "2026-04-14T16:20:55+01:00 2026-04-14T16:20:55+01:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
## Vault Plugin Secrets GitHub

- [About](#about)
	- [Why?](#why)
		- [What?](#what)
		- [How?](#how)
- [Installation](#installation)
- [API](#api)
- [Development](#development)
	- [Tests](#tests)
- [Security](#security)

## About

Are you using HashiCorp Vault and GitHub in your organisation? Do you want ephemeral, finely-scoped GitHub tokens? If so, this plugin might be for you.

> UPDATE: The plugin was recently demoed at HashiCorp’s [Hashitalks 2021](https://www.youtube.com/watch?v=JuzBolDyGdg&t=17308s).

## Why?

Performing automation against GitHub APIs often neccessitates the creation of [OAuth Tokens](https://help.github.com/en/github/extending-github/git-automation-with-oauth-tokens). These tokens are tied to a user account, have *very* [coarsely-scoped permissions](https://developer.github.com/apps/building-oauth-apps/understanding-scopes-for-oauth-apps/#available-scopes) and do not expire.

As an organisation owner this likely means your automation-savvy users have created personal access tokens with powerful permissions which are being neither rotated nor deleted.

You will also commonly have wasted at least one of your GitHub seats on a [robot/machine user](https://help.github.com/en/github/getting-started-with-github/types-of-github-accounts#personal-user-accounts) for CI/CD purposes. These users share a similar access token and SSH key story as your human users do, and additonally need their credentials managed and rotated for them (arguably made more awkward when authenticating through an IdP).

[GitHub Apps](https://developer.github.com/apps/building-github-apps/) offer a better approach to this automation problem:

- They do not consume a seat (license) nor need credential management.
- They have *much* finer-grained [permissions](https://developer.github.com/v3/apps/permissions/) available to the access tokens.
- The tokens they issue expire after one hour.

However, GitHub Apps require the management of at least one private key which is needed to mint the JWTs used for the [App installation authentication](https://developer.github.com/apps/building-github-apps/authenticating-with-github-apps/#authenticating-as-an-installation) token request flow.

## What?

This plugin allows you to take advantage of your existing Vault deployment’s durable storage backend to protect the GitHub App private key, and your enabled Vault authN/Z mechanisms and highly-available API to perform the GitHub App token request flow on behalf of your users.

## How?

The Vault plugin acts as an intermediary for a GitHub App that you install into your organisation:

[![vault_github_plugin.png](https://github.com/martinbaillie/vault-plugin-secrets-github/raw/master/vault_github_plugin.png)](https://github.com/martinbaillie/vault-plugin-secrets-github/blob/master/vault_github_plugin.png)

Users login using your existing Vault auth backend(s) and, Vault RBAC permitting, can request GitHub tokens from the plugin. The plugin, in turn, authenticates with the GitHub App and requests a token on behalf of the user. This flow is better explained in the sequence diagram below:

[![https://mermaid.ink/img/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gICAgcGFydGljaXBhbnQgVSBhcyBVc2VyXG4gICAgcGFydGljaXBhbnQgViBhcyBWYXVsdFxuICAgIHBhcnRpY2lwYW50IEcgYXMgR2l0SHViXG4gICAgTm90ZSBvdmVyIFU6IEh1bWFuLCBDSS9DRCBhZ2VudCBldGMuXG4gICAgVS0+PlY6IFBPU1QgeW91ci52YXVsdC5vcmcvdjEvYXV0aFxuICAgIGFjdGl2YXRlIFZcbiAgICBOb3RlIG92ZXIgVjogU1NPLCBBRCwgQ2xvdWQgSUFNIGV0Yy5cbiAgICBWLS0+PlU6IE9LXG4gICAgZGVhY3RpdmF0ZSBWXG4gICAgTm90ZSByaWdodCBvZiBVOiBSZXF1ZXN0IGEgR2l0SHViIHRva2VuXG4gICAgYWx0XG4gICAgVS0+PlY6IFBPU1QgeW91ci52YXVsdC5vcmcvdjEvZ2l0aHViL3Rva2VuXG4gICAgZWxzZSByZXBvczogWzEyMyw0NTZdLCBwZXJtczogXCJpc3N1ZXM6d3JpdGVcIlxuICAgIFUtPj5WOiBQT1NUIHlvdXIudmF1bHQub3JnL3YxL2dpdGh1Yi90b2tlblxuICAgIGVuZFxuICAgIGFjdGl2YXRlIFZcbiAgICBOb3RlIG92ZXIgVjogTWludCBKV1QgdXNpbmcgUHJpdmF0ZSBLZXlcbiAgICBWLT4+VjogR2l0SHViIEpXVCAoZXhwOiAxMG0pXG4gICAgVi0+Pkc6IFBPU1QgYXBpLmdpdGh1Yi5jb20vLi4uL2FjY2Vzc190b2tlbnNcbiAgICBHLS0+PlY6IHRva2VuOiBbIFwidjEuMTIzNDU2Nzg5Li4uXCIgZXhwOiBcIjFoXCIgXVxuICAgIFYtPj5WOiBSZWNvcmQgbWV0cmljcywgbG9nc1xuICAgIFYtLT4+VTogWyB0b2tlbjogXCJ2MS4xMjM0NTY3ODkuLi5cIiBleHA6IFwiMWhcIiBdXG4gICAgZGVhY3RpdmF0ZSBWXG4gICAgTm90ZSBvdmVyIFU6IFVzZSBhY2Nlc3MgdG9rZW4gb24gR2l0SHViXG4gICAgYWx0IE9wZXJhdGUgb24gcmVwb3N0b3JpZXMgYWNjZXNzIHRva2VuIGhhcyBwZXJtaXNzaW9ucyBvblxuICAgIFUtPj5HOiAkIGdpdCBjbG9uZSBodHRwczovL3gtYWNjZXNzLXRva2VuOnYxLjEyMzQ1Njc4OS4uLkBnaXRodWIuY29tL29yZy9yZXBvLmdpdFxuICAgIGVsc2UgUGVyZm9ybSBBUEkgcmVxdWVzdHMgYWdhaW5zdCByZXNvdXJjZXMgYWNjZXNzIHRva2VuIGhhcyBwZXJtaXNzaW9ucyBvblxuICAgIFUtPj5HOiAkIGN1cmwgLUggXCJBdXRob3JpemF0aW9uOiBCZWFyZXIgdjEuMTIzNDU2Nzg5Li4uXCIgaHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXNvdXJjZVxuICAgIGVuZCIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0Iiwic2VxdWVuY2UiOnsibWlycm9yQWN0b3JzIjpmYWxzZSwiYWN0b3JNYXJnaW4iOjEyMCwibm90ZU1hcmdpbiI6MTAsIm1lc3NhZ2VNYXJnaW4iOjMwLCJib3hUZXh0TWFyZ2luIjoxLCJoZWlnaHQiOjMwLCJ3aWR0aCI6MjAwfX19?nothing.svg](https://camo.githubusercontent.com/a2cdb53f9e17ed922e628c4ca27aa6db9cffb23f953c60108d15a05431006892/68747470733a2f2f6d65726d6169642e696e6b2f696d672f65794a6a6232526c496a6f696332567864575675593256456157466e636d467458473467494341676347467964476c6a61584268626e516756534268637942566332567958473467494341676347467964476c6a61584268626e5167566942686379425759585673644678754943416749484268636e527059326c77595735304945636759584d6752326c30534856695847346749434167546d39305a534276646d56794946553649456831625746754c43424453533944524342685a3256756443426c64474d7558473467494341675653302b506c5936494642505531516765573931636935325958567364433576636d6376646a45765958563061467875494341674947466a64476c325958526c49465a63626941674943424f6233526c494739325a584967566a6f6755314e504c4342425243776751327876645751675355464e494756305979356362694167494342574c53302b506c55364945394c58473467494341675a47566859335270646d46305a5342575847346749434167546d39305a5342796157646f644342765a6942564f6942535a5846315a584e304947456752326c3053485669494852766132567558473467494341675957783058473467494341675653302b506c5936494642505531516765573931636935325958567364433576636d6376646a45765a326c30614856694c3352766132567558473467494341675a57787a5a5342795a584276637a6f67577a45794d7977304e545a644c4342775a584a74637a6f6758434a7063334e315a584d3664334a7064475663496c78754943416749465574506a35574f69425154314e5549486c7664584975646d46316248517562334a6e4c3359784c32647064476831596939306232746c626c787549434167494756755a467875494341674947466a64476c325958526c49465a63626941674943424f6233526c494739325a584967566a6f6754576c756443424b5631516764584e70626d636755484a70646d46305a53424c5a586c6362694167494342574c54342b566a6f6752326c3053485669494570585643416f5a5868774f6941784d47307058473467494341675669302b506b63364946425055315167595842704c6d6470644768315969356a623230764c6934754c32466a5932567a633139306232746c626e4e6362694167494342484c53302b506c593649485276613256754f69426249467769646a45754d54497a4e4455324e7a67354c693475584349675a5868774f694263496a466f58434967585678754943416749465974506a35574f6942535a574e76636d516762575630636d6c6a637977676247396e6331787549434167494659744c54342b56546f67577942306232746c626a6f6758434a324d5334784d6a4d304e5459334f446b754c6935634969426c65484136494677694d5768634969426458473467494341675a47566859335270646d46305a5342575847346749434167546d39305a534276646d5679494655364946567a5a53426859324e6c63334d67644739725a5734676232346752326c3053485669584734674943416759577830494539775a584a686447556762323467636d567762334e3062334a705a584d6759574e6a5a584e7a494852766132567549476868637942775a584a7461584e7a6157397563794276626c78754943416749465574506a35484f69416b494764706443426a624739755a53426f64485277637a6f764c33677459574e6a5a584e7a4c585276613256754f6e59784c6a45794d7a51314e6a63344f5334754c6b426e6158526f64574975593239744c3239795a7939795a5842764c6d647064467875494341674947567363325567554756795a6d39796253424255456b67636d56786457567a64484d67595764686157357a644342795a584e7664584a6a5a584d6759574e6a5a584e7a494852766132567549476868637942775a584a7461584e7a6157397563794276626c78754943416749465574506a35484f69416b49474e31636d77674c55676758434a426458526f62334a70656d4630615739754f6942435a5746795a584967646a45754d54497a4e4455324e7a67354c693475584349676148523063484d364c79396863476b755a326c30614856694c6d4e76625339795a584e7664584a6a5a56787549434167494756755a434973496d316c636d3168615751694f6e73696447686c625755694f694a6b5a575a6864577830496977696332567864575675593255694f6e736962576c79636d397951574e3062334a7a496a706d5957787a5a53776959574e3062334a4e59584a6e615734694f6a45794d437769626d39305a553168636d6470626949364d544173496d316c63334e685a32564e59584a6e615734694f6a4d774c434a69623368555a586830545746795a326c75496a6f784c434a6f5a576c6e614851694f6a4d774c434a3361575230614349364d6a4177665831393f6e6f7468696e672e737667)](https://mermaid-js.github.io/mermaid-live-editor/#/view/eyJjb2RlIjoic2VxdWVuY2VEaWFncmFtXG4gICAgcGFydGljaXBhbnQgVSBhcyBVc2VyXG4gICAgcGFydGljaXBhbnQgViBhcyBWYXVsdFxuICAgIHBhcnRpY2lwYW50IEcgYXMgR2l0SHViXG4gICAgTm90ZSBvdmVyIFU6IEh1bWFuLCBDSS9DRCBhZ2VudCBldGMuXG4gICAgVS0+PlY6IFBPU1QgeW91ci52YXVsdC5vcmcvdjEvYXV0aFxuICAgIGFjdGl2YXRlIFZcbiAgICBOb3RlIG92ZXIgVjogU1NPLCBBRCwgQ2xvdWQgSUFNIGV0Yy5cbiAgICBWLS0+PlU6IE9LXG4gICAgZGVhY3RpdmF0ZSBWXG4gICAgTm90ZSByaWdodCBvZiBVOiBSZXF1ZXN0IGEgR2l0SHViIHRva2VuXG4gICAgYWx0XG4gICAgVS0+PlY6IFBPU1QgeW91ci52YXVsdC5vcmcvdjEvZ2l0aHViL3Rva2VuXG4gICAgZWxzZSByZXBvczogWzEyMyw0NTZdLCBwZXJtczogXCJpc3N1ZXM6d3JpdGVcIlxuICAgIFUtPj5WOiBQT1NUIHlvdXIudmF1bHQub3JnL3YxL2dpdGh1Yi90b2tlblxuICAgIGVuZFxuICAgIGFjdGl2YXRlIFZcbiAgICBOb3RlIG92ZXIgVjogTWludCBKV1QgdXNpbmcgUHJpdmF0ZSBLZXlcbiAgICBWLT4+VjogR2l0SHViIEpXVCAoZXhwOiAxMG0pXG4gICAgVi0+Pkc6IFBPU1QgYXBpLmdpdGh1Yi5jb20vLi4uL2FjY2Vzc190b2tlbnNcbiAgICBHLS0+PlY6IHRva2VuOiBbIFwidjEuMTIzNDU2Nzg5Li4uXCIgZXhwOiBcIjFoXCIgXVxuICAgIFYtPj5WOiBSZWNvcmQgbWV0cmljcywgbG9nc1xuICAgIFYtLT4+VTogWyB0b2tlbjogXCJ2MS4xMjM0NTY3ODkuLi5cIiBleHA6IFwiMWhcIiBdXG4gICAgZGVhY3RpdmF0ZSBWXG4gICAgTm90ZSBvdmVyIFU6IFVzZSBhY2Nlc3MgdG9rZW4gb24gR2l0SHViXG4gICAgYWx0IE9wZXJhdGUgb24gcmVwb3N0b3JpZXMgYWNjZXNzIHRva2VuIGhhcyBwZXJtaXNzaW9ucyBvblxuICAgIFUtPj5HOiAkIGdpdCBjbG9uZSBodHRwczovL3gtYWNjZXNzLXRva2VuOnYxLjEyMzQ1Njc4OS4uLkBnaXRodWIuY29tL29yZy9yZXBvLmdpdFxuICAgIGVsc2UgUGVyZm9ybSBBUEkgcmVxdWVzdHMgYWdhaW5zdCByZXNvdXJjZXMgYWNjZXNzIHRva2VuIGhhcyBwZXJtaXNzaW9ucyBvblxuICAgIFUtPj5HOiAkIGN1cmwgLUggXCJBdXRob3JpemF0aW9uOiBCZWFyZXIgdjEuMTIzNDU2Nzg5Li4uXCIgaHR0cHM6Ly9hcGkuZ2l0aHViLmNvbS9yZXNvdXJjZVxuICAgIGVuZCIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0Iiwic2VxdWVuY2UiOnsibWlycm9yQWN0b3JzIjpmYWxzZSwiYWN0b3JNYXJnaW4iOjEyMCwibm90ZU1hcmdpbiI6MTAsIm1lc3NhZ2VNYXJnaW4iOjMwLCJib3hUZXh0TWFyZ2luIjoxLCJoZWlnaHQiOjMwLCJ3aWR0aCI6MjAwfX19)

## Installation

To begin plugin installation, either download a [release](https://github.com/martinbaillie/vault-plugin-secrets-github/releases) or build from source for your chosen OS and architecture.

## From release

Always download the latest stable release from the [releases](https://github.com/martinbaillie/vault-plugin-secrets-github/releases) section.

### Verify

You can and should verify the authenticity and integrity of the plugin you downloaded. All released binaries are hashed and the resulting sums are signed by my GPG key.

```
# Import my key.
curl -sS https://github.com/martinbaillie.gpg | gpg --import -

# Verify the authenticity.
gpg --verify SHA256SUMS.sig SHA256SUMS

# Verify the integrity.
shasum -a 256 -c SHA256SUMS
```

## From source

> NOTE: You will need at least a [Go 1.22+ toolchain](https://golang.org/dl/) to build this plugin from source. Ideally you will also be in the project’s Nix shell. See [Development](https://github.com/martinbaillie/vault-plugin-secrets-github/blob/master/Development) for more.

1. Either download the source zip/tar.gz of the latest release from the [releases](https://github.com/martinbaillie/vault-plugin-secrets-github/blob/master/releases) section and uncompress, or shallow clone to the target release tag as in below:
	```
	git clone --depth 1 -b <target_release_tag> \
	    https://github.com/martinbaillie/vault-plugin-secrets-github.git
	```
2. Build for your target OS and architecture.
	```
	# Recommended for accurate release-like reproduction.
	goreleaser build --single-target # Your current OS/Arch.
	GOOS=darwin GOARCH=amd64 goreleaser build --single-target # Another supported OS/Arch.
	goreleaser build # All supported OS/Arch combinations.
	# Alternatively,
	go build
	# or
	nix build
	```

## Setup (GitHub)

> NOTE: You will need access to admin of your GitHub or GitHub Enterprise organisation to continue with the one-time setup. You can of course use this plugin on your personal account if so desired.

1. Sign in as an org admin and begin creating a new [GitHub App.](https://github.com/settings/apps/new)
2. Choose any unique name, and homepage / webhook URLs (these can be anything; they are not required by the plugin).
	> NOTE: You may wish to take advantage of having GitHub call a webhook URL you own each time the App is used for auditing purposes.
3. Carefully choose the permissions the App will have access to. This is the superset of permissions. You will have the option of further restricting access to all or some repositories when you install an instance of the App, and users of this plugin will be able to even further restrict access in their individual token requests.
4. Decide if you want the app to be installable to other accounts. Usually you just want the one you are signed into.
5. Create the App. On the next screen GitHub will prompt you to create a **Private Key**. Do so, and save it somewhere safe (this is the key that will be ultimately lodged into the plugin configuration).
6. Note the **App ID** at the top of this page as well.
	> NOTE: Get the App ID anytime: Settings > Developer > settings > GitHub App > About item.
7. Click Install App from the LHS. You will be taken to the account installation pages where you can confirm the app was installed.
8. (OPTIONAL as of v1.3.0) Note the **Installation ID** from the URL of this page (usually: [https://github.com/settings/installations/<installation](https://github.com/settings/installations/%3Cinstallation) id>) if you wish to configure using the installation ID directly.
	> NOTE: Get the Installation ID anytime: Settings > Developer > settings > GitHub Apps > Advanced > Payload in Request tab.

## Setup (Vault)

Using the information noted from the previous step (Private Key, App ID and optionally the Installation ID), you are ready to move on to setting up the Vault plugin.

1. Move the desired plugin binary into your Vault’s configured `plugin_directory`.
	```
	mv vault-plugin-secrets-github-<os>-<arch> <plugin_directory>/vault-plugin-secrets-github
	```
2. (OPTIONAL) Allow [`mlock()`](https://linux.die.net/man/2/mlock) capabilities for the plugin binary. Memory locking is available to most UNIX-like OSes; the example below is for Linux.
	```
	setcap cap_ipc_lock=+ep <plugin_directory>/vault-plugin-secrets-github
	```
3. (OPTIONAL) Calculate the SHA256 sum of the plugin and register it in Vault’s plugin catalog. If you are downloading the pre-compiled binary, it is highly recommended that you use the published SHA256SUMS file.
	> NOTE: The rest of these commands assume you have a valid VAULT\_TOKEN and VAULT\_API environment variables.
	```
	# If using a pre-compiled binary:
	SHA256SUM=$(grep <downloaded_binary> SHA256SUMS | cut -d' ' -f1)
	# If building from source:
	SHA256SUM=$(shasum -a 256 <compiled_binary> | cut -d' ' -f1)
	vault write sys/plugins/catalog/secret/vault-plugin-secrets-github \
	    sha_256=${SHA256SUM} command=vault-plugin-secrets-github
	```
4. Mount the secrets engine, choosing a prefix path (recommendation: `github`).
	```
	vault secrets enable -path=github -plugin-name=vault-plugin-secrets-github plugin
	```
5. Configure the plugin with the details noted from the previous section.
	```
	# Write the configuration
	vault write /github/config app_id=<app_id> prv_key=@<private_key_file>
	# (OPTIONAL) Exclude repository metadata from token responses (reduces memory footprint).
	vault write /github/config exclude_repository_metadata=true
	# (OPTIONAL) Confirm the configuration landed as you expected.
	vault read /github/config
	# (OPTIONAL) Test a token creation.
	vault read /github/token installation_id=<installation_id>
	vault read /github/token org_name=<org_name> # Installation ID discovered from Org.
	```
6. (OPTIONAL) Use Vault policy to constrain user capabilities on the GitHub endpoints. Example:
	```
	# Create a restrictive policy that only permits GitHub tokens that can write
	# pull requests to a single repository.
	vault policy write github-only-prs -<<EOF
	path "github/token" {
	  capabilities = ["update"]
	  required_parameters = ["installation_id","permissions","repository_ids"]
	  allowed_parameters = {
	    "installation_id" = ["987654"]
	    "repository_ids" = ["69857131"]
	    "permissions"= ["pull_requests=write"]
	  }
	}
	EOF
	# Create and login as an example user with the policy attached.
	vault auth enable userpass
	vault write auth/userpass/users/martin password=baillie policies="github-only-prs"
	vault login -method=userpass username=martin password=baillie
	# Test the efficacy of the policy.
	# Successfully creates token:
	vault write /github/token installation_id=987654 repository_ids=69857131 permissions=pull_requests=write
	# Permission denied:
	vault write -f /github/token
	vault write /github/token installation_id=987654 permissions=pull_requests=write
	vault write /github/token installation_id=987654 repository_ids=69857131 permissions=pull_requests=read
	vault write /github/token installation_id=987654 repository_ids=69857131 permissions=metadata=read
	vault write /github/token installation_id=987654 repository_ids=123 permissions=pull_requests=write
	vault write /github/token installation_id=987654 repository_ids=69857131
	vault write /github/token installation_id=123456 repository_ids=69857131
	```

## API

Each plugin path is documented using Vault’s own help framework. To find out more information about any path, use `vault path-help`. For brevity, the API is also documented below.

## Token

Instruct the plugin to create an installation access token against the configured GitHub App.

| Method | Path | Produces |
| --- | --- | --- |
| GET | /token | application/json |
| POST | /token | application/json |
| PUT | /token | application/json |

### Parameters

> NOTE: Only one of `installation_id` or `org_name` is required. If only `org_name` is provided, an additional lookup against the GitHub instance is performed per token creation to discover the `installation_id`. If both are provided, `installation_id` takes precedence to avoid the additional round trip. Also note that no caching is performed so for high traffic use cases, favour `installation_id`.
> 
> All other parameters are optional. Omitting them results in a token that has access to all of the repositories and permissions that the GitHub App installation has.
> 
> When crafting Vault policy, hyper security sensitive organisations may wish to favour `repository_ids` (GitHub repository IDs are immutable) instead of `repositories` (GitHub repository names are mutable).

> NOTE: All token responses (including those from permission sets) include `hashed_token`, a base64-encoded SHA-256 hash of the returned token that matches GitHub’s [audit log](https://docs.github.com/en/enterprise-cloud@latest/admin/monitoring-activity-in-your-enterprise/reviewing-audit-logs-for-your-enterprise/identifying-audit-log-events-performed-by-an-access-token#token-data-in-audit-log-events) `hashed_token` field. This value is safe to log and enables correlation between Vault-issued tokens and GitHub audit events by searching for `hashed_token:"VALUE"`. You can verify the hash yourself with: `echo -n TOKEN | openssl dgst -sha256 -binary | base64`.

- `installation_id` (int64) — the ID of the app installation.
- `org_name` (string) — the organisation name.
- `repositories` (\[\]string) — a list of the names of the repositories within the organisation that the installation token can access.
- `repository_ids` (\[\]int64) — a list of the IDs of the repositories that the installation token can access. See this [StackOverflow post](https://stackoverflow.com/a/47223479) for the quickest way to find a repository ID.
- `permissions` (map\[string\]string) — a key value map of permission names to their access type (read or write). See [GitHub’s documentation](https://developer.github.com/v3/apps/permissions) on permission names and access types.

### Examples

```
# Create a token with all the superset of all permissions and repositories that
# the GitHub App installation has access to.
vault read /github/token

# Create a token with read permissions on the packages and write permissions on
# the pull requests of repositories named "demo-repo" and ID 123.
vault write /github/token \
  installation_id=456 \
    repository_ids=123 \
    repositories=demo-repo \
    permissions=packages=read \
    permissions=pull_requests=write

# Create a token with all permissions but only on the "demo-repo" repository.
vault write /github/token installation_id=456 repository_ids=123 repository_ids=456

# Create a token with all permissions but only on repositories 123 and 456.
vault write /github/token installation_id=456 repository_ids=123 repository_ids=456

# Create a token with write access to pull requests using read / GET.
vault write /github/token permissions=pull_requests=write

# Create a token with read access to metadata and write access to pull requests
# on repositories "demo-repo", 123 and 456 only.
# NOTE: Uses a Vault CLI JSON heredoc to submit the complex map type.
vault write /github/token - <<EOF
{
"installation_id": 456,
"repositories": ["demo-repo"],
"repository_ids": [123,456],
"permissions": {"metadata": "read", "pull_requests": "write"}
}
EOF
```

> NOTE: a 422 response usually indicates you have requested repositories IDs or permissions that your GitHub App install does not have access to.

### Revocation

It is possible to revoke tokens in your configured GitHub using Vault constructs. For example:

```
# Revoke an individual token with just the lease ID.
vault lease revoke <lease_id previously received from token endpoint>
# List currently active lease IDs.
vault list sys/leases/lookup/github/token
# Revoke all tokens currently leased by Vault.
vault lease revoke -prefix github/token
```

> NOTE: the previous commands presume your plugin is mounted at `/github`.

Alternatively, you can go directly to your GitHub with the token in hand:

```
curl -H "Authorization: Bearer ${GITHUB_TOKEN}" \
    -X DELETE https://api.mygithub.com/installation/token
```

## Permission sets

Instruct the plugin to create a specific permission set.

| Method | Path | Produces |
| --- | --- | --- |
| GET | /permissionset/<name> | application/json |
| POST | /permissionset/<name> | application/json |
| PUT | /permissionset/<name> | application/json |
| DELETE | /permissionset/<name> | application/json |
| GET | /permissionsets?list=true | application/json |

### Parameters

> NOTE: Only one of `installation_id` or `org_name` is required. If only `org_name` is provided, an additional lookup against the GitHub instance is performed per token creation to discover the `installation_id`. If both are provided, `installation_id` takes precedence to avoid the additional round trip. Also note that no caching is performed so for high traffic use cases, favour `installation_id`.
> 
> All other parameters are optional. Omitting them results in a token that has access to all of the repositories and permissions that the GitHub App installation has.
> 
> When crafting Vault policy, hyper security sensitive organisations may wish to favour `repository_ids` (GitHub repository IDs are immutable) instead of `repositories` (GitHub repository names are mutable).

- `installation_id` (int64) — the ID of the app installation.
- `org_name` (string) — the organisation name.
- `repositories` (\[\]string) — a list of the names of the repositories within the organisation that the installation token can access.
- `repository_ids` (\[\]int64) — a list of the IDs of the repositories that the installation token can access. See this [StackOverflow post](https://stackoverflow.com/a/47223479) for the quickest way to find a repository ID.
- `permissions` (map\[string\]string) — a key value map of permission names to their access type (read or write). See [GitHub’s documentation](https://developer.github.com/v3/apps/permissions) on permission names and access types.

### Request a token from a permission set

Similar to the [token](#token) flow in the previous section, you can instruct the plugin to create an installation access token by using a permission set name. The token returned will be constrained by that pre-configured permission set.

| Method | Path | Produces |
| --- | --- | --- |
| GET | /token/<name> | application/json |
| POST | /token/<name> | application/json |
| PUT | /token/<name> | application/json |

### Examples

```
# Configure a permission set that only allows metadata reads and PR writes
# against three repositories.
vault write /github/permissionset/demo-set - <<EOF
{
"installation_id": 987,
"repositories": ["demo-repo"],
"repository_ids": [123,456],
"permissions": {"metadata": "read", "pull_requests": "write"}
}
EOF
# Or
vault write /github/permissionset/demo-set \
    installation_id=987 \
    repositories=demo-repo \
    repository_ids=123 \
    repository_ids=456 \
    permissions=pull_requests=read \
    permissions=metadata=read

# Read the permission set configuration.
vault read /github/permissionset/demo-set

# List all permission sets.
vault list /github/permissionsets

# Create a token automatically constrained by the permission set.
vault read /github/token/demo-set

# Delete an existing permission set.
vault delete /github/permissionset/demo-set
```

## Config

General CRUD operations against the configuration of the plugin.

| Method | Path | Produces |
| --- | --- | --- |
| POST | /config | application/json |
| GET | /config | application/json |
| PUT | /config | application/json |
| DELETE | /config | application/json |

### Parameters

- `app_id` (int64) — the Application ID of the GitHub App.
- `prv_key` (string) — a private key configured in the GitHub App. This private key must be in PEM PKCS#1 RSAPrivateKey format. It is not returned with read requests for security reasons but its presence or lack thereof is indicated.
- `base_url` (string) — the base URL for API requests (defaults to the public GitHub API).
- `exclude_repository_metadata` (bool) — reduce the verbose \`repositories\` array in GitHub token responses to a simple list of repository names. This significantly reduces the memory required by the plugin when used at scale.

### Examples

```
# Write the plugin configuration using the default base URL, and reading the key from a file.
vault write /github/config app_id=123 prv_key=@key.pem

# Read the plugin configuration.
vault read /github/config

# Update the plugin configuration to a GitHub Enterprise base URL.
vault write /github/config base_url="https://api.mygithub.org"

# Significantly reduce memory consumed per token.
vault write /github/config exclude_repository_metadata=true

# Delete the plugin configuration.
vault delete /github/config
```

## Metrics

Prometheus/OpenMetrics formatted metrics exposition.

| Method | Path | Produces |
| --- | --- | --- |
| GET | /metrics | text/plain |

### Metrics

In addition to standard Go metrics, the following custom metrics are exposed:

- `vault_github_token_request_duration_seconds` — a summary of token request latency and status.
- `vault_github_token_revocation_request_duration_seconds` — a summary of token revocation request latency and status.
- `vault_github_token_build_info` — a constant with useful build information.

### Sample Dashboard

A sample dashboard is [provided](https://github.com/martinbaillie/vault-plugin-secrets-github/blob/master/dashboard.json).

[![dashboard.png](https://github.com/martinbaillie/vault-plugin-secrets-github/raw/master/dashboard.png)](https://github.com/martinbaillie/vault-plugin-secrets-github/blob/master/dashboard.png)

## Info

Information about the GitHub secrets plugin, such as the plugin version, VCS detail and where to get help.

| Method | Path | Produces |
| --- | --- | --- |
| GET | /info | application/json |

## Development

This plugin is written using modern [Go](https://golang.org/dl/) (1.22+). Its project infrastructure supports Linux and macOS aarch64/amd64 platforms and is handled by [Nix](https://nixos.org/).

Nix is the only pre-requisite you need to have installed. If you do not already have or wish to install `nix`, consider the `nixos/nix` container image.

The Nix [flake](https://github.com/martinbaillie/vault-plugin-secrets-github/blob/master/flake.nix) at the project root provides the Go toolchain as well as any ancillary tooling needed. If you use [direnv](https://direnv.net/docs/installation.html) (recommended) you will automatically be in a usable project shell after trusting it once with `direnv allow`.

Otherwise you will need to enter a Nix shell manually:

```
nix develop
```

Once in the Nix shell you should be presented with the following:

```
vault-plugin-secrets-github
menu                              - available commands
```

Proceed to browse the `menu` or learn how to test the project below.

## Tests

This plugin is comprehensively tested by both unit and acceptance tests. Pull requests that do not maintain an [\>90% coverage](https://codecov.io/gh/martinbaillie/vault-plugin-secrets-github) will **not** be accepted.

```
# View the developer shell menu.
menu

# Run linting.
lint

# Run CI-grade linting.
env CI=true lint

# Run unit tests.
unit

# Run unit and acceptance tests, integrating against a local Vault and stubbed
# GitHub API.
integration

# Run integration tests with debug logging.
env DEBUG=true integration

# Run unit and acceptance tests, integrating against a local Vault and the real
# GitHub API against your own GitHub App installation (you can also run these
# tests against a GitHub Enterprise deployment). Setting \`BASE_URL\` causes the
# tests to call against a real API.
# NOTE: Keep in mind this test configuration will create real tokens.
env \
    BASE_URL=https://api.github.com \
    APP_ID=<your application id> \
    ORG_NAME=<org_name> \
    INSTALLATION_ID=<installation_id> \
    PRV_KEY="$(cat /path/to/your/app/prv_key_file)" integration
```

## Security

HashiCorp and GitHub take their security seriously. If you believe you have found a security issue with either through using this plugin, do not open an issue here. Responsibly disclose by getting in touch with [HashiCorp](mailto:security@hashicorp.com) or [GitHub](https://hackerone.com/github) security teams respectively.
