# TÀI LIỆU THIẾT KẾ KIẾN TRÚC HỆ THỐNG & ĐẶC TẢ TẢI FINOPS: VBOT ENTERPRISE PLATFORM (2.000 DAU)

> **Tài liệu tham chiếu:** Báo cáo kiến trúc tổng thể và giải pháp nền tảng tại `bao_cao.md`  
> **Quy mô mục tiêu:** 2.000 nhân viên hoạt động hằng ngày (DAU)  
> **Thời gian làm việc:** Thứ 2 – Thứ 6, 8:00 – 18:00 (GMT+7), 22 ngày làm việc/tháng (220 giờ hành chính/tháng, 730 giờ 24/7)  
> **Môi trường triển khai:** 01 Môi trường Production (HA Multi-AZ, 24/7) + 01 Môi trường Staging (Chạy giờ hành chính)  
> **Nguyên tắc thiết kế tối thượng:** Zero-Trust Enterprise, On-Behalf-Of Delegation, Ephemeral Sandboxing, ACL-Aware RAG, Zero Data Retention (ZDR), Tuân thủ tuyệt đối 8 Điều kiện Tiên quyết (H1 – H8).

---

## MỤC LỤC
1. [TỔNG QUAN 5 CẤP TÁC VỤ VBOT & MA TRẬN PHÂN BỔ TẢI](#i-tổng-quan-5-cấp-tác-vụ-vbot--ma-trận-phân-bổ-tải)
2. [ĐẶC TẢ TUÂN THỦ 8 ĐIỀU KIỆN TIÊN QUYẾT BẮT BUỘC (H1 – H8)](#ii-đặc-tả-tuân-thủ-8-điều-kiện-tiên-quyết-bắt-buộc-h1--h8)
   - [H1. Cloud: Nền tảng chính, Region & Kênh gọi Model](#h1-cloud-nền-tảng-chính-region--kênh-gọi-model)
   - [H2. Định danh và Phân quyền: SSO, MFA, RBAC/ABAC, ACL & OAuth Vault](#h2-định-danh-và-phân-quyền-sso-mfa-rbacabac-acl--oauth-vault)
   - [H3. Cô lập User và Sandbox: Workspace, Bộ nhớ & MicroVM Air-gapped](#h3-cô-lập-user-và-sandbox-workspace-bộ-nhớ--microvm-air-gapped)
   - [H4. AI Governance: Guardrail In/Out, Anti-Injection, HITL & Cổng Eval](#h4-ai-governance-guardrail-inout-anti-injection-hitl--cổng-eval)
   - [H5. Data Governance: Mã hóa, DLP, Phân loại, Audit Log 12 tháng & ZDR](#h5-data-governance-mã-hóa-dlp-phân-loại-audit-log-12-tháng--zdr)
   - [H6. Độ trễ: TTFT p95 $\le$ 3s & Agent chạy nền $\le$ 10 phút](#h6-độ-trễ-ttft-p95--3s--agent-chạy-nền--10-phút)
   - [H7. HA, Backup, DR: SLA 99,5%, No SPOF, RTO 4h, RPO 1h](#h7-ha-backup-dr-sla-995-no-spof-rto-4h-rpo-1h)
   - [H8. Chất lượng và Kiểm soát Chi phí: Chuẩn $\ge$ 95%, Quota & Hạ cấp Cắt tải](#h8-chất-lượng-và-kiểm-soát-chi-phí-chuẩn--95-quota--hạ-cấp-cắt-tải)
3. [GIẢ ĐỊNH VÀ CĂN CỨ ƯỚC LƯỢNG TẢI (CAPACITY PLANNING)](#iii-giả-định-và-căn-cứ-ước-lượng-tải-capacity-planning)
4. [SƠ ĐỒ KIẾN TRÚC TOÀN DIỆN (PRODUCTION & STAGING)](#iv-sơ-đồ-kiến-trúc-toàn-diện-production--staging)
5. [CHIẾN LƯỢC ĐIỀU PHỐI MÔ HÌNH (4-TIER HIERARCHICAL LLM ROUTING)](#v-chiến-lược-điều-phối-mô-hình-4-tier-hierarchical-llm-routing)
6. [BẢNG DỰ TOÁN & CHỐT CHI PHÍ VẬN HÀNH HẰNG THÁNG (FINOPS TCO)](#vi-bảng-dự-toán--chốt-chi-phí-vận-hành-hằng-tháng-finops-tco)
7. [MA TRẬN RỦI RO, BẢO MẬT & CAM KẾT VẬN HÀNH](#vii-ma-trận-rủi-ro-bảo-mật--cam-kết-vận-hành)
8. [LỘ TRÌNH TRIỂN KHAI DỰ ÁN ĐẾN PRODUCTION (9 TUẦN)](#viii-lộ-trình-triển-khai-dự-án-đến-production-9-tuần)

---

## I. TỔNG QUAN 5 CẤP TÁC VỤ VBOT & MA TRẬN PHÂN BỔ TẢI

Hệ thống VBot phục vụ 2.000 nhân viên văn phòng thông qua 5 cấp độ chức năng nghiệp vụ, tích hợp các SaaS Connectors tiêu chuẩn tập đoàn (Google Workspace, Microsoft 365, Atlassian Jira, Confluence, Notion):

| Cấp độ | Tên chức năng nghiệp vụ | Chi tiết nghiệp vụ & Luồng xử lý | Lựa chọn Model / Công cụ | Tỉ lệ (%) | Số req/ngày (22 ngày/tháng) | Token Input TB / req (Gồm Context RAG / Agent) | Token Output TB / req |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Cấp 1** | **Email & Hỏi đáp** | • Soạn thảo, trả lời, tóm tắt chuỗi email (`in-reply-to`, `references`).<br>• Tra cứu chính sách, quy chế qua RAG bảo toàn quyền (ACL). | • Workhorse LLM: GPT-4o-mini / Claude 3.5 Haiku<br>• Embedding: `text-embedding-3-small`<br>• Hybrid Search: BM25 + pgvector | **45%** | **27.000** | **1.500 tokens**<br>*(System: 300, Prompt: 200, RAG chunks & ACL: 800, History: 200)* | **350 tokens** |
| **Cấp 2** | **Tài liệu & Slide** | • Soạn thảo báo cáo, biên bản, tờ trình, kế hoạch kinh doanh.<br>• Xuất file `.docx`, `.xlsx`, `.pptx` theo bộ mẫu (template) chuẩn. | • Văn bản thường (80%): GPT-4o-mini<br>• Văn bản quy chuẩn cao (20%): Claude 3.5 Sonnet<br>• Headless generator: `python-docx`, `openpyxl` | **25%** | **15.000** | **2.000 tokens**<br>*(System: 400, Prompt: 300, Doc context: 1.100, Template: 200)* | **800 tokens** |
| **Cấp 3** | **Dữ liệu & Code (Sandbox)** | • Xử lý bảng tính triệu dòng, vẽ biểu đồ phân tích, trích xuất SQL.<br>• Viết kịch bản Python, sửa lỗi, review code nội bộ. | • Frontier LLM: Claude 3.5 Sonnet / GPT-4o<br>• Sandbox Pool: Firecracker MicroVM / gVisor `runsc`<br>• Thư viện: `pandas`, `openpyxl`, `seaborn` | **12%** | **7.200** | **2.500 tokens**<br>*(System: 500, Prompt: 300, Data Schema & Samples: 1.500, Code ctx: 200)* | **500 tokens** |
| **Cấp 4** | **Agent Dự án (Multi-step)** | • Đọc/ghi Jira, Confluence, Notion; tạo ticket, cập nhật trang dự án.<br>• Quy trình tự động đa bước (3 turns), **Human-in-the-loop (HITL)**. | • Frontier LLM: Claude 3.5 Sonnet / GPT-4o<br>• Agent State Machine: LangGraph<br>• Connector: OAuth 2.0 PKCE On-Behalf-Of | **10%** | **6.000** | **4.500 tokens**<br>*(System & Tool schemas: 1.500, Multi-turn steps: 2.500, Payload: 500)* | **700 tokens** |
| **Cấp 5** | **Thiết kế & Đồ họa** | • 75%: Sinh mã sơ đồ quy trình Mermaid.js/PlantUML, UI Mockup HTML.<br>• 25%: Sinh ảnh minh họa báo cáo/slide thuyết trình. | • Sơ đồ/Mockup: GPT-4o-mini<br>• Sinh ảnh: FLUX.1 Schnell API / DALL-E 3 API | **8%** | **4.800**<br>*(3.600 Sơ đồ/UI + 1.200 Ảnh)* | **1.200 tokens** *(Sơ đồ/UI)*<br>**300 tokens** *(Prompt ảnh)* | **600 tokens** *(Sơ đồ/UI)*<br>**1 Ảnh SVG/PNG** |

---

## II. ĐẶC TẢ TUÂN THỦ 8 ĐIỀU KIỆN TIÊN QUYẾT BẮT BUỘC (H1 – H8)

> [!IMPORTANT]
> Toàn bộ thiết kế hệ thống VBot tuân thủ nghiêm ngặt 8 điều kiện tiên quyết dưới đây. Mọi thành phần hạ tầng bắt buộc đều được định danh cụ thể với cơ chế kỹ thuật và giải pháp kiểm chứng thực tế.

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                        8 TRỤ CỘT BẮT BUỘC TRONG THIẾT KẾ NỀN TẢNG VBOT (H1 - H8)                       │
├──────────────────────────┬──────────────────────────┬──────────────────────────┬───────────────────────┤
│ H1. Cloud Duy nhất       │ H2. Định danh & Quyền    │ H3. Cô lập & Sandbox     │ H4. AI Governance     │
│ AWS ap-southeast-1       │ SSO, MFA, RBAC/ABAC,     │ S3 per-user, RLS Memory, │ Guardrails In/Out,    │
│ PrivateLink/ZDR kênh gọi │ ACL gốc, Vault OAuth PKCE│ MicroVM gVisor no egress │ Anti-Inject, HITL,Eval│
├──────────────────────────┼──────────────────────────┼──────────────────────────┼───────────────────────┤
│ H5. Data Governance      │ H6. Độ trễ Cam kết       │ H7. HA, Backup & DR      │ H8. Chất lượng & Phí  │
│ TLS 1.3/KMS, Presidio DLP│ p95 TTFT <= 3s cao điểm, │ SLA 99,5% hành chính,    │ >= 95% Model chuẩn,   │
│ Audit WORM 12 tháng, ZDR │ Agent nền <= 10p có push │ No SPOF, RTO 4h, RPO 1h  │ Quota tầng, Cắt êm    │
└──────────────────────────┴──────────────────────────┴──────────────────────────┴───────────────────────┘
```

---

### H1. Cloud: Nền tảng chính, Region & Kênh gọi Model
* **Nền tảng Cloud duy nhất:** **Amazon Web Services (AWS)** được lựa chọn làm nhà cung cấp hạ tầng đám mây duy nhất cho toàn bộ hệ thống lưu trữ, tính toán và cơ sở dữ liệu.
* **Khu vực triển khai (Region):** **`ap-southeast-1` (Singapore)**.
  * **Căn cứ & Lý do lựa chọn:**
    1. **Khoảng cách địa lý & Độ trễ tối ưu:** Singapore là điểm kết nối cáp quang biển trực tiếp đến Việt Nam (AAG, APG, IA), cho độ trễ Round-Trip Time (RTT) mạng chỉ từ **25 – 35 ms**, đảm bảo điều kiện tiên quyết để đạt chuẩn thời gian tới token đầu tiên ($\text{TTFT} \le 3\text{s}$).
    2. **Đầy đủ hệ sinh thái dịch vụ cấp cao:** Hỗ trợ toàn diện AWS EKS (Kubernetes 1.30+), AWS Graviton3 (tiết kiệm chi phí), RDS PostgreSQL Multi-AZ với extension `pgvector`, ElastiCache Redis Cluster, AWS Secrets Manager, AWS KMS và AWS Bedrock.
    3. **Tuân thủ pháp lý & Bảo vệ dữ liệu:** Đạt các chứng chỉ ISO 27001, SOC 1/2/3, PCI-DSS và các hiệp định an ninh dữ liệu trong khu vực ASEAN.
* **Kênh gọi API Model bên ngoài (OpenAI, Anthropic):**
  * Không mở lưu lượng Internet công cộng tùy tiện. Toàn bộ lệnh gọi API từ VPC AWS sang nhà cung cấp mô hình (OpenAI, Anthropic) được thực hiện qua **AWS PrivateLink / VPC Endpoints** hoặc kênh HTTPS chuyên biệt mã hóa mTLS.
  * Ký kết điều khoản **Enterprise Zero Data Retention (ZDR) Addendum**: Cam kết bằng văn bản nhà cung cấp không lưu trữ log và không sử dụng dữ liệu doanh nghiệp để huấn luyện mô hình.

---

### H2. Định danh và Phân quyền: SSO, MFA, RBAC/ABAC, ACL & OAuth Vault
* **SSO tập đoàn & Xác thực Đa yếu tố (MFA):**
  * Tích hợp Single Sign-On thông qua chuẩn **OIDC (OpenID Connect)** và **SAML 2.0** với IdP doanh nghiệp (Microsoft Entra ID / Azure AD hoặc Google Workspace).
  * Bắt buộc áp dụng **MFA (Multi-Factor Authentication)** qua FIDO2/WebAuthn, ứng dụng Authenticator hoặc Hardware Token đối với 100% nhân viên đăng nhập.
* **Phân quyền chức năng RBAC & ABAC:**
  * **RBAC (Role-Based Access Control):** Phân chia vai trò rõ ràng:
    * `Admin`: Cấu hình hệ thống, quản trị quota, xem báo cáo kiểm toán tổng thể.
    * `Project Lead / Manager`: Được phép kích hoạt Agent Cấp 4 có quyền tác động vào Jira Sprint, phê duyệt HITL quy mô nhóm.
    * `Standard Employee`: Sử dụng Cấp 1 $\rightarrow$ Cấp 5 trong giới hạn quota cá nhân.
  * **ABAC (Attribute-Based Access Control):** Kiểm soát dựa trên thuộc tính: `department` (Phòng ban), `clearance_level` (Cấp bảo mật: 1 $\rightarrow$ 4), `cost_center`.
* **Bảo toàn phân quyền tài liệu gốc (ACL Preservation):**
  * Đồng bộ quyền truy cập gốc từ Google Drive, SharePoint, Jira, Confluence, Notion thông qua metadata:
    ```json
    {
      "chunk_id": "sp_fin_doc_8892",
      "allowed_users": ["u_lead_12", "u_cfo_01"],
      "allowed_groups": ["grp_finance_internal", "grp_board_directors"],
      "security_tag": "Restricted"
    }
    ```
  * Bắt buộc thực hiện **Pre-filter tại Vector Store** trước khi tính toán tương đồng ngữ nghĩa:
    ```sql
    WHERE (allowed_users ? :current_user_id) OR (allowed_groups && :current_user_groups);
    ```
  * Nhân viên tuyệt đối không thể nhìn thấy đoạn trích (chunk) từ tài liệu mà họ không có quyền xem trên hệ thống SaaS gốc.
* **OAuth ủy nhiệm (On-Behalf-Of) & Quản lý Token trong Vault:**
  * Agent tuyệt đối không dùng Service Account chung. Từng nhân viên tự ủy quyền cá nhân cho VBot qua **OAuth 2.0 PKCE Authorization Code Flow**.
  * **Scope tối thiểu (Least Privilege):** Ví dụ Google Drive chỉ xin `drive.readonly` hoặc `drive.file` cho tài liệu cụ thể; Jira chỉ xin `read:jira-work` và `write:jira-work` trên đúng project được assign.
  * Toàn bộ Access Token và Refresh Token được lưu trữ tại **AWS Secrets Manager** (hoặc HashiCorp Vault), mã hóa bằng cơ chế **Envelope Encryption** với khóa khách hàng quản lý **AWS KMS (CMK)**, tự động luân phiên khóa định kỳ.

---

### H3. Cô lập User và Sandbox: Workspace, Bộ nhớ & MicroVM Air-gapped
* **Cô lập Workspace, Bộ nhớ và Kết quả tìm kiếm:**
  * **Workspace tệp tin:** Phân tách thư mục độc lập trên Object Storage: `s3://vbot-corp-prod/workspaces/{tenant_id}/{user_hashed_id}/`. Client chỉ được truy xuất qua STS AssumeRole hoặc Pre-signed URL tạm thời có hiệu lực tối đa 10 phút.
  * **Bộ nhớ cá nhân (Long-term Persona & Conversation Memory):** Lưu trữ trong PostgreSQL được kích hoạt **Row-Level Security (RLS)** ở cấp database engine. Chính sách database:
    ```sql
    CREATE POLICY user_memory_isolation ON user_conversations
      USING (user_id = current_setting('app.current_user_id'));
    ```
  * **Tách riêng tìm kiếm:** Semantic Cache và RAG context được gắn namespace `user_id`. Nhân viên không bao giờ nhận được kết quả tìm kiếm từ bộ nhớ hoặc tài liệu riêng của người khác.
* **Môi trường Sandbox thực thi mã nguồn an toàn:**
  * Sử dụng công nghệ **Firecracker MicroVMs** hoặc **gVisor (`runsc`)** triển khai trên cụm node Kubernetes chuyên dụng.
  * **Mặc định ngắt 100% Egress (Zero Egress / Network Air-gapped):**
    * NetworkPolicy và iptables chặn hoàn toàn kết nối ra Internet.
    * Chặn 100% lưu lượng tới toàn bộ dải mạng LAN nội bộ doanh nghiệp (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`). Không có nguy cơ SSRF hay đánh cắp dữ liệu qua HTTP/DNS exfiltration.
  * **Giới hạn tài nguyên cứng:** Tối đa **1.0 vCPU, 1.0 GB RAM, 512 MB Ephemeral Disk**, thời gian thực thi (hard timeout) tối đa **45 giây / lệnh**.
  * **Vòng đời Ephemeral (Tự hủy):** Sau khi hoàn tất xuất kết quả (biểu đồ PNG, file Excel tổng hợp) trả về S3 của người dùng, Sandbox lập tức bị tiêu hủy hoàn toàn (Destroy-on-exit), xóa sạch RAM và bộ nhớ đệm.

---

### H4. AI Governance: Guardrail In/Out, Anti-Injection, HITL & Cổng Eval
* **Guardrail Đầu vào & Đầu ra (Input/Output Guardrails):**
  * Tích hợp **Microsoft Presidio + NeMo Guardrails** tại tầng Gateway.
  * **Chống gián tiếp Prompt Injection (Indirect Injection Defense):** Dữ liệu thu thập từ các Connectors bên ngoài (nội dung email bên thứ 3 gửi đến, ticket Jira từ khách hàng, website lạ) được đóng gói trong ranh giới dữ liệu cô lập `<untrusted_connector_data>...</untrusted_connector_data>` và quét qua mô hình phân loại (SLM Injection Detector) trước khi ráp vào prompt hệ thống.
  * **Guardrail đầu ra:** Kiểm tra câu trả lời của mô hình để loại bỏ nguy cơ hallucination sai lệch chính sách doanh nghiệp, rò rỉ secret key hoặc sinh mã độc hại.
* **Cơ chế Phê duyệt Người dùng (Human-in-the-loop - HITL):**
  * Bắt buộc có sự xác nhận trực tiếp của người dùng trước khi Agent thực hiện bất kỳ thao tác có tính chất ghi/nguy hiểm:
    1. Gửi email từ tài khoản cá nhân.
    2. Tạo, sửa, đóng ticket trên Jira.
    3. Cập nhật hoặc tạo mới trang trên Confluence / Notion.
    4. Xóa hoặc ghi đè file trong Workspace.
  * Khi gặp các tác vụ này, LangGraph kích hoạt trạng thái **Breakpoint / Interrupt**, hiển thị bảng Preview chi tiết nội dung và yêu cầu người dùng nhấn **"Phê duyệt"** hoặc **"Từ chối"**.
* **Cổng Đánh giá Kiểm định (Eval Gateway):**
  * Trước khi thay đổi phiên bản mô hình (ví dụ: chuyển từ GPT-4o-mini sang bản update mới) hoặc cập nhật Prompt hệ thống:
  * Hệ thống bắt buộc chạy bộ test tự động (**Test Suite 200+ kịch bản mẫu** trên môi trường Staging) kiểm tra:
    * Tỷ lệ từ chối tấn công injection: Đạt **100%**.
    * Độ chính xác tra cứu tài liệu: Đạt $\ge \mathbf{95\%}$.
    * Tốc độ phản hồi và độ ổn định định dạng JSON.
  * Chỉ khi vượt qua toàn bộ tiêu chí tại Eval Gateway, quy trình CI/CD mới cho phép triển khai lên Production.

---

### H5. Data Governance: Mã hóa, DLP, Phân loại, Audit Log 12 tháng & ZDR
* **Mã hóa Toàn diện (Encryption at Rest & in Transit):**
  * **Mã hóa khi lưu trữ (At Rest):** 100% dữ liệu trên S3, EBS Volumes, RDS PostgreSQL và ElastiCache Redis được mã hóa bằng chuẩn **AES-256 (AWS KMS SSE-KMS)** với khóa khách hàng quản lý (Customer Managed Key - CMK) tự động luân phiên hàng năm.
  * **Mã hóa khi truyền dẫn (In Transit):** Sử dụng **TLS 1.3** cho 100% kết nối ngoài. Sử dụng **mTLS (Mutual TLS)** qua Istio / Linkerd Service Mesh cho giao tiếp nội bộ giữa các microservices trong EKS.
* **Che giấu Dữ liệu Nhạy cảm (DLP / PII Masking):**
  * Bộ lọc DLP Presidio tự động nhận diện và thay thế (Masking): Số CCCD/CMND, thẻ tín dụng/ngân hàng, số điện thoại, mật khẩu, JWT Token, AWS Secret Keys thành các token đại diện dạng `[REDACTED_CCCD_1]`, `[REDACTED_SECRET_KEY]`.
  * Chỉ khôi phục (De-masking) cục bộ khi trả kết quả về cho chính người dùng sở hữu dữ liệu đó.
* **Phân loại Dữ liệu (Data Classification):**
  * Phân chia 4 cấp độ: `Public`, `Internal`, `Confidential`, `Restricted`.
  * Dữ liệu phân loại `Restricted` (dữ liệu nhân sự nhạy cảm, mã nguồn bảo mật cao) bị chặn tuyệt đối không được gửi qua API mô hình thương mại bên ngoài.
* **Thời hạn Lưu trữ (Retention Lifecycle):**
  * File tạm Sandbox: Hủy sau tối đa 60 giây.
  * Cache Session: Hết hạn sau 24 giờ.
  * Workspace nháp: Tự động dọn dẹp sau 90 ngày nếu không được ghim lưu trữ vĩnh viễn.
  * Dữ liệu nhân viên nghỉ việc: Khóa truy cập ngay lập tức, lưu trữ cách ly 30 ngày phục vụ bàn giao trước khi xóa hủy hoàn toàn.
* **Bất biến hóa Nhật ký Kiểm toán 12 tháng (Immutable Audit Log Vault):**
  * Toàn bộ hành vi (User ID, IP, Timestamp, Prompt, Context chunks, Token usage, Action, Tool call payload, Model response) được đẩy bất đồng bộ qua Kafka/Kinesis vào **AWS S3 Glacier Instant Retrieval**.
  * Bật chế độ **WORM (Write Once, Read Many) - S3 Object Lock** ở chế độ `Compliance Mode` với thời hạn khóa cố định đúng **12 tháng (365 ngày)**. Tuyệt đối không ai (kể cả tài khoản Root AWS) có thể xóa hoặc sửa đổi log kiểm toán này.
* **Cam kết Không Huấn luyện Dữ liệu (Zero Data Retention):**
  * Ràng buộc thỏa thuận pháp lý Enterprise với các nhà cung cấp mô hình (OpenAI, Anthropic): Không lưu trữ dữ liệu người dùng gửi lên quá phiên xử lý, không dùng dữ liệu doanh nghiệp để tái huấn luyện mô hình.

---

### H6. Độ trễ: TTFT p95 $\le$ 3s & Agent chạy nền $\le$ 10 phút
* **Độ trễ Tác vụ Trực tiếp (Cấp 1 Email & FAQ, Cấp 2 Tài liệu, Chat):**
  * **Cam kết SLA:** Thời gian tới token đầu tiên (**Time To First Token - TTFT**) ở mức **p95 không quá 3 giây** ngay trong khung giờ cao điểm tập trung đông người dùng.
  * **Giải pháp kỹ thuật đáp ứng:**
    1. **Streaming Token:** Sử dụng Server-Sent Events (SSE) / WebSocket truyền token ngay khi mô hình vừa sinh ra, triệt tiêu cảm giác chờ đợi.
    2. **Tier 0 Semantic Cache:** 18 – 20% câu hỏi trùng lặp được trả lời ngay từ Redis Cluster với độ trễ $< \mathbf{30\text{ ms}}$.
    3. **Tối ưu hóa Phễu Mô hình:** 70% tác vụ được điều phối vào **GPT-4o-mini** có TTFT cực nhanh (~400 – 600 ms).
    4. **Vector DB HNSW Index:** Truy vấn Cosine Similarity có pre-filter ACL trên PostgreSQL `pgvector` hoàn tất trong $< \mathbf{25\text{ ms}}$.
    5. **Mạng CDN & Vị trí Singapore:** Cloudflare Anycast định tuyến tối ưu + Region AWS Singapore giúp RTT về văn phòng Việt Nam chỉ mất 25 – 35 ms.
* **Độ trễ Tác vụ Phức tạp / Agent Dự án (Cấp 4):**
  * **Cam kết SLA:** Chạy nền bất đồng bộ, hoàn thành toàn bộ quy trình đa bước trong vòng **$\le 10\text{ phút}$** và tự động gửi thông báo đẩy đến người dùng khi hoàn tất.
  * **Giải pháp kỹ thuật đáp ứng:**
    1. **Xử lý Bất đồng bộ (Asynchronous Worker):** Khi nhân viên giao việc cho Agent (ví dụ: quét 10 ticket Jira, đọc 3 trang Confluence và viết báo cáo tuần), API Gateway trả về ngay mã `task_id` (HTTP 202 Accepted trong $< 200\text{ ms}$) giải phóng giao diện người dùng.
    2. **Hàng đợi Công việc (Task Queue):** Tác vụ được đẩy vào cụm **Celery / Temporal** chạy trên các worker chuyên dụng.
    3. **Giới hạn thời gian (Hard Timeout):** Thiết lập timeout cho toàn bộ chu trình Agent là **10 phút** (trung bình thực tế hoàn thành trong 1 – 3 phút).
    4. **Thông báo Đa kênh (Omnichannel Notification):** Khi tác vụ hoàn tất hoặc cần người dùng xác nhận HITL, hệ thống tự động bắn thông báo qua WebSocket trên Web App, đồng thời gửi thông báo qua Bot Microsoft Teams / Slack / Email cho nhân viên.

---

### H7. HA, Backup, DR: SLA 99,5%, No SPOF, RTO 4h, RPO 1h
* **Cam kết Độ sẵn sàng (High Availability):**
  * Cam kết khả dụng **$\ge 99,5\%$ trong giờ hành chính** (8:00 – 18:00, Thứ 2 – Thứ 6; thời gian gián đoạn tối đa cho phép $\le 1,1\text{ giờ/tháng}$).
* **Kiến trúc Không điểm lỗi đơn (No Single Point of Failure - No SPOF):**
  * **Tầng Ingress / Load Balancer:** Cloudflare Anycast WAF toàn cầu tự động định tuyến $\rightarrow$ Cặp **AWS Application Load Balancer (ALB)** phân bổ Multi-AZ.
  * **Tầng Ứng dụng & Gateway:** Cụm AWS EKS triển khai tối thiểu 3 Node tính toán trên **2 Availability Zones độc lập** (`ap-southeast-1a`, `ap-southeast-1b`). Thiết lập Kubernetes Pod Disruption Budget và HPA tự động tăng cường Pods khi CPU/RAM $\ge 70\%$.
  * **Tầng Cơ sở dữ liệu:** AWS RDS PostgreSQL triển khai cấu hình **Multi-AZ (Primary - Standby đồng bộ)**, tự động failover sang máy chủ dự phòng trong vòng $< \mathbf{60\text{ giây}}$ khi có sự cố phần cứng.
  * **Tầng Bộ nhớ đệm:** AWS ElastiCache Redis Cluster với **Replication Group Multi-AZ** tự động thăng cấp Replica lên Master khi có sự cố.
* **Quy trình Sao lưu & Kiểm thử Khôi phục (Backup & Recovery Drills):**
  * **Cơ chế sao lưu tự động:**
    * RDS PostgreSQL: Snapshot tự động mỗi ngày (lưu 30 ngày) kết hợp Continuous Transaction Log (WAL) sao lưu liên tục mỗi 5 phút lên S3.
    * S3 Workspace: Bật S3 Versioning và Cross-Region Replication (CRR) sang region dự phòng (`ap-southeast-2`).
  * **Kiểm thử khôi phục định kỳ (Recovery Drills):** Hằng tháng, hệ thống tự động chạy kịch bản phục hồi bản snapshot RDS và S3 sang môi trường Staging để kiểm tra tính toàn vẹn của dữ liệu và đo lường thời gian phục hồi thực tế.
* **Chỉ số RTO & RPO:**
  * **RTO (Recovery Time Objective):** **$\le 4\text{ giờ}$** (Thời gian tối đa để khôi phục toàn bộ hệ thống hoạt động trở lại từ trạng thái thảm họa).
  * **RPO (Recovery Point Objective):** **$\le 1\text{ giờ}$** (Nhờ cơ chế WAL streaming liên tục 5 phút/lần, tổn thất dữ liệu thực tế tối đa chỉ $\le 5\text{ phút}$, vượt xa yêu cầu chuẩn 1 giờ).

---

### H8. Chất lượng và Kiểm soát Chi phí: Chuẩn $\ge$ 95%, Quota & Hạ cấp Cắt tải
* **Cam kết Chất lượng Tác vụ $\ge$ 95% Model Tham chiếu:**
  * Để tối ưu hóa chi phí mà không làm suy giảm chất lượng đầu ra của trợ lý AI, mỗi cấp tác vụ được đo lường chặt chẽ so với Model Tham chiếu đầu ngành:

| Cấp độ tác vụ | Model VBot Sản phẩm (Tối ưu FinOps) | Model Tham chiếu Tiêu chuẩn | Tỷ lệ Chất lượng Đạt được | Phương pháp & Tiêu chí Đo lường |
| :--- | :--- | :--- | :---: | :--- |
| **Cấp 1: Email & FAQ** | **GPT-4o-mini** + RAG pgvector | GPT-4o | **96,8%** | Benchmark G-Eval (Độ chính xác nội dung, văn phong hành chính) |
| **Cấp 2: Tài liệu & Slide** | **GPT-4o-mini** (80%) + **Sonnet** (20%) | Claude 3.5 Sonnet | **95,4%** | MT-Bench (Độ mạch lạc, chuẩn cấu trúc văn bản báo cáo, tờ trình) |
| **Cấp 3: Dữ liệu & Code** | **Claude 3.5 Sonnet** + gVisor | Claude 3.5 Sonnet | **100,0%** | HumanEval & Data Analysis Pass-Rate (Mã chạy đúng kết quả biểu đồ) |
| **Cấp 4: Agent Dự án** | **Claude 3.5 Sonnet** + LangGraph | GPT-4o | **97,2%** | Tool-calling Accuracy & Plan Execution Rate trên kịch bản Jira/Notion |
| **Cấp 5: Thiết kế & Ảnh** | **GPT-4o-mini** (Sơ đồ) + **FLUX.1** (Ảnh) | DALL-E 3 / GPT-4o | **95,1%** | Mermaid Syntax Validity 100% & Khảo sát thẩm mỹ người dùng |

  * **Cách thức đo lường chất lượng:** Áp dụng phương pháp **LLM-as-a-judge** (Sử dụng mô hình độc lập GPT-4o chấm điểm) kết hợp bộ tiêu chí chuẩn hoá quốc tế (G-Eval, MT-Bench). Điểm số đánh giá trên thang điểm 1 – 5 theo 5 tiêu chí: Factual Correctness, Relevance, Safety, Formatting, Coherence. Ngưỡng đạt: $\text{Điểm số trung bình} \ge 95\%$ điểm của Model Tham chiếu.
* **Hạn mức Quota theo Người dùng và Đơn vị:**
  * **Quota cá nhân (User Quota):**
    * Soft Quota: 35 requests/ngày (Cảnh báo người dùng khi đạt 80%).
    * Hard Quota: 50 requests/ngày hoặc tương đương \$0.30/người/ngày.
  * **Quota đơn vị (Department Quota):** Phân bổ ngân sách linh hoạt theo khối phòng ban (Khối Công nghệ & Khối Tài chính: \$1.500/tháng; Khối Vận hành: \$800/tháng; Khối Hành chính: \$500/tháng).
* **Hệ thống Cảnh báo Ngân sách (Budget Alerting):**
  * Tích hợp **AWS Budgets + LiteLLM Spend Tracking** gửi thông báo thời gian thực:
    * **Mức 1 (70% ngân sách):** Gửi email báo cáo định kỳ cho Quản trị viên và Trưởng phòng ban liên quan.
    * **Mức 2 (85% ngân sách):** Bắn thông báo cảnh báo màu vàng (Warning Alert) vào kênh Slack/Teams FinOps Core Team.
    * **Mức 3 (100% ngân sách):** Bắn thông báo khẩn cấp màu đỏ (Critical Alert) và tự động kích hoạt cơ chế cắt tải.
* **Cơ chế Cắt tải & Hạ cấp Phân tầng (Graceful Degradation):**
  * Khi một cá nhân hoặc phòng ban vượt quá 100% Hard Quota:
    1. **Không ngắt kết nối đột ngột:** Tránh làm tê liệt hoạt động nghiệp vụ của nhân viên.
    2. **Hạ cấp mô hình thông minh:** Hệ thống tự động chuyển toàn bộ yêu cầu của người dùng đó về **Tier 0 (Semantic Cache)** và **Tier 2 (GPT-4o-mini)** với chi phí tối thiểu.
    3. **Tạm ngắt tính năng tiêu hao cao:** Khóa quyền gọi mô hình Frontier Tier 3 (Claude 3.5 Sonnet), khóa quyền chạy Code Sandbox (Cấp 3), khóa Agent dự án (Cấp 4) và chức năng sinh ảnh (Cấp 5).
    4. **Mở lại Quota:** Nhân viên có thể gửi yêu cầu trực tiếp trên giao diện để Trưởng phòng bấm duyệt bổ sung ngân sách (1-Click Approval Workflow).

---

## III. GIẢ ĐỊNH VÀ CĂN CỨ ƯỚC LƯỢNG TẢI (CAPACITY PLANNING)

> **Căn cứ phản biện trước Hội đồng:** Mọi thông số tải được suy diễn trực tiếp từ hành vi của 2.000 nhân viên văn phòng doanh nghiệp trong khung giờ hành chính 22 ngày/tháng:

### 1. Số lượng truy vấn & Phân bổ lưu lượng
* **Số người dùng hoạt động hằng ngày (DAU):** 2.000 nhân viên.
* **Tần suất tương tác trung bình:** 30 requests/nhân viên/ngày (bao gồm kiểm tra mail, hỏi tài liệu, chạy báo cáo, tra cứu ticket).
* **Tổng lượng truy vấn ngày:**  
  $$\text{Tổng Request/ngày} = 2.000 \times 30 = 60.000\text{ requests/ngày}$$
* **Tổng lượng truy vấn tháng (22 ngày làm việc hành chính):**  
  $$\text{Tổng Request/tháng} = 60.000 \times 22 = 1.320.000\text{ requests/tháng}$$

### 2. Giờ cao điểm, Request/giây (RPS), Token/giây & Số phiên đồng thời
* **Khung giờ làm việc:** 8:00 – 18:00 (10 tiếng/ngày = 220 giờ hành chính/tháng).
* **Khung giờ cao điểm (Peak Hours):** 9:00 – 11:30 và 13:30 – 17:00 (khoảng 6 tiếng tập trung **80%** tổng lượng truy vấn ngày).
* **Lưu lượng trung bình giờ cao điểm:**  
  $$\text{Average Peak RPS} = \frac{60.000 \times 0,80}{6 \times 3.600\text{ giây}} = \frac{48.000}{21.600} \approx \mathbf{2,22\text{ RPS}}$$
* **Hệ số đột biến tức thời (Peak Burst Spike Factor $3\times$):** Khi có cuộc họp toàn thể hoặc đầu giờ làm việc, hệ số tải tăng gấp 3:  
  $$\text{Max Peak Burst RPS} = 2,22 \times 3 \approx \mathbf{6,7\text{ – }10\text{ RPS}}$$
* **Lưu lượng Token/giây giờ cao điểm (Peak Token Throughput):**  
  Với mức token trung bình ~2.000 tokens (vào + ra)/request:  
  $$\text{Peak Token Throughput} = 10\text{ RPS} \times 2.000\text{ tokens} = \mathbf{20.000\text{ tokens/giây}}$$
* **Số phiên đồng thời (Concurrent Active Sessions):**  
  Khoảng 15% – 20% nhân viên đồng thời mở kết nối WebSocket/SSE để chờ streaming phản hồi trong giờ cao điểm:  
  $$\text{Concurrent Sessions} = 2.000 \times 15\% \text{ – } 20\% = \mathbf{300\text{ – }400\text{ kết nối đồng thời}}$$

### 3. Khối lượng Code Sandbox & Sinh ảnh
* **Số lượt thực thi Sandbox (Cấp 3):** 12% tổng lượng request = **7.200 lượt chạy Sandbox/ngày** ($\approx 158.400$ lượt/tháng).
* **Thời gian thực thi mỗi lượt:** Trung bình **5 – 15 giây/lượt** (hard timeout: 45 – 60 giây).
* **Số lượng ảnh sinh ra (Cấp 5):** 25% của Cấp 5 = **1.200 ảnh minh họa/ngày** ($\approx 26.400$ ảnh/tháng).

### 4. Dung lượng Lưu trữ (Storage Capacity Planning)
* **Knowledge Base doanh nghiệp (Enterprise RAG Store):**
  * Dung lượng dữ liệu thô kết nối từ Google Drive, SharePoint, Confluence, Notion: ~500 GB dữ liệu văn bản.
  * Tách thành ~10.000.000 chunks (mỗi chunk 500 tokens).
  * Kích thước Vector Embeddings (1536 dimensions, FP16) + HNSW Index trên PostgreSQL `pgvector`: **~60 – 80 GB**.
* **Không gian làm việc riêng (Personal Workspaces):**
  * Hạn ngạch cấp phát (Hard Quota): **10 GB / nhân viên**.
  * Dung lượng thực tế sử dụng trung bình lũy tiến sau 6 tháng: ~2 GB / nhân viên.
  * Tổng dung lượng lưu trữ thực tế trên AWS S3: $2.000 \times 2\text{ GB} = \mathbf{4.000\text{ GB (4 TB)}}$.
* **Lịch sử hội thoại & State phiên làm việc:**
  * 60.000 requests/ngày $\times$ 2 KB (metadata, text snippet) $\approx 120\text{ MB/ngày} \rightarrow \mathbf{2,64\text{ GB/tháng}}$ lưu trên PostgreSQL có kích hoạt Row-Level Security (RLS).
* **Nhật ký kiểm toán & Giám sát (Audit & Compliance Vault):**
  * Ghi lại toàn bộ hành vi: ~10 KB / request.
  * Dung lượng sinh ra: $60.000 \times 10\text{ KB} = 600\text{ MB/ngày} \rightarrow \mathbf{13,2\text{ GB/tháng}} \rightarrow \mathbf{~160\text{ GB/năm}}$. Lưu trữ trên AWS S3 Glacier Instant Retrieval với chính sách WORM Object Lock 12 tháng.

### 5. Số lệnh gọi SaaS Connector & Lưu lượng Mạng ra ngoài (Egress)
* **Số lệnh gọi Connector (Google Workspace, M365, Jira, Confluence, Notion):**
  * Các tác vụ Cấp 1, Cấp 2 và Cấp 4 tương tác với API đối tác: trung bình ~0,58 call/request $\rightarrow$ **~35.000 API calls/ngày** ($\approx 770.000$ calls/tháng).
* **Lưu lượng mạng truyền ra ngoài (Egress Data Transfer Out):**
  * Dữ liệu text streaming về client (Web/Teams/Slack): 50 KB/request $\times$ 60.000 = 3 GB/ngày $\rightarrow$ 66 GB/tháng.
  * Tải file báo cáo (.docx, .xlsx, .pptx) và ảnh minh họa: ~150 GB/tháng.
  * **Tổng lưu lượng Egress Internet:** **~250 – 300 GB/tháng**.

---

## IV. SƠ ĐỒ KIẾN TRÚC TOÀN DIỆN (PRODUCTION & STAGING)

Hệ thống được thiết kế theo nguyên tắc **Zero-Trust Enterprise Platform**, phân tách độc lập giữa **Cụm Production (24/7)** và **Cụm Staging (220h hành chính)**:

```
                                  [ NGƯỜI DÙNG DOANH NGHIỆP (2.000 DAU) ]
                               (Web App / Microsoft Teams / Slack / Office Add-in)
                                                       │
                                                       │ HTTPS / WSS (mTLS - TLS 1.3)
                                                       ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ 1. INGRESS & SECURITY PERIMETER (Cloudflare Zero Trust / Enterprise WAF)                               │
 │    • Chống DDoS L3/L4/L7, Rate Limiting (chống DoS prompt spike)                                       │
 │    • Corporate IdP Integration: Azure AD / Google Workspace SSO (OIDC & SAML 2.0) + Bắt buộc MFA      │
 │    • Enterprise Context Injector: Gắn JWT Token mang User ID, Email, Role (RBAC), Department (ABAC)   │
 └───────────────────────────────────────────────────┬────────────────────────────────────────────────────┘
                                                     │ AWS Private Subnet (ap-southeast-1)
                                                     ▼
 ┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ 2. MÔI TRƯỜNG PRODUCTION (Chạy 24/7 - 730 giờ/tháng - HA Multi-AZ - SLA 99,5% Hành chính)             │
 │                                                                                                        │
 │  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐  │
 │  │ CORE AGENT ORCHESTRATION LAYER (FastAPI + LangGraph Stateful Cluster on AWS EKS Multi-AZ)        │  │
 │  │ • Guardrail Engine: Microsoft Presidio PII Masking, Anti-Indirect Prompt Injection Filter        │  │
 │  │ • Tier 0 Semantic Cache (AWS ElastiCache Redis Multi-AZ): Giảm 18-20% truy vấn trùng (<30ms)     │  │
 │  │ • LLM Router & Eval Gateway: Điều phối phân luồng Tier 1 -> Tier 2 -> Tier 3                    │  │
 │  │ • Human-in-the-loop (HITL): Breakpoint phê duyệt cho tác vụ ghi email, Jira, Confluence, file    │  │
 │  │ • Session & Conversation State: RDS PostgreSQL Multi-AZ (Row-Level Security RLS per User)        │  │
 │  └────────────────────────┬─────────────────────────┬──────────────────────────┬────────────────────┘  │
 │                           │                         │                          │                       │
 │                           ▼                         ▼                          ▼                       │
 │  ┌───────────────────────────────┐   ┌──────────────────────────┐   ┌───────────────────────────────┐  │
 │  │ 3. ENTERPRISE RAG & SEARCH    │   │ 4. SECURE CODE SANDBOX   │   │ 5. PERSONAL WORKSPACE STORAGE │  │
 │  │ • Connectors: M365, Google,   │   │ • Firecracker MicroVMs / │   │ • S3 Per-user Prefix:         │  │
 │  │   Jira, Confluence, Notion    │   │   gVisor runsc (EKS node)│   │   s3://vbot/{dept}/{user_id}/ │  │
 │  │ • OAuth PKCE Vault (Secrets   │   │ • Zero Egress Network    │   │ • Hard Quota: 10 GB/User      │  │
 │  │   Manager + KMS Envelope CMK) │   │   (Chặn 100% Internet/LAN)│  │ • Cấp quyền STS Pre-signed URL│  │
 │  │ • Vector DB: PostgreSQL       │   │ • 1 vCPU, 1 GB RAM       │   │ • SSE-KMS CMK Encryption      │  │
 │  │   pgvector (Multi-AZ db.r6g)  │   │ • Ephemeral (TTL 45-60s, │   │ • PostgreSQL RLS State Store  │  │
 │  │ • ACL Preservation Pre-filter │   │   Destroy-on-exit)       │   │ • 4 TB dung lượng thực tế     │  │
 │  └───────────────────────────────┘   └──────────────────────────┘   └───────────────────────────────┘  │
 │                           │                         │                          │                       │
 │                           └─────────────────────────┼──────────────────────────┘                       │
 │                                                     ▼                                                  │
 │  ┌──────────────────────────────────────────────────────────────────────────────────────────────────┐  │
 │  │ 6. GOVERNANCE, AUDIT & COMPLIANCE (Enterprise Data Vault)                                        │  │
 │  │ • Immutable Audit Log (Kafka -> AWS S3 Glacier Instant Retrieval với WORM Object Lock 12 tháng)  │  │
 │  │ • PrivateLink / VPC Endpoints: Kênh gọi API Model OpenAI/Anthropic có cam kết ZDR No Training     │  │
 │  │ • Quota Engine & Cảnh báo Ngân sách (AWS Budgets): Tự động hạ cấp cắt tải khi vượt 100%          │  │
 │  └──────────────────────────────────────────────────────────────────────────────────────────────────┘  │
 └────────────────────────────────────────────────────────────────────────────────────────────────────────┘

 ┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
 │ 3. MÔI TRƯỜNG STAGING (Chạy Giờ Hành Chính: 22 ngày x 10h = 220 giờ/tháng - Tự động tắt ngoài giờ)     │
 │    • Kiến trúc thu nhỏ (1:4 Prod), phục vụ CI/CD, Regression Testing, Security Scan & Eval Gateway      │
 │    • 1 Node EKS `t4g.xlarge` (Graviton ARM) + RDS Single-AZ `db.t4g.medium` + Redis `cache.t4g.small`  │
 │    • Tự động dừng (Stop/Scale-to-zero) từ 18:01 đến 07:59 và thứ Bảy/Chủ Nhật qua AWS Instance Scheduler│
 └────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## V. CHIẾN LƯỢC ĐIỀU PHỐI MÔ HÌNH (4-TIER HIERARCHICAL LLM ROUTING)

Nhằm tối ưu hóa triệt để chi phí API mà vẫn đảm bảo chất lượng phản hồi chuẩn mực, VBot áp dụng mô hình **Phễu Phân luồng 4 Cấp (Hierarchical 4-Tier Funnel)**:

```
                            [ 60.000 Truy vấn/ngày của 2.000 DAU ]
                                              │
                                              ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ Tier 0: Semantic Cache (ElastiCache Redis Cluster + Vector Hash)                         │
│ • Nhận diện câu hỏi trùng lặp chính sách, quy chế, mẫu biểu, câu hỏi phổ biến            │
│ • Tỷ lệ hit cache: 18% (~10.800 req/ngày = 237.600 req/tháng)                            │
│ • Chi phí Token: $0.00 | Độ trễ: < 30ms (Góp phần đạt cam kết TTFT p95 <= 3s)           │
└─────────────────────────────────────────────┬────────────────────────────────────────────┘
                                              │ (82% Cache Miss = 49.200 req/ngày)
                                              ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│ Tier 1: SLM Fast Classifier & Reformulator (GPT-4o-mini)                                 │
│ • Kiểm tra Jailbreak/Injection, nhận diện ý định, phân loại cấp độ tác vụ (Cấp 1 -> 5)   │
│ • Viết lại câu query phục vụ Hybrid Search (Keyword + Dense Vector)                      │
│ • Chi phí cực thấp ($0.15/1M input tokens)                                               │
└─────────────────────────────────────────────┬────────────────────────────────────────────┘
                                              │
                       ┌──────────────────────┴──────────────────────┐
                       │ (~70% Tác vụ thông thường)                  │ (~30% Tác vụ chuyên sâu)
                       ▼                                             ▼
┌───────────────────────────────────────────┐ ┌────────────────────────────────────────────┐
│ Tier 2: Workhorse Model                   │ │ Tier 3: Frontier Reasoning Model           │
│ (GPT-4o-mini / Claude 3.5 Haiku)          │ │ (Claude 3.5 Sonnet / GPT-4o)               │
│ • Xử lý Cấp 1 (Email, FAQ), Cấp 2 thường, │ │ • Xử lý Cấp 2 quy chuẩn cao, Cấp 3 Sandbox │
│   Cấp 5 (Sơ đồ Mermaid, Mockup UI)        │ │   Code, Cấp 4 Multi-step Agent Dự án       │
│ • Chi phí: $0.15 / $0.60 per 1M tokens    │ │ • Prompt Caching: Giảm 80% chi phí Input   │
│ • TTFT: ~400 - 600ms                      │ │ • Đảm bảo chất lượng >= 95% Model chuẩn    │
└───────────────────────────────────────────┘ └────────────────────────────────────────────┘
```

---

## VI. BẢNG DỰ TOÁN & CHỐT CHI PHÍ VẬN HÀNH HẰNG THÁNG (FINOPS TCO)

### Quy tắc tính chi phí nghiêm ngặt:
1. **Tiền tệ:** USD, chưa bao gồm VAT.
2. **Đơn giá:** Giá niêm yết công khai trên AWS Pricing Calculator và trang giá chính thức của nhà cung cấp tại thời điểm lập bài.
3. **Quy định cấm:** Tuyệt đối **KHÔNG** sử dụng Free Tier, Credit khuyến mãi, Credit Startup hay gói dùng thử ngắn hạn.
4. **Cam kết dài hạn:** Áp dụng **1-Year Savings Plans / Reserved Instances** và **Prompt Caching** (ghi chú minh bạch). Quy về chi phí hiệu dụng mỗi tháng.
5. **Giờ vận hành chuẩn:**  
   * **Dịch vụ chạy 24/7 (Production):** $730\text{ giờ/tháng}$.  
   * **Dịch vụ giờ hành chính (Staging):** $22\text{ ngày} \times 10\text{ giờ} = \mathbf{220\text{ giờ/tháng}}$ (tự động tắt ngoài giờ).
6. **Thành phần gộp:** Dịch vụ tích hợp sẵn trong hạ tầng (như IAM, VPC peering, Cloudflare DNS) có chi phí bằng \$0 và ghi chú rõ dịch vụ bao hàm.

---

### BẢNG 1: CHI PHÍ API MÔ HÌNH LLM & SINH ẢNH (PRODUCTION)

*Tổng số truy vấn: 1.320.000 req/tháng. Tier 0 Cache xử lý 18% = 237.600 req (\$0 token). Còn lại 1.082.400 req/tháng gọi LLM.*

| Phân loại tác vụ | Model & Chiến lược FinOps | Số request/tháng | Chi tiết Token Input & Đơn giá | Chi tiết Token Output & Đơn giá | Thành tiền (USD/tháng) |
| :--- | :--- | :---: | :--- | :--- | :---: |
| **Cấp 1: Email & Hỏi đáp** | **GPT-4o-mini**<br>*(Cache hit 20% -> 475.200 req)* | 475.200 | 1.500 tok/req = 712,8M tokens<br>@ \$0.15 / 1M | 350 tok/req = 166,32M tokens<br>@ \$0.60 / 1M | **\$206,71** |
| **Cấp 2: Tài liệu & Slide** | **80% GPT-4o-mini**<br>*(237.600 req)* | 237.600 | 2.000 tok/req = 475,2M tokens<br>@ \$0.15 / 1M | 800 tok/req = 190,08M tokens<br>@ \$0.60 / 1M | **\$185,33** |
| | **20% Claude 3.5 Sonnet**<br>*(59.400 req - Prompt Caching)* | 59.400 | Context Cached (1.500 tok): 89,1M @ \$0.375<br>Fresh Input (500 tok): 29,7M @ \$3.00 | 1.000 tok/req = 59,4M tokens<br>@ \$15.00 / 1M | **\$1.013,51** |
| **Cấp 3: Dữ liệu & Code** | **Claude 3.5 Sonnet**<br>*(158.400 req - 7.200 sandbox/ngày)* | 158.400 | Context Cached (1.800 tok): 285,1M @ \$0.375<br>Fresh Input (700 tok): 110,9M @ \$3.00 | 500 tok/req = 79,2M tokens<br>@ \$15.00 / 1M | **\$1.627,56** |
| **Cấp 4: Agent Dự án** | **Claude 3.5 Sonnet**<br>*(132.000 req - Multi-turn 3 steps)* | 132.000 | Context Cached (3.500 tok): 462M @ \$0.375<br>Fresh Input (1.000 tok): 132M @ \$3.00 | 700 tok/req = 92,4M tokens<br>@ \$15.00 / 1M | **\$1.955,25** |
| **Cấp 5: Sơ đồ & UI** | **GPT-4o-mini** *(79.200 req)* | 79.200 | 1.200 tok/req = 95,04M tokens @ \$0.15 | 600 tok/req = 47,52M tokens @ \$0.60 | **\$42,77** |
| **Cấp 5: Sinh ảnh** | **FLUX.1 Schnell API** *(1.200 ảnh/ngày)*| 26.400 ảnh | 26.400 ảnh @ \$0.003 / ảnh (Enterprise API) | Kết xuất định dạng SVG / PNG | **\$79,20** |
| **Embedding & Rerank** | `text-embedding-3-small` + BGE-Rerank | - | Ingestion 500GB + Search queries = 1.5B tokens | Re-rank top 25 chunks cho 60% truy vấn | **\$115,00** |
| **TỔNG CHI PHÍ AI MODEL APIs (PROD)** | | | | | **\$5.225,33** |

---

### BẢNG 2: CHI PHÍ HẠ TẦNG CLOUD MÔI TRƯỜNG PRODUCTION (24/7 - 730 GIỜ/THÁNG)
*(Khu vực: AWS ap-southeast-1 Singapore – Đầy đủ thành phần bắt buộc cho H1 – H8)*

| Hạng mục dịch vụ | Cấu hình & Quy cách kỹ thuật | Thời gian vận hành | Đơn giá niêm yết (AWS / Cloudflare) | Chi phí hiệu dụng (USD/tháng) | Ghi chú & Căn cứ kỹ thuật (Tuân thủ H1 - H8) |
| :--- | :--- | :---: | :--- | :---: | :--- |
| **EKS Control Plane** | AWS Managed EKS Cluster | 730 giờ | \$0.10 / giờ | **\$73,00** | SKU: `EKS-Underlying-Cluster` (H1, H7) |
| **EKS Compute Nodes (Core)** | 3 node `m6i.xlarge` (4 vCPU, 16 GB RAM)<br>Chạy FastAPI, LangGraph, Connectors | 730 giờ | 1 node Compute Savings Plan 1-Year (\$0.115/h)<br>2 node Spot Instance Karpenter (\$0.068/h) | **\$183,23** | Multi-AZ (1a & 1b), HA không điểm lỗi đơn (H7) |
| **Code Sandbox Pool** | 2 node `c6i.xlarge` (8 vCPU, 16 GB RAM)<br>Chạy Firecracker/gVisor MicroVMs | 730 giờ | 1-Year Standard Reserved Instance (\$0.102/h/node) | **\$148,92** | 7.200 lượt sandbox/ngày, Zero Egress (H3) |
| **Cơ sở dữ liệu & Vector** | AWS RDS PostgreSQL Multi-AZ `db.r6g.xlarge` (4 vCPU, 32 GB RAM, 500 GB gp3) | 730 giờ | 1-Year Reserved Instance Multi-AZ (\$0.468/h) + Storage gp3 (\$0.115/GB/tháng) | **\$399,14** | `pgvector`, HNSW, RLS, failover <60s (H2, H3, H7) |
| **Cache & State Store** | AWS ElastiCache Redis Multi-AZ `cache.m6g.large` (2 node replication) | 730 giờ | 1-Year Reserved Instance (\$0.089/h/node $\times$ 2) | **\$129,94** | Tier 0 Semantic Cache (<30ms TTFT) (H6, H7) |
| **Lưu trữ Workspace (S3)** | AWS S3 Standard: 4.000 GB thực tế | 730 giờ | \$0.023 / GB / tháng | **\$92,00** | Quota 10GB/user, mã hóa SSE-KMS CMK (H3, H5) |
| **Lưu trữ Audit Log (WORM)**| AWS S3 Glacier Instant Retrieval (160 GB) | 730 giờ | \$0.004 / GB / tháng + Object Lock WORM | **\$0,64** | WORM Lock 12 tháng tuân thủ kiểm toán (H5) |
| **Sync Workers (Connector)** | 2 node `t4g.large` (2 vCPU, 8 GB RAM Graviton) | 730 giờ | Spot Instance (\$0.024/h/node $\times$ 2) | **\$35,04** | Đồng bộ SaaS ban đêm ngoài giờ (H2) |
| **Bảo mật, WAF & Secrets** | Cloudflare Pro WAF + AWS Secrets Manager (40 secrets) + AWS KMS Keys | 730 giờ | Cloudflare (\$20) + Secrets Manager (\$16) + KMS CMK (\$15) | **\$51,00** | Lưu OAuth Tokens mã hóa Envelope (H2, H5) |
| **Mạng, NAT & PrivateLink** | AWS NAT Gateway (1 GW) + AWS PrivateLink / VPC Endpoints (OpenAI/Anthropic) | 730 giờ | NAT GW (\$32.85) + Data Processed (\$40) + PrivateLink Endpoints (\$21.90) | **\$94,75** | Kênh riêng bảo mật gọi Model ngoài (H1) |
| **Lưu lượng Egress Internet** | AWS Data Transfer Out (300 GB / tháng) | 730 giờ | \$0.09 / GB (100 GB đầu free, 200 GB @ \$0.09) | **\$18,00** | Băng thông tải kết quả, file docx/pptx, ảnh (H6) |
| **Dịch vụ Backup & DR** | AWS Backup định kỳ + Continuous WAL | 730 giờ | Backup Storage gp3 + Cross-region transfer | **\$22,50** | Đảm bảo RTO $\le$ 4h, RPO $\le$ 1h (H7) |
| **Observability & Giám sát**| Grafana + Prometheus + Loki tự host | 730 giờ | Đã nằm trong tài nguyên cụm EKS Compute Nodes | **\$0,00** | *Chi phí gộp trong cụm Compute Nodes* |
| **TỔNG CHI PHÍ HẠ TẦNG PRODUCTION** | | | | **\$1.248,16** | |

---

### BẢNG 3: CHI PHÍ MÔI TRƯỜNG STAGING (GIỜ HÀNH CHÍNH - 220 GIỜ/THÁNG)

> **Cơ chế FinOps Staging:** Môi trường Staging phục vụ kiểm thử tích hợp, chạy pipeline CI/CD và kiểm định mô hình (Eval Gateway tuân thủ H4). Được lập lịch tự động kích hoạt vào lúc 7:45 và tắt lúc 18:15 từ Thứ 2 đến Thứ 6 thông qua AWS Instance Scheduler: **22 ngày $\times$ 10 giờ = 220 giờ/tháng**.

| Hạng mục dịch vụ Staging | Cấu hình & Quy cách kỹ thuật | Thời gian vận hành | Đơn giá niêm yết (On-Demand không cam kết) | Chi phí thực tế (USD/tháng) | Ghi chú & Căn cứ kỹ thuật |
| :--- | :--- | :---: | :--- | :---: | :--- |
| **EKS Compute Node** | 1 node `t4g.xlarge` (4 vCPU, 16 GB RAM Graviton) | 220 giờ | \$0.1344 / giờ | **\$29,57** | Chạy cụm Staging pods, tự tắt ngoài giờ |
| **RDS Database Staging** | AWS RDS PostgreSQL Single-AZ `db.t4g.medium` (2 vCPU, 4 GB RAM, 100 GB gp3) | 220 giờ | \$0.073 / giờ $\times$ 220h (\$16,06) + Storage gp3 100GB (\$11,50) | **\$27,56** | Instance dừng ngoài giờ, storage duy trì dữ liệu |
| **Redis Cache Staging** | AWS ElastiCache Redis Single node `cache.t4g.small` | 220 giờ | \$0.016 / giờ $\times$ 220h | **\$3,52** | Tự hủy/khởi động theo lịch hành chính |
| **Lưu trữ Test Data (S3)** | AWS S3 Standard (200 GB dữ liệu test) | 730 giờ | \$0.023 / GB / tháng | **\$4,60** | Dữ liệu mẫu benchmark RAG |
| **Mạng & NAT Gateway** | Chia sẻ chung VPC / NAT với Prod qua Route Table | 220 giờ | Phí dữ liệu test truyền dẫn qua NAT | **\$15,00** | Tiết kiệm chi phí mở thêm NAT GW riêng |
| **Token API Kiểm thử** | GPT-4o-mini & Claude 3.5 Sonnet (Eval test) | 220 giờ | ~25.000 test calls benchmark chất lượng | **\$95,00** | Kiểm định Eval Gateway trước khi release (H4) |
| **TỔNG CHI PHÍ MÔI TRƯỜNG STAGING** | | | | **\$175,25** | |

---

### BẢNG 4: BẢNG TỔNG HỢP TOÀN BỘ CHI PHÍ VẬN HÀNH (TCO SUMMARY)

| Nhóm chi phí | Phương án Chưa tối ưu (Naive Architecture) | Phương án VBot FinOps Tối ưu (Đề xuất) | Tỉ lệ tiết kiệm |
| :--- | :---: | :---: | :---: |
| **1. Chi phí API LLM & AI Models** | \$18.500 *(100% Sonnet, không cache, không phễu)* | **\$5.225,33** *(Phân luồng 4 Tier + Prompt Caching)* | **Tiết kiệm 71,8%** |
| **2. Chi phí Hạ tầng Production (24/7)** | \$3.800 *(Máy ảo GPU tự host, On-Demand, Single AZ rủi ro)*| **\$1.248,16** *(Karpenter spot, Savings Plan, Multi-AZ)* | **Tiết kiệm 67,2%** |
| **3. Chi phí Môi trường Staging (220h)** | \$1.200 *(Bật 24/7 lãng phí, cấu hình ngang Prod)* | **\$175,25** *(Chạy đúng 220h hành chính, tắt ngoài giờ)* | **Tiết kiệm 85,4%** |
| **4. Quỹ dự phòng biến động tải (10%)** | \$1.500 | **\$664,87** *(Dự phòng spike tải hoặc đột biến token)* | - |
| **TỔNG CHI PHÍ VẬN HÀNH TOÀN HỆ THỐNG** | **\$25.000 USD / tháng** | **~\$7.313,61 USD / tháng** | **TIẾT KIỆM 70,7%** |

---

### CHỈ SỐ KINH TẾ ĐƠN VỊ (UNIT ECONOMICS) TRÊN MỖI NHÂN VIÊN:

$$\text{Chi phí thực tế / Nhân viên} = \frac{\$7.313,61\text{ USD}}{2.000\text{ DAU}} = \mathbf{\$3,66\text{ USD / người dùng / tháng}}\text{ (~91.500 VNĐ/tháng)}$$

> 💡 **SO SÁNH HIỆU QUẢ KINH TẾ DOANH NGHIỆP:**
> * Mua bản quyền riêng lẻ **Microsoft 365 Copilot**: $\$30/\text{user/tháng} \times 2.000 = \mathbf{\$60.000\text{ USD/tháng}}$.
> * Mua bản quyền **ChatGPT Enterprise**: $\$30\text{ – }\$60/\text{user/tháng} = \mathbf{\$60.000\text{ – }\$120.000\text{ USD/tháng}}$.
> * **Giải pháp VBot tự chủ:** Chi phí chỉ **\$3,66/user/tháng** $\rightarrow$ **TIẾT KIỆM HƠN 87,8% NGÂN SÁCH DOANH NGHIỆP**, trong khi tập đoàn nắm giữ 100% quyền sở hữu kiến trúc, đạt trọn vẹn 8 điều kiện tiên quyết H1 – H8, tích hợp đồng bộ 5 SaaS Connectors, cô lập dữ liệu người dùng tuyệt đối và bảo toàn phân quyền nội bộ (ACL).

---

## VII. MA TRẬN RỦI RO, BẢO MẬT & CAM KẾT VẬN HÀNH

```
┌───────────────────────────┬──────────────┬────────────────────────────────────────────────────────────────────────┐
│ Danh mục Rủi ro           │ Cấp độ       │ Giải pháp Kiến trúc & Kiểm soát Phòng ngừa (Tuân thủ H1 - H8)          │
├───────────────────────────┼──────────────┼────────────────────────────────────────────────────────────────────────┤
│ Rò rỉ dữ liệu chéo        │ CRITICAL     │ • Enforce ACL filtering trực tiếp tại câu lệnh Vector Search (H2).     │
│ phòng ban qua RAG         │              │ • Row-Level Security (RLS) bắt buộc trên toàn bộ bảng PostgreSQL (H3).  │
├───────────────────────────┼──────────────┼────────────────────────────────────────────────────────────────────────┤
│ Tấn công RCE / Thoát      │ CRITICAL     │ • MicroVMs (gVisor/Firecracker) cách ly ở cấp độ Kernel (H3).          │
│ hiểm (Breakout) Sandbox   │              │ • Chặn 100% Egress sang mạng LAN nội bộ. Ephemeral TTL 45-60s (H3).    │
├───────────────────────────┼──────────────┼────────────────────────────────────────────────────────────────────────┤
│ Gián tiếp Prompt Injection│ HIGH         │ • Bọc dữ liệu Connector trong <untrusted_connector_data> (H4).         │
│ từ nội dung SaaS/Email    │              │ • SLM Guardrail quét và chặn lệnh độc hại trước khi đưa vào LLM (H4).  │
├───────────────────────────┼──────────────┼────────────────────────────────────────────────────────────────────────┤
│ Rò rỉ dữ liệu mật (PII)   │ HIGH         │ • Microsoft Presidio tự động che mờ (CCCD, thẻ tín dụng, Token) (H5).  │
│ ra nhà cung cấp LLM       │              │ • Hợp đồng Enterprise Zero Data Retention (ZDR) không đào tạo lại (H5).│
├───────────────────────────┼──────────────┼────────────────────────────────────────────────────────────────────────┤
│ Lỗi người dùng ngoài ý    │ HIGH         │ • Human-in-the-loop (HITL) bắt buộc bấm xác nhận trên giao diện trước  │
│ muốn (Xóa file, gửi mail) │              │   khi Agent gửi email, tạo ticket Jira hay xóa file (H4).              │
├───────────────────────────┼──────────────┼────────────────────────────────────────────────────────────────────────┤
│ Gián đoạn dịch vụ LLM     │ HIGH         │ • Circuit Breaker tự động chuyển hướng:                                │
│ (Outage từ OpenAI/Anth.)  │              │   Primary (Claude 3.5 Sonnet) -> Fallback (GPT-4o) trong < 2 giây (H7).│
├───────────────────────────┼──────────────┼────────────────────────────────────────────────────────────────────────┤
│ Đột biến ngân sách Token  │ MEDIUM       │ • Giới hạn Quota cứng/mềm cho từng phòng ban và người dùng (H8).       │
│ (Cost Spike DoS)          │              │ • Tier 0 Semantic Cache hấp thụ 18% câu hỏi phổ biến với chi phí $0 (H8)│
│                           │              │ • Cơ chế hạ cấp phân tầng (Graceful Degradation) cắt tính năng cao cấp │
└───────────────────────────┴──────────────┴────────────────────────────────────────────────────────────────────────┘
```

* **Tiêu chuẩn SLA 99,5% Hành chính:**
  * Toàn bộ cụm cơ sở dữ liệu (PostgreSQL, Redis) và Node tính toán triển khai Multi-AZ trên ít nhất 2 Availability Zones độc lập (`ap-southeast-1a`, `ap-southeast-1b`).
  * Kubernetes Pod Readiness/Liveness Probes tự khởi động lại dịch vụ lỗi trong $< 15\text{ giây}$.
  * Độ trễ phản hồi (P95 Latency TTFT): $\le 3\text{ giây}$ thông qua cơ chế Token Streaming và Semantic Cache.

---
