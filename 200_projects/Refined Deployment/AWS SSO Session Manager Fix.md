---
aliases: []
confidence: 
created: 2025-09-25T11:44:47Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:09Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [aws, iam, permissions, project/work/fitfile, session-manager, sso]
title: AWS SSO Session Manager Fix
type:
uid: 
updated: 
version:
---

## AWS SSO Session Manager Fix

**Date**: 2025-09-25
**Issue**: IAM user `tf-deployment` lacked permissions for AWS Systems Manager Session Manager
**Solution**: Configured AWS SSO authentication with broader permissions

### Problem

Original error when trying to start SSM session:

```sh
An error occurred (AccessDeniedException) when calling the StartSession operation: User: arn:aws:iam::135808916559:user/tf-deployment is not authorized to perform: ssm:StartSession on resource: arn:aws:ssm:eu-west-2:135808916559:document/SSM-SessionManagerRunShell
```

The `tf-deployment` IAM user in profile `eoe-hie` had very limited permissions and couldn't:

- Start SSM sessions
- List IAM policies
- Assume roles

### Solution Implemented

#### 1. AWS SSO Configuration

Added to `~/.aws/config`:

```ini
[sso-session fitfile]
sso_start_url = https://d-9c677d0fd8.awsapps.com/start/#
sso_region = eu-west-2
sso_registration_scopes = sso:account:access

[profile discovery-access]
region = eu-west-2
output = json
sso_session = fitfile
sso_account_id = 135808916559
sso_role_name = DiscoveryEngineeringAccess
```

#### 2. Authentication & Usage

**Initial login**:

```bash
aws sso login --profile discovery-access
```

**Using the profile**:

```bash
# Option 1: Use profile flag
aws ssm start-session --target i-09f84bb55556a2c10 --profile discovery-access

# Option 2: Set environment variable
export AWS_PROFILE=discovery-access
aws ssm start-session --target i-09f84bb55556a2c10
```

**Token refresh when expired**:

```bash
aws sso login --profile discovery-access
```

#### 3. Identity Verification

The SSO profile uses the role:

```sh
arn:aws:sts::135808916559:assumed-role/AWSReservedSSO_DiscoveryEngineeringAccess_b38ff0a73dfb5f6d/leon.ormes@fitfile.com
```

### Key Details

- **Account ID**: 135808916559
- **SSO Start URL**: <https://d-9c677d0fd8.awsapps.com/start/>#
- **Role**: AWSReservedSSO_DiscoveryEngineeringAccess_b38ff0a73dfb5f6d
- **Profile Name**: discovery-access
- **Region**: eu-west-2

### Files Modified

- `~/.aws/config` - Added SSO session and profile configuration
- Created `ssm-session-manager-policy.json` - Reference policy for required permissions

### Benefits

✅ **Security**: Uses temporary STS credentials instead of long-lived IAM user keys

✅ **Permissions**: SSO role has appropriate permissions for SSM Session Manager

✅ **Audit**: Better logging and tracking through SSO

✅ **Management**: Centralized permission management through AWS SSO

---

**Tags**:

## Files Modified

### Files Modified

- `~/.aws/config` - Added SSO session and profile configuration
- `~/.ssh/config` - Updated ProxyCommand to use `--profile discovery-access` instead of `--profile eoe-hie`
- Created `ssm-session-manager-policy.json` - Reference policy for required permissions

### SSH Configuration

Updated SSH config for `jumphost-ssm` host:

```bash
ProxyCommand sh -c "aws ssm start-session --target %h --region eu-west-2 --profile discovery-access --document-name AWS-StartSSHSession --parameters 'portNumber=22'"
```

**Usage**:

```bash
ssh jumphost-ssm
```

This now uses the AWS SSO profile with proper permissions instead of the limited IAM user.
