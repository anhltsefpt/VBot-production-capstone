# R2 / R4 / R7 – Đơn giá database, vector, cache/queue, object storage, DR (3 cloud)

> Ngày truy cập: **2026-10-16**. Giá list pay-as-you-go của doanh nghiệp, USD. Không dùng free tier, trial, credit hay giá đàm phán. Giá cam kết (CUD / RI / Reservation) ghi riêng.
> Region chính: GCP `asia-southeast1`, AWS `ap-southeast-1` (APS1), Azure `southeastasia` (SEA). Region DR: GCP asia-east1/asia-southeast2, AWS ap-northeast-1 Tokyo (APN1) hoặc ap-southeast-3 Jakarta, Azure `eastasia`.
> Quy đổi tháng = 730 giờ. Những ô ghi **(suy ra)** là phép tính của người tổng hợp, không phải số nhà cung cấp công bố.

## Nguồn gốc giá

| Cloud | Cách lấy | URL gốc |
|---|---|---|
| GCP | Trang giá chính thức, chọn region asia-southeast1 bằng trình duyệt (Playwright) | https://cloud.google.com/sql/pricing · https://cloud.google.com/alloydb/pricing · https://cloud.google.com/vertex-ai/pricing (redirect sang `/products/gemini-enterprise-agent-platform/pricing`) · https://cloud.google.com/memorystore/docs/redis/pricing · https://cloud.google.com/memorystore/docs/valkey/pricing · https://cloud.google.com/pubsub/pricing · https://cloud.google.com/tasks/pricing · https://cloud.google.com/storage/pricing · https://cloud.google.com/vpc/network-pricing |
| AWS | AWS Price List Bulk API (OnDemand + Reserved) | `https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/<Service>/current/<region>/index.json`. publicationDate: AmazonRDS 2026-10-06; AmazonS3 2026-10-15; AmazonElastiCache 2026-10-14; AmazonES 2026-10-15; AWSQueueService 2026-09-11; AWSDataTransfer 2026-09-16. Trang tham chiếu: https://aws.amazon.com/rds/postgresql/pricing/ · https://aws.amazon.com/rds/aurora/pricing/ · https://aws.amazon.com/opensearch-service/pricing/ · https://aws.amazon.com/elasticache/pricing/ · https://aws.amazon.com/sqs/pricing/ · https://aws.amazon.com/s3/pricing/ |
| Azure | Azure Retail Prices API (`priceType` Consumption và Reservation). Trang azure.microsoft.com chỉ hiện "$-" khi fetch | `https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&$filter=serviceName eq '<Service>' and armRegionName eq 'southeastasia'` với Service = `Azure Database for PostgreSQL`, `Azure Cognitive Search`, `Redis Cache`, `Service Bus`, `Storage`, `Bandwidth` |

---

## 1. Managed PostgreSQL có HA (standby khác zone)

### 1.1 Bảng so sánh chính

| Hạng mục | GCP | AWS | Azure |
|---|---|---|---|
| Dịch vụ / edition | Cloud SQL for PostgreSQL **Enterprise** và **Enterprise Plus**; AlloyDB | RDS for PostgreSQL **Multi-AZ DB instance** (1 standby); Aurora PostgreSQL | Azure Database for PostgreSQL **Flexible Server**, zone-redundant HA |
| Cách tính HA | Đơn giá HA = **×2** đơn giá thường (vCPU, RAM, storage) | Giá Multi-AZ = **×2** Single-AZ (instance và gp3). Aurora: writer + ≥1 reader ở AZ khác, mỗi instance tính riêng; storage dùng chung | Standby tính **như primary** (compute + storage) → ×2; replication giữa zone không tính phí. **Burstable không hỗ trợ zone-redundant HA** |
| Compute, cấu hình nhỏ nhất có HA + SLA | Enterprise: vCPU HA **0.1156/h**, RAM HA **0.0196/GiB-h** (thường: 0.0578 / 0.0098). Tối thiểu 1 vCPU, custom ≥ 3.75 GB | db.t4g.medium Multi-AZ **0.203/h** (Single-AZ 0.102) | General Purpose D2ds_v5 (2 vCore) **0.244/h** mỗi node (0.122/vCore-h) → HA ≈ **0.488/h (suy ra)** |
| Các cấu hình khác | Enterprise N4: 0.05782 / 0.0098 (HA 0.11564 / 0.0196). Enterprise Plus C4: 0.0756 / 0.0126 (HA 0.1512 / 0.0252); Enterprise Plus N2/C4A: 0.0752 / 0.0127 (HA 0.1503 / 0.0255); tối thiểu 2 vCPU / 13.5 GB | Multi-AZ: db.t4g.large 0.406/h · db.m7g.large 0.468/h · db.r7g.large 0.574/h. Single-AZ db.m7g.large 0.234/h | D4ds_v5 0.488/h mỗi node. Memory Optimized Edsv5 0.15/vCore-h. Burstable (không HA): B1ms 0.026/h, B2s 0.104/h, B2ms 0.208/h |
| Shared-core (không SLA, chỉ dùng staging) | db-f1-micro 0.0147/h, db-g1-small 0.049/h (HA 0.0294 / 0.098) | — | Burstable B1ms 0.026/h |
| Storage | SSD **0.000326027/GiB-h ≈ 0.238/GiB-tháng**; HA 0.000652055/GiB-h ≈ 0.476 (suy ra). HDD 0.000172603 (HA 0.000345205). Hyperdisk Balanced 0.000220548 (HA 0.000441096) | gp3 Multi-AZ **0.276/GB-tháng** (Single-AZ 0.138); IOPS gp3 Multi-AZ 0.048/IOPS-tháng | Premium SSD **0.138/GB-tháng** mỗi node (HA ×2). Premium SSD v2 0.138/GiB-tháng + 0.026/IOPS-tháng + 0.104/MBps-tháng; IOPS Scaling 0.06/IOPS-tháng |
| Backup | **0.000153425/GiB-h ≈ 0.112/GiB-tháng** (HA và không HA như nhau) | Phần vượt dung lượng DB đã cấp phát: **0.095/GB-tháng** | Backup Storage LRS **0.095/GB-tháng**; kèm sẵn bằng 100% storage cấp phát; có HA thì backup chỉ tính 1 lần; server zone-redundant lưu backup ZRS (API chỉ có meter LRS) |
| PITR | Enterprise Plus: WAL lưu trong Cloud Storage cùng region, 1–35 ngày (mặc định 14); Enterprise: WAL trên disk, 1–7 ngày. Phí WAL riêng: **KHÔNG TÌM THẤY** (https://cloud.google.com/sql/docs/postgres/backup-recovery/configure-pitr) | Nằm trong automated backup, không có SKU riêng | 7–35 ngày, RPO ~5 phút; không có backup dài hạn quá 35 ngày (cần Azure Backup LTR) |
| IP | IPv4 idle 0.014/h | — | — |
| pgvector | Có (PG13+, pgvector 0.8.5; docs extensions cập nhật 2026-10-15) | Có, RDS PG và Aurora PG 16/17, pgvector 0.8.2 | Có, extension `vector` (allowlist rồi `CREATE EXTENSION vector`) |
| SLA / failover | — | — | 99.99% (zone-redundant), 99.95% (zonal); failover 60–120 s |
| Nguồn docs | https://cloud.google.com/sql/docs/postgres/extensions | https://docs.aws.amazon.com/AmazonRDS/latest/PostgreSQLReleaseNotes/postgresql-extensions.html · https://docs.aws.amazon.com/AmazonRDS/latest/AuroraPostgreSQLReleaseNotes/AuroraPostgreSQL.Extensions.html | https://learn.microsoft.com/en-us/azure/postgresql/extensions/how-to-use-pgvector · https://learn.microsoft.com/en-us/azure/postgresql/high-availability/concepts-high-availability · https://learn.microsoft.com/en-us/azure/postgresql/backup-restore/concepts-backup-restore · https://learn.microsoft.com/en-us/azure/reliability/reliability-database-postgresql |

### 1.2 Lựa chọn "cao cấp": AlloyDB / Aurora

| Hạng mục | GCP AlloyDB | AWS Aurora PostgreSQL | Azure |
|---|---|---|---|
| Compute | N2/C4A: vCPU **0.08128/h**, RAM **0.01378/GiB-h**; C4: 0.11193 / 0.012915. Primary HA = 2 node, tính cả 2 | Standard: db.t4g.medium 0.114/h · db.t4g.large 0.229/h · db.r6g.large 0.313/h · db.r7g.large 0.333/h. I/O-Optimized: 0.148 / 0.298 / 0.407 / 0.433 | Không có tương đương (dùng Flexible Server) |
| Serverless | — | Serverless v2 **0.20/ACU-h** (I/O-Optimized 0.26); 1 ACU ≈ 2 GiB RAM; dải 0–256 ACU, 0 = auto-pause (PG 16.3+) (https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.how-it-works.html) | — |
| Storage | Regional cluster storage 0.0005054/GiB-h ≈ **0.369/GiB-tháng**, tính theo dung lượng dùng, dùng chung giữa instance | **0.11/GB-tháng** (Standard) + I/O **0.22/1M request**; I/O-Optimized 0.248/GB-tháng, không tính I/O | — |
| Backup | 0.0001685/GiB-h ≈ 0.123/GiB-tháng; log PITR 7 ngày đầu không tính phí | 0.023/GB-tháng (phần vượt) | — |
| Khác | Extension `vector` 0.8.2.google-1 và `alloydb_scann` | RDS Proxy 0.018/vCPU-h, hoặc 0.025/ACU-h với Serverless v2 | — |

### 1.3 Giá cam kết (ghi riêng, không dùng trong giá list)

| Cloud | Mục | 1 năm | 3 năm |
|---|---|---|---|
| GCP | Cloud SQL Enterprise vCPU / RAM (thường) | 0.04335 / 0.00735 (−25%) | 0.027744 / 0.004704 (−52%) |
| GCP | Cloud SQL Enterprise HA vCPU / RAM | 0.0867 / 0.0147 | 0.055488 / 0.009408 |
| GCP | Cloud SQL Enterprise Plus C4 HA vCPU / RAM | 0.1134 / 0.0189 | 0.072576 / 0.012096 |
| GCP | AlloyDB vCPU / RAM | 0.06096 / 0.010335 | 0.0390144 / 0.0066144 |
| GCP | Lưu ý | CUD không áp cho storage và backup | |
| AWS | RDS PG Multi-AZ db.t4g.medium | No Upfront 0.1605/h; Partial 668 + 0.0762/h; All Upfront 1,299 | Partial 1,549 + 0.0589/h; All Upfront 3,044 |
| AWS | RDS PG Multi-AZ db.t4g.large | No Upfront 0.3211/h; Partial 1,335 + 0.1524/h; All Upfront 2,599 | Partial 3,097 + 0.1179/h; All Upfront 6,088 |
| AWS | RDS PG Multi-AZ db.m7g.large | No Upfront 0.3607/h; Partial 1,539 + 0.1757/h; All Upfront 2,995 | Partial 3,385 + 0.1288/h; All Upfront 6,524 |
| AWS | RDS PG Multi-AZ db.r7g.large | No Upfront 0.4418/h; Partial 1,885 + 0.2152/h; All Upfront 3,669 | Partial 4,146 + 0.1578/h; All Upfront 7,991 |
| AWS | Lưu ý | File giá không có RI 3 năm No Upfront | |
| Azure | PG Flexible GP Ddsv5/Dadsv5/Ddsv4 (trả trước/vCore) | 641 USD/vCore ≈ 0.0732/vCore-h, −40% (suy ra) | 1,282 USD/vCore ≈ 0.0488/vCore-h, −60% (suy ra) |
| Azure | Memory Optimized Edsv5 (trả trước/vCore) | 788 | 1,577 |
| Azure | Burstable | Không có Reservation trong API | |

---

## 2. Vector search chuyên dụng (thay cho pgvector)

| Hạng mục | GCP – Vertex AI Vector Search | AWS – OpenSearch Serverless / OpenSearch Service | Azure – Azure AI Search |
|---|---|---|---|
| Đơn vị tính chính | Serving node e2-standard-2 **0.1157212/node-h**; e2-standard-16 0.9257696; e2-highmem-16 1.2487776 | Serverless: Indexing OCU **0.283/h**, Search OCU **0.283/h** | Basic **0.101/SU-h**; S1 **0.336/SU-h**; S2 1.344; S3 2.688; L1 3.839; L2 7.677 (SU = replica × partition; Basic partition 15 GB) |
| Phí dữ liệu | Build/update index 3.00/GiB; streaming insert 0.45/GiB; storage-optimized tier 2.30/CU-h mỗi replica (write 0.45/GiB) | Serverless storage S3-managed 0.026/GB-tháng; hot 0.36/GB-tháng. Managed domain: gp3 0.1464/GB-tháng | Semantic Ranker 1.00/1K query |
| Lựa chọn nhỏ khác | — | OpenSearch Service: t3.small.search 0.056/h · t3.medium.search 0.112/h · or2.medium.search 0.1208/h · m7g.large.search 0.169/h · r7g.large.search 0.214/h. S3 Vectors: 0.066/GB-tháng, PUT 0.219/GB, query 0.0027/1K, byte trả về 0.01/GB | Serverless: 0.2895/CU-h, 0.259/GB-tháng — **preview, không SLA**, không dùng cho prod |
| **Chi phí tối thiểu luôn chạy** | 1 node e2-standard-2 ≈ **84.48/tháng** (suy ra) | Classic collection: tối thiểu 2 OCU ≈ **413/tháng** (suy ra: 2 × 0.283 × 730). NextGen collection: không có OCU tối thiểu, scale về 0 sau 10 phút | 1 SU Basic ≈ **73.7/tháng** (suy ra). Số replica cần cho SLA: **chưa xác minh** (xem Gaps) |
| Cam kết | Savings Plan e2-standard-2: 1y 0.10414908, 3y 0.09257696/node-h | — | — |
| Ghi chú | — | Serverless không hỗ trợ cross-Region replication | https://learn.microsoft.com/en-us/azure/search/search-sku-tier |

Nhận xét: cả 3 lựa chọn đều cộng thêm ≥ 74–413 USD/tháng chạy 24/7 so với pgvector trong DB đã có. Với vector index nhỏ (D4), pgvector có chi phí biên gần bằng 0 (chỉ tốn thêm storage và RAM của DB).

---

## 3. Cache và queue

### 3.1 Cache (Redis / Valkey)

| Hạng mục | GCP | AWS | Azure |
|---|---|---|---|
| Lựa chọn nhỏ nhất có HA | Memorystore for **Valkey** custom-pico (1.25 GB) **0.037884/node-h**; HA = primary + replica, tính từng node | ElastiCache **Valkey** cache.t4g.small **0.0384/node-h**; Multi-AZ = primary + replica | Azure **Managed Redis** Balanced B0 **0.02/h**; B1 0.04/h (meter "Cache Instance"). Giá HA 2 node: chưa xác nhận (xem Gaps) |
| Lựa chọn khác | Valkey custom-micro (2.5 GB) 0.075768/node-h; standard-small (6.5 GB) 0.1758/node-h; shared-core-nano 0.0392 (không SLA). **Memorystore for Redis Standard (HA)**: M1 (1–4 GiB) **0.114/GiB-h**, M2 0.075, M3 0.063; Basic M1 0.065 | Valkey: t4g.medium 0.076 · m7g.large 0.1576 · r7g.large 0.2104. Redis OSS: t4g.small 0.048 · t4g.medium 0.095 · m7g.large 0.197 · r7g.large 0.263 | Managed Redis B3 0.081/h, B5 0.193/h. Azure Cache for Redis Standard C0 0.055/h (2 node × 0.0275); C1 0.138/h (2 × 0.069) |
| Serverless | — | ElastiCache Serverless Valkey: **0.101/GB-h**, ECPU **0.0027/1M**, tối thiểu 100 MB/cache. Redis OSS: 0.151/GB-h, 0.0041/1M ECPU, tối thiểu 1 GB | — |
| Backup / persistence | Valkey backup 0.00011111/GB-h; AOF 0.000676/GB-h | Backup 0.085/GB-tháng | — |
| Cam kết | Redis CUD chỉ từ M2: 1y −20%, 3y −40%. Valkey standard-small 1y 0.14064 / 3y 0.10548; pico/micro không có CUD | — | Managed Redis Reserved (trả trước/kỳ hạn): B0 1y 114 / 3y 237; B1 1y 228 / 3y 473 |
| Lưu ý | — | — | **Azure Cache for Redis retire 2028-09-30; tenant mới bị chặn tạo cache từ 2026-04-01** → dùng Managed Redis (https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/retirement-faq). B0/B1 không hỗ trợ active geo-replication (https://learn.microsoft.com/en-us/azure/redis/overview) |

### 3.2 Queue

| Hạng mục | GCP | AWS | Azure |
|---|---|---|---|
| Queue tác vụ | **Cloud Tasks 0.40/1M operation** (chia chunk 32 KB) | **SQS Standard 0.40/1M request**; FIFO 0.50/1M; Fair queue 0.10/1M | **Storage Queues** "Queues v2": operation **0.004/10K** (LRS và ZRS); dung lượng LRS 0.045, ZRS 0.0562/GB-tháng |
| Pub/sub, message broker | **Pub/Sub** message delivery **40/TiB** (tối thiểu 1 KB/request); storage 0.27/GiB-tháng | — | **Service Bus Standard** base **10.00/tháng** (0.013441/h), gồm 13M op đầu; 13–100M 0.80/M; 100–2,500M 0.50/M; > 2,500M 0.20/M. Basic 0.05/M. Premium 0.9275/MU-h. Geo Replication Data Transfer 0.12/GB |
| Bậc miễn phí bỏ qua | Cloud Tasks và Pub/Sub có bậc đầu 0 USD — không dùng | SQS 1M request đầu — không dùng | — |

---

## 4. Object storage (workspace, archive audit log)

### 4.1 Giá lưu trữ (USD/GB-tháng; GCP tính GiB)

| Lớp | GCP (regional asia-southeast1) | AWS S3 (APS1, regional đa AZ mặc định) | Azure Blob (SEA, "General Block Blob v2") |
|---|---|---|---|
| Chuẩn | Standard **0.020** | Standard **0.025** (50 TB đầu); 0.024 (450 TB tiếp); 0.023 (> 500 TB) | Hot LRS **0.02** (≥ 50 TB 0.0192; ≥ 500 TB 0.0184); Hot ZRS **0.025** |
| Truy cập ít (≥ 30 ngày) | Nearline 0.010 | Standard-IA 0.0138 | Cool LRS 0.011, ZRS 0.0138 |
| Lạnh | Coldline 0.005 (90 ngày) | Glacier Instant Retrieval 0.005 (90 ngày) | Cold LRS 0.0045, ZRS 0.005 |
| Lưu trữ dài | Archive 0.0015 (365 ngày) | Glacier Flexible Retrieval 0.0045; Deep Archive: **KHÔNG TÌM THẤY** (180 ngày) | Archive LRS 0.002 |
| Dự phòng đa zone | Regional = mặc định | Regional (≥ 3 AZ) = mặc định | Phải chọn ZRS (giá ở trên) |

### 4.2 Operation và truy xuất

| Mục | GCP | AWS | Azure |
|---|---|---|---|
| Ghi (lớp chuẩn) | Class A 0.005/1K | PUT/COPY/POST/LIST 0.005/1K | Hot write LRS 0.05/10K; ZRS 0.0625/10K |
| Đọc (lớp chuẩn) | Class B 0.0004/1K | GET 0.004/10K | Hot read 0.004/10K |
| Ghi / đọc lớp ít truy cập | Nearline A 0.01 / B 0.001 per 1K; Coldline 0.02 / 0.01; Archive 0.05 / 0.05 | IA PUT 0.01/1K, GET 0.01/10K; GIR PUT 0.02/1K, GET 0.10/10K; lifecycle sang Deep Archive 0.06/1K | Cool write 0.10, read 0.01 per 10K; Cold 0.18 / 0.10; Archive 0.12 / 6.00 |
| Phí truy xuất (USD/GB) | Standard 0; Nearline 0.01; Coldline 0.02; Archive 0.05 | IA 0.01; GIR 0.03; Glacier Flexible: Expedited 0.036, Standard 0.012, Bulk 0; Deep Archive: Standard 0.024, Bulk 0.005 | Hot 0; Cool 0.01; Cold 0.03; Archive 0.024 |
| Ràng buộc | Lưu tối thiểu: Nearline 30, Coldline 90, Archive 365 ngày | Lưu tối thiểu: IA 30, GIR 90, Deep Archive 180 ngày; object tối thiểu bị tính 128 KB; phí xóa sớm IA 0.0138, GIR 0.005/GB-tháng | Cool, Cold, Archive có phí xóa sớm |

---

## 5. R4 – Dung lượng thực dùng mỗi user (số liệu, không phải giá)

Không tìm thấy nguồn primary nào công bố **dung lượng trung bình/trung vị trên mỗi user doanh nghiệp** cho Google Drive, OneDrive for Business, Dropbox Business hay Box. Các số dưới đây là **proxy**.

| # | Giá trị | Định nghĩa | Nguồn | Ngày | Tin cậy |
|---|---|---|---|---|---|
| 1 | ≈ **5.4 GB/user** (suy ra: 75 TB ÷ 14,000) | Microsoft: một số ít user "exceeded 75TB per user or 14,000 times the average". Tài khoản **consumer** Office 365 Home/Personal/University, năm 2015 | Microsoft OneDrive Team, "OneDrive changes" — https://blog.onedrive.com/onedrive_changes/ (đọc qua Computerworld, https://www.computerworld.com/article/1629201/microsoft-pulls-the-plug-on-onedrive-unlimited-storage.html) | 2015-11-02 | B |
| 2 | ≈ **1 GB/tài khoản đăng ký** (suy ra: ~500 PB ÷ > 500 triệu signup) | Mọi tài khoản Dropbox, đa số free consumer | Dropbox Tech Blog, "Scaling to exabytes and beyond" — https://dropbox.tech/infrastructure/magic-pocket-infrastructure | 2016-03-14 | B |
| 3 | 100 TB pooled/tổ chức; "more than 99% of institutions will be within the pooled storage" | Gộp Drive + Gmail + Photos của cả trường. Ví dụ: trường 20,000 user ⇒ ≤ 5 GB/user (suy ra) | Google, "More options for learning with Google Workspace for Education" — https://blog.google/outreach-initiatives/education/google-workspace-for-education/ | 2021-02-17 | A (chỉ là cận trên) |
| 4 | "most schools (99.96%) are well below their storage allotment" (100 TB pooled) | Microsoft 365 Education, tính đến 08/2024; không có số/user | Microsoft, "Storage Changes for Microsoft 365 Education" — https://www.microsoft.com/en-us/education/products/microsoft-365-storage-options | 2024-08 | A (chỉ là cận trên) |
| 5 | Dung lượng/doanh nghiệp tăng ~55%/năm; file trung bình 3.13 MB (2017) | Theo công ty, phân tích 14 PB | Egnyte data report (đọc qua BetaNews; trang gốc trả 403) | 2018-02-13 | C |
| 6 | Trung bình **3.34 TB/công ty (2018) → 25.64 TB (2023)** | > 3,000 công ty AEC; không có số nhân viên nên không đổi ra GB/user được | Egnyte press release (đọc qua trang thứ cấp; Business Wire trả 403) | 2024-02-27 | B/C |

**Không dùng được (là quota, không phải mức dùng):** OneDrive for Business mặc định 1 TB/user (mở rộng đến 5 TB); SharePoint tenant 1 TB + 10 GB/license; gói backup Commvault 5 GB/user (Standard) hoặc 50 GB/user (Enterprise); bài blog "Exchange 5–15 GB per active user" (nguồn thứ cấp, hạng C).

**Đề xuất cho báo giá (giả định, ghi trên slide):** các mốc gần nhất đều ở mức vài GB/user (≈ 1–5.4 GB). Tính workspace theo dải **2–10 GB/user** (2,000 user → 4–20 TB), kịch bản rủi ro là đầy quota 20 TB (D5).

---

## 6. R7 – DR liên region

### 6.1 Backup DB sang region khác và read replica

| Hạng mục | GCP | AWS | Azure |
|---|---|---|---|
| Backup DB cross-region | Cloud SQL: chọn custom backup location (multi-region hoặc region khác). Phí riêng ngoài giá backup storage: **KHÔNG TÌM THẤY** (https://cloud.google.com/sql/docs/postgres/backup-recovery/backing-up · https://cloud.google.com/sql/docs/postgres/backup-recovery/backups) | RDS cross-Region automated backup replication: tính **data transfer 0.09/GB** + backup storage ở region đích (Tokyo **0.095/GB-tháng**). Hỗ trợ Multi-AZ DB instance, **không** hỗ trợ Multi-AZ DB cluster. **Đích Jakarta không được hỗ trợ từ Singapore** → chọn Tokyo (https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReplicateBackups.html) | **Geo-redundant backup**: chỉ bật được lúc tạo server; copy bất đồng bộ sang region cặp (SEA ↔ East Asia), RPO ≤ ~1 giờ; không PITR ở region DR. Công thức: ((2 × backup local) − storage cấp phát) × 0.095/GB-tháng (https://learn.microsoft.com/en-us/azure/postgresql/backup-restore/concepts-backup-restore) |
| Read replica cross-region | Cloud SQL: tính như instance độc lập + egress **0.12/GiB** (trang giá Cloud SQL). Advanced DR chỉ có ở Enterprise Plus | RDS read replica ở Tokyo: db.t4g.medium 0.101/h, db.t4g.large 0.202/h, db.m7g.large 0.234/h + gp3 0.138/GB-tháng + transfer 0.09/GB. Aurora Global Database: replicated write I/O 0.22/1M + instance Tokyo (t4g.medium 0.113/h, t4g.large 0.225/h) + transfer; backup Aurora Tokyo 0.023/GB-tháng | Tính như server riêng ở East Asia: D2ds_v5 **0.269/h**, storage **0.15/GB-tháng**. Không hỗ trợ Burstable; replica không có HA, không backup (https://learn.microsoft.com/en-us/azure/postgresql/read-replica/concepts-read-replicas) |
| Giá DB ở region DR (tham khảo) | Jakarta: chưa lấy (Gaps) | Tokyo: RDS backup 0.095, gp3 Single-AZ 0.138 | East Asia: B1ms 0.0286/h, B2s 0.1144/h, D2ds_v5 0.269/h, storage 0.15, Backup LRS 0.095 |

### 6.2 Truyền dữ liệu và nhân bản storage

| Hạng mục | GCP | AWS | Azure |
|---|---|---|---|
| Liên region (USD/GB) | SG → châu Á (asia-east1/east2, Tokyo) **0.08**; SG → Jakarta **0.10** (trang VPC). Trang Cloud SQL ghi 0.12 cho replica | APS1 → Jakarta **0.09**; APS1 → Tokyo **0.09**; chiều vào 0 | "Standard Inter-Region Data Transfer" **0.08** (SEA và East Asia; trang bandwidth: "Between regions within Asia $0.08 per GB") |
| Giữa zone trong region | **0.01/GiB** | Mâu thuẫn: dòng "xAZ" 0.00, dòng "IntraRegion" 0.01/GB | Mâu thuẫn: API có meter Inter-AZ 0.01/GB; trang bandwidth ghi không tính phí |
| Egress Internet (tham khảo) | — | 0.12/GB (10 TB đầu), 0.085 (40 TB tiếp) | 0.12/GB (10 TB sau 100 GB đầu; bậc 100 GB đầu không dùng) |
| Nhân bản object storage | **Dual-region**: Standard 0.022 / Nearline 0.011 / Coldline 0.0055 / Archive 0.0017 GiB-tháng **mỗi region**; Class A gấp đôi (Standard 0.01/1K); replication Asia default **0.08/GiB**, turbo **0.11/GiB** (RPO 15 phút). Multi-region asia: 0.026 / 0.015 / 0.00875 / 0.003 | **S3 CRR**: transfer 0.09/GB (tính theo region nguồn) + storage và PUT ở region đích (Jakarta Standard 0.025); Replication Time Control +0.015/GB | **GRS** Hot 0.04, Cool 0.022, Cold 0.009, Archive 0.004; RA-GRS Hot 0.05, Cool 0.0275; GZRS Hot 0.049; write GRS Hot 0.10/10K; + "Geo-Replication v2 Data Transfer" **0.09/GB**. East Asia Hot LRS 0.024, ZRS 0.03, GRS 0.048 |

---

## Gaps

1. **GCP Cloud SQL**: phí riêng cho custom/cross-region backup location và cho WAL/PITR — KHÔNG TÌM THẤY (đã xem docs `backing-up`, `backups`, `configure-pitr`).
2. **GCP**: giá AlloyDB cross-region secondary cluster; giá Backup and DR Service (enhanced backup); giá Cloud SQL và GCS ở asia-southeast2 (Jakarta) — chưa lấy.
3. **GCP**: hai giá liên region khác nhau (Cloud SQL 0.12/GiB vs VPC 0.08–0.10/GiB) — cần chụp cả hai, chọn một khi tính.
4. **AWS**: giá S3 Glacier Deep Archive storage ở APS1 — KHÔNG TÌM THẤY (file bulk APS1 chỉ có giá staging 0.023 và retrieval; https://aws.amazon.com/s3/pricing/ không hiện giá theo region).
5. **AWS**: giá RDS Multi-AZ DB cluster (2 readable standby) cho db.t4g/m7g — chưa lấy (chỉ có gp3 cluster 0.414/GB-tháng); giá instance Aurora ở Jakarta — chưa lấy.
6. **AWS**: OCU tối thiểu của OpenSearch Serverless khi bật vector search — docs chỉ ghi chung 2 OCU cho Classic.
7. **AWS và Azure**: phí truyền dữ liệu giữa AZ trong region mâu thuẫn giữa các nguồn — cần chụp trang làm bằng chứng.
8. **Azure**: giá Managed Redis HA (2 node) — trang https://azure.microsoft.com/en-us/pricing/details/managed-redis/ chỉ hiện "$-"; giả định "Cache Instance" = 1 node (HA B0 ≈ 0.04/h) **chưa xác nhận**.
9. **Azure**: số replica AI Search cần cho SLA (2 cho đọc, 3 cho đọc–ghi) **chưa xác minh** từ trang SLA chính thức.
10. **Azure**: meter riêng cho backup ZRS/GRS của PG — KHÔNG TÌM THẤY (API với `contains(productName,'PostgreSQL Flex')` chỉ có LRS); giá Azure Backup LTR cho PG — chưa lấy.
11. **R4**: không có số dung lượng/user doanh nghiệp từ Google, Microsoft, Dropbox, Box (10-K/S-1 chỉ có doanh thu/user); bài Redmondmag 2024 "How Much Space Are You Using in Microsoft 365?" trả 403.
12. **Bằng chứng**: các giá AWS/Azure lấy từ API; khi làm sheet `BangChung` cần chụp thêm trang giá hoặc calculator chính thức tương ứng.
