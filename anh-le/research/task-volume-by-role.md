# Khối lượng công việc theo vai trò → số request AI (bottom-up, sizing VBot)

> Ngày tổng hợp: 2026-10-16. Báo cáo này **bổ sung** cho [`usage-benchmarks.md`](./usage-benchmarks.md) (top-down: telemetry Copilot/ChatGPT, token, giờ cao điểm). Không lặp lại các số ở đó; khi cần, trích theo mã `#n` của báo cáo cũ (ví dụ `UB#3` = mục #3 trong usage-benchmarks.md).
>
> **Công thức:** `request/người/ngày = Σ_tác vụ  V × s × t`
> - **V** — khối lượng công việc thật / người / ngày làm việc (có nguồn, mục 1).
> - **s** — tỷ lệ khối lượng đó được giao cho trợ lý AI (mục 2).
> - **t** — số user turn cho một tác vụ được giao AI (1 turn = 1 prompt người dùng gửi, cùng đơn vị với UB mục 6).
>
> Quy ước: **(suy ra)** = phép tính của người tổng hợp, có ghi phép tính. **GT** = giả định, không có nguồn trực tiếp. **GAP** = không tìm thấy dữ liệu. Độ tin cậy: **A** telemetry/thực nghiệm có phương pháp rõ; **B** khảo sát tự báo cáo, benchmark vendor có phương pháp, hoặc số đọc qua trích dẫn/snippet khi trang gốc không truy cập được; **C** thứ cấp / phương pháp không rõ.
>
> Ngày làm việc: 22 ngày/tháng; tuần làm việc 5 ngày; ngày làm việc 8 giờ dùng để quy đổi % thời gian ra giờ.

---

## 1. Khối lượng công việc thực tế (V) — có nguồn

| Mã | Giá trị | Quy đổi / người / ngày (suy ra) | Định nghĩa chính xác | Nguồn — URL | Ngày | Tin cậy |
|---|---|---|---|---|---|---|
| W1 | **117 email nhận/ngày**; **153 tin nhắn Teams nhận/ngày làm việc**; 50% cuộc họp rơi vào 9–11h và 13–15h; 57% cuộc họp là ad hoc (không có lịch) | 117 email nhận; 153 tin nhắn chat nhận | Tín hiệu Microsoft 365 tổng hợp, ẩn danh, loại trừ tenant Education và EU; "average worker" | Microsoft WorkLab, *Breaking down the infinite workday* (Work Trend Index Special Report) — https://www.microsoft.com/en-us/worklab/work-trend-index/breaking-down-infinite-workday | 17/06/2025 (dữ liệu đến 15/02/2025) | A (telemetry; không công bố phân phối/median) |
| W2 | 2015: **122 email gửi+nhận/business user/ngày** = **88 nhận + 34 gửi**; 2013: 78 nhận + 37 gửi; 2012: 78 nhận + 36 gửi | 34 email gửi | Ước tính mô hình thị trường của Radicati, "business email" | The Radicati Group, *Email Statistics Report, 2015–2019 — Executive Summary* — https://www.radicati.com/wp/wp-content/uploads/2015/02/Email-Statistics-Report-2015-2019-Executive-Summary.pdf | 02/2015 | B (domain radicati.com không phân giải được khi truy cập; số lấy qua snippet tìm kiếm của chính PDF. Bản 2024–2028 chỉ có tổng 361,6 tỷ email/ngày, số per-user nằm trong bản trả phí) |
| W3 | Nhóm đối chứng: **160,83 email đọc/tuần** (SD 117,74); Outlook session **11,65 giờ/tuần** | **32,2 email đọc/ngày** = 160,83 ÷ 5 | Telemetry, giai đoạn trước can thiệp, RCT 66 công ty, 7.137 người | Dillon et al. (Microsoft Research), *Shifting Work Patterns with Generative AI* — https://arxiv.org/abs/2504.11436 | 04/2025 | A |
| W4 | **14,51 thread email được trả lời/tuần** (SD 14,17) | **2,9 thread trả lời/ngày** = 14,51 ÷ 5 | Số *thread duy nhất* có trả lời — thấp hơn số email gửi (một thread có thể nhiều reply, chưa tính email mới) | Dillon et al. (như W3) | 04/2025 | A |
| W5 | Email gửi/ngày — **dải 2,9 → 34**, giá trị Base **9,9** | Base = √(2,9 × 34) = 9,93 (trung bình nhân hai đầu dải) | Kết hợp W4 (cận dưới) và W2 (cận trên) | (suy ra) | — | B (suy ra) |
| W6 | **9,93 cuộc họp Teams/tuần** (SD 6,93); **5,22 giờ họp/tuần** | **≈ 2,0 cuộc họp/ngày** = 9,93 ÷ 5; TB 0,53 giờ/cuộc = 5,22 ÷ 9,93 | Telemetry nhóm đối chứng | Dillon et al. (như W3) | 04/2025 | A |
| W7 | Executive TB **gần 23 giờ họp/tuần** (từ <10 giờ những năm 1960) | ≈ **4,6 giờ/ngày** = 23 ÷ 5; nếu mỗi cuộc ~1 giờ (GT) → **4,6 cuộc/ngày** | Khảo sát 182 senior manager | Perlow, Hadley, Eun, *Stop the Meeting Madness*, Harvard Business Review — https://hbr.org/2017/07/stop-the-meeting-madness | 07–08/2017 | B |
| W8 | **0,76 tài liệu Word hoàn thành/tuần**; Word session **1,63 giờ/tuần** | **0,15 tài liệu/ngày** = 0,76 ÷ 5 | "Completed documents" theo telemetry | Dillon et al. (như W3) | 04/2025 | A |
| W9 | Interaction worker dành **~28%** tuần làm việc cho email và **gần 20%** để tìm thông tin nội bộ / tìm đồng nghiệp | 20% × 8 h = **1,6 giờ/ngày tìm thông tin** | Ước tính từ khảo sát + phân tích hoạt động | McKinsey Global Institute, *The social economy* — https://www.mckinsey.com/industries/technology-media-and-telecommunications/our-insights/the-social-economy | 07/2012 | B (cũ) |
| W10 | Knowledge worker dành **~9,5 giờ/tuần** tìm thông tin, trong đó **3,5 giờ** là tìm không ra | 3,5 ÷ 5 = **0,7 giờ/ngày** (phần "lãng phí") | Khảo sát IDC (Susan Feldman) | IDC, *The High Cost of Not Finding Information* (trích qua https://www.networkworld.com/article/2303260/software/you-are-wasting-time--find-out-why.html) | ~2001–2004 | C (rất cũ, chỉ có trích dẫn thứ cấp) |
| W11 | **25%** lãnh đạo và nhân viên dành **1/4 tuần làm việc** để tìm thông tin | 25% × 8 h = **2 giờ/ngày** | Khảo sát 12.000 knowledge worker + 200 exec Fortune 1000 | Atlassian, *State of Teams 2025* (đưa tin: https://www.unleash.ai/artificial-intelligence/atlassian-ai-could-help-workers-stop-wasting-2-4-billion-hours-searching-for-information-every-year/) | 04/2025 | B |
| W9–11 (suy ra) | **Số lượt tìm thông tin/ngày: 1,75 / 4,0 / 5,0** | Chia số giờ ở W10/W9/W11 cho **24 phút/lượt** — thời gian baseline của tác vụ "information search" trong thí nghiệm Copilot (D13): 0,7 h ÷ 0,4 h = 1,75; 1,6 ÷ 0,4 = 4,0; 2,0 ÷ 0,4 = 5,0 | Quy đổi thô: 24 phút là thời lượng một tác vụ thí nghiệm, không phải trung bình thực tế | (suy ra) | — | C |
| W12 | CSKH: baseline **2,6 chat xử lý/giờ**; **2,12 chat giải quyết/giờ**; AI tăng resolution/giờ **14%** TB (22% theo một đặc tả), giảm thời gian xử lý 3,8 phút (9%) | 2,6 × 8 h = **20,8 chat/ngày** | Dữ liệu vận hành 5.172 agent hỗ trợ khách hàng (công ty phần mềm Fortune 500) | Brynjolfsson, Li, Raymond, *Generative AI at Work*, NBER WP 31161 — https://www.nber.org/papers/w31161 | 04/2023, sửa 11/2023 (đăng QJE 2025) | A |
| W13 | Desktop support: **tickets/technician/tháng** TB theo ngành **87–133** (Financial services 99, High tech 100, Equipment mfg 98, Telecom 124, Business services 87, Healthcare 108, Energy/Utilities 133); min 30, max 198 | 87 ÷ 22 = **4,0**; 100 ÷ 22 = **4,5**; 133 ÷ 22 = **6,0 ticket/ngày** | Ticket = incident + service request của desktop support (không gồm L1 service desk) | Jeff Rumburg (MetricNet), *Metric of the Month: Tickets per Technician per Month*, HDI — https://www.thinkhdi.com/~/media/HDICorp/Files/Library-Archive/Insider%20Articles/tickets-per-technician.pdf | 2012 | B (benchmark cũ) |
| W14 | Median active developer merge **2 PR/tuần** (median of medians); 48% dev tạo 80% PR | **0,4 PR/ngày** = 2 ÷ 5 | Dữ liệu nền tảng Graphite từ 01/2023, loại tuần code-freeze cuối năm | Graphite Research — https://graphite.com/research/commit-frequency | 2023– (truy cập 10/2026) | B (vendor, người dùng Graphite thiên về team năng suất cao) |
| W15 | Median active reviewer nhận **3 review request/tuần**; review rate median **71,5%** | **0,6 review/ngày** = 3 ÷ 5 | Như W14 | Graphite Research — https://graphite.com/research/review-request-frequency | 2023– | B (lấy qua snippet tìm kiếm) |
| W16 | AP: median **~12.000 hóa đơn/FTE/năm** (3.748 tổ chức) | 12.000 ÷ 264 ngày = **45,5 hóa đơn/ngày** | Số hóa đơn xử lý / FTE thực hiện quy trình "process accounts payable" | APQC Open Standards Benchmarking — https://www.apqc.org/what-we-do/benchmarking/open-standards-benchmarking/measures/number-invoices-processed-fte-1 | liên tục cập nhật | B (trang trả 403; số lấy qua snippet tìm kiếm) |
| W17 | Mua hàng: median **728,6 PO/FTE/năm**; P25 **333**; P75 **1.461** (5.108 tổ chức) | 333 ÷ 264 = **1,3**; 728,6 ÷ 264 = **2,8**; 1.461 ÷ 264 = **5,5 PO/ngày** | Số PO xử lý / FTE nhóm quy trình "procure materials and services" | APQC — https://www.apqc.org/resources/benchmarking/open-standards-benchmarking/measures/number-purchase-orders-processed-fte-0 | liên tục cập nhật | B (như W16) |
| W18 | FP&A: **41%** quy trình làm thủ công ≈ **10 giờ/tuần** chuyên viên tài chính dành cho bảng tính | 10 ÷ 5 = **2 giờ/ngày** | Khảo sát CFO của DataRails (vendor) | DataRails (đưa tin: https://beckershospitalreview.com/finance/cfos-bored-with-constant-spreadsheet-jockeying-survey.html) | ~2022 | C |
| W19 | Sales rep dành **70%** thời gian cho việc **không bán hàng** (admin, chuẩn bị họp…), chỉ ~30% bán hàng | — (chỉ là phân bổ thời gian, không phải số tác vụ) | Khảo sát 5.500 người làm sales, 27 nước, 08/03–18/04/2024 | Salesforce, *State of Sales* 6th ed. — https://www.salesforce.com/news/stories/sales-ai-statistics-2024/ | 25/07/2024 | B |
| W20 | Trung bình **57%** thời gian trong M365 là giao tiếp (họp, email, chat), **43%** là tạo nội dung (tài liệu, bảng tính, slide); top 25% email user **8,8 giờ email/tuần**, top 25% meeting user **7,5 giờ họp/tuần**; số cuộc họp/cuộc gọi Teams mỗi tuần **gấp 3 (+192%)** so với 02/2020 | — | Telemetry M365 28 ngày đến 03/2023 (thương mại, không gồm Education) | Microsoft, *2023 Work Trend Index: Will AI Fix Work?* — https://www.microsoft.com/en-us/worklab/work-trend-index/will-ai-fix-work | 09/05/2023 | A (telemetry) / B (phần survey) |

**Ghi chú về email:** "nhận" (117, W1) ≠ "đọc" (32,2, W3) ≠ "gửi" (2,9–34, W4/W2). Báo cáo này dùng **email đọc** làm V cho tóm tắt và **email gửi** làm V cho soạn thảo — vì tóm tắt/soạn chỉ xảy ra trên email người dùng thực sự xử lý.

**Không có số theo phòng ban** cho email, họp, tài liệu: W1–W8 là trung bình toàn bộ người dùng M365. Chỉ W7 (lãnh đạo), W12 (CSKH), W13 (IT support), W14–W15 (dev), W16 (AP), W17 (mua hàng), W18 (FP&A), W19 (sales) là số theo vai trò.

---

## 2. Tỷ lệ giao việc cho AI (s) và cường độ sử dụng — có nguồn

| Mã | Giá trị | Định nghĩa | Nguồn — URL | Ngày | Tin cậy |
|---|---|---|---|---|---|
| D1 | Văn bản được LLM hỗ trợ (cuối 2024): **~18%** khiếu nại tài chính của người tiêu dùng; **tới 24%** thông cáo báo chí doanh nghiệp; **gần 10%** tin tuyển dụng (doanh nghiệp nhỏ); **~14%** thông cáo báo chí của Liên Hợp Quốc | Ước lượng thống kê phân phối từ ngữ trên 687k khiếu nại, 537k thông cáo, 304 triệu tin tuyển dụng, 15,9k thông cáo UN (01/2022–09/2024) — **số đo, không phải tự khai** | Liang et al. (Stanford), *The Widespread Adoption of Large Language Model-Assisted Writing Across Society* — https://arxiv.org/abs/2502.09747 | 02/2025 | A (đo trên văn bản công khai; email nội bộ chưa được đo) |
| D2 | Microsoft Copilot Dashboard: **power user** = TB **≥15 Copilot action/tuần** và dùng ≥9/12 tuần; **habitual user** = 1–14 action/tuần | Ngưỡng phân loại do Microsoft định nghĩa | Microsoft Viva Insights / Copilot Dashboard (thông báo RM560705 — https://mc.merill.net/message/RM560705) | 2025 | B (định nghĩa chính thức, lấy qua bản tóm tắt message center) |
| D3 | UK cross-government: TB tiết kiệm **26 phút/ngày**; soạn tài liệu tiết kiệm **24 phút**, làm slide **19 phút**, lên lịch họp **9 phút**; 13/15 nghề có >25% dùng Copilot trong Teams **hằng ngày**; 11/15 nghề có >40% dùng trong Word **hằng tuần** | Khảo sát 7.115 người, trial 20.000 công chức | UK GDS, *Microsoft 365 Copilot Experiment: Cross-Government Findings Report* — https://www.gov.uk/government/publications/microsoft-365-copilot-experiment-cross-government-findings-report/microsoft-365-copilot-experiment-cross-government-findings-report-html | 02/06/2025 | B |
| D3b | DBT: Word, Teams, Outlook là ba app dùng Copilot nhiều nhất, **~10–15% license dùng hằng ngày** trong mỗi app; M365 Copilot app **6–10%**; PowerPoint và Excel đỉnh **7%**/ngày. Phỏng vấn: phù hợp nhất với **HR, Communications, Commercial**; **Legal và Policy** thấy ít phù hợp | Telemetry dashboard + phỏng vấn theo vai trò | UK DBT evaluation (URL ở UB#1) — https://assets.publishing.service.gov.uk/media/68adbe409e1cebdd2c96a19d/dbt-microsoft-365-copilot-evaluation.pdf | 28/08/2025 | A (telemetry) / B (phỏng vấn) |
| D4 | ChatGPT Enterprise: tiết kiệm **40–60 phút/ngày active**; data science, engineering, communications **60–80 phút**; *time saved per message* lớn nhất ở **accounting & finance**, rồi analytics, communications, engineering; **87%** IT worker báo xử lý sự cố nhanh hơn; **85%** marketing/product báo chạy campaign nhanh hơn; **73%** kỹ sư báo giao code nhanh hơn; coding message ngoài engineering/IT/research **+36%** trong 6 tháng | Khảo sát ~100 doanh nghiệp + dữ liệu sử dụng | OpenAI, *The state of enterprise AI — 2025 report* — https://cdn.openai.com/pdf/7ef17d82-96bf-4dd1-9df2-228f7f377a29/the-state-of-enterprise-ai_2025-report.pdf | 08/12/2025 | B (không có số tuyệt đối theo chức năng) |
| D5 | DBT diary: "Generating images" **1,54%** use case (UB#49) | — | UB#49 | 28/08/2025 | B |
| D6 | Consumer ChatGPT: Multimedia **~7%** message (UB#48) | — | UB#48 | 15/09/2025 | A |
| D7 | Stack Overflow 2025: **51%** professional developer dùng AI tool **hằng ngày**; toàn bộ người trả lời 47,1% hằng ngày + 17,7% hằng tuần | Khảo sát 49.009 người, 29/05–23/06/2025 | Stack Overflow Developer Survey 2025 — https://survey.stackoverflow.co/2025/ai | 07/2025 | B |
| D8 | Anthropic nội bộ: nhân viên tự báo dùng Claude trong **59%** công việc (năm trước 28%); chỉ "fully delegate" được **0–20%** công việc; **27%** việc có Claude hỗ trợ là việc "lẽ ra không làm" | Khảo sát 132 kỹ sư/nhà nghiên cứu + 53 phỏng vấn | Anthropic, *How AI is transforming work at Anthropic* — https://www.anthropic.com/research/how-ai-is-transforming-work-at-anthropic | 02/12/2025 | B (nhóm dùng AI cực cao — dùng làm cận trên) |
| D9 | **70%** muốn giao càng nhiều việc càng tốt cho AI; thoải mái dùng AI cho việc hành chính **76%**, phân tích **79%**, sáng tạo **73%**; muốn AI giúp tìm thông tin **86%**, tóm tắt cuộc họp và action item **80%**, lên kế hoạch ngày **77%** | Khảo sát 31.000 người, 31 nước — **mức sẵn sàng, không phải mức dùng thực tế** | Microsoft, *2023 Work Trend Index* (như W20) | 09/05/2023 | B |
| D10 | Gallup (Mỹ): dùng AI **hằng ngày 12%**, **≥ vài lần/tuần 26%** (Q4/2025); nhóm remote-capable: **19% hằng ngày, 40% thường xuyên**; dùng ít nhất vài lần/năm: leader **69%**, manager **55%**, individual contributor **40%**; theo ngành: technology/IS **76%**, finance **58%**, professional services **57%**, manufacturing 38%, retail 33% | Khảo sát panel đại diện người lao động Mỹ | Gallup, *Frequent Use of AI in the Workplace Continued to Rise* / *AI Use at Work Rises* — https://www.gallup.com/workplace/699689/ai-use-at-work-rises.aspx | 2025–2026 | B |
| D11 | Accenture × GitHub Copilot: **90%** dev đã commit code do Copilot gợi ý; chấp nhận ~30% gợi ý; số PR **+8,69%** | Field experiment | GitHub Blog, *Quantifying GitHub Copilot's impact in the enterprise with Accenture* — https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-in-the-enterprise-with-accenture/ | 2024 | B (vendor) |
| D12 | Claude Code nội bộ Anthropic: **human turn/transcript giảm 6,2 → 4,1**; tool call liên tiếp **9,8 → 21,2** (02→08/2025) | Phân tích 200.000 transcript | Anthropic (như D8) | 02/12/2025 | A |
| D13 | Copilot early users: nhanh hơn **29%** ở chuỗi tác vụ tìm kiếm/viết/tóm tắt; tác vụ tìm thông tin **24 → 18 phút**; tóm tắt cuộc họp bị lỡ **43 → 11 phút**; viết bản nháp **14 → 8 phút**; sales (n=133) tiết kiệm **90 phút/tuần**; customer service: thời gian xử lý case **−12%** | Thí nghiệm có đối chứng + khảo sát EAP | Microsoft WorkLab, *What Can Copilot's Earliest Users Teach Us About Generative AI at Work?* — https://www.microsoft.com/en-us/worklab/work-trend-index/copilots-earliest-users-teach-us-about-generative-ai-at-work | 15/11/2023 | A (thí nghiệm) / B (khảo sát) |
| D14 | Copilot làm thời gian Outlook **giảm 1,4 giờ/tuần (−12%)**, email đọc **−6,69/tuần (≈ −4%)**; **không** thay đổi đáng kể thời gian họp và viết tài liệu | ITT tháng 4–6 | Dillon et al. (như W3) | 04/2025 | A |
| D15 | BCG: dùng AI **≥ vài lần/tuần**: manager **78%** (2024: 64%), frontline **52%** (2024: 51%) | Khảo sát 10.000+ nhân viên | BCG, *AI at Work 2025: Momentum Builds, but Gaps Remain* — https://www.bcg.com/press/26june2025-beyond-ai-adoption-full-potential | 26/06/2025 | B |
| D16 | Slack: **1/5** desk worker dùng AI **hằng ngày** (+233% trong 6 tháng); 60% có dùng AI | Khảo sát 5.156 desk worker (AU, FR, DE, JP, UK, US), 09/04–01/05/2025 | Salesforce/Slack Workforce Index — https://www.salesforce.com/news/stories/daily-ai-workforce-use-growth/ | 2025 | B |
| D17 | Pew: chỉ **9%** người lao động Mỹ dùng chatbot AI cho công việc **hằng ngày hoặc vài lần/tuần**; người đã dùng: research 57%, sửa văn bản 52%, soạn văn bản 47% | Khảo sát 5.273 người lao động, 07–13/10/2024 | Pew Research Center — https://www.pewresearch.org/social-trends/2025/02/25/u-s-workers-are-more-worried-than-hopeful-about-future-ai-use-in-the-workplace/ | 25/02/2025 | B |
| D18 | Việt Nam: **88%** knowledge worker dùng GenAI ở nơi làm việc (toàn cầu 75%) | Khảo sát WTI 2024 | Microsoft & LinkedIn, *2024 Work Trend Index* (đưa tin: https://vietnamnews.vn/economy/1656260/rate-of-using-ai-to-work-in-viet-nam-is-higher-than-world-s-average-microsoft.html) | 05/2024 | B (chỉ là "có dùng", không có tần suất) |
| D19 | Claude.ai theo nhóm nghề (O*NET): Computer & Mathematical **37,2%**, Arts/Design/Media **10,3%**, Education **9,3%**, **Office & Administrative 7,9%**, Life sciences 6,4%, **Business & Financial 5,9%** | Phân loại ~1 triệu conversation | Anthropic, *The Anthropic Economic Index* — https://www.anthropic.com/news/the-anthropic-economic-index | 10/02/2025 | A (là tỷ trọng conversation, **không** phải tỷ lệ công việc được giao) |
| D20 | Australian Treasury / DTA: xem UB#8, UB#9. DTA: tiết kiệm cao nhất cho **tóm tắt thông tin ~1,1 giờ/ngày**, tạo tài liệu ~1 giờ/ngày; SES và EL2 dùng tóm tắt cuộc họp nhiều hơn các bậc khác | Tự báo cáo | DTA — https://www.digital.gov.au/initiatives/copilot-trial/summary-evaluation-findings/cts-executive-summary | 2024 | C (trang/PDF gốc timeout; số lấy qua tóm tắt tìm kiếm) |

**Kết luận mục 2:** không nguồn nào công bố trực tiếp "x% email được soạn bằng AI" hay "x% cuộc họp được recap bằng AI" trong doanh nghiệp. Số **đo được** gần nhất là D1 (10–24% văn bản chuyên nghiệp công khai có LLM hỗ trợ). Các số khác là tần suất dùng (D7, D10, D15–D17), mức sẵn sàng (D9) hoặc thời gian tiết kiệm (D3, D4, D13) — chỉ dùng để **neo** và **kiểm tra chéo** giả định s.

---

## 3. Tác vụ hằng ngày theo phòng ban

### 3.0. Tham số dùng chung

**Năm tác vụ chung** — áp cho mọi phòng ban (riêng Lãnh đạo dùng số họp từ W7):

| Tác vụ chung | Tier | V | s (L / B / H) | Căn cứ s | t (L / B / H) | Căn cứ t |
|---|---|---|---|---|---|---|
| Soạn/trả lời email | T1 | 2,9 / 9,9 / 34 (W4, W5, W2) | 10% / 16% / 24% | D1: thấp nhất 10% (tin tuyển dụng), trung vị của 4 lĩnh vực (10, 14, 18, 24) = 16%, cao nhất 24% (thông cáo báo chí) | 1 / 2 / 3 | Median 2 prompt/conversation, TB 5,09 (UB#16, tin cậy C) |
| Tóm tắt/triage email & thread | T1 | 32,2 (W3) | 2% / 5% / 10% | **GT.** Kiểm tra chéo: Base cho 32,2 × 5% = 1,6 tác vụ tóm tắt so với 9,9 × 16% = 1,6 tác vụ soạn → tỷ lệ 1,0; DBT diary có tỷ lệ "summarising written communications" : "writing an email" = 10,74 : 11,73 = 0,92 (UB mục 2.1) | 1 | Một lần bấm/gọi = 1 turn |
| Hỏi đáp tài liệu nội bộ (thay tìm kiếm) | T1 | 1,75 / 4,0 / 5,0 (W9–W11, suy ra) | 15% / 30% / 50% | **GT**, neo vào D9 (86% *muốn* AI giúp tìm thông tin). DBT: "searching" + "asking simple questions" = 12,71% use case ≈ 1,08 × "writing an email" | 1 / 2 / 3 | UB#16 |
| Biên bản/tóm tắt cuộc họp → DOCX | T2 | 2,0 (W6) | 10% / 20% / 40% | **GT.** Thấp hơn mức Copilot vì VBot không tự có transcript Teams/Meet — người dùng phải đưa ghi âm/ghi chú vào. D9: 80% muốn AI tóm tắt cuộc họp; DBT: meeting là use case số 1 (16,43%) | 2 / 3 / 5 | Tóm tắt + chỉnh + xuất file; UB#16 |
| Báo cáo/tờ trình/đề xuất → DOCX/PPTX | T2 | 0,15 (W8) | 30% / 50% / 80% | **GT**, neo vào D3 (Word >40% dùng hằng tuần ở 11/15 nghề) và D8 (59% công việc — cận trên) | 2 / 3 / 5 | Dàn ý → từng phần → chỉnh → xuất |

**t cho tác vụ đặc thù:** T3 phân tích bảng tính 3 / 4 / 6 (GT); T3 viết code theo PR 4,1 / 8,2 / 12,3 = 4,1 human turn/transcript (D12) × 1 / 2 / 3 session mỗi PR (GT); T4 agent 1 / 2 / 3 turn người dùng mỗi run (GT — một run có nhiều LLM call, xem UB#38–#40); T5 2 / 3 / 4 vòng chỉnh (GT).

**Cách đọc bảng:** Request = V × s × t, tính riêng cho từng kịch bản. Low = mọi tham số ở mức thấp, High = mọi tham số ở mức cao — nên High là **cận trên cực đoan**, không phải P90 (xem mục 4.3).

### 3.1. Sales & CSKH (500 người)

| Tác vụ | Tier | Khối lượng/ngày V (L / B / H) | Nguồn V | Tỷ lệ giao AI s (L / B / H) | Nguồn s | Turn/tác vụ t (L / B / H) | = Request/người/ngày (L / B / H) |
|---|---|---|---|---|---|---|---|
| Soạn/trả lời email | T1 | 2,9 / 9,9 / 34,0 | W4 / W5 / W2 | 10% / 16% / 24% | D1 | 1,0 / 2,0 / 3,0 | 0,29 / **3,2** / 24,5 |
| Tóm tắt/triage email & thread | T1 | 32,2 | W3 | 2% / 5% / 10% | GT | 1,0 | 0,64 / **1,6** / 3,2 |
| Hỏi đáp tài liệu nội bộ (thay tìm kiếm) | T1 | 1,7 / 4,0 / 5,0 | W9–W11 (suy ra) | 15% / 30% / 50% | GT | 1,0 / 2,0 / 3,0 | 0,26 / **2,4** / 7,5 |
| Biên bản/tóm tắt cuộc họp → DOCX | T2 | 2,0 | W6 | 10% / 20% / 40% | GT | 2,0 / 3,0 / 5,0 | 0,40 / **1,2** / 4,0 |
| Báo cáo/tờ trình/đề xuất → DOCX/PPTX | T2 | 0,15 | W8 | 30% / 50% / 80% | D3,D9 | 2,0 / 3,0 / 5,0 | 0,09 / **0,23** / 0,61 |
| Gợi ý trả lời chat/ticket khách hàng (½ bộ phận là CSKH) | T1 | 10,4 | W12 | 5% / 10% / 20% | GT | 1,0 | 0,52 / **1,0** / 2,1 |
| Phân tích pipeline/doanh số trên Excel | T3 | 0,20 | GT | 30% / 50% / 80% | GT | 3,0 / 4,0 / 6,0 | 0,18 / **0,40** / 0,96 |
| Agent cập nhật CRM/tạo task follow-up | T4 | 1,0 | GT | 5% / 10% / 25% | GT | 1,0 / 2,0 / 3,0 | 0,05 / **0,20** / 0,75 |
| Ảnh/visual cho báo giá, slide | T5 | 0,10 | GT | 20% / 30% / 50% | GT | 2,0 / 3,0 / 4,0 | 0,04 / **0,09** / 0,20 |
| **Tổng** | | | | | | | **2,5 / 10,3 / 43,8** |

Tier mix (Base): T1 80%, T2 14%, T3 4%, T4 2%, T5 1%

### 3.2. Kế toán/Tài chính (240 người)

| Tác vụ | Tier | Khối lượng/ngày V (L / B / H) | Nguồn V | Tỷ lệ giao AI s (L / B / H) | Nguồn s | Turn/tác vụ t (L / B / H) | = Request/người/ngày (L / B / H) |
|---|---|---|---|---|---|---|---|
| Soạn/trả lời email | T1 | 2,9 / 9,9 / 34,0 | W4 / W5 / W2 | 10% / 16% / 24% | D1 | 1,0 / 2,0 / 3,0 | 0,29 / **3,2** / 24,5 |
| Tóm tắt/triage email & thread | T1 | 32,2 | W3 | 2% / 5% / 10% | GT | 1,0 | 0,64 / **1,6** / 3,2 |
| Hỏi đáp tài liệu nội bộ (thay tìm kiếm) | T1 | 1,7 / 4,0 / 5,0 | W9–W11 (suy ra) | 15% / 30% / 50% | GT | 1,0 / 2,0 / 3,0 | 0,26 / **2,4** / 7,5 |
| Biên bản/tóm tắt cuộc họp → DOCX | T2 | 2,0 | W6 | 10% / 20% / 40% | GT | 2,0 / 3,0 / 5,0 | 0,40 / **1,2** / 4,0 |
| Báo cáo/tờ trình/đề xuất → DOCX/PPTX | T2 | 0,15 | W8 | 30% / 50% / 80% | D3,D9 | 2,0 / 3,0 / 5,0 | 0,09 / **0,23** / 0,61 |
| Phân tích bảng tính FP&A/đối soát | T3 | 2,0 | W18 (2h/ngày ÷ 1h/việc) | 10% / 20% / 40% | D4,D10 | 3,0 / 4,0 / 6,0 | 0,60 / **1,6** / 4,8 |
| Ngoại lệ hóa đơn AP: trích xuất/đối chiếu (⅓ bộ phận là AP) | T3 | 15,2 | W16 | 1% / 2% / 5% | GT | 1,0 | 0,15 / **0,30** / 0,76 |
| Agent tạo ticket/nhắc việc khóa sổ | T4 | 0,50 | GT | 5% / 10% / 25% | GT | 1,0 / 2,0 / 3,0 | 0,03 / **0,10** / 0,38 |
| **Tổng** | | | | | | | **2,5 / 10,6 / 45,7** |

Tier mix (Base): T1 68%, T2 13%, T3 18%, T4 1%

### 3.3. HC-NS-Pháp chế (260 người)

| Tác vụ | Tier | Khối lượng/ngày V (L / B / H) | Nguồn V | Tỷ lệ giao AI s (L / B / H) | Nguồn s | Turn/tác vụ t (L / B / H) | = Request/người/ngày (L / B / H) |
|---|---|---|---|---|---|---|---|
| Soạn/trả lời email | T1 | 2,9 / 9,9 / 34,0 | W4 / W5 / W2 | 10% / 16% / 24% | D1 | 1,0 / 2,0 / 3,0 | 0,29 / **3,2** / 24,5 |
| Tóm tắt/triage email & thread | T1 | 32,2 | W3 | 2% / 5% / 10% | GT | 1,0 | 0,64 / **1,6** / 3,2 |
| Hỏi đáp tài liệu nội bộ (thay tìm kiếm) | T1 | 1,7 / 4,0 / 5,0 | W9–W11 (suy ra) | 15% / 30% / 50% | GT | 1,0 / 2,0 / 3,0 | 0,26 / **2,4** / 7,5 |
| Biên bản/tóm tắt cuộc họp → DOCX | T2 | 2,0 | W6 | 10% / 20% / 40% | GT | 2,0 / 3,0 / 5,0 | 0,40 / **1,2** / 4,0 |
| Báo cáo/tờ trình/đề xuất → DOCX/PPTX | T2 | 0,15 | W8 | 30% / 50% / 80% | D3,D9 | 2,0 / 3,0 / 5,0 | 0,09 / **0,23** / 0,61 |
| Soạn JD/thông báo tuyển dụng, chính sách | T1 | 0,30 | GT | 10% / 30% / 60% | D1 | 1,0 / 2,0 / 3,0 | 0,03 / **0,18** / 0,54 |
| Rà soát hợp đồng/văn bản pháp lý (Q&A trên tài liệu) | T1 | 0,50 | GT | 5% / 15% / 30% | D3b | 1,0 / 2,0 / 3,0 | 0,03 / **0,15** / 0,45 |
| Tổng hợp chấm công/nhân sự trên Excel | T3 | 0,20 | GT | 20% / 40% / 60% | GT | 3,0 / 4,0 / 6,0 | 0,12 / **0,32** / 0,72 |
| Agent đặt lịch phỏng vấn/onboarding | T4 | 0,50 | GT | 5% / 10% / 25% | GT | 1,0 / 2,0 / 3,0 | 0,03 / **0,10** / 0,38 |
| **Tổng** | | | | | | | **1,9 / 9,4 / 41,9** |

Tier mix (Base): T1 80%, T2 15%, T3 3%, T4 1%

### 3.4. Marketing (200 người)

| Tác vụ | Tier | Khối lượng/ngày V (L / B / H) | Nguồn V | Tỷ lệ giao AI s (L / B / H) | Nguồn s | Turn/tác vụ t (L / B / H) | = Request/người/ngày (L / B / H) |
|---|---|---|---|---|---|---|---|
| Soạn/trả lời email | T1 | 2,9 / 9,9 / 34,0 | W4 / W5 / W2 | 10% / 16% / 24% | D1 | 1,0 / 2,0 / 3,0 | 0,29 / **3,2** / 24,5 |
| Tóm tắt/triage email & thread | T1 | 32,2 | W3 | 2% / 5% / 10% | GT | 1,0 | 0,64 / **1,6** / 3,2 |
| Hỏi đáp tài liệu nội bộ (thay tìm kiếm) | T1 | 1,7 / 4,0 / 5,0 | W9–W11 (suy ra) | 15% / 30% / 50% | GT | 1,0 / 2,0 / 3,0 | 0,26 / **2,4** / 7,5 |
| Biên bản/tóm tắt cuộc họp → DOCX | T2 | 2,0 | W6 | 10% / 20% / 40% | GT | 2,0 / 3,0 / 5,0 | 0,40 / **1,2** / 4,0 |
| Báo cáo/tờ trình/đề xuất → DOCX/PPTX | T2 | 0,15 | W8 | 30% / 50% / 80% | D3,D9 | 2,0 / 3,0 / 5,0 | 0,09 / **0,23** / 0,61 |
| Viết nội dung (post, PR, landing copy) | T1 | 2,0 | GT | 14% / 24% / 40% | D1 | 1,0 / 2,0 / 3,0 | 0,28 / **0,96** / 2,4 |
| Ảnh/mockup/banner | T5 | 1,0 | GT | 10% / 25% / 50% | D5,D6 | 2,0 / 3,0 / 4,0 | 0,20 / **0,75** / 2,0 |
| Phân tích số liệu campaign | T3 | 0,30 | GT | 20% / 40% / 60% | D4 | 3,0 / 4,0 / 6,0 | 0,18 / **0,48** / 1,1 |
| Agent cập nhật kế hoạch trên Notion/Confluence | T4 | 0,50 | GT | 5% / 15% / 30% | GT | 1,0 / 2,0 / 3,0 | 0,03 / **0,15** / 0,45 |
| **Tổng** | | | | | | | **2,4 / 10,9 / 45,7** |

Tier mix (Base): T1 74%, T2 13%, T3 4%, T4 1%, T5 7%

### 3.5. QLDA/Vận hành (300 người)

| Tác vụ | Tier | Khối lượng/ngày V (L / B / H) | Nguồn V | Tỷ lệ giao AI s (L / B / H) | Nguồn s | Turn/tác vụ t (L / B / H) | = Request/người/ngày (L / B / H) |
|---|---|---|---|---|---|---|---|
| Soạn/trả lời email | T1 | 2,9 / 9,9 / 34,0 | W4 / W5 / W2 | 10% / 16% / 24% | D1 | 1,0 / 2,0 / 3,0 | 0,29 / **3,2** / 24,5 |
| Tóm tắt/triage email & thread | T1 | 32,2 | W3 | 2% / 5% / 10% | GT | 1,0 | 0,64 / **1,6** / 3,2 |
| Hỏi đáp tài liệu nội bộ (thay tìm kiếm) | T1 | 1,7 / 4,0 / 5,0 | W9–W11 (suy ra) | 15% / 30% / 50% | GT | 1,0 / 2,0 / 3,0 | 0,26 / **2,4** / 7,5 |
| Biên bản/tóm tắt cuộc họp → DOCX | T2 | 2,0 | W6 | 10% / 20% / 40% | GT | 2,0 / 3,0 / 5,0 | 0,40 / **1,2** / 4,0 |
| Báo cáo/tờ trình/đề xuất → DOCX/PPTX | T2 | 0,15 | W8 | 30% / 50% / 80% | D3,D9 | 2,0 / 3,0 / 5,0 | 0,09 / **0,23** / 0,61 |
| Agent tạo/cập nhật ticket Jira, trang Confluence | T4 | 3,0 | GT | 5% / 15% / 30% | GT | 1,0 / 2,0 / 3,0 | 0,15 / **0,90** / 2,7 |
| Báo cáo tiến độ tuần → DOCX/PPTX | T2 | 0,20 | GT (1 báo cáo/tuần) | 30% / 50% / 80% | D3 | 2,0 / 3,0 / 5,0 | 0,12 / **0,30** / 0,80 |
| Sơ đồ quy trình/Gantt/diagram | T5 | 0,20 | GT | 20% / 40% / 60% | GT | 2,0 / 3,0 / 4,0 | 0,08 / **0,24** / 0,48 |
| Phân tích dữ liệu vận hành trên Excel | T3 | 0,30 | GT | 20% / 40% / 60% | GT | 3,0 / 4,0 / 6,0 | 0,18 / **0,48** / 1,1 |
| **Tổng** | | | | | | | **2,2 / 10,5 / 44,8** |

Tier mix (Base): T1 68%, T2 16%, T3 5%, T4 9%, T5 2%

### 3.6. Mua hàng/Chuỗi cung ứng (200 người)

| Tác vụ | Tier | Khối lượng/ngày V (L / B / H) | Nguồn V | Tỷ lệ giao AI s (L / B / H) | Nguồn s | Turn/tác vụ t (L / B / H) | = Request/người/ngày (L / B / H) |
|---|---|---|---|---|---|---|---|
| Soạn/trả lời email | T1 | 2,9 / 9,9 / 34,0 | W4 / W5 / W2 | 10% / 16% / 24% | D1 | 1,0 / 2,0 / 3,0 | 0,29 / **3,2** / 24,5 |
| Tóm tắt/triage email & thread | T1 | 32,2 | W3 | 2% / 5% / 10% | GT | 1,0 | 0,64 / **1,6** / 3,2 |
| Hỏi đáp tài liệu nội bộ (thay tìm kiếm) | T1 | 1,7 / 4,0 / 5,0 | W9–W11 (suy ra) | 15% / 30% / 50% | GT | 1,0 / 2,0 / 3,0 | 0,26 / **2,4** / 7,5 |
| Biên bản/tóm tắt cuộc họp → DOCX | T2 | 2,0 | W6 | 10% / 20% / 40% | GT | 2,0 / 3,0 / 5,0 | 0,40 / **1,2** / 4,0 |
| Báo cáo/tờ trình/đề xuất → DOCX/PPTX | T2 | 0,15 | W8 | 30% / 50% / 80% | D3,D9 | 2,0 / 3,0 / 5,0 | 0,09 / **0,23** / 0,61 |
| So sánh báo giá/đánh giá NCC theo PO | T3 | 1,3 / 2,8 / 5,5 | W17 | 10% / 20% / 40% | GT | 3,0 / 4,0 / 6,0 | 0,38 / **2,2** / 13,3 |
| Soạn RFQ/email NCC theo PO | T1 | 1,3 / 2,8 / 5,5 | W17 | 10% / 16% / 24% | D1 | 1,0 / 2,0 / 3,0 | 0,13 / **0,88** / 4,0 |
| Agent theo dõi PO/nhắc giao hàng | T4 | 0,50 | GT | 5% / 10% / 25% | GT | 1,0 / 2,0 / 3,0 | 0,03 / **0,10** / 0,38 |
| **Tổng** | | | | | | | **2,2 / 11,8 / 57,4** |

Tier mix (Base): T1 68%, T2 12%, T3 19%, T4 1%

### 3.7. IT (dev/QA/hạ tầng) (200 người)

| Tác vụ | Tier | Khối lượng/ngày V (L / B / H) | Nguồn V | Tỷ lệ giao AI s (L / B / H) | Nguồn s | Turn/tác vụ t (L / B / H) | = Request/người/ngày (L / B / H) |
|---|---|---|---|---|---|---|---|
| Soạn/trả lời email | T1 | 2,9 / 9,9 / 34,0 | W4 / W5 / W2 | 10% / 16% / 24% | D1 | 1,0 / 2,0 / 3,0 | 0,29 / **3,2** / 24,5 |
| Tóm tắt/triage email & thread | T1 | 32,2 | W3 | 2% / 5% / 10% | GT | 1,0 | 0,64 / **1,6** / 3,2 |
| Hỏi đáp tài liệu nội bộ (thay tìm kiếm) | T1 | 1,7 / 4,0 / 5,0 | W9–W11 (suy ra) | 15% / 30% / 50% | GT | 1,0 / 2,0 / 3,0 | 0,26 / **2,4** / 7,5 |
| Biên bản/tóm tắt cuộc họp → DOCX | T2 | 2,0 | W6 | 10% / 20% / 40% | GT | 2,0 / 3,0 / 5,0 | 0,40 / **1,2** / 4,0 |
| Báo cáo/tờ trình/đề xuất → DOCX/PPTX | T2 | 0,15 | W8 | 30% / 50% / 80% | D3,D9 | 2,0 / 3,0 / 5,0 | 0,09 / **0,23** / 0,61 |
| Viết/sửa code trong sandbox theo PR (⅔ bộ phận là dev/QA) | T3 | 0,27 | W14 | 51% / 59% / 90% | D7,D8,D11; t: D12 | 4,1 / 8,2 / 12,3 | 0,56 / **1,3** / 3,0 |
| Review code/PR (⅔ dev/QA) | T3 | 0,40 | W15 | 30% / 50% / 70% | GT | 1,0 / 2,0 / 3,0 | 0,12 / **0,40** / 0,84 |
| Xử lý ticket hỗ trợ IT: tra cứu/triage (⅓ hạ tầng/support) | T1 | 1,3 / 1,5 / 2,0 | W13 | 20% / 40% / 60% | GT (D4) | 1,0 / 2,0 / 3,0 | 0,26 / **1,2** / 3,6 |
| Agent tạo/cập nhật ticket Jira, runbook Confluence | T4 | 1,0 | GT | 10% / 20% / 40% | GT | 1,0 / 2,0 / 3,0 | 0,10 / **0,40** / 1,2 |
| Diagram kiến trúc/flow | T5 | 0,10 | GT | 30% / 50% / 70% | GT | 2,0 / 3,0 / 4,0 | 0,06 / **0,15** / 0,28 |
| **Tổng** | | | | | | | **2,8 / 12,1 / 48,7** |

Tier mix (Base): T1 70%, T2 12%, T3 14%, T4 3%, T5 1%

### 3.8. Lãnh đạo & trợ lý (100 người)

| Tác vụ | Tier | Khối lượng/ngày V (L / B / H) | Nguồn V | Tỷ lệ giao AI s (L / B / H) | Nguồn s | Turn/tác vụ t (L / B / H) | = Request/người/ngày (L / B / H) |
|---|---|---|---|---|---|---|---|
| Soạn/trả lời email | T1 | 2,9 / 9,9 / 34,0 | W4 / W5 / W2 | 10% / 16% / 24% | D1 | 1,0 / 2,0 / 3,0 | 0,29 / **3,2** / 24,5 |
| Tóm tắt/triage email & thread | T1 | 32,2 | W3 | 2% / 5% / 10% | GT | 1,0 | 0,64 / **1,6** / 3,2 |
| Hỏi đáp tài liệu nội bộ (thay tìm kiếm) | T1 | 1,7 / 4,0 / 5,0 | W9–W11 (suy ra) | 15% / 30% / 50% | GT | 1,0 / 2,0 / 3,0 | 0,26 / **2,4** / 7,5 |
| Biên bản/tóm tắt cuộc họp → DOCX | T2 | 4,6 | W6 | 10% / 20% / 40% | GT | 2,0 / 3,0 / 5,0 | 0,92 / **2,8** / 9,2 |
| Báo cáo/tờ trình/đề xuất → DOCX/PPTX | T2 | 0,15 | W8 | 30% / 50% / 80% | D3,D9 | 2,0 / 3,0 / 5,0 | 0,09 / **0,23** / 0,61 |
| Bản tóm tắt điều hành/briefing trước họp | T1 | 4,6 | W7 | 10% / 20% / 40% | GT | 1,0 | 0,46 / **0,92** / 1,8 |
| Agent sắp lịch/Calendar (trợ lý) | T4 | 1,0 | GT | 10% / 20% / 40% | GT | 1,0 / 2,0 / 3,0 | 0,10 / **0,40** / 1,2 |
| Slide trình bày → PPTX | T2 | 0,20 | GT | 30% / 50% / 80% | D3 | 2,0 / 3,0 / 5,0 | 0,12 / **0,30** / 0,80 |
| **Tổng** | | | | | | | **2,9 / 11,8 / 48,8** |

Tier mix (Base): T1 69%, T2 28%, T4 3%


**Giả định chia nhóm trong phòng ban (GT):** Sales & CSKH: ½ là CSKH (dòng chat nhân 0,5). Kế toán: ⅓ là AP (dòng hóa đơn chia 3). IT: ⅔ dev/QA (PR, review nhân ⅔), ⅓ hạ tầng/support (ticket chia 3). Tỷ lệ thật cần lấy từ HRIS của tập đoàn.

---

## 4. Tổng theo phòng ban, bình quân toàn công ty, tier mix

### 4.1. Request (user turn) / người / ngày

| Phòng ban | Số người | Low | **Base** | High | Request/ngày cả phòng (Base) | Tier mix Base % (T1 / T2 / T3 / T4 / T5) |
|---|---|---|---|---|---|---|
| Sales & CSKH | 500 | 2,5 | **10,3** | 43,8 | 5168 | 80 / 14 / 4 / 2 / 1 |
| Kế toán/Tài chính | 240 | 2,5 | **10,6** | 45,7 | 2546 | 68 / 13 / 18 / 1 / 0 |
| HC-NS-Pháp chế | 260 | 1,9 | **9,4** | 41,9 | 2433 | 80 / 15 / 3 / 1 / 0 |
| Marketing | 200 | 2,4 | **10,9** | 45,7 | 2189 | 74 / 13 / 4 / 1 / 7 |
| QLDA/Vận hành | 300 | 2,2 | **10,5** | 44,8 | 3158 | 68 / 16 / 5 / 9 / 2 |
| Mua hàng/Chuỗi cung ứng | 200 | 2,2 | **11,8** | 57,4 | 2360 | 68 / 12 / 19 / 1 / 0 |
| IT (dev/QA/hạ tầng) | 200 | 2,8 | **12,1** | 48,7 | 2412 | 70 / 12 / 14 / 3 / 1 |
| Lãnh đạo & trợ lý | 100 | 2,9 | **11,8** | 48,8 | 1179 | 69 / 28 / 0 / 3 / 0 |
| **Toàn công ty (bình quân gia quyền)** | **2000** | **2,4** | **10,7** | **46,2** | **21445** | 73 / 15 / 8 / 3 / 1 |

Phép tính bình quân gia quyền: Σ(số người × request/người) ÷ 2.000. Base: 21.445 ÷ 2.000 = **10,7 request/người/ngày**. Low: 4.745 ÷ 2.000 = 2,4. High: 92.433 ÷ 2.000 = 46,2.

Theo tháng (22 ngày): Low ≈ **104 nghìn**, Base ≈ **472 nghìn**, High ≈ **2,03 triệu** request.

### 4.2. Tier mix toàn công ty

| Tier | Low | **Base** | High | Request/ngày (Base) |
|---|---|---|---|---|
| T1 | 60,0% | 73,1% | 79,9% | 15683 |
| T2 | 22,7% | 14,5% | 10,8% | 3116 |
| T3 | 12,7% | 8,2% | 6,4% | 1760 |
| T4 | 2,6% | 2,8% | 2,1% | 590 |
| T5 | 2,0% | 1,4% | 0,8% | 297 |

### 4.3. Kiểm tra chéo và độ nhạy

| Kiểm tra | Kết quả |
|---|---|
| So với top-down ở UB mục 6.1 (Low 5 / Base 12 / High 30) | Base bottom-up **10,7** ≈ Base top-down 12. Low bottom-up (2,4) **thấp hơn** DBT ≈ 3,8 action/active user/ngày (UB#3): kịch bản Low ở đây tương đương người dùng mới, chưa quen công cụ |
| So với ngưỡng Microsoft (D2) | Power user ≥ 15 action/tuần = **≥ 3/ngày**. Base 10,7 turn/ngày ≈ 3,5 lần ngưỡng power user. Lưu ý đơn vị khác nhau: 1 action Copilot có thể là 1 nút bấm; 1 turn VBot là 1 prompt |
| Tier mix so với DBT diary (UB mục 2.1: T1 73%, T2 14%, T3 4,6%, T4 1%, T5 1,5%) | Base bottom-up: T1 73%, T2 15%, T3 8%, T4 3%, T5 1%. Gần như trùng; T3 cao hơn vì có phòng Kế toán, Mua hàng, IT. **T4 chỉ 2,8%**, thấp hơn mức 6% giả định ở UB mục 6.2, vì gần như mọi dòng T4 là GT với s thấp |
| Biến chi phối | "Soạn/trả lời email" chiếm **~30%** request ở Base và **>50%** ở High (34 email gửi × 24% × 3 turn = 24,5 turn/người). Biến nhạy nhất là **số email gửi thật/ngày** (dải 2,9–34 gấp 12 lần) |
| High "thực tế" hơn | Giữ V ở Base, chỉ đẩy s và t lên High → **26,4 request/người/ngày** (52,9 nghìn/ngày; ~1,16 triệu/tháng). Con số này gần High top-down (30, UB mục 6.1) và hợp lý hơn để làm **capacity target** so với 46,2 |
| Phạm vi | Số trên tính trên **người dùng active trong ngày** (đúng định nghĩa DAU của VBot). Theo D10/D16, chỉ 12–20% người lao động dùng AI hằng ngày ở Mỹ/Âu; nếu VBot đếm DAU = 2.000 trên tổng nhân sự lớn hơn thì số này đúng; nếu 2.000 là tổng license, cần nhân tỷ lệ DAU/license (DBT: 30%, UB#2) |

---

## 5. Gaps và danh sách giả định

### 5.1. GAP — không tìm thấy dữ liệu đáng tin

1. **Khối lượng email/họp/tài liệu theo phòng ban:** chỉ có trung bình toàn bộ M365 (W1, W3–W8). Không có số email gửi theo vai trò (sales, HR, mua hàng…).
2. **Tỷ lệ email soạn/tóm tắt bằng AI trong doanh nghiệp:** không có. D1 đo văn bản công khai, không đo email nội bộ.
3. **Tỷ lệ cuộc họp được recap bằng AI:** không có nguồn primary (một số con số "70% tổ chức dùng recap", "43% user tóm tắt email" chỉ xuất hiện trên blog không rõ nguồn — không dùng).
4. **Số prompt/ngày theo vai trò (phần C của đề bài):** **không có** nguồn nào công bố. Gần nhất là ngưỡng power user Microsoft (D2), tỷ lệ P95/median theo loại tác vụ của OpenAI (UB#12), và Claude Code human turn/transcript (D12). Glean "14 query/ngày" (UB#17) vẫn không có nguồn primary.
5. **Số lượt tìm kiếm thông tin/ngày:** chỉ có % thời gian (W9–W11); quy đổi ra lượt dựa trên 24 phút/lượt (D13) là phép quy đổi thô.
6. **HR, pháp chế, marketing, QLDA:** không có benchmark khối lượng đáng tin (số JD, câu hỏi chính sách, hợp đồng, bài content, ticket Jira/người/ngày). APQC có các measure liên quan nhưng sau paywall.
7. **Số ticket Jira/Confluence page mỗi người QLDA tạo/sửa:** không có. Đây là input chính của T4 → tỷ lệ agent là phần yếu nhất của mô hình.
8. **Dữ liệu Việt Nam:** chỉ có D18 (88% có dùng GenAI). Không có telemetry email/họp của doanh nghiệp Việt Nam; thói quen dùng Zalo thay email có thể làm W1–W5 **cao hơn thực tế** cho VBot.
9. **Radicati per-user hiện tại:** bản 2024–2028 không công khai số email/business user/ngày; số dùng ở đây là bản 2015 (W2).

### 5.2. Số liệu là giả định (GT) — cần đo trong pilot

| Nhóm | Giả định | Ảnh hưởng |
|---|---|---|
| s cho tóm tắt email | 2 / 5 / 10% số email đọc | Trung bình (1,6 turn/người ở Base) |
| s cho Q&A tài liệu | 15 / 30 / 50% số lượt tìm kiếm | Lớn (2,4 turn/người ở Base) |
| s cho biên bản họp | 10 / 20 / 40% số cuộc họp | Trung bình; tăng mạnh nếu VBot tích hợp transcript Teams/Meet |
| Toàn bộ V có nhãn GT | phân tích pipeline 0,2/ngày; agent CRM 1,0; JD 0,3; hợp đồng 0,5; content 2,0; ảnh marketing 1,0; Jira 3,0 (QLDA) / 1,0 (IT); briefing exec = số họp; slide exec 0,2… | Từng dòng nhỏ, nhưng **quyết định toàn bộ T4 và T5** |
| t cho mọi tier | T1 1–3; T2 2–5; T3 3–6; T4 1–3; T5 2–4 | Lớn: t nhân thẳng vào tổng |
| Số giờ/cuộc họp của exec | 1 giờ (để quy đổi W7) | Chỉ ảnh hưởng 100 người |
| Cơ cấu trong phòng ban | ½ CSKH, ⅓ AP, ⅔ dev/QA | Nhỏ |
| FP&A áp cho toàn phòng Kế toán | 2 giờ bảng tính/ngày cho mọi người (W18 là FP&A, tin cậy C) | Trung bình cho 240 người |

### 5.3. Đề xuất đo trong pilot (2–4 tuần)

- Gắn mỗi turn với **department** (từ HRIS) và **task type** (router của VBot đã phân tier) → thay toàn bộ cột s × t bằng số đo.
- Lấy V thực từ chính connector: số email đọc/gửi (Gmail/M365 API), số cuộc họp (Calendar), số ticket/page tạo (Jira/Confluence audit log) theo phòng ban → chia ra s thực = tác vụ VBot ÷ V.
- So DAU/license theo phòng ban với D10 (leader 69% vs IC 40%) và D3b (HR/Commercial cao, Legal/Policy thấp) để kiểm tra giả định "mọi phòng ban có cường độ như nhau".
