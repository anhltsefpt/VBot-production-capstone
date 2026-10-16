# Token cho mỗi tác vụ (sizing chi phí LLM cho VBot)

> Ngày tổng hợp: 2026-10-16. Bổ sung cho `usage-benchmarks.md` §3 và §6.3; không lặp lại các nguồn đã có ở đó (OpenRouter ~6k/400, Azure trace 2024, agent 4x chat, SWE-agent).
>
> Quy ước: mỗi con số có **giá trị — định nghĩa — nguồn (URL) — ngày — độ tin cậy**. "**(suy ra)**" = phép tính của người tổng hợp. "**(tự đo)**" = người tổng hợp tự đo bằng tokenizer công khai, có mô tả phương pháp. "**GT**" = giả định thiết kế. Không tìm thấy dữ liệu → **GAP**.
>
> Độ tin cậy: **A** = tài liệu chính thức / paper / dữ liệu gốc; **B** = blog vendor, nguồn thứ cấp, số đọc qua trích đoạn; **C** = nguồn yếu, phương pháp không rõ.
>
> Quy đổi dùng chung: tiếng Anh 1 token ≈ 4 ký tự ≈ ¾ từ (OpenAI Help, https://help.openai.com/en/articles/4936856 — B, chỉ đọc được qua trích đoạn); Gemini: "a token is equivalent to about 4 characters. 100 tokens is equal to about 60-80 English words" (https://ai.google.dev/gemini-api/docs/tokens, cập nhật 13/10/2026 — A).

---

## 1. Email

| # | Giá trị | Định nghĩa | Nguồn | Ngày | Tin cậy |
|---|---|---|---|---|---|
| E1 | Thread TB **233,2 từ**; email TB **50,3 từ**; **4,5 email/thread** | Dataset EmailSum (Avocado + W3C), **đã lọc**: 3–10 email/thread, 5–200 từ/email, 30–1.000 từ/thread → là cận dưới | Zhang et al., *EmailSum* (ACL 2021) — https://arxiv.org/abs/2107.14691 | 07/2021 | A |
| E2 | BC3 (40 thread W3C): **550,4 từ/thread**, **85,3 từ/email**, **6,4 email/thread**; tóm tắt người viết TB **134,3 từ** | Bảng 2 của EmailSum | Như trên | 07/2021 | A |
| E3 | Tóm tắt EmailSum: ngắn TB **27,1 từ** (<30), dài TB **68,5 từ** (<100) | Tóm tắt do người viết cho 2.549 thread | Như trên | 07/2021 | A |
| E4 | EnronSent: 96.106 message, 13.810.266 từ → **≈144 từ/message** **(suy ra)** | Chỉ thư mục "Sent Mail", đã bỏ phần trích dẫn và forward | Styler, *EnronSent README* — https://wstyler.ucsd.edu/files/enronsent_README.txt | 2011 | A (số đếm) |
| E5 | Thread Enron "usually short (fewer than 3 emails) and noisy" | Nhận xét, không phải thống kê | EmailSum (E1) | 07/2021 | A |
| E6 | Độ dài email tối ưu **50–125 từ** (tỷ lệ phản hồi >50%) | Nghiên cứu tỷ lệ phản hồi trên >40 triệu email, **không** phải độ dài trung bình | Boomerang — https://blog.boomerangapp.com/2016/02/7-tips-for-getting-more-responses-to-your-emails-with-data/ | 12/02/2016 | B |
| E7 | Smart Reply: "∼25% of replies have 20 tokens or less" | Phân phối độ dài reply Gmail | Kannan et al., *Smart Reply* (KDD 2016) — https://arxiv.org/abs/1606.04870 | 06/2016 | A |
| E8 | Copilot Outlook "Draft with Copilot", Gemini "Help me write": chỉ có tùy chọn ngắn/dài, **không công bố số từ**; giới hạn input khi tóm tắt thread **không công bố** (số "15.000 token" trên các site thứ ba = C, không dùng) | | support.microsoft.com, blog.google | 2026 | **GAP** |

**Suy ra cho VBot (token):**
- Thread BC3 550 từ ÷ 0,75 ≈ **733 token tiếng Anh**; Enron 144 từ × 4,5 email ≈ 648 từ ≈ 864 token.
- Tiếng Việt × 1,4 (xem §6) → **≈ 1.000–1.200 token** phần nội dung. Header, chữ ký, phần trích dẫn lặp lại: **GT ×2 → ~2.000 token/thread**.
- Reply soạn sẵn: 50–125 từ (E6) → 67–167 token EN → **~95–235 token tiếng Việt**. Tóm tắt dài 68,5–134 từ → **~130–250 token tiếng Việt**.

---

## 2. RAG hỏi đáp: chunk, top-k và system prompt

### 2.1 Mặc định của vendor

| # | Nền tảng | Chunk / overlap mặc định | Top-k mặc định | Context **(suy ra = k × chunk, cận trên)** | Nguồn | Tin cậy |
|---|---|---|---|---|---|---|
| R1 | Azure OpenAI "On your data" | "The default chunk size is 1,024 tokens" | `topNDocuments` "5 by default" (3/5/10/20); strictness 3 | 1.024 × 5 = **5.120** (Microsoft đo thực tế: **3.997–4.854** token generation prompt); tối đa 1.024 × 20 = 20.480 | https://learn.microsoft.com/en-us/azure/foundry-classic/openai/concepts/use-your-data (ms.date 14/10/2026) | A |
| R2 | Azure OYD: giới hạn khác | Câu hỏi + lịch sử "capped at 2,000 tokens"; 20% token dành cho response; system message tối đa 4.000 token (GPT-4o) | | | Như trên | A |
| R3 | Azure AI Search, Text Split skill | `maximumPageLength` mặc định **5.000 ký tự** (≈ 1.250 token **(suy ra)**); khuyến nghị 512 token | | | https://learn.microsoft.com/en-us/azure/search/cognitive-search-skill-textsplit (07/01/2026) | A |
| R4 | Azure AI Search, chunking guide | "starting with a chunk size of 512 tokens … overlap of 25%" (128 token) | | | https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-chunk-documents (08/06/2026) | A |
| R5 | Azure, thí nghiệm hybrid retrieval | Recall@50: chunk 512 → 42,4; 1.024 → 37,5; 4.096 → 36,4; overlap 25% → 43,9 | | | techcommunity.microsoft.com (blog 18/09/2023, URL trong tiêu đề *Azure AI Search: Outperforming vector search with hybrid retrieval and ranking*) | B |
| R6 | Vertex AI RAG Engine | "default chunk size is 1,024 tokens", "default chunk overlap is 256 tokens" | **Không công bố** (quickstart ví dụ `similarity_top_k=3`, chunk 512) | Ví dụ quickstart: 512 × 3 = **1.536** | https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/fine-tune-rag-transformations (15/10/2026) | A (top-k: GAP) |
| R7 | Vertex AI Search, layout parser | Chunk mặc định **500 token** (100–500); thêm tối đa 5 chunk trước + 5 chunk sau | GAP | 1 kết quả ≤ 11 × 500 = **5.500** | https://docs.cloud.google.com/generative-ai-app-builder/docs/parse-chunk-documents (13/10/2026) | A |
| R8 | Amazon Bedrock Knowledge Bases | Default ≈ **300 token**, giữ ranh giới câu (overlap mặc định: GAP) | "up to five results … by default" (1–100) | 300 × 5 = **1.500**; hierarchical (khuyến nghị parent 1.500/child 300) ≤ 5 × 1.500 = **7.500** | https://docs.aws.amazon.com/bedrock/latest/userguide/kb-chunking.html ; kb-test-config.html | A |
| R9 | OpenAI file_search | `max_chunk_size_tokens` 800, overlap 400 | "up to 20 chunks for gpt-4* … 5 for gpt-3.5"; ngân sách 16.000 / 4.000 token | 800 × 20 = **16.000** (khớp ngân sách) | community.openai.com/t/811723 (trích docs); rubydoc SDK | B (docs gốc hiện 404) |
| R10 | Anthropic Contextual Retrieval | Chunk "no more than a few hundred tokens" (ví dụ tính chi phí: 800) | "top-20 chunks … more effective than … top-10 or top-5" | 20 × 800 = 16.000; + 100 token context/chunk → **18.000** | https://www.anthropic.com/news/contextual-retrieval | 19/09/2024, B |
| R11 | LlamaIndex | `DEFAULT_CHUNK_SIZE = 1024`, overlap 20 (SentenceSplitter: 200) | `DEFAULT_SIMILARITY_TOP_K = 2` | 1.024 × 2 = **2.048** | GitHub run-llama/llama_index (nhánh main, xem 16/10/2026) | A |
| R12 | LangChain text splitter | 4.000 **ký tự** / overlap 200 (≈ 1.000 token, quy ước 4 ký tự/token) | | | `langchain_text_splitters/base.py` | A |
| R13 | NVIDIA chunking study | Thử 128–2.048 token, top-k 10; tốt nhất: page-level; theo token: 512–1.024 | k = 10 | 10 × 512–1.024 = **5.120–10.240** | https://developer.nvidia.com/blog/finding-the-best-chunking-strategy-for-accurate-ai-responses/ | 18/06/2025, B |
| R14 | Microsoft 365 Copilot Retrieval API | `maximumNumberOfResults` tối đa 25; `queryString` ≤ 1.500 ký tự. Kích thước extract và context Copilot thực tế: **GAP** | | | https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/api/ai-services/retrieval/overview (20/08/2026) | A |
| R15 | Glean, Gemini Enterprise grounding | Không công bố | | | | **GAP** |

**Lưu ý:** chunk đo bằng **token**, nên context RAG theo token **không tăng** khi nội dung là tiếng Việt (chỉ ít chữ hơn trong mỗi chunk). Phụ phí tiếng Việt chỉ áp dụng cho phần đo bằng từ/ký tự (email, transcript, output).

### 2.2 System prompt và tool schema

| # | Giá trị | Định nghĩa | Nguồn | Ngày | Tin cậy |
|---|---|---|---|---|---|
| P1 | System prompt claude.ai (Opus 5.5): **4.162 từ / 27.507 ký tự → ≈ 6.900 token (suy ra, ÷4)** | Chỉ phần core được công bố, không gồm hướng dẫn tool | https://platform.claude.com/docs/en/release-notes/system-prompts/claude-opus-5-5 | 22/09/2026 | A (nguồn) / B (token ước lượng) |
| P2 | Claude.ai kèm tool ~24k token; Claude 4.6 ~15k; ChatGPT "as many as 15,000 tokens" | Bản rò rỉ | TowardsAI, adversa.ai, … | 2025–2026 | C |
| P3 | Overhead tool use (chưa tính schema): Opus/Sonnet 5.5 **286** token (auto); Opus 4.7 675/804; Sonnet 4.5 496/588 | System prompt Anthropic tự chèn khi có tools | https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview | xem 16/10/2026 | A |
| P4 | GitHub MCP: 35 tool ~**26K** token; Slack ~21K; 58 tool ~**55K**; nội bộ Anthropic từng 134K; Tool Search: ~77K → ~8,7K (−85%) | Tool definitions nạp sẵn vào context | Anthropic, *Advanced tool use* — https://www.anthropic.com/engineering/advanced-tool-use | 24/11/2025 | B |
| P5 | Code execution with MCP: **150.000 → 2.000 token (−98,7%)**; transcript họp 2 giờ "could mean processing an additional 50,000 tokens" | Tool definitions + kết quả trung gian | https://www.anthropic.com/engineering/code-execution-with-mcp | 04/11/2025 | B |

---

## 3. Sinh tài liệu (DOCX/PPTX)

### 3.1 Độ dài tài liệu

| # | Giá trị | Định nghĩa | Nguồn | Ngày | Tin cậy |
|---|---|---|---|---|---|
| D1 | **500 từ/trang** (single-spaced, 12pt) | Quy ước trình bày | Grammarly — https://www.grammarly.com/blog/frequently-asked-questions/how-many-pages-is-500-words/ | xem 10/2026 | B |
| D2 | Executive summary **300–500 từ** (5–10% tài liệu); proposal thường 1 trang | Hướng dẫn viết | HurleyWrite — https://www.hurleywrite.com/how-long-should-an-executive-summary-be/ | 11/06/2026 | B/C |
| D3 | Biên bản họp: "a record of what was **done** … not what was **said**" (Robert's Rules §48:2) | Quy tắc, không có số trang | MSU Academic Governance — https://acadgov.msu.edu/About/Writing-Minutes | — | A (quy tắc) |
| D4 | Biên bản điều hành **1 trang**: 3–7 quyết định, 3–8 dòng action, ≤10 chủ đề × 1–2 câu | Template | GoTranscript — https://gotranscript.com/en/blog/executive-meeting-minutes-template-decision-first-one-page | 04/01/2026 | C |
| D5 | SlidesBench: 310 deck PPTX thật, **20 slide/deck** TB | Dataset paper | Ge et al., *AutoPresent* (CVPR 2025) — https://arxiv.org/html/2501.00912v2 | 2025 | A |
| D6 | **33,4 từ/slide**, 7,5 dòng text (1.381 slide, 72 bài nói ASEE 2008) | Đếm trên slide thật | Penn State — https://pure.psu.edu/en/publications/application-of-multimedia-theory-to-powerpoint-slides-created-by--2/ | 2009 | A |
| D7 | Pitch deck TB ~19 slide (DocSend, ~200 deck) | Chỉ qua nguồn thứ cấp (docsend.com 403) | avalaunchmedia; TechCrunch 08/06/2015 | 2015 | B/C |
| D8 | PPTAgent: deck đánh giá **12,9–18,4 trang**, **3.700–6.600 ký tự**/deck; tài liệu nguồn 12k–18k ký tự; 2 vòng self-correction/slide | | Zheng et al., *PPTAgent* — https://arxiv.org/html/2501.03936v3 | 21/02/2025 | A |
| D9 | LLM không hỗ trợ "struggle to generate outputs exceeding … 2,000 words"; LongWriter >10.000 từ | Giới hạn output dài | Bai et al., *LongWriter* — https://arxiv.org/abs/2408.07055 | 08/2024 | A |
| D10 | Độ dài báo cáo tư vấn; số trang biên bản HĐQT | | | | **GAP** |

**Suy ra (token tiếng Việt, ×1,4 so với EN — xem §6):**
- Biên bản 1 trang ≈ 500 từ ≈ 667 token EN ≈ **930 token** (markdown).
- Báo cáo 10 trang ≈ 5.000 từ ≈ 6.667 token EN ≈ **9.300 token**.
- Deck 20 slide × 33,4 từ = 668 từ ≈ 890 token EN ≈ **1.250 token** chữ trên slide (chưa tính notes).

### 3.2 Output khi sinh file bằng code

| # | Giá trị | Định nghĩa | Nguồn | Tin cậy |
|---|---|---|---|---|
| C1 | **170 dòng code/slide** khi dùng python-pptx thô; **13 dòng** với thư viện helper (SlidesLib) | Mỗi chương trình sinh 1 slide trong SlidesBench | AutoPresent (D5) | A |
| C2 | Code python-pptx 1 slide (tiêu đề + 4 bullet + ghi chú, nội dung tiếng Việt): **482 token / 37 dòng = 13,0 token/dòng**; bản markdown cùng nội dung: **109 token** → code ≈ **4,4×** markdown | o200k_base (tiktoken), 1 mẫu do người tổng hợp viết | **(tự đo)**, script trong scratchpad | C (1 mẫu) |
| C3 | Anthropic Agent Skills `SKILL.md`: pptx 20.796 byte, docx 6.911 byte, xlsx 8.598 byte → ≈ **5,2k / 1,7k / 2,1k token** (÷4) | Hướng dẫn nạp vào context khi dùng skill (chưa tính script phụ) | https://github.com/anthropics/skills/tree/main/skills (commit 17/07/2026) | A (byte) / C (token) |
| C4 | Token/dòng của AutoPresent, PPTAgent; so sánh đo được DOCX-code vs markdown | | | **GAP** |

**Suy ra:**
- Deck 20 slide python-pptx thô: 20 × 170 × 13 ≈ **44.200 token** output. Với helper library: 20 × 13 × 13 ≈ **3.380 token**.
- Biên bản DOCX bằng code: 930 × 4,4 ≈ **4.100 token**.
- → Thiết kế VBot nên có **template + helper library** (kiểu SlidesLib); nếu không, output T2 tăng ~10×.

---

## 4. Phân tích dữ liệu / code interpreter

| # | Giá trị | Định nghĩa | Nguồn | Ngày | Tin cậy |
|---|---|---|---|---|---|
| A1 | DA-Code: TB **7,3 bước** (GPT-4), 7,1 (DeepSeek-Coder-V2.5), 11,1 (Mixtral-8x22B); tối đa 20; **85 dòng code/task**; 5,7 file/task | 500 task phân tích dữ liệu agentic | Huang et al., *DA-Code* (EMNLP 2024) — https://arxiv.org/html/2410.07331v2 | 2024 | A |
| A2 | DABstep tổng chi phí 450 task: Claude 3.7 Sonnet **$139**, o4-mini $93, GPT-4.1 $155, GPT-4o $53; tối đa 10 bước (ReAct) | "estimates based on public pricing … Q1 2025 and token usage" | https://arxiv.org/html/2506.23719 | 2025 | A |
| A3 | DABstep/task **(suy ra)**: $139 ÷ 450 = **$0,309** (Claude 3.7); nếu toàn bộ là input $3/M → ≈ **103k token/task** ≈ **~10k token/bước** với 10 bước (cận trên số bước) | | | | B (suy ra thô, bỏ qua output) |
| A4 | DSBench data analysis (466 task): AutoGen+GPT-4o $114,05 → **$0,245/task**; Code Interpreter+GPT-4o $87,04 → $0,187 **(suy ra, giả sử là tổng)** | Paper không ghi rõ tổng hay mỗi task | Jing et al., *DSBench* — https://arxiv.org/html/2409.07703v2 | 09/2024 | A (định nghĩa mơ hồ) |
| A5 | Gemini code execution: code sinh ra và kết quả tính là input token ở bước trung gian; runtime tối đa **30 s**; tự sửa lỗi "up to 5 times" | | https://ai.google.dev/gemini-api/docs/code-execution (13/10/2026) | 2026 | A |
| A6 | Anthropic code execution: **$0,05/container-giờ**, 1.550 giờ miễn phí/tháng/org, tối thiểu 5 phút; 5 GiB RAM, 1 CPU | Tính theo thời gian, tách khỏi token | https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool | xem 16/10/2026 | A |
| A7 | OpenAI Code Interpreter: **$0,03/phiên 20 phút** (1 GB) … $1,92 (64 GB); tính theo phút, tối thiểu 5 phút | | https://developers.openai.com/api/docs/pricing | 2026 | A |
| A8 | SpreadsheetLLM: sheet 576 × 23 = **61.240 token** (vanilla) → 708 sau nén; nén TB **24,79×** | Mã hóa `|Address, Value, Format|` | Microsoft, *SpreadsheetLLM* — https://arxiv.org/html/2407.09025v1 | 07/2024 | A |
| A9 | **(suy ra từ A8)**: 61.240 ÷ 13.248 ô ≈ **4,62 token/ô**; ≈ **106 token/dòng** | | | | A |
| A10 | Token/bước của code-interpreter agent (InfiAgent-DABench, TaskWeaver, Spider2…) | Không paper nào công bố token/bước, chỉ tổng chi phí | | | **GAP** |

**Ý nghĩa cho VBot:**
- Không nên đưa nguyên sheet vào prompt: sheet 1.000 dòng ≈ 106k token. Agent chỉ đọc `df.head()` / schema (vài trăm token) rồi chạy code.
- Code output nhỏ: 85 dòng/task × ~13 token/dòng (C2) ≈ **1.100 token code/task** **(suy ra)**.
- Chi phí sandbox nhỏ so với token: tối thiểu $0,0042 (Anthropic) – $0,0075 (OpenAI) mỗi phiên **(suy ra)**.

---

## 5. Agent văn phòng (không phải coding)

| # | Benchmark | Bước / tool call mỗi task | Token / chi phí mỗi task | Nguồn | Tin cậy |
|---|---|---|---|---|---|
| G1 | **MCPMark – Notion** (28 task) | gpt-4.1: 8,58 turn / 11,82 call; o3: 13,72 / 12,72; gemini-2.5-pro: 7,12 / 8,67; claude-sonnet-4: 19,71 / 18,71; gpt-5-medium: 12,94 / 21,60 | Input: **135,55K** (gpt-4.1), 224,93K (o3), 212,92K (gemini), **646,64K** (sonnet-4), 375,04K (gpt-5). Output: 1,37K / 9,47K / 7,13K / 4,24K / 31,62K | https://arxiv.org/html/2509.24002 (Table 6) | A |
| G2 | MCPMark – toàn bộ (127 task) | "16.2 execution turns and 17.4 tool calls per task" | gpt-5-medium 627,66K in / 21,91K out / $1,00 | Như trên | A |
| G3 | **(suy ra từ G1)** input/turn | | gpt-4.1: 135,55K ÷ 8,58 = **15,8K**; o3: 16,4K; gpt-5: 29,0K; gemini: 29,9K; sonnet-4: **32,8K**. Output/turn: gpt-4.1 **160**; sonnet-4 215; o3 690; gpt-5 2,4K (reasoning) | | A |
| G4 | MCP-Universe (231 task, 11 server) | TB bước: GPT-5 8,22; Claude-4.0-Sonnet 7,46; o3 **4,82** | GAP | https://arxiv.org/html/2508.14704 | A |
| G5 | LiveMCP-101 | TB **5,4 tool call/task**, tối đa 15 | GAP | https://arxiv.org/html/2508.15760 | A |
| G6 | MCP-Bench (28 server, 250 tool) | GPT-5: 9,2 round / 78,9 call; GPT-4o, o3: 5,8–6,3 round / 21,8–28,3 call | | https://arxiv.org/html/2508.20453 | A |
| G7 | Toolathlon (32 app gồm Notion, Google Calendar) | TB turn: Claude-4.5-Sonnet 20,2; GPT-5 18,7; Claude-4-Sonnet 27,3; "overlong tool outputs" ở 15–35% trajectory | "Most models operate under $1 per task" | https://arxiv.org/html/2510.25726v2 | A |
| G8 | **TheAgentCompany** (GitLab, Plane, RocketChat, ownCloud) | "Steps = total number of LLM calls": Claude-3.7 **27,8**; Gemini-2.5-Pro 27,2; GPT-4o 14,6 | Claude-3.7 **$4,1/task** (không cache) → $0,147/call → ≈ **49k token input-tương-đương/call** **(suy ra, giá $3/M, bỏ output)** | https://arxiv.org/html/2412.14161v3 | A |
| G9 | *Is Bash All You Need?* (TheAgentCompany) | Median 14,0 tool call (typed tools), 12,8 (bash) | Typed tools: Opus-4.8 ~945K token, GPT-5.5 ~465K; bash: 264K / 377K; bash giảm "19-72%" token | https://arxiv.org/html/2609.11999 | B (preprint mới) |
| G10 | tau-bench (retail) | Tối đa 30 action | gpt-4o: **$0,38/task** (agent); input chiếm **95,9%** chi phí do system prompt dài (policy + function definitions) | https://arxiv.org/html/2406.12045 | A |
| G11 | tau2-bench | | gpt-4.1: $0,086/task (agent) | https://arxiv.org/html/2506.07982 | A |
| G12 | HAL tau-airline (50 task) | | Claude-3.7 tool calling $15,45 → **$0,309/task**; o4-mini $0,227; Opus 4.1 $1,396 **(suy ra ÷50)** | https://hal.cs.princeton.edu/taubench_airline | A |
| G13 | AppWorld | Lời giải tham chiếu: 42,5–46,8 API call, 8,2–10,5 API khác nhau, 1,5–2 app/task | GPT-4o ReAct ~$0,7/task | https://arxiv.org/html/2407.18901 | A |
| G14 | AgentBench | TB round: OS 8, DB 5, KG 15, WebShop 5, Mind2Web 10 | | https://arxiv.org/abs/2308.03688 | A |
| G15 | WorkArena (ServiceNow) | Tối đa 15 bước (WorkArena++: 50) | HTML phẳng **40k–500k token**/trang dù đã làm sạch → phải dùng AXTree rút gọn | https://arxiv.org/html/2403.07718 | A |
| G16 | OSWorld | Tối đa 15 bước | "context length of 6000 … about 90% of cases for a single observation" | https://arxiv.org/html/2404.07972 | A |

**Kích thước tool schema và tool result:**

| # | Giá trị | Nguồn | Tin cậy |
|---|---|---|---|
| S1 | Atlassian Rovo MCP quảng bá một nhóm nhỏ tool chính, phần còn lại khám phá qua tool `discover` | https://developer.atlassian.com/cloud/rovo-mcp/ (02/09/2026) | A |
| S2 | Notion MCP: ~8.000 token (15+ tool); khác: 24 tool ≈ 17.500 token | dev.to (01/2026); TowardsAI (snippet) | C |
| S3 | GitHub MCP: 42K–55K token (93 tool); bộ mặc định 26 tool ≈ 4.200 token | dev.to; getunblocked.com | B/C |
| S4 | Jira issue JSON không lọc field ">3KB" (≈ **750+ token**), lọc field "<500 bytes" (≈ **125 token**) **(suy ra ÷4)**; có comment/changelog sẽ lớn hơn nhiều | reintech.io (04/2024) | C |
| S5 | MCP Jira bên thứ ba cắt response >40.000 ký tự (≈ 10k token) | mcpservers.org | C |
| S6 | Notion page qua markdown ít hơn ~6–7× token so với block JSON thô | mcpservers.org (easy-notion-mcp) | C |
| S7 | Kích thước page Confluence (storage format), event Google Calendar, metadata Drive | | **GAP** — cần tự đo payload thật trong pilot |

**Ý nghĩa cho VBot:**
- Tác vụ T4 của VBot (tạo/cập nhật ticket, đặt lịch) đơn giản hơn MCPMark. Neo gần nhất là LiveMCP-101 (5,4 call) và MCP-Universe (4,8–8,2 bước).
- Input/call ~16k (gpt-4.1, o3 trên Notion) là neo thực nghiệm cho mức base.
- Cấp 15 call × 10k của §6.3 cũ tương đương 150k/turn, nằm giữa MCPMark gpt-4.1 (135k/task) và o3 (225k/task), nhưng đó là cho **cả task khó**, không phải cho mỗi turn của task văn phòng đơn giản.

---

## 6. Phụ phí token tiếng Việt

**Tự đo** trên FLORES-200 dev+devtest: 2.009 cặp câu song song (VI 270.586 ký tự / 59.918 âm tiết; EN 257.160 ký tự / 42.855 từ), dùng tiktoken và HF `tokenizers`. Tỷ lệ = token VI ÷ token EN cho **cùng nội dung**.

| Tokenizer | Token VI | Token EN | **VI/EN** | Ký tự/token VI | Ký tự/token EN |
|---|---|---|---|---|---|
| cl100k (GPT-4, GPT-3.5) | 129.317 | 52.983 | **2,44** | 2,09 | 4,85 |
| o200k (GPT-4o trở đi) | 77.820 | 52.409 | **1,49** | 3,48 | 4,91 |
| Gemma 3 (= tokenizer Gemini 2.0) | 72.346 | 52.995 | **1,37** | 3,74 | 4,85 |
| Llama 3 | 73.460 | 52.963 | 1,39 | 3,68 | 4,86 |
| Qwen2.5 | 77.095 | 53.876 | 1,43 | 3,51 | 4,77 |
| Llama 2 | 177.065 | 60.619 | 2,92 | 1,53 | 4,24 |

| # | Giá trị | Nguồn | Ngày | Tin cậy |
|---|---|---|---|---|
| V1 | cl100k VI/EN = 129.258 / 52.835 = **2,45**; GPT-2 = **4,54** (nguồn của con số "4,5×" hay được trích); LLaMA-1 = 2,92 **(suy ra từ file dữ liệu)** | Petrov et al., *Language Model Tokenizers Introduce Unfairness Between Languages* (NeurIPS 2023) — https://arxiv.org/abs/2305.15425 ; dữ liệu https://aleksandarpetrov.github.io/tokenization-fairness/ | 2023 | A |
| V2 | "Vietnamese 1.5x fewer tokens (from 46 to 30)" khi chuyển cl100k → o200k (1 câu mẫu). Tự đo lại câu mẫu: cl100k VI 46 / EN 25, o200k VI 30 / EN 23 | OpenAI, *Hello GPT-4o* (bản Wayback) — http://web.archive.org/web/20240601000000/https://openai.com/index/hello-gpt-4o/ | 13/05/2024 | A |
| V3 | Gemma 3 "same tokenizer as Gemini 2.0 … 262k entries … more balanced for non-English languages" | https://arxiv.org/html/2503.19786v1 | 03/2025 | A |
| V4 | Claude Opus 4.7: "The same input can map to more tokens—roughly 1.0–1.35×"; OpenRouter đo: +~45% (<2K token), +32–34% (≥10K) | https://www.anthropic.com/news/claude-opus-4-7 ; https://openrouter.ai/blog/insights/opus-47-tokenizer-analysis/ | 04/2026 | A / B |
| V5 | Tỷ lệ VI/EN của **Claude** | Tokenizer không công khai; chỉ đo được qua endpoint `count_tokens` | | **GAP** — đo trong pilot |
| V6 | SeaLLMs: VI 4,41 (ChatGPT) / 3,46 (Llama-2) / 1,48 (SeaLLM) so với EN | https://arxiv.org/html/2312.00738v2 | 2023 | B (cột ChatGPT có vẻ là tokenizer cũ) |

**Áp dụng (GT):**
- Nội dung đo bằng từ (email, transcript, output) × **1,4** khi quy từ token tiếng Anh. Căn cứ: 1,37 (Gemini) – 1,49 (GPT o200k); Claude chưa đo.
- Hỗn hợp 70% VI / 30% EN cho kết quả 0,7 × 1,4 + 0,3 = **1,28**; dùng 1,4 cho an toàn.
- System prompt và tool schema viết bằng tiếng Anh nên không nhân.
- Chunk RAG đo bằng token nên không nhân.

---

## 7. Tích lũy context nhiều lượt và prompt caching

### 7.1 Lịch sử gửi lại mỗi lượt

- Anthropic: "The Messages API is stateless, which means that you always send the full conversational history" (https://platform.claude.com/docs/en/build-with-claude/working-with-messages — A).
- OpenAI: "Even when using `previous_response_id`, all previous input tokens … are billed as input tokens" (https://developers.openai.com/api/docs/guides/conversation-state — A).

| Dataset | Số conversation | TB lượt | Token user/lượt | Token assistant/lượt | Nguồn |
|---|---|---|---|---|---|
| LMSYS-Chat-1M | 1.000.000 | **2,02** | 69,83 | 215,71 | WildChat Table 1 — https://arxiv.org/html/2405.01470 (A) |
| WildChat | 1.039.785 | **2,54** | 295,58 | 441,34 | Như trên |
| ShareGPT | 94.145 | 3,51 | 94,46 | 348,45 | Như trên |

**Mô hình tăng trưởng (suy ra):**
- Context ở lượt k = S + k·U + (k−1)·A.
- Tổng input T lượt = U·T(T+1)/2 + A·T(T−1)/2 + T·S, tức tăng theo **bình phương** số lượt.
- Với giá trị TB của WildChat, S = 0:
  - 3 lượt: tổng input 3.098 token, context lượt cuối 1.769.
  - 10 lượt: tổng 36.117 token (12,2× so với chỉ gửi tin mới).
- Sizing VBot có 1–4 lượt/nhiệm vụ (IT code: 8), nên lịch sử chỉ thêm ~1–3k token/call ở mức base.

### 7.2 Điều khoản caching (10/2026)

| Provider | Giá đọc cache | Ghi cache | TTL | Ngưỡng tối thiểu | Nguồn (A) |
|---|---|---|---|---|---|
| Anthropic | 0,1× (cũ); **0,05×** Opus/Sonnet 5.5; 0,025× Fable/Mythos 5.1 | 1,25× (5 phút), 2× (1 giờ) | 5 phút mặc định | 512–4.096 token tùy model | https://platform.claude.com/docs/en/build-with-claude/prompt-caching |
| OpenAI | **0,1×** (0,05× GPT-6.1 Sol); lúc ra mắt 10/2024: 50% | Tự động, không phí ghi | 30 phút (GPT-5.6+) | 1.024 token | https://developers.openai.com/api/docs/guides/prompt-caching |
| Gemini | Giảm 90% (2.5 Pro $1,25 → $0,125); implicit caching bật mặc định | | | 2.048 (2.5), 4.096 (3.x/4) | https://ai.google.dev/gemini-api/docs/caching ; /pricing |
| DeepSeek | $0,014 vs $0,14 (hit vs miss); "users save over 50% on average" | | | 64 token | https://api-docs.deepseek.com/news/news0802 |

### 7.3 Tỷ lệ cache hit đã công bố

| # | Giá trị | Định nghĩa | Nguồn | Tin cậy |
|---|---|---|---|---|
| K1 | "~70%" (LLM judge 1 lượt); "**>90%**" (agent nhiều lượt) | Ví dụ deployment trong guide, không nêu tên | OpenAI prompt caching guide (URL trên) | A |
| K2 | **62%** (trace A, chat consumer) / **54%** (trace B, business API), cache lý tưởng không giới hạn; trace B: request 1 lượt chiếm 97% cache hit; P99 vòng đời cache 97 giây | Tỷ lệ KV block tái sử dụng | Alibaba, *KVCache Cache in the Wild* (USENIX ATC'25) — https://arxiv.org/html/2506.02634v4 | A |
| K3 | Kimi/Mooncake: ~**50%** (input TB 7.590, output TB 182 token) | Trace 1 giờ, 23.608 request | https://arxiv.org/html/2407.00079v3 | A |
| K4 | SGLang Chatbot Arena: 52,4% (LLaVA-Next-34B), 74,1% (Vicuna-33B) | Production | https://arxiv.org/html/2312.07104v2 | A |
| K5 | Manus: "KV-cache hit rate is the single most important metric"; input:output ≈ **100:1** | Blog agent production | https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus (18/07/2025) | A (blog 1st-party) |
| K6 | Claude Code chạy cảnh báo và "declare SEVs" khi cache hit thấp (ngưỡng không công bố) | | claude.dev blog (30/04/2026) | A |
| K7 | OpenRouter "82,8%" toàn nền tảng; user Claude Code 95–98% | | aireiter.com, Substack | C |

**Ví dụ (suy ra):** WildChat, S = 2.000 token, 10 lượt, điều khoản Anthropic 5 phút. Không cache: 56.117 đơn vị input. Có cache: 11.311 đơn vị (**0,20×**). Tỷ lệ token hit 91,2%.

**Lưu ý cho VBot:** chat ngắn kiểu LMSYS có context đỉnh ~355 token, dưới mọi ngưỡng cache. VBot chỉ hưởng cache khi **prefix chung** (system prompt + tool schema ≥ 1–4k token) đặt cố định ở đầu và dùng lại trong TTL. Với ~27k lượt/ngày dùng chung một prefix, điều này gần như luôn thỏa.

---

## 8. Sinh ảnh

| # | Giá trị | Định nghĩa | Nguồn | Ngày | Tin cậy |
|---|---|---|---|---|---|
| I1 | Prompt TB **27,16 term** (Midjourney), **30,34** (DiffusionDB); median 20 / 26; max 426 / 540 | Log prompt thật | Xie et al., *Prompt log analysis* (WWW '23) — https://arxiv.org/abs/2303.04587 | 2023 | A |
| I2 | DiffusionDB: prompt 6–12 token phổ biến nhất; đỉnh ở 75 (giới hạn CLIP) | 1,82 triệu prompt | Wang et al. — https://arxiv.org/abs/2210.14896 | 07/2023 | A |
| I3 | DALL-E 3 prompt rewriting: "Image descriptions must be between 15 -80 words" | Prompt GPT-4 viết lại | Betker et al. — https://cdn.openai.com/papers/dall-e-3.pdf | 10/2023 | A |
| I4 | Vertex Imagen: prompt rewriting bật mặc định; `sampleCount` 1–4 (mặc định: nguồn mâu thuẫn) | | docs.cloud.google.com/vertex-ai/generative-ai/docs/image/generate-images (13/10/2026) | 2026 | A / GAP |
| I5 | OpenAI `n` 1–10; DALL-E 3 chỉ n = 1 (đã retire trên Azure 04/03/2026) | | OpenAI API reference; learn.microsoft.com | 2026 | A / B |
| I6 | Midjourney: lưới **4** ảnh/lệnh; Firefly Image 3/4: **4** biến thể, Image 4 Ultra/5: 1 | | Hướng dẫn thứ cấp; helpx.adobe.com (snippet) | | B/C |
| I7 | **Token ảnh output:** gpt-image-1 1024² low/medium/high = **272 / 1.056 / 4.160**; Gemini 2.5 Flash Image ≤1024² = **1.290 token** ($0,039); Gemini 3 Pro Image 1K–2K = 1.120 token ($0,134) | Ảnh tính như output token | https://developers.openai.com/api/docs/models/gpt-image-1 ; https://ai.google.dev/gemini-api/docs/pricing (15/10/2026) | 2026 | A |

**Suy ra:**
- Prompt ảnh do LLM viết 15–80 từ ≈ 20–107 token EN. Phần prompt là không đáng kể; chi phí nằm ở **ảnh**.
- Trong T5 của sizing, ảnh raster chiếm (150 + 45) ÷ 297 ≈ **66%** lượt. Tính: Marketing 0,25 × 200 × 3 = 150; Kinh doanh 0,03 × 500 × 3 = 45.
- 34% còn lại là diagram sinh bằng code (Mermaid/HTML): PM 72 + IT 30 lượt, không có ảnh.

---

## 9. Kiểm tra giả định §6.3 hiện tại

| Tier | Giả định cũ (call × in / out) | Kết luận |
|---|---|---|
| T1 | 1,5 × 6k / 400 | Input/call **gần đúng** (5,5k). Output **cao**: reply 50–125 từ (E6) và tóm tắt 68–134 từ (E2–E3) ≈ 100–250 token; Q&A ≈ 440 (WildChat). Đề xuất **250**. Số call nên là **2** (tool fetch email/RAG + trả lời). |
| T2 | 2 × 8k / 2,5k | Input **thấp**: biên bản (81% nhiệm vụ T2) thường kèm transcript (1 giờ ≈ 25k token EN theo P5, ≈ 35k VI) và skill docx/pptx 1,7–5,2k (C3). Đề xuất **18k**. Output 2,5k hợp lý nếu có template/helper (C1–C2). |
| T3 | 4 × 15k / 1,5k | Input/call hơi cao so với DABstep (~10k/bước, A3). DA-Code 7,3 bước/**task** tương đương ~3,5 call/**turn** trên 4 turn/task. Output **thấp hơn**: 85 dòng code/task (A1). Đề xuất **3,5 × 12k / 1k**. |
| T4 | 15 × 10k / 800 | Số call **cao** cho task văn phòng: LiveMCP 5,4; MCP-Universe 4,8–8,2. Input/call **thấp** so với MCPMark-Notion 15,8k–32,8k/turn (G3). Output **cao** với model không reasoning (160–215, G3). Đề xuất **8 × 15k / 300**. |
| T5 | 1 × 3k / 500 + 1 ảnh | Gần đúng. Thêm diagram bằng code (34% lượt) nên output tăng nhẹ. Ảnh/lượt 0,66–2,6. |

---

## 10. Đề xuất token theo cấp

Định nghĩa: mỗi ô là giá trị **mỗi LLM call**, trừ cột "call/lượt". Input đã gồm system prompt, tool schema, lịch sử và phụ phí tiếng Việt ×1,4 cho phần nội dung đo bằng từ. "Cache" = tỷ lệ input token được đọc từ cache (giả định điều khoản Anthropic/OpenAI, prefix cố định).

| Tier | Mức | Call/lượt | Input/call | Output/call | Cache | Căn cứ |
|---|---|---|---|---|---|---|
| **T1** Email, hỏi đáp | Low | 1,5 | 3.500 | 150 | 30% | Bedrock 300 × 5 = 1,5k (R8) + system 2k (GT); reply 50–125 từ (E6); hit thấp vì chat ngắn dưới ngưỡng cache (§7.3) |
| | **Base** | **2** | **5.500** | **250** | **50%** | Call 1 (~4k: system + tool 3k **GT**, theo R2 cap 4k và P3; lịch sử ~1k từ WildChat × 1,4) + call 2 (draft 6k / tóm tắt 5k / Q&A 9,2k = 3k + Azure 5,1k (R1) + 1k; tỷ trọng 60/16/24% theo sizing-load) → TB (4 + 6,6) ÷ 2 ≈ 5,3k. Output: TB (80 + 237) ÷ 2 ≈ 160, nâng lên 250 (**GT**, có lời dẫn). Cache: prefix 3k/5,5k ≈ 55%; Alibaba business 54% (K2) |
| | High | 2,5 | 10.000 | 500 | 70% | file_search 16k / Contextual Retrieval 18k (R9–R10) chia cho các call; OpenAI ~70% (K1) |
| **T2** Tài liệu | Low | 1,5 | 7.000 | 1.500 | 40% | Ghi chú tay ~1,5k + system 3k + skill docx 1,7k (C3) + lịch sử; biên bản 930 token (D1, §6) + code helper |
| | **Base** | **2** | **18.000** | **2.500** | **60%** | Nguồn TB 12k (**GT**: ⅓ transcript 35k [P5: 2 giờ ≈ 50k token EN → 1 giờ 25k × 1,4] + ⅔ ghi chú 1,5k) + system/skill 4,7k + lịch sử; output = (markdown 1k + code 4k) ÷ 2 (C2: code ≈ 4,4× markdown); cache: nguồn + skill dùng lại qua các call và lượt |
| | High | 3 | 45.000 | 6.000 | 80% | Transcript 35k + skill pptx 5,2k + lịch sử; báo cáo 10 trang ≈ 9,3k token (D1); 2 vòng self-correction (D8) |
| **T3** Dữ liệu, code | Low | 2 | 6.000 | 600 | 40% | Schema/`head()` vài trăm token (A8–A9), system 3k; 85 dòng code/task (A1) |
| | **Base** | **3,5** | **12.000** | **1.000** | **65%** | DA-Code 7,3 bước/task (A1) → (7 + 2 + 2 + 2) ÷ 4 ≈ 3,25 call/lượt; DABstep ~10k/bước (A3) + phụ phí VI; Gemini sửa lỗi ≤5 lần (A5) |
| | High | 7 | 30.000 | 2.500 | 85% | DA-Code Mixtral 11,1 bước; TheAgentCompany ~49k/call (G8); IT viết code 8 lượt/nhiệm vụ; OpenAI agent >90% (K1) |
| **T4** Agent dự án | Low | 5 | 8.000 | 200 | 60% | LiveMCP-101 5,4 call (G5); MCP-Universe o3 4,82 (G4); Rovo discovery giữ schema nhỏ (S1) |
| | **Base** | **8** | **15.000** | **300** | **80%** | MCP-Universe 7,5–8,2 bước (G4); MCPMark-Notion gpt-4.1/o3 15,8k–16,4k/turn (G3); output 160–690 (G3); OpenAI multi-turn agent >90% (K1), hạ xuống 80% (**GT**) |
| | High | 18 | 30.000 | 700 | 90% | MCPMark-Notion Claude 17–20 turn, 29,9k–32,8k/turn (G1, G3); Toolathlon 18,7–20,2 turn (G7); K1 |
| **T5** Thiết kế | Low | 1 | 3.000 | 300 | 20% | Prompt ảnh 15–80 từ (I3); 0,66 ảnh/lượt (§8) |
| | **Base** | **1,5** | **4.000** | **600** | **40%** | Diagram code Mermaid/HTML (34% lượt) cần thêm call render/sửa (**GT**); 1 ảnh/lượt (có "sinh thêm", **GT**) |
| | High | 2 | 6.000 | 1.000 | 60% | 2,6 ảnh/lượt = 0,66 × 4 biến thể (I6) |

Token ảnh: **1.290 token/ảnh** (Gemini 2.5 Flash Image, I7). gpt-image-1 medium là 1.056.

### Tổng theo tháng

Lượt/tháng = lượt/ngày (sizing-load.md) × 22 ngày:

| Tier | Lượt/ngày | Lượt/tháng |
|---|---|---|
| T1 | 20.507 | 451.154 |
| T2 | 3.153 | 69.366 |
| T3 | 2.099 | 46.178 |
| T4 | 1.042 | 22.924 |
| T5 | 297 | 6.534 |

Công thức: input/tháng = lượt/tháng × call/lượt × input/call (output tương tự). Ví dụ T1 Base: 451.154 × 2 × 5.500 = **4,96B**. Script: `scratchpad/tpt.py` (tính lại được từ bảng trên).

| Tier | Low: in / out (tỷ token) | **Base: in / out** | High: in / out | Base: input/lượt | Base: % input |
|---|---|---|---|---|---|
| T1 | 2,37 / 0,10 | **4,96 / 0,23** | 11,28 / 0,56 | 11.000 | 40,7% |
| T2 | 0,73 / 0,16 | **2,50 / 0,35** | 9,36 / 1,25 | 36.000 | 20,5% |
| T3 | 0,55 / 0,06 | **1,94 / 0,16** | 9,70 / 0,81 | 42.000 | 15,9% |
| T4 | 0,92 / 0,02 | **2,75 / 0,06** | 12,38 / 0,29 | 120.000 | 22,6% |
| T5 | 0,02 / 0,00 | **0,04 / 0,01** | 0,08 / 0,01 | 6.000 | 0,3% |
| **Tổng** | **4,59 / 0,34** | **12,19 / 0,79** | **42,80 / 2,92** | | |
| Trong đó input đọc cache | 1,78 | **7,46** | 34,82 | | |
| Input không cache | 2,81 | **4,73** | 7,98 | | |
| Ảnh/tháng (token ảnh) | 4.312 (5,6M) | **6.534 (8,4M)** | 16.988 (21,9M) | | |

**Đọc kết quả:**
- **Base** mới cho 12,19B input / 0,79B output mỗi tháng. Giả định cũ §6.3 (tính lại với cùng số lượt) cho 11,40B / 1,17B.
- Tổng input gần như không đổi, nhưng **output giảm ~32%** và cơ cấu dịch chuyển: T2 tăng (do transcript), T4 giảm.
- 61% input base đọc từ cache: 7,46 ÷ 12,19.
- Low → High chênh **9×** về input. Biến nhạy nhất:
  - Số call/lượt của T4 và T3.
  - Có đưa transcript vào T2 hay không.
  - Model reasoning: output/turn của gpt-5 trên MCPMark là 2,4k, so với 160 của gpt-4.1 (G3).
- Với model reasoning, nên nhân output T3/T4 lên 3–10× (**GT**).

### GAP cần đo trong pilot

1. Tỷ lệ token VI/EN của Claude (`count_tokens`).
2. Kích thước payload Jira/Confluence/Notion/Calendar thật.
3. Tỷ lệ biên bản có transcript.
4. Cache hit thực tế theo tier.
5. Output token khi sinh DOCX/PPTX bằng template của VBot.
