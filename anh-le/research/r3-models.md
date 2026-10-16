# R3 – Đơn giá model cho từng cấp (Vertex AI · Amazon Bedrock · Azure AI Foundry)

- Ngày truy cập mọi nguồn: **2026-10-16**. Đơn vị: USD. Giá token là **USD / 1M token** trừ khi ghi khác.
- Chỉ dùng giá niêm yết pay-as-you-go. **Không** dùng free tier, credit, giá khuyến mãi. Khi trang giá có giá khuyến mãi (Google ghi "Promotional pricing provided through 50% credits back"), file này ghi **giá chuẩn** và ghi chú giá khuyến mãi riêng.
- Region mục tiêu: GCP `asia-southeast1`, AWS `ap-southeast-1`, Azure `southeastasia`. Ký hiệu: **[SG]** = endpoint/region Singapore; **[GLOBAL]** = endpoint global / Global CRIS / Global Standard (dữ liệu có thể xử lý ngoài Singapore); **[GẦN NHẤT]** = region khác gần nhất.
- Cách lấy số:
  - GCP: tải HTML trang giá chính thức, đọc từng tab (Standard / Priority / Flex-Batch; với Claude có tab theo region).
  - AWS: trang giá Bedrock render bằng JS. File này lấy số từ chính file giá mà trang dùng (`https://b0.p.awsstatic.com/pricing/2.0/meteredUnitMaps/bedrockfoundationmodels/USD/current/*.json` và `.../bedrock/USD/current/bedrock.json`), chọn region "Asia Pacific (Singapore)". Kết quả giống khi chọn Singapore trong ô {regionSelector} của trang. Model OpenAI và một số model khác có bảng giá riêng trong model card của Bedrock.
  - Azure: dùng **Azure Retail Prices API** chính thức (`https://prices.azure.com/api/retail/prices`, `armRegionName eq 'southeastasia'`). Đây là nguồn dữ liệu của trang giá Azure và Azure Pricing Calculator. Region khả dụng lấy từ Microsoft Learn.

## Nguồn chính

| Mã | Nguồn | URL |
|---|---|---|
| G1 | Google Cloud – Agent Platform (Vertex AI) Generative AI pricing | https://cloud.google.com/vertex-ai/generative-ai/pricing |
| G2 | Google Cloud – Locations (model theo region) | https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations |
| G3 | Google Cloud – Agent Search pricing (Ranking API) | https://cloud.google.com/generative-ai-app-builder/pricing |
| G4 | Google Cloud – Imagen 4 model page (ngày ngừng) | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/imagen/4-0-generate |
| A1 | Amazon Bedrock pricing (region Singapore) | https://aws.amazon.com/bedrock/pricing/ |
| A2 | Amazon Bedrock model cards (giá OpenAI, region, model ID) | https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html |
| Z1 | Azure Retail Prices API (southeastasia, Foundry Models) | https://prices.azure.com/api/retail/prices?$filter=armRegionName%20eq%20%27southeastasia%27 |
| Z2 | Azure OpenAI pricing page | https://azure.microsoft.com/en-us/pricing/details/azure-openai/ |
| Z3 | Microsoft Learn – Foundry Models sold by Azure: region availability | https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-region-availability |
| C1 | Anthropic – Pricing (gồm Claude in Microsoft Foundry) | https://platform.claude.com/docs/en/about-claude/pricing |
| C2 | Anthropic – Claude in Microsoft Foundry | https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry |
| O1 | OpenAI – Image generation guide (chi phí mỗi ảnh) | https://developers.openai.com/api/docs/guides/image-generation |
| Q1 | Artificial Analysis – Leaderboard | https://artificialanalysis.ai/leaderboards/models |
| Q2 | Artificial Analysis – Model pages | https://artificialanalysis.ai/models/{slug} |

---

## 1. GCP – Vertex AI (Gemini Enterprise Agent Platform)

### 1.1 Gemini – text (Standard, nguồn G1)

Quy tắc của G1: "Non-global" = endpoint region (gồm `asia-southeast1`), giá **+10%** so với Global, áp dụng cho Gemini 3 trở lên từ 01/07/2026. Ngữ cảnh > 200K token: toàn bộ request tính giá long-context. Batch/Flex = 50% giá Standard. Priority = 1,8× Standard.

| Model (ID) | Có ở SG? (G2) | Endpoint | Input | Cached input | Output | Batch/Flex in / out | Ghi chú |
|---|---|---|---|---|---|---|---|
| Gemini 3.1 Flash-Lite (`gemini-3.1-flash-lite`) | Không | [GLOBAL] | 0,25 | 0,025 | 1,50 | 0,125 / 0,75 | Non-global 0,275 / 1,65 (không có ở SG) |
| Gemini 3.5 Flash-Lite (`gemini-3.5-flash-lite`) | Không | [GLOBAL] | 0,30 | 0,03 | 2,50 | 0,15 / 1,25 | Non-global 0,33 / 2,75 |
| Gemini 2.5 Flash-Lite (`gemini-2.5-flash-lite`) | Không | [GLOBAL] | 0,10 | 0,01 | 0,40 | 0,05 / 0,20 | Thế hệ cũ |
| Gemini 2.5 Flash (`gemini-2.5-flash`) | **Có** | [SG] | 0,30 | 0,03 | 2,50 | 0,15 / 1,25 | Bảng 2.5 không tách global/non-global |
| **Gemini 3.5 Flash** (`gemini-3.5-flash`) | **Có** | [SG] non-global | **1,65** | 0,165 | **9,90** | 0,825 / 4,95 | Global: 1,50 / 0,15 / 9,00 |
| Gemini 3.8 Flash (`gemini-3.8-flash`) | Không | [GLOBAL] | **1,50** | 0,15 | **7,50** | 0,75 / 3,75 | Giá chuẩn (từ 01/01/2027). Đến 31/12/2026 có **khuyến mãi** 0,75 / 3,75 dưới dạng credit 50%, không dùng. 3.6 Flash và 3.7 Flash cùng giá |
| Gemini 3.1 Pro Preview (`gemini-3.1-pro-preview`) | Không | [GLOBAL] | 2,00 (>200K: 4,00) | 0,20 (0,40) | 12,00 (18,00) | 1,00 / 6,00 | Preview |
| Gemini 2.5 Pro (`gemini-2.5-pro`) | Không | [GLOBAL] | 1,25 (>200K: 2,50) | 0,125 | 10,00 (15,00) | 0,625 / 5,00 | Thế hệ cũ |
| Gemini 4 Argon (`gemini-4-argon`) | Không | [GLOBAL] | **4,00** | 0,20 | **20,00** | 2,00 / 10,00 | Giá chuẩn từ 01/12/2026. Đến 30/11/2026 khuyến mãi 2 / 10, không dùng. Non-global 4,40 / 22,00 |

Cache storage (explicit caching, G1): Pro 0,0000045 USD/token/giờ; Flash, Flash-Lite 0,000001 USD/token/giờ.

### 1.2 Claude trên Vertex AI (Partner model, nguồn G1, tab theo region)

G1 tách tab giá theo region. Tab `asia-southeast1` chỉ có 5 model. Regional = Global +10% (C1 xác nhận "Regional and multi-region endpoints include a 10% premium").

| Model | Endpoint | Input | Output | Cache write 5m / 1h | Cache hit | Batch in / out | Long context |
|---|---|---|---|---|---|---|---|
| Claude Haiku 5.5 | [GLOBAL] | 0,10 | 0,50 | 0,125 / 0,20 | 0,01 | 0,05 / 0,25 | >100K: 0,50 / 2,50 |
| Claude Haiku 5.5 | [SG] tab asia-southeast1 | 0,11 | 0,55 | 0,1375 / 0,22 | 0,011 | 0,055 / 0,275 | >100K: 0,55 / 2,75. **Mâu thuẫn**: G2 không liệt kê Haiku 5.5 ở SG |
| Claude Haiku 4.5 | [GLOBAL] | 1,00 | 5,00 | 1,25 / 2,00 | 0,10 | 0,50 / 2,50 | Không có tab SG |
| Claude Sonnet 5.5 | [GLOBAL] | 2,00 | 10,00 | 2,50 / 4,00 | 0,10 | 1,00 / 5,00 | Chỉ global |
| Claude Sonnet 5 | [GLOBAL] | 2,00 | 10,00 | 2,50 / 4,00 | 0,20 | 1,00 / 5,00 | |
| Claude Sonnet 4.6 | [SG] | 3,30 | 16,50 | 4,13 / 6,60 | 0,33 | 1,65 / 8,25 | Global 3,00 / 15,00 |
| Claude Sonnet 4.5 | [SG] | 3,30 (>200K 6,60) | 16,50 (24,75) | 4,13 / 6,60 | 0,33 | 1,65 / 8,25 | |
| Claude Opus 5.5 | [GLOBAL] | 4,00 | 20,00 | 5,00 / 8,00 | 0,20 | 2,50 / 12,50 | Rẻ hơn Opus 5 |
| Claude Opus 5 / 4.8 / 4.7 | [GLOBAL] | 5,00 | 25,00 | 6,25 / 10,00 | 0,50 | 2,50 / 12,50 | |
| Claude Opus 4.6 | [SG] | 5,50 | 27,50 | 6,875 / 11,00 | 0,55 | 2,75 / 13,75 | |
| Claude Opus 4.5 | [SG] | 5,50 | 27,50 | 6,875 / 11,00 | 0,55 | 2,75 / 13,75 | |
| Claude Fable 5.1 | [GLOBAL] | 10,00 | 50,00 | 12,50 / 20,00 | 0,25 | 5,00 / 25,00 | Cao nhất |

Tool: Web search 10 USD / 1.000 lượt.

### 1.3 Open-weight / partner MaaS trên Vertex AI (G1)

G2 **không** liệt kê model nào dưới đây ở `asia-southeast1` → coi là [GLOBAL] hoặc region khác. Trang giá không ghi giá theo region.

| Model | Input | Output | Cache hit | Batch in / out |
|---|---|---|---|---|
| gpt-oss-20b | 0,07 | 0,25 | 0,007 | 0,035 / 0,125 |
| gpt-oss-120b | 0,09 | 0,36 | – | 0,045 / 0,18 |
| Qwen3-Next-80B Instruct / Thinking | 0,15 | 1,20 | – | – |
| Qwen3-235B-A22B-Instruct-2507 | 0,22 | 0,88 | – | 0,11 / 0,44 |
| Qwen3-Coder-480B-A35B-Instruct | 0,22 | 1,80 | 0,022 | 0,11 / 0,90 |
| Gemma 4 26B | 0,15 | 0,60 | 0,015 | – |
| Llama 4 Scout / Maverick | 0,25 / 0,35 | 0,70 / 1,15 | – | 0,125/0,35 · 0,175/0,575 |
| Llama 3.3 70B | 0,72 | 0,72 | – | 0,36 / 0,36 |
| Mistral Small 3.1 / Medium 3 / Codestral 2 | 0,10 / 0,40 / 0,30 | 0,30 / 2,00 / 0,90 | – | – |
| DeepSeek-V4.1-Flash | 0,30 | 1,20 | 0,03 | – (trang ghi "no charge until Oct 16, 2026", không tính) |
| DeepSeek-V3.2 | 0,56 | 1,68 | 0,056 | 0,28 / 0,84 |
| MiniMax-M2 | 0,30 | 1,20 | 0,03 | – |
| Kimi-K2-Thinking | 0,60 | 2,50 | 0,06 | – |
| GLM-4.7 / GLM-5 / GLM-5.2 | 0,60 / 1,00 / 1,40 | 2,20 / 3,20 / 4,40 | 0,06 / 0,10 / 0,14 | – |
| Grok 4.1 Fast | 0,20 | 0,50 | 0,05 | – |
| Grok 4.7 | 2,00 (>200K 4,00) | 6,00 (12,00) | 0,50 | – |

### 1.4 Ảnh (tier 5, G1, G4)

**Imagen 4 / 4 Fast / 4 Ultra có "Discontinuation date: June 30, 2026"** (G4). Google khuyên chuyển sang Gemini image. Không model ảnh nào có ở `asia-southeast1` theo G2 → mọi dòng là [GLOBAL].

| Model | Giá ảnh output (/1M token) | Giá mỗi ảnh (theo chú thích G1) | Batch |
|---|---|---|---|
| Gemini 3.1 Flash-Lite Image (Nano Banana 2 Lite) | 30 | 1K: **0,034** | 50% |
| Gemini Nano Banana 2.1 | 30 | 1K: **0,034** · 2K: 0,05 · 4K: 0,113 | 50% (không có Flex) |
| Gemini 2.5 Flash Image | 30 | 1024×1024: 0,039 | 15/1M (50%) |
| Gemini 3.1 Flash Image (Nano Banana 2) | 60 (non-global 66) | 512: 0,045 · 1K: 0,067 · 2K: 0,101 · 4K: 0,15 | 50% |
| Gemini 3 Pro Image (Nano Banana Pro) | 120 | 1K/2K: 0,134 · 4K: 0,24 | 50% |
| Imagen 4 Fast / 4 / 4 Ultra (đã ngừng 30/06/2026) | – | 0,02 / 0,04 / 0,06 | – |

Ngoài giá ảnh output còn tính input text/ảnh theo giá input của từng model.

### 1.5 Embedding + rerank (G1, G3)

| Model | Có ở SG? | Đơn vị trên trang | Giá online | Giá batch |
|---|---|---|---|---|
| Gemini Embedding (`gemini-embedding-001`) | **Có** | USD / 1.000 count (input) | 0,00015 (≈ 0,15 / 1M nếu count = token) | 0,00012 |
| Embeddings for Text (text-embedding, không phải Gemini) | **Có** | USD / 1.000 count | 0,000025 | 0,00002 |
| Gemini Embedding 2 (Preview, multimodal) | Không | USD / 1M token text | 0,20 | 0,10 |
| multilingual-e5-small / -large (MaaS) | Không | USD / 1M token | 0,015 / 0,025 | 0,0075 / 0,0125 |
| **Ranking API** (rerank) | Không ghi region | USD / 1.000 query (≤ 100 tài liệu/query) | **1,00** | – |

### 1.6 Committed / provisioned (G1)

- Provisioned Throughput theo GSU (Hourly): Global 7,14 (cam kết 1 tuần) · 3,699 (1 tháng) · 3,288 (3 tháng) · 2,740 (1 năm). Non-global: 7,854 · 4,068 · 3,616 · 3,014.
- Flexible Savings Plans (cam kết theo chi tiêu) áp dụng cho các sản phẩm đủ điều kiện. Ranking API: FSP 1 năm 0,90, 3 năm 0,80 / 1.000 query.

---

## 2. AWS – Amazon Bedrock (`ap-southeast-1`)

Quy tắc chung (A1, A2): Global CRIS = định tuyến toàn cầu; Geo CRIS (APAC) = trong vùng APAC; In-Region = chỉ Singapore. Priority = +75%; Flex và Batch = −50%. Model OpenAI: In-Region/Geo CRIS = Global +10%.

### 2.1 Claude trên Bedrock (A1, region Singapore)

Model card (A2): ở `ap-southeast-1` mọi Claude 4.5+ **chỉ có Global CRIS**, trừ **Claude Sonnet 5 có In-Region** ở Singapore.

| Model (ID) | Endpoint từ SG | Input | Output | Cache write 5m / 1h | Cache read | Batch in / out |
|---|---|---|---|---|---|---|
| Claude Haiku 5.5 (`global.anthropic.claude-haiku-5-5`) | [GLOBAL] | 0,10 | 0,50 | 0,125 / 0,20 | 0,01 | N/A |
| Claude Haiku 5.5 – Long Context (>100K) | [GLOBAL] | 0,50 | 2,50 | 0,625 / 1,00 | 0,05 | N/A |
| Claude Haiku 4.5 | [GLOBAL] | 1,00 | 5,00 | 1,25 / 2,00 | 0,10 | 0,50 / 2,50 |
| Claude Sonnet 5.5 (`global.anthropic.claude-sonnet-5-5`) | [GLOBAL] | 2,00 | 10,00 | 2,50 / 4,00 | 0,10 | N/A |
| **Claude Sonnet 5** (`anthropic.claude-sonnet-5`) | **[SG] In-Region** | **2,20** | **11,00** | 2,75 / 4,40 | 0,22 | N/A |
| Claude Sonnet 5 | [GLOBAL] | 2,00 | 10,00 | 2,50 / 4,00 | 0,20 | N/A |
| Claude Sonnet 4.6 / 4.5 | [GLOBAL] | 3,00 | 15,00 | 3,75 / 6,00 | 0,30 | 1,50 / 7,50 |
| Claude Opus 5.5 (`global.anthropic.claude-opus-5-5`) | [GLOBAL] | 4,00 | 20,00 | 5,00 / 8,00 | 0,20 | N/A |
| Claude Opus 5 / 4.8 / 4.7 / 4.6 / 4.5 | [GLOBAL] | 5,00 | 25,00 | 6,25 / 10,00 | 0,50 | Opus 5, 4.6, 4.5: 2,50 / 12,50 |
| Claude Fable 5.1 | [GLOBAL] | 10,00 | 50,00 | 12,50 / 20,00 | 0,25 | N/A |
| Claude Sonnet 4 (thế hệ cũ) | [SG] Geo APAC | 3,00 | 15,00 | 3,75 / – | 0,30 | 1,50 / 7,50 |

**Reserved Tier** (Claude, A1, giá theo giờ cho mỗi 1K TPM): Global CRIS – Haiku 4.5: 0,06 input / 0,30 output (1 tháng), 0,054 / 0,27 (3 tháng); Sonnet 4.6 và 4.5: 0,18 / 0,90 (1 tháng); Opus 4.6 và 4.5: 0,30 / 1,50 (1 tháng). Geo/In-Region: +10%. Claude 5.x chưa có Reserved.

### 2.2 Amazon Nova (A1, region Singapore)

| Model (ID) | Endpoint từ SG | Input | Output | Cache read | Batch / Flex |
|---|---|---|---|---|---|
| Nova Micro (`amazon.nova-micro-v1:0`) | [SG] Geo APAC | **0,047** | **0,188** | rẻ hơn 75% so với input | 0,0235 / 0,094 |
| Nova Lite (`apac.amazon.nova-lite-v1:0`) | [SG] Geo APAC | 0,081 | 0,324 | rẻ hơn 75% | 0,0405 / 0,162 |
| Nova Pro (`apac.amazon.nova-pro-v1:0`) | [SG] Geo APAC | 1,08 | 4,32 | rẻ hơn 75% | 0,54 / 2,16; Priority 1,89 / 7,56 |
| Nova 2 Lite (`global.amazon.nova-2-lite-v1:0`) | [GLOBAL] | 0,41 | 3,39 | rẻ hơn 75% | 0,205 / 1,695; Priority 0,7175 / 5,9325 |
| Nova 2 Pro (Preview) | [GLOBAL] | 1,69 | 13,56 | rẻ hơn 75% | 0,845 / 6,78 |
| Nova 2 Omni (Preview) | [GLOBAL] | 0,4 (audio 1,4) | text 3,4 · **ảnh 54,7** | rẻ hơn 75% | 0,2 / 1,7 |
| Nova Premier | Không có ở SG | – | – | – | us-east-1: 2,5 / 12,5 |

Ghi chú: giá Nova 2 Lite Global khi gọi từ Singapore (0,41 / 3,39) cao hơn khi gọi từ us-east-1 (0,30 / 2,50). Đây là số trong file giá của AWS.

### 2.3 OpenAI trên Bedrock (A2, model card, Standard tier)

Ở `ap-southeast-1` các model GPT-5.4 trở lên **chỉ có Global CRIS** (A2). Giá Global CRIS = giá first-party của OpenAI.

| Model (ID) | Endpoint từ SG | Input | Cache write | Cache read | Output | Long context (>272K) in / out |
|---|---|---|---|---|---|---|
| GPT-6 Luna (`global.openai.gpt-6-luna`) | [GLOBAL] | **0,10** | 0,125 | 0,01 | **0,50** | 0,20 / 0,75 |
| GPT-5.6 Luna (`global.openai.gpt-5.6-luna`) | [GLOBAL] | 0,20 | 0,25 | 0,02 | 1,20 | 0,40 / 1,80 |
| GPT-5.6 Terra | [GLOBAL] | 2,00 | 2,50 | 0,20 | 12,00 | 4,00 / 18,00 |
| GPT-6 Sol (`global.openai.gpt-6-sol`) | [GLOBAL] | 2,00 | 2,50 | 0,20 | 10,00 | 4,00 / 15,00 |
| GPT-6.1 Sol (`global.openai.gpt-6.1-sol`) | [GLOBAL] – model card không liệt kê từng source region | **2,00** | 2,50 | 0,10 | **10,00** | 4,00 / 15,00 |
| GPT-5.6 Sol | [GLOBAL] | 4,00 | 5,00 | 0,40 | 20,00 | 8,00 / 30,00 |
| GPT-6 Astra | [GLOBAL] | 10,00 | 12,50 | 1,00 | 50,00 | 20,00 / 75,00 |
| gpt-oss-20b / 120b (`openai.gpt-oss-120b-1:0`) | **[SG] In-Region** (A2) | **KHÔNG TÌM THẤY giá SG** (A1 trả N/A cho SG) | – | – | – | [GẦN NHẤT] Sydney: 20b 0,0721 / 0,309; 120b 0,1545 / 0,618 |

Priority và Flex không hỗ trợ cho GPT-5.4 trở lên. GPT-6.1 Sol có tier "Ultrafast" giá gấp 6 lần.

### 2.4 Open-weight khác trên Bedrock

Model card (A2) ghi **In-Region ở `ap-southeast-1`** cho: DeepSeek V3.1 / V3.2, Gemma 3 (4B/12B/27B), MiniMax M2 / M2.1 / M2.5, Mistral Large 3, Devstral 2, Ministral 3B/8B/14B, Magistral Small, Kimi K2 Thinking / K2.5, Qwen3 (32B, 235B, Coder 30B/480B, Next 80B, VL 235B, Coder Next), GLM 4.7 / 4.7 Flash / 5, Nemotron, gpt-oss. Llama: **không** có ở SG.

Bảng giá A1 **không có giá cho Singapore** của các model này (ô region trả N/A; các bảng giá cố định chỉ ghi US, Mumbai, Tokyo, Jakarta, Sydney…). → **KHÔNG TÌM THẤY** giá SG. Giá region gần nhất (A1):

| Model | US (N. Virginia/Ohio/Oregon) in / out | [GẦN NHẤT] APAC in / out |
|---|---|---|
| DeepSeek v3.2 | 0,62 / 1,85 | Jakarta/Tokyo/Mumbai 0,74 / 2,22 · Sydney 0,6386 / 1,9055 |
| Qwen3 Next 80B A3B | 0,15 / 1,20 | Sydney 0,1545 / 1,236 · Tokyo 0,18 / 1,45 |
| Qwen3 235B A22B 2507 | – | Sydney 0,2266 / 0,9064 |
| Mistral Large 3 | 0,50 / 1,50 | Mumbai 0,59 / 1,76 · Tokyo 0,61 / 1,82 |
| Ministral 8B 3.0 | 0,15 / 0,15 | Mumbai 0,18 / 0,18 |
| Kimi K2.5 | 0,60 / 3,00 | Sydney 0,618 / 3,09 · Tokyo/Jakarta 0,72 / 3,60 |
| Kimi K3 | Global CRIS 3,00 / 15,00 (Global CRIS có từ SG theo A2) | – |
| GLM 5 | 1,00 / 3,20 | Sydney 1,03 / 3,30 · Tokyo/Jakarta 1,20 / 3,84 |
| GLM 5.3 | Global CRIS 1,68 / 5,28 (Global CRIS có từ SG theo A2) | – |
| MiniMax (M2 họ) | 0,30 / 1,20 | Sydney 0,309 / 1,236 |
| Gemma 3 27B | 0,23 / 0,38 | Tokyo 0,28 / 0,46 |

### 2.5 Ảnh (A1, A2)

| Model | Có ở SG? | Giá | Ghi chú |
|---|---|---|---|
| Amazon Nova Canvas | Không (us-east-1, eu-west-1, ap-northeast-1) | 1024²: 0,04 (standard) / 0,06 (premium); 2048²: 0,06 / 0,08 | **Lifecycle: Legacy, Model EOL date: September 30, 2026** → đã EOL |
| Amazon Titan Image Generator v2 | Không có giá SG; không có model card | ≤512²: 0,008 / 0,01; >1024²: 0,01 / 0,012 (us-east-1) | Kiểm tra lại tình trạng |
| Stability: Stable Image Core / SD 3.5 Large / Stable Image Ultra | Không (us-west-2) | 0,04 / 0,08 / 0,14 mỗi ảnh | |
| Nova 2 Omni (Preview) | [GLOBAL] từ SG | 54,7 / 1M token ảnh output | **KHÔNG TÌM THẤY** số token mỗi ảnh → chưa tính được giá/ảnh |

### 2.6 Embedding + rerank (A1, A2)

| Model (ID) | Có ở SG? | Giá |
|---|---|---|
| Cohere Embed Multilingual v3 (`cohere.embed-multilingual-v3`) | **[SG] In-Region** | **0,10 / 1M token**; ảnh 0,0001 / ảnh |
| Cohere Embed English v3 | [SG] In-Region | 0,10 / 1M token |
| Cohere Embed v4 (`global.cohere.embed-v4:0`) | [GLOBAL] | 0,12 / 1M token |
| Amazon Titan Text Embeddings V2 | **Mâu thuẫn**: A1 có giá SG **0,028 / 1M**; model card A2 không có dòng SG | us-east-1: 0,02 / 1M, batch 0,01 |
| Amazon Nova Multimodal Embeddings | Không (us-east-1) | 0,135 / 1M token text; batch 0,0675 |
| Amazon Rerank 1.0 | Không | **1,00 / 1.000 query** [GẦN NHẤT] Tokyo |
| Cohere Rerank 3.5 | Không | 2,00 / 1.000 query (≤100 chunk/query) [GẦN NHẤT] Tokyo |

---

## 3. Azure – Microsoft Foundry (`southeastasia`)

Loại deployment: **Global Standard** (xử lý ở bất kỳ geography nào), **Data Zone Standard** (trong data zone), **Standard/Regional** (trong geography của resource). Z3 cho biết ở `southeastasia`:
- Global Standard: GPT-4.1 (cả họ), GPT-5, 5-mini, 5-nano, 5.1, 5.2, 5.3-codex, 5.4, 5.4-mini, 5.4-nano, 5.5, **5.6-luna/sol/terra**, **6-astra, 6-luna, 6-sol, 6.1-sol**, o3, o4-mini, text-embedding-3-large/small, ada-002.
- Data Zone Standard: gpt-5.2, 5.3-codex, 5.4, **5.4-mini**, 5.6-sol, 6.1-sol, gpt-chat-latest.
- Standard (regional): chỉ text-embedding-3-large.
- Model không phải OpenAI (DeepSeek, Llama, Mistral, Grok, Kimi, Cohere, FLUX, MAI): bảng APAC của Z3 **không có cột southeastasia**.

### 3.1 OpenAI GPT (Z1; meter "Gl" = Global, "Dz" = Data Zone)

Meter Global của GPT-5.4 trở lên không có trong `southeastasia` của Z1. Giá Global trong Z1 giống nhau ở mọi region có meter (ví dụ eastus2, malaysiawest), và giống giá trên Bedrock Global CRIS.

| Model | Endpoint | Input | Cached input | Output | Ghi chú |
|---|---|---|---|---|---|
| GPT-5 nano | [GLOBAL] (meter có ở SEA) | **0,05** | 0,005 | **0,40** | |
| GPT-4.1 nano | [GLOBAL] (meter SEA) | 0,10 | 0,025 | 0,40 | Batch 0,05 / 0,20 |
| GPT-6 Luna | [GLOBAL] | **0,10** | 0,01 (cache write 0,125) | **0,50** | Flex 0,05 / 0,25. DZ ngoài SEA: 0,11 / 0,55 |
| GPT-5.6 Luna | [GLOBAL] | 0,20 | 0,02 (write 0,25) | 1,20 | |
| GPT-5.4 nano | [SG] DZ (meter SEA) | 0,24 | 0,024 | 1,50 | Global: 0,20 / 0,02 / 1,25 |
| GPT-5 mini | [GLOBAL] (meter SEA) | 0,25 | 0,025 | 2,00 | |
| GPT-4.1 mini | [GLOBAL] (meter SEA) | 0,40 | 0,10 | 1,60 | Batch 0,20 / 0,80 |
| **GPT-5.4 mini** | **[SG] DZ** (meter SEA) | **0,90** | 0,09 | **5,40** | Global: 0,75 / 0,075 / 4,50; Batch Global 0,375 / 2,25 |
| GPT-5.1 | [SG] DZ (meter SEA) | 1,50 | 0,15 | 12,00 | Batch DZ 0,75 / 6,00 |
| GPT-4.1 | [GLOBAL] (meter SEA) | 2,00 | 0,50 | 8,00 | Batch 1,00 / 4,00 |
| GPT-5.6 Terra | [GLOBAL] | 2,00 | 0,20 (write 2,50) | 12,00 | |
| GPT-6 Sol | [GLOBAL] | 2,00 | 0,20 (write 2,50) | 10,00 | Flex 1,00 / 5,00 |
| **GPT-6.1 Sol** | [GLOBAL] | **2,00** | 0,10 (write 2,50) | **10,00** | Flex 1,00 / 5,00. DZ ở SEA có trong Z3, **giá DZ cho SEA KHÔNG TÌM THẤY** (DZ eastus2: 2,20 / 11,00) |
| GPT-5.4 | [SG] DZ (meter SEA) | 3,00 (>272K 6,00) | 0,30 | 18,00 (27,00) | |
| GPT-5.6 Sol | [GLOBAL] | 4,00 | 0,40 (write 5,00) | 20,00 | DZ ở SEA có trong Z3, giá DZ SEA KHÔNG TÌM THẤY |
| GPT-5.5 | [SG] DZ (meter SEA) | 6,00 (>272K 12,00) | 0,60 | 36,00 (54,00) | Global 5,00 / 30,00 |
| GPT-6 Astra | [GLOBAL] | 10,00 | 1,00 (write 12,50) | 50,00 | Flex 5,00 / 25,00 |

Ghi chú: giá "Dz" ở meter SEA cao hơn Global 20% (ví dụ GPT-5.4 mini 0,90 so với 0,75). Ở region US/EU, DZ cao hơn Global 10%.

### 3.2 Claude trong Microsoft Foundry (C1, C2)

- Tính phí qua Azure Marketplace bằng CCU (0,01 USD/CCU). Giá token = giá Claude API (C1). Retail Prices API không có meter riêng.
- Loại deployment: chỉ **Global Standard** và **US Data Zone Standard** (+10%). **Không có** lựa chọn giữ dữ liệu ở Singapore/APAC. Sonnet 5.5 chỉ Global.

| Model | Input | Cache write 5m / 1h | Cache hit | Output | Batch |
|---|---|---|---|---|---|
| Claude Haiku 5.5 (≤100K) | 0,10 | 0,125 / 0,20 | 0,01 | 0,50 | −50% |
| Claude Sonnet 5.5 | 2,00 | 2,50 / 4,00 | 0,10 | 10,00 | −50% |
| Claude Sonnet 5 | 2,00 | 2,50 / 4,00 | 0,20 | 10,00 | −50% |
| Claude Opus 5.5 | 4,00 | 5,00 / 8,00 | 0,20 | 20,00 | −50% |
| Claude Fable 5.1 | 10,00 | 12,50 / 20,00 | 0,25 | 50,00 | −50% |

### 3.3 Model khác do Azure bán (Z1 – có meter ở SEA, nhưng Z3 không liệt kê SEA)

| Model | Input | Output | Cached |
|---|---|---|---|
| gpt-oss-120B (glbl) | 0,15 | 0,60 | – |
| DeepSeek V4.1 Flash (Glbl) | 0,30 | 1,20 | 0,006 |
| DeepSeek V3.2 (glbl / DZ) | 0,58 / 0,64 | 1,68 / 1,85 | – |
| Llama 4 Maverick 17B (glbl / regnl) | 0,25 / 0,33 | 1,00 / 1,32 | – |
| Llama 3.3 70B (glbl / regnl) | 0,71 / 0,937 | 0,71 / 0,937 | – |
| Mistral Large 3 (glbl) | 0,50 | 1,50 | – |
| Kimi K2.6 Thinking (glbl) | 0,95 | 4,00 | 0,16 |
| Grok 4.1 (Glbl) | 0,20 | 0,50 | – |
| MAI-Thinking-1 (glbl) | 2,00 | 8,00 | 0,20 |
| Cohere Command A Plus (Glbl) | 0,80 | 3,20 | – |

### 3.4 Ảnh (Z1, Z3, O1)

Z3: gpt-image-* Global Standard chỉ ở eastus2, westus3, polandcentral, swedencentral, uaenorth (gpt-image-2 Global PTU có ở australiaeast). **Không có ở SEA** → [GẦN NHẤT] Global Standard qua resource ở eastus2 hoặc westus3.

| Model | Token giá (Z1, Global) | Giá mỗi ảnh 1024×1024 (O1, cùng đơn giá token với Azure Global) |
|---|---|---|
| gpt-image-1-mini | input text 2,00; output ảnh 8,00 / 1M | low **0,005** · medium 0,011 · high 0,036 (1024×1536: 0,006 / 0,015 / 0,052) |
| gpt-image-2 | input text 5,00, ảnh 8,00; output ảnh 30,00 / 1M; batch 50% | low **0,006** · medium 0,053 · high 0,211 (1024×1536: 0,005 / 0,041 / 0,165) |
| gpt-image-1.5 | output ảnh 32,00 / 1M | low 0,009 · medium 0,034 · high 0,133 |
| FLUX 1.1 Pro (glbl) | 40 USD / 1.000 ảnh → **0,04/ảnh** (regnl 0,0528) | Z3 không liệt kê SEA |
| FLUX 2 Pro | 0,03 / megapixel đầu + 0,015 / MP thêm | Z3 không liệt kê SEA |
| MAI-Image-2.5 / 2.6 (Global, southindia gần nhất) | output ảnh 2.6: 38,00 / 1M token | **KHÔNG TÌM THẤY** số token mỗi ảnh |

### 3.5 Embedding + rerank (Z1, Z3)

| Model | Endpoint | Giá / 1M token |
|---|---|---|
| text-embedding-3-small | [GLOBAL] 0,02 · [SG] DZ 0,024 | |
| text-embedding-3-large | [GLOBAL] 0,13 · **[SG] Regional 0,172** · DZ 0,156 | Chỉ model này có Standard (regional) ở SEA |
| text-embedding-ada-002 | [GLOBAL] 0,10 · DZ 0,12 | |
| Cohere Embed v4 / Embed V5 Fast / V5 Pro (Glbl) | 0,12 / 0,08 / 0,12 | Z3 không liệt kê SEA |
| Cohere Rerank v4 Fast / Pro (Glbl) | 2,00 / 2,50 USD mỗi "1K" (Z1 ghi unitOfMeasure "1K", hiểu là 1.000 query, **chưa xác nhận**) | Z3 không liệt kê SEA |

### 3.6 Committed / provisioned (Z1)

- Provisioned Managed (PTU) ở SEA: Global 1,00 USD/PTU/giờ · Data Zone 1,20 · Regional 2,72. Có sản phẩm "Azure AI Foundry Provisioned Throughput Reservation" (giảm giá khi đặt trước tháng/năm; chưa lấy chi tiết).

---

## 4. Bảng so sánh giữa 3 cloud theo lớp tier

Giá Standard pay-as-you-go, ngữ cảnh ngắn. "Rẻ nhất có ở SG" = endpoint giữ dữ liệu ở Singapore (hoặc Geo APAC); "Rẻ nhất global" = chấp nhận Global endpoint. AAII = Artificial Analysis Intelligence Index v4.3.2 (biến thể cao nhất trên Q1/Q2).

### 4.1 Nhỏ / nhanh (tier 1–2: email, tóm tắt, hỏi đáp RAG)

| Cloud | Rẻ nhất có ở SG (in / out) | Rẻ nhất global, chất lượng tốt (in / out) | Rẻ nhất tuyệt đối (global) |
|---|---|---|---|
| GCP | Gemini 2.5 Flash 0,30 / 2,50 (AAII: không có số) | **Claude Haiku 5.5 0,10 / 0,50 (AAII 43)**; SG theo tab giá 0,11 / 0,55 (mâu thuẫn với G2) | gpt-oss-20b 0,07 / 0,25; Gemini 2.5 Flash-Lite 0,10 / 0,40 |
| AWS | **Nova Micro 0,047 / 0,188** (Geo APAC, AAII ~6, ước tính); Nova Lite 0,081 / 0,324 | **Claude Haiku 5.5 0,10 / 0,50**; GPT-6 Luna 0,10 / 0,50 (AAII 38) | Nova Micro |
| Azure | GPT-5.4 nano DZ 0,24 / 1,50 | **GPT-6 Luna 0,10 / 0,50** (Global Standard có ở SEA); Claude Haiku 5.5 0,10 / 0,50 (Foundry Global) | GPT-5 nano 0,05 / 0,40 |

### 4.2 Tầm trung (tier 2–3: viết báo cáo, phân tích bảng, code)

| Cloud | Có ở SG | Global |
|---|---|---|
| GCP | Gemini 3.5 Flash 1,65 / 9,90 (AAII 33); Sonnet 4.6 3,30 / 16,50 | Gemini 3.8 Flash 1,50 / 7,50 (AAII 41); Claude Sonnet 5.5 2,00 / 10,00 (AAII 56); DeepSeek-V4.1-Flash 0,30 / 1,20 (AAII 39, region chưa xác nhận) |
| AWS | **Claude Sonnet 5 In-Region 2,20 / 11,00**; Nova Pro 1,08 / 4,32 (Geo APAC) | GPT-5.6 Luna 0,20 / 1,20 (AAII 37); Claude Sonnet 5.5 2,00 / 10,00; GPT-6 Sol 2,00 / 10,00 (AAII 48) |
| Azure | GPT-5.4 mini DZ 0,90 / 5,40; GPT-5.1 DZ 1,50 / 12,00 | GPT-5.6 Luna 0,20 / 1,20; GPT-6 Sol 2,00 / 10,00; Claude Sonnet 5.5 2,00 / 10,00 |

### 4.3 Frontier (tier 4: agent nhiều bước; model tham chiếu H8)

| Cloud | Có ở SG | Global |
|---|---|---|
| GCP | Claude Opus 4.6 / 4.5 5,50 / 27,50 | Claude Opus 5.5 4,00 / 20,00 (AAII 58); Gemini 4 Argon 4,00 / 20,00 (AAII 53); Gemini 3.1 Pro Preview 2,00 / 12,00 (AAII 30) |
| AWS | Không có (Opus chỉ Global CRIS ở SG) | **GPT-6.1 Sol 2,00 / 10,00 (AAII 52)**; Claude Opus 5.5 4,00 / 20,00 |
| Azure | GPT-6.1 Sol DZ ở SEA (giá KHÔNG TÌM THẤY) | **GPT-6.1 Sol 2,00 / 10,00**; Claude Opus 5.5 4,00 / 20,00 (Foundry) |

### 4.4 Ảnh (tier 5) – giá mỗi ảnh ~1 MP

| Cloud | Rẻ nhất | Có ở SG? |
|---|---|---|
| GCP | Gemini 3.1 Flash-Lite Image / Nano Banana 2.1: **0,034** (1K); batch −50% | Không (global) |
| AWS | Titan Image v2 0,008–0,012; Stable Image Core 0,04; Nova Canvas đã EOL 30/09/2026 | Không (us-east-1 / us-west-2) |
| Azure | gpt-image-1-mini low **0,005**, medium 0,011; gpt-image-2 low 0,006, medium 0,053 | Không (eastus2 / westus3) |

### 4.5 Embedding (/1M token) và rerank (/1.000 query)

| Cloud | Embedding rẻ nhất có ở SG | Rerank |
|---|---|---|
| GCP | gemini-embedding-001 0,00015 / 1.000 count; text-embedding 0,000025 / 1.000 count (đơn vị "count" cần xác nhận) | Ranking API 1,00 |
| AWS | Cohere Embed Multilingual v3 **0,10** (In-Region SG); Titan V2 0,028 (giá SG có nhưng availability mâu thuẫn) | Amazon Rerank 1.0 1,00 (Tokyo); Cohere Rerank 3.5 2,00 (Tokyo) |
| Azure | text-embedding-3-small DZ **0,024** (Global 0,02); 3-large Regional 0,172 | Cohere Rerank v4 Fast 2,00 (SEA không liệt kê) |

---

## 5. Chất lượng và độ trễ

Nguồn: Q1 (leaderboard) và Q2 (trang từng model), truy cập 2026-10-16. Artificial Analysis Intelligence Index **v4.3.2** gồm 10 bài: AA-Briefcase v1.1, GDPval-AA v2.1, AutomationBench-AA, Terminal-Bench 4.0, SciCode, Humanity's Last Exam, GDP.pdf, CritPt, AA-Omniscience, AA-LCR v1.1. "Latency First Chunk" của model reasoning **gồm cả thời gian thinking**, nên số lớn khi chạy mức max. Giá trong cột "Cost/task" là chi phí AA đo để chạy bộ Index, không phải đơn giá cloud. Dấu * = AA ước tính.

| Model (biến thể AA) | AAII | Output tok/s (median) | First chunk (s) | Total response (s) |
|---|---|---|---|---|
| Claude Opus 5.5 (max) | 58 | 96 | 666,7 | 671,9 |
| Claude Opus 5.5 (medium) | 51 | 88 | 17,4 | 23,1 |
| Claude Opus 5.5 (low) | 42 | 87 | 6,7 | 12,4 |
| Claude Sonnet 5.5 (max) | 56 | 135 | 379,6 | 383,3 |
| Claude Sonnet 5.5 (medium / low) | 41 / 36 | 115 / 113 | 3,0 / 1,35 | 7,3 / 5,8 |
| Claude Fable 5.1 (max) | 53 | 71 | 258,5 | 265,5 |
| Gemini 4 Argon (high) | 53 | – | – | – |
| GPT-6 Astra (max) | 53 | 54 | 252,9 | 262,3 |
| GPT-6.1 Sol (max) | 52 | 54 | 271,7 | 281,0 |
| GPT-6.1 Sol (medium / low) | 48 / 42 | 50 / 48 | 4,2 / 3,1 | 14,3 / 13,5 |
| GPT-6 Sol (max) | 48 | 107,8 | – | – |
| GPT-5.6 Sol (max) | 47 | 94,8 | – | – |
| GLM-5.3 (max) | 45 | 67 | 3,1 | 40,5 |
| Kimi K3 (max) | 44 | 43 | 3,75 | 61,3 |
| **Claude Haiku 5.5 (max)** | **43** | **238** | 334,5 | 336,6 |
| Claude Haiku 5.5 (high / medium / low) | 38 / 34 / 29 | 182 / 188 / 183 | 19,8 / 8,5 / 6,3 | 22,5 / 11,1 / 9,1 |
| GPT-5.6 Terra (max) | 42 | 134 | 118,3 | 122,0 |
| Gemini 3.8 Flash (high) | 41 | 147 | 24,4 | 27,8 |
| DeepSeek V4.1 Flash (max) | 39 | 179 | 1,15 | 15,1 |
| DeepSeek V4.1 Flash (non-reasoning) | 25 | 192 | 1,16 | 3,8 |
| GPT-6 Luna (max) | 38 | 120 | 97,0 | 101,1 |
| GPT-6 Luna (low / non-reasoning) | 22 / 18 | 120 / 112 | 2,2 / 0,95 | 6,3 / 5,4 |
| GPT-5.6 Luna (max) | 37 | 123,4 | – | – |
| Gemini 3.5 Flash (high) | 33 | 205,2 | – | – |
| Gemini 3.1 Pro Preview | 30 | 142 | 16,9 | 20,5 |
| Gemini 3.5 Flash-Lite | 22 | 446 | 7,0 | 8,1 |
| Gemini 3.1 Flash-Lite | 16 | 384,8 | – | – |
| Nova 2.0 Pro Preview (medium) | 14* | 134 | 11,3 | 29,9 |
| Nova 2.0 Lite (high / non-reasoning) | 13* / 9* | 183 / 178 | 16,8 / 1,1 | 30,5 / 3,9 |
| gpt-oss-120b (high) | 12 | 213 | 0,84 | 12,6 |
| Qwen3-235B-A22B-2507 | 12* | 46 | – | – |
| Qwen3 Next 80B A3B | 11* | 160 | 0,68 | 16,3 |
| Mistral Large 3 | 9 | 80 | – | – |
| Llama 4 Maverick | 9 | 56 | 1,11 | 10,1 |
| Nova Lite / Nova Pro | 7* / 7* | 169,5 / 129,4 | – | – |
| Nova Micro | 6* | 322 | 0,84 | 2,4 |

Nhận xét cho routing: với cùng giá 0,10 / 0,50, Claude Haiku 5.5 (AAII 43 ở max, 29–38 ở low–high) cao hơn GPT-6 Luna (38 / 22) và nhanh hơn (≈ 185–238 tok/s). Ở tier 1, chạy mức reasoning low hoặc non-reasoning để first chunk < 10 s (H6). Chỉ số tool-use/agent chuyên biệt (τ²-bench, SWE-bench Verified, MMLU-Pro, GPQA) từ model card của vendor: **chưa thu thập** (xem mục 7).

---

## 6. Quản trị dữ liệu và private endpoint

| Hạng mục | GCP Vertex AI | AWS Bedrock | Azure Foundry |
|---|---|---|---|
| Không dùng dữ liệu để train | "Google won't use your data to train or fine-tune any AI/ML models without your prior permission or instruction." – https://docs.cloud.google.com/vertex-ai/generative-ai/docs/data-governance (cập nhật 2026-10-15) | Model provider không truy cập được Model Deployment Account, log, prompt và completion – https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html | Prompt, completion, embedding "are NOT used to train any generative AI foundation models without your permission" và không chia sẻ cho OpenAI – https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/data-privacy (ms.date 2026-05-18) |
| Lưu dữ liệu mặc định | Cache trong bộ nhớ và durable cache bật mặc định, xóa trong ≤ 24 giờ; có thể ghi log prompt để phát hiện lạm dụng | Theo `data_retention_mode`. Model OpenAI (trừ gpt-oss): traffic bị classifier đánh dấu lưu ≤ 30 ngày. Claude Fable 5/5.1: mọi traffic lưu ≤ 30 ngày, có thể AWS review – https://docs.aws.amazon.com/bedrock/latest/userguide/abuse-detection.html | Abuse monitoring lưu prompt/completion bị đánh dấu trong geography của resource để human review (trang không ghi số ngày); Responses API, Assistants, Stored completions lưu dữ liệu tới khi khách xóa |
| Zero data retention | Tắt durable cache (`retentionConfig: EPHEMERAL`) hoặc `disableCache: true`; xin ngoại lệ abuse monitoring. **Không tắt được**: Grounding with Google Search (lưu 3 ngày), Google Maps (30 ngày) | `data_retention_mode: none` cho account/project trong từng region, ép bằng SCP – https://docs.aws.amazon.com/bedrock/latest/userguide/data-retention.html. ZDR cho Claude do Anthropic quản lý | Đăng ký "modified abuse monitoring" (Limited Access); kiểm tra `ContentLogging=false` – https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/abuse-monitoring |
| Nơi xử lý khi dùng global | Global endpoint: xử lý ở bất kỳ đâu Google có model. Regional `asia-southeast1` chỉ có cho Gemini 3.5 Flash, 2.5 Flash, Claude Sonnet/Opus 4.5–4.6, embedding | Global CRIS định tuyến mọi region; dữ liệu bị lưu (nếu có) nằm ở region đích – https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html | Global: xử lý ở bất kỳ geography nào; DataZone: trong data zone; dữ liệu lưu trữ vẫn ở geography của resource |
| Claude qua cloud | Vertex: hợp đồng Google; dữ liệu trong Google Cloud | Bedrock: model provider không truy cập prompt | Foundry: "Anthropic acts as an independent processor for Microsoft… subject to Anthropic's data use terms"; hosted on Azure thì prompt ở lại Azure, chỉ metadata và nội dung bị safety system đánh dấu ra Anthropic (C2) |
| Private endpoint | Private Service Connect cho Google APIs (`aiplatform.googleapis.com`) – https://docs.cloud.google.com/vpc/docs/configure-private-service-connect-apis ; PSC cho Vertex – https://docs.cloud.google.com/vertex-ai/docs/general/psc-endpoints ; kết hợp VPC Service Controls | AWS PrivateLink (interface VPC endpoint) cho Bedrock – https://docs.aws.amazon.com/bedrock/latest/userguide/vpc-interface-endpoints.html , https://docs.aws.amazon.com/bedrock/latest/userguide/usingVPC.html | Private Endpoint (Private Link) cho Foundry resource – https://learn.microsoft.com/en-us/azure/foundry/how-to/configure-private-link ; Claude in Foundry hỗ trợ VNet (C2) |

---

## 7. Gaps (chưa tìm thấy hoặc cần xác nhận)

1. **AWS – giá Singapore cho open-weight** (DeepSeek, Qwen, Mistral, MiniMax, Kimi K2.x, GLM 4.7/5, Gemma, gpt-oss): model card ghi có In-Region ở `ap-southeast-1`, nhưng trang giá A1 không có giá SG. Đã ghi giá Sydney/Tokyo/Mumbai thay thế. Kiểm tra lại bằng AWS Pricing Calculator (https://calculator.aws/) chọn ap-southeast-1.
2. **AWS – Titan Text Embeddings V2 ở SG**: A1 có giá 0,028; model card không có dòng SG. Cần thử gọi API hoặc xem console.
3. **GCP – Claude Haiku 5.5 ở `asia-southeast1`**: tab giá có (0,11 / 0,55), trang Locations (G2) không có. Cần xác nhận bằng console.
4. **GCP – đơn vị "count" của embedding** (`gemini-embedding-001`, Embeddings for Text): trang ghi "/1,000 count", không ghi rõ token hay ký tự.
5. **GCP – khả dụng ở SG của model MaaS** (gpt-oss, Qwen, DeepSeek V4.1 Flash, Llama, Mistral): G2 không liệt kê SG; chưa rõ region thực tế (có thể chỉ global hoặc us-central1).
6. **GCP – PSC với Global endpoint**: chưa xác nhận gọi global endpoint của Vertex qua PSC được hay không.
7. **Azure – giá Data Zone cho GPT-6.1 Sol và GPT-5.6 Sol ở SEA**: Z3 ghi có DZ ở SEA, Z1 không có meter → KHÔNG TÌM THẤY. Nếu cần ở lại vùng, phải hỏi Microsoft hoặc Pricing Calculator.
8. **Azure – model không phải OpenAI ở SEA**: Z1 có meter, Z3 không có cột southeastasia → chưa rõ deploy được không.
9. **Azure – đơn vị Cohere Rerank v4** ("1K"): chưa xác nhận là 1.000 query.
10. **Azure – Claude trong Foundry tạo từ resource ở SEA**: C2 chỉ nói Global Standard / US Data Zone; chưa thấy danh sách region resource được hỗ trợ.
11. **Ảnh**: không cloud nào có model ảnh ở Singapore. Bedrock Nova 2 Omni và Azure MAI-Image: KHÔNG TÌM THẤY số token mỗi ảnh → chưa ra giá mỗi ảnh. Imagen 4 (ngừng 30/06/2026) và Nova Canvas (EOL 30/09/2026) **không dùng được** cho thiết kế mới.
12. **Benchmark của vendor** (MMLU-Pro, GPQA Diamond, SWE-bench Verified, τ²-bench) cho từng model: chưa thu thập. **LMArena**: trang bị chặn bởi Cloudflare khi truy cập tự động (https://lmarena.ai/leaderboard/text) → chưa có điểm Elo.
13. **TTFT cho region Singapore**: số của Artificial Analysis đo qua endpoint mặc định của nhà cung cấp, không phải từ Singapore. Cần đo thực tế từ VPC Singapore (Global vs Regional).
14. **AA chưa có số** cho Gemini 2.5 Flash/Flash-Lite (phiên bản hiện tại trên leaderboard), Gemini 4 Argon (tốc độ), Claude Sonnet 5, Nova Premier.
15. **Reserved / PTU**: chưa lấy giá đặt trước tháng/năm của Azure PTU Reservation; chưa có giá Reserved cho Claude 5.x trên Bedrock.
