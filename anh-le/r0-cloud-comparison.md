# R0 – So sánh tổng chi phí tháng: GCP vs AWS vs Azure (Singapore)

Nguồn số: `cost_model.py` (chạy `python3 cost_model.py`). Đơn giá lấy từ `research/r1-compute-network.md`, `r2-data.md`, `r3-models.md`, `r5-r9-security-governance.md`, `r8-r6-connectors-labor.md`. Khối lượng lấy từ D1–D30 (`PLAN.md`), `sizing-load.md`. USD/tháng, giá niêm yết, chưa VAT. D30 = cấu hình compute đã chốt ở Q32 (3 loại pod × 1 vCPU/2 GB, 2 pod/zone giờ hành chính, 1 pod ngoài giờ, staging là namespace trong cluster prod).

## 1. Bảng tổng (DR phương án A – chỉ chịu mất 1 zone)

| Component | GCP | AWS | Azure | Ghi chú |
|---|---|---|---|---|
| compute | 272,13 | 256,01 | 310,60 | GKE Autopilot / EKS + Fargate / AKS Standard + D4s_v5; gồm phí cluster 73 USD |
| llm | 1.093,34 | 1.119,21 | 994,15 | Haiku 5.5 text 946,72 (giống nhau 3 cloud) + 4.312 ảnh/tháng: 0,034 / 0,04 / 0,011 USD/ảnh |
| embedding | 19,50 | 13,00 | 3,12 | 130 triệu token/tháng |
| gateway | 0 | 0 | 0 | LiteLLM nằm trong compute (D23) |
| load_balancer | 29,44 | 24,24 | 352,15 | Azure: Application Gateway WAF v2 (đã gồm WAF) |
| authn | 0 | 0 | 0 | IAP / ALB OIDC / Entra app registration — nằm trong LB hoặc compute (D6) |
| authz | 0 | 0 | 0 | Nằm trong database (RLS) + gateway (D25) |
| database | 466,71 | 537,64 | 501,14 | Postgres HA 2 vCPU / 13–16 GB + 150 GB + staging DB nhỏ |
| vector_db | 0 | 0 | 0 | Nằm trong database (pgvector) |
| object_storage | 82,80 | 102,80 | 103,30 | 4 TB (2 GB/user); Azure dùng ZRS |
| cache_queue | 55,75 | 56,50 | 15,04 | Valkey/Redis HA + queue; Azure: giá HA chưa xác nhận |
| sandbox | 314,64 | 289,18 | 402,25 | 140.789 lượt × 2 phút (D29); Azure: node pool Kata |
| connectors | 0 | 0 | 0 | Nằm trong compute; API không tính phí (r8) |
| secrets_kms | 3,96 | 13,78 | 2,58 | Envelope encryption (D22) |
| backup_dr | 11,20 | 0 | 0 | AWS/Azure: backup nằm trong database |
| monitoring | 22,51 | 47,39 | 53,16 | Log 30 GB, audit 4 GB/tháng giữ 12 tháng, prompt log 30 ngày |
| governance | 805,98 | 2.435,41 | 8.059,38 | Guardrail + DLP theo D24 (2,81 tỉ token quét/tháng) + eval gate 525,46 |
| network | 64,26 | 165,64 | 114,00 | WAF (GCP/AWS), NAT, private endpoint, egress, inter-zone |
| cicd | 14,00 | 12,00 | 45,07 | Build 2.000 phút + registry |
| ops_labor | 3.400,00 | 3.400,00 | 3.400,00 | D8 |
| licenses | 0 | 0 | 0 | D19: không mua support |
| **TOTAL** | **6.656,22** | **8.472,80** | **14.355,95** | |
| **USD/DAU** | **3,33** | **4,24** | **7,18** | |

**Rẻ nhất: GCP.** AWS đắt hơn 1.816,58 USD/tháng (+27%), Azure đắt hơn 7.699,73 USD/tháng (+116%).

**Nếu bỏ dòng governance**, ba cloud gần nhau: GCP 5.850, AWS 6.037, Azure 6.297 USD. **Chênh lệch chủ yếu do giá guardrail + DLP:**
- GCP: Model Armor 0,10 USD/1 triệu token, đã gồm DLP → 280,52 USD.
- AWS: Bedrock Guardrails, prompt attack 0,08 + PII 0,10 USD/1.000 text unit → ~1.910 USD.
- Azure: Content Safety ở SEA chỉ có gói cam kết 338 USD + phí vượt 0,338/1.000 record, cộng PII của Azure Language → ~7.534 USD.

## 2. Q9 – Chênh lệch DR phương án B (thêm backup sang region khác)

| | GCP | AWS | Azure |
|---|---|---|---|
| Thêm cho DR B | +153,20 | +159,25 | +128,25 |
| TOTAL với DR B | 6.809,42 | 8.632,05 | 14.484,20 |
| Cách làm | Backup Cloud SQL sang Jakarta + GCS dual-region | RDS cross-region backup sang Tokyo + S3 CRR | Geo-redundant backup + Blob GZRS |

DR B chỉ thêm khoảng 2% tổng chi phí trên mọi cloud.

## 3. Năm dòng lớn nhất

| # | GCP | AWS | Azure |
|---|---|---|---|
| 1 | ops_labor 3.400 | ops_labor 3.400 | governance 8.059 |
| 2 | llm 1.093 | governance 2.435 | ops_labor 3.400 |
| 3 | governance 806 | llm 1.119 | llm 994 |
| 4 | database 467 | database 538 | database 501 |
| 5 | sandbox 315 | sandbox 289 | sandbox 402 |

## 4. Kiểm tra LiteLLM (D23, D30)

Tài liệu chính thức (https://docs.litellm.ai/docs/proxy/prod) khuyến nghị mỗi pod **"1 vCPU and 4Gi of memory, as both requests and limits"**, ghi rõ "4Gi is a floor rather than a target"; chạy 1 Uvicorn worker mỗi pod và scale ngang; **bắt buộc Redis (≥ 7.0) khi chạy > 1 instance** và Postgres cho production.

→ D30 đặt 2 GB/pod cho LiteLLM là **thấp hơn khuyến nghị**. Nâng 2 pod LiteLLM lên 4 GiB làm compute tăng khoảng 12 USD (GCP), 11 USD (AWS), 0 USD (Azure, vẫn vừa node). Redis và Postgres đã có trong kiến trúc. **Chưa sửa D30 — cần user quyết.**

## 5. Giả định chưa chốt (cần user rà)

| # | Giả định | Giá trị trong model | Ảnh hưởng |
|---|---|---|---|
| 1 | Mức dùng workspace | 2 GB/user (4 TB) | object_storage, DR |
| 2 | Shared KB và workspace mới cần embed | KB 100 triệu token, đổi 10%/tháng; 20 file × 3.000 token/user/tháng | embedding (nhỏ) |
| 3 | Dung lượng DB | 150 GB (chat 12 tháng ~60 GB, ~3 triệu vector ~18 GB, spend log LiteLLM ~16 GB) | database |
| 4 | Cấu hình DB | 2 vCPU, 13 GB (GCP) / 16 GB (AWS, Azure) cho pgvector | database |
| 5 | Lượng token guardrail quét (D24) | Mỗi lượt: cấp 1 3.000, cấp 2 10.000, cấp 3 3.000, cấp 4 12.000, cấp 5 200 token đầu vào + output cuối; tổng 2,81 tỉ token/tháng | **governance — biến quyết định cloud** |
| 6 | Ký tự/token | 4 | governance AWS, Azure |
| 7 | Eval gate | 100 nhiệm vụ/cấp × 5 cấp, 4 lần/tháng, Haiku + Opus + Opus làm giám khảo | governance 525 USD |
| 8 | Mạng | LB 500 GB, 6,2 triệu HTTP request, NAT 100 GB, model API 60 GB, egress 200 GB, inter-zone 200 GB | network, LB |
| 9 | Log | App log 30 GB, audit 4 GB, prompt log 52 GB, 50 triệu metric sample, 7 triệu span | monitoring |
| 10 | Azure node packing | 70% hiệu suất node | compute, sandbox Azure |
| 11 | Số lần gọi KMS, secret, queue | 760.000 KMS op, 20 secret, 1,1 triệu queue op | nhỏ |
| 12 | CI/CD | 2.000 phút build, registry 20 GB | nhỏ |
| 13 | DR B | 300 GB truyền backup DB, 200 GB object mới/tháng | DR |
| 14 | Model ảnh | GCP Gemini Flash-Lite Image; AWS Stable Image Core; Azure gpt-image-1-mini medium (AWS, Azure chạy ở US) | llm |

## 6. THIẾU GIÁ hoặc cần xác minh

| Hạng mục | Xử lý trong model |
|---|---|
| Phí backup cross-region riêng của Cloud SQL | Không có giá; chỉ tính transfer + backup storage |
| Giá backup storage ở Jakarta (GCP) | Dùng giá Singapore làm proxy |
| Azure Managed Redis bản HA 2 node | Dùng giá B0 0,02 USD/giờ (có thể thấp hơn thực tế) |
| RDS instance nhỏ hơn t4g.medium cho staging | Không có trong research; dùng t4g.medium Single-AZ |
| `gemini-embedding-001` đơn vị "count" | Coi là token |
| Bedrock InvokeGuardrailChecks (0,08) | Giá từ trang giá, chưa thấy SKU APS1 |
| Model Armor ở asia-southeast1 | Chưa xác minh có sẵn ở region |
| Content filter mặc định của Azure miễn phí | Chỉ có nguồn Microsoft Q&A → **không dùng**; nếu xác minh được thì governance Azure giảm mạnh |
| Titan Image v2 (AWS) còn dùng được không | Dùng Stable Image Core thay |

## 7. Lưu ý

- Chưa tính phí **ghi cache** của Claude (0,125 USD/1 triệu token cho cache 5 phút); chỉ tính cache read → llm có thể cao hơn vài %.
- Embedding chỉ tính phần hằng tháng; index ban đầu 100 triệu token là chi phí một lần (GCP 15, AWS 10, Azure 2,4 USD).
- Rerank không đưa vào (chưa có quyết định); nếu dùng: khoảng 1–2 USD/1.000 truy vấn.
- Giá AWS và Azure lấy từ API giá chính thức; nhóm vẫn phải chụp màn hình trang giá hoặc calculator cho sheet `BangChung`.
- Ảnh cấp 5 trên AWS và Azure chỉ chạy ở region US (D26 cho phép endpoint ngoài Singapore nếu có cam kết zero-retention).
- Sandbox tính theo trần 2 phút/lượt (D29) → chi phí thật thấp hơn.
