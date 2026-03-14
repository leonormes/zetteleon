---
captured: "2026-03-07T16:50:21+00:00 2026-03-07T16:50:21+00:00"
created: 2026-03-07T16:50:22+00:00
modified: 2026-03-14T11:10:31+00:00
source: "https://gemini.google.com/app/53d41e76fb83ea25"
status: "processing"
tags: ["input", failure, success]
title: HEAD You said kubectl describe pod hutch-relay-6bc9f49f...
type: "head"
---

## Raw Output / Content

kubectl describe pod hutch-relay-6bc9f49f7c-gwjnw -n hutch

Name: hutch-relay-6bc9f49f7c-gwjnw

Namespace: hutch

Priority: 0

Service Account: hutch-relay

Node: ip-10-66-7-80.eu-west-2.compute.internal/10.66.7.80

Start Time: Tue, 17 Feb 2026 16:55:01 +0000

Labels: app.kubernetes.io/instance=hutch

app.kubernetes.io/managed-by=Helm

app.kubernetes.io/name=relay

app.kubernetes.io/version=0.0.1

helm.sh/chart=hutch-0.1.0

pod-template-hash=6bc9f49f7c

Annotations: kubectl.kubernetes.io/restartedAt: 2026-02-17T16:48:19Z

vso.secrets.hashicorp.com/restartedAt: 2026-02-17T15:58:27Z

Status: Running

IP: 10.66.6.90

IPs:

IP: 10.66.6.90

Controlled By: ReplicaSet/hutch-relay-6bc9f49f7c

Containers:

relay:

Container ID: containerd://af5c3c3c7e66eb2d7c033eeb4fe56bf2c6ff6b0d40cf959a4e01ab484a2e96bf

Image: fitfileregistry.azurecr.io/hutch/relay:1.0.1

Image ID: fitfileregistry.azurecr.io/hutch/relay@sha256:549c1c444bf998637eeb80f2430604df141dd100e6e6003e0a838e5c2b46648d

Ports: 8080/TCP (http), 8081/TCP (other)

Host Ports: 0/TCP (http), 0/TCP (other)

State: Waiting

Reason: CrashLoopBackOff

Last State: Terminated

Reason: Completed

Exit Code: 0

Started: Thu, 19 Feb 2026 12:34:02 +0000

Finished: Thu, 19 Feb 2026 12:34:04 +0000

Ready: False

Restart Count: 233

Limits:

cpu: 1

memory: 1Gi

Requests:

cpu: 500m

memory: 512Mi

Liveness: http-get http://:http/healthz delay=0s timeout=1s period=5s success=1 failure=5

Readiness: http-get http://:http/healthz delay=5s timeout=1s period=5s success=1 failure=3

Environment:

ConnectionStrings\_\_Default: <set to the key 'db\_connection\_string' in secret 'relay'> Optional: false

DOTNET\_Environment: Development

Database\_\_ApplyMigrationsOnStartup: true

Logging\_\_LogLevel\_\_Default: Debug

Obfuscation\_\_LowNumberSuppressionThreshold: 0

Obfuscation\_\_RoundingTarget: 0

RelayTaskQueue\_\_ConnectionString: <set to the key 'rabbitmq\_connection\_string' in secret 'relay'> Optional: false

UpstreamTaskApi\_\_BaseUrl: <https://rquest.preprod.hdruk.cloud>

UpstreamTaskApi\_\_CollectionId: RQ-CC-563f7364-d8d5-4b10-b6ff-182b10b7cb7a

UpstreamTaskApi\_\_Enable: true

UpstreamTaskApi\_\_Password: <set to the key 'upstream\_task\_api\_password' in secret 'relay'> Optional: false

UpstreamTaskApi\_\_Username: <set to the key 'upstream\_task\_api\_username' in secret 'relay'> Optional: false

SubNodes\_\_test-node: placeholder-id

Mounts:

/var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-rqncb (ro)

Conditions:

Type Status

PodReadyToStartContainers True

Initialized True

Ready False

ContainersReady False

PodScheduled True

Volumes:

kube-api-access-rqncb:

Type: Projected (a volume that contains injected data from multiple sources)

TokenExpirationSeconds: 3607

ConfigMapName: kube-root-ca.crt

Optional: false

DownwardAPI: true

QoS Class: Burstable

Node-Selectors: <none>

Tolerations: node.kubernetes.io/not-ready:NoExecute op=Exists for 300s

node.kubernetes.io/unreachable:NoExecute op=Exists for 300s

Events:

Type Reason Age From Message

\---- ------ ---- ---- -------

Warning BackOff 4m25s (x5198 over 43h) kubelet Back-off restarting failed container relay in pod hutch-relay-6bc9f49f7c-gwjnw\_hutch(f1167bea-1d40-430f-bec8-a240c0a647e4)

Normal Pulling 33s (x544 over 43h) kubelet Pulling image "fitfileregistry.azurecr.io/hutch/relay:1.0.1"

awsadmin@ip-10-66-2-4:~$ kubectl logs hutch-relay-6bc9f49f7c-gwjnw -n hutch

\_ \_ \_ \_ \_\_\_\_ \_

| | | | \_ \_ | |\_ \_\_\_ | |\_\_ | \_ \\ \_\_\_ | | \_\_ \_ \_ \_

| |\_| | | | | | | \_\_| / \_\_| | '\_ \\ | |\_) | / \_ \\ | | / \_\` | | | | |

| \_ | | |\_| | | |\_ | (\_\_ | | | | | \_ < | \_\_/ | | | (\_| | | |\_| |

|\_| |\_| \\\_\_,\_| \\\_\_| \\\_\_\_| |\_| |\_| |\_| \\\_\\ \\\_\_\_| |\_| \\\_\_,\_| \\\_\_, |

|\_\_\_/

\[12:34:04 INF\] Executed DbCommand (17ms) \[Parameters=\[\], CommandType='Text', CommandTimeout='30'\]

SELECT "MigrationId", "ProductVersion"

FROM "\_\_EFMigrationsHistory"

ORDER BY "MigrationId"; <s:Microsoft.EntityFrameworkCore.Database.Command>

\[12:34:04 INF\] Executed DbCommand (9ms) \[Parameters=\[\], CommandType='Text', CommandTimeout='30'\]

CREATE TABLE IF NOT EXISTS "\_\_EFMigrationsHistory" (

"MigrationId" character varying(150) NOT NULL,

"ProductVersion" character varying(32) NOT NULL,

CONSTRAINT "PK\_\_\_EFMigrationsHistory" PRIMARY KEY ("MigrationId")

); <s:Microsoft.EntityFrameworkCore.Database.Command>

\[12:34:04 INF\] Executed DbCommand (3ms) \[Parameters=\[\], CommandType='Text', CommandTimeout='30'\]

LOCK TABLE "\_\_EFMigrationsHistory" IN ACCESS EXCLUSIVE MODE <s:Microsoft.EntityFrameworkCore.Database.Command>

\[12:34:04 INF\] Executed DbCommand (1ms) \[Parameters=\[\], CommandType='Text', CommandTimeout='30'\]

SELECT "MigrationId", "ProductVersion"

FROM "\_\_EFMigrationsHistory"

ORDER BY "MigrationId"; <s:Microsoft.EntityFrameworkCore.Database.Command>

\[12:34:04 INF\] No migrations were applied. The database is already up to date. <s:Microsoft.EntityFrameworkCore.Migrations>

\[12:34:04 INF\] Executed DbCommand (3ms) \[Parameters=\[\], CommandType='Text', CommandTimeout='30'\]

SELECT a."Id", a."AccessFailedCount", a."ConcurrencyStamp", a."Discriminator", a."Email", a."EmailConfirmed", a."LockoutEnabled", a."LockoutEnd", a."NormalizedEmail", a."NormalizedUserName", a."PasswordHash", a."PhoneNumber", a."PhoneNumberConfirmed", a."SecurityStamp", a."TwoFactorEnabled", a."UserName", a."IsDeclared", s0."Id", s0."RelayUsersId", s0."SubNodesId"

FROM "AspNetUsers" AS a

LEFT JOIN (

SELECT s."Id", r."RelayUsersId", r."SubNodesId"

FROM "RelayUserSubNode" AS r

INNER JOIN "SubNodes" AS s ON r."SubNodesId" = s."Id"

) AS s0 ON a."Id" = s0."RelayUsersId"

WHERE a."Discriminator" = 'RelayUser'

ORDER BY a."Id", s0."RelayUsersId", s0."SubNodesId" <s:Microsoft.EntityFrameworkCore.Database.Command>

\[12:34:04 WRN\] Storing keys in a directory '/root/.aspnet/DataProtection-Keys' that may not be persisted outside of the container. Protected data will be unavailable when container is destroyed. For more information go to <https://aka.ms/aspnet/dataprotectionwarning> <s:Microsoft.AspNetCore.DataProtection.Repositories.FileSystemXmlRepository>

\[12:34:04 INF\] User profile is available. Using '/root/.aspnet/DataProtection-Keys' as key repository; keys will not be encrypted at rest. <s:Microsoft.AspNetCore.DataProtection.KeyManagement.XmlKeyManager>

\[12:34:04 INF\] Creating key {562218ef-1461-45f8-a865-0028ea12792e} with creation date 2026-02-19 12:34:04Z, activation date 2026-02-19 12:34:04Z, and expiration date 2026-05-20 12:34:04Z. <s:Microsoft.AspNetCore.DataProtection.KeyManagement.XmlKeyManager>

\[12:34:04 WRN\] No XML encryptor configured. Key {562218ef-1461-45f8-a865-0028ea12792e} may be persisted to storage in unencrypted form. <s:Microsoft.AspNetCore.DataProtection.KeyManagement.XmlKeyManager>

\[12:34:04 INF\] Writing data to file '/root/.aspnet/DataProtection-Keys/key-562218ef-1461-45f8-a865-0028ea12792e.xml'. <s:Microsoft.AspNetCore.DataProtection.Repositories.FileSystemXmlRepository>

\[12:34:04 INF\] Executed DbCommand (1ms) \[Parameters=\[\], CommandType='Text', CommandTimeout='30'\]

SELECT EXISTS (

SELECT 1

FROM "SubNodes" AS s) <s:Microsoft.EntityFrameworkCore.Database.Command>

\[12:34:04 ERR\] Hosting failed to start <s:Microsoft.Extensions.Hosting.Internal.Host>

System.InvalidOperationException: There are no subnodes configured!

at Hutch.Relay.Services.SubNodeService.EnsureSubNodes() in /src/app/Hutch.Relay/Services/SubNodeService.cs:line 17

at Hutch.Relay.Services.Hosted.BackgroundUpstreamTaskPoller.ExecuteAsync(CancellationToken stoppingToken) in /src/app/Hutch.Relay/Services/Hosted/BackgroundUpstreamTaskPoller.cs:line 21

at Microsoft.Extensions.Hosting.Internal.Host.<StartAsync>b\_\_14\_1(IHostedService service, CancellationToken token)

at Microsoft.Extensions.Hosting.Internal.Host.ForeachService\[T\](IEnumerable\`1 services, CancellationToken token, Boolean concurrent, Boolean abortOnFirstException, List\`1 exceptions, Func\`3 operation)

Unhandled exception: System.InvalidOperationException: There are no subnodes configured!

at Hutch.Relay.Services.SubNodeService.EnsureSubNodes() in /src/app/Hutch.Relay/Services/SubNodeService.cs:line 17

at Hutch.Relay.Services.Hosted.BackgroundUpstreamTaskPoller.ExecuteAsync(CancellationToken stoppingToken) in /src/app/Hutch.Relay/Services/Hosted/BackgroundUpstreamTaskPoller.cs:line 21

at Microsoft.Extensions.Hosting.Internal.Host.<StartAsync>b\_\_14\_1(IHostedService service, CancellationToken token)

at Microsoft.Extensions.Hosting.Internal.Host.ForeachService\[T\](IEnumerable\`1 services, CancellationToken token, Boolean concurrent, Boolean abortOnFirstException, List\`1 exceptions, Func\`3 operation)

at Microsoft.Extensions.Hosting.Internal.Host.StartAsync(CancellationToken cancellationToken)

at Microsoft.Extensions.Hosting.HostingAbstractionsHostExtensions.RunAsync(IHost host, CancellationToken token)

at Microsoft.Extensions.Hosting.HostingAbstractionsHostExtensions.RunAsync(IHost host, CancellationToken token)

at Hutch.Relay.Startup.Web.WebEntrypoint.Run(String\[\] args) in /src/app/Hutch.Relay/Startup/Web/WebEntrypoint.cs:line 28

at Hutch.Relay.Commands.Helpers.CliMiddlewareExtensions.<>c\_\_DisplayClass0\_0.<<UseRootCommandBypass>b\_\_0>d.MoveNext() in /src/app/Hutch.Relay/Commands/Helpers/CliMiddlewareExtensions.cs:line 22

\--- End of stack trace from previous location ---

at Hutch.Relay.Startup.Cli.CliEntrypoint.<>c.<<UseCliLogo>b\_\_1\_0>d.MoveNext() in /src/app/Hutch.Relay/Startup/Cli/CliEntrypoint.cs:line 34

\--- End of stack trace from previous location ---

at System.CommandLine.Builder.CommandLineBuilderExtensions.<>c\_\_DisplayClass12\_0.<<UseHelp>b\_\_0>d.MoveNext()

\--- End of stack trace from previous location ---

at System.CommandLine.Builder.CommandLineBuilderExtensions.<>c\_\_DisplayClass22\_0.<<UseVersionOption>b\_\_0>d.MoveNext()

\--- End of stack trace from previous location ---

at System.CommandLine.Builder.CommandLineBuilderExtensions.<>c\_\_DisplayClass19\_0.<<UseTypoCorrections>b\_\_0>d.MoveNext()

\--- End of stack trace from previous location ---

at System.CommandLine.Builder.CommandLineBuilderExtensions.<>c.<<UseSuggestDirective>b\_\_18\_0>d.MoveNext()

\--- End of stack trace from previous location ---

at System.CommandLine.Builder.CommandLineBuilderExtensions.<>c\_\_DisplayClass16\_0.<<UseParseDirective>b\_\_0>d.MoveNext()

\--- End of stack trace from previous location ---

at System.CommandLine.Builder.CommandLineBuilderExtensions.<>c.<<RegisterWithDotnetSuggest>b\_\_5\_0>d.MoveNext()

\--- End of stack trace from previous location ---

at System.CommandLine.Builder.CommandLineBuilderExtensions.<>c\_\_DisplayClass8\_0.<<UseExceptionHandler>b\_\_0>d.MoveNext()

---

The good news is that your deployment pipeline is working perfectly! I can see the pod template hash has updated to `6bc9f49f7c`, which means ArgoCD successfully detected your commit and rolled out the new configuration.

However, we can also see exactly why it is still crashing. If you look closely at the `Environment:` section of the `kubectl describe` output you just shared, this is what was injected:

It looks like your local assistant (or a manual edit) added a placeholder variable instead of the correct `DownstreamUsers` block we discussed.

Having just reviewed the official Hutch configuration documentation you provided, I can confirm that Relay does not recognise `SubNodes__…` as a valid configuration path for declarative state. To declare a downstream user and subnode via environment variables, Hutch strictly expects the format `DownstreamUsers__<username>__Subnode`.

Because Relay didn't recognise the `SubNodes__test-node` variable, it assumed the database was still empty and threw the exact same `System.InvalidOperationException: There are no subnodes configured!` error.

### How to Fix It (For Real This Time!)

You will need to open your `/ffnodes/eoe/hie-test-34/hutch_values.yaml` file, locate the `relay.extraEnvVars` section, and replace the `SubNodes__test-node` entry with the correct `DownstreamUsers` block.

It needs to look exactly like this:

Once you commit this specific block and ArgoCD synchronises, the container will receive the variables in the exact format ASP.NET Core needs to seed the database, and the application should finally start.

Would you like me to wait while you make this edit and check the logs one last time?

---

This is the full values file

global:

imagePullSecrets:

\- name: fitfile-image-pull-secret

relay:

enabled: true

service:

metadata:

annotations:

gateway.networking.k8s.aws/target-type: "instance"

type: NodePort

port: 8080

nodePort: 32080

extraPorts:

\- name: other

port: 8081

targetPort: other

nodePort: 32081

image:

repository: fitfileregistry.azurecr.io/hutch/relay

pullPolicy: Always

db:

auth:

existingSecretName: "relay"

host: hutch-postgresql

extraEnvVars:

\- name: Logging\_\_LogLevel\_\_Default

value: Debug

\- name: Obfuscation\_\_LowNumberSuppressionThreshold

value: "0"

\- name: DownstreamUsers\_\_test\_user\_1\_\_Subnode

value: "019528e1-50cb-73a6-b624-70beb205a9bf"

\- name: DownstreamUsers\_\_test\_user\_1\_\_Password

valueFrom:

secretKeyRef:

name: relay-downstream-users

key: test\_user\_1\_password

queue:

auth:

existingSecretName: "relay"

host: hutch-rabbitmq

upstreamTaskApi:

basicAuth:

existingSecretName: "relay"

baseUrl: "https://rquest.preprod.hdruk.cloud"

\# Old collection called "East of England SDE Test Collection"

collectionId: "RQ-CC-563f7364-d8d5-4b10-b6ff-182b10b7cb7a"

\# New collection called "East of England SDE Test Collection 2"

\# Currently this collection isn't receiving any queries - perhaps the credentials are wrong.

\# collectionId: RQ-CC-d4e0eecf-ca8e-4f06-a6a2-1bd4e19c2ab8

resources:

requests:

cpu: "500m"

memory: 512Mi

limits:

cpu: "1"

memory: 1024Mi

bunny:

enabled: false

image:

repository: fitfileregistry.azurecr.io/hutch/bunny

pullPolicy: Always

\# This is our own custom image which allows the concept table to exist in the vocab schema

tag: 1.0.0-alpha.9

db:

auth:

existingSecretName: "bunny"

existingSecretUsernameKey: "db\_username"

existingSecretPasswordKey: "db\_password"

host: "thehyve-postgresql.thehyve.svc.cluster.local"

port: 5432

driverName: postgresql

dbName: ohdsi

schema: cdm

extraEnvVars:

\- name: COLLECTION\_ID

value: 019528e1-50cb-73a6-b624-70beb205a9bf

\# Used when directly connecting bunny to National Portal

\# - name: COLLECTION\_ID

\# value: RQ-CC-d4e0eecf-ca8e-4f06-a6a2-1bd4e19c2ab8

\- name: POLLING\_INTERVAL

value: "10"

\- name: BUNNY\_LOGGER\_LEVEL

value: "DEBUG"

\# To set when HIE tell us what the values should be

\# - name: LOW\_NUMBER\_SUPPRESSION\_THRESHOLD

\# value: ""

\# - name: POLLING\_INTERVAL

\# value: "5"

\# - name: ROUNDING\_TARGET

\# value: ""

taskApi:

\# Used when connecting bunny directly to the National Portal

\# baseUrl: "https://rquest.preprod.hdruk.cloud"

basicAuth:

existingSecretName: "bunny"

existingSecretUsernameKey: "task\_api\_username"

existingSecretPasswordKey: "task\_api\_password"

resources:

requests:

cpu: 200m

memory: 512Mi

limits:

cpu: "1"

memory: 1024Mi

rabbitmq:

\# Enables the rabbitmq templates

enabled: true

auth:

existingPasswordSecret: hutch-rabbitmq

existingErlangSecret: hutch-rabbitmq

username: "relay"

persistence:

enabled: true

size: 8Gi

resources:

requests:

cpu: 250m

memory: 512Mi

limits:

cpu: "1"

memory: 1024Mi

postgresql:

enabled: true

primary:

resources:

requests:

cpu: 200m

memory: 512Mi

limits:

cpu: 500m

memory: 1Gi

persistence:

size: 8Gi

auth:

existingSecret: "hutch-postgresql"

extraDeploy:

\- apiVersion: secrets.hashicorp.com/v1beta1

kind: VaultStaticSecret

metadata:

name: bunny

namespace: "{{.Release.Namespace }}"

spec:

\# Vault namespace where the secrets backend is

namespace: admin/deployments/hie-test-34

\# Vault mount path of the secrets backend

mount: secrets

\# Vault path in secrets engine mount to the secret

path: hutch

\# Type of the Vault static secret

type: kv-v2

\# Used for environment drift detection. Should always be on

hmacSecretData: true

\# Where to store the secrets, VSO will create the secret

destination:

create: true

name: bunny

\# Transform hutch.bunny secrets

transformation:

excludes:

\-.\*

templates:

db\_username:

text: '{{\`{{get.Secrets "bunny\_postgresql\_username"}}\`}}'

db\_password:

text: '{{\`{{get.Secrets "bunny\_postgresql\_password"}}\`}}'

task\_api\_username:

text: '{{\`{{get.Secrets "bunny\_relay\_username"}}\`}}'

task\_api\_password:

text: '{{\`{{get.Secrets "bunny\_relay\_password"}}\`}}'

\# Restart these pods when secrets rotated

rolloutRestartTargets:

\- kind: Deployment

name: '{{ include "hutch.bunny.fullname". }}'

\# Refresh interval

refreshAfter: 10m

\# Name of the CRD to authenticate to Vault

vaultAuthRef: default

\- apiVersion: secrets.hashicorp.com/v1beta1

kind: VaultStaticSecret

metadata:

name: relay

namespace: "{{.Release.Namespace }}"

spec:

\# Vault namespace where the secrets backend is

namespace: admin/deployments/hie-test-34

\# Vault mount path of the secrets backend

mount: secrets

\# Vault path in secrets engine mount to the secret

path: hutch

\# Type of the Vault static secret

type: kv-v2

\# Used for environment drift detection. Should always be on

hmacSecretData: true

\# Where to store the secrets, VSO will create the secret

destination:

create: true

name: relay

\# Transform thehyve secrets

transformation:

excludes:

\-.\*

templates:

db\_connection\_string:

text: 'Host=hutch-postgresql;Port=5432;Database=postgres;User Id={{\`{{get.Secrets "relay\_postgresql\_username"}}\`}};Password={{\`{{get.Secrets "relay\_postgresql\_password"}}\`}}'

rabbitmq\_connection\_string:

text: 'amqp://{{\`{{get.Secrets "relay\_rabbitmq\_username"}}\`}}:{{\`{{get.Secrets "relay\_rabbitmq\_password"}}\`}}@hutch-rabbitmq:5672'

upstream\_task\_api\_username:

text: '{{\`{{get.Secrets "relay\_task\_api\_username"}}\`}}'

upstream\_task\_api\_password:

text: '{{\`{{get.Secrets "relay\_task\_api\_password"}}\`}}'

\# Restart these pods when secrets rotated

rolloutRestartTargets:

\- kind: Deployment

name: '{{ include "hutch.relay.fullname". }}'

\# Refresh interval

refreshAfter: 10m

\# Name of the CRD to authenticate to Vault

vaultAuthRef: default

\- apiVersion: secrets.hashicorp.com/v1beta1

kind: VaultStaticSecret

metadata:

name: hutch-postgresql

namespace: "{{.Release.Namespace }}"

spec:

\# Vault namespace where the secrets backend is

namespace: admin/deployments/hie-test-34

\# Vault mount path of the secrets backend

mount: secrets

\# Vault path in secrets engine mount to the secret

path: hutch

\# Type of the Vault static secret

type: kv-v2

\# Used for environment drift detection. Should always be on

hmacSecretData: true

\# Where to store the secrets, VSO will create the secret

destination:

create: true

name: hutch-postgresql

\# Transform thehyve secrets

transformation:

excludes:

\-.\*

templates:

postgres-password:

text: '{{\`{{get.Secrets "postgres\_admin\_password"}}\`}}'

\# Restart these pods when secrets rotated

rolloutRestartTargets:

\- kind: StatefulSet

name: "hutch-postgresql"

\# Refresh interval

refreshAfter: 10m

\# Name of the CRD to authenticate to Vault

vaultAuthRef: default

\- apiVersion: secrets.hashicorp.com/v1beta1

kind: VaultStaticSecret

metadata:

name: hutch-rabbitmq

namespace: "{{.Release.Namespace }}"

spec:

\# Vault namespace where the secrets backend is

namespace: admin/deployments/hie-test-34

\# Vault mount path of the secrets backend

mount: secrets

\# Vault path in secrets engine mount to the secret

path: hutch

\# Type of the Vault static secret

type: kv-v2

\# Used for environment drift detection. Should always be on

hmacSecretData: true

\# Where to store the secrets, VSO will create the secret

destination:

create: true

name: hutch-rabbitmq

\# Transform thehyve secrets

transformation:

excludes:

\-.\*

templates:

rabbitmq-password:

text: '{{\`{{get.Secrets "rabbitmq\_admin\_password"}}\`}}'

rabbitmq-erlang-cookie:

text: '{{\`{{get.Secrets "rabbitmq\_erlang\_cookie"}}\`}}'

\# Restart these pods when secrets rotated

rolloutRestartTargets:

\- kind: StatefulSet

name: "hutch-rabbitmq"

\# Refresh interval

refreshAfter: 10m

\# Name of the CRD to authenticate to Vault

vaultAuthRef: default

\- apiVersion: secrets.hashicorp.com/v1beta1

kind: VaultStaticSecret

metadata:

name: relay-downstream-users

namespace: "{{.Release.Namespace }}"

spec:

\# Vault namespace where the secrets backend is

namespace: admin/deployments/hie-test-34

\# Vault mount path of the secrets backend

mount: secrets

\# Vault path in secrets engine mount to the secret

path: hutch

\# Type of the Vault static secret

type: kv-v2

\# Used for environment drift detection. Should always be on

hmacSecretData: true

\# Where to store the secrets, VSO will create the secret

destination:

create: true

name: relay-downstream-users

\# Transform thehyve secrets

transformation:

excludeRaw: true

excludes:

\-.\*

templates:

test\_user\_1\_password:

text: '{{\`{{get.Secrets "test\_user\_1\_password"}}\`}}'

\# Restart these pods when secrets rotated

rolloutRestartTargets:

\- kind: Deployment

name: '{{ include "hutch.relay.fullname". }}'

\# Refresh interval

refreshAfter: 10m

\# Name of the CRD to authenticate to Vault

vaultAuthRef: default

---

This updated `values.yaml` file looks spot on. You have successfully removed the unsupported `relay.downstreamUsers` block and correctly mapped the declarative configuration directly into the ASP.NET Core environment variables using `relay.extraEnvVars`.

The formatting for the `DownstreamUsers__test_user_1__Subnode` and the `secretKeyRef` for the password are both perfectly aligned with standard Kubernetes syntax and Hutch's expected configuration structure.

### Next Steps to Apply the Fix

1. Commit and Push: Save this file and push the commit to your `eoe-test-release` branch.
2. Sync ArgoCD: ArgoCD will either pick this up on its next polling cycle, or you can force it immediately with:
3. Verify the Rollout: Watch the pods in the `hutch` namespace. You should see a new `hutch-relay` pod spinning up with a brand new pod template hash in its name.

Because the `.NET` application will finally receive the `DownstreamUsers` block on startup, the `SubNodeService` will be able to seed the database properly, and the `CrashLoopBackOff` should be resolved.

Would you like me to stay on standby while you deploy this so we can check the logs of the newly spun-up pod together?

---

kubectl get pods -n hutch

NAME READY STATUS RESTARTS AGE

hutch-postgresql-0 1/1 Running 0 44h

hutch-rabbitmq-0 1/1 Running 0 43h

hutch-relay-5d449974dc-nzh58 0/1 CrashLoopBackOff 24 (43s ago) 94m

hutch-relay-6bc9f49f7c-plrsx 0/1 CrashLoopBackOff 1 (6s ago) 13s

awsadmin@ip-10-66-2-4:~$ argocd app sync argocd/hutch

{"execID":"69a17","level":"error","msg":"\`helm version --client --short\` failed exit status 1: Error: unknown flag: --client","time":"2026-02-19T12:39:14Z"}

TIMESTAMP GROUP KIND NAMESPACE NAME STATUS HEALTH HOOK MESSAGE

2026-02-19T12:39:14+00:00 Service hutch hutch-relay Synced Healthy

2026-02-19T12:39:14+00:00 ServiceAccount hutch hutch-postgresql Synced

2026-02-19T12:39:14+00:00 policy PodDisruptionBudget hutch hutch-postgresql Synced Healthy

2026-02-19T12:39:14+00:00 rbac.authorization.k8s.io Role hutch hutch-rabbitmq-endpoint-reader Synced

2026-02-19T12:39:14+00:00 secrets.hashicorp.com VaultStaticSecret hutch bunny Synced

2026-02-19T12:39:14+00:00 Service hutch hutch-postgresql Synced Healthy

2026-02-19T12:39:14+00:00 ServiceAccount hutch hutch-rabbitmq Synced

2026-02-19T12:39:14+00:00 apps Deployment hutch hutch-relay Synced Progressing

2026-02-19T12:39:14+00:00 apps StatefulSet hutch hutch-postgresql Synced Healthy

2026-02-19T12:39:14+00:00 policy PodDisruptionBudget hutch hutch-rabbitmq Synced Healthy

2026-02-19T12:39:14+00:00 secrets.hashicorp.com VaultStaticSecret hutch relay Synced

2026-02-19T12:39:14+00:00 Service hutch hutch-rabbitmq-headless Synced Healthy

2026-02-19T12:39:14+00:00 ServiceAccount hutch hutch-relay Synced

2026-02-19T12:39:14+00:00 networking.k8s.io NetworkPolicy hutch hutch-postgresql Synced

2026-02-19T12:39:14+00:00 networking.k8s.io NetworkPolicy hutch hutch-rabbitmq Synced

2026-02-19T12:39:14+00:00 rbac.authorization.k8s.io RoleBinding hutch hutch-rabbitmq-endpoint-reader Synced

2026-02-19T12:39:14+00:00 Secret hutch hutch-rabbitmq-config Synced

2026-02-19T12:39:14+00:00 Service hutch hutch-rabbitmq Synced Healthy

2026-02-19T12:39:14+00:00 apps StatefulSet hutch hutch-rabbitmq Synced Healthy

2026-02-19T12:39:14+00:00 secrets.hashicorp.com VaultStaticSecret hutch hutch-postgresql Synced

2026-02-19T12:39:14+00:00 secrets.hashicorp.com VaultStaticSecret hutch hutch-rabbitmq Synced

2026-02-19T12:39:14+00:00 Service hutch hutch-postgresql-hl Synced Healthy

2026-02-19T12:39:15+00:00 policy PodDisruptionBudget hutch hutch-rabbitmq Synced Healthy poddisruptionbudget.policy/hutch-rabbitmq configured

2026-02-19T12:39:15+00:00 ServiceAccount hutch hutch-relay Synced serviceaccount/hutch-relay unchanged

2026-02-19T12:39:15+00:00 Secret hutch hutch-rabbitmq-config Synced secret/hutch-rabbitmq-config unchanged

2026-02-19T12:39:15+00:00 Service hutch hutch-postgresql Synced Healthy service/hutch-postgresql configured

2026-02-19T12:39:15+00:00 apps StatefulSet hutch hutch-postgresql Synced Healthy statefulset.apps/hutch-postgresql configured

2026-02-19T12:39:15+00:00 apps StatefulSet hutch hutch-rabbitmq Synced Healthy statefulset.apps/hutch-rabbitmq configured

2026-02-19T12:39:15+00:00 secrets.hashicorp.com VaultStaticSecret hutch hutch-rabbitmq Synced vaultstaticsecret.secrets.hashicorp.com/hutch-rabbitmq unchanged

2026-02-19T12:39:15+00:00 Service hutch hutch-rabbitmq Synced Healthy service/hutch-rabbitmq configured

2026-02-19T12:39:15+00:00 networking.k8s.io NetworkPolicy hutch hutch-rabbitmq Synced networkpolicy.networking.k8s.io/hutch-rabbitmq configured

2026-02-19T12:39:15+00:00 networking.k8s.io NetworkPolicy hutch hutch-postgresql Synced networkpolicy.networking.k8s.io/hutch-postgresql configured

2026-02-19T12:39:15+00:00 ServiceAccount hutch hutch-rabbitmq Synced serviceaccount/hutch-rabbitmq unchanged

2026-02-19T12:39:15+00:00 rbac.authorization.k8s.io Role hutch hutch-rabbitmq-endpoint-reader Synced role.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader reconciled. role.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader unchanged

2026-02-19T12:39:15+00:00 rbac.authorization.k8s.io RoleBinding hutch hutch-rabbitmq-endpoint-reader Synced rolebinding.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader reconciled. rolebinding.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader unchanged

2026-02-19T12:39:15+00:00 apps Deployment hutch hutch-relay Synced Progressing deployment.apps/hutch-relay configured

2026-02-19T12:39:15+00:00 secrets.hashicorp.com VaultStaticSecret hutch bunny Synced vaultstaticsecret.secrets.hashicorp.com/bunny unchanged

2026-02-19T12:39:15+00:00 Service hutch hutch-rabbitmq-headless Synced Healthy service/hutch-rabbitmq-headless unchanged

2026-02-19T12:39:15+00:00 Service hutch hutch-relay Synced Healthy service/hutch-relay unchanged

2026-02-19T12:39:15+00:00 secrets.hashicorp.com VaultStaticSecret hutch relay Synced vaultstaticsecret.secrets.hashicorp.com/relay unchanged

2026-02-19T12:39:15+00:00 secrets.hashicorp.com VaultStaticSecret hutch hutch-postgresql Synced vaultstaticsecret.secrets.hashicorp.com/hutch-postgresql unchanged

2026-02-19T12:39:15+00:00 policy PodDisruptionBudget hutch hutch-postgresql Synced Healthy poddisruptionbudget.policy/hutch-postgresql configured

2026-02-19T12:39:15+00:00 ServiceAccount hutch hutch-postgresql Synced serviceaccount/hutch-postgresql unchanged

2026-02-19T12:39:15+00:00 Service hutch hutch-postgresql-hl Synced Healthy service/hutch-postgresql-hl unchanged

Name: argocd/hutch

Project: fitfile

Server: <https://kubernetes.default.svc>

Namespace: hutch

URL: <https://argocd.eoe-test-codisc.privatelink.fitfile.net/applications/argocd/hutch>

Source:

\- Repo: <https://gitlab.com/fitfile/deployment.git>

Target: eoe-test-release

Path: charts/hutch

Helm Values: /ffnodes/eoe/hie-test-34/hutch\_values.yaml

SyncWindow: Sync Allowed

Sync Policy: Automated (Prune)

Sync Status: Synced to eoe-test-release (e92d8ae)

Health Status: Progressing

Operation: Sync

Sync Revision: e92d8ae5334c1db1cd3d957913c9a3131f7e7995

Phase: Succeeded

Start: 2026-02-19 12:39:14 +0000 UTC

Finished: 2026-02-19 12:39:15 +0000 UTC

Duration: 1s

Message: successfully synced (all tasks run)

GROUP KIND NAMESPACE NAME STATUS HEALTH HOOK MESSAGE

networking.k8s.io NetworkPolicy hutch hutch-rabbitmq Synced networkpolicy.networking.k8s.io/hutch-rabbitmq configured

networking.k8s.io NetworkPolicy hutch hutch-postgresql Synced networkpolicy.networking.k8s.io/hutch-postgresql configured

policy PodDisruptionBudget hutch hutch-postgresql Synced Healthy poddisruptionbudget.policy/hutch-postgresql configured

policy PodDisruptionBudget hutch hutch-rabbitmq Synced Healthy poddisruptionbudget.policy/hutch-rabbitmq configured

ServiceAccount hutch hutch-postgresql Synced serviceaccount/hutch-postgresql unchanged

ServiceAccount hutch hutch-relay Synced serviceaccount/hutch-relay unchanged

ServiceAccount hutch hutch-rabbitmq Synced serviceaccount/hutch-rabbitmq unchanged

Secret hutch hutch-rabbitmq-config Synced secret/hutch-rabbitmq-config unchanged

rbac.authorization.k8s.io Role hutch hutch-rabbitmq-endpoint-reader Synced role.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader reconciled. role.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader unchanged

rbac.authorization.k8s.io RoleBinding hutch hutch-rabbitmq-endpoint-reader Synced rolebinding.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader reconciled. rolebinding.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader unchanged

Service hutch hutch-postgresql-hl Synced Healthy service/hutch-postgresql-hl unchanged

Service hutch hutch-rabbitmq-headless Synced Healthy service/hutch-rabbitmq-headless unchanged

Service hutch hutch-relay Synced Healthy service/hutch-relay unchanged

Service hutch hutch-rabbitmq Synced Healthy service/hutch-rabbitmq configured

Service hutch hutch-postgresql Synced Healthy service/hutch-postgresql configured

apps Deployment hutch hutch-relay Synced Progressing deployment.apps/hutch-relay configured

apps StatefulSet hutch hutch-postgresql Synced Healthy statefulset.apps/hutch-postgresql configured

apps StatefulSet hutch hutch-rabbitmq Synced Healthy statefulset.apps/hutch-rabbitmq configured

secrets.hashicorp.com VaultStaticSecret hutch bunny Synced vaultstaticsecret.secrets.hashicorp.com/bunny unchanged

secrets.hashicorp.com VaultStaticSecret hutch relay Synced vaultstaticsecret.secrets.hashicorp.com/relay unchanged

secrets.hashicorp.com VaultStaticSecret hutch hutch-postgresql Synced vaultstaticsecret.secrets.hashicorp.com/hutch-postgresql unchanged

secrets.hashicorp.com VaultStaticSecret hutch hutch-rabbitmq Synced vaultstaticsecret.secrets.hashicorp.com/hutch-rabbitmq unchanged

awsadmin@ip-10-66-2-4:~$ kubectl get pods -n hutch -w

NAME READY STATUS RESTARTS AGE

hutch-postgresql-0 1/1 Running 0 44h

hutch-rabbitmq-0 1/1 Running 0 43h

hutch-relay-5d449974dc-nzh58 0/1 CrashLoopBackOff 24 (2m8s ago) 95m

hutch-relay-6bc9f49f7c-plrsx 0/1 Completed 4 (44s ago) 98s

hutch-relay-6bc9f49f7c-plrsx 0/1 CrashLoopBackOff 4 (4s ago) 101s

---

I see exactly what is happening here, and it is a classic trap we all fall into!

If you look closely at the `Sync Revision` in your ArgoCD output, it says:`e92d8ae5334c1db1cd3d957913c9a3131f7e7995`

Now, if we look back at the very first message you sent me at the start of our debugging session, the sync status was:`Synced to eoe-test-release (e92d8ae)`

It is the exact same Git commit hash. You have perfectly updated the `hutch_values.yaml` file locally, but it has not been pushed to the GitLab repository yet.

Because ArgoCD pulls its source of truth directly from Git, your local `argocd app sync` command just told it to forcefully re-apply the old, broken configuration. This is also why the pod template hash in your terminal (`6bc9f49f7c`) hasn't budged.

### How to Fix It

You just need to push your local changes up to GitLab so ArgoCD can see them.

1. Go to the terminal or code editor where you modified the `hutch_values.yaml` file.
2. Stage and commit the file:
3. Push it to your target branch:
4. Finally, tell ArgoCD to synchronise the new commit:

Once you do this, you will see a brand new Git hash in the ArgoCD output, and Kubernetes will finally spin up a pod with the correct environment variables.

Would you like to run those Git commands and let me know when the new pod starts up?

---

argocd app sync argocd/hutch

{"execID":"b23f2","level":"error","msg":"\`helm version --client --short\` failed exit status 1: Error: unknown flag: --client","time":"2026-02-19T12:46:05Z"}

TIMESTAMP GROUP KIND NAMESPACE NAME STATUS HEALTH HOOK MESSAGE

2026-02-19T12:46:05+00:00 Service hutch hutch-rabbitmq-headless Synced Healthy

2026-02-19T12:46:05+00:00 Service hutch hutch-relay Synced Healthy

2026-02-19T12:46:05+00:00 ServiceAccount hutch hutch-rabbitmq Synced

2026-02-19T12:46:05+00:00 ServiceAccount hutch hutch-relay Synced

2026-02-19T12:46:05+00:00 apps Deployment hutch hutch-relay Synced Progressing

2026-02-19T12:46:05+00:00 rbac.authorization.k8s.io RoleBinding hutch hutch-rabbitmq-endpoint-reader Synced

2026-02-19T12:46:05+00:00 secrets.hashicorp.com VaultStaticSecret hutch hutch-rabbitmq Synced

2026-02-19T12:46:05+00:00 Service hutch hutch-postgresql Synced Healthy

2026-02-19T12:46:05+00:00 ServiceAccount hutch hutch-postgresql Synced

2026-02-19T12:46:05+00:00 apps StatefulSet hutch hutch-postgresql Synced Healthy

2026-02-19T12:46:05+00:00 apps StatefulSet hutch hutch-rabbitmq Synced Healthy

2026-02-19T12:46:05+00:00 networking.k8s.io NetworkPolicy hutch hutch-rabbitmq Synced

2026-02-19T12:46:05+00:00 rbac.authorization.k8s.io Role hutch hutch-rabbitmq-endpoint-reader Synced

2026-02-19T12:46:05+00:00 secrets.hashicorp.com VaultStaticSecret hutch bunny Synced

2026-02-19T12:46:05+00:00 secrets.hashicorp.com VaultStaticSecret hutch relay Synced

2026-02-19T12:46:05+00:00 Service hutch hutch-postgresql-hl Synced Healthy

2026-02-19T12:46:05+00:00 Service hutch hutch-rabbitmq Synced Healthy

2026-02-19T12:46:05+00:00 networking.k8s.io NetworkPolicy hutch hutch-postgresql Synced

2026-02-19T12:46:05+00:00 policy PodDisruptionBudget hutch hutch-postgresql Synced Healthy

2026-02-19T12:46:05+00:00 policy PodDisruptionBudget hutch hutch-rabbitmq Synced Healthy

2026-02-19T12:46:05+00:00 secrets.hashicorp.com VaultStaticSecret hutch hutch-postgresql Synced

2026-02-19T12:46:05+00:00 Secret hutch hutch-rabbitmq-config Synced

2026-02-19T12:46:05+00:00 secrets.hashicorp.com VaultStaticSecret hutch relay-downstream-users Synced

2026-02-19T12:46:07+00:00 Service hutch hutch-postgresql-hl Synced Healthy service/hutch-postgresql-hl unchanged

2026-02-19T12:46:07+00:00 Service hutch hutch-postgresql Synced Healthy service/hutch-postgresql configured

2026-02-19T12:46:07+00:00 secrets.hashicorp.com VaultStaticSecret hutch hutch-postgresql Synced vaultstaticsecret.secrets.hashicorp.com/hutch-postgresql unchanged

2026-02-19T12:46:07+00:00 secrets.hashicorp.com VaultStaticSecret hutch relay-downstream-users Synced vaultstaticsecret.secrets.hashicorp.com/relay-downstream-users unchanged

2026-02-19T12:46:07+00:00 networking.k8s.io NetworkPolicy hutch hutch-rabbitmq Synced networkpolicy.networking.k8s.io/hutch-rabbitmq configured

2026-02-19T12:46:07+00:00 policy PodDisruptionBudget hutch hutch-postgresql Synced Healthy poddisruptionbudget.policy/hutch-postgresql configured

2026-02-19T12:46:07+00:00 ServiceAccount hutch hutch-relay Synced serviceaccount/hutch-relay unchanged

2026-02-19T12:46:07+00:00 Secret hutch hutch-rabbitmq-config Synced secret/hutch-rabbitmq-config unchanged

2026-02-19T12:46:07+00:00 Service hutch hutch-rabbitmq-headless Synced Healthy service/hutch-rabbitmq-headless unchanged

2026-02-19T12:46:07+00:00 apps StatefulSet hutch hutch-postgresql Synced Healthy statefulset.apps/hutch-postgresql configured

2026-02-19T12:46:07+00:00 apps StatefulSet hutch hutch-rabbitmq Synced Healthy statefulset.apps/hutch-rabbitmq configured

2026-02-19T12:46:07+00:00 networking.k8s.io NetworkPolicy hutch hutch-postgresql Synced networkpolicy.networking.k8s.io/hutch-postgresql configured

2026-02-19T12:46:07+00:00 ServiceAccount hutch hutch-postgresql Synced serviceaccount/hutch-postgresql unchanged

2026-02-19T12:46:07+00:00 ServiceAccount hutch hutch-rabbitmq Synced serviceaccount/hutch-rabbitmq unchanged

2026-02-19T12:46:07+00:00 Service hutch hutch-rabbitmq Synced Healthy service/hutch-rabbitmq configured

2026-02-19T12:46:07+00:00 apps Deployment hutch hutch-relay Synced Progressing deployment.apps/hutch-relay configured

2026-02-19T12:46:07+00:00 secrets.hashicorp.com VaultStaticSecret hutch relay Synced vaultstaticsecret.secrets.hashicorp.com/relay unchanged

2026-02-19T12:46:07+00:00 secrets.hashicorp.com VaultStaticSecret hutch hutch-rabbitmq Synced vaultstaticsecret.secrets.hashicorp.com/hutch-rabbitmq unchanged

2026-02-19T12:46:07+00:00 Service hutch hutch-relay Synced Healthy service/hutch-relay unchanged

2026-02-19T12:46:07+00:00 policy PodDisruptionBudget hutch hutch-rabbitmq Synced Healthy poddisruptionbudget.policy/hutch-rabbitmq configured

2026-02-19T12:46:07+00:00 rbac.authorization.k8s.io Role hutch hutch-rabbitmq-endpoint-reader Synced role.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader reconciled. role.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader unchanged

2026-02-19T12:46:07+00:00 rbac.authorization.k8s.io RoleBinding hutch hutch-rabbitmq-endpoint-reader Synced rolebinding.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader reconciled. rolebinding.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader unchanged

2026-02-19T12:46:07+00:00 secrets.hashicorp.com VaultStaticSecret hutch bunny Synced vaultstaticsecret.secrets.hashicorp.com/bunny unchanged

Name: argocd/hutch

Project: fitfile

Server: <https://kubernetes.default.svc>

Namespace: hutch

URL: <https://argocd.eoe-test-codisc.privatelink.fitfile.net/applications/argocd/hutch>

Source:

\- Repo: <https://gitlab.com/fitfile/deployment.git>

Target: eoe-test-release

Path: charts/hutch

Helm Values: /ffnodes/eoe/hie-test-34/hutch\_values.yaml

SyncWindow: Sync Allowed

Sync Policy: Automated (Prune)

Sync Status: Synced to eoe-test-release (db745b9)

Health Status: Progressing

Operation: Sync

Sync Revision: db745b90ebe98e856c3ebb0ffe5bf95a85c40400

Phase: Succeeded

Start: 2026-02-19 12:46:05 +0000 UTC

Finished: 2026-02-19 12:46:07 +0000 UTC

Duration: 2s

Message: successfully synced (all tasks run)

GROUP KIND NAMESPACE NAME STATUS HEALTH HOOK MESSAGE

networking.k8s.io NetworkPolicy hutch hutch-postgresql Synced networkpolicy.networking.k8s.io/hutch-postgresql configured

networking.k8s.io NetworkPolicy hutch hutch-rabbitmq Synced networkpolicy.networking.k8s.io/hutch-rabbitmq configured

policy PodDisruptionBudget hutch hutch-rabbitmq Synced Healthy poddisruptionbudget.policy/hutch-rabbitmq configured

policy PodDisruptionBudget hutch hutch-postgresql Synced Healthy poddisruptionbudget.policy/hutch-postgresql configured

ServiceAccount hutch hutch-postgresql Synced serviceaccount/hutch-postgresql unchanged

ServiceAccount hutch hutch-rabbitmq Synced serviceaccount/hutch-rabbitmq unchanged

ServiceAccount hutch hutch-relay Synced serviceaccount/hutch-relay unchanged

Secret hutch hutch-rabbitmq-config Synced secret/hutch-rabbitmq-config unchanged

rbac.authorization.k8s.io Role hutch hutch-rabbitmq-endpoint-reader Synced role.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader reconciled. role.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader unchanged

rbac.authorization.k8s.io RoleBinding hutch hutch-rabbitmq-endpoint-reader Synced rolebinding.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader reconciled. rolebinding.rbac.authorization.k8s.io/hutch-rabbitmq-endpoint-reader unchanged

Service hutch hutch-rabbitmq-headless Synced Healthy service/hutch-rabbitmq-headless unchanged

Service hutch hutch-relay Synced Healthy service/hutch-relay unchanged

Service hutch hutch-postgresql-hl Synced Healthy service/hutch-postgresql-hl unchanged

Service hutch hutch-postgresql Synced Healthy service/hutch-postgresql configured

Service hutch hutch-rabbitmq Synced Healthy service/hutch-rabbitmq configured

apps Deployment hutch hutch-relay Synced Progressing deployment.apps/hutch-relay configured

apps StatefulSet hutch hutch-postgresql Synced Healthy statefulset.apps/hutch-postgresql configured

apps StatefulSet hutch hutch-rabbitmq Synced Healthy statefulset.apps/hutch-rabbitmq configured

secrets.hashicorp.com VaultStaticSecret hutch hutch-postgresql Synced vaultstaticsecret.secrets.hashicorp.com/hutch-postgresql unchanged

secrets.hashicorp.com VaultStaticSecret hutch relay-downstream-users Synced vaultstaticsecret.secrets.hashicorp.com/relay-downstream-users unchanged

secrets.hashicorp.com VaultStaticSecret hutch bunny Synced vaultstaticsecret.secrets.hashicorp.com/bunny unchanged

secrets.hashicorp.com VaultStaticSecret hutch relay Synced vaultstaticsecret.secrets.hashicorp.com/relay unchanged

secrets.hashicorp.com VaultStaticSecret hutch hutch-rabbitmq Synced vaultstaticsecret.secrets.hashicorp.com/hutch-rabbitmq unchanged

awsadmin@ip-10-66-2-4:~$ kubectl get pods -n hutch

NAME READY STATUS RESTARTS AGE

hutch-postgresql-0 1/1 Running 0 44h

hutch-rabbitmq-0 1/1 Running 0 44h

hutch-relay-5b695c4c7c-tcl82 0/1 Running 5 (87s ago) 3m9s

hutch-relay-6bc9f49f7c-plrsx 0/1 CrashLoopBackOff 6 (2m21s ago) 8m25s

awsadmin@ip-10-66-2-4:~$ kubectl get pods -n hutch

NAME READY STATUS RESTARTS AGE

hutch-postgresql-0 1/1 Running 0 44h

hutch-rabbitmq-0 1/1 Running 0 44h

hutch-relay-5b695c4c7c-tcl82 0/1 CrashLoopBackOff 5 (8s ago) 3m17s

hutch-relay-6bc9f49f7c-plrsx 0/1 CrashLoopBackOff 6 (2m29s ago) 8m33s

---

Brilliant, the Git push and ArgoCD sync worked perfectly! I can see the new commit hash (`db745b9`), and Kubernetes has successfully spun up a brand new pod with a new template hash (`5b695c4c7c`). We have officially moved forward.

However, as you can see, `hutch-relay-5b695c4c7c-tcl82` is still entering a `CrashLoopBackOff`.

In debugging, this usually means one of two things has happened:

1. We successfully bypassed the "no subnodes configured" error, but the application hit a completely new error further down the startup sequence (such as a database connection issue, invalid GUID format, or missing password from the Vault secret).
2. The `.NET` configuration parser _still_ doesn't like the way the `DownstreamUsers` variables are formatted.

To find out exactly what is happening, we need to inspect the logs of this newly generated pod.

Could you run these two commands and share the output?

We are definitely getting closer; let's see what the application is complaining about this time!

---

kubectl logs hutch-relay-5b695c4c7c-tcl82 -n hutch

kubectl describe pod hutch-relay-5b695c4c7c-tcl82 -n hutch

\_ \_ \_ \_ \_\_\_\_ \_

| | | | \_ \_ | |\_ \_\_\_ | |\_\_ | \_ \\ \_\_\_ | | \_\_ \_ \_ \_

| |\_| | | | | | | \_\_| / \_\_| | '\_ \\ | |\_) | / \_ \\ | | / \_\` | | | | |

| \_ | | |\_| | | |\_ | (\_\_ | | | | | \_ < | \_\_/ | | | (\_| | | |\_| |

|\_| |\_| \\\_\_,\_| \\\_\_| \\\_\_\_| |\_| |\_| |\_| \\\_\\ \\\_\_\_| |\_| \\\_\_,\_| \\\_\_, |

|\_\_\_/

\[12:46:21 INF\] Executed DbCommand (18ms) \[Parameters=\[\], CommandType='Text', CommandTimeout='30'\]

SELECT "MigrationId", "ProductVersion"

FROM "\_\_EFMigrationsHistory"

ORDER BY "MigrationId"; <s:Microsoft.EntityFrameworkCore.Database.Command>

\[12:46:21 INF\] Executed DbCommand (9ms) \[Parameters=\[\], CommandType='Text', CommandTimeout='30'\]

CREATE TABLE IF NOT EXISTS "\_\_EFMigrationsHistory" (

"MigrationId" character varying(150) NOT NULL,

"ProductVersion" character varying(32) NOT NULL,

CONSTRAINT "PK\_\_\_EFMigrationsHistory" PRIMARY KEY ("MigrationId")

); <s:Microsoft.EntityFrameworkCore.Database.Command>

\[12:46:21 INF\] Executed DbCommand (3ms) \[Parameters=\[\], CommandType='Text', CommandTimeout='30'\]

LOCK TABLE "\_\_EFMigrationsHistory" IN ACCESS EXCLUSIVE MODE <s:Microsoft.EntityFrameworkCore.Database.Command>

\[12:46:21 INF\] Executed DbCommand (1ms) \[Parameters=\[\], CommandType='Text', CommandTimeout='30'\]

SELECT "MigrationId", "ProductVersion"

FROM "\_\_EFMigrationsHistory"

ORDER BY "MigrationId"; <s:Microsoft.EntityFrameworkCore.Database.Command>

\[12:46:21 INF\] No migrations were applied. The database is already up to date. <s:Microsoft.EntityFrameworkCore.Migrations>

\[12:46:21 INF\] Executed DbCommand (4ms) \[Parameters=\[\], CommandType='Text', CommandTimeout='30'\]

SELECT a."Id", a."AccessFailedCount", a."ConcurrencyStamp", a."Discriminator", a."Email", a."EmailConfirmed", a."LockoutEnabled", a."LockoutEnd", a."NormalizedEmail", a."NormalizedUserName", a."PasswordHash", a."PhoneNumber", a."PhoneNumberConfirmed", a."SecurityStamp", a."TwoFactorEnabled", a."UserName", a."IsDeclared", s0."Id", s0."RelayUsersId", s0."SubNodesId"

FROM "AspNetUsers" AS a

LEFT JOIN (

SELECT s."Id", r."RelayUsersId", r."SubNodesId"

FROM "RelayUserSubNode" AS r

INNER JOIN "SubNodes" AS s ON r."SubNodesId" = s."Id"

) AS s0 ON a."Id" = s0."RelayUsersId"

WHERE a."Discriminator" = 'RelayUser'

ORDER BY a."Id", s0."RelayUsersId", s0."SubNodesId" <s:Microsoft.EntityFrameworkCore.Database.Command>

\[12:46:21 INF\] Executed DbCommand (7ms) \[Parameters=\[@\_\_NormalizeName\_0='?'\], CommandType='Text', CommandTimeout='30'\]

SELECT a0."Id", a0."AccessFailedCount", a0."ConcurrencyStamp", a0."Discriminator", a0."Email", a0."EmailConfirmed", a0."LockoutEnabled", a0."LockoutEnd", a0."NormalizedEmail", a0."NormalizedUserName", a0."PasswordHash", a0."PhoneNumber", a0."PhoneNumberConfirmed", a0."SecurityStamp", a0."TwoFactorEnabled", a0."UserName", a0."IsDeclared", s0."RelayUsersId", s0."SubNodesId", s0."Id"

FROM (

SELECT a."Id", a."AccessFailedCount", a."ConcurrencyStamp", a."Discriminator", a."Email", a."EmailConfirmed", a."LockoutEnabled", a."LockoutEnd", a."NormalizedEmail", a."NormalizedUserName", a."PasswordHash", a."PhoneNumber", a."PhoneNumberConfirmed", a."SecurityStamp", a."TwoFactorEnabled", a."UserName", a."IsDeclared"

FROM "AspNetUsers" AS a

WHERE a."Discriminator" = 'RelayUser' AND a."NormalizedUserName" = @\_\_NormalizeName\_0

LIMIT 2

) AS a0

LEFT JOIN (

SELECT r."RelayUsersId", r."SubNodesId", s."Id"

FROM "RelayUserSubNode" AS r

INNER JOIN "SubNodes" AS s ON r."SubNodesId" = s."Id"

) AS s0 ON a0."Id" = s0."RelayUsersId"

ORDER BY a0."Id", s0."RelayUsersId", s0."SubNodesId" <s:Microsoft.EntityFrameworkCore.Database.Command>

Unhandled exception: System.InvalidOperationException: User creation failed with errors for test\_user\_1.

at Hutch.Relay.Services.DeclarativeConfigService.ReconcileDownstreamUsers() in /src/app/Hutch.Relay/Services/DeclarativeConfigService.cs:line 117

at Hutch.Relay.Startup.Web.WebInitialisationService.Initialise() in /src/app/Hutch.Relay/Startup/Web/WebInitialisation.cs:line 26

at Hutch.Relay.Startup.Web.WebInitialisationExtensions.Initialise(WebApplication app) in /src/app/Hutch.Relay/Startup/Web/WebInitialisation.cs:line 46

at Hutch.Relay.Startup.Web.WebEntrypoint.Run(String\[\] args) in /src/app/Hutch.Relay/Startup/Web/WebEntrypoint.cs:line 22

at Hutch.Relay.Commands.Helpers.CliMiddlewareExtensions.<>c\_\_DisplayClass0\_0.<<UseRootCommandBypass>b\_\_0>d.MoveNext() in /src/app/Hutch.Relay/Commands/Helpers/CliMiddlewareExtensions.cs:line 22

\--- End of stack trace from previous location ---

at Hutch.Relay.Startup.Cli.CliEntrypoint.<>c.<<UseCliLogo>b\_\_1\_0>d.MoveNext() in /src/app/Hutch.Relay/Startup/Cli/CliEntrypoint.cs:line 34

\--- End of stack trace from previous location ---

at System.CommandLine.Builder.CommandLineBuilderExtensions.<>c\_\_DisplayClass12\_0.<<UseHelp>b\_\_0>d.MoveNext()

\--- End of stack trace from previous location ---

at System.CommandLine.Builder.CommandLineBuilderExtensions.<>c\_\_DisplayClass22\_0.<<UseVersionOption>b\_\_0>d.MoveNext()

\--- End of stack trace from previous location ---

at System.CommandLine.Builder.CommandLineBuilderExtensions.<>c\_\_DisplayClass19\_0.<<UseTypoCorrections>b\_\_0>d.MoveNext()

\--- End of stack trace from previous location ---

at System.CommandLine.Builder.CommandLineBuilderExtensions.<>c.<<UseSuggestDirective>b\_\_18\_0>d.MoveNext()

\--- End of stack trace from previous location ---

at System.CommandLine.Builder.CommandLineBuilderExtensions.<>c\_\_DisplayClass16\_0.<<UseParseDirective>b\_\_0>d.MoveNext()

\--- End of stack trace from previous location ---

at System.CommandLine.Builder.CommandLineBuilderExtensions.<>c.<<RegisterWithDotnetSuggest>b\_\_5\_0>d.MoveNext()

\--- End of stack trace from previous location ---

at System.CommandLine.Builder.CommandLineBuilderExtensions.<>c\_\_DisplayClass8\_0.<<UseExceptionHandler>b\_\_0>d.MoveNext()

Name: hutch-relay-5b695c4c7c-tcl82

Namespace: hutch

Priority: 0

Service Account: hutch-relay

Node: ip-10-66-7-80.eu-west-2.compute.internal/10.66.7.80

Start Time: Thu, 19 Feb 2026 12:43:12 +0000

Labels: app.kubernetes.io/instance=hutch

app.kubernetes.io/managed-by=Helm

app.kubernetes.io/name=relay

app.kubernetes.io/version=0.0.1

helm.sh/chart=hutch-0.1.0

pod-template-hash=5b695c4c7c

Annotations: kubectl.kubernetes.io/restartedAt: 2026-02-17T16:48:19Z

vso.secrets.hashicorp.com/restartedAt: 2026-02-17T15:58:27Z

Status: Running

IP: 10.66.6.141

IPs:

IP: 10.66.6.141

Controlled By: ReplicaSet/hutch-relay-5b695c4c7c

Containers:

relay:

Container ID: containerd://9a9df099ea7d5cc07ff7c01266f6fd00e599afdc19b4316cdcd7d7a2203aaafb

Image: fitfileregistry.azurecr.io/hutch/relay:1.0.1

Image ID: fitfileregistry.azurecr.io/hutch/relay@sha256:549c1c444bf998637eeb80f2430604df141dd100e6e6003e0a838e5c2b46648d

Ports: 8080/TCP (http), 8081/TCP (other)

Host Ports: 0/TCP (http), 0/TCP (other)

State: Waiting

Reason: CrashLoopBackOff

Last State: Terminated

Reason: Completed

Exit Code: 0

Started: Thu, 19 Feb 2026 12:46:19 +0000

Finished: Thu, 19 Feb 2026 12:46:21 +0000

Ready: False

Restart Count: 5

Limits:

cpu: 1

memory: 1Gi

Requests:

cpu: 500m

memory: 512Mi

Liveness: http-get http://:http/healthz delay=0s timeout=1s period=5s success=1 failure=5

Readiness: http-get http://:http/healthz delay=5s timeout=1s period=5s success=1 failure=3

Environment:

ConnectionStrings\_\_Default: <set to the key 'db\_connection\_string' in secret 'relay'> Optional: false

DOTNET\_Environment: Development

Database\_\_ApplyMigrationsOnStartup: true

DownstreamUsers\_\_test\_user\_1\_\_Password: <set to the key 'test\_user\_1\_password' in secret 'relay-downstream-users'> Optional: false

DownstreamUsers\_\_test\_user\_1\_\_Subnode: 019528e1-50cb-73a6-b624-70beb205a9bf

Logging\_\_LogLevel\_\_Default: Debug

Obfuscation\_\_LowNumberSuppressionThreshold: 0

Obfuscation\_\_RoundingTarget: 0

RelayTaskQueue\_\_ConnectionString: <set to the key 'rabbitmq\_connection\_string' in secret 'relay'> Optional: false

UpstreamTaskApi\_\_BaseUrl: <https://rquest.preprod.hdruk.cloud>

UpstreamTaskApi\_\_CollectionId: RQ-CC-563f7364-d8d5-4b10-b6ff-182b10b7cb7a

UpstreamTaskApi\_\_Enable: true

UpstreamTaskApi\_\_Password: <set to the key 'upstream\_task\_api\_password' in secret 'relay'> Optional: false

UpstreamTaskApi\_\_Username: <set to the key 'upstream\_task\_api\_username' in secret 'relay'> Optional: false

SubNodes\_\_test-node: placeholder-id

Mounts:

/var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-7zns7 (ro)

Conditions:

Type Status

PodReadyToStartContainers True

Initialized True

Ready False

ContainersReady False

PodScheduled True

Volumes:

kube-api-access-7zns7:

Type: Projected (a volume that contains injected data from multiple sources)

TokenExpirationSeconds: 3607

ConfigMapName: kube-root-ca.crt

Optional: false

DownwardAPI: true

QoS Class: Burstable

Node-Selectors: <none>

Tolerations: node.kubernetes.io/not-ready:NoExecute op=Exists for 300s

node.kubernetes.io/unreachable:NoExecute op=Exists for 300s

Events:

Type Reason Age From Message

\---- ------ ---- ---- -------

Normal Scheduled 4m22s default-scheduler Successfully assigned hutch/hutch-relay-5b695c4c7c-tcl82 to ip-10-66-7-80.eu-west-2.compute.internal

Normal Pulled 4m22s kubelet Successfully pulled image "fitfileregistry.azurecr.io/hutch/relay:1.0.1" in 145ms (145ms including waiting). Image size: 97562955 bytes.

Normal Pulled 4m19s kubelet Successfully pulled image "fitfileregistry.azurecr.io/hutch/relay:1.0.1" in 107ms (107ms including waiting). Image size: 97562955 bytes.

Normal Pulled 3m59s kubelet Successfully pulled image "fitfileregistry.azurecr.io/hutch/relay:1.0.1" in 146ms (146ms including waiting). Image size: 97562955 bytes.

Normal Pulled 3m26s kubelet Successfully pulled image "fitfileregistry.azurecr.io/hutch/relay:1.0.1" in 286ms (286ms including waiting). Image size: 97562955 bytes.

Normal Pulled 2m43s kubelet Successfully pulled image "fitfileregistry.azurecr.io/hutch/relay:1.0.1" in 182ms (182ms including waiting). Image size: 97562955 bytes.

Warning Unhealthy 2m42s (x3 over 4m17s) kubelet Liveness probe failed: Get "http://10.66.6.141:8080/healthz": dial tcp 10.66.6.141:8080: connect: connection refused

Normal Pulling 76s (x6 over 4m22s) kubelet Pulling image "fitfileregistry.azurecr.io/hutch/relay:1.0.1"

Normal Created 76s (x6 over 4m22s) kubelet Created container: relay

Normal Started 76s (x6 over 4m22s) kubelet Started container relay

Normal Pulled 76s kubelet Successfully pulled image "fitfileregistry.azurecr.io/hutch/relay:1.0.1" in 144ms (144ms including waiting). Image size: 97562955 bytes.

Warning BackOff 22s (x22 over 4m16s) kubelet Back-off restarting failed container relay in pod hutch-relay-5b695c4c7c-tcl82\_hutch(d634d518-a541-4ab1-b33b-f9e70ae4abad)

---

This is excellent news, even though it might not feel like it! We have successfully conquered the `There are no subnodes configured!` error.

The application is now seeing your `DownstreamUsers` configuration and is actively trying to seed the database with `test_user_1`. However, it is hitting a brand new error during that process.

If we look at the logs you just shared, we can see the exact point of failure:

> `Unhandled exception: System.InvalidOperationException: User creation failed with errors for test_user_1.``at Hutch.Relay.Services.DeclarativeConfigService.ReconcileDownstreamUsers()`

### The Likely Culprit: Password Complexity

Hutch is built on ASP.NET Core, which uses Microsoft's Identity framework for user management. By default, this framework enforces strict password complexity rules. When Hutch tries to create `test_user_1` on startup, it passes the password you stored in HashiCorp Vault (and synced to the `relay-downstream-users` Kubernetes secret).

If that password does not meet the minimum security requirements, the user creation will fail, and the application will crash.

Typically, the password must contain:

- At least 6 characters
- At least one uppercase letter (A-Z)
- At least one lowercase letter (a-z)
- At least one number (0-9)
- At least one special, non-alphanumeric character (e.g., `!`, `@`, `#`, `?`)

If your test password is just something simple like `password` or `test1234`, it will be rejected.

### How to Check and Fix This

Step 1: Check the current password Let's decode the password currently sitting in the Kubernetes secret to see if it meets the complexity requirements. Run this command:

Step 2: Update the Vault Secret (if needed) If the password is too simple, you will need to update it in your HashiCorp Vault instance (located at `admin/deployments/hie-test-34` under the `hutch` path, as defined in your Vault CRDs). Change it to something robust like `MySuperSecureP@ssw0rd!`.

Once Vault is updated, the `VaultStaticSecret` operator will automatically sync the new password into the Kubernetes secret within a few minutes, and the failing pod will automatically pick it up on its next restart loop and successfully create the user.

Would you mind running that `kubectl get secret` command to see what the current password is set to?

---

the password was completely missing. I have added a new key to the admin/deployments/hie-test-34 - test\_user\_1\_password

---

That makes perfect sense! A completely null or empty password would instantly trigger a validation failure in the application's user creation logic, leading to the exact crash you saw.

Now that you have added the key to HashiCorp Vault, the Vault Secrets Operator will pull it down into the cluster and update the Kubernetes secret.

Looking at your `hutch_values.yaml`, your `VaultStaticSecret` for `relay-downstream-users` is configured with a `refreshAfter: 10m` polling interval. It also has a `rolloutRestartTargets` configured, meaning once the operator spots the new secret in Vault, it should automatically restart your `hutch-relay` deployment.

If you don't want to wait around for the polling cycle, you can manually verify the sync and force the pod to restart.

### 1\. Check the Kubernetes Secret

Verify that the Vault operator has successfully pulled your new password into the cluster:

### 2\. Force the Pod to Restart

If the password prints out correctly, you can instantly kill the crashing pod. Kubernetes will immediately spin up a new one with the newly populated secret attached:

Would you like to run those commands and grab the logs of the newly spawned pod to confirm we have finally achieved a successful startup?

---

i need to make vso pick up the new secret

---

To force the HashiCorp Vault Secrets Operator (VSO) to immediately synchronise and bypass that 10-minute `refreshAfter` timer, you just need to trigger a reconciliation on the `VaultStaticSecret` custom resource.

The cleanest way to do this in Kubernetes is to inject or update a dummy annotation on the resource. The operator will see the metadata change and instantly re-fetch the secret from Vault.

### 1\. Force the VSO Sync

Run this command to annotate the `relay-downstream-users` Vault resource:

### 2\. Verify the Kubernetes Secret Updated

Give it a few seconds, then decode the Kubernetes secret to ensure VSO successfully pulled your new password down into the cluster:

### 3\. Watch the Rollout

Because your `hutch_values.yaml` perfectly configured the `rolloutRestartTargets` for this secret, VSO should automatically trigger a restart of the `hutch-relay` deployment the moment it detects the secret has changed.

You can watch the old crashing pod terminate and the new one spin up:

Once the new pod is running, grab the logs one last time (`kubectl logs -l app.kubernetes.io/name=relay -n hutch`). Fingers crossed, you should see it successfully run the database migrations, create `test_user_1`, and start the web host!

Would you like to share the logs once the new pod starts up to confirm it is completely healthy?

---

kubectl get secret relay-downstream-users -n hutch -o jsonpath='{.data.test\_user\_1\_password}' | base64 --decode

awsadmin@ip-10-66-2-4:~$ kubectl annotate vaultstaticsecret relay-downstream-users -n hutch force-sync=$(date +%s) --overwrite

vaultstaticsecret.secrets.hashicorp.com/relay-downstream-users annotated

awsadmin@ip-10-66-2-4:~$ kubectl get pods -n hutch

NAME READY STATUS RESTARTS AGE

hutch-postgresql-0 1/1 Running 0 44h

hutch-rabbitmq-0 1/1 Running 0 44h

hutch-relay-55bb744576-7vp99 1/1 Running 0 27s

awsadmin@ip-10-66-2-4:~$ kubectl get pods -n hutch

NAME READY STATUS RESTARTS AGE

hutch-postgresql-0 1/1 Running 0 44h

hutch-rabbitmq-0 1/1 Running 0 44h

hutch-relay-55bb744576-7vp99 1/1 Running 0 32s

---

Brilliant! Seeing `1/1 Running` with `0` restarts is exactly the result we have been working towards. You have officially fixed the deployment.

Here is exactly what happened in that sequence:

1. When you added the annotation, it forced the HashiCorp Vault Secrets Operator to instantly reach out to Vault and fetch your newly added `test_user_1_password`.
2. As soon as the Kubernetes secret was updated, the operator recognised the change and automatically triggered a rolling restart of the `hutch-relay` deployment (which is why your pod hash changed to `55bb744576`).
3. This time, the `.NET` application received the correct `DownstreamUsers` block _and_ a valid password. It successfully seeded the PostgreSQL database, created the user, and started the web host without crashing.

As a final victory lap, if you check the ArgoCD status now, it should finally show the application as completely green.

Would you like to run `argocd app get argocd/hutch` one last time to confirm the entire application has shifted from `Degraded` to `Healthy`?

---

give me a playbook wiki page for my notes of this work

---

Here is a structured playbook wiki page you can drop straight into your team's documentation or knowledge base. It covers the symptoms, the underlying architecture, and the exact steps to resolve the issue.

---

## Playbook: Debugging Hutch Relay CrashLoopBackOff

## Overview

This playbook addresses scenarios where the `argocd/hutch` application enters a `Degraded` state, specifically when the `hutch-relay` deployment is stuck in a `CrashLoopBackOff`.

This is typically caused by missing declarative configuration for subnodes in the Helm values or missing/invalid passwords in HashiCorp Vault. Because Hutch is built on ASP.NET Core, it requires these variables to successfully initialise and seed the PostgreSQL database on startup.

## Symptoms

- ArgoCD Status:`Degraded`
- Pod Status:`CrashLoopBackOff` for `hutch-relay-xxx`
- Pod Logs (`kubectl logs -l app.kubernetes.io/name=relay -n hutch`):
	- _Error 1:_`System.InvalidOperationException: There are no subnodes configured!`
	- _Error 2:_`Unhandled exception: System.InvalidOperationException: User creation failed with errors for test_user_1.`

## Root Cause Analysis

1. Unmapped Helm Values: The current version of the `hutch` Helm chart may not natively map the `relay.downstreamUsers` YAML block into the container's environment variables. This results in the `.NET` application receiving an empty configuration.
2. Incorrect Variable Format: ASP.NET Core expects nested configuration variables in a specific format (e.g., `DownstreamUsers__<username>__Subnode`). Using arbitrary names like `SubNodes__test-node` will be ignored.
3. Vault Secret Missing/Invalid: If the declarative user password stored in Vault is completely missing or fails Microsoft Identity's strict password complexity requirements (requires uppercase, lowercase, numbers, and special characters), the application will crash during the user seeding phase.

---

## Resolution Steps

### Step 1: Inject Declarative Configuration via extraEnvVars

Bypass the unsupported Helm blocks and forcefully inject the required ASP.NET Core environment variables.

Open your environment's values file (e.g., `/ffnodes/eoe/hie-test-34/hutch_values.yaml`), remove any existing `relay.downstreamUsers` block, and update the `relay.extraEnvVars` array:

### Step 2: Commit, Push, and Synchronise

ArgoCD relies entirely on the Git state. Ensure your changes are pushed to the remote repository branch configured in ArgoCD before attempting to sync.

### Step 3: Verify the HashiCorp Vault Secret

If the pod is still crashing with a `User creation failed` error, the password in Vault is missing or weak.

1. Add a complex password to the corresponding Vault path (e.g., `admin/deployments/hie-test-34`, key: `test_user_1_password`).
2. Force the Vault Secrets Operator (VSO) to immediately reconcile and pull the new secret into the cluster by annotating the `VaultStaticSecret` resource:

### Step 4: Verify the Rollout

Check that VSO has successfully populated the Kubernetes secret:

Because `rolloutRestartTargets` is configured in the Helm chart for this secret, VSO will automatically trigger a rolling restart of the `hutch-relay` pods. Watch the pods until they reach a `1/1 Running` state with `0` restarts:

---

Would you like me to format any other notes from our session, such as how to quickly decode and check the other Vault secrets (like RabbitMQ or PostgreSQL) if they ever cause similar startup issues?

---

yes

---

Here is a supplementary playbook section you can add to your wiki. This covers the architecture of how the secrets flow into your cluster, how to spot authentication crashes, and a cheat sheet of commands to instantly decode and verify every core secret in the Hutch stack.

---

## Playbook Appendix: Debugging Hutch Vault Secrets

## Overview: The Secret Pipeline

In the Hutch deployment architecture, secrets do not exist statically in Kubernetes. They follow a strict pipeline managed by the HashiCorp Vault Secrets Operator (VSO):

1. HashiCorp Vault: The absolute source of truth (e.g., `admin/deployments/hie-test-34`).
2. VaultStaticSecret (CRD): The Kubernetes resource that polls Vault (every 10 minutes) and templates the values.
3. Kubernetes Secret: The standard opaque secret generated by VSO.
4. Pod (`hutch-relay`, `hutch-postgresql`, etc.): Consumes the Kubernetes secret via environment variables or volume mounts.

If a pod crashes with an authentication error, the break is usually between Step 1 (Vault has the wrong password) or Step 2 (VSO hasn't synchronised the update yet).

## 1\. Spotting Secret-Related Crashes

If a pod is stuck in `CrashLoopBackOff`, check the logs (`kubectl logs <pod-name> -n hutch`). Secret mismatches usually look like this:

- PostgreSQL:`FATAL: password authentication failed for user`
- RabbitMQ:`AMQP connection failed: authentication failure` or `access_refused`
- Relay/Bunny:`.NET` exceptions complaining about missing connection strings, or `User creation failed with errors`.

## 2\. Checking VSO Sync Status

Before tearing down pods, verify that the Vault Secrets Operator is successfully communicating with your Vault server and synchronising the secrets.

_Look for the `STATUS` column to say `Synced`. If it says `AuthFailed` or `Error`, the cluster has lost its connection to HashiCorp Vault._

## 3\. The Secret Decoding Cheat Sheet

If you suspect a password is wrong, use these one-liners to instantly decode the active values currently sitting inside the Kubernetes cluster.

Relay Downstream Users (ASP.NET Core Identity):

PostgreSQL Admin Password:

RabbitMQ Admin Password & Erlang Cookie:

Relay Connection Strings (Templated by VSO):

## 4\. Forcing a Synchronisation and Restart

If you update a password in HashiCorp Vault, VSO will naturally take up to 10 minutes (defined by `refreshAfter: 10m`) to pull it down. To force an immediate synchronisation, annotate the target `VaultStaticSecret`.

Because your Helm charts are configured with `rolloutRestartTargets`, doing this will also automatically restart the affected pods so they pick up the new password immediately.

Command Template:

Examples:

---

Now that you have all the configuration and secret debugging documented, would you like me to help you review anything else in the cluster, or are you all set to continue your testing with the East of England environment?
