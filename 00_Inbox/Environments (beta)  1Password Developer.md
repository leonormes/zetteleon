---
title: "Environments (beta) | 1Password Developer"
source: "https://developer.1password.com/docs/environments/"
author:
published:
created: 2026-01-07
description: "Learn how to use environments to simplify how you manage your environment variables and secrets."
tags:
  - "input"
---
## Environments Beta

1Password Environments provide the ability to store, organize, and manage project secrets in the form of environment variables from a dedicated location in 1Password. This creates a simplified process for accessing and syncing developer credentials stored in 1Password in development contexts and with other platforms. Each environment is self-contained, giving you the flexibility to organize your secrets by project, stage, application, or your own convention.

Use environments to import existing `.env` files, create an intuitive onboarding experience for your team to manage secrets, and more.

## Requirements

Before you can use Environments, you'll need to:

- [Sign up for 1Password](https://1password.com/pricing/password-manager).
- Install and sign in to 1Password for [Mac](https://1password.com/downloads/mac), [Windows](https://1password.com/downloads/windows), or [Linux](https://1password.com/downloads/linux).  
	This feature is not available in 1Password for iOS or Android.
- Have [1Password Developer turned on](https://developer.1password.com/docs/environments/#turn-on-1password-developer).

### Turn on 1Password Developer

1. Open and unlock the 1Password desktop app.
2. Select your account or collection at the top of the sidebar and choose **Settings** > [**Developer**](https://developer.1password.com/docs/environments/developers).
3. Turn on **Show 1Password Developer experience**.

## Create an environment

1. In the 1Password desktop app, go to **Developer** > **View Environments**.
2. Select **New environment**.
3. Enter a name for the new environment, then select **Save**. If you have multiple 1Password accounts, you can select which account to save the environment to.

### Manage an environment

If you want to rename or remove an environment, select **Manage Environment** from within that environment. Choose **Rename environment** or **Delete environment** as needed.

Deleted environments cannot be restored and any associated integrations will stop working. 1Password will prompt you to confirm whether or not you want to delete your environment before proceeding.

#### Add or remove users to an environment

If you're using a shared account, such as for a team or business, you can share environments with team members. Each environment remains independent, allowing you to work across multiple environments in different accounts while keeping environment variables separate. Access must be granted for each environment.

1. From your environment, select **Manage environment** > **Manage access**.
2. Select **Add People**, then search for and select the user you want to add to the environment. Select **Next**.
3. Select **View & Edit**, and choose whether the user can view, edit, and or manage the environment.
4. To remove a user from an environment, return to that user on the "Manage access" screen and select **Remove from environment**.

### Add variables

Variables are where key-value pairs are stored within 1Password Environments. From the Environments screen, select **View environment** for the environment you want to add variables for.

- If you have an existing `.env` file with the variable information you want to add to the Environment, select **Import.env file**. The information will automatically fill into the correct fields.
- To manually add environment variables, select **New variable**. Enter your key-value pair information to the **Name** and **Value** fields.

Select **New variable** to add additional key-value pairs to the same environment.

Values are hidden by default, but you can toggle the visibility on or off in the **Actions** column. You can also delete variables from this column. Select **Edit** within the environment to add, edit, or delete variables at a later time.

After you've added variables to an environment, you can use the Action column on the Variables screen within your environment to quickly copy your values without revealing them. Or, you can choose to reveal them.

## Destinations

Destinations are the places where you can use the variables in your environments. Right now, you can [sync environment variables to AWS Secrets Manager](https://developer.1password.com/docs/environments/aws-secrets-manager) or use [local `.env` file mounting](https://developer.1password.com/docs/environments/local-env-file) as a destination.

You can view, add, or edit destinations from the **Destination** tab within your environment. You might also need to configure settings within your destination.

## Learn more

- [Sync secrets between 1Password and AWS Secrets Manager (beta)](https://developer.1password.com/docs/environments/aws-secrets-manager)
- [Access secrets from 1Password through local `.env` files](https://developer.1password.com/docs/environments/local-env-file)