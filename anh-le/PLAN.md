# VBot Capstone – Kế hoạch làm bài

Đề: `vbot-capstone.html`. Mục tiêu: chi phí tháng thấp nhất **sau khi** đã đủ 19 component bắt buộc và đạt H1–H8.

## Quyết định đã chốt

| # | Quyết định | Lý do |
|---|---|---|
| D1 | Region **Singapore**. Cloud provider: **chọn theo tổng chi phí** sau khi so sánh GCP / AWS / Azure (R0) | Gần người dùng tại Việt Nam, độ trễ thấp (H6) |
| D2 | LLM: **API model managed của cloud chính, không tự host GPU**; routing nhiều bậc theo cấp tác vụ. **Model cụ thể từng cấp: chưa chốt, quyết bằng bảng R3** (Q17a) | (1) Cùng cloud chính, gọi qua private endpoint (Private Service Connect / PrivateLink / Private Endpoint) → đạt H1 mà không cần egress ra ngoài. (2) Dịch vụ model managed của cloud (Vertex AI / Bedrock / Azure AI Foundry) có cam kết không dùng dữ liệu khách hàng để huấn luyện → H5. (3) Nhiều bậc model cho phép routing theo cấp tác vụ → giảm chi phí mà vẫn giữ ngưỡng 95% (H8). (4) Trả theo token, không trả tiền GPU nhàn rỗi ngoài 220 giờ hành chính; tự host cần tối thiểu 2 GPU chạy HA. (5) Một hóa đơn, một IAM, ít thành phần vận hành hơn. Tự host GPU chỉ dùng làm phương án so sánh trên slide, kèm điểm hòa vốn **tính từ giá đã research** |
| D3 | Giờ phục vụ: **giờ hành chính chạy đầy đủ (multi-AZ, HA); ngoài giờ giữ mức tối thiểu** — DB, storage, vault, log chạy 24/7; app 1 replica; sandbox scale về 0 node, bật khi có job | Đề chỉ yêu cầu 99,5% trong giờ hành chính (T2–T6, 8:00–18:00). App và sandbox tính phần lớn theo 220 giờ thay vì 730 giờ. Ngoài giờ không ràng buộc H6 nên chấp nhận cold start. Ghi rõ giả định trên slide |
| D4 | Connector **hybrid**: gọi trực tiếp API search của SaaS bằng OAuth của user cho dữ liệu cá nhân/hay đổi (email, lịch, Jira…); index trước **KB chung** (chính sách, wiki công khai) kèm metadata ACL; index **workspace riêng** tách theo user | Quyền gốc do SaaS áp → đạt H2, không cần service account quyền rộng. Vector DB nhỏ (chỉ KB chung + workspace) → rẻ. Đánh đổi: độ trễ và rate limit của SaaS so với chi phí index lớn |
| D5 | Workspace: **object storage trả theo dung lượng thực dùng** (GCS / S3 / Blob); quota 10 GB/user đảm bảo bằng chính sách ở tầng app (chặn khi vượt). Báo giá tính theo **mức dùng dự kiến có số liệu nguồn**; phần rủi ro ghi chi phí khi đầy 20 TB | Object storage không cần cấp phát trước → "cấp dần" là mặc định. Tính theo trần làm phồng object_storage và backup_dr |
| D6 | SSO: **dùng IdP sẵn có của tập đoàn** (OIDC/SAML + MFA); cloud nhận token qua dịch vụ tương ứng (R5) | Đề nói "SSO tập đoàn" → IdP đã có. Chỉ tính phần trên cloud. Giả định ghi trên slide; **hỏi giảng viên** có chấp nhận chi phí 0 cho IdP sẵn có |
| D7 | ops_labor: **2 FTE** (1 platform/SRE + 1 AI/MLOps), trực luân phiên giờ hành chính | Khối lượng 2.000 user chỉ cần ~1 FTE, nhưng cần người thứ hai để luôn có người trực (bảo vệ 99,5%, không phụ thuộc một người) |
| D9 | Loại công ty: **tập đoàn đa ngành, chỉ tính khối văn phòng, có phòng IT viết code** | Đúng mô tả đề ("tập đoàn", "nhân viên văn phòng"), dùng đủ 5 cấp và 11 connector; phòng IT tạo nhu cầu cấp 3–4 thật |
| D10 | Cơ cấu 2.000 người: Kinh doanh/CSKH 25%, Kế toán 12%, Nhân sự/HC/pháp chế 13%, Marketing 10%, Dự án/vận hành 15%, Mua hàng/SCM 10%, IT 10%, Lãnh đạo 5% | Giả định của nhóm, dùng để suy ra tỉ lệ 5 cấp tác vụ |
| D11 | Đơn vị đếm: **1 request = 1 nhiệm vụ** (trọn vòng, kể cả vài lượt qua lại). Quy đổi: nhiệm vụ × lượt/nhiệm vụ × token/lượt = token; nhiệm vụ × LLM call/nhiệm vụ = tải giờ cao điểm | Dễ đối chiếu với công việc thật của từng phòng; vẫn tính đúng token và tải |
| D12 | Thời hạn lưu: audit log **12 tháng** (30 ngày truy vấn nhanh, sau đó archive); lịch sử chat **12 tháng**; file workspace đến khi user xóa, file tạm agent 30 ngày; bộ nhớ dài hạn đến khi user xóa; log ứng dụng 30 ngày; prompt/response đầy đủ 30 ngày (đã che PII) | H5 yêu cầu thời hạn lưu và audit 12 tháng; chat khớp audit; text chat dung lượng nhỏ |
| D13 | Sandbox: hạng mặc định 1 vCPU / 2 GB / trần 2 phút; hạng mở rộng 2 vCPU / 4 GB / **trần 10 phút** cho mọi tác vụ; đĩa tạm 5 GB; không egress; hủy sau khi chạy. Việc nặng hơn (build lớn, test suite, dữ liệu GB) chuyển sang CI/CD hoặc hệ thống data | Theo H6 (agent ≤ 10 phút) và H3 (giới hạn tài nguyên). Trần là giới hạn trên; chi phí tính theo thời gian chạy thực |
| D14 | Sandbox **chỉ dùng image dựng sẵn** (Python: pandas, numpy, openpyxl, python-docx, python-pptx, matplotlib, plotly; Node), không cài thư viện lúc chạy; cập nhật image qua CI/CD | Đạt H3 tuyệt đối (không egress), không thêm chi phí mirror, tránh rủi ro supply chain. Mirror nội bộ ghi vào phần mở rộng |
| D15 | Xác nhận hành động ghi theo **mức rủi ro**: cao (gửi ra ngoài tập đoàn, xóa, chia sẻ quyền) → xác nhận từng hành động; thấp (ticket/email/trang nháp) → duyệt gộp một lần cho cả lô. Nội dung từ connector **không bao giờ** kích hoạt hành động ghi; màn hình xác nhận hiện rõ người nhận, nội dung, đính kèm | Đạt H4, không làm agent cấp 4 kẹt; trả lời câu hỏi prompt injection trong email |
| D16 | Staging **thu nhỏ, chỉ bật khi cần** (deploy, eval gate), giả định ~40 giờ/tháng: 1 zone, 1 replica, DB không HA, cấu hình nhỏ nhất, dữ liệu giả/đã che PII. Compute bật/tắt bằng IaC; DB và storage của staging giữ 24/7 (dung lượng nhỏ) | Đề bắt buộc "prod và 1 staging" nhưng không quy định quy mô → tiết kiệm. Rủi ro "deploy gấp phải chờ staging khởi động" — ghi thời gian khởi động trên slide |
| D17 | Quota đo bằng **USD/tháng** (quy đổi token, ảnh, phút sandbox tại gateway); theo user và phòng ban (phòng = tổng quota nhân viên, trưởng phòng điều phối). Cơ chế **3 nấc**: 80% cảnh báo; 100% hạ cấp (chỉ model rẻ nhất cho cấp 1–2, khóa cấp 4–5); 120% chặn đến đầu tháng sau trừ khi trưởng phòng duyệt. Ngân sách toàn hệ thống 90% → cảnh báo FinOps. Mức quota cụ thể tính sau khi có số liệu tải | H8: quota theo người và đơn vị, cảnh báo, cách cắt. USD gắn trực tiếp với chi phí; hạ cấp trước khi chặn để không gián đoạn công việc |
| D18 | License SaaS (Google Workspace, M365, Notion, Jira, Confluence): **không tính**, giả định tập đoàn đã có. Báo giá chỉ tính phần chạy connector trên cloud + API tính phí theo lượt (nếu có) | Giống D6: không tính trùng chi phí tập đoàn đã trả. Ghi giả định trên slide |
| D19 | **Không có dòng contingency**; **không mua gói support** của cloud | Điểm chi phí tính theo tổng; rủi ro trình bày bằng kịch bản (DAU ×2, giá token ±) trên slide. Không support: chuẩn bị trả lời "sự cố tầng cloud ai hỗ trợ" bằng SLA của dịch vụ managed + 2 FTE trực + runbook |
| D20 | Giờ cao điểm = **15%** traffic ngày (2.118 nhiệm vụ/giờ ≈ 0,59/giây; 1,13 lượt chat/giây), dùng cho cả chi phí và capacity; autoscale lo phần vượt | Mức cơ sở của research (một múi giờ, họp dồn 9–11h và 13–15h). Tải nhỏ, chủ yếu ảnh hưởng quota token/phút và số replica |
| D21 | Sizing tải: **7,06 nhiệm vụ/người/ngày, 14.120/ngày, 310.644/tháng; 27.098 lượt chat/ngày**; mix nhiệm vụ 84,0 / 7,4 / 3,9 / 3,9 / 0,7% | Bottom-up theo 8 phòng ban, chi tiết `sizing-load.md`, công thức `sizing.py` |
| D22 | Token vault: **envelope encryption bằng KMS, lưu token đã mã hóa trong Postgres** (bảng riêng, RLS); chỉ service account connector được gọi KMS giải mã, cho đúng user của request; audit mọi lần giải mã | Đạt H2; chạy được trên cả 3 cloud; tránh ~720 USD (GCP) / ~4.800 USD (AWS) mỗi tháng nếu lưu 12.000 secret riêng (`research/r5-r9-security-governance.md`) |
| D23 | LLM gateway: **LiteLLM open-source tự chạy trên K8s, 2 replica ở 2 zone**, dùng chung Postgres + Redis; quota USD, routing, fallback, log chi phí. `authz` phần quota ghi "nằm trong gateway" | Duy nhất có sẵn quota theo USD (D17). Managed: GCP API Gateway/AWS HTTP API rẻ (~2–4 USD) nhưng không quota; Apigee ~1.595 USD, APIM Basic v2 ~150 / Std v2 ~700 USD và chỉ quota theo token (`research/r5-r9-security-governance.md` §6). Rủi ro: tự vận hành, không SLA |
| D24 | Guardrail + DLP **chỉ quét phần mới và không đáng tin**: tin nhắn mới của user, nội dung lấy từ connector, output cuối cho user/hành động ghi. Không quét lại system prompt, lịch sử chat, bước trung gian của agent. "Mỗi đoạn text chỉ quét một lần, khi vào hệ thống" | Đạt H4/H5 (đầu vào + đầu ra, chặn injection tại nguồn connector; D15 chặn connector kích hoạt ghi). Quét toàn bộ ~12,6 tỉ token/tháng tốn ~1.260 USD (Model Armor) đến ~7.500 USD (Bedrock Guardrails) |
| D25 | authz **trong ứng dụng + DB**: RBAC theo group từ token SSO; ACL tài liệu = cột `allowed_groups`/`owner_id` trên chunk pgvector + Row-Level Security; quota trong LiteLLM; dữ liệu connector do SaaS áp quyền gốc. Báo giá: 0 USD, "nằm trong database và gateway" | GCP/Azure không có policy engine managed; luật quyền VBot đơn giản. Ba lớp chặn A đọc file B: RLS, lọc ACL kết quả search, token OAuth của chính user |
| D26 | Model được gọi qua **endpoint global** của cloud chính, điều kiện có cam kết zero-retention + no-training; dữ liệu lưu (DB, storage, log) ở Singapore | H1 chỉ yêu cầu private endpoint hoặc kênh cam kết không lưu dữ liệu; H5 yêu cầu no-training; đề không yêu cầu data residency. Hybrid theo nhãn DLP ghi vào "Rủi ro và mở rộng" (Nghị định 13/2023) |
| D27 | Token theo cấp (mức cơ sở, mỗi lượt): T1 2 × 5,5k / 250 (cache 50%); T2 2 × 18k / 2,5k (60%); T3 3,5 × 12k / 1k (65%); T4 8 × 15k / 300 (80%); T5 1,5 × 4k / 600 + 1 ảnh. Tổng **12,19 tỉ input (≈61% cache) + 0,79 tỉ output/tháng** | `research/token-per-task.md`, mọi số có nguồn; khoảng thấp–cao 4,6–42,8 tỉ input |
| D28 | Model: **tham chiếu = Claude Opus 5.5**; mặc định **Claude Haiku 5.5 cho mọi cấp** (cấp 1–2 tắt reasoning để đạt H6); eval gate theo từng cấp, cấp nào < 95% thì LiteLLM chuyển sang Sonnet 5.5. Báo giá theo Haiku (~947 USD/tháng LLM text); rủi ro: Sonnet cho cấp 3–4 (~5.652 USD/tháng). Ảnh cấp 5 theo cloud chọn | Haiku 5.5 giá 0,10/0,50 như nhau trên cả 3 cloud → LLM không quyết định cloud. Gap: TTFT của Haiku khi tắt reasoning chưa có số đo |
| D29 | Sandbox: **≈ 6.400 lượt/ngày, 140.800 lượt/tháng** (cấp 2: 1/nhiệm vụ; cấp 3: 2,5/lượt chat; cấp 5: 34% lượt là sơ đồ code); tính chi phí theo **trần 2 phút/lượt, 1 vCPU / 2 GB** (cận trên). Nền tảng theo cloud chọn; ưu tiên tự chạy trên K8s (gVisor / Fargate / Kata) | Thời gian chạy thật chưa có nguồn → dùng trần chính sách D13. Chi phí 289–509 USD/tháng tùy nền tảng; tự chạy rẻ hơn managed và kiểm soát egress tốt hơn |
| D30 | Compute app: web/API, LiteLLM, worker mỗi loại **2 pod × 1 vCPU / 2 GB ở 2 zone** trong giờ hành chính (220 h), 1 pod ngoài giờ (510 h), 1 pod staging (40 h) → ≈ **2.970 vCPU-giờ + 5.940 GB-giờ/tháng**; autoscale tối đa ×2 (không tính vào cơ sở). **Staging = namespace riêng trong cluster prod** (NetworkPolicy, DB, bucket, service account riêng) | Tải ~1,1 lượt/giây, chủ yếu chờ stream model; 2 zone → H7. Namespace tiết kiệm ~73 USD/tháng phí cluster. Gap: cấu hình khuyến nghị của LiteLLM |
| D31 | Cloud: **GCP asia-southeast1** — tổng 3.421 USD/tháng (DR B, không gồm nhân sự) vs AWS 5.243, Azure 11.084 | `r0-cloud-comparison.md`, `cost_model.py`. Chênh chủ yếu ở governance (Model Armor 0,10 USD/1M token, DLP đi kèm) |
| D32 | DR **mức B**: Cloud SQL HA + PITR, bản sao backup sang Jakarta, bucket workspace dual-region, dựng lại bằng IaC (+153 USD/tháng) | Đáp ứng RTO 4 h / RPO 1 h cả khi mất region, chỉ thêm ~2% |
| D33 | LiteLLM pod 4 GiB RAM (tài liệu LiteLLM khuyến nghị ≥ 4 GiB) | +12 USD/tháng |
| D34 | **Bỏ chi phí nhân sự khỏi báo giá** (16/10/2026): `ops_labor` = 0, thay cho 3.400 USD của D7/D8 | Coach hướng dẫn báo giá không cần phí nhân sự. TOTAL còn 3.421,44 USD/tháng (1,71 USD/DAU) |
| D8 | Lương FTE theo **thị trường Việt Nam**, tính **package gross năm × 12, không cộng bảo hiểm công ty đóng**: SRE senior 5–8 năm 53,85 tr + AI/MLOps mid 3–4 năm 34,1 tr = 87,95 tr/tháng → **3.400 USD/tháng** (25.870 VND/USD, Vietcombank 16/10/2026) | Trung vị gross ITviec 2024–2025 (loại thưởng) → khớp định nghĩa nguồn. SRE senior vì chịu HA/DR/bảo mật; MLOps mid đủ khi đã có LiteLLM + eval gate. Bảo hiểm bắt buộc coi là chi phí nhân sự chung của tập đoàn (chuẩn bị trả lời hội đồng) |

> Quy tắc: mọi đơn giá phải lấy từ trang giá chính thức hoặc calculator, kèm ảnh/link. Không dùng giá ước đoán.

## Hàng đợi research giá (quyết định bằng bảng so sánh)

| R | Cần so sánh | Phương án |
|---|---|---|
| R0 | Chọn cloud provider (theo tổng chi phí) | GCP vs AWS vs Azure tại Singapore, so các dòng lớn: LLM (R3 cho cả 3 cloud), Kubernetes + sandbox, Postgres HA, object storage, egress |
| R1 | Nền compute + sandbox (theo cloud) | GCP: GKE Standard (scale theo lịch) / Autopilot / Cloud Run + gVisor · AWS: EKS / Fargate + Firecracker · Azure: AKS + Kata / Container Apps |
| R2 | Database + vector DB + cache/queue (theo cloud) | Postgres HA + pgvector (Cloud SQL / RDS / Azure PG) vs AlloyDB / Aurora vs vector DB riêng (Vertex Vector Search / OpenSearch / AI Search); Redis managed; queue (Pub/Sub / SQS / Service Bus) |
| R3 | Model cho từng cấp: giá token, benchmark, TTFT | Gemini (Flash-Lite/Flash/Pro), Claude (Haiku/Sonnet/Opus), open-weight MaaS (Llama, Mistral, Qwen); model ảnh; embedding; giá cache, batch |
| R5 | authn/authz/secrets (theo cloud) | GCP IAP / Identity Platform · AWS Cognito / Verified Access · Azure Entra External ID; KMS + Secret Manager / Key Vault cho token vault |
| R6 | Lương SRE và AI/MLOps tại VN (số liệu) | Báo cáo lương ITviec, TopDev, Glassdoor; tỉ lệ BHXH/BHYT/BHTN công ty đóng |
| R7 | Chi phí DR (cho Q9) | A: DB HA multi-zone + K8s regional + storage regional; B: A + backup DB cross-region + bucket backup region khác + egress liên region; C: B + read replica + cụm K8s nhỏ ở region khác |
| R9 | Gateway, governance, monitoring, network (theo cloud) | LLM gateway (managed vs tự chạy LiteLLM), guardrail/prompt injection (Model Armor / Bedrock Guardrails / Azure Content Safety), DLP (Sensitive Data Protection / Macie / Purview), log + audit 12 tháng, LB + WAF, NAT, private endpoint, egress, CI/CD + registry |
| R8 | Connector: API tính phí theo lượt + rate limit (11 connector) | Gmail, Drive, Calendar, Docs/Sheets/Slides, Outlook, M365/Graph (Teams metered API), OneDrive/SharePoint, Teams, Notion, Jira, Confluence |
| R4 | Mức dùng storage thực tế/user (số liệu, không phải giá) | Dung lượng Google Drive / OneDrive trung bình mỗi user doanh nghiệp; giá object storage lớp chuẩn và lớp lưu trữ rẻ ở Singapore (3 cloud) |

## Quyết định đang mở (grilling)

- [ ] Model cho từng cấp 1–5 và model tham chiếu (H8)
- [ ] Giả định tải: số request/user/ngày, tỉ lệ 5 cấp, token mỗi cấp — **research xong** → `research/usage-benchmarks.md` (đề xuất: 5 / 12 / 30 req/user/ngày; mix 65/17/8/6/4; giờ cao điểm 15%). Đang estimate từ dưới lên theo phòng ban (Q13) → `research/task-volume-by-role.md`
- [ ] Cloud provider (R0) → kéo theo compute + sandbox (R1), DB/vector/cache/queue (R2), authn/secrets (R5), gateway/governance/monitoring/network (R9)
- [x] Connector (D4) · SSO (D6) · sandbox spec (D13, D14) · xác nhận hành động (D15) · quota (D17) · license SaaS (D18)
- [ ] HA/DR: thành phần nào multi-AZ, cách backup — **pending Q9**: chỉ chịu mất 1 zone (A) / thêm backup sang region khác (B) / warm standby region khác (C). Quyết sau khi có bảng giá R7
- [x] Số FTE vận hành (D7, D8)
- [ ] Danh sách đòn bẩy tiết kiệm

## Các bước

### Bước 0 – Chuẩn bị
- [ ] Chia 5 vai (nhóm 4 người: gộp Sandbox/bảo mật với Cloud/HA)
- [ ] Lấy file mẫu XLSX có dropdown từ trợ giảng
- [x] Chọn region Singapore (D1) · [ ] cloud provider (R0)
- [x] Chốt hướng LLM: API managed, không tự host (D2) · [ ] model từng cấp (R3)

### Bước 1 – Sizing từ 2.000 DAU
- [ ] Số request/user/ngày và tỉ lệ 5 cấp tác vụ
- [ ] Token vào/ra từng cấp (gồm context RAG, số bước agent) → token/tháng (× 22 ngày)
- [ ] Giờ cao điểm: request/giây, token/giây, số phiên đồng thời
- [ ] Số lượt sandbox × thời gian mỗi lượt; số ảnh sinh mỗi tháng
- [ ] Dung lượng: workspace, số vector của KB, lịch sử chat, log và audit 12 tháng
- [ ] Số lệnh gọi connector, lượng egress
- [ ] Model từng cấp và model tham chiếu

### Bước 2 – Kiến trúc và báo giá (chia agent tìm giá)

| Vai | Component |
|---|---|
| Model serving | `llm`, `embedding`, `gateway` |
| Data/workspace | `connectors`, `database`, `vector_db`, `object_storage`, `cache_queue` |
| Sandbox/bảo mật | `sandbox`, `authn`, `authz`, `secrets_kms`, `governance` |
| Cloud/HA | `compute`, `load_balancer`, `network`, `backup_dr`, `monitoring`, `cicd` |
| Kiến trúc sư trưởng | `ops_labor`, `licenses`, `contingency`, `TOTAL`, sơ đồ |

Mỗi dòng báo giá:
- [ ] Ảnh chụp giá (dịch vụ, SKU, region, đơn giá) → sheet `BangChung`, mã E01…
- [ ] Ghi chú dạng `đơn giá × số lượng × giờ`, ghi rõ HA và staging
- [ ] Đối chiếu H1–H8

### Bước 3 – Tối ưu và đóng gói
- [ ] Áp đòn bẩy tiết kiệm, ghi rõ giả định
- [ ] Chạy validator đến khi ĐẠT (không có chữ free/trial/miễn phí/dùng thử)
- [ ] Slide theo 12 mục khung; tổng trên slide = TOTAL
- [ ] Tập trả lời 6 câu hỏi hội đồng
- [ ] Nộp form trước 03:05
