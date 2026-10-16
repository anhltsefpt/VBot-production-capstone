# R5 + R9 (governance / monitoring / CI): đơn giá bảo mật, quản trị, giám sát, CI/CD trên GCP, AWS, Azure

> Ngày truy cập mọi nguồn: **2026-10-16**. Region: GCP `asia-southeast1`, AWS `ap-southeast-1` (mã usage `APS1`), Azure `southeastasia`. Đơn vị USD.
>
> Quy ước:
> - Chỉ dùng **giá niêm yết pay-as-you-go**. Không dùng free tier, trial, credit, giá thương lượng. Khi trang giá có bậc miễn phí (ví dụ "50 MAU đầu"), file vẫn ghi bậc đó ở cột ghi chú nhưng **khi tính chi phí nên bỏ qua** (tính toàn bộ theo đơn giá trả phí) để tuân thủ quy tắc.
> - Nguồn giá AWS: **AWS Price List API** chính thức, `https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/<ServiceCode>/current/ap-southeast-1/index.json` (ký hiệu bên dưới: **[AWS-PL:<ServiceCode>]**). SKU ghi theo `usagetype`.
> - Nguồn giá Azure: **Azure Retail Prices API** chính thức, `https://prices.azure.com/api/retail/prices?$filter=serviceName eq '<Service>' and armRegionName eq 'southeastasia'` (ký hiệu **[AZ-RP:<Service>]**). Trang giá azure.microsoft.com hiện chỉ hiển thị "$-" khi không đăng nhập, nên lấy số từ API. SKU ghi theo `productName / skuName / meterName`.
> - Nguồn giá GCP: trang `cloud.google.com/.../pricing` (bảng theo region đọc từ dữ liệu nhúng trong trang).
> - "Phép tính" là số học trên đơn giá đã dẫn, không phải giá do nhà cung cấp công bố.

---

## 1. Authn front door (federate với IdP sẵn có của tập đoàn, D6)

| Hạng mục | GCP | AWS | Azure |
|---|---|---|---|
| Proxy xác thực trước app | **Identity-Aware Proxy (IAP)**: "at no charge" cho tài nguyên trên Google Cloud; chỉ trả phí load balancing bắt buộc. Tính năng trả phí thuộc Chrome Enterprise Premium (proxy tài nguyên ngoài GCP, custom access level, device attributes) — không cần cho VBot. [IAP pricing](https://cloud.google.com/iap/pricing) | **ALB `authenticate-oidc`**: ALB tự xác thực với IdP chuẩn OIDC. Price list ELB **không có SKU riêng** cho authentication → chỉ trả ALB: `APS1-LoadBalancerUsage` **$0.0252/ALB-giờ** + `APS1-LCUUsage` **$0.008/LCU-giờ** [AWS-PL:AWSELB]; tính năng: [ALB authenticate users](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html) | **App Service / Container Apps built-in auth ("Easy Auth")**: hỗ trợ Microsoft Entra và "Any OpenID Connect provider", chạy như middleware của nền tảng. Không có meter riêng trong Retail Prices API → nằm trong giá App Service plan. [App Service auth](https://learn.microsoft.com/en-us/azure/app-service/overview-authentication-authorization) |
| Federate IdP ngoài vào IAP / cloud | **Workforce Identity Federation**: "Workforce Identity Federation is free of charge." IAP hỗ trợ WIF ("Identity-Aware Proxy with Workforce Identity Federation"). [WIF product page](https://cloud.google.com/workforce-identity-federation), [WIF docs](https://docs.cloud.google.com/iam/docs/workforce-identity-federation) | **Amazon Verified Access** (zero-trust, thay ALB auth): `APS1-VerifiedAccess-App-Hours` **$0.35/app-giờ** (0–148.800 giờ), $0.26 sau đó; `APS1-VerifiedAccess-DataProcess-Bytes` **$0.02/GB**; `APS1-VerifiedAccess-ConnectionHours` $0.001/giờ (non-HTTP); non-HTTP app $0.26/giờ [AWS-PL:AmazonVPC]. Trang [Verified Access pricing](https://aws.amazon.com/verified-access/pricing/) chỉ ví dụ US East | Nếu IdP tập đoàn là Entra ID (workforce tenant): đăng ký app trong tenant sẵn có → chi phí cloud = 0 (license tính theo D6/D18). **Application Gateway**: không tìm thấy meter/tính năng xác thực người dùng trong price list; giá cổng: `Application Gateway Standard v2` Fixed **$0.26/giờ** + **$0.008/capacity unit-giờ**; WAF v2 Fixed **$0.468/giờ** + **$0.0144/CU-giờ**; Basic v2 Fixed $0.0252/giờ + $0.008/CU-giờ [AZ-RP:Application Gateway] |
| CIAM theo MAU (chỉ cần nếu không federate trực tiếp) | **Identity Platform**, Tier 2 (OIDC, SAML): **$0.015/MAU** (bậc 0–50 MAU: $0); Tier 1 (email/social): $0.0055/MAU (50K–100K), bậc 0–50K: $0. [Identity Platform pricing](https://cloud.google.com/identity-platform/pricing) | **Amazon Cognito**: user đăng nhập qua SAML/OIDC federation **$0.015/MAU** cho mọi tier ("50 MAUs per month per account" miễn phí). SKU `APS1-CognitoEnterpriseMAU` $0.015 [AWS-PL:AmazonCognito]. Tier thường: Lite `APS1-CognitoLiteMAU` $0.0055; Essentials $0.015; Plus $0.02/MAU. [Cognito pricing](https://aws.amazon.com/cognito/pricing/) | **Microsoft Entra External ID** (`Microsoft Entra / Microsoft Entra External ID`, meter Global): Core MAU **$0.01625** (bậc từ 50.000 MAU; bậc 0–50.000: $0); Basic MAU tier $0.03 từ 50.000 [AZ-RP: contains(productName,'External ID')]. Dành cho người dùng bên ngoài (khách hàng/đối tác), **không phải** cho nhân viên |
| Phép tính 2.000 user/tháng (không dùng bậc miễn phí) | Identity Platform Tier 2: 2.000 × $0.015 = **$30/tháng**; IAP + WIF: **$0** (chỉ LB) | Cognito federated: 2.000 × $0.015 = **$30/tháng**; ALB auth: **$0** thêm (chỉ ALB) | External ID Core: 2.000 × $0.01625 = **$32,5/tháng** (nếu bỏ bậc 0–50K); Easy Auth + Entra workforce: **$0** thêm |

**Nằm trong (included):**
- GCP: xác thực ở IAP nằm trong IAP (miễn phí) + phí External HTTPS LB (giá LB thuộc phần network R9, không nằm trong file này).
- AWS: `authenticate-oidc` nằm trong ALB (không có SKU riêng trong price list AWSELB).
- Azure: Easy Auth nằm trong App Service / Container Apps (không có meter riêng).

---

## 2. Authz (RBAC/ABAC + document ACL)

| Hạng mục | GCP | AWS | Azure |
|---|---|---|---|
| Policy engine managed cho quyền tầng ứng dụng | **KHÔNG TÌM THẤY** dịch vụ managed tương đương. IAM chỉ cho tài nguyên GCP. Đã kiểm: [IAP pricing](https://cloud.google.com/iap/pricing) | **Amazon Verified Permissions** (Cedar): `APS1-SingleAuthorizationRequest` **$5/1M request**; `APS1-AuthorizationRequest` (batch) **$150/1M** (0–40M), $75/1M (40M–100M), $40/1M (>100M); CreatePolicy / GetPolicy / UpdatePolicy / ListPolicies **$40/1M** mỗi loại [AWS-PL:AmazonVerifiedPermissions] | **KHÔNG TÌM THẤY** dịch vụ managed tương đương (Entra app roles/group claims chỉ cung cấp thuộc tính, không phải policy engine). Đã kiểm [AZ-RP] với từ khoá "Permissions", "Policy" |
| Tự chạy (OPA / Cedar open-source) | Chi phí = compute (sidecar/pod trong GKE). Không có license | Như cột GCP | Như cột GCP |

Ghi chú mô hình chi phí: ACL tài liệu (D4) có thể kiểm ngay trong DB (cột `allowed_groups` + filter khi truy vấn vector) → $0 thêm; policy engine riêng chỉ cần khi luật ABAC phức tạp.

---

## 3. Secrets / KMS (token vault OAuth mã hoá)

| Hạng mục | GCP | AWS | Azure |
|---|---|---|---|
| Khoá phần mềm | **Cloud KMS** SOFTWARE: **$0.000082192/key version-giờ** (≈ $0.06/tháng, theo ví dụ trên trang); key operations (crypto) **$0.03/10.000**; admin ops: miễn phí. Trang không phân giá theo region. [Cloud KMS pricing](https://cloud.google.com/kms/pricing) | **AWS KMS**: `ap-southeast-1-KMS-Keys` **$1/customer managed key (version)/tháng**; `ap-southeast-1-KMS-Requests` **$0.03/10.000**; asymmetric (trừ RSA 2048) **$0.15/10.000**; RSA 2048 $0.03/10.000; GenerateDataKeyPair RSA **$12/10.000**, ECC $0.10/10.000 [AWS-PL:awskms] | **Key Vault Standard**: meter `Key Vault / Standard / Operations` **$0.03/10.000** (secrets + khoá phần mềm RSA 2048); `Advanced Key Operations` **$0.15/10.000**; `Automated Key Rotation` $1/lần; `Secret Renewal` $1; `Certificate Renewal Request` $3 [AZ-RP:Key Vault]. Không thấy meter phí theo khoá/secret cho khoá phần mềm |
| Khoá HSM | Cloud KMS HSM: **$0.001369863/version-giờ** (≈ $1/tháng) cho AES-256/HMAC/RSA 2048; RSA 3072/4096/EC: $0.003424658/giờ (0–2.000 tháng-version), $0.001369863 sau đó; crypto ops $0.03/10.000, asymmetric HSM $0.15/10.000; EXTERNAL (EKM) $0.004109589/giờ. Single-tenant Cloud HSM **$4.794520548/giờ** | **CloudHSM** `APS1-CloudHSMv2Usage-hsm2m.m` **$1.86/HSM-giờ** [AWS-PL:CloudHSM] | **Key Vault Premium**: `Premium HSM-protected RSA 2048-bit key` **$1/khoá/tháng** + Operations $0.03/10.000; `Premium HSM-protected Advanced Key` **$5** (khoá 1–250), $2.5 (250–1.500), $0.9 (1.500–4.000), $0.4 (>4.000)/khoá/tháng; **Managed HSM** `Key Vault HSM Pool / Standard B1` **$3.20/giờ**; Dedicated HSM $4.85/giờ [AZ-RP:Key Vault] |
| Secret store | **Secret Manager**: active secret version **$0.000082192/giờ** (≈ $0.06/version/tháng, theo ví dụ trên trang); access ops **$0.03/10.000**; rotation notification **$0.05/lần**; management ops miễn phí. Bản sao user-managed tính theo từng location. [Secret Manager pricing](https://cloud.google.com/secret-manager/pricing) | **Secrets Manager**: `APS1-AWSSecretsManager-Secret` **$0.40/secret/tháng**; `APS1-AWSSecretsManagerAPIRequest` **$0.05/10.000** [AWS-PL:AWSSecretsManager] | Key Vault secrets: chỉ tính **operations $0.03/10.000** (Standard và Premium) [AZ-RP:Key Vault] |

**Lưu ý thiết kế token vault (phép tính, minh hoạ):** nếu lưu mỗi refresh token OAuth thành 1 secret riêng, với 2.000 user × 6 connector = 12.000 secret:
- GCP Secret Manager: 12.000 × $0.06 ≈ **$720/tháng**.
- AWS Secrets Manager: 12.000 × $0.40 = **$4.800/tháng**.
- Azure Key Vault: $0 theo số secret, chỉ tính operations.
- Phương án rẻ hơn trên GCP/AWS: **envelope encryption** — token mã hoá bằng 1 khoá KMS rồi lưu trong Postgres. Chi phí = vài key version + $0.03/10.000 thao tác.

---

## 4. Governance: guardrail / prompt injection, DLP / PII, phân loại dữ liệu

### 4.1 Guardrail đầu vào/đầu ra + chống prompt injection

| Hạng mục | GCP | AWS | Azure |
|---|---|---|---|
| Dịch vụ | **Model Armor** (standalone): **$0.10/1M token** sau hạn mức 2M token/tháng không tính phí. Token = 4 ký tự (UTF-8 code point), không tính khoảng trắng. Trong SCC Premium/Enterprise subscription: 3 tỷ token/tháng đi kèm, vượt $0.10/1M. [SCC pricing – Model Armor](https://cloud.google.com/security-command-center/pricing) | **Bedrock Guardrails**: `APS1-Guardrail-ContentPolicyUnitsConsumed` **$0.15/1.000 text unit**; `TopicPolicy` (denied topics) **$0.15**; `SensitiveInformationPolicy` (PII) **$0.10**; `ContextualGroundingPolicy` **$0.10**; `WordPolicy` **$0** [AWS-PL:AmazonBedrock]. Automated Reasoning $0.17/1.000 text unit/policy (trang giá, chưa thấy SKU APS1). Với **InvokeGuardrailChecks API**: content filters $0.07, **prompt attack $0.08**, PII $0.10/1.000 text unit. 1 text unit ≤ 1.000 ký tự. Giá như nhau cho Standard và Classic tier. [Bedrock pricing](https://aws.amazon.com/bedrock/pricing/) | **Azure AI Content Safety** (Prompt Shields, text moderation, protected material, groundedness): S0 `Standard Text Records` **$0.375/1.000 record** — **không có meter PAYG ở Southeast Asia**; có ở `Global`, `japaneast`, `australiaeast`, `southindia`, `koreacentral`… Ở `southeastasia` chỉ có commitment tier: `Commitment Tier Txt Azure 1M` **$338/tháng** (overage $0.338/1.000) [AZ-RP: contains(productName,'Content Safety')]. 1 text record ≤ 1.000 ký tự. [Content Safety pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/content-safety/) |
| Prompt injection | Model Armor có bộ lọc prompt injection & jailbreak (trong cùng đơn giá theo token) | Prompt attack nằm trong content filters; trang giá ghi "With the InvokeGuardrailChecks API, you can use the prompt attack filter separately outside of content filters." | Prompt Shields (user prompt attack + indirect attack) là tính năng text của Content Safety |
| Nằm trong dịch vụ khác | "When Sensitive Data Protection is enabled within Model Armor, there are no additional charges to use it." (DLP đi kèm Model Armor) | PII masking cho prompt/response = sensitive information filter của Guardrails ($0.10/1.000 text unit) | Content filter mặc định (DefaultV2) của Azure OpenAI/Foundry có Prompt Shields; nguồn nói "no additional cost" là **Microsoft Q&A** ([link](https://learn.microsoft.com/en-gb/answers/questions/2148430/are-we-charged-of-the-customized-or-the-defaultv2)), **không phải trang giá** → cần xác minh. Tính năng: [Foundry content filter](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/content-filter) |

### 4.2 DLP / PII masking

| Hạng mục | GCP | AWS | Azure |
|---|---|---|---|
| PII trên luồng text (online) | **Sensitive Data Protection** content methods: inspection **$3.00/GiB** (1 GiB–1 TiB), $2.00/GiB (>1 TiB); transformation (de-identify) **$2.00/GiB** (1 GiB–1 TiB), $1.00/GiB (>1 TiB). **Tối thiểu 1 KB/request**. Simple redaction (RedactConfig, ReplaceWithInfoTypeConfig) không tính bytes transformed khi đã inspect. Hybrid job inspect $3.00/GiB. [SDP pricing](https://cloud.google.com/sensitive-data-protection/pricing) | **Amazon Comprehend** `APS1-DetectPiiEntities` **$0.0001/unit** (0–10M unit), $0.00005 (10–50M), $0.000025 (50–100M), $0.000005 (>100M); `APS1-ContainsPiiEntities` **$0.000002/unit** (0–10M)…; 1 unit = 100 ký tự, **tối thiểu 3 unit/request** [AWS-PL:comprehend], [Comprehend pricing](https://aws.amazon.com/comprehend/pricing/) | **Azure Language** (PII detection, Text PII redaction tính là "Standard Text Records"): **$1/1.000 record** (0–0,5M), $0.75 (0,5–2,5M), $0.30 (2,5–10M), $0.25 (>10M) [AZ-RP: Foundry Tools / Azure Language / Standard / Standard Text Records]; 1 record ≤ 1.000 ký tự. [Language pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/language-service/) |
| Quét dữ liệu lưu trữ | SDP storage inspection job **$1.00/GiB** (1 GiB–50 TiB), transformation job $1.00/GiB | **Amazon Macie** `APS1-SensitiveDataDiscovery` **$1.35/GB** (1–50.000 GB), $0.68, $0.34; bucket inventory `APS1-PaidDataInventoryEvaluation` $0.003288/bucket-ngày; automated object monitoring $0.0000000044/object-ngày [AWS-PL:AmazonMacie] | **Microsoft Purview**: `On-Demand Classification / Standard Assets` **$20/10.000 asset**; `Data Security / In Transit Protection Request` **$0.00005/request**; `Data Compliance / Audit Standard Asset` **$0.015/1.000 record** (audit app AI không phải Microsoft); `Data Security Processing Unit` $25/DSPU [AZ-RP: contains(serviceName,'Purview')]. [Purview pricing](https://azure.microsoft.com/en-us/pricing/details/purview/) |

### 4.3 Phân loại dữ liệu (data classification / discovery)

| GCP | AWS | Azure |
|---|---|---|
| SDP Discovery (consumption): **$0.03/GB** dữ liệu được profile (Cloud Storage: trần 3 TB/bucket, tối thiểu $0.03/bucket; Cloud SQL tối thiểu $0.01/bảng). Subscription: $2.500/unit. [SDP pricing](https://cloud.google.com/sensitive-data-protection/pricing) | Macie automated sensitive data discovery (giá ở 4.2) | **Purview Data Map** `Standard Capacity Unit` **$0.411/CU-giờ**; `Scanning Ingestion and Classification / Standard vCore` **$0.63/vCore-giờ** [AZ-RP: Azure Purview] |

---

## 5. Monitoring + audit log 12 tháng

### 5.1 Log

| Hạng mục | GCP (Cloud Logging) | AWS (CloudWatch Logs) | Azure (Azure Monitor Logs) |
|---|---|---|---|
| Ingest | **$0.50/GiB** (gồm 30 ngày lưu trong log bucket, query/Log Analytics không tính thêm); vended network logs $0.25/GiB | Standard `APS1-DataProcessing-Bytes` **$0.70/GB**; Infrequent Access `APS1-DataProcessingIA-Bytes` **$0.35/GB** [AWS-PL:AmazonCloudWatch] | Analytics Logs `Analytics Logs Data Ingestion` **$2.99/GB** (gồm 31 ngày analytics retention); Basic Logs **$0.65/GB**; **Auxiliary Logs $0.07/GB** [AZ-RP:Log Analytics, Azure Monitor] |
| Lưu thêm | Retention > 30 ngày: **$0.01/GiB-tháng** | Storage `APS1-TimedStorage-ByteHrs` **$0.03/GB-tháng**; IA `APS1-TimedStorage-IA-ByteHrs` **$0.018/GB-tháng** | Analytics retention mở rộng `Analytics Logs Data Retention` **$0.13/GB-tháng**; long-term retention (meter `Data Archive`) **$0.026/GB-tháng**, tối đa 12 năm |
| Query | Không tính phí | Logs Insights `APS1-DataScanned-Bytes` **$0.007/GB** scan | Basic/Auxiliary: `Search Queries Scanned` **$0.0065/GB**; `Search Jobs Scanned` $0.0065/GB; `Data Restore` $0.13/GB/ngày (tối thiểu 2 TB × 12 giờ) |
| Export | Log Router: miễn phí; export sang Cloud Storage không tính Class A ops | (không nghiên cứu Firehose/S3 export) | `Log Analytics data export` **$0.13/GB**; `Platform Logs Data Processed` $0.325/GB |
| Nguồn | [Observability pricing](https://cloud.google.com/stackdriver/pricing) | [AWS-PL:AmazonCloudWatch] | [AZ-RP], [cost-logs](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/cost-logs), [data retention](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/data-retention-configure) |

### 5.2 Metrics, trace, audit hạ tầng

| Hạng mục | GCP | AWS | Azure |
|---|---|---|---|
| Metrics | Cloud Monitoring **$0.2580/MiB** (150–100.000 MiB), $0.1510 (100K–250K), $0.0610 (>250K); Managed Prometheus **$0.06/1M sample** (0–50 tỷ); read API $0.50/1M time series; uptime check $0.30/1.000; alerting $0.35/metric reference/tháng (effective date trên trang: 1/9/2027) | `APS1-CW:MetricMonitorUsage` **$0.30/metric-tháng** (10.000 đầu), $0.10, $0.05, $0.02; alarm standard **$0.10/alarm-metric-tháng** | `Metric Samples Ingested` **$0.11/10M sample**; Prometheus query $0.001/10M sample; log alert 5 phút **$1.50/tháng**, 15 phút $0.50 |
| Trace | Cloud Trace **$0.20/1M span** | X-Ray `APS1-XRay-TracesStored` **$5/1M trace** ($0.000005), TracesAccessed $0.50/1M [AWS-PL:AWSXRay] | Application Insights lưu vào Log Analytics → giá ingest/retention của Log Analytics (cost-logs) |
| Audit log hạ tầng | Admin Activity / System Event audit log nằm trong bucket `_Required`, **lưu 400 ngày, không tính phí**. Data Access audit log vào `_Default` → tính như log thường | **CloudTrail**: bản sao đầu tiên của management events vào S3 **miễn phí**; bản sao thêm **$2/100.000** (`APS1-PaidEventsRecorded` $0.00002/event); data events **$0.10/100.000**. CloudTrail Lake: 1 năm mở rộng **$0.75/GB** (gồm năm đầu), lưu thêm $0.023/GB-tháng; 7 năm: $2.5/GB (5 TB đầu) [AWS-PL:AWSCloudTrail], [CloudTrail pricing](https://aws.amazon.com/cloudtrail/pricing/) | Bảng `AzureActivity` không tính ingest và giữ 90 ngày miễn phí (data-retention-configure) |

### 5.3 Lưu archive object storage (đích export audit)

| GCP Cloud Storage `asia-southeast1` (regional) | AWS S3 `ap-southeast-1` | Azure Blob `southeastasia` (LRS) |
|---|---|---|
| Standard **$0.02**, Nearline **$0.01**, Coldline **$0.005**, **Archive $0.0015**/GiB-tháng. Thời hạn lưu tối thiểu: Nearline 30 ngày, Coldline 90, Archive 365. [Storage pricing](https://cloud.google.com/storage/pricing) | Standard `APS1-TimedStorage-ByteHrs` $0.025/GB-tháng (50 TB đầu); Glacier Instant Retrieval $0.005; Glacier Flexible $0.0045; **Glacier Deep Archive `APS1-TimedStorage-GDA-ByteHrs` $0.002**; PUT vào GDA $0.06/1.000; Standard retrieval GDA $0.024/GB [AWS-PL:AmazonS3, AmazonS3GlacierDeepArchive] | Hot $0.02 (50 TB đầu), Cool $0.011, Cold $0.0045, **Archive $0.002**/GB-tháng [AZ-RP:Storage, General Block Blob v2] |

### 5.4 Cách rẻ nhất giữ audit log 12 tháng (D12: 30 ngày truy vấn nhanh, sau đó archive)

Phép tính trên **1 GB audit log ghi mỗi tháng**, giữ đủ 12 tháng:

| Cloud | Phương án | Chi phí cho 1 GB (12 tháng) |
|---|---|---|
| GCP | Log bucket 30 ngày ($0.50) + sink song song sang GCS **Archive** ($0.0015 × 12) | ≈ **$0.518** |
| GCP | Chỉ dùng log bucket, retention 365 ngày ($0.50 + 11 × $0.01) | ≈ $0.61 |
| AWS | App ghi thẳng audit event vào S3; 30 ngày Standard ($0.025) → lifecycle sang Glacier Deep Archive ($0.002 × 11) | ≈ **$0.047** + phí request (PUT/transition $0.06/1.000 object) |
| AWS | CloudWatch Logs IA ($0.35 + 12 × $0.018) | ≈ $0.566 |
| Azure | **Auxiliary Logs** ($0.07) + long-term retention ($0.026 × 11; giả định 30 ngày đầu nằm trong ingest — xem gap) | ≈ **$0.356** |
| Azure | Ghi thẳng vào Blob; 30 ngày Hot ($0.02) → Archive ($0.002 × 11) | ≈ $0.042 + phí giao dịch (chưa lấy) |

Kết luận: rẻ nhất trên cả 3 cloud là **ghi audit trail của VBot thẳng vào object storage (lớp archive)**, không qua dịch vụ log. Muốn truy vấn nhanh 30 ngày thì: GCP giữ log bucket (đã gồm 30 ngày); Azure dùng Auxiliary Logs; AWS dùng CloudWatch Logs IA rồi xoá sau 30 ngày.

---

## 6. LLM gateway (quota USD theo user/phòng ban, D17)

| Hạng mục | GCP | AWS | Azure |
|---|---|---|---|
| Gateway API managed rẻ | **API Gateway**: **$3.00/1M call** (2M–1B), $1.50 (>1B); bậc 0–2M: $0. Không tìm thấy tính năng quota theo token. [API Gateway pricing](https://cloud.google.com/api-gateway/pricing) | **Amazon API Gateway** HTTP API `APS1-ApiGatewayHttpRequest` **$1.25/1M** (300M đầu); REST `APS1-ApiGatewayRequest` **$4.25/1M** (333M đầu); WebSocket message $1.15/1M, connection $0.288/1M phút [AWS-PL:AmazonApiGateway]. **KHÔNG TÌM THẤY** tính năng quota theo token LLM | **API Management**: Consumption **$0.0425/10.000 call** (từ 1M call); Basic v2 **$0.20548/giờ** (call $0.03/10.000 từ 10M); Standard v2 **$0.9589/giờ** (call $0.025/10.000 từ 50M); Developer $0.0658/giờ (không dùng cho prod); Basic (classic) $0.2016/giờ; Standard $0.9407/giờ; Premium $3.829/giờ; Premium v2 $3.83562/giờ [AZ-RP:API Management] |
| Gateway có tính năng AI | **Apigee** pay-as-you-go: Standard API Proxy **$20/1M call** (≤50M), Extensible **$100/1M**; môi trường Base **$365**, Intermediate **$1.460**, Comprehensive **$3.431**/tháng/region; API Analytics $20/1M; Advanced API Security $350/1M. [Apigee pricing](https://cloud.google.com/apigee/pricing). Policy **LLMTokenQuota** (quota theo token input/output, theo phút…tháng) là **Extensible policy** → cần Extensible proxy + môi trường từ Intermediate. [LLMTokenQuota](https://docs.cloud.google.com/apigee/docs/api-platform/reference/policies/llm-token-quota-policy) | (Không có tính năng tương đương trong price list) | `llm-token-limit` (rate + quota token Hourly…Monthly, `counter-key` theo user/subscription) áp dụng cho **Developer, Basic, Basic v2, Standard, Standard v2, Premium, Premium v2**; **không có ở Consumption**. Đếm theo token, không theo USD; mỗi gateway đếm riêng. [llm-token-limit](https://learn.microsoft.com/en-us/azure/api-management/llm-token-limit-policy) |
| Tự chạy | **LiteLLM** Open Source: "$0 — Free forever · self-hosted"; gồm "Virtual keys, users & teams", "Spend tracking", "Budgets + rate limits", "LLM fallbacks". Chi phí = compute + DB. **Enterprise** (SSO+SCIM, OIDC/JWT auth, audit logs, secret managers, 24/7 SLA): "Annual · sized to your usage" → **KHÔNG TÌM THẤY giá niêm yết**. [LiteLLM pricing](https://www.litellm.ai/pricing) | Như cột GCP | Như cột GCP |

Nhận xét: D17 yêu cầu quota **bằng USD** và 3 nấc. Apigee và APIM đếm **token**, phải tự quy đổi USD; LiteLLM OSS có sẵn spend tracking + budget theo user/team (khớp D17). Các tính năng Enterprise của LiteLLM (SSO, audit log) không bắt buộc nếu VBot tự xác thực user và tự ghi audit.

---

## 7. CI/CD + registry + IaC

| Hạng mục | GCP | AWS | Azure |
|---|---|---|---|
| Build | **Cloud Build** default pool `e2-standard-2` **$0.006/phút** (global); default pool tại Singapore: e2-medium $0.00369, e2-highcpu-8 $0.019188, e2-highcpu-32 $0.076752/phút; **private pool Singapore** e2-standard-2 **$0.00738/phút**, e2-standard-4 $0.01476. (2.500 phút/tháng miễn phí: trang ghi là "promotional free tier" → bỏ qua.) [Cloud Build pricing](https://cloud.google.com/build/pricing) | **CodeBuild** `APS1-Build-Min:Linux:g1.small` (build.general1.small) **$0.005/phút**; general1.medium **$0.01/phút**; Lambda arm 1 GB $0.00001/giây [AWS-PL:CodeBuild] | **Azure Pipelines**: Microsoft-hosted CI/CD **$40/parallel job/tháng**; self-hosted **$15/parallel job/tháng**; theo phút (từ 2026-05): Linux 8-core $0.022/phút, Linux 16-core $0.042 [AZ-RP:Azure DevOps] |
| Registry | **Artifact Registry** **$0.000136986/GiB-giờ** (≈ $0.10/GiB-tháng; 0,5 GiB đầu: $0); egress cùng location: $0; giữa các region châu Á $0.05/GiB. [Artifact Registry pricing](https://cloud.google.com/artifact-registry/pricing) | **ECR** `APS1-TimedStorage-ByteHrs` **$0.10/GB-tháng**; archive $0.10/GB-tháng (153,6 TB đầu), retrieval archive $0.03/GB; image signing $0.02/lần [AWS-PL:AmazonECR] | **ACR**: Basic **$0.1666/ngày**, Standard **$0.6666/ngày**, Premium **$1.6666/ngày**; `Data Stored` $0.10/GB-tháng; Task vCPU $0.0001/giây (từ 6.000 giây) [AZ-RP:Container Registry] |
| Tham khảo GitHub Actions | Linux 2-core x64 **$0.006/phút**, Linux 2-core arm64 **$0.005/phút**, Windows 2-core **$0.010/phút**. [Actions runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing) | (như cột GCP) | (như cột GCP) |
| IaC | Terraform/OpenTofu open-source: $0 license. Dịch vụ IaC managed (Infrastructure Manager / CloudFormation / Deployment Stacks): **chưa nghiên cứu** | — | — |
| Eval gate | Không có SKU riêng: chạy như 1 job CI (phút build) + token LLM (R3) | — | — |

---

## 8. Gói support (chỉ tham khảo — D19 không mua)

| GCP | AWS | Azure |
|---|---|---|
| Gói rẻ nhất có hỗ trợ 24/7 cho sự cố nghiêm trọng: **Enhanced Support** = max(**$100**; 10% chi phí cloud tháng phần $0–10K + 7% phần $10K–80K + 5% phần $80K–250K + 3% phần >$250K); "24/7 response for high- and critical-impact issues". (Standard Support: max($29; 3%) — không thấy dòng 24/7.) [Google Cloud Support](https://cloud.google.com/support) | **Business Support+** = max(**$29**/tháng/account; 9% phần ≤$10K + 7% phần $10K–80K + 5% phần $80K–250K + 3% phần >$250K); "24/7 phone, web, chat, email"; "Production system down: < 1 hour". Gói Developer/Business cũ không còn trong bảng so sánh. [Support pricing](https://aws.amazon.com/premiumsupport/pricing/), [Support plans](https://aws.amazon.com/premiumsupport/plans/) | **Standard**: **$100/tháng** (giá cố định), hỗ trợ 24x7, Severity A "Within one hour". Developer ($29) không có 24/7. [Azure support plans](https://azure.microsoft.com/en-us/support/plans/) |

---

## Gaps (cần bổ sung hoặc xác minh)

1. **Azure Content Safety PAYG ở Southeast Asia**: Retail Prices API không có meter `Standard Text Records` cho `southeastasia` (chỉ commitment tier $338/tháng). Cần kiểm [region availability](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/region-availability) xem Prompt Shields có ở SEA không, hoặc gọi resource ở `Global` / `japaneast` ($0.375/1.000 record).
2. **Azure OpenAI content filter mặc định (gồm Prompt Shields) miễn phí**: chỉ có nguồn Microsoft Q&A, chưa thấy câu chữ trên trang giá chính thức.
3. **Model Armor tại asia-southeast1**: chưa xác minh region; giá trên trang không phân theo region.
4. **Bedrock Automated Reasoning** ($0.17) và **InvokeGuardrailChecks** ($0.07 / $0.08): lấy từ trang giá, chưa thấy SKU APS1 trong Price List.
5. **Policy engine managed** cho GCP/Azure: KHÔNG TÌM THẤY (đã kiểm IAP pricing, Azure Retail Prices API).
6. **LiteLLM Enterprise**: không có giá niêm yết ("Annual · sized to your usage").
7. **Azure Auxiliary/Basic Logs**: tài liệu ghi "total retention 30 days by default" nhưng không nói rõ 30 ngày đó nằm trong giá ingest — phép tính 5.4 đang giả định có.
8. **Thời hạn lưu tối thiểu + phí retrieval/early delete** của S3 Glacier Deep Archive và Azure Blob Archive: chưa lấy trong phiên này (chỉ có GCS: Archive 365 ngày). Phí giao dịch Blob Archive chưa lấy.
9. **Phí load balancer / WAF** đứng trước IAP / ALB / App Gateway (GCP forwarding rule, AWS WAF, Azure WAF policy): thuộc phần network R9, chưa nằm trong file này. Giá Application Gateway ở mục 1 chỉ là tham khảo.
10. **ACR dung lượng kèm theo từng tier**, **ECR data transfer**, **dịch vụ IaC managed**: chưa xác minh.
11. **Cloud KMS / Secret Manager / Cloud Logging / Cloud Trace / Model Armor**: trang giá GCP không phân giá theo region; giả định áp dụng cho asia-southeast1.
12. **CloudWatch Logs IA storage $0.018/GB-tháng**: lấy từ Price List (`APS1-TimedStorage-IA-ByteHrs`); chưa đối chiếu với trang giá CloudWatch.
