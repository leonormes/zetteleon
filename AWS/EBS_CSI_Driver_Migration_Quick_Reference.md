---
created: 2026-06-22T14:55:49+00:00
modified: 2026-07-20T16:33:34+00:00
permalink: llmeon/aws/ebs-csi-driver-migration-quick-reference
title: EBS_CSI_Driver_Migration_Quick_Reference
type: note
---

## EBS CSI Driver Policy Migration—Quick Reference

Last Updated: 16 June 2026

Status: Ready for Execution

---

### Summary

| Aspect | Detail |
|--------|--------|
| Affected Roles | 2 |
| Affected Clusters | 2 (eoe-sde-codisc, eoe-test-codisc) |
| Untagged Volumes | 9 |
| Migration Type | Managed Policy Swap |
| AWS Profile | eoe-hie |
| Region | eu-west-2 |
| Authorisation Level | ✅ Sufficient |

---

### Step-by-Step Migration

#### Phase 1: Pre-Migration Validation

```bash
# Confirm you can access AWS
aws sts get-caller-identity --profile eoe-hie

# Verify both roles exist and have legacy policy
aws iam list-attached-role-policies \
  --role-name eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --profile eoe-hie | grep -i ebscsi

aws iam list-attached-role-policies \
  --role-name eoe-test-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --profile eoe-hie | grep -i ebscsi
```

Expected Output: Should show `AmazonEBSCSIDriverPolicy` with ARN ending in `service-role/AmazonEBSCSIDriverPolicy`

---

#### Phase 2: Tag Untagged Volumes (CRITICAL)

Execute tagging for all 9 untagged volumes before policy migration:

```bash
# Volume vol-0f512bf32e7a77a79 (UNKNOWN CLUSTER — investigate first)
aws ec2 describe-volume-attribute --volume-id vol-0f512bf32e7a77a79 \
  --attribute attachmentSet --region eu-west-2 --profile eoe-hie

# High-risk volumes (determine cluster from tags or attachments)
aws ec2 create-tags \
  --resources vol-03c23f95447153a18 \
  --tags Key=ebs.csi.aws.com/cluster,Value=eoe-test-codisc \
  --region eu-west-2 --profile eoe-hie

aws ec2 create-tags \
  --resources vol-0ec0cf31c76b3e885 \
  --tags Key=ebs.csi.aws.com/cluster,Value=eoe-sde-codisc \
  --region eu-west-2 --profile eoe-hie

# Medium-risk volumes (extract cluster from eks:cluster-name tag)
for VOL in vol-0495ed05c42bdb021 vol-0834da1f3486fea9a vol-0a929e0fedba97937 \
           vol-045d9a2ba2ce0059c vol-084a2470987348115 vol-0c9b7bbfc0f08c77d; do
  CLUSTER=$(aws ec2 describe-volumes --volume-ids $VOL --region eu-west-2 \
    --profile eoe-hie --query 'Volumes[0].Tags[?Key==`eks:cluster-name`].Value' \
    --output text)
  aws ec2 create-tags --resources $VOL \
    --tags Key=ebs.csi.aws.com/cluster,Value=$CLUSTER \
    --region eu-west-2 --profile eoe-hie
done
```

Verification:

```bash
# Confirm all volumes now have CSI tags
aws ec2 describe-volumes \
  --region eu-west-2 --profile eoe-hie \
  --query 'Volumes[?Tags[?Key==`ebs.csi.aws.com/cluster`]].{VolumeId:VolumeId,Cluster:Tags[?Key==`ebs.csi.aws.com/cluster`]|[0].Value}' \
  --output table
```

---

#### Phase 3: Detach Legacy Policy

DO NOT PROCEED if EBS CSI pods are not healthy. Check first:

```bash
# For eoe-sde-codisc
kubectl get pods -n kube-system -l app=ebs-csi-controller \
  --context eoe-sde-codisc

# For eoe-test-codisc
kubectl get pods -n kube-system -l app=ebs-csi-controller \
  --context eoe-test-codisc
```

Detach legacy policy from both roles:

```bash
aws iam detach-role-policy \
  --role-name eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
  --profile eoe-hie

aws iam detach-role-policy \
  --role-name eoe-test-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
  --profile eoe-hie
```

---

#### Phase 4: Attach New Policy

Attach the cluster-scoped policy to both roles:

```bash
aws iam attach-role-policy \
  --role-name eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverEKSClusterScopedPolicy \
  --profile eoe-hie

aws iam attach-role-policy \
  --role-name eoe-test-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverEKSClusterScopedPolicy \
  --profile eoe-hie
```

---

#### Phase 5: Verify Policy Migration

```bash
# Verify new policy is attached
aws iam list-attached-role-policies \
  --role-name eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --profile eoe-hie | jq '.AttachedPolicies[] | {PolicyName, PolicyArn}'

aws iam list-attached-role-policies \
  --role-name eoe-test-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --profile eoe-hie | jq '.AttachedPolicies[] | {PolicyName, PolicyArn}'

# Both should show: AmazonEBSCSIDriverEKSClusterScopedPolicy
```

---

#### Phase 6: Restart EBS CSI Controller Pods

The pods need to re-authenticate with the new policy:

```bash
# For eoe-sde-codisc
kubectl delete pod -n kube-system -l app=ebs-csi-controller \
  --context eoe-sde-codisc

# For eoe-test-codisc
kubectl delete pod -n kube-system -l app=ebs-csi-controller \
  --context eoe-test-codisc

# Wait for pods to restart (should take 30-60 seconds)
sleep 60

# Verify pods are healthy
kubectl get pods -n kube-system -l app=ebs-csi-controller \
  --context eoe-sde-codisc

kubectl get pods -n kube-system -l app=ebs-csi-controller \
  --context eoe-test-codisc
```

---

#### Phase 7: Functional Testing

##### Test 1: Create a Test PVC

```bash
# For eoe-sde-codisc
kubectl apply -f - --context eoe-sde-codisc << 'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ebs-csi-test-sde
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: ebs-sc
  resources:
    requests:
      storage: 4Gi
EOF

# For eoe-test-codisc
kubectl apply -f - --context eoe-test-codisc << 'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ebs-csi-test-test
  namespace: default
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: ebs-sc
  resources:
    requests:
      storage: 4Gi
EOF
```

##### Test 2: Verify Volume Creation

```bash
# Check PVC status
kubectl get pvc ebs-csi-test-sde --context eoe-sde-codisc
kubectl get pvc ebs-csi-test-test --context eoe-test-codisc

# Verify AWS volume exists and is tagged
aws ec2 describe-volumes \
  --filters "Name=tag:ebs.csi.aws.com/cluster,Values=eoe-sde-codisc" \
  --region eu-west-2 --profile eoe-hie \
  --query 'Volumes[-1].{VolumeId:VolumeId,Size:Size,State:State}'
```

##### Test 3: Check Controller Logs

```bash
# For eoe-sde-codisc
kubectl logs -n kube-system -l app=ebs-csi-controller \
  --context eoe-sde-codisc | tail -20

# For eoe-test-codisc
kubectl logs -n kube-system -l app=ebs-csi-controller \
  --context eoe-test-codisc | tail -20
```

Look for: No error messages about permissions or authentication failures.

##### Test 4: Cleanup Test Volumes

```bash
# For eoe-sde-codisc
kubectl delete pvc ebs-csi-test-sde --context eoe-sde-codisc

# For eoe-test-codisc
kubectl delete pvc ebs-csi-test-test --context eoe-test-codisc
```

---

### Rollback (If Needed)

If issues occur, quickly revert to the legacy policy:

```bash
# Detach new policy
aws iam detach-role-policy \
  --role-name eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverEKSClusterScopedPolicy \
  --profile eoe-hie

aws iam detach-role-policy \
  --role-name eoe-test-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverEKSClusterScopedPolicy \
  --profile eoe-hie

# Re-attach legacy policy
aws iam attach-role-policy \
  --role-name eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
  --profile eoe-hie

aws iam attach-role-policy \
  --role-name eoe-test-codisc-AmazonEKS_EBS_CSI_DriverRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonEBSCSIDriverPolicy \
  --profile eoe-hie

# Restart pods
kubectl delete pod -n kube-system -l app=ebs-csi-controller --context eoe-sde-codisc
kubectl delete pod -n kube-system -l app=ebs-csi-controller --context eoe-test-codisc
```

---

### Troubleshooting

#### Issue: EBS CSI Pods Won't Start / CrashLoopBackOff

Symptom: Pods restart repeatedly, logs show authentication errors

Resolution:

1. Verify policy is attached: `aws iam list-attached-role-policies --role-name <ROLE> --profile eoe-hie`
2. Check IAM role trust policy hasn't changed: `aws iam get-role --role-name <ROLE> --profile eoe-hie`
3. If trust policy is wrong, execute rollback
4. Check service account annotation: `kubectl describe sa ebs-csi-controller-sa -n kube-system`

#### Issue: PVC Stuck in "Pending" sTate

Symptom: `kubectl get pvc` shows "Pending" despite having EBS storage class

Resolution:

1. Check controller pod logs: `kubectl logs -n kube-system -l app=ebs-csi-controller`
2. Look for "AccessDenied" or permission errors
3. Verify role has the new policy attached
4. Check security group allows EBS API calls (unlikely in managed EKS)

#### Issue: Existing Volumes Become Inaccessible

Symptom: Pods with mounted PVs fail to start; EBS errors in logs

Resolution:

1. This should not happen with cluster-scoped policy (broader permissions)
2. If it occurs, immediately rollback to legacy policy
3. Investigate why specific volume operations are failing
4. Contact AWS Support with full error logs

---

### Verification Checklist

- [ ] Pre-Migration
  - [ ] AWS CLI access confirmed
  - [ ] Both roles have legacy policy attached
  - [ ] EBS CSI pods healthy on both clusters
  - [ ] All volumes tagged with CSI cluster identifier
- [ ] Post-Migration
  - [ ] Legacy policy detached from both roles
  - [ ] Cluster-scoped policy attached to both roles
  - [ ] EBS CSI pods restarted and healthy
  - [ ] PVC creation test successful
  - [ ] No errors in controller logs
  - [ ] Existing volumes remain accessible

---

### Timeline Estimate

| Phase | Duration | Notes |
|-------|----------|-------|
| Pre-migration tagging | 10–15 min | Verify attachments and clusters |
| Policy detach | 1–2 min | Immediate |
| Policy attach | 1–2 min | Immediate |
| Pod restart | 1–2 min | Automatic, K8s handles |
| Verification testing | 10–15 min | Create test PVC, check logs |
| Total | ~30–40 min | Can be done in a single maintenance window |

---

### Success Criteria

✅ Migration complete when:

1. ✅ Both roles show `AmazonEBSCSIDriverEKSClusterScopedPolicy` attached
2. ✅ Legacy `AmazonEBSCSIDriverPolicy` is detached
3. ✅ All 9 volumes have CSI tags
4. ✅ EBS CSI controller pods show no errors
5. ✅ New PVC test successfully created and provisioned
6. ✅ Existing volumes remain in-use and accessible

---

Ready to execute. Please proceed with Phase 1 validation.
