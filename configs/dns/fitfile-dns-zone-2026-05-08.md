---
title: fitfile.net DNS Zone
tags: [dns, bind, infra, fitfile, cloudflare]
date: 2026-05-08
source: Downloads
---

;;
;; Domain:     fitfile.net.
;; Exported:   2026-05-08 11:49:04
;;
;; This file is intended for use for informational and archival
;; purposes ONLY and MUST be edited before use on a production
;; DNS server.  In particular, you must:
;;   -- update the SOA record with the correct authoritative name server
;;   -- update the SOA record with the contact e-mail address information
;;   -- update the NS record(s) with the authoritative name servers for this domain.
;;
;; For further information, please consult the BIND documentation
;; located on the following website:
;;
;; http://www.isc.org/
;;
;; And RFC 1035:
;;
;; http://www.ietf.org/rfc/rfc1035.txt
;;
;; Please note that we do NOT offer technical support for any use
;; of this zone data, the BIND name server, or any other third-party
;; DNS software.
;;
;; Use at your own risk.
;; SOA Record
fitfile.net	3600	IN	SOA	aragorn.ns.cloudflare.com. dns.cloudflare.com. 2052990754 10000 2400 604800 3600

;; NS Records
fitfile.net.	86400	IN	NS	aragorn.ns.cloudflare.com.
fitfile.net.	86400	IN	NS	carioca.ns.cloudflare.com.

;; A Records
ac.fitfile.net.	1	IN	A	172.167.50.137 ; cf_tags=cf-proxied:true
acr-test-argocd.fitfile.net.	1	IN	A	172.167.48.42 ; cf_tags=cf-proxied:true
acr-test-argo-workflows.fitfile.net.	1	IN	A	172.167.48.42 ; cf_tags=cf-proxied:true
acr-test.fitfile.net.	1	IN	A	172.167.48.42 ; cf_tags=cf-proxied:true
app2.fitfile.net.	1	IN	A	172.167.50.137 ; cf_tags=cf-proxied:true
app3.fitfile.net.	1	IN	A	172.167.50.137 ; cf_tags=cf-proxied:true
app.fitfile.net.	1	IN	A	172.167.50.137 ; cf_tags=cf-proxied:true
app.testing.fitfile.net.	1	IN	A	172.167.216.23 ; For testing TLS certs from hashicorp vault cf_tags=cf-proxied:false
argocd.fitfile.net.	1	IN	A	172.167.50.137 ; cf_tags=cf-proxied:true
argocd-kch-mn2.fitfile.net.	1	IN	A	20.58.55.134 ; cf_tags=cf-proxied:true
argocd-kch-mn4.fitfile.net.	1	IN	A	20.117.102.187 ; cf_tags=cf-proxied:true
argocd.sandbox-testing-1.fitfile.net.	1	IN	A	20.117.146.221 ; cf_tags=cf-proxied:true
argocd-sh.fitfile.net.	1	IN	A	51.11.43.42 ; cf_tags=cf-proxied:true
argo-workflows.fitfile.net.	1	IN	A	172.167.50.137 ; cf_tags=cf-proxied:true
barts.fitfile.net.	1	IN	A	172.167.50.137 ; cf_tags=cf-proxied:true
cuh-poc-1.privatelink.fitfile.net.	1	IN	A	217.38.237.183 ; cf_tags=cf-proxied:false
cuh-prod-1.fitfile.net.	1	IN	A	217.38.237.183 ; cf_tags=cf-proxied:false
cuh-prod-1.privatelink.fitfile.net.	1	IN	A	217.38.237.183 ; cf_tags=cf-proxied:false
demo.fitfile.net.	1	IN	A	51.11.2.213 ; cf_tags=cf-proxied:true
dev-ac.fitfile.net.	1	IN	A	51.145.24.103 ; cf_tags=cf-proxied:true
dev-argocd.fitfile.net.	1	IN	A	51.145.24.103 ; cf_tags=cf-proxied:true
dev-argo-workflows.fitfile.net.	1	IN	A	51.145.24.103 ; cf_tags=cf-proxied:true
dev-storybook.fitfile.net.	1	IN	A	51.145.24.103 ; cf_tags=cf-proxied:true
echo.fitfile.net.	1	IN	A	131.145.24.249 ; cf_tags=cf-proxied:false
ff-dev-a.fitfile.net.	1	IN	A	51.145.24.103 ; cf_tags=cf-proxied:true
ff-test-a.fitfile.net.	1	IN	A	172.167.91.135 ; cf_tags=cf-proxied:true
ff-test-b.fitfile.net.	1	IN	A	172.167.91.135 ; cf_tags=cf-proxied:true
ff-test-c.fitfile.net.	1	IN	A	172.167.91.135 ; cf_tags=cf-proxied:true
ff-test-network.fitfile.net.	1	IN	A	51.104.228.71 ; cf_tags=cf-proxied:true
fitfile.net.	1	IN	A	35.214.23.206 ; cf_tags=cf-proxied:false
kch-mn4.fitfile.net.	1	IN	A	51.132.186.147 ; cf_tags=cf-proxied:true
kch-sandbox.fitfile.net.	1	IN	A	51.142.204.28 ; cf_tags=cf-proxied:true
lca-prd-2.fitfile.net.	1	IN	A	4.158.64.255 ; cf_tags=cf-proxied:false
mkuh-prd-4.fitfile.net.	1	IN	A	51.11.146.209 ; cf_tags=cf-proxied:false
mn5.fitfile.net.	1	IN	A	51.132.186.147 ; cf_tags=cf-proxied:true
mn5-kube.fitfile.net.	60	IN	A	51.132.186.147 ; cf_tags=cf-proxied:false
nb.fitfile.net.	1	IN	A	18.135.158.41 ; cf_tags=cf-proxied:false
nbtesting.fitfile.net.	1	IN	A	3.9.185.218 ; cf_tags=cf-proxied:false
nhs-provider-1-argocd.fitfile.net.	1	IN	A	172.167.30.85 ; cf_tags=cf-proxied:true
nhs-provider-1-argo-workflows.fitfile.net.	1	IN	A	172.167.30.85 ; cf_tags=cf-proxied:true
nhs-provider-1.fitfile.net.	1	IN	A	172.167.30.85 ; cf_tags=cf-proxied:true
nhs-provider-1.thehyve.fitfile.net.	1	IN	A	172.167.30.85 ; cf_tags=cf-proxied:true
nhs-provider-2-argocd.fitfile.net.	1	IN	A	172.167.42.203 ; cf_tags=cf-proxied:true
nhs-provider-2-argo-workflows.fitfile.net.	1	IN	A	172.167.42.203 ; cf_tags=cf-proxied:true
nhs-provider-2.fitfile.net.	1	IN	A	172.167.42.203 ; cf_tags=cf-proxied:true
nhs-provider-2.thehyve.fitfile.net.	1	IN	A	172.167.42.203 ; cf_tags=cf-proxied:true
nnuh-prod-1.fitfile.net.	1	IN	A	195.171.151.154 ; cf_tags=cf-proxied:false
old-ac.fitfile.net.	1	IN	A	51.11.2.213 ; For old production cluster cf_tags=cf-proxied:true
old-app2.fitfile.net.	1	IN	A	51.11.2.213 ; For old production cluster cf_tags=cf-proxied:true
old-app3.fitfile.net.	1	IN	A	51.11.2.213 ; For old production cluster cf_tags=cf-proxied:true
old-app.fitfile.net.	1	IN	A	51.11.2.213 ; For old production cluster cf_tags=cf-proxied:true
old-barts.fitfile.net.	1	IN	A	51.11.2.213 ; For old production cluster cf_tags=cf-proxied:true
oncology-demo.fitfile.net.	1	IN	A	51.11.2.213 ; cf_tags=cf-proxied:true
pentest-argocd.fitfile.net.	1	IN	A	20.162.255.100 ; cf_tags=cf-proxied:true
pentest-argo-workflows.fitfile.net.	1	IN	A	20.162.255.100 ; cf_tags=cf-proxied:true
pentest.fitfile.net.	1	IN	A	20.162.255.100 ; cf_tags=cf-proxied:true
prod-mongoweb.fitfile.net.	1	IN	A	51.11.2.213 ; cf_tags=cf-proxied:true
prod-pgweb.fitfile.net.	1	IN	A	172.167.50.137 ; cf_tags=cf-proxied:true
sandbox-testing-1.fitfile.net.	1	IN	A	20.117.146.221 ; cf_tags=cf-proxied:true
secrets.fitfile.net.	1	IN	A	51.132.47.130 ; cf_tags=cf-proxied:false
sh-sandbox.fitfile.net.	1	IN	A	51.11.43.42 ; cf_tags=cf-proxied:true
sonar.fitfile.net.	1	IN	A	51.11.153.23 ; cf_tags=cf-proxied:false
sonarqube.fitfile.net.	1	IN	A	51.11.153.23 ; cf_tags=cf-proxied:false
staging-ac.fitfile.net.	1	IN	A	172.167.91.135 ; cf_tags=cf-proxied:true
staging-argocd.fitfile.net.	1	IN	A	172.167.91.135 ; cf_tags=cf-proxied:true
staging-argo-workflows.fitfile.net.	1	IN	A	172.167.91.135 ; cf_tags=cf-proxied:true
staging.fitfile.net.	1	IN	A	172.166.204.72 ; cf_tags=cf-proxied:true
staging-ohdsi.fitfile.net.	1	IN	A	172.167.91.135 ; cf_tags=cf-proxied:true
storybook.fitfile.net.	1	IN	A	172.167.91.135 ; cf_tags=cf-proxied:true
test-ac.fitfile.net.	1	IN	A	51.145.44.190 ; cf_tags=cf-proxied:true
test-argocd.fitfile.net.	1	IN	A	51.145.44.190 ; cf_tags=cf-proxied:true
test-argo-workflows.fitfile.net.	1	IN	A	51.145.44.190 ; cf_tags=cf-proxied:true
testing-argocd.fitfile.net.	1	IN	A	172.167.216.23 ; cf_tags=cf-proxied:true
testing-argo-workflows.fitfile.net.	1	IN	A	172.167.216.23 ; cf_tags=cf-proxied:true
testing.fitfile.net.	1	IN	A	172.167.216.23 ; cf_tags=cf-proxied:true
vpn.fitfile.net.	1	IN	A	52.56.250.251 ; cf_tags=cf-proxied:false
vpntesting.fitfile.net.	1	IN	A	18.134.26.213 ; cf_tags=cf-proxied:false
www.fitfile.net.	1	IN	A	35.214.23.206 ; cf_tags=cf-proxied:false

;; CNAME Records
30519247.fitfile.net.	1	IN	CNAME	sendgrid.net. ; cf_tags=cf-proxied:false
_62631442aad08d1ebcf38c223e60e420.fitfile.net.	1	IN	CNAME	_eacf9513afbc73637834744b70e15128.xlfgrmvvlj.acm-validations.aws. ; cf_tags=cf-proxied:false
apples.fitfile.net.	1	IN	CNAME	ff-eoe-sde-relay-680202258.eu-west-2.elb.amazonaws.com. ; cf_tags=cf-proxied:false
_domainconnect.fitfile.net.	1	IN	CNAME	_domainconnect.gd.domaincontrol.com. ; cf_tags=cf-proxied:false
em6282.fitfile.net.	1	IN	CNAME	u30519247.wl248.sendgrid.net. ; cf_tags=cf-proxied:false
email.fitfile.net.	1	IN	CNAME	email.secureserver.net. ; cf_tags=cf-proxied:false
fitfile-api-docs.fitfile.net.	1	IN	CNAME	ssl.redocly.com. ; cf_tags=cf-proxied:false
ftp.fitfile.net.	1	IN	CNAME	fitfile.net. ; cf_tags=cf-proxied:false
s1._domainkey.fitfile.net.	1	IN	CNAME	s1.domainkey.u30519247.wl248.sendgrid.net. ; cf_tags=cf-proxied:false
s2._domainkey.fitfile.net.	1	IN	CNAME	s2.domainkey.u30519247.wl248.sendgrid.net. ; cf_tags=cf-proxied:false
url3851.fitfile.net.	1	IN	CNAME	sendgrid.net. ; cf_tags=cf-proxied:false

;; MX Records
fitfile.net.	1	IN	MX	0 smtp.secureserver.net.
fitfile.net.	1	IN	MX	10 mailstore1.secureserver.net.

;; NS Records
eoe.relay.fitfile.net.	1	IN	NS	ns-598.awsdns-10.net. ; cf_tags=eoe
eoe.relay.fitfile.net.	1	IN	NS	ns-1072.awsdns-06.org. ; cf_tags=eoe
eoe.relay.fitfile.net.	1	IN	NS	ns-2013.awsdns-59.co.uk. ; relay eoe delegation cf_tags=eoe
eoe.relay.fitfile.net.	1	IN	NS	ns-388.awsdns-48.com. ; adding relay dns delegation cf_tags=eoe

;; TXT Records
_acme-challenge.app2.fitfile.net.	120	IN	TXT	"15mscpmMUMJVk6xW5IupVBRwaJ2A8APGnTlipr0mImg"
_acme-challenge.app2.fitfile.net.	120	IN	TXT	"K1PiEpHjjZfB9JoWUQCq-IeAY1ChY1ILlE85FXFtEmQ"
_acme-challenge.app3.fitfile.net.	120	IN	TXT	"IF72MkC5s_yPd6Pk0ZWLqc2zwj3Y_pLovE7Sffu2oZc"
_acme-challenge.app3.fitfile.net.	120	IN	TXT	"2TGmhLnaH1aORCy21IM2Oo94f-ML4xHUwZlVmcHZ7uA"
_acme-challenge.app.fitfile.net.	120	IN	TXT	"NarhIiM-hhfW0TR4Y2y_HgQyIHRq6hA-uWsIH-Cx1co"
_acme-challenge.app.fitfile.net.	120	IN	TXT	"i6cq_qh-cicGmy9UmYA79lAdMbhdOEKP-MtBy9DbMh0"
_acme-challenge.argocd.fitfile.net.	120	IN	TXT	"yN_arUQ_G0-aPs4noMAD-QaAZyuOo7xtdFvhSIuJxfg"
_acme-challenge.argocd.fitfile.net.	120	IN	TXT	"aV1m7T-dNmrnAHCTJJopkj_SIdbA54P1QcCWlKUYYVk"
_acme-challenge.argo-workflows.fitfile.net.	120	IN	TXT	"uG30zu_G0V9AeKi_IbYHXmImrclsKjktamaoMO-lwsQ"
_acme-challenge.argo-workflows.fitfile.net.	120	IN	TXT	"nj-bcyx_DlYhZBWExG0LtfHveUqFFPFCgdqGb3-M1uY"
_acme-challenge.barts.fitfile.net.	120	IN	TXT	"evwi9FjmWb97o3zEIkxA0DqVWAgeLA9C7sW-ZnX_78w"
_acme-challenge.barts.fitfile.net.	120	IN	TXT	"KmA5rnSawDQxez3xgYCpVIHlcEMGbKq2LHBYnAOSRew"
_acme-challenge.ff-test-a.fitfile.net.	120	IN	TXT	"XPPDDoV7xUmk-yqbzFBR9kolmAyqQHow0E0QM5-MpKo"
_acme-challenge.ff-test-a.fitfile.net.	120	IN	TXT	"eJ1-4YpU8TKi4JzoUPy3Z9YzDCX_cjdCHKi5jr4BhOk"
_acme-challenge.ff-test-a.fitfile.net.	120	IN	TXT	"Vw36FkesBQ9D0HCtxCQkkaRKIWPMuaSHCWuNN31buDc"
_acme-challenge.ff-test-b.fitfile.net.	120	IN	TXT	"0JGNT4UfayNf5LqmyS1iLO7M_RTGvifcSKMKQq_fYIA"
_acme-challenge.ff-test-b.fitfile.net.	120	IN	TXT	"-wrfaA-t3LcKQgCmm93hXSwqemfmSxW5mQfE1gV-48k"
_acme-challenge.ff-test-b.fitfile.net.	120	IN	TXT	"4NauSULPwKHGM_m4-h_cIxu5NK2dwYWQWBfYAyAKYHA"
_acme-challenge.ff-test-c.fitfile.net.	120	IN	TXT	"nmgKahIyRHOWYAJW1mTQuJzP0GVs5oi7eSyc6_dNs64"
_acme-challenge.ff-test-c.fitfile.net.	120	IN	TXT	"ziPRCwdnApLKWSBRbDMrioG7A-7l-yb4PUCCCCSn1w0"
_acme-challenge.ff-test-c.fitfile.net.	120	IN	TXT	"_xHAJ1C1CfvUraOK4nhY4obbhEobXomBIa9LYGjlRkw"
_acme-challenge.pentest-argocd.fitfile.net.	120	IN	TXT	"zbax7hU6Pc9i51V6NMwKA-rd-SlRN3iD1BgrrlfKOx8"
_acme-challenge.pentest-argocd.fitfile.net.	120	IN	TXT	"PZIzH1NChcEKVLGMj3O3OyTYKheCpwr1Yfb7VIhEF5g"
_acme-challenge.pentest-argo-workflows.fitfile.net.	120	IN	TXT	"HEtqlF3UUbJPuh7f-zcfs7tumEGTK1f5jIZ2JPDwJ6s"
_acme-challenge.pentest-argo-workflows.fitfile.net.	120	IN	TXT	"Orcg0h-OqJbEwX8WCiUghNBK7e7n2xloHgi1inoZwXs"
_acme-challenge.pentest.fitfile.net.	120	IN	TXT	"NbPUw2MYZiKilS4q6WJZplx4M9vSThLv6WVx8m5xFLk"
_acme-challenge.pentest.fitfile.net.	120	IN	TXT	"8QvghVAzXxT33JEOtH2gX1njeSdcDiyaPKzD5ODctj4"
_acme-challenge.primary-care.fitfile.net.	120	IN	TXT	"jONUkHYFY8yZUGI5DV2pqtcnqG2jTqMBCLt25q9ucc4"
_acme-challenge.primary-care.fitfile.net.	120	IN	TXT	"2gTQ3RIquOoyswUTzEC2Y5peqGpH-ec5kKrbkUfU8Q8"
_acme-challenge.staging-argocd.fitfile.net.	120	IN	TXT	"h0DApk_JqUvS3W8avtX6CZXhVCO-uBpDFNdPkcZUPS8"
_acme-challenge.staging-argocd.fitfile.net.	120	IN	TXT	"hs_20Hr8E9g_8Xmrc1sacTXschzO0agzby_zDvgyFY4"
_acme-challenge.staging-argocd.fitfile.net.	120	IN	TXT	"ym80DJtk8wdHyZ72WGGlFdgPLwxlLCdE7yBxnDbCP9c"
_acme-challenge.staging-argo-workflows.fitfile.net.	120	IN	TXT	"A9Fj-1xI98i-GiEr_4L84i8iYJy9Ym0j1A7hNk4TRZs"
_acme-challenge.staging-argo-workflows.fitfile.net.	120	IN	TXT	"9tlXU_38Ul5Ow5BmDhhfxhOZDlm1W6PI8DeI_8XzNL4"
_acme-challenge.staging-argo-workflows.fitfile.net.	120	IN	TXT	"ruEZVwBSko3hYAg9q5DmYAjE6AZdLR8eb7CKUMpId3U"
_acme-challenge.storybook.fitfile.net.	120	IN	TXT	"SF2VF0wk5CH5ez3msMa_vpEkPO8qvBzk7PDTU2b_brQ"
_acme-challenge.storybook.fitfile.net.	120	IN	TXT	"0wHQLKN5YnreCA84CSxyC-hJ8KeTRUaghIk95lVpiI0"
_acme-challenge.storybook.fitfile.net.	120	IN	TXT	"VNR6n4sf8z_Cd02SxvohA9zedthomiHcQ378aOpNRgg"
_acme-challenge.testing-argocd.fitfile.net.	120	IN	TXT	"lk97ozCdjUhhEYwi1_R1qLZyMc-POCwRDrVfN_smNhQ"
_acme-challenge.testing-argocd.fitfile.net.	120	IN	TXT	"I-og-12lELv11BBNpL4hSRmNUn_sBQPl-L_kQ-m7dTE"
_acme-challenge.testing-argocd.fitfile.net.	120	IN	TXT	"yQ_qr7FK_U8ZG9LZaXAIYzDsays_0wTtwmYUnrh42_8"
_acme-challenge.testing-argocd.fitfile.net.	120	IN	TXT	"oxlhcO-HX3FyOPVdz0zpKZi5x-T0wailxsFVKMSGSPo"
_acme-challenge.testing-argo-workflows.fitfile.net.	120	IN	TXT	"-I7CwdD2TMg1V8TonU58tu0lv1ER8xd4vo7jW4dwFKU"
_acme-challenge.testing-argo-workflows.fitfile.net.	120	IN	TXT	"Vc3ZaMKatawVxY4YBv9SOU1z432wxnT6q8DNl5lpdbQ"
_acme-challenge.testing-argo-workflows.fitfile.net.	120	IN	TXT	"MuK3-794GqNoDe2fPJmiZXRE3DK00TDcHDrl85Yqb_8"
_acme-challenge.testing-argo-workflows.fitfile.net.	120	IN	TXT	"HBJlfSnZd9wT3mPd3aBs2BSDMng6-8cHWCmS-nogKdY"
_acme-challenge.testing.fitfile.net.	120	IN	TXT	"mFZVUQYZgXKt0fkOLrRkz7qsKlpK7Npyzes7jXNFQAU"
_acme-challenge.testing.fitfile.net.	120	IN	TXT	"e4OrqGxJa-IZbR7R6mF9nX7Krwal1KP2QC8bTrmc9Do"
_acme-challenge.testing.fitfile.net.	120	IN	TXT	"fJ7zoOSBu3yEx5YeV024AC0jQ-_d4EQ_GNz5IxliweU"
_acme-challenge.testing.fitfile.net.	120	IN	TXT	"1PMk0qaUm4we3jkXULWnztkQBeuoQqULHHEjmTs591Y"
cf2024-1._domainkey.fitfile.net.	1	IN	TXT	"v=DKIM1; h=sha256; k=rsa; p=MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAiweykoi+o48IOGuP7GR3X0MOExCUDY/BCRHoWBnh3rChl7WhdyCxW3jgq1daEjPPqoi7sJvdg5hEQVsgVRQP4DcnQDVjGMbASQtrY4WmB1VebF+RPJB2ECPsEDTpeiI5ZyUAwJaVX7r6bznU67g7LvFq35yIo4sdlmtZGV+i0H4cpYH9+3JJ78k" "m4KXwaf9xUJCWF6nxeD+qG6Fyruw1Qlbds2r85U9dkNDVAS3gioCvELryh1TxKGiVTkg4wqHTyHfWsp7KD3WQHYJn0RyfJJu6YEmL77zonn7p2SRMvTMP3ZEXibnC9gz3nnhR6wcYL8Q7zXypKTMD58bTixDSJwIDAQAB"
fitfile.net.	1	IN	TXT	"MS=ms72564386"
pentest.fitfile.net.	1	IN	TXT	"Probely=719d01df-a6c8-497d-b476-f0ebd23e2399"
