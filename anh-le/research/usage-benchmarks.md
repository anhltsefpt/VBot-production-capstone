# Usage benchmarks cho trợ lý AI doanh nghiệp (sizing VBot)

> Ngày tổng hợp: 2026-10-16. Mục đích: lấy số liệu thực tế (telemetry, báo cáo vendor, paper, đánh giá của chính phủ) để ước lượng tải cho VBot — 2.000 DAU văn phòng tại Việt Nam, Thứ 2–Thứ 6, 8:00–18:00, 22 ngày làm việc/tháng.
>
> Quy ước: mỗi con số có **giá trị — định nghĩa — nguồn — URL — ngày — độ tin cậy**. Những dòng ghi "**(suy ra)**" là phép tính của người tổng hợp từ số liệu gốc, không phải số do nguồn công bố. Không có số nào được bịa; chỗ không có dữ liệu được đánh dấu **GAP**.
>
> Thang độ tin cậy: **A** = telemetry/primary có phương pháp rõ; **B** = primary nhưng là khảo sát tự báo cáo, hoặc số đọc từ biểu đồ; **C** = vendor marketing / thứ cấp / phương pháp không rõ.

---

## 1. Số request/message/prompt trên mỗi người dùng

### 1.1 Microsoft 365 Copilot

| # | Giá trị | Định nghĩa chính xác | Nguồn | Ngày | Tin cậy |
|---|---|---|---|---|---|
| 1 | **1,14 Copilot actions / user / working day** (72 actions / user trong 63 ngày làm việc) | "M365 Copilot actions" theo Microsoft Copilot Dashboard, chia cho **tổng số license** (gồm cả người không dùng); không trừ nghỉ phép. Action ≠ prompt (một action có thể là một lần bấm Summarise trong Teams/Outlook). | UK Department for Business and Trade (DBT), *Microsoft 365 Copilot pilot: DBT evaluation report* — https://assets.publishing.service.gov.uk/media/68adbe409e1cebdd2c96a19d/dbt-microsoft-365-copilot-evaluation.pdf | 28/08/2025 (pilot 10–12/2024, 1.000 license) | A |
| 2 | DAU trung bình **30%** số license (ngày làm việc), **21%** tính cả cuối tuần; đỉnh **50%** (8/10/2024). WAU trung bình **64%** (đỉnh 68%) | "Active user" theo dashboard Microsoft | DBT report (như trên) | 28/08/2025 | A |
| 3 | **≈ 3,8 actions / active user / ngày làm việc** **(suy ra)** | = 1,14 ÷ 0,30. Ước lượng thô vì 1,14 chia trên toàn bộ license | Tính từ #1, #2 | — | B |
| 4 | Diary 1 tuần: **1.424 use case / 300 nhật ký ≈ 4,7 use case / người / tuần** **(suy ra)** | Số "use case" người dùng tự ghi trong 1 tuần (11/2024); một use case có thể gồm nhiều prompt. Mẫu tự chọn (tỷ lệ phản hồi 32%) | DBT report, Table 1 | 28/08/2025 | B |
| 5 | **39%** dùng *nhiều lần mỗi ngày*; thêm **43%** dùng ít nhất nhiều lần mỗi tuần; 2% không dùng | Khảo sát 7.115 người; trial 20.000 công chức, 30/09–31/12/2024 | UK GDS, *Microsoft 365 Copilot Experiment: Cross-Government Findings Report* — https://www.gov.uk/government/publications/microsoft-365-copilot-experiment-cross-government-findings-report/microsoft-365-copilot-experiment-cross-government-findings-report-html | 02/06/2025 | B |
| 6 | Theo app: **34%** dùng Copilot hằng ngày trong Teams, **33%** trong Outlook, **25%** trong Word (+43% hằng tuần); >55% chưa từng dùng OneNote/Business Chat | Tự báo cáo | UK GDS (như trên) | 02/06/2025 | B |
| 7 | Adoption cao nhất theo app: Teams **71%**, PowerPoint **24%**, Excel **23%** | Telemetry adoption (14.500 user ẩn danh) | UK GDS (như trên) | 02/06/2025 | A |
| 8 | Treasury (Úc): đa số dùng **2–3 lần/tuần hoặc ít hơn**; ~22% dùng 4–5 lần/tuần | Khảo sát 218 nhân sự, 20/05–23/08/2024 | Australian Centre for Evaluation, *Evaluation of a trial of generative AI (Copilot) in the Treasury — Summary report* — https://evaluation.treasury.gov.au/sites/evaluation.treasury.gov.au/files/2025-02/evaluation-generative-artificial-intelligence-summary.pdf | 02/2025 | B |
| 9 | DTA (Úc, toàn chính phủ): khoảng **1/3** dùng hằng ngày; **46%** "a few times a week"; **21%** "a few times a month" | Khảo sát; gần 6.000 license, 56 cơ quan, 01–06/2024 | Digital Transformation Agency — https://digital.gov.au/initiatives/copilot-trial/summary-evaluation-findings/cts-evaluation-findings (trang primary timeout khi truy cập; số lấy qua tóm tắt thứ cấp, ví dụ https://the-decoder.com/australian-government-pilots-microsoft-copilot-with-mixed-results/) | 2024 (trial 01–06/2024) | C (chưa đối chiếu được trang gốc) |
| 10 | Người được cấp Copilot trung vị dùng Copilot trong **39% số tuần** (tháng 4–6); >90% dùng ít nhất một lần trong 6 tháng | Telemetry *có/không dùng* theo tuần, **không** có số prompt ("We do not observe any information about prompts") | Dillon et al. (Microsoft Research), *Shifting Work Patterns with Generative AI* — https://arxiv.org/abs/2504.11436 | 04/2025 (RCT 66 firm, 7.137 người, 09/2023–10/2024) | A |

### 1.2 ChatGPT (Enterprise và consumer)

| # | Giá trị | Định nghĩa | Nguồn | Ngày | Tin cậy |
|---|---|---|---|---|---|
| 11 | Weekly Enterprise messages tăng **~8x** từ 11/2024; **average worker gửi nhiều hơn 30%** messages | Tổng message ChatGPT Enterprise; **không công bố số tuyệt đối/user** | OpenAI, *The state of enterprise AI — 2025 report* — https://cdn.openai.com/pdf/7ef17d82-96bf-4dd1-9df2-228f7f377a29/the-state-of-enterprise-ai_2025-report.pdf | 08/12/2025 | A (nhưng chỉ tương đối) |
| 12 | Frontier worker (P95 cường độ dùng) gửi **6x** messages so với median; coding **17x**, writing & communication **11x**, analysis & calculations **10x**, how-to **9x**, information gathering **9x**, creative media **8x**; frontier firm **2x** messages/seat và **7x** messages tới GPTs | Tỷ lệ P95/median trong dữ liệu enterprise | OpenAI (như trên), tr. 13–15 | 08/12/2025 | A |
| 13 | ~**20%** Enterprise messages đi qua Custom GPT hoặc Project | Tỷ lệ message | OpenAI (như trên) | 08/12/2025 | A |
| 14 | Consumer: **2,627 tỷ message/ngày** (06/2025), trong đó **716 triệu (27%)** liên quan công việc; **18 tỷ message/tuần** từ **700 triệu WAU** (07/2025) | Chỉ consumer plans (Free/Plus/Pro), không gồm Enterprise | Chatterji et al. (OpenAI/NBER), *How People Use ChatGPT*, NBER WP 34255 — https://www.nber.org/papers/w34255 ; PDF: https://cdn.openai.com/pdf/a253471f-8260-40c6-a2cc-aa93fe9f142e/economic-research-chatgpt-usage-paper.pdf | 15/09/2025 | A |
| 15 | **≈ 3,7 message / WAU / ngày**; ≈ 26 message / WAU / tuần **(suy ra)** | = 18 tỷ ÷ 700 triệu ÷ 7. Tính trên *weekly* user, toàn cầu, phần lớn phi công việc | Tính từ #14 | — | B |

### 1.3 Các sản phẩm khác

| # | Giá trị | Định nghĩa | Nguồn | Ngày | Tin cậy |
|---|---|---|---|---|---|
| 16 | Trung bình **5,09 prompt/conversation**; median **2**; P95 **18**. Trung bình **36 conversation/user** (median 12, P95 144) — **không nêu cửa sổ thời gian** | Browser telemetry trên nhiều AI app trong doanh nghiệp | LayerX, *State of AI Usage Report 2026* — https://layerxsecurity.com/library/reports/state-of-ai-usage-report-2026/ | 2026 | C (vendor bảo mật, phương pháp không rõ) |
| 17 | "Glean Assistant users average **14 queries per day**" | Được trích nhiều nơi; **không tìm thấy nguồn primary của Glean** | Thứ cấp (ví dụ https://fourweekmba.com/gleans-4-5b-business-model-how-ex-googlers-built-the-enterprise-search-that-actually-works/) | không rõ | C — chỉ dùng tham khảo |
| 18 | Google Workspace: **>2 tỷ AI assists/tháng** cho business users | Tổng hợp; không chia theo user | Google, *Cloud Next 25* — https://blog.google/products/google-cloud/next-2025/ | 09/04/2025 | B (không tính được per-user vì không có mẫu số) |
| 19 | Claude Code: trung bình **~$13 / developer / active day**, $150–250 / developer / tháng; 90% user < $30 / active day | Chi phí token trên các enterprise deployment | Anthropic, *Claude Code docs — Manage costs effectively* — https://code.claude.com/docs/en/costs | cập nhật 04/2026 | A |
| 20 | Khuyến nghị rate limit cho org 500+ user: **10k–15k TPM/user, 0,25–0,35 RPM/user** (100–500 user: 15k–20k TPM, 0,37–0,47 RPM) | Hạn mức *mức tổ chức* giả định đồng thời thấp | Anthropic, Claude Code docs (như trên) | 2026 | A (cho workload coding agent) |

**GAP:** Không vendor nào (OpenAI, Microsoft, Google, Anthropic, Glean) công bố **số prompt tuyệt đối / active user / ngày** cho sản phẩm enterprise. Số tốt nhất là DBT (actions/license/ngày) và tỷ lệ tương đối của OpenAI. Gemini for Workspace không có số per-user công khai (chỉ có báo cáo trong Admin console của từng tổ chức: https://workspaceupdates.googleblog.com/2024/12/gemini-per-app-usage-reporting-admin-console.html).

**Phân biệt đơn vị đo:**
- *Chat turn/message*: một prompt người dùng gửi (OpenAI, LayerX).
- *Action*: một lần kích hoạt tính năng Copilot (Microsoft dashboard) — có thể là một nút bấm.
- *Use case / task*: một việc người dùng làm (DBT diary) — gồm nhiều turn (LayerX: TB 5,09 prompt/conversation).
- *Agent run*: một lần agent chạy, gồm nhiều LLM call và tool call (xem mục 3.4).
- *LLM call / API request*: đơn vị mà gateway (OpenRouter, Azure trace) đếm; 1 turn có thể sinh 1–nhiều call.

---

## 2. Cơ cấu tác vụ (task mix)

### 2.1 Office workers dùng Copilot — DBT diary study (gần với VBot nhất)

Nguồn: DBT evaluation report (URL ở #1), Chart B. Tỷ lệ % trên **1.424 use case** tự ghi trong 1 tuần (11/2024). Tin cậy **B** (tự báo cáo, mẫu tự chọn).

| Use case | % | Tier VBot tương ứng |
|---|---|---|
| Transcribing or summarising a meeting | 16,43 | T1 |
| Writing an email | 11,73 | T1 |
| Summarising written communications (e.g. emails) | 10,74 | T1 |
| Asking simple questions (alternative to internet search) | 8,71 | T1 |
| Drafting a written report or briefing | 8,01 | T2 |
| Editing written materials | 6,46 | T1/T2 |
| Checking own writing for grammar, tone or spelling | 6,25 | T1 |
| Other | 5,97 | — |
| Brainstorming ideas | 5,76 | T1 |
| Producing or editing slide decks and presentations | 5,69 | T2 |
| Searching for existing information or resources | 4,00 | T1 (RAG) |
| Data analysis | 3,37 | T3 |
| Summarising research | 3,16 | T1 |
| Generating images | 1,54 | T5 |
| Reviewing code | 1,19 | T3 |
| Scheduling | 0,98 | T4 (gần nhất) |

Gộp **(suy ra)**: T1 ≈ **73%**, T2 ≈ **14%** (drafting + slides), T3 ≈ **4,6%**, T5 ≈ **1,5%**, T4 ≈ **1%** (trial không có agent), Other ≈ 6%.

### 2.2 Các nguồn khác

| # | Giá trị | Định nghĩa | Nguồn | Ngày | Tin cậy |
|---|---|---|---|---|---|
| 21 | Work-related messages (07/2025): **Writing 40%**, Practical Guidance **24%**, Technical Help **>10%** (giảm từ 18% 07/2024) | ChatGPT consumer, chỉ message liên quan công việc; phân loại tự động | *How People Use ChatGPT* (URL #14), Fig. 8 | 15/09/2025 | A |
| 22 | Tất cả message: Practical Guidance **~29%**, Seeking Information **24%**, Writing **24%**, Multimedia **>7%** (từ 2%), Technical Help **~5%**; Computer Programming **4,2%**, Mathematical Calculation **3%**, **Data Analysis 0,4%** | Như trên | Như trên | 15/09/2025 | A |
| 23 | Writing: **2/3** là sửa/biến đổi văn bản có sẵn (edit/critique, translation, summary) thay vì viết mới | Như trên | Như trên | 15/09/2025 | A |
| 24 | Intent: Asking **49%**, Doing **40%**, Expressing **11%**; trong work messages: Doing **~56%**, Asking 35% | Như trên | Như trên | 15/09/2025 | A |
| 25 | Claude.ai: Computer & Mathematical **34%** (11/2025, đỉnh 40% 03/2025) → **35%** (02/2026); 1P API: **46%** (11/2025) | Phân loại O*NET trên mẫu 1 triệu transcript | Anthropic, *Economic Index report: Economic Primitives* — https://www.anthropic.com/research/anthropic-economic-index-january-2026-report (PDF: https://www-cdn.anthropic.com/096d94c1a91c6480806d8f24b2344c7e2a4bc666.pdf); *Learning curves* — https://www.anthropic.com/research/economic-index-march-2026-report | 15/01/2026; 24/03/2026 | A |
| 26 | 1P API: Office & Administrative Support **13%** (11/2025, tăng 3pp), **15%** vs 8% trên Claude.ai; API **74%** work-related, **~75%** automation; Claude.ai: directive 32%, automation 41–45% | Như trên | Anthropic Jan 2026 report | 15/01/2026 | A |
| 27 | API: **77%** automation-dominant; Claude.ai directive tăng 27% → **39%** (12/2024 → 08/2025) | | Anthropic, *Economic Index September 2025 report* — https://www.anthropic.com/research/anthropic-economic-index-september-2025-report | 15/09/2025 | A |
| 28 | Thời gian người dùng với AI: Claude.ai **15 phút** vs API **5 phút** / task; task success **67%** vs **49%** | Claude tự đánh giá | Anthropic Jan 2026 report | 15/01/2026 | B |
| 29 | Top API use cases: In-app Assistant & Search, Coding & Developer Tools, Customer Support, Agentic Workflow Automation, Data Analysis/Summarization/Extraction; customer service + content generation ≈ **20%** API activity | | OpenAI state of enterprise AI 2025 (URL #11) | 08/12/2025 | B (chỉ xếp hạng) |
| 30 | Bing Copilot: hoạt động phổ biến nhất của user là **gathering information** và **writing**; AI thực hiện chủ yếu providing information, writing, teaching, advising | 200.000 conversation US, 01–09/2024 | Tomlinson et al. (Microsoft), *Working with AI* — https://arxiv.org/abs/2507.07935 | 07/2025 | A (định tính, không có % gộp đơn giản) |
| 31 | Copilot consumer: "Work and Career" là chủ đề hàng đầu trên desktop trong **8h–17h**; programming tăng vọt vào ngày thường | 37,5 triệu conversation, 01–09/2025, **loại trừ** enterprise | Microsoft AI, *It's About Time: The Copilot Usage Report 2025* — https://news.microsoft.com/source/emea/?p=220088 | 12/2025 | B |

**GAP:** Không có nguồn nào công bố tỷ lệ **agent run** (multi-step, đọc/ghi Jira/Confluence/Notion) trên tổng tương tác của trợ lý văn phòng. Chỉ có tín hiệu gián tiếp: API automation 75–77%, Office/Admin trên API 13–15%, Custom GPT/Projects 20% message.

---

## 3. Token mỗi request

### 3.1 Telemetry tổng quát

| # | Giá trị | Định nghĩa | Nguồn | Ngày | Tin cậy |
|---|---|---|---|---|---|
| 32 | Prompt TB **~1.500 → ~6.000+ token/request** (đầu 2024 → cuối 2025); completion TB **~150 → ~400 token/request**; programming prompt thường **>20.000 token** (3–4x prompt thông thường); programming >50% token cuối 2025; reasoning model >50% token | Trung bình trên toàn bộ request qua OpenRouter (đọc từ biểu đồ) | Aubakirova et al. (OpenRouter, a16z), *State of AI: An Empirical 100 Trillion Token Study* — https://arxiv.org/abs/2601.10088 ; https://openrouter.ai/state-of-ai | 12/2025 | B (dân số developer/API, không phải văn phòng; số đọc từ chart) |
| 33 | Azure **conversation** trace (1 tuần, 10–19/05/2024, 27,3 triệu request): context TB **1.632**, median **932**, P90 3.845, P99 6.681; generated TB **106**, median **41**, P90 342 **(suy ra từ dữ liệu gốc)** | `ContextTokens`, `GeneratedTokens` mỗi invocation | Azure Public Dataset, *Azure LLM inference trace 2024* (DynamoLLM, HPCA 2025) — https://github.com/Azure/AzurePublicDataset/blob/master/AzureLLMInferenceDataset2024.md | 2024 (trace) / 2025 (paper) | A (dữ liệu gốc; tác giả tự tính, mẫu 2% cho percentile) |
| 34 | Azure **code** trace (16,8 triệu request): context TB **2.511**, median **1.930**, P90 6.234; generated TB **23**, median **8** **(suy ra)** | Chủ yếu code completion (output ngắn) | Như trên | 2024 | A |
| 35 | Azure trace 11/2023: coding median prompt **1.500** / output **13**; conversation median prompt **1.020** / output **129** | | Patel et al., *Splitwise* — https://arxiv.org/abs/2311.18677 | 11/2023 | A (đã cũ) |
| 36 | Mỗi 1% tăng input length ↔ **0,38%** tăng output length (API) | Hồi quy trên 1P API | Anthropic Sep 2025 report (URL #27) | 15/09/2025 | A |

### 3.2 Coding / sandbox

- Claude Code `/usage` ví dụ trong docs: một session 1,2k input, 5,3k output, **940k cache read**, 50k cache write — minh họa rằng agent coding đọc lại context rất lớn qua cache (https://code.claude.com/docs/en/costs). Tin cậy A (ví dụ minh họa, không phải trung bình).
- Docs cũng nêu "one debugging session can consume more than a day of chat" và thinking budget "can be tens of thousands of tokens per request".

### 3.3 RAG, tóm tắt email, sinh tài liệu

**GAP:** Không tìm thấy telemetry công khai về (a) kích thước context RAG thực tế trong trợ lý nội bộ, (b) token cho tóm tắt email, (c) token output khi sinh DOCX/XLSX/PPTX. Proxy tốt nhất: Azure conversation trace (#33) và OpenRouter (#32). Số ở mục "Implications" là giả định thiết kế.

### 3.4 Agent: số bước và token mỗi run

| # | Giá trị | Định nghĩa | Nguồn | Ngày | Tin cậy |
|---|---|---|---|---|---|
| 37 | Agent dùng **~4x** token so với chat; multi-agent **~15x**; token usage giải thích **80%** phương sai hiệu năng | Hệ Research của Anthropic | Anthropic Engineering, *How we built our multi-agent research system* — https://www.anthropic.com/engineering/multi-agent-research-system | 13/06/2025 | A |
| 38 | Fact-finding đơn giản: **1 agent, 3–10 tool calls**; so sánh trực tiếp: **2–4 subagent × 10–15 calls**; nghiên cứu phức tạp: **>10 subagent** | Quy tắc scale effort trong prompt | Như trên | 13/06/2025 | A |
| 39 | SWE-agent (GPT-4): TB **14,71 turns**/trajectory, median **12** (full SWE-bench); Claude 3 Opus trên Lite: TB 12,71, median 13 | 1 turn = 1 LLM call + 1 action | Yang et al., *SWE-agent* — https://arxiv.org/abs/2405.15793 | 05/2024 | A |
| 40 | SWE-agent ~**130.846 token/run** (Claude); OpenHands + Claude Sonnet 4 **20,5 rounds, ~219.299 token/run** | Benchmark lọc false-positive lỗ hổng, không phải task văn phòng | https://arxiv.org/abs/2601.22952 | 01/2026 | B (task khác domain) |
| 41 | Agent teams dùng **~7x** token so với session thường (plan mode) | | Claude Code docs (URL #19) | 2026 | A |

---

## 4. Tập trung giờ cao điểm

| # | Giá trị | Định nghĩa | Nguồn | Ngày | Tin cậy |
|---|---|---|---|---|---|
| 42 | Azure **code** trace, ngày thường (Thứ 2–5): giờ cao nhất chiếm **9,3–9,7%** lưu lượng 24h; peak/mean giờ **2,2–2,3x**; cửa sổ 10 giờ liên tiếp bận nhất chiếm **72–75%**; cuối tuần chỉ còn ~30% lưu lượng ngày thường **(suy ra từ dữ liệu gốc, giờ UTC)** | Đếm request theo giờ | Azure LLM inference trace 2024 (URL #33) | 05/2024 | A (dữ liệu gốc; người dùng có thể trải nhiều múi giờ nên **đánh giá thấp** độ tập trung so với một văn phòng một múi giờ) |
| 43 | Azure **conversation** trace: giờ cao nhất **5,2–5,8%** / 24h; peak/mean 1,25–1,39x; top-10h ~48% **(suy ra)** | Như trên | Như trên | 05/2024 | A (traffic đa múi giờ, gần như phẳng — không đại diện văn phòng một múi giờ) |
| 44 | Conversation service của ChatGPT/GPT-4 trên Azure "peak during weekdays and diminish during weekends", đỉnh trong giờ làm việc; API service thì bursty, không chu kỳ | | Wang et al., *BurstGPT* — https://arxiv.org/abs/2401.17644 | 2024–2025 | A (định tính) |
| 45 | DBT: ngày đỉnh 50% DAU vs trung bình 30% → **peak-day factor ~1,67x** **(suy ra)**; cuối tuần ~1% | | DBT report (URL #1) | 28/08/2025 | A |
| 46 | Copilot consumer desktop: chủ đề công việc chiếm ưu thế đúng **8h–17h** | | Microsoft Copilot Usage Report 2025 (URL #31) | 12/2025 | B |

**GAP:** Không có nguồn primary công bố "% lưu lượng hằng ngày trong giờ cao nhất" cho trợ lý văn phòng **một múi giờ**. (Một số trang web cho rằng "business apps often see 10–20% of daily requests in the busiest hour", nhưng nguồn là nội dung tự sinh, không có dữ liệu — không dùng.)

---

## 5. Tần suất sinh ảnh và code interpreter / sandbox

| # | Giá trị | Định nghĩa | Nguồn | Ngày | Tin cậy |
|---|---|---|---|---|---|
| 47 | **>700 triệu ảnh** do **>130 triệu user** tạo trong ~1 tuần sau khi ra mắt image gen (25/03/2025) → **≈ 5,4 ảnh/user-đã-dùng/tuần** **(suy ra)** | Consumer, tuần ra mắt (đỉnh bất thường) | Brad Lightcap (COO OpenAI) trên X, đưa tin bởi TechCrunch/The Decoder — https://the-decoder.com/chatgpts-image-generation-explodes-with-700m-creations-in-first-week/ | 03–04/2025 | B |
| 48 | Multimedia (chủ yếu "Create an Image") **~7%** consumer messages (từ 2%) | | *How People Use ChatGPT* (URL #14) | 15/09/2025 | A |
| 49 | DBT: "Generating images" **1,54%** use case; slides 5,69% | | DBT (URL #1) | 28/08/2025 | B |
| 50 | ChatGPT Enterprise: trong **monthly active users**, **19% chưa từng dùng data analysis** (14% chưa dùng reasoning, 12% chưa dùng search); trong **daily active users**: 3% / 1% / 1% | Tỷ lệ chưa từng dùng tính năng | OpenAI state of enterprise AI 2025 (URL #11), tr. 15 | 08/12/2025 | A |
| 51 | Frontier worker trong nhóm data analytics dùng data-analysis tool **16x** median | | Như trên | 08/12/2025 | A |
| 52 | Coding messages của **non-technical** workers tăng TB **36%** trong 6 tháng; 75% người khảo sát làm được việc trước đây không làm được (gồm programming support) | | Như trên | 08/12/2025 | A/B |
| 53 | Data Analysis **0,4%**, Mathematical Calculation 3%, Programming 4,2% consumer messages | | *How People Use ChatGPT* | 15/09/2025 | A |
| 54 | DBT: Data analysis **3,37%**, Reviewing code **1,19%** use case | | DBT | 28/08/2025 | B |

**GAP:** Không có số "ảnh/user/ngày" cho môi trường doanh nghiệp, và không có tỷ lệ message gọi code interpreter (chỉ có tỷ lệ "đã từng dùng").

---

## 6. Implications for sizing (đề xuất cho VBot)

> Mọi số dưới đây là **giả định thiết kế** suy ra từ nguồn ở trên, không phải dữ liệu đo. Đơn vị gốc: **user turn** (một prompt người dùng gửi). VBot đếm *daily active* user nên dùng số **per active user per active day**, không chia trên license.

### 6.1 Request (user turn) / DAU / ngày

| Kịch bản | Turn / DAU / ngày | Căn cứ |
|---|---|---|
| **Low** | **5** | DBT ≈ 3,8 actions/active user/ngày (#3); consumer ChatGPT ≈ 3,7 message/WAU/ngày (#15); Treasury/DTA cho thấy tần suất thấp khi công cụ còn hạn chế (#8, #9) |
| **Base** | **12** | ≈ 2–3 task/ngày (DBT 4,7 use case/tuần là *mức sàn* của người mới; 39% dùng nhiều lần/ngày ở UK GDS #5) × ~5 prompt/conversation (LayerX TB 5,09, #16). VBot có connector Gmail/M365/Jira nên kỳ vọng cao hơn Copilot 2024 |
| **High** | **30** | Frontier worker = 6x median (#12); Glean tuyên bố 14 query/ngày (#17, tin cậy C); dư địa cho power user + agent |

Tháng (22 ngày, 2.000 DAU): Low 220k, Base **528k**, High 1,32 triệu turn.

### 6.2 Tier mix (tỷ lệ turn)

| Tier | Low-complexity mix | **Base** | Agent-heavy mix | Căn cứ |
|---|---|---|---|---|
| T1 Email/tóm tắt/RAG Q&A | 75% | **65%** | 50% | DBT ≈ 73% (#2.1); OpenAI work: Writing 40% + Practical Guidance 24% (#21) |
| T2 Báo cáo/biên bản + DOCX/XLSX/PPTX | 15% | **17%** | 18% | DBT drafting + slides ≈ 14% |
| T3 Spreadsheet/code sandbox | 5% | **8%** | 12% | DBT 4,6%; 81% MAU Enterprise đã dùng data analysis (#50); coding non-tech +36%/6 tháng (#52) |
| T4 Agent đa bước (Jira/Confluence/Notion) | 3% | **6%** | 15% | DBT ~1% (trial không có agent); API Office/Admin 13–15% & automation ~75% (#26) cho thấy nhu cầu tự động hóa — **GAP**, cần đo sau pilot |
| T5 Thiết kế: mockup/diagram/ảnh | 2% | **4%** | 5% | DBT ảnh 1,54%; consumer Multimedia ~7% (#48) |

### 6.3 Giả định token theo tier (Base) — giả định thiết kế

| Tier | LLM call / turn | Input / call | Output / call | Căn cứ |
|---|---|---|---|---|
| T1 | 1,5 (router/retrieval + answer) | 6k | 400 | OpenRouter TB ~6k/~400 (#32); Azure conv P90 3,8k (#33) + 5–10 chunk RAG |
| T2 | 2 | 8k | 2,5k | GAP — output dài cho tài liệu |
| T3 | 4 | 15k | 1,5k | Programming prompt >20k (#32); vòng viết–chạy–sửa code |
| T4 | 15 | 10k | 800 | SWE-agent median 12–15 turn (#39); 3–15 tool call/agent (#38); ~130k–220k token/run (#40) |
| T5 | 1 + 1 image gen | 3k | 500 | GAP |

Kết quả **(suy ra)**: TB ≈ **22,5k input + 2,5k output token / turn**. Base: 24.000 turn/ngày → ~540M input + ~59M output token/ngày; ~11,9B input + ~1,3B output token/tháng. **T4 chỉ chiếm 6% turn nhưng ~40% input token** — đây là biến nhạy nhất của chi phí. Prompt caching (Claude Code docs: phần lớn input là cache read) làm giảm mạnh chi phí input thực tế.

Ảnh: Base 4% × 24.000 ≈ 960 tác vụ T5/ngày (≈ 0,5/DAU/ngày); nếu chỉ một nửa T5 là sinh ảnh raster, ~480 ảnh/ngày × số biến thể mỗi lần.

### 6.4 Giờ cao điểm

| Kịch bản | % lưu lượng ngày trong giờ cao nhất | Căn cứ |
|---|---|---|
| Low | 12% | Phân bố đều trong 10 giờ làm việc = 10%; Azure code trace (đa múi giờ) đã đạt 9,3–9,7% trên 24h (#42) |
| **Base** | **15%** | Một múi giờ (Việt Nam) + đỉnh sáng 9–11h và sau 13h30; peak/mean giờ ~2,2x của code trace áp lên cửa sổ 10h |
| High | 20% | Ngày đỉnh (peak-day factor ~1,67x của DBT, #45) và burst đầu giờ / sau họp |

Base: 24.000 × 15% = **3.600 turn trong giờ cao điểm ≈ 1 turn/giây**, tương đương ~3,4M input token/phút trước khi tính cache. Nên thiết kế capacity cho **High** (≈ 4.800 turn/giờ) kết hợp ngày đỉnh (×1,67).

### 6.5 Việc cần làm sau pilot

Các GAP lớn nhất — tỷ lệ agent run, context RAG thực tế, token sinh tài liệu, tần suất ảnh — chỉ có thể đo từ telemetry của chính VBot. Cần log theo từng turn: tier, số LLM call, input/output/cached token, tool call, và timestamp để hiệu chỉnh lại bảng trên sau 2–4 tuần pilot.
