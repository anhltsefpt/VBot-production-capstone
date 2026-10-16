# NỘI DUNG TRÌNH BÀY SLIDE: THIẾT KẾ KIẾN TRÚC & TỐI ƯU CHI PHÍ FINOPS TRỢ LÝ AI VBOT (2.000 DAU)

> **Tài liệu nguồn:** Dự án VBot Enterprise Platform (`bot_ai.md` & `bao_cao.md`)  
> **Mục tiêu:** Cung cấp toàn bộ nội dung thuyết trình 12 slide chuẩn hóa, cô đọng, sắc bén, đầy đủ công thức, mã định danh component, bảng so sánh và số liệu tài chính để bảo vệ đồ án trước Hội đồng.

---

## SLIDE 1: GIẢ ĐỊNH VÀ ƯỚC LƯỢNG TẢI (CAPACITY PLANNING)

### 1. Tham số đầu vào cố định (Đề bài cho sẵn)
* **Quy mô:** **2.000 DAU** (Daily Active Users - Nhân viên văn phòng tập đoàn).
* **Khung giờ làm việc:** Thứ 2 – Thứ 6, từ 8:00 – 18:00 (10 giờ/ngày = **220 giờ hành chính/tháng**; các dịch vụ 24/7 chạy **730 giờ/tháng**).
* **Môi trường triển khai:** 01 Môi trường Production (Multi-AZ 24/7) + 01 Môi trường Staging (chạy giờ hành chính).

### 2. Công thức ước lượng Lưu lượng & Token
* **Tần suất tương tác:** 30 requests/nhân viên/ngày (trung bình 20 phút/tương tác xử lý email, hỏi tài liệu, chạy phân tích, tra cứu Jira).
* **Tổng lưu lượng:**
  $$\text{Request/ngày} = 2.000\text{ DAU} \times 30 = \mathbf{60.000\text{ req/ngày}}$$
  $$\text{Request/tháng} = 60.000 \times 22\text{ ngày} = \mathbf{1.320.000\text{ req/tháng}}$$
* **Tải giờ cao điểm (Peak Hours: 9:00–11:30 & 13:30–17:00 = 6 tiếng tập trung 80% tải):**
  $$\text{Avg Peak RPS} = \frac{60.000 \times 0,80}{6 \times 3.600\text{s}} = \mathbf{2,22\text{ RPS}} \quad\xrightarrow{\text{Spike Factor } 3\times}\quad \text{Peak Burst} = \mathbf{6,7\text{ – }10\text{ RPS}}$$
* **Lưu lượng Token cao điểm:** $10\text{ RPS} \times 2.000\text{ tokens (in+out)} = \mathbf{20.000\text{ tokens/giây}}$ (trong đó output 5.000 tok/s).
* **Phiên đồng thời (Concurrent Active Sessions):** 15% – 20% DAU = **300 – 400 kết nối đồng thời** (WebSocket/SSE).

### 3. Phân bổ 5 cấp tác vụ & Khối lượng đặc thù
* **Cấp 1 (Email & FAQ):** **45%** (27.000 req/ngày) | In: 1.500 tok | Out: 350 tok.
* **Cấp 2 (Tài liệu & Slide):** **25%** (15.000 req/ngày) | In: 2.000 tok | Out: 800 tok.
* **Cấp 3 (Dữ liệu & Code):** **12%** (7.200 req/ngày) | In: 2.500 tok | Out: 500 tok $\rightarrow$ **7.200 lượt sandbox/ngày** (5–15s/lượt).
* **Cấp 4 (Agent Dự án Multi-step):** **10%** (6.000 req/ngày) | In: 4.500 tok | Out: 700 tok (3 turns).
* **Cấp 5 (Thiết kế & Đồ họa):** **8%** (4.800 req/ngày: 3.600 req sơ đồ Mermaid/HTML + **1.200 ảnh sinh/ngày** qua FLUX.1).

### 4. Dung lượng Lưu trữ & Mạng
* **Knowledge Base:** 500 GB thô $\rightarrow$ 10 triệu chunks $\approx$ **60 – 80 GB** pgvector HNSW index.
* **Workspace riêng:** Quota 10 GB/user; thực tế sau 6 tháng $\approx$ **4 TB trên AWS S3 Standard**.
* **Chat history & State:** 120 MB/ngày $\rightarrow$ **2,64 GB/tháng** trên PostgreSQL RLS.
* **Audit Log Vault:** 600 MB/ngày $\rightarrow$ **13,2 GB/tháng (~160 GB/năm)** S3 Glacier Instant Retrieval WORM Lock 12 tháng.
* **Lệnh gọi Connector:** ~35.000 SaaS calls/ngày; **Lưu lượng Egress mạng:** ~300 GB/tháng.

---

## SLIDE 2: KIẾN TRÚC TỔNG THỂ (HIGH-LEVEL ARCHITECTURE)

### Sơ đồ Hệ thống với Mã định danh Component (Component Codes)

```
                            [ NGƯỜI DÙNG DOANH NGHIỆP (2.000 DAU) ]
                       (Web Browser, Microsoft Teams, Slack, Office Add-in)
                                                │
                                                │ HTTPS / WSS (TLS 1.3 / mTLS)
                                                ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ [ING-01] CLOUDFLARE ENTERPRISE WAF & ZERO TRUST PERIMETER                                        │
 │ • Chống DDoS L3/L4/L7, Rate Limiting (chặn DoS prompt injection spike)                           │
 │ • [IDP-01] Corporate IdP: Azure AD / Google Workspace SSO (OIDC & SAML 2.0) + Bắt buộc MFA       │
 │ • Enterprise Context Injector: Gắn JWT Token mang User ID, Role (RBAC), Department (ABAC)        │
 └──────────────────────────────────────────────┬───────────────────────────────────────────────────┘
                                                │ AWS Private Subnet (ap-southeast-1 Singapore)
                                                ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ [ALB-01] AWS APPLICATION LOAD BALANCER (Multi-AZ: ap-southeast-1a & 1b)                          │
 └──────────────────────────────────────────────┬───────────────────────────────────────────────────┘
                                                │ Internal Traffic
                                                ▼
 ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ MÔI TRƯỜNG PRODUCTION (Chạy 24/7 - 730 giờ/tháng - HA Multi-AZ - SLA 99,5% Hành chính)           │
 │                                                                                                  │
 │  ┌────────────────────────────────────────────────────────────────────────────────────────────┐  │
 │  │ [APP-01] CORE AGENT ORCHESTRATION CLUSTER (FastAPI + LangGraph on AWS EKS Multi-AZ)        │  │
 │  │ • [SEC-01] Guardrail Engine: Microsoft Presidio PII Masking, Anti-Injection Scanner       │  │
 │  │ • [CAC-01] Tier 0 Semantic Cache (ElastiCache Redis Multi-AZ): Giảm 18% queries (<30ms)   │  │
 │  │ • [ROU-01] LLM Dynamic Router & Model Selector (Tier 1 -> Tier 2 -> Tier 3)               │  │
 │  │ • [HITL-01] Human-in-the-loop Breakpoint: Tạm dừng duyệt lệnh ghi email, Jira, Confluence  │  │
 │  │ • [QUE-01] Background Task Queue: Temporal.io + Celery Worker cho Agent Cấp 4 chạy nền     │  │
 │  └───────┬─────────────────────────┬──────────────────────────┬───────────────────────────────┘  │
 │          │                         │                          │                                  │
 │          ▼                         ▼                          ▼                                  │
 │  ┌───────────────────────┐ ┌──────────────────────┐ ┌─────────────────────────────────────────┐  │
 │  │ [RAG-01] ENTERPRISE   │ │ [SBX-01] SECURE CODE │ │ [STG-01] PERSONAL WORKSPACE STORAGE     │  │
 │  │ SEARCH & INGESTION    │ │ SANDBOX POOL         │ │                                         │  │
 │  │ • [CON-01] SaaS Conn: │ │ • Firecracker /      │ │ • S3 Prefix per-user:                   │  │
 │  │   M365, Google, Jira, │ │   gVisor runsc Micro │ │   s3://vbot-corp/workspaces/{user_id}/  │  │
 │  │   Confluence, Notion  │ │ • Zero Egress Net    │ │ • Hard Quota: 10 GB/User (4 TB thực tế) │  │
 │  │ • [VLT-01] OAuth Vault│ │   (Chặn 100% LAN/Net)│ │ • STS Dynamic Pre-signed URL (10 phút)  │  │
 │  │   (Secrets Mgr + KMS) │ │ • 1 vCPU, 1 GB RAM   │ │ • [DB-01] State Store: PostgreSQL Multi │  │
 │  │ • [DB-01] Vector DB:  │ │ • Ephemeral (45s TTL,│ │   -AZ `db.r6g.xlarge` kích hoạt RLS     │  │
 │  │   Postgres pgvector   │ │   Destroy-on-exit)   │ │   (Row-Level Security per User ID)      │  │
 │  │ • Pre-filter ACL bắt  │ └──────────────────────┘ └─────────────────────────────────────────┘  │
 │  │   buộc tại Vector DB  │                                    │                                  │
 │  └───────────────────────┘                                    │                                  │
 │          │                                                    │                                  │
 │          └─────────────────────────┬──────────────────────────┘                                  │
 │                                    ▼                                                             │
 │  ┌────────────────────────────────────────────────────────────────────────────────────────────┐  │
 │  │ [LOG-01] IMMUTABLE AUDIT & COMPLIANCE VAULT                                                │  │
 │  │ • Kafka Stream -> AWS S3 Glacier Instant Retrieval với WORM Object Lock khóa đúng 12 tháng │  │
 │  │ • [NET-01] AWS PrivateLink / VPC Endpoints: Kênh riêng gọi API Model (OpenAI / Anthropic)   │  │
 │  │ • [FIN-01] AWS Budgets & LiteLLM Proxy: Giám sát hạn mức Quota và tự động cắt tải phân tầng │  │
 │  └────────────────────────────────────────────────────────────────────────────────────────────┘  │
 └──────────────────────────────────────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ [STAG-01] MÔI TRƯỜNG STAGING (Chạy Giờ Hành Chính: 22 ngày x 10h = 220h/tháng - Tự tắt ngoài giờ) │
 │ • Cấu hình tinh gọn 1:4 Prod: 1 Node EKS `t4g.xlarge` + RDS Single-AZ + Redis Single Node        │
 │ • [EVAL-01] Eval Gateway: Test suite 200+ kịch bản benchmark chất lượng >= 95% trước khi release  │
 └──────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## SLIDE 3: LUỒNG MỘT REQUEST (END-TO-END REQUEST LIFECYCLE)

### Trình tự 10 bước xử lý một Request điển hình (Từ Client đến Model và ngược lại):

```
[User] ──(1) Prompt + Auth──> [ING-01 WAF] ──(2) Check SSO/MFA──> [IDP-01]
                                    │
                               (3) Valid JWT
                                    ▼
[User] <──(10) Stream Token── [APP-01 Core] <──(4) Scrub PII── [SEC-01 Guardrail]
       ▲                            │
       │                       (5) Query Cache
       │                            ▼
       │                      [CAC-01 Redis] ── Hit (18%) ──> Trả kết quả < 30ms
       │                            │ Miss (82%)
       │                            ▼
       │                      [ROU-01 Router]
       │                       /    │    \
       │         ┌────────────┘     │     └────────────┐
       │     (6a) RAG          (6b) Sandbox       (6c) Agent Tool
       │         ▼                  ▼                  ▼
       │   [DB-01 pgvector]   [SBX-01 MicroVM]   [CON-01 SaaS / Jira]
       │   (Pre-filter ACL)   (Zero Egress 15s)   (OAuth Vault + HITL)
       │         \                  │                 /
       │          └───────────┐     │     ┌──────────┘
       │                      ▼     ▼     ▼
       │               (7) Enriched Safe Context
       │                            │
       │                   [NET-01 PrivateLink]
       │                            │
       │                            ▼
       │               [EXT-01 Model API (ZDR)]
       │               (GPT-4o-mini / Sonnet 3.5)
       │                            │
       │                   (8) Raw Token Stream
       │                            ▼
       │               [SEC-01 De-anonymize PII]
       │                            │
       └────────────── (9) Async Log ──> [LOG-01 S3 Glacier WORM 12M]
```

* **Bước 1 – 3 (Ingress & Auth):** Request qua Cloudflare WAF `[ING-01]` chống DDoS/Injection, xác thực SSO/MFA `[IDP-01]`, cấp JWT Token chứa `user_id`, `role`, `department`.
* **Bước 4 – 5 (Guardrail & Cache):** Presidio `[SEC-01]` che mờ PII; kiểm tra Semantic Cache `[CAC-01]` (nếu hit trả về ngay sau <30ms).
* **Bước 6 (Phân luồng & Thực thi nghiệp vụ):**
  * *Nếu tra cứu:* `[DB-01]` thực hiện **Pre-filtering ACL** lọc tài liệu người dùng có quyền trước khi tính Cosine similarity.
  * *Nếu phân tích code:* `[SBX-01]` khởi động MicroVM gVisor cô lập hoàn toàn mạng (Zero Egress), xuất biểu đồ về `[STG-01]` rồi tự hủy.
  * *Nếu thao tác Jira/Email:* Lấy token từ `[VLT-01]`, nếu là lệnh ghi $\rightarrow$ Kích hoạt `[HITL-01]` chờ người dùng bấm xác nhận.
* **Bước 7 – 8 (Gọi Model & Kiểm duyệt Output):** Context an toàn truyền qua AWS PrivateLink `[NET-01]` sang mô hình (OpenAI/Anthropic có cam kết ZDR); nhận token streaming và giải mã PII cục bộ.
* **Bước 9 – 10 (Audit & Streaming):** Bắn log bất biến vào `[LOG-01]` S3 Glacier WORM (12 tháng); stream token trực tiếp về giao diện người dùng qua SSE/WebSocket (TTFT p95 $\le$ 3s).

---

## SLIDE 4: MODEL VÀ ROUTING STRATEGY

### 1. Bảng phân bổ Model cho 5 cấp tác vụ (Cam kết chất lượng $\ge$ 95%)

| Cấp tác vụ | Tỉ lệ tải | Model Phục vụ (Tối ưu FinOps) | Model Tham chiếu | Điểm chất lượng | Chi phí Input / Output per 1M |
| :--- | :---: | :--- | :--- | :---: | :--- |
| **Cấp 1: Email & FAQ** | 45% | **GPT-4o-mini** | GPT-4o | **96,8%** | \$0.15 / \$0.60 |
| **Cấp 2: Tài liệu & Slide** | 25% | **80% GPT-4o-mini + 20% Sonnet** | Claude 3.5 Sonnet | **95,4%** | Sonnet: \$3.00 (Cache: \$0.375) / \$15.00 |
| **Cấp 3: Dữ liệu & Code** | 12% | **Claude 3.5 Sonnet** + gVisor | Claude 3.5 Sonnet | **100,0%** | Dùng Prompt Caching mẫu data |
| **Cấp 4: Agent Dự án** | 10% | **Claude 3.5 Sonnet** + LangGraph | GPT-4o | **97,2%** | Function Calling chuẩn xác |
| **Cấp 5: Thiết kế & Ảnh** | 8% | **GPT-4o-mini** (Sơ đồ) + **FLUX.1** | DALL-E 3 / GPT-4o | **95,1%** | FLUX.1: \$0,003 / ảnh |

### 2. Chiến lược Prompt Caching (Đòn bẩy FinOps cốt lõi)
* System prompt, tool schemas và context RAG lớn (>1.024 tokens) được lưu cache tại nhà cung cấp:
  * **Cache Write:** \$3.75 / 1M | **Cache Read:** **\$0.375 / 1M (Giảm 80% so với giá gốc \$3.00)**.
  * Giúp giảm chi phí Token của Tier 3 từ \$8.600 xuống còn **\$3.208/tháng**.

### 3. Phân tích: API vs Tự Host GPU (Điểm hòa vốn)
* **Chi phí tự host cụm GPU Frontier (8x NVIDIA H100):** Tối thiểu **\$14.000 – \$18.000 USD/tháng** (máy chủ, điện toán, MLOps, cụm dự phòng HA).
* **Chi phí API VBot hiện tại (2.000 DAU):** Chỉ **\$5.225 USD/tháng**.
* **Điểm hòa vốn:** Chỉ xảy ra khi quy mô đạt **> 8.000 – 10.000 DAU** (> 15 – 20 triệu tokens/ngày). Ở quy mô 2.000 DAU, **dùng Commercial API Hybrid rẻ hơn 67%** và loại bỏ 100% rủi ro lỗi thời phần cứng GPU.
* **Tải giờ cao điểm:** 5.000 output tokens/giây được phủ trọn vẹn bằng hạn ngạch API 1,2M TPM (Tier 4 OpenAI + Anthropic) thay vì phải duy trì 32 chip GPU H100 tốn > \$60.000/tháng.

---

## SLIDE 5: LÝ DO CHỌN CÔNG NGHỆ (TECHNOLOGY SELECTION & TRADE-OFFS)

Bảng đối chiếu ít nhất 2 phương án cho 4 quyết định kiến trúc then chốt:

```
┌─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
│ Thành phần & Lựa chọn           │ Phương án Đề xuất (CHỌN)        │ Phương án Đối ứng (LOẠI)        │
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ 1. Vector Database              │ AWS RDS PostgreSQL (pgvector)   │ Qdrant / Pinecone Dedicated     │
│ • Chi phí / tháng               │ $399 (Multi-AZ db.r6g.xlarge)   │ $750 - $1.200 (Cloud Cluster)   │
│ • Quản trị dữ liệu & ACID       │ Đồng nhất trong 1 DB quan hệ    │ Phân tán, rủi ro lệch đồng bộ   │
│ • Khả năng Pre-filter ACL       │ Cực mạnh bằng SQL WHERE metadata│ Giới hạn payload filter         │
│ • Lý do chọn                    │ Tiết kiệm 50% phí, tích hợp sâu RLS, zero cross-system latency │
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ 2. Code Execution Sandbox       │ Firecracker MicroVM / gVisor    │ Docker Container truyền thống   │
│ • Thời gian khởi tạo (Spin-up)  │ < 150 ms (từ RAM snapshot)      │ 1,5 - 3,0 giây                  │
│ • Cô lập Kernel (Isolation)     │ Cấp độ Phần cứng / Virtualized  │ Dùng chung Host Kernel (Rủi ro) │
│ • Nguy cơ Container Escape      │ Triệt tiêu (Hardware boundary)  │ Rất cao (RCE, Privilege Esc.)   │
│ • Lý do chọn                    │ Bảo vệ an toàn tuyệt đối mạng tập đoàn, khởi động sub-second    │
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ 3. Mô hình Phục vụ LLM          │ Hybrid API (Prompt Caching)     │ Self-Hosted Llama 3 70B on GPU  │
│ • Chi phí vận hành / tháng      │ $5.225 USD / tháng              │ $14.000 - $18.000 USD / tháng   │
│ • Khả năng suy luận & Tool Call │ Xuất sắc (Claude 3.5 / GPT-4o)  │ Trung bình, dễ sai schema JSON  │
│ • Thời gian tới token đầu (TTFT)│ ~400 - 600 ms                   │ 1.200 - 2.500 ms (hàng đợi GPU) │
│ • Lý do chọn                    │ Rẻ hơn 67%, không tốn chi phí MLOps, đảm bảo TTFT p95 <= 3s     │
├─────────────────────────────────┼─────────────────────────────────┼─────────────────────────────────┤
│ 4. Cloud Region                 │ AWS ap-southeast-1 (Singapore)  │ AWS us-east-1 (Mỹ)              │
│ • Độ trễ mạng (RTT) về VN       │ 25 - 35 ms                      │ 220 - 260 ms                    │
│ • Đạt cam kết TTFT p95 <= 3s    │ Hoàn toàn đạt (Dư địa 2,4s)     │ Rất khó đạt khi có mạng biến động│
│ • Chủ quyền dữ liệu (Sovereignty│ Tối ưu tuân thủ ASEAN & VN      │ Rủi ro pháp lý xuyên lục địa    │
│ • Lý do chọn                    │ Độ trễ tối ưu cho trải nghiệm người dùng doanh nghiệp Việt Nam  │
└─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
```

---

## SLIDE 6: CONNECTORS VÀ PHÂN QUYỀN (SECURITY & PERMISSIONS)

### 1. Cơ chế Ủy quyền On-Behalf-Of Delegation (Không dùng Service Account chung)
* **Nguyên tắc:** Nhân viên A chỉ được VBot hỗ trợ đọc/ghi dữ liệu mà nhân viên A có quyền truy cập trên SaaS gốc.
* **Luồng xác thực:** OAuth 2.0 Authorization Code Flow kèm PKCE.
* **Scope tối thiểu (Least Privilege):**
  * Google Workspace: Chỉ xin `drive.readonly` hoặc `drive.file`.
  * Microsoft 365: Chỉ xin `Files.Read.Selected`, `Mail.ReadWrite`.
  * Jira: Chỉ xin `read:jira-work`, `write:jira-work` trên dự án được phân công.

### 2. Quản lý Token trong Vault mã hóa 2 lớp (Envelope Encryption)
* **Nơi cất giữ:** **AWS Secrets Manager**, tách biệt vật lý khỏi cơ sở dữ liệu ứng dụng.
* **Mã hóa:** Data Key mã hóa Token $\rightarrow$ Master Key **AWS KMS CMK** mã hóa Data Key.
* **Quyền giải mã:** Chỉ gán cho IAM Role nội bộ của Pod Connector (`IRSA`). Quản trị viên hệ thống (Admin, DBA) không thể đọc plaintext.

### 3. Đồng bộ & Bảo toàn phân quyền tài liệu (ACL Preservation)
* **Metadata lưu trữ:** Mỗi chunk vector lưu mảng `allowed_users` và `allowed_groups`.
* **Cơ chế Pre-filtering (Lọc trước):**
  ```sql
  -- Thực thi tại Database trước khi tính Cosine Similarity:
  WHERE (allowed_users ? :user_id) OR (allowed_groups && :user_groups);
  ```
* **Vì sao Pre-filter bắt buộc?** Nếu dùng Post-filter (lấy Top-K rồi mới lọc), các tài liệu mật của người khác sẽ chiếm hết Top-K khiến người dùng không nhận được câu trả lời (False Negative), hoặc rủi ro rò rỉ khi lọc sót. Pre-filter triệt tiêu 100% rủi ro leo thang đặc quyền.

---

## SLIDE 7: WORKSPACE RIÊNG VÀ SANDBOX CÔ LẬP

### 1. Cô lập dữ liệu cá nhân (Personal Workspace Isolation)
* **Phân tách tệp tin:** Sử dụng **Prefix** trên cùng S3 Bucket:
  `s3://vbot-corp-prod/workspaces/{tenant_id}/{user_hashed_id}/`
  *(AWS giới hạn 100 buckets/account $\rightarrow$ Dùng prefix mở rộng vô hạn, tối ưu hiệu năng).*
* **Kiểm soát truy cập:** Cấp quyền động qua **AWS STS AssumeRole / Pre-signed URL (hạn 10 phút)** gắn chặt với `user_hashed_id`. Nhân viên A tuyệt đối không thể đọc/ghi vào prefix của nhân viên B.
* **Mã hóa dữ liệu tĩnh (At Rest):** AES-256 qua **AWS KMS CMK**.
* **Cô lập bộ nhớ hội thoại:** **PostgreSQL Row-Level Security (RLS)** ở cấp database kernel:
  `WHERE user_id = current_setting('app.current_user_id')`.

### 2. Môi trường Sandbox thực thi mã an toàn (Secure Sandbox Pool)
* **Công nghệ:** Cụm **Firecracker MicroVMs / gVisor (`runsc`)** trên 2 node `c6i.xlarge` chuyên dụng.
* **Khởi tạo siêu tốc:** Sub-second (< 150 ms) từ memory snapshot đóng gói sẵn Python 3.11, pandas, numpy, matplotlib, seaborn, openpyxl.
* **Cách ly mạng tuyệt đối (Air-gapped Zero Egress):**
  * NetworkPolicy chặn 100% kết nối Internet.
  * Chặn toàn bộ dải mạng LAN nội bộ doanh nghiệp (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`). Không thể rò rỉ dữ liệu qua SSRF hay DNS tunneling.
* **Hạn mức tài nguyên cứng:** Tối đa **1.0 vCPU, 1.0 GB RAM, 512 MB disk**, timeout **45 giây / lệnh**.
* **Vòng đời Ephemeral:** Xuất kết quả (file ảnh/Excel) về S3 người dùng xong là tiêu hủy hoàn toàn (Destroy-on-exit), xóa sạch RAM.

---

## SLIDE 8: AI VÀ DATA GOVERNANCE

### 1. Hàng rào bảo vệ (Guardrails In/Out) & Chống Prompt Injection
* **Inbound Guardrail:** Quét kiểm tra jailbreak, system prompt override.
* **Chống Indirect Prompt Injection từ Connectors:** Dữ liệu từ email bên ngoài, ticket Jira được bọc trong thẻ dữ liệu cô lập `<untrusted_connector_data>...</untrusted_connector_data>` và đi qua bộ phân loại SLM Injection Classifier trước khi đưa vào context.
* **Outbound Guardrail:** Kiểm tra câu trả lời, ngăn chặn rò rỉ dữ liệu nhạy cảm hoặc sinh mã độc.

### 2. Cơ chế Xác nhận Người dùng (Human-in-the-loop - HITL)
* Bắt buộc người dùng bấm xác nhận trực tiếp (Phê duyệt / Từ chối) trước khi Agent thực hiện:
  1. Gửi email từ tài khoản cá nhân.
  2. Tạo mới, sửa, đóng ticket trên Jira.
  3. Cập nhật hoặc xuất bản trang trên Confluence / Notion.
  4. Xóa hoặc ghi đè file trong Workspace.

### 3. Data Loss Prevention (DLP) & Phân loại dữ liệu
* **Microsoft Presidio:** Tự động che mờ (Masking) số CCCD/CMND, thẻ ngân hàng, secret key thành `[REDACTED_CCCD_1]`. Giải mã cục bộ khi trả về cho chủ sở hữu.
* **Phân loại dữ liệu:** 4 cấp độ (`Public`, `Internal`, `Confidential`, `Restricted`). Cấp `Restricted` bị cấm tuyệt đối không được gửi qua LLM bên ngoài.

### 4. Cổng Kiểm định (Eval Gateway) & Audit Log 12 tháng
* **Eval Gateway:** Chạy bộ test tự động 200+ kịch bản trên Staging trước khi đổi model hoặc sửa prompt. Bắt buộc đạt tỷ lệ chống injection 100% và độ chính xác RAG $\ge 95\%$.
* **Immutable Audit Log:** Toàn bộ prompt, context, response, token đẩy qua Kafka vào **AWS S3 Glacier Instant Retrieval** bật **WORM Object Lock khóa cố định 12 tháng**.

---

## SLIDE 9: HA, BACKUP VÀ DISASTER RECOVERY

### 1. Cam kết Độ sẵn sàng & Kiến trúc Không Điểm lỗi đơn (No SPOF)
* **Cam kết SLA:** $\ge \mathbf{99,5\%}$ trong giờ hành chính (downtime cho phép $\le 1,1$ giờ/tháng).
* **Kiến trúc Multi-AZ:**
  * Ingress Load Balancer: Cloudflare Anycast WAF + AWS ALB Multi-AZ.
  * Cụm Compute EKS: Tối thiểu 3 Node trải trên 2 AZs (`ap-southeast-1a`, `ap-southeast-1b`).
  * Cơ sở dữ liệu: AWS RDS PostgreSQL Multi-AZ (Active-Standby đồng bộ, tự động failover < 60s).
  * Bộ nhớ đệm: AWS ElastiCache Redis Cluster Multi-AZ có replica tự động thăng cấp.

### 2. Chiến lược Backup & Khôi phục Thảm họa (DR)
* **Sao lưu liên tục:**
  * RDS PostgreSQL Snapshot tự động hàng ngày + Continuous WAL Streaming 5 phút/lần lên S3.
  * S3 Workspace: Bật S3 Versioning và Cross-Region Replication (CRR) sang Singapore $\rightarrow$ Sydney (`ap-southeast-2`).
* **Chỉ số RTO & RPO:**
  * **RTO (Recovery Time Objective):** $\le \mathbf{4\text{ giờ}}$ (thời gian khôi phục hoàn toàn dịch vụ).
  * **RPO (Recovery Point Objective):** $\le \mathbf{1\text{ giờ}}$ (nhờ WAL streaming 5 phút/lần, mất mát dữ liệu tối đa thực tế $\le 5$ phút).
* **Diễn tập khôi phục định kỳ (Recovery Drills):** **01 lần / tháng**, hệ thống tự động restore snapshot sang môi trường Staging, kiểm tra tính toàn vẹn 10.000 bản ghi và đo thời gian thực tế.

---

## SLIDE 10: MONITORING VÀ FINOPS

### 1. Hệ thống Giám sát & 4 Golden Signals (Tự host $0 chi phí thêm)
* Cài đặt **Prometheus + Grafana + Loki + OpenTelemetry** ngay trên cụm EKS:
  * **Latency:** Giám sát p95 TTFT ($\le 3$ giây) và thời gian thực thi Agent ($\le 10$ phút).
  * **Traffic:** Theo dõi RPS (bình thường 2,22 RPS, đỉnh 10 RPS), Token/giây.
  * **Errors:** Tỷ lệ lỗi HTTP 5xx, lỗi LLM Provider Rate Limit (429).
  * **Saturation:** Tải CPU/RAM cụm EKS, số kết nối RDS PostgreSQL, tỷ lệ đầy bộ nhớ Redis.

### 2. Cảnh báo Ngân sách Đa tầng (Budget Alerting)
* Tích hợp **AWS Budgets + LiteLLM Spend Tracking**:
  * **Mức 1 (70% ngân sách):** Gửi email báo cáo cho Quản trị viên và Trưởng phòng ban.
  * **Mức 2 (85% ngân sách):** Gửi cảnh báo Warning vào kênh Slack FinOps Core Team.
  * **Mức 3 (100% ngân sách):** Gửi cảnh báo Critical và kích hoạt cơ chế cắt tải phân tầng.

### 3. Cơ chế Quota & Cắt tải Phân tầng (Graceful Degradation)
* **Quota cá nhân:** Soft Quota 35 req/ngày (cảnh báo); Hard Quota 50 req/ngày (~$0.30/user/ngày).
* **Khi vượt 100% Hard Quota:**
  * **Không cắt đột ngột:** Không làm gián đoạn công việc của nhân viên.
  * **Hạ cấp mô hình:** Tự động chuyển toàn bộ yêu cầu về **Tier 0 (Semantic Cache)** và **Tier 2 (GPT-4o-mini)** chi phí thấp.
  * **Tạm khóa tính năng cao cấp:** Khóa gọi Claude 3.5 Sonnet, khóa Sandbox Cấp 3, khóa Agent Cấp 4 và sinh ảnh Cấp 5. Mở lại khi được Trưởng phòng duyệt thêm Quota qua giao diện 1-click.

---

## SLIDE 11: CHI PHÍ TỔNG HỢP VÀ ĐÒN BẨY TIẾT KIỆM (FINOPS TCO)

### 1. Bảng chốt Chi phí Toàn diện (Chạy 2.000 DAU)
* **Tổng chi phí hằng tháng:** **~\$7.313,61 USD / tháng**
* **Đơn giá trên từng nhân viên:** **\$3,66 USD / user / tháng** (~91.500 VNĐ/tháng).
* *So sánh thị trường:* Rẻ hơn **87,8%** so với Microsoft 365 Copilot (\$30/user = \$60.000/tháng).

### 2. Top 5 Hạng mục Chi phí Lớn nhất

```
┌─────────────────────────────────────────────────────────────┬──────────────┬────────────┐
│ Hạng mục Chi phí                                            │ USD / Tháng  │ Tỉ trọng   │
├─────────────────────────────────────────────────────────────┼──────────────┼────────────┤
│ 1. API Mô hình LLM (Tier 2 GPT-4o-mini & Tier 3 Sonnet 3.5) │ $5.031,13    │ 68,8%      │
│ 2. Database & Vector Store (RDS Multi-AZ db.r6g.xlarge)     │ $399,14      │ 5,5%       │
│ 3. Compute Nodes Core (3 node EKS m6i.xlarge Savings/Spot)  │ $183,23      │ 2,5%       │
│ 4. Môi trường Staging (Chạy 220h hành chính, tắt ngoài giờ) │ $175,25      │ 2,4%       │
│ 5. Cụm Code Sandbox Nodes (2 node c6i.xlarge Reserved)      │ $148,92      │ 2,0%       │
│ Các thành phần còn lại (Redis, S3, WAF, NAT, Egress, Dự phòng)│ $1.375,94   │ 18,8%      │
├─────────────────────────────────────────────────────────────┼──────────────┼────────────┤
│ TỔNG CHI PHÍ VẬN HÀNH HẰNG THÁNG                            │ ~$7.313,61   │ 100,0%     │
└─────────────────────────────────────────────────────────────┴──────────────┴────────────┘
```

### 3. Năm Đòn bẩy Tiết kiệm Lớn nhất (Kèm số USD cụ thể)
1. **Phân luồng 4 Tier + Prompt Caching:** Tiết kiệm **\$13.275 USD/tháng** (từ \$18.500 xuống \$5.225, giảm 71,8% chi phí API).
2. **Staging chạy giờ hành chính (220h vs 730h):** Tiết kiệm **\$1.025 USD/tháng** (từ \$1.200 xuống \$175, giảm 85,4%).
3. **Tự host Sandbox microVM gVisor vs thuê E2B:** Tiết kiệm **\$1.640 USD/tháng** (từ \$1.800 xuống \$160, giảm 91%).
4. **Sinh ảnh FLUX.1 Schnell vs DALL-E 3:** Tiết kiệm **\$976 USD/tháng** (từ \$1.056 xuống \$79,20, giảm 92,5%).
5. **Karpenter Spot + Compute Savings Plans cho EKS:** Tiết kiệm **\$260 USD/tháng** (giảm 58% so với On-Demand).
* 👉 **TỔNG TIẾT KIỆM SO VỚI THIẾT KẾ CHƯA TỐI ƯU:** **~\$17.686 USD / THÁNG (TIẾT KIỆM 70,7%)**.

---

## SLIDE 12: QUẢN TRỊ RỦI RO VÀ MỞ RỘNG (SCALE TO 4.000 DAU)

### 1. Ma trận Top 3 Rủi ro Lớn nhất & Biện pháp Kiểm soát
1. **Rò rỉ dữ liệu chéo phòng ban qua RAG:**  
   * *Kiểm soát:* Bắt buộc Pre-filtering ACL tại Vector Database kết hợp PostgreSQL Row-Level Security (RLS). Triệt tiêu 100% rủi ro đọc chéo.
2. **Tấn công gián tiếp Prompt Injection từ Email / Jira ngoài:**  
   * *Kiểm soát:* Bọc dữ liệu trong thẻ cô lập `<untrusted_connector_data>`, quét qua SLM Guardrail và bắt buộc Human-in-the-loop (HITL) phê duyệt trước khi ghi.
3. **Spike chi phí bất thường do vòng lặp Agent vô tận:**  
   * *Kiểm soát:* Hard timeout 10 phút, Quota cứng theo ngày, Rate limiting và hệ thống Budget Alerting tự động cắt tải khi chạm ngưỡng 100%.

### 2. Kịch bản Mở rộng khi Quy mô DAU GẤP ĐÔI (Từ 2.000 lên 4.000 DAU)
* **Quy luật tăng trưởng chi phí:** **Tăng phi tuyến dạng Lợi thế theo quy mô (Sub-linear Scaling)**:
  * *Chi phí API Token:* Tăng từ \$5.225 lên **~\$9.400 USD/tháng** (nhờ quy mô lớn làm tăng tỷ lệ hit Semantic Cache từ 18% lên 23% – 25%).
  * *Chi phí Hạ tầng Cloud:* Chỉ tăng nhẹ ~35% – 40% (EKS tự scale thêm 2 node Spot qua Karpenter, RDS tăng dung lượng lưu trữ gp3, NAT/WAF tăng rất ít) $\rightarrow$ Từ \$1.248 lên **~\$1.750 USD/tháng**.
  * *Chi phí Staging:* Giữ nguyên **\$175 USD/tháng**.
  * *Quỹ dự phòng (10%):* **~\$1.130 USD/tháng**.
* **Tổng chi phí dự kiến tại 4.000 DAU:** **~\$12.455 USD / tháng**.
* **HIỆU QUẢ KINH TẾ QUY MÔ (UNIT ECONOMICS TIẾP TỤC GIẢM):**  
  $$\text{Chi phí / DAU tại 4.000 users} = \frac{\$12.455}{4.000\text{ DAU}} = \mathbf{\$3,11\text{ USD / user / tháng}}\text{ (Giảm thêm 15% so với mức \$3,66)}$$

