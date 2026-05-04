These tasks need to be performed by DevOps contributors who are responsible for the Central Services tooling.

The terraform for Central Services is found here: <https://gitlab.com/fitfile/terraform-infrastructure/production/central-services>

This customer deploy will be referenced with what we are calling a deployment-key. This is the short name FITFILE uses for the specific customer everywhere in the infrastructure. Do not use the full name of the customer but something like WM-Prod. Make sure to keep this consistent where ever you use it. It is important!

## Vault

To get the cluster effective outbound ip address, it depends on the outboundType assigned to the aks cluster. This guide details how to retrieve it if the type was set to `loadBalancer`

1. On your customer deployment repo, run `terraform output` and copy the ip address in the aks_cluster_outbound_ip_address 

   Example output:

   ```
   > terraform output
   aks_cluster_outbound_ip_address = "172.167.26.199"
   ```

   

2. Go to HCP Cloud portal: <https://portal.cloud.hashicorp.com/> 

3. Sign in if needed

4. Go to “Vault dedicated” and click on the vault cluster

5. In the Cluster networking section, click on the **Public** link

   

   ![image 1.png](image%201.png)

6. Click on “Add ip address”

   

7. Enter the ip address to whitelist, using the **32** mask (meaning, only whitelist that single ip address). Name it with the deployment key.

   

8. Click save (or add more if you need to). 

This will take up to **30 minutes**, so make sure you’ve added all the ips you intend to before clicking save!

1. Wait until the vault cluster has finished updating

   

### Create Vault Resources

Complete

This just creates empty secrets on vault.

Inside the Central Services repository, cd to hcp/vault

1. [Central Services](https://gitlab.com/fitfile/terraform-infrastructure/production/central-services)

2. Within [locals.tf](locals.tf) add a new block to the deployments variable. The secret objects to create may differ with each deployment, but generally for new deployments it will look like this:

   ```
   "<replace_with_deployment_key>" = {
     secrets = tomap({
       "application" = {},
       "spicedb" = {},
       "cloudflare" = {}, # only needed if using cloudflare
       "monitoring" = {}, # for grafana creds
     })
   }
   ```

   

3. Commit and push the change to trigger the terraform plan and apply in Terraform Cloud: <https://app.terraform.io/app/FITFILE-Platforms/workspaces/hcp-vault> 

4. A DevOps engineer will need to manually press the apply button on the Run page

5. Once the run has complete, now we need to set up the secrets. 

### Populate secrets 

Complete

At the time of writing this, SSO for the vault instance has not been set up, so the only way to login to vault is through the HCP portal: <https://portal.cloud.hashicorp.com/> and then navigating to the vault dedicated instance, and generating an admin token.

1. Login to HCP Portal: <https://portal.cloud.hashicorp.com/> and ensure you’re on the ops-project

   

2. Go to Vault Dedicated, then click on vault-cluster:

   

3. Click on Generate admin token and then click on the “Public“ web access link, which will open a new browser tab

   

4. Paste the token into the “Sign in Vault” form

   

5. Navigate to the deployments/<deployment-name> namespace

   

6. Go to secrets engines and click on secrets - You should see the secrets we created in the previous step.

   

7. Create a new version of each secret and populate the json secrets:

   

   

   

   **FOLLOW THE COMMENTS BESIDE EACH SECRET FOR HOW TO POPULATE THEM**\
   VAULT DOES NOT EXCEPT JSON WITH COMMENTS AND SO WILL NOT SAVE UNTIL THEY ARE REMOVED

   1. application secrets:

      ```
      {
        "cli_auth0_client_id": "", // Leave blank - do not need to fill
        "cli_auth0_client_secret": "", // Leave blank - do not need to fill
      
        "mesh_client_cert": "", // Leave blank if optout not required
        "mesh_client_key": "", // Leave blank if optout not required
        "mesh_hash_secret": "", // Leave blank if optout not required
        "mesh_mailbox_password": "", // Leave blank if optout not required
      
        "mongodb_password": "", // generate secure password (e.g. from LastPass) (min length 10, alphanumeric only)
        "mongodb_username": "root",
        "mongodb_replica_set_key": "", // generate secure password (length: 64, alphanumeric only)
      
        "postgresql_password": "", // generate secure password (e.g. from LastPass) (min length 10, alphanumeric only)
        "postgresql_username": "postgres",
      
        "s3_access_key_id": "ffadmin",
        "s3_secret_access_key": "", // generate secure password (min length 10, alphanumeric only)
      
        "ude_key": "", // generate from ude_cli using `key-gen` command. Needs to be same in all connected tenants
      
        "spicedb_pre_shared_key": "" // This may be different based on whether you use centralised spicedb or not. If centralised, get it from vault from admin/fitfile/production/spicedb_secrets. Otherwise, get from spicedb_secrets you will create
      }
      ```

      

   2. spicedb secrets:

      ```
      {
        "postgresql_password": "", // generate secure password (min length 10, alphanumeric only)
        "postgresql_username": "postgres",
        "spicedb_preshared_key": "" // generated and shared within application_secrets (min length 10, alphanumeric only)
      }
      ```

      

   3. cloudflare secrets (required if using cloudflare as DNS):\
      Generate from Cloudflare portal → Account → API Tokens. Ensure it has Edit DNS for the <http://fitfile.net>  zone. Name it appropriately, like <deployment-name>-challenge-token

      ```
      {
        "api_token": ""
      }
      ```

   

#### UDE secret generation

Complete

1. Checkout this repo: <https://gitlab.com/fitfile/ude-cli> 

2. Run this command:

   ```
   rustup install nightly
   ```

   This will install the nightly version of rust, required by the testing framework.

3. run cargo run -- key-gen - this will download dependencies, build the binary and run the keygen command. 

4. Copy the final line of the output, which should be a unique string

## Grafana

Complete

1. Go to the central services repo

2. cd to grafana

3. Open the [locals.tf](locals.tf) file

4. Add a new key value pair to the “deployments” local variable

   ```
   locals {
     ...
     deployments = tomap({
       ...
       "<replace-with-deployment-key>" = {
         stack = local.prod_stack # or local.non_prod_stack if not production
       }
     })
     ...
   }
   ```

   

5. Apply terraform

6. Get the terraform output with:

   ```
   terraform output -json
   ```

   You will need to reference this output later

7. Follow these [steps](#) to get to the secrets engine

8. Click on the monitoring secret and click “create new version”

9. Add the following values:

   ```
   {
     // Get from Central Services grafana module output
     "prometheus_host": "",
     "prometheus_username": "",
     "prometheus_password": "", // The access policy token for this deployment
     "loki_host": "",
     "loki_username": "",
     "loki_password": "", // The same access policy token for this deployment
     "tempo_host": "", // Ensure you add the port :443 on the end
     "tempo_username": "",
     "tempo_password": "" // The same access policy token for this deployment
   }
   ```

   ![image 2.png](image%202.png)

10. Save the secret


