---
aliases: []
confidence: 
created: 2025-10-23T10:59:32Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:14Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Untitled
type:
uid: 
updated: 
version:
---

**Command Executed:**

```bash
kubectl config current-context
```

**Output:**

```sh
arn:aws:eks:eu-west-2:135808916559:cluster/eoe-sde-codisc
```

**Command Executed:**

```bash
aws eks list-clusters --output json
```

**Output:**

```sh
{
    "clusters": [
        "eoe-sde-codisc"
    ]
}
```

**Command Executed:**

```bash
aws eks describe-cluster --name eoe-sde-codisc --query 'cluster.identity.oidc' --output json
```

**Output:**

```sh
{
    "issuer": "https://oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB"
}
```

**Command Executed:**

```bash
kubectl get sa -A -o json | jq -r '.items[] | select(.metadata.annotations["eks.amazonaws.com/role-arn"] != null) | "\(.metadata.namespace)/\(.metadata.name): \(.metadata.annotations["eks.amazonaws.com/role-arn"])"'
```

**Output:**

```sh
kube-system/aws-cluster-autoscaler-sa: arn:aws:iam::135808916559:role/eoe-sde-codisc-eks-cluster-autoscaler-role
kube-system/ebs-csi-controller-sa: arn:aws:iam::135808916559:role/eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole
```

**Command Executed:**

```bash
aws iam list-open-id-connect-providers --output json
```

**Output:**

```sh
{
    "OpenIDConnectProviderList": [
        {
            "Arn": "arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB"
        }
    ]
}
```

**Command Executed:**

```bash
kubectl get sa -n default -o yaml | grep -A5 "eks.amazonaws.com/role-arn" || echo "No IRSA-enabled service accounts in default namespace"
```

**Output:**

```sh
No IRSA-enabled service accounts in default namespace
```

**Command Executed:**

```bash
aws iam get-open-id-connect-provider --open-id-connect-provider-arn "arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB" --output json
```

**Output:**

```sh
{
    "Url": "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB",
    "ClientIDList": [
        "sts.amazonaws.com"
    ],
    "ThumbprintList": [
        "06b25927c42a721631c1efd9431e648fa62e1e39",
        "d9fe0a65fa00cabf61f5120d373a8135e1461f15",
        "9113c492911635f730e51f259f28873df5b7f01a"
    ],
    "CreateDate": "2025-02-14T17:49:20.280000+00:00",
    "Tags": [
        {
            "Key": "ProvisionByOrgName",
            "Value": "FITFILE"
        },
        {
            "Key": "branch",
            "Value": "master"
        },
        {
            "Key": "GitlabRepo",
            "Value": "gitlab.com/fitfile/customers/eoe/hie-sde-v2"
        },
        {
            "Key": "eks_cluster_name",
            "Value": "eoe-sde-codisc"
        }
    ]
}
```

**Command Executed:**

```bash
kubectl get ns -o name | wc -l
```

**Output:**

```sh
36
```

**Command Executed:**

```bash
aws iam list-roles --output json | jq -r '.Roles[] | select(.AssumeRolePolicyDocument != null) | select(.RoleName | contains("eoe-sde-codisc")) | .RoleName'
```

**Output:**

```sh
eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole
eoe-sde-codisc-cluster
eoe-sde-codisc-eks-cluster-autoscaler-role
eoe-sde-codisc-jumpbox-ssm-role
eoe-sde-codisc-node-group
```

**Command Executed:**

```bash
kubectl get ns | grep -i hyve || echo "No namespace containing 'hyve' found"
```

**Output:**

```sh
thehyve                         Active   245d
```

**Command Executed:**

```bash
kubectl get sa -n thehyve -o yaml
```

**Output:**

```sh
apiVersion: v1
items:
- apiVersion: v1
  automountServiceAccountToken: true
  imagePullSecrets:
  - name: fitfile-image-pull-secret
  kind: ServiceAccount
  metadata:
    creationTimestamp: "2025-02-19T12:44:29Z"
    name: default
    namespace: thehyve
    resourceVersion: "2044103"
    uid: 77dbf4ab-c24e-489f-a0dd-726a6d735723
- apiVersion: v1
  automountServiceAccountToken: true
  kind: ServiceAccount
  metadata:
    annotations:
      argocd.argoproj.io/tracking-id: thehyve:/ServiceAccount:thehyve/thehyve
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"v1","automountServiceAccountToken":true,"kind":"ServiceAccount","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"thehyve:/ServiceAccount:thehyve/thehyve"},"labels":{"app.kubernetes.io/instance":"thehyve","app.kubernetes.io/managed-by":"Helm","app.kubernetes.io/name":"thehyve","app.kubernetes.io/version":"0.0.3","helm.sh/chart":"thehyve-0.0.2"},"name":"thehyve","namespace":"thehyve"}}
    creationTimestamp: "2025-05-07T14:53:39Z"
    labels:
      app.kubernetes.io/instance: thehyve
      app.kubernetes.io/managed-by: Helm
      app.kubernetes.io/name: thehyve
      app.kubernetes.io/version: 0.0.3
      helm.sh/chart: thehyve-0.0.2
    name: thehyve
    namespace: thehyve
    resourceVersion: "166649455"
    uid: af4e183f-e1fe-43f9-a5e9-e751b7140acf
- apiVersion: v1
  automountServiceAccountToken: false
  kind: ServiceAccount
  metadata:
    annotations:
      argocd.argoproj.io/tracking-id: thehyve:/ServiceAccount:thehyve/thehyve-postgresql
      kubectl.kubernetes.io/last-applied-configuration: |
        {"apiVersion":"v1","automountServiceAccountToken":false,"kind":"ServiceAccount","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"thehyve:/ServiceAccount:thehyve/thehyve-postgresql"},"labels":{"app.kubernetes.io/instance":"thehyve","app.kubernetes.io/managed-by":"Helm","app.kubernetes.io/name":"postgresql","app.kubernetes.io/version":"16.3.0","helm.sh/chart":"postgresql-15.5.15"},"name":"thehyve-postgresql","namespace":"thehyve"}}
    creationTimestamp: "2025-05-07T14:53:39Z"
    labels:
      app.kubernetes.io/instance: thehyve
      app.kubernetes.io/managed-by: Helm
      app.kubernetes.io/name: postgresql
      app.kubernetes.io/version: 16.3.0
      helm.sh/chart: postgresql-15.5.15
    name: thehyve-postgresql
    namespace: thehyve
    resourceVersion: "166649456"
    uid: 99552a94-c91a-4655-9e8f-f9bffc3b5518
kind: List
metadata:
  resourceVersion: ""
```

**Command Executed:**

```bash
aws iam get-role --role-name eoe-sde-codisc-eks-cluster-autoscaler-role --output json | jq '.Role.AssumeRolePolicyDocument'
```

**Output:**

```sh
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:sub": "system:serviceaccount:kube-system:aws-cluster-autoscaler-sa"
        }
      }
    }
  ]
}
```

**Command Executed:**

```bash
kubectl get pods -n thehyve -o json | jq -r '.items[].spec.serviceAccountName' | sort -u
```

**Output:**

```sh
thehyve
thehyve-postgresql
```

**Command Executed:**

```bash
aws iam list-roles --output json | jq -r '.Roles[] | select(.RoleName | contains("hyve") or contains("thehyve")) | .RoleName'
```

**Output:**

```sh

```

**Command Executed:**

```bash
kubectl get deployment,statefulset -n thehyve -o yaml | grep -i "aws\|s3\|iam" || echo "No AWS/IAM references found in workload specs"
```

**Output:**

```sh
        {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"thehyve:apps/Deployment:thehyve/thehyve"},"labels":{"app.kubernetes.io/instance":"thehyve","app.kubernetes.io/managed-by":"Helm","app.kubernetes.io/name":"thehyve","app.kubernetes.io/version":"0.0.3","helm.sh/chart":"thehyve-0.0.2"},"name":"thehyve","namespace":"thehyve"},"spec":{"replicas":1,"selector":{"matchLabels":{"app.kubernetes.io/instance":"thehyve","app.kubernetes.io/name":"thehyve"}},"strategy":{"type":"Recreate"},"template":{"metadata":{"labels":{"app.kubernetes.io/instance":"thehyve","app.kubernetes.io/managed-by":"Helm","app.kubernetes.io/name":"thehyve","app.kubernetes.io/version":"0.0.3","helm.sh/chart":"thehyve-0.0.2"}},"spec":{"containers":[{"command":["airflow","webserver"],"env":[{"name":"AIRFLOW_ADMIN_EMAIL","valueFrom":{"secretKeyRef":{"key":"airflow_admin_email","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_FIRSTNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_firstname","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_LASTNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_lastname","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_PASSWORD","valueFrom":{"secretKeyRef":{"key":"airflow_admin_password","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_USERNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_username","name":"thehyve"}}},{"name":"AIRFLOW__CORE__EXECUTOR","value":"LocalExecutor"},{"name":"AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS","value":"False"},{"name":"AIRFLOW__CORE__LOAD_EXAMPLES","value":"False"},{"name":"AIRFLOW__CORE__SQL_ALCHEMY_CONN","valueFrom":{"secretKeyRef":{"key":"airflow_db_connection_string","name":"thehyve"}}},{"name":"AIRFLOW__CORE__STORE_DAG_CODE","value":"True"},{"name":"AIRFLOW__CORE__STORE_SERIALIZED_DAGS","value":"True"},{"name":"AIRFLOW__WEBSERVER__EXPOSE_CONFIG","value":"True"},{"name":"AIRFLOW__WEBSERVER__RBAC","value":"False"},{"name":"NHS_SITE","value":"cuh"},{"name":"OMOP_TARGET_DB","valueFrom":{"secretKeyRef":{"key":"omop_db_connection_string","name":"thehyve"}}},{"name":"QCR_ACCES_KEY_ID","valueFrom":{"secretKeyRef":{"key":"qcr_access_key_id","name":"thehyve"}}},{"name":"QCR_BUCKET","valueFrom":{"secretKeyRef":{"key":"qcr_bucket","name":"thehyve"}}},{"name":"QCR_IAM_ROLE","valueFrom":{"secretKeyRef":{"key":"qcr_iam_role","name":"thehyve"}}},{"name":"QCR_SECRET_ACCESS_KEY","valueFrom":{"secretKeyRef":{"key":"qcr_secret_access_key","name":"thehyve"}}}],"image":"fitfileregistry.azurecr.io/thehyve/fitfile_etl_container_cuh:0.4.1","imagePullPolicy":"Always","livenessProbe":{"httpGet":{"path":"/","port":8080},"initialDelaySeconds":10,"periodSeconds":10},"name":"webserver","ports":[{"containerPort":8080,"name":"http","protocol":"TCP"}],"readinessProbe":{"httpGet":{"path":"/","port":8080},"initialDelaySeconds":5,"periodSeconds":10},"resources":{"limits":{"cpu":"1","memory":"6Gi"},"requests":{"cpu":"250m","memory":"512Mi"}},"securityContext":{"runAsGroup":50000,"runAsUser":50000},"volumeMounts":[{"mountPath":"/tmp/reports","name":"reports"},{"mountPath":"/opt/airflow/logs","name":"log-volume"}]},{"command":["airflow","scheduler"],"env":[{"name":"AIRFLOW_ADMIN_EMAIL","valueFrom":{"secretKeyRef":{"key":"airflow_admin_email","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_FIRSTNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_firstname","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_LASTNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_lastname","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_PASSWORD","valueFrom":{"secretKeyRef":{"key":"airflow_admin_password","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_USERNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_username","name":"thehyve"}}},{"name":"AIRFLOW__CORE__EXECUTOR","value":"LocalExecutor"},{"name":"AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS","value":"False"},{"name":"AIRFLOW__CORE__LOAD_EXAMPLES","value":"False"},{"name":"AIRFLOW__CORE__SQL_ALCHEMY_CONN","valueFrom":{"secretKeyRef":{"key":"airflow_db_connection_string","name":"thehyve"}}},{"name":"AIRFLOW__CORE__STORE_DAG_CODE","value":"True"},{"name":"AIRFLOW__CORE__STORE_SERIALIZED_DAGS","value":"True"},{"name":"AIRFLOW__WEBSERVER__EXPOSE_CONFIG","value":"True"},{"name":"AIRFLOW__WEBSERVER__RBAC","value":"False"},{"name":"NHS_SITE","value":"cuh"},{"name":"OMOP_TARGET_DB","valueFrom":{"secretKeyRef":{"key":"omop_db_connection_string","name":"thehyve"}}},{"name":"QCR_ACCES_KEY_ID","valueFrom":{"secretKeyRef":{"key":"qcr_access_key_id","name":"thehyve"}}},{"name":"QCR_BUCKET","valueFrom":{"secretKeyRef":{"key":"qcr_bucket","name":"thehyve"}}},{"name":"QCR_IAM_ROLE","valueFrom":{"secretKeyRef":{"key":"qcr_iam_role","name":"thehyve"}}},{"name":"QCR_SECRET_ACCESS_KEY","valueFrom":{"secretKeyRef":{"key":"qcr_secret_access_key","name":"thehyve"}}}],"image":"fitfileregistry.azurecr.io/thehyve/fitfile_etl_container_cuh:0.4.1","imagePullPolicy":"Always","name":"scheduler","resources":{"limits":{"cpu":"1","memory":"6Gi"},"requests":{"cpu":"250m","memory":"512Mi"}},"securityContext":{"runAsGroup":50000,"runAsUser":50000},"volumeMounts":[{"mountPath":"/tmp/reports","name":"reports"}]}],"imagePullSecrets":[{"name":"fitfile-image-pull-secret"}],"initContainers":[{"args":["chown -R 50000:50000 /tmp/reports;\nairflow db upgrade \u0026\u0026 \\\nsleep 5 \u0026\u0026 \\\nairflow db init \u0026\u0026 \\\nairflow users create \\\n    --username $AIRFLOW_ADMIN_USERNAME \\\n    --password $AIRFLOW_ADMIN_PASSWORD \\\n    --firstname $AIRFLOW_ADMIN_FIRSTNAME \\\n    --lastname $AIRFLOW_ADMIN_LASTNAME \\\n    --role Admin \\\n    --email $AIRFLOW_ADMIN_EMAIL\n"],"command":["/bin/bash","-c"],"env":[{"name":"AIRFLOW_ADMIN_EMAIL","valueFrom":{"secretKeyRef":{"key":"airflow_admin_email","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_FIRSTNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_firstname","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_LASTNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_lastname","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_PASSWORD","valueFrom":{"secretKeyRef":{"key":"airflow_admin_password","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_USERNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_username","name":"thehyve"}}},{"name":"AIRFLOW__CORE__EXECUTOR","value":"LocalExecutor"},{"name":"AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS","value":"False"},{"name":"AIRFLOW__CORE__LOAD_EXAMPLES","value":"False"},{"name":"AIRFLOW__CORE__SQL_ALCHEMY_CONN","valueFrom":{"secretKeyRef":{"key":"airflow_db_connection_string","name":"thehyve"}}},{"name":"AIRFLOW__CORE__STORE_DAG_CODE","value":"True"},{"name":"AIRFLOW__CORE__STORE_SERIALIZED_DAGS","value":"True"},{"name":"AIRFLOW__WEBSERVER__EXPOSE_CONFIG","value":"True"},{"name":"AIRFLOW__WEBSERVER__RBAC","value":"False"},{"name":"NHS_SITE","value":"cuh"},{"name":"OMOP_TARGET_DB","valueFrom":{"secretKeyRef":{"key":"omop_db_connection_string","name":"thehyve"}}},{"name":"QCR_ACCES_KEY_ID","valueFrom":{"secretKeyRef":{"key":"qcr_access_key_id","name":"thehyve"}}},{"name":"QCR_BUCKET","valueFrom":{"secretKeyRef":{"key":"qcr_bucket","name":"thehyve"}}},{"name":"QCR_IAM_ROLE","valueFrom":{"secretKeyRef":{"key":"qcr_iam_role","name":"thehyve"}}},{"name":"QCR_SECRET_ACCESS_KEY","valueFrom":{"secretKeyRef":{"key":"qcr_secret_access_key","name":"thehyve"}}}],"image":"fitfileregistry.azurecr.io/thehyve/fitfile_etl_container_cuh:0.4.1","imagePullPolicy":"Always","name":"thehyve-init","securityContext":{"runAsUser":0},"volumeMounts":[{"mountPath":"/tmp/reports","name":"reports"}]}],"securityContext":{},"serviceAccountName":"thehyve","volumes":[{"name":"reports","persistentVolumeClaim":{"claimName":"thehyve-reports"}},{"emptyDir":{"sizeLimit":"500Mi"},"name":"log-volume"}]}}}}
          - name: QCR_IAM_ROLE
                key: qcr_iam_role
          - name: QCR_IAM_ROLE
                key: qcr_iam_role
          - name: QCR_IAM_ROLE
                key: qcr_iam_role
```

**Command Executed:**

```bash
aws eks describe-cluster --name eoe-sde-codisc --query 'cluster.[version,resourcesVpcConfig.clusterSecurityGroupId,roleArn]' --output json
```

**Output:**

```sh
[
    "1.33",
    "sg-02dcb1a5bbe8844b8",
    "arn:aws:iam::135808916559:role/eoe-sde-codisc-cluster"
]
```

**Command Executed:**

```bash
kubectl get secret -n thehyve -o json | jq -r '.items[].metadata.name' | grep -v "token\|docker\|pull-secret"
```

**Output:**

```sh
role-secrets
thehyve
thehyve-postgresql
thehyve-postgresql-init-db
```

**Command Executed:**

```bash
kubectl describe sa thehyve -n thehyve | grep -i "annotation\|label" -A5
```

**Output:**

```sh
Labels:              app.kubernetes.io/instance=thehyve
                     app.kubernetes.io/managed-by=Helm
                     app.kubernetes.io/name=thehyve
                     app.kubernetes.io/version=0.0.3
                     helm.sh/chart=thehyve-0.0.2
Annotations:         argocd.argoproj.io/tracking-id: thehyve:/ServiceAccount:thehyve/thehyve
Image pull secrets:  <none>
Mountable secrets:   <none>
Tokens:              <none>
Events:              <none>
```

**Command Executed:**

```bash
kubectl get secret role-secrets -n thehyve -o jsonpath='{.data}' | jq -r 'keys[]'
```

**Output:**

```sh
id
role_id
```

Perfect! I now have enough information to provide you with a comprehensive IRSA report. Let me summarize the findings:

## IRSA Investigation Report for `eoe-sde-codisc` Cluster

### Summary

The EKS cluster **has IRSA fully configured and operational**, but the `thehyve` namespace is **NOT currently using IRSA**. Instead, it appears to be using static AWS credentials stored in Kubernetes secrets.

---

### ✅ IRSA Infrastructure Status

**OIDC Provider:**

- **Status:** ✅ Configured and Active
- **Issuer:** `https://oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB`
- **IAM Provider ARN:** `arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB`
- **Client ID:** `sts.amazonaws.com`
- **Created:** February 14, 2025
- **Tags:** Provisioned by FITFILE for this cluster

---

### 📊 Current IRSA Usage

**Existing IRSA-Enabled Service Accounts:**

1. **kube-system/aws-cluster-autoscaler-sa**
   - Role: `arn:aws:iam::135808916559:role/eoe-sde-codisc-eks-cluster-autoscaler-role`
   - Purpose: Cluster autoscaling

2. **kube-system/ebs-csi-controller-sa**
   - Role: `arn:aws:iam::135808916559:role/eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole`
   - Purpose: EBS volume management

Both follow the standard IRSA pattern with trust policies using `AssumeRoleWithWebIdentity` and OIDC conditions.

---

### ❌ TheHyve Namespace Status

**Service Accounts in `thehyve` namespace:**

- `default`
- `thehyve` (used by main deployment)
- `thehyve-postgresql`

**IRSA Configuration:**

- ❌ No `eks.amazonaws.com/role-arn` annotation on any service account
- ❌ No IAM roles found with "hyve" or "thehyve" in the name

**Current AWS Credential Method:**
The `thehyve` deployment uses **static credentials from secrets**:

- Secret contains: `qcr_iam_role`, `qcr_access_key_id`, `qcr_secret_access_key`, `qcr_bucket`
- Environment variables: `QCR_IAM_ROLE`, `QCR_ACCES_KEY_ID`, `QCR_SECRET_ACCESS_KEY`, `QCR_BUCKET`

---

### 🔍 Cluster Details

- **Cluster Name:** `eoe-sde-codisc`
- **Region:** `eu-west-2`
- **Account:** `135808916559`
- **Kubernetes Version:** `1.33`
- **Namespace Count:** 36 namespaces

---

### 📝 Recommendations

To enable IRSA for `thehyve`, you would need to:

1. **Create an IAM role** with a trust policy referencing the OIDC provider
2. **Add appropriate permissions** to the role for AWS services `thehyve` needs to access
3. **Annotate the service account** with `eks.amazonaws.com/role-arn: <role-arn>`
4. **Update the deployment** to remove static credential environment variables
5. **Delete the static credentials** from the secret

The infrastructure is already in place - you just need to create the role and configure the service account annotation.

Suggest new conversation rejected for message

I'll create a comprehensive LLM prompt with all the context needed to implement IRSA for theHyve via Terraform.

**Command Executed:**

```bash
kubectl get deployment thehyve -n thehyve -o yaml
```

**Output:**

```sh
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    argocd.argoproj.io/tracking-id: thehyve:apps/Deployment:thehyve/thehyve
    deployment.kubernetes.io/revision: "17"
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"annotations":{"argocd.argoproj.io/tracking-id":"thehyve:apps/Deployment:thehyve/thehyve"},"labels":{"app.kubernetes.io/instance":"thehyve","app.kubernetes.io/managed-by":"Helm","app.kubernetes.io/name":"thehyve","app.kubernetes.io/version":"0.0.3","helm.sh/chart":"thehyve-0.0.2"},"name":"thehyve","namespace":"thehyve"},"spec":{"replicas":1,"selector":{"matchLabels":{"app.kubernetes.io/instance":"thehyve","app.kubernetes.io/name":"thehyve"}},"strategy":{"type":"Recreate"},"template":{"metadata":{"labels":{"app.kubernetes.io/instance":"thehyve","app.kubernetes.io/managed-by":"Helm","app.kubernetes.io/name":"thehyve","app.kubernetes.io/version":"0.0.3","helm.sh/chart":"thehyve-0.0.2"}},"spec":{"containers":[{"command":["airflow","webserver"],"env":[{"name":"AIRFLOW_ADMIN_EMAIL","valueFrom":{"secretKeyRef":{"key":"airflow_admin_email","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_FIRSTNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_firstname","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_LASTNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_lastname","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_PASSWORD","valueFrom":{"secretKeyRef":{"key":"airflow_admin_password","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_USERNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_username","name":"thehyve"}}},{"name":"AIRFLOW__CORE__EXECUTOR","value":"LocalExecutor"},{"name":"AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS","value":"False"},{"name":"AIRFLOW__CORE__LOAD_EXAMPLES","value":"False"},{"name":"AIRFLOW__CORE__SQL_ALCHEMY_CONN","valueFrom":{"secretKeyRef":{"key":"airflow_db_connection_string","name":"thehyve"}}},{"name":"AIRFLOW__CORE__STORE_DAG_CODE","value":"True"},{"name":"AIRFLOW__CORE__STORE_SERIALIZED_DAGS","value":"True"},{"name":"AIRFLOW__WEBSERVER__EXPOSE_CONFIG","value":"True"},{"name":"AIRFLOW__WEBSERVER__RBAC","value":"False"},{"name":"NHS_SITE","value":"cuh"},{"name":"OMOP_TARGET_DB","valueFrom":{"secretKeyRef":{"key":"omop_db_connection_string","name":"thehyve"}}},{"name":"QCR_ACCES_KEY_ID","valueFrom":{"secretKeyRef":{"key":"qcr_access_key_id","name":"thehyve"}}},{"name":"QCR_BUCKET","valueFrom":{"secretKeyRef":{"key":"qcr_bucket","name":"thehyve"}}},{"name":"QCR_IAM_ROLE","valueFrom":{"secretKeyRef":{"key":"qcr_iam_role","name":"thehyve"}}},{"name":"QCR_SECRET_ACCESS_KEY","valueFrom":{"secretKeyRef":{"key":"qcr_secret_access_key","name":"thehyve"}}}],"image":"fitfileregistry.azurecr.io/thehyve/fitfile_etl_container_cuh:0.4.1","imagePullPolicy":"Always","livenessProbe":{"httpGet":{"path":"/","port":8080},"initialDelaySeconds":10,"periodSeconds":10},"name":"webserver","ports":[{"containerPort":8080,"name":"http","protocol":"TCP"}],"readinessProbe":{"httpGet":{"path":"/","port":8080},"initialDelaySeconds":5,"periodSeconds":10},"resources":{"limits":{"cpu":"1","memory":"6Gi"},"requests":{"cpu":"250m","memory":"512Mi"}},"securityContext":{"runAsGroup":50000,"runAsUser":50000},"volumeMounts":[{"mountPath":"/tmp/reports","name":"reports"},{"mountPath":"/opt/airflow/logs","name":"log-volume"}]},{"command":["airflow","scheduler"],"env":[{"name":"AIRFLOW_ADMIN_EMAIL","valueFrom":{"secretKeyRef":{"key":"airflow_admin_email","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_FIRSTNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_firstname","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_LASTNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_lastname","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_PASSWORD","valueFrom":{"secretKeyRef":{"key":"airflow_admin_password","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_USERNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_username","name":"thehyve"}}},{"name":"AIRFLOW__CORE__EXECUTOR","value":"LocalExecutor"},{"name":"AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS","value":"False"},{"name":"AIRFLOW__CORE__LOAD_EXAMPLES","value":"False"},{"name":"AIRFLOW__CORE__SQL_ALCHEMY_CONN","valueFrom":{"secretKeyRef":{"key":"airflow_db_connection_string","name":"thehyve"}}},{"name":"AIRFLOW__CORE__STORE_DAG_CODE","value":"True"},{"name":"AIRFLOW__CORE__STORE_SERIALIZED_DAGS","value":"True"},{"name":"AIRFLOW__WEBSERVER__EXPOSE_CONFIG","value":"True"},{"name":"AIRFLOW__WEBSERVER__RBAC","value":"False"},{"name":"NHS_SITE","value":"cuh"},{"name":"OMOP_TARGET_DB","valueFrom":{"secretKeyRef":{"key":"omop_db_connection_string","name":"thehyve"}}},{"name":"QCR_ACCES_KEY_ID","valueFrom":{"secretKeyRef":{"key":"qcr_access_key_id","name":"thehyve"}}},{"name":"QCR_BUCKET","valueFrom":{"secretKeyRef":{"key":"qcr_bucket","name":"thehyve"}}},{"name":"QCR_IAM_ROLE","valueFrom":{"secretKeyRef":{"key":"qcr_iam_role","name":"thehyve"}}},{"name":"QCR_SECRET_ACCESS_KEY","valueFrom":{"secretKeyRef":{"key":"qcr_secret_access_key","name":"thehyve"}}}],"image":"fitfileregistry.azurecr.io/thehyve/fitfile_etl_container_cuh:0.4.1","imagePullPolicy":"Always","name":"scheduler","resources":{"limits":{"cpu":"1","memory":"6Gi"},"requests":{"cpu":"250m","memory":"512Mi"}},"securityContext":{"runAsGroup":50000,"runAsUser":50000},"volumeMounts":[{"mountPath":"/tmp/reports","name":"reports"}]}],"imagePullSecrets":[{"name":"fitfile-image-pull-secret"}],"initContainers":[{"args":["chown -R 50000:50000 /tmp/reports;\nairflow db upgrade \u0026\u0026 \\\nsleep 5 \u0026\u0026 \\\nairflow db init \u0026\u0026 \\\nairflow users create \\\n    --username $AIRFLOW_ADMIN_USERNAME \\\n    --password $AIRFLOW_ADMIN_PASSWORD \\\n    --firstname $AIRFLOW_ADMIN_FIRSTNAME \\\n    --lastname $AIRFLOW_ADMIN_LASTNAME \\\n    --role Admin \\\n    --email $AIRFLOW_ADMIN_EMAIL\n"],"command":["/bin/bash","-c"],"env":[{"name":"AIRFLOW_ADMIN_EMAIL","valueFrom":{"secretKeyRef":{"key":"airflow_admin_email","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_FIRSTNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_firstname","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_LASTNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_lastname","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_PASSWORD","valueFrom":{"secretKeyRef":{"key":"airflow_admin_password","name":"thehyve"}}},{"name":"AIRFLOW_ADMIN_USERNAME","valueFrom":{"secretKeyRef":{"key":"airflow_admin_username","name":"thehyve"}}},{"name":"AIRFLOW__CORE__EXECUTOR","value":"LocalExecutor"},{"name":"AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS","value":"False"},{"name":"AIRFLOW__CORE__LOAD_EXAMPLES","value":"False"},{"name":"AIRFLOW__CORE__SQL_ALCHEMY_CONN","valueFrom":{"secretKeyRef":{"key":"airflow_db_connection_string","name":"thehyve"}}},{"name":"AIRFLOW__CORE__STORE_DAG_CODE","value":"True"},{"name":"AIRFLOW__CORE__STORE_SERIALIZED_DAGS","value":"True"},{"name":"AIRFLOW__WEBSERVER__EXPOSE_CONFIG","value":"True"},{"name":"AIRFLOW__WEBSERVER__RBAC","value":"False"},{"name":"NHS_SITE","value":"cuh"},{"name":"OMOP_TARGET_DB","valueFrom":{"secretKeyRef":{"key":"omop_db_connection_string","name":"thehyve"}}},{"name":"QCR_ACCES_KEY_ID","valueFrom":{"secretKeyRef":{"key":"qcr_access_key_id","name":"thehyve"}}},{"name":"QCR_BUCKET","valueFrom":{"secretKeyRef":{"key":"qcr_bucket","name":"thehyve"}}},{"name":"QCR_IAM_ROLE","valueFrom":{"secretKeyRef":{"key":"qcr_iam_role","name":"thehyve"}}},{"name":"QCR_SECRET_ACCESS_KEY","valueFrom":{"secretKeyRef":{"key":"qcr_secret_access_key","name":"thehyve"}}}],"image":"fitfileregistry.azurecr.io/thehyve/fitfile_etl_container_cuh:0.4.1","imagePullPolicy":"Always","name":"thehyve-init","securityContext":{"runAsUser":0},"volumeMounts":[{"mountPath":"/tmp/reports","name":"reports"}]}],"securityContext":{},"serviceAccountName":"thehyve","volumes":[{"name":"reports","persistentVolumeClaim":{"claimName":"thehyve-reports"}},{"emptyDir":{"sizeLimit":"500Mi"},"name":"log-volume"}]}}}}
  creationTimestamp: "2025-05-07T14:53:39Z"
  generation: 18
  labels:
    app.kubernetes.io/instance: thehyve
    app.kubernetes.io/managed-by: Helm
    app.kubernetes.io/name: thehyve
    app.kubernetes.io/version: 0.0.3
    helm.sh/chart: thehyve-0.0.2
  name: thehyve
  namespace: thehyve
  resourceVersion: "166702724"
  uid: fb7f3077-b8ba-4581-907b-467be8bbd29a
spec:
  progressDeadlineSeconds: 600
  replicas: 1
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      app.kubernetes.io/instance: thehyve
      app.kubernetes.io/name: thehyve
  strategy:
    type: Recreate
  template:
    metadata:
      annotations:
        kubectl.kubernetes.io/restartedAt: "2025-10-23T09:05:46Z"
        vso.secrets.hashicorp.com/restartedAt: "2025-10-23T11:07:37Z"
      creationTimestamp: null
      labels:
        app.kubernetes.io/instance: thehyve
        app.kubernetes.io/managed-by: Helm
        app.kubernetes.io/name: thehyve
        app.kubernetes.io/version: 0.0.3
        helm.sh/chart: thehyve-0.0.2
    spec:
      containers:
      - command:
        - airflow
        - webserver
        env:
        - name: AIRFLOW_ADMIN_EMAIL
          valueFrom:
            secretKeyRef:
              key: airflow_admin_email
              name: thehyve
        - name: AIRFLOW_ADMIN_FIRSTNAME
          valueFrom:
            secretKeyRef:
              key: airflow_admin_firstname
              name: thehyve
        - name: AIRFLOW_ADMIN_LASTNAME
          valueFrom:
            secretKeyRef:
              key: airflow_admin_lastname
              name: thehyve
        - name: AIRFLOW_ADMIN_PASSWORD
          valueFrom:
            secretKeyRef:
              key: airflow_admin_password
              name: thehyve
        - name: AIRFLOW_ADMIN_USERNAME
          valueFrom:
            secretKeyRef:
              key: airflow_admin_username
              name: thehyve
        - name: AIRFLOW__CORE__EXECUTOR
          value: LocalExecutor
        - name: AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS
          value: "False"
        - name: AIRFLOW__CORE__LOAD_EXAMPLES
          value: "False"
        - name: AIRFLOW__CORE__SQL_ALCHEMY_CONN
          valueFrom:
            secretKeyRef:
              key: airflow_db_connection_string
              name: thehyve
        - name: AIRFLOW__CORE__STORE_DAG_CODE
          value: "True"
        - name: AIRFLOW__CORE__STORE_SERIALIZED_DAGS
          value: "True"
        - name: AIRFLOW__WEBSERVER__EXPOSE_CONFIG
          value: "True"
        - name: AIRFLOW__WEBSERVER__RBAC
          value: "False"
        - name: NHS_SITE
          value: cuh
        - name: OMOP_TARGET_DB
          valueFrom:
            secretKeyRef:
              key: omop_db_connection_string
              name: thehyve
        - name: QCR_ACCES_KEY_ID
          valueFrom:
            secretKeyRef:
              key: qcr_access_key_id
              name: thehyve
        - name: QCR_BUCKET
          valueFrom:
            secretKeyRef:
              key: qcr_bucket
              name: thehyve
        - name: QCR_IAM_ROLE
          valueFrom:
            secretKeyRef:
              key: qcr_iam_role
              name: thehyve
        - name: QCR_SECRET_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              key: qcr_secret_access_key
              name: thehyve
        image: fitfileregistry.azurecr.io/thehyve/fitfile_etl_container_cuh:0.4.1
        imagePullPolicy: Always
        livenessProbe:
          failureThreshold: 3
          httpGet:
            path: /
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 10
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        name: webserver
        ports:
        - containerPort: 8080
          name: http
          protocol: TCP
        readinessProbe:
          failureThreshold: 3
          httpGet:
            path: /
            port: 8080
            scheme: HTTP
          initialDelaySeconds: 5
          periodSeconds: 10
          successThreshold: 1
          timeoutSeconds: 1
        resources:
          limits:
            cpu: "1"
            memory: 6Gi
          requests:
            cpu: 250m
            memory: 512Mi
        securityContext:
          runAsGroup: 50000
          runAsUser: 50000
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /tmp/reports
          name: reports
        - mountPath: /opt/airflow/logs
          name: log-volume
      - command:
        - airflow
        - scheduler
        env:
        - name: AIRFLOW_ADMIN_EMAIL
          valueFrom:
            secretKeyRef:
              key: airflow_admin_email
              name: thehyve
        - name: AIRFLOW_ADMIN_FIRSTNAME
          valueFrom:
            secretKeyRef:
              key: airflow_admin_firstname
              name: thehyve
        - name: AIRFLOW_ADMIN_LASTNAME
          valueFrom:
            secretKeyRef:
              key: airflow_admin_lastname
              name: thehyve
        - name: AIRFLOW_ADMIN_PASSWORD
          valueFrom:
            secretKeyRef:
              key: airflow_admin_password
              name: thehyve
        - name: AIRFLOW_ADMIN_USERNAME
          valueFrom:
            secretKeyRef:
              key: airflow_admin_username
              name: thehyve
        - name: AIRFLOW__CORE__EXECUTOR
          value: LocalExecutor
        - name: AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS
          value: "False"
        - name: AIRFLOW__CORE__LOAD_EXAMPLES
          value: "False"
        - name: AIRFLOW__CORE__SQL_ALCHEMY_CONN
          valueFrom:
            secretKeyRef:
              key: airflow_db_connection_string
              name: thehyve
        - name: AIRFLOW__CORE__STORE_DAG_CODE
          value: "True"
        - name: AIRFLOW__CORE__STORE_SERIALIZED_DAGS
          value: "True"
        - name: AIRFLOW__WEBSERVER__EXPOSE_CONFIG
          value: "True"
        - name: AIRFLOW__WEBSERVER__RBAC
          value: "False"
        - name: NHS_SITE
          value: cuh
        - name: OMOP_TARGET_DB
          valueFrom:
            secretKeyRef:
              key: omop_db_connection_string
              name: thehyve
        - name: QCR_ACCES_KEY_ID
          valueFrom:
            secretKeyRef:
              key: qcr_access_key_id
              name: thehyve
        - name: QCR_BUCKET
          valueFrom:
            secretKeyRef:
              key: qcr_bucket
              name: thehyve
        - name: QCR_IAM_ROLE
          valueFrom:
            secretKeyRef:
              key: qcr_iam_role
              name: thehyve
        - name: QCR_SECRET_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              key: qcr_secret_access_key
              name: thehyve
        image: fitfileregistry.azurecr.io/thehyve/fitfile_etl_container_cuh:0.4.1
        imagePullPolicy: Always
        name: scheduler
        resources:
          limits:
            cpu: "1"
            memory: 6Gi
          requests:
            cpu: 250m
            memory: 512Mi
        securityContext:
          runAsGroup: 50000
          runAsUser: 50000
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /tmp/reports
          name: reports
      dnsPolicy: ClusterFirst
      imagePullSecrets:
      - name: fitfile-image-pull-secret
      initContainers:
      - args:
        - |
          chown -R 50000:50000 /tmp/reports;
          airflow db upgrade && \
          sleep 5 && \
          airflow db init && \
          airflow users create \
              --username $AIRFLOW_ADMIN_USERNAME \
              --password $AIRFLOW_ADMIN_PASSWORD \
              --firstname $AIRFLOW_ADMIN_FIRSTNAME \
              --lastname $AIRFLOW_ADMIN_LASTNAME \
              --role Admin \
              --email $AIRFLOW_ADMIN_EMAIL
        command:
        - /bin/bash
        - -c
        env:
        - name: AIRFLOW_ADMIN_EMAIL
          valueFrom:
            secretKeyRef:
              key: airflow_admin_email
              name: thehyve
        - name: AIRFLOW_ADMIN_FIRSTNAME
          valueFrom:
            secretKeyRef:
              key: airflow_admin_firstname
              name: thehyve
        - name: AIRFLOW_ADMIN_LASTNAME
          valueFrom:
            secretKeyRef:
              key: airflow_admin_lastname
              name: thehyve
        - name: AIRFLOW_ADMIN_PASSWORD
          valueFrom:
            secretKeyRef:
              key: airflow_admin_password
              name: thehyve
        - name: AIRFLOW_ADMIN_USERNAME
          valueFrom:
            secretKeyRef:
              key: airflow_admin_username
              name: thehyve
        - name: AIRFLOW__CORE__EXECUTOR
          value: LocalExecutor
        - name: AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS
          value: "False"
        - name: AIRFLOW__CORE__LOAD_EXAMPLES
          value: "False"
        - name: AIRFLOW__CORE__SQL_ALCHEMY_CONN
          valueFrom:
            secretKeyRef:
              key: airflow_db_connection_string
              name: thehyve
        - name: AIRFLOW__CORE__STORE_DAG_CODE
          value: "True"
        - name: AIRFLOW__CORE__STORE_SERIALIZED_DAGS
          value: "True"
        - name: AIRFLOW__WEBSERVER__EXPOSE_CONFIG
          value: "True"
        - name: AIRFLOW__WEBSERVER__RBAC
          value: "False"
        - name: NHS_SITE
          value: cuh
        - name: OMOP_TARGET_DB
          valueFrom:
            secretKeyRef:
              key: omop_db_connection_string
              name: thehyve
        - name: QCR_ACCES_KEY_ID
          valueFrom:
            secretKeyRef:
              key: qcr_access_key_id
              name: thehyve
        - name: QCR_BUCKET
          valueFrom:
            secretKeyRef:
              key: qcr_bucket
              name: thehyve
        - name: QCR_IAM_ROLE
          valueFrom:
            secretKeyRef:
              key: qcr_iam_role
              name: thehyve
        - name: QCR_SECRET_ACCESS_KEY
          valueFrom:
            secretKeyRef:
              key: qcr_secret_access_key
              name: thehyve
        image: fitfileregistry.azurecr.io/thehyve/fitfile_etl_container_cuh:0.4.1
        imagePullPolicy: Always
        name: thehyve-init
        resources: {}
        securityContext:
          runAsUser: 0
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
        volumeMounts:
        - mountPath: /tmp/reports
          name: reports
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      serviceAccount: thehyve
      serviceAccountName: thehyve
      terminationGracePeriodSeconds: 30
      volumes:
      - name: reports
        persistentVolumeClaim:
          claimName: thehyve-reports
      - emptyDir:
          sizeLimit: 500Mi
        name: log-volume
status:
  availableReplicas: 1
  conditions:
  - lastTransitionTime: "2025-10-23T11:08:59Z"
    lastUpdateTime: "2025-10-23T11:08:59Z"
    message: Deployment has minimum availability.
    reason: MinimumReplicasAvailable
    status: "True"
    type: Available
  - lastTransitionTime: "2025-05-07T14:53:39Z"
    lastUpdateTime: "2025-10-23T11:08:59Z"
    message: ReplicaSet "thehyve-68bd4dd57" has successfully progressed.
    reason: NewReplicaSetAvailable
    status: "True"
    type: Progressing
  observedGeneration: 18
  readyReplicas: 1
  replicas: 1
  updatedReplicas: 1
```

**Command Executed:**

```bash
kubectl get secret role-secrets -n thehyve -o jsonpath='{.data.qcr_iam_role}' | base64 -d && echo
```

**Output:**

```sh

```

**Command Executed:**

```bash
kubectl get secret thehyve -n thehyve -o jsonpath='{.data.qcr_iam_role}' | base64 -d && echo
```

**Output:**

```sh
arn:aws:iam::339713007003:role/dlz-tst-writer-codisc
```

**Command Executed:**

```bash
kubectl get secret thehyve -n thehyve -o jsonpath='{.data.qcr_bucket}' | base64 -d && echo
```

**Output:**

```sh
eoe-sde-prd-dqr-381492210920
```

**Command Executed:**

```bash
aws iam get-role --role-name eoe-sde-codisc-eks-cluster-autoscaler-role --output json | jq '{RoleName: .Role.RoleName, AssumeRolePolicyDocument: .Role.AssumeRolePolicyDocument, Tags: .Role.Tags}'
```

**Output:**

```sh
{
  "RoleName": "eoe-sde-codisc-eks-cluster-autoscaler-role",
  "AssumeRolePolicyDocument": {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Federated": "arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB"
        },
        "Action": "sts:AssumeRoleWithWebIdentity",
        "Condition": {
          "StringEquals": {
            "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:sub": "system:serviceaccount:kube-system:aws-cluster-autoscaler-sa"
          }
        }
      }
    ]
  },
  "Tags": [
    {
      "Key": "GitlabRepo",
      "Value": "gitlab.com/fitfile/customers/eoe/hie-sde-v2"
    },
    {
      "Key": "eks_cluster",
      "Value": "eoe-sde-codisc"
    },
    {
      "Key": "ProvisionByOrgName",
      "Value": "FITFILE"
    },
    {
      "Key": "branch",
      "Value": "master"
    }
  ]
}
```

Perfect! Now I have all the information needed. Let me create a comprehensive prompt for your IDE LLM:

---

## **LLM PROMPT: Enable IRSA for TheHyve on EKS Cluster**

### **Context**

I need to enable IAM Roles for Service Accounts (IRSA) for the `thehyve` application running in an EKS cluster. The cluster already has IRSA infrastructure configured, but the `thehyve` namespace is currently using static AWS credentials stored in Kubernetes secrets. I need to migrate to IRSA for better security.

---

### **Cluster Information**

- **Cluster Name:** `eoe-sde-codisc`
- **AWS Region:** `eu-west-2`
- **AWS Account ID:** `135808916559`
- **Kubernetes Version:** `1.33`
- **OIDC Provider:** Already configured
  - **Issuer URL:** `https://oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB`
  - **IAM OIDC Provider ARN:** `arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB`
  - **OIDC ID:** `23BDD27C5ECF85950BCEA129801871CB`

---

### **Current TheHyve Configuration**

#### **Namespace & Service Account**

- **Namespace:** `thehyve`
- **Service Account:** `thehyve`
- **Current Status:** No IRSA annotation on service account

#### **Current AWS Credential Method (to Be replaced)**

The deployment currently uses these environment variables from Kubernetes secrets:

- `QCR_IAM_ROLE` = `arn:aws:iam::339713007003:role/dlz-tst-writer-codisc` (cross-account role)
- `QCR_ACCES_KEY_ID` (static credential)
- `QCR_SECRET_ACCESS_KEY` (static credential)
- `QCR_BUCKET` = `eoe-sde-prd-dqr-381492210920`

**Note:** The application currently assumes a cross-account role (`339713007003`) to access resources.

#### **Application Details**

- **Image:** `fitfileregistry.azurecr.io/thehyve/fitfile_etl_container_cuh:0.4.1`
- **Type:** Apache Airflow deployment (webserver + scheduler containers)
- **Workload:** ETL container accessing S3 buckets

---

### **Working Example from This Cluster**

Here's an existing IRSA configuration in this cluster that works:

```json
{
  "RoleName": "eoe-sde-codisc-eks-cluster-autoscaler-role",
  "AssumeRolePolicyDocument": {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Federated": "arn:aws:iam::135808916559:oidc-provider/oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB"
        },
        "Action": "sts:AssumeRoleWithWebIdentity",
        "Condition": {
          "StringEquals": {
            "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB:sub": "system:serviceaccount:kube-system:aws-cluster-autoscaler-sa"
          }
        }
      }
    ]
  },
  "Tags": [
    {
      "Key": "GitlabRepo",
      "Value": "gitlab.com/fitfile/customers/eoe/hie-sde-v2"
    },
    { "Key": "eks_cluster", "Value": "eoe-sde-codisc" },
    { "Key": "ProvisionByOrgName", "Value": "FITFILE" },
    { "Key": "branch", "Value": "master" }
  ]
}
```

The service account annotation:

```yaml
metadata:
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::135808916559:role/eoe-sde-codisc-eks-cluster-autoscaler-role
```

---

### **Requirements**

#### **1. Create IAM Role with Terraform**

I need Terraform code to create an IAM role that:

1. **Allows the `thehyve` service account to assume it via IRSA**
   - Trust policy must reference the OIDC provider
   - Condition must match `system:serviceaccount:thehyve:thehyve`

2. **Has permissions to assume the cross-account role**
   - Must be able to call `sts:AssumeRole` on `arn:aws:iam::339713007003:role/dlz-tst-writer-codisc`

3. **Follows the naming convention:** `eoe-sde-codisc-thehyve-irsa-role`
4. **Has appropriate tags:**
   - `GitlabRepo`: `gitlab.com/fitfile/customers/eoe/hie-sde-v2`
   - `eks_cluster`: `eoe-sde-codisc`
   - `ProvisionByOrgName`: `FITFILE`
   - `branch`: `master`
   - `service_account`: `thehyve`
   - `namespace`: `thehyve`

#### **2. Kubernetes Service Account Annotation**

Provide Terraform code (using `kubernetes` provider or kubectl) to annotate the existing service account:

```yaml
metadata:
  annotations:
    eks.amazonaws.com/role-arn: <new-role-arn>
```

#### **3. Update the Cross-Account Role (if needed)**

Provide guidance or Terraform code to update the trust policy of `arn:aws:iam::339713007003:role/dlz-tst-writer-codisc` to allow the new IRSA role to assume it.

---

### **Architecture Flow**

```sh
Pod with Service Account "thehyve"
  ↓ (IRSA - automatic credential injection)
IAM Role: eoe-sde-codisc-thehyve-irsa-role (in account 135808916559)
  ↓ (sts:AssumeRole)
Cross-Account IAM Role: dlz-tst-writer-codisc (in account 339713007003)
  ↓ (permissions)
S3 Bucket: eoe-sde-prd-dqr-381492210920
```

---

### **Deliverables**

Please provide:

1. **Terraform code** to create the IRSA role in account `135808916559`
2. **Terraform code** to annotate the Kubernetes service account
3. **Trust policy JSON** or Terraform code for the cross-account role in account `339713007003`
4. **Instructions** on:
   - How the application code should be modified (if at all) to use IRSA
   - What environment variables to remove from the deployment
   - Testing steps to verify IRSA is working

---

### **Important Considerations**

- The OIDC provider is already configured - do not recreate it
- The service account `thehyve` already exists - only annotation is needed
- The application is managed by ArgoCD/Helm, so consider how to integrate changes
- The cross-account role trust policy will need to be updated in the target account
- Ensure the Terraform code uses data sources where appropriate (e.g., for existing OIDC provider)

---

### **Expected Terraform Structure**

Assume the Terraform code will be part of the infrastructure repository:

- Use appropriate data sources for existing resources
- Use variables for configurable values
- Follow AWS and Kubernetes provider best practices
- Include outputs for the role ARN

---

### **Additional Context**

- This is for a production-like environment (eoe-sde cluster)
- The application is Apache Airflow running ETL jobs
- Security is important - follow AWS least privilege principles
- The infrastructure is managed via GitLab CI/CD

---

**Please provide complete, production-ready Terraform code with explanations for each component.**

To tailor the Terraform to your repo patterns and avoid conflicts with Helm/Argo, I'll quickly inspect the `hie-sde-v2` infrastructure folder for any existing IRSA/OIDC patterns or Kubernetes provider usage. This helps me match naming, providers, and tagging conventions.

I'll open the key Terraform files in the [hie-sde-v2](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2:0:0-0:0) folder to align provider configuration, patterns, and naming (so the new IRSA code fits cleanly).

I'll inspect key Terraform files ([config.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2/config.tf:0:0-0:0), [main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2/main.tf:0:0-0:0), [variables.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2/variables.tf:0:0-0:0), and possibly `locals.tf`) to align with existing locals, tags, and provider patterns before proposing the new IRSA module code.

I'll scan the [modules/](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2/modules:0:0-0:0) folder to find any existing IRSA/IAM role patterns so the new code matches your current module structure and tagging conventions.

I'll open [main.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2/main.tf:0:0-0:0) to check if a Kubernetes provider is already configured and how the EKS cluster outputs are wired, so the service account annotation can be done consistently.

I'll quickly check [data.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2/data.tf:0:0-0:0) to confirm whether `data.aws_eks_cluster` and other data sources are already present, and to reuse existing patterns for EKS cluster info and AWS identity.

I will consult the Context7 documentation for Terraform AWS and Kubernetes providers to validate the correct resources and fields for IRSA trust policies and Kubernetes annotations.

## Plan

- **Create IAM role (IRSA)** in account `135808916559` named `eoe-sde-codisc-thehyve-irsa-role` with trust to the EKS OIDC provider and permission to assume the cross-account role.
- **Annotate the existing ServiceAccount** `thehyve` in namespace `thehyve` with the role ARN using the Kubernetes provider (import the existing SA into state).
- **Provide cross-account trust policy update** so role `dlz-tst-writer-codisc` in account `339713007003` trusts the new IRSA role.
- **Document app changes and tests** to verify IRSA.

All snippets align with your repo patterns and locals in [Production/hie-sde-v2](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2:0:0-0:0) (e.g., `local.name`, `local.region`, `local.tags`, and `module.eks.cluster_name` from [modules/eks/outputs.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2/modules/eks/outputs.tf:0:0-0:0)).

---

## 1) Terraform – IRSA Role for TheHyve

Create a new file, for example: `irsa_thehyve.tf`.

```hcl
############################################
# IRSA for thehyve
############################################

variable "thehyve_namespace" {
  type        = string
  description = "Namespace of the thehyve application"
  default     = "thehyve"
}

variable "thehyve_service_account_name" {
  type        = string
  description = "ServiceAccount name used by the thehyve application"
  default     = "thehyve"
}

variable "cross_account_role_arn" {
  type        = string
  description = "Target cross-account role to assume from the IRSA role"
  default     = "arn:aws:iam::339713007003:role/dlz-tst-writer-codisc"
}

# Optional: override if your cluster name is not from module.eks
# data "aws_eks_cluster" "this" will depend on module.eks.cluster_name
data "aws_eks_cluster" "this" {
  name       = module.eks.cluster_name
  depends_on = [module.eks]
}

# EKS publishes an issuer like "https://oidc.eks.eu-west-2.amazonaws.com/id/..."
# IAM OIDC provider ARN is "arn:aws:iam::<account-id>:oidc-provider/<issuer without https://>"
locals {
  # Issuer hostpath, e.g. "oidc.eks.eu-west-2.amazonaws.com/id/23BDD27C5ECF85950BCEA129801871CB"
  oidc_issuer_hostpath = replace(data.aws_eks_cluster.this.identity[0].oidc[0].issuer, "https://", "")

  oidc_provider_arn    = "arn:aws:iam::${local.aws_account_id}:oidc-provider/${local.oidc_issuer_hostpath}"

  # "system:serviceaccount:<namespace>:<sa>"
  thehyve_service_account_sub = "system:serviceaccount:${var.thehyve_namespace}:${var.thehyve_service_account_name}"

  # Merge standard tags with SA context
  thehyve_irsa_tags = merge(
    local.tags,
    {
      eks_cluster    = local.name
      service_account = var.thehyve_service_account_name
      namespace       = var.thehyve_namespace
    }
  )
}

# IAM role assumed by the ServiceAccount via IRSA
resource "aws_iam_role" "thehyve_irsa" {
  name = "${local.name}-thehyve-irsa-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Federated = local.oidc_provider_arn
        },
        Action = "sts:AssumeRoleWithWebIdentity",
        Condition = {
          StringEquals = {
            # bind to this specific ServiceAccount
            "${local.oidc_issuer_hostpath}:sub" = local.thehyve_service_account_sub
            # AWS strongly recommends also checking the audience
            "${local.oidc_issuer_hostpath}:aud" = "sts.amazonaws.com"
          }
        }
      }
    ]
  })

  tags = local.thehyve_irsa_tags
}

# Inline policy to allow assuming the cross-account role
data "aws_iam_policy_document" "thehyve_assume_cross_account" {
  statement {
    sid     = "AllowAssumeCrossAccountRole"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]
    resources = [
      var.cross_account_role_arn
    ]
  }
}

resource "aws_iam_role_policy" "thehyve_irsa_assume_cross_account" {
  name   = "allow-assume-dlz-tst-writer-codisc"
  role   = aws_iam_role.thehyve_irsa.id
  policy = data.aws_iam_policy_document.thehyve_assume_cross_account.json
}

output "thehyve_irsa_role_arn" {
  value       = aws_iam_role.thehyve_irsa.arn
  description = "IRSA role ARN to annotate on the ServiceAccount"
}
```

Notes:

- Uses existing locals from [config.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2/config.tf:0:0-0:0) (`local.name`, `local.tags`, `local.aws_account_id`, etc.).
- Trust policy matches `system:serviceaccount:thehyve:thehyve` and includes `aud: sts.amazonaws.com`.
- Role name: `eoe-sde-codisc-thehyve-irsa-role` (because `local.name = "eoe-sde-codisc"`).

---

## 2) Terraform – Annotate Existing ServiceAccount

Add the Kubernetes provider in [versions.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2/versions.tf:0:0-0:0) and provider config. Then manage the existing SA via import and set the annotation.

### 2.1 Required Providers (add to [versions.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2/versions.tf:0:0-0:0))

```hcl
terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = ">= 2.24"
    }
  }
}
```

### 2.2 Configure the Kubernetes Provider (in a New `k8s_provider.tf`)

```hcl
# EKS cluster data already declared in IRSA file
data "aws_eks_cluster_auth" "this" {
  name       = module.eks.cluster_name
  depends_on = [module.eks]
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.this.endpoint
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.this.certificate_authority[0].data)

  # Uses awscli to fetch auth token (requires awscli available in runner)
  exec {
    api_version = "client.authentication.k8s.io/v1beta1"
    command     = "aws"
    args        = ["eks", "get-token", "--cluster-name", module.eks.cluster_name, "--region", local.region]
  }
}
```

### 2.3 Manage and Annotate the Existing SA (in `thehyve_sa.tf`)

```hcl
resource "kubernetes_service_account_v1" "thehyve" {
  metadata {
    name      = var.thehyve_service_account_name
    namespace = var.thehyve_namespace
    annotations = {
      "eks.amazonaws.com/role-arn" = aws_iam_role.thehyve_irsa.arn
    }
  }

  # Avoid Terraform trying to control auto-managed SA fields
  automount_service_account_token = true

  # If Helm/Argo modifies `secrets` or `image_pull_secrets`, ignore those
  lifecycle {
    ignore_changes = [
      secret, image_pull_secrets, metadata[0].labels, metadata[0].annotations["kubectl.kubernetes.io/last-applied-configuration"]
    ]
  }

  depends_on = [module.eks, aws_iam_role.thehyve_irsa]
}
```

#### One-time Import (required)

Since the ServiceAccount already exists, import it before apply:

```bash
terraform import kubernetes_service_account_v1.thehyve thehyve/thehyve
```

If you prefer not to import, you can annotate via ArgoCD/Helm (recommended long-term) by adding:

```yaml
# values.yaml for the thehyve chart (pattern varies by chart)
serviceAccount:
  create: false # if SA is pre-created by you; true if the chart creates it
  name: thehyve
  annotations:
    eks.amazonaws.com/role-arn: arn:aws:iam::135808916559:role/eoe-sde-codisc-thehyve-irsa-role
```

This avoids Terraform/Helm ownership conflicts.

---

## 3) Cross-account Role Trust (Account 339713007003)

The target role must trust the new IRSA role to allow `sts:AssumeRole`.

### 3.1 Minimal Trust Policy JSON (to Add or merge)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "TrustEoeSdeCodiscThehyveIrsa",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::135808916559:role/eoe-sde-codisc-thehyve-irsa-role"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

### 3.2 Terraform Snippet (to Be Applied in account 339713007003)

```hcl
# In account 339713007003 workspace/profile
data "aws_iam_policy_document" "dlz_tst_writer_trust" {
  statement {
    sid     = "TrustEoeSdeCodiscThehyveIrsa"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::135808916559:role/eoe-sde-codisc-thehyve-irsa-role"]
    }
  }
}

resource "aws_iam_role" "dlz_tst_writer_codisc" {
  name               = "dlz-tst-writer-codisc"
  assume_role_policy = data.aws_iam_policy_document.dlz_tst_writer_trust.json
  # ... existing attached policies remain unchanged
}
```

If the cross-account role already has other trusted principals, merge this statement into the existing policy instead of replacing it.

---

## 4) Application Changes

- **Use AWS Default Credentials chain** in code (no code changes usually required if you use official AWS SDKs).
- **Remove these environment variables** from the deployment:
  - `QCR_ACCES_KEY_ID` (typo in name, but remove whichever variant exists)
  - `QCR_SECRET_ACCESS_KEY`
  - Any `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` static credentials
- **Keep (or set) these environment variables**:
  - `QCR_IAM_ROLE` = `arn:aws:iam::339713007003:role/dlz-tst-writer-codisc` (if your app explicitly reads this to decide which role to assume)
  - `QCR_BUCKET` = `eoe-sde-prd-dqr-381492210920`
  - `AWS_REGION` = `eu-west-2` (optional if SDK picks up region from the environment or kube config)
- The SDK will automatically use the projected web identity token from IRSA to obtain base credentials, then call `sts:AssumeRole` to the cross-account role.

---

## 5) Testing and Verification

- **Verify annotation**
  - `kubectl -n thehyve describe sa thehyve` → Check `eks.amazonaws.com/role-arn` is set to the new role.
- **Verify caller identity (base IRSA)**
  - Run a one-off debug pod:

```bash
kubectl -n thehyve run aws-cli --image=amazon/aws-cli:2.15.34 --serviceaccount=thehyve --restart=Never -it -- \
  sts get-caller-identity
```

- Should show `Arn` similar to `arn:aws:sts::135808916559:assumed-role/eoe-sde-codisc-thehyve-irsa-role/...`
- **Verify cross-account assume**

```bash
kubectl -n thehyve exec -it pod/aws-cli -- \
  sts assume-role --role-arn arn:aws:iam::339713007003:role/dlz-tst-writer-codisc --role-session-name thehyve-test --duration-seconds 900
```

- Export the returned temporary creds and then:

```bash
aws s3 ls s3://eoe-sde-prd-dqr-381492210920 --region eu-west-2
```

- **App-level smoke test**
  - Trigger an Airflow DAG or ETL task that touches S3 and confirm access succeeds without static creds.

---

## 6) Notes on ArgoCD/Helm Ownership

- If Helm manages the `ServiceAccount`, prefer setting the annotation in the chart values to avoid Terraform vs Helm drift.
- If Terraform must manage it, import the SA as shown and add `ignore_changes` for fields Helm might mutate.

---

## 7) What to Commit

- **New files**:
  - `irsa_thehyve.tf` (IAM role + policy)
  - `k8s_provider.tf` (Kubernetes provider)
  - `thehyve_sa.tf` (ServiceAccount resource)
- **Updated**:
  - [versions.tf](cci:7://file:///Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Production/hie-sde-v2/versions.tf:0:0-0:0) to add the Kubernetes provider

Run:

- `terraform init -upgrade`
- `terraform import kubernetes_service_account_v1.thehyve thehyve/thehyve`
- `terraform plan` → `terraform apply`

---

## Summary

- **IAM role created**: `eoe-sde-codisc-thehyve-irsa-role` with OIDC trust bound to `system:serviceaccount:thehyve:thehyve` and permission to `sts:AssumeRole` to `dlz-tst-writer-codisc`.
- **ServiceAccount annotated** via Terraform (with import) or via Helm values to avoid drift.
- **Cross-account trust**: JSON and Terraform provided to update role in `339713007003`.
- **App guidance and tests** provided to validate IRSA end-to-end.

**Subject:** Request for AWS Access Keys for Pod Testing (Temporary Measure)

Hi Keiran,

Could you please generate an AWS access key (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY) for the user(s) that need S3 write access for the current test deployment? My IAM permissions don’t allow me to create access keys myself (see attached error screenshot).

**Context:**

- In this initial phase, we need to provide static credentials via Kubernetes secrets so the pods can write to S3 using the current code/config.
- This is a stop-gap measure—static keys will be used *only until* we switch to the recommended IAM Role (IRSA/AssumeRole) approach, which will eliminate the need for long-term credentials.
- Once the basic workflow is validated, I’ll implement the pod-based AssumeRole setup for better security and key rotation.

Let me know if you need any additional info.

Thanks,  
Leon
