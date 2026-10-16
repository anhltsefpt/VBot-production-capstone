# R8 + R6: Chi phí/giới hạn API của 11 connector và chi phí nhân sự vận hành tại Việt Nam

> Ngày tổng hợp và truy cập mọi nguồn: **2026-10-16**. Phục vụ D4 (connector hybrid, OAuth ủy quyền của user), D18 (license SaaS đã có, chỉ tính API trả theo lượt), D7/D8 (2 FTE, tổng chi phí công ty trả).
>
> Quy ước: mỗi số có **giá trị, định nghĩa, nguồn [Sx], ngày cập nhật của trang**. Danh sách nguồn ở mục 5. Dòng ghi **(suy ra)** là phép tính của người tổng hợp, không phải số do nguồn công bố. Chỗ không có dữ liệu: **KHÔNG TÌM THẤY** kèm URL đã kiểm tra.

---

## 1. Kết luận nhanh

1. **Không connector nào có phí API theo lượt cho kiểu dùng của VBot** (đọc/tìm/ghi bằng token ủy quyền của user) tại ngày 2026-10-16.
   - Microsoft Graph: từ **25/08/2025, Teams APIs không còn metered**. API metered duy nhất còn lại là `assignSensitivityLabel` của SharePoint/OneDrive: **0,00185 USD/lần gọi**, VBot không dùng API này [S1].
   - Google Workspace: "All standard use ... is available at no additional cost". Phần dùng **vượt ngưỡng hằng ngày** của Gmail/Drive/Calendar "is planned to incur charges ... later in 2026", **chưa công bố giá** và sẽ báo trước ít nhất 90 ngày [S8][S9][S10][S11].
   - Atlassian (Jira/Confluence): giới hạn theo điểm (points), **không có tầng trả phí** [S20][S21].
   - Notion: trang rate limit không nêu giá API [S27].
2. **Rủi ro chính là rate limit, không phải chi phí.** Hai điểm dễ nghẽn nhất:
   - Atlassian OAuth 3LO Tier 1: **65.000 điểm/giờ dùng chung cho mọi tenant**. Muốn quota theo tenant (Tier 2) thì phải qua Atlassian review [S20][S21].
   - Notion: **180 request/phút/connection** (gói không phải Business/Enterprise) hoặc **600 request/phút/connection** (Business/Enterprise) [S27].
3. **Chi phí CASA ≈ 0 USD nếu OAuth app Google để ở chế độ Internal.** App "only used by people in your Google Workspace or Cloud Identity organization" được miễn verification [S14]. Chỉ khi app ở chế độ External và dùng scope restricted (`gmail.readonly`, `drive.readonly`, …) mới phải làm CASA hằng năm: TAC Security niêm yết **675 USD (Basic Tier 2)**, **855 USD (Premium Tier 2)**, **3.600 USD (Tier 3)** mỗi app [S15]. Leviathan niêm yết **3.000 / 4.500 / 6.000 USD** cho gói AL1 [S16].
4. **Chi phí 2 FTE (gross + phần công ty đóng bắt buộc), tính từ ITviec 2024–2025 (median gross):**
   - Thấp: **104,48 triệu VND/tháng ≈ 4.039 USD/tháng**
   - Cơ sở: **132,91 triệu VND/tháng ≈ 5.138 USD/tháng**
   - Cao: **179,12 triệu VND/tháng ≈ 6.924 USD/tháng**
   - Cách tính ở mục 4.

---

## 2. Bảng connector (R8)

Ghi chú chung cho Microsoft Graph:
- Giới hạn toàn cục: **130.000 request / 10 giây / app, tính trên mọi tenant** [S3].
- Change notifications (webhook) có thời hạn subscription tối đa theo từng resource [S6].
- Mọi permission ủy quyền (delegated) liệt kê dưới đây có `AdminConsentRequired = No`, trừ khi ghi khác [S5]. Tuy vậy, tenant có thể tắt quyền tự consent của user; khi đó admin phải consent. Microsoft khuyến nghị chỉ cho user consent với app của verified publisher [S7].

| Connector | Phí metered | Rate limit / quota | Search API | Webhook | Scope tối thiểu (đọc / ghi) | Verification / chi phí | Nguồn |
|---|---|---|---|---|---|---|---|
| **Gmail** | 0 USD trong ngưỡng. Ngưỡng **80.000.000 quota unit/ngày/project**, không xin tăng được. Vượt ngưỡng: dự kiến tính phí "later in 2026", **giá: KHÔNG TÌM THẤY** | **1.200.000 unit/phút/project**; **6.000 unit/phút/user/project**. Chi phí mỗi lệnh: `messages.list` 5, `messages.get` 20, `threads.get` 40, `threads.list` 10, `history.list` 2, `messages.modify` 5, `drafts.create` 10, `drafts.send` 100, `messages.send` 100, `watch` 100 | `users.messages.list?q=` dùng cú pháp ô tìm kiếm Gmail; `maxResults` mặc định 100, tối đa 500. **Không dùng được `q` với scope `gmail.metadata`** | Push qua Cloud Pub/Sub. Phải gọi `watch` ít nhất 7 ngày/lần. Tối đa **1 event/giây/user**, vượt thì bị bỏ | Đọc: `gmail.readonly` (**restricted**). Nháp: `gmail.compose` (**restricted**). Gửi: `gmail.send` (**sensitive**). `gmail.metadata` là sensitive nhưng không search được | Internal app: **miễn verification**. External + restricted: CASA hằng năm (giá ở mục 1.3) | S8, S12, S17, S18, S14, S15 |
| **Google Drive** | 0 USD trong ngưỡng **400.000.000 unit/24h/project**. Vượt ngưỡng: dự kiến tính phí năm 2026, **giá: KHÔNG TÌM THẤY** | **1.000.000 unit/phút/project**; **325.000 unit/phút/user/project**. Read (`files.get`) 5, List (`files.list`) 100, Download 200, Edit 50. Upload tối đa 750 GB/user/ngày | `files.list?q=` có `fullText contains`. Chỉ trả về file user có quyền. `corpora` mặc định `user`; khi gộp nhiều corpora có thể bị `incompleteSearch` | `changes.watch` (tối đa 1 tuần), `files.watch` (tối đa 1 ngày). Bắt buộc HTTPS | Đọc toàn Drive: `drive.readonly` (**restricted**). Chỉ file app mở/tạo: `drive.file` (**non-sensitive**). Ghi toàn Drive: `drive` (**restricted**) | Như Gmail | S9, S13, S19, S22, S14 |
| **Google Calendar** | 0 USD trong ngưỡng **1.000.000 request/ngày/project**. Vượt ngưỡng: dự kiến tính phí năm 2026, **giá: KHÔNG TÌM THẤY** | **10.000 request/phút/project**; **600 request/phút/user/project** | `events.list` có tham số `q`: **chưa đối chiếu trang reference** (xem mục 6) | `watch` cho Events/ACL/CalendarList/Settings. Không tự gia hạn channel; Google nói "not 100% reliable" | Đọc: `calendar.events.readonly` hoặc `calendar.readonly`. Ghi: `calendar.events`. Phân loại sensitive/restricted: **KHÔNG TÌM THẤY** trên trang scopes | Internal app: miễn | S10, S23, S24, S14 |
| **Google Docs / Sheets / Slides** | 0 USD. Có câu "planned to incur charges later in 2026" khi vượt quota; **không có ngưỡng ngày**: "no limit to the number of requests ... per day" (Sheets, Slides) | Docs: đọc 3.000/phút/project, **300/phút/user**; ghi 600/phút/project, **60/phút/user**. Sheets: đọc và ghi đều **300/phút/project, 60/phút/user**. Slides: đọc 3.000 / **600/user**; ghi 600 / **60/user**; `getThumbnail` 300 / 60 | Không có search riêng; tìm file qua Drive `files.list` | Qua Drive `files.watch` / `changes.watch` | `documents.readonly` / `documents` (**sensitive**); `drive.file` (**non-sensitive**) | Internal app: miễn. External + sensitive: phải verification. S14b chỉ yêu cầu security assessment với restricted scope, nên **(suy ra)** không cần CASA | S11, S25, S14 |
| **Outlook mail + calendar (Graph)** | **0 USD.** Standard API "available as part of the user license without additional costs" | Mỗi cặp app + mailbox: **10.000 request / 10 phút**; **4 request đồng thời**; upload 150 MB / 5 phút | `/search/query` với entity `message` / `event`: tối đa **25 kết quả/trang**. Kết quả chỉ gồm item user có quyền | Subscription cho message/event tối đa **10.080 phút** (<7 ngày); có resource data thì **1.440 phút** | Đọc: `Mail.Read` (hoặc `Mail.ReadBasic`, không có body), `Calendars.Read`. Ghi: `Mail.ReadWrite`, `Mail.Send`, `Calendars.ReadWrite`. Thêm `offline_access`, `User.Read`. **Delegated: không cần admin consent** | Không có phí. Có thể cần admin consent tùy chính sách tenant | S2, S4, S26, S6, S5, S7 |
| **Microsoft 365 / Graph chung** | Chỉ `assignSensitivityLabel` có phí: **0,00185 USD/lần gọi**. Copilot connectors: synced connector "no extra cost" cho tenant M365 (chỉ phục vụ Microsoft Search). Federated connector cần license **Microsoft 365 Copilot add-on cho mọi user** (giá add-on: không thu thập trong phạm vi này) | **130.000 request/10 giây/app** trên mọi tenant | `/search/query` (Microsoft Search API): chạy bằng token delegated, kết quả theo quyền của user. Mỗi request chỉ chứa 1 `searchRequest` | Có (xem các dòng khác) | Theo từng workload | — | S1, S2, S3, S28 |
| **OneDrive / SharePoint** | 0 USD (trừ `assignSensitivityLabel`) | Chi phí theo **resource unit (RU)**: get item / delta có token = 1 RU; list / tạo / sửa / xóa = 2 RU; mọi thao tác permission = 5 RU. **Mỗi app/tenant** (tenant 1.001–5.000 license): **2.500 RU/phút**, **2.400.000 RU/24h**; 5.001–15.000 license: 3.750 RU/phút, 3.600.000 RU/24h. **Mỗi user**: 3.000 request / 5 phút. **Search delegated: tối đa 10 request/giây/user** | `/search/query` với entity `driveItem` / `listItem` / `site`: tối đa **1.000 kết quả/trang** (khuyến nghị 200) | Subscription `driveItem` / SharePoint `list` tối đa **42.300 phút** (<30 ngày) | Đọc: `Files.Read.All` hoặc `Sites.Read.All`. Ghi: `Files.ReadWrite.All` / `Sites.ReadWrite.All`. **Delegated: không cần admin consent** | Không | S1, S29, S26, S6, S5 |
| **Microsoft Teams** | **0 USD từ 25/08/2025** ("Teams APIs are no longer metered") | Mặc định GET: **1.500 rps/app**, **30 rps/app/tenant**, **1 rps/chat hoặc channel**, **1 rps/user**. `GET /chats/{id}/messages`: 20 rps/app/tenant, 1 rps/chat. `POST` chat message: **1 rps/user**. Tải liên tục bị đánh giá ở ≈83% mức niêm yết | `/search/query` với entity `chatMessage` (scope `Chat.Read` / `ChannelMessage.Read.All`). Không gộp được với entity khác | Subscription `chatMessage` / `chat` / `channel` tối đa **4.320 phút** (3 ngày) | Đọc chat: `Chat.Read` (không cần admin consent). Đọc channel: `ChannelMessage.Read.All` (**delegated vẫn cần admin consent**). Gửi: `ChatMessage.Send`, `ChannelMessage.Send` | Cần admin consent cho channel | S1, S30, S26, S6, S5 |
| **Notion** | Trang rate limit không nêu giá API → không thấy phí metered | Mỗi connection: **600 request/phút** (Business, Enterprise) hoặc **180 request/phút** (gói khác), dùng dồn một lúc cũng được. Có thêm giới hạn chung toàn workspace (không công bố số). Payload tối đa 1.000 block và 500 KB | `POST /v1/search`: **chỉ tìm theo tiêu đề**. Có thể trả `incomplete` khi gặp `query_result_limit_reached` | Có webhooks (`page.content_updated` được gộp và gửi trễ; `comment.created` gửi trong vài giây). Áp dụng cho loại integration nào: **KHÔNG TÌM THẤY** | Capability: Read / Update / Insert content; Read / Insert comments; user info có hoặc không có email. Public integration dùng OAuth; user tự chọn page để chia sẻ | Có cần review khi phát hành public integration không: **KHÔNG TÌM THẤY** | S27, S31, S32, S33, S34 |
| **Jira Cloud** | Không có tầng trả phí; hạn mức tính theo điểm, từ **02/03/2026** | **Tier 1 (mặc định): 65.000 điểm/giờ, dùng chung mọi tenant.** Tier 2 (theo tenant, **phải qua Atlassian review**): Standard 100.000 + 10×user; Premium 130.000 + 20×user; Enterprise 150.000 + 30×user; tối đa 500.000 điểm/giờ. Mỗi GET/ghi = 1 điểm; GET nhóm identity = 2 điểm. Burst: GET/POST 100 rps, PUT/DELETE 50 rps. Mỗi issue: 20 lần ghi / 2 giây. Traffic bằng API token không thuộc mô hình này | JQL qua `/rest/api/3/search/jql` (granular scope `read:jql:jira`) | Dynamic webhook qua REST: hết hạn sau **30 ngày** (phải refresh), tối đa **5 webhook/app/user/tenant**, JQL filter bị giới hạn | Đọc: `read:jira-work`, `read:jira-user`. Ghi: `write:jira-work`. Webhook: `manage:jira-webhook`. Thêm `offline_access` (refresh token xoay vòng, hết hạn sau **90 ngày** không dùng) | Đăng ký app trong developer console. App chưa được Atlassian review thì user thấy cảnh báo. Không thấy phí | S20, S35, S36, S37 |
| **Confluence Cloud** | Như Jira | Như Jira: 65.000 điểm/giờ Tier 1; Tier 2 theo edition | CQL qua `GET /wiki/rest/api/search` (scope `search:confluence`); "only entities that the user has permission to view will be returned" | Webhook cho app OAuth 2.0 (3LO): **KHÔNG TÌM THẤY** (trang webhook chỉ nói về Connect; Atlassian đã ngừng nhận Connect app mới lên Marketplace) | Đọc: `search:confluence`, `read:confluence-content.all` (hoặc granular `read:page:confluence`). Ghi: `write:confluence-content` / `write:page:confluence` | Như Jira | S21, S38, S39, S40 |

### 2.1 Google: Internal app và CASA

- Trường hợp miễn verification [S14]:
  - Internal Use Apps: "The app is only used by people in your Google Workspace or Cloud Identity organization" (consent screen đặt Internal).
  - App được Workspace admin đánh dấu trusted, hoặc admin cài từ Marketplace.
- App dùng restricted scope phải "submit to an annual security assessment from a Google empanelled group of security assessors" [S14b].
- Giá CASA do các lab tự niêm yết:
  - **TAC Security** (tự nhận là "Google Preferred and Recommended ADA CASA Partner"): Basic Tier 2 **675 USD/app**, Premium Tier 2 **855 USD/app**, Enterprise Tier 3 **3.600 USD/app** [S15].
  - **Leviathan Security**: AL1 **3.000 USD** (No Rush), **4.500 USD** (Standard), **6.000 USD** (Priority); mỗi gói gồm 1 lần retest [S16].
- **Áp vào VBot (suy ra):** tập đoàn đã có Google Workspace (D18) và chỉ nhân viên dùng VBot, nên đặt OAuth app là Internal → **không cần verification, chi phí CASA = 0**. Chỉ tính CASA nếu có user ngoài tổ chức.

### 2.2 Google: thay đổi quota năm 2026 cần theo dõi

- "As of May 1, 2026, we are adjusting usage quotas across several Google Workspace product APIs, starting with Gmail API, Google Calendar API, and Google Drive API."
- "API usage over standard daily thresholds will generate charges on your Google Cloud bill."
- Google "will share full billing details later in 2026 with at least 90 days' notice".
- Project cũ giữ quota cũ ít nhất 60 days.

Nguồn: [S8][S17]. **Giá mỗi unit vượt ngưỡng: KHÔNG TÌM THẤY** (đã kiểm tra S17, S8, S9, S10).

### 2.3 Microsoft Teams: trạng thái metered

Metered API list ghi: "Starting August 25, 2025, the Teams APIs are no longer metered, and no billing configuration is required to use these APIs." [S1]. Bảng giá Teams cũ (Model A/B) không còn áp dụng, nên không thu thập.

---

## 3. Lương (R6)

### 3.1 Số liệu tìm được

Nguồn chính: ITviec, *Vietnam IT Salary & Recruitment Market Report 2024–2025* (PDF) [S41]. Khảo sát online **10/09–10/10/2024**, 2.324 người trả lời. Định nghĩa: "(*) **Median gross monthly salary (VND), excluding Bonus and other welfare benefits.**" Số năm kinh nghiệm là số năm ở **vị trí hiện tại**, không phải tổng số năm làm IT.

| Vị trí (theo nhãn ITviec) | 1–2 năm | 3–4 năm (mid) | 5–8 năm (senior) | >8 năm | Khoảng thấp–cao trong biểu đồ (đọc từ biểu đồ) |
|---|---|---|---|---|---|
| DevOps Engineer / DevSecOps Engineer (đại diện cho SRE/platform) | 30.000.000 | **50.500.000** | **53.850.000** | **84.400.000** | 3–4 năm: 30,5–52,2 tr; 5–8 năm: 35,3–75 tr; >8 năm: 41–111,9 tr |
| AI Engineer / Blockchain Engineer (đại diện cho AI/MLOps; ITviec không có nhãn MLOps riêng) | 18.100.000 | **34.100.000** | **55.200.000** | **70.400.000** | 3–4 năm: 25,5–50,4 tr; 5–8 năm: 42,9–98,2 tr |
| Cloud Engineer | N/A | N/A | N/A | 65.000.000 (<1 năm: 29.200.000) | — |
| Data Engineer | 17.800.000 | 30.100.000 | N/A | N/A | — |

- ITviec không định nghĩa hai đầu thấp/cao của khoảng trong biểu đồ (min–max hay percentile).
- Quy đổi USD theo tỷ giá Vietcombank ngày **16/10/2026, 07:58 (UTC+7)**: USD mua chuyển khoản **25.680**, bán **26.060** [S42]. Dùng **giá giữa 25.870 VND/USD** (suy ra).
  - DevOps: 3–4 năm ≈ **1.952 USD**, 5–8 năm ≈ **2.082 USD**, >8 năm ≈ **3.262 USD**/tháng gross.
  - AI Engineer: 3–4 năm ≈ **1.318 USD**, 5–8 năm ≈ **2.134 USD**, >8 năm ≈ **2.721 USD**/tháng gross.

**ITviec 2025–2026** (trang công khai; khảo sát 27/05–31/07 và 21/10–11/11/2025; 1.839 người trả lời) [S43]:
- Bảng median công khai **không có DevOps, Cloud, SRE hay AI/ML**.
- Data Engineer: median 41,3 tr; 3–4 năm 56,9 tr.
- Trang không ghi gross hay net.
- PDF đầy đủ chỉ tải được sau khi điền form.

### 3.2 Nguồn đã kiểm tra nhưng không lấy được số

| Nguồn | Kết quả |
|---|---|
| Robert Walters Vietnam Salary Survey 2026 | Trang gốc trả **HTTP 403** (https://www.robertwalters.com.vn/insights/salary-survey.html). Tuổi Trẻ News (30/11/2025) chỉ dẫn **mức tăng dự báo**: AI/data/fintech **+15–25%**, software developer **+5–15%**, không có số VND [S44]. **Số lương: KHÔNG TÌM THẤY** |
| Navigos Search Talent Guide 2025/2026 | Trang giới thiệu (18/02/2025) có nói đến bản 2026 (26/01/2026), nhưng **không có số lương IT** [S45]. **KHÔNG TÌM THẤY** |
| TopDev Vietnam IT Market Report | Không tìm thấy bảng lương DevOps/AI từ nguồn gốc TopDev. **KHÔNG TÌM THẤY** (đã tìm topdev.vn qua search) |
| Adecco Vietnam Salary Guide | adecco.com.vn/salary-guide chuyển hướng về https://www.adecco.com/en-vn, không có số. **KHÔNG TÌM THẤY** |
| Glassdoor | Chưa truy cập được (thường phải đăng nhập). **KHÔNG TÌM THẤY** |
| Talentnet | Chưa kiểm tra. **KHÔNG TÌM THẤY** |

---

## 4. Chi phí công ty đóng bắt buộc năm 2026 và tổng chi phí mỗi FTE

### 4.1 Tỷ lệ và mức trần (người lao động Việt Nam, HĐLĐ, doanh nghiệp vùng I)

| Khoản công ty đóng | Tỷ lệ | Căn cứ tính và trần | Nguồn |
|---|---|---|---|
| BHXH – quỹ ốm đau, thai sản | **3%** | Lương đóng BHXH, **trần 20 × mức tham chiếu** | Luật BHXH 41/2024/QH15, Điều 34 khoản 1a; Điều 31 khoản 1đ [S46] |
| BHXH – quỹ hưu trí, tử tuất | **14%** | Như trên | Luật BHXH 2024, Điều 34 khoản 1b [S46] |
| BHXH – quỹ TNLĐ-BNN | **0,5%** (0,3% nếu doanh nghiệp ngành rủi ro cao đủ điều kiện xin giảm) | Quỹ lương đóng BHXH | Nghị định 58/2020/NĐ-CP, Điều 4 (đã sửa bởi NĐ 158/2025) [S47] |
| BHYT | **3%** (= 2/3 của mức 4,5%) | "4,5% tiền lương tháng làm căn cứ đóng bảo hiểm xã hội bắt buộc", nên trần theo lương BHXH **(suy ra)** | Nghị định 188/2025/NĐ-CP, dẫn qua Thời báo Tài chính VN [S48] |
| BHTN | **1%** (luật ghi "tối đa 1%"; NĐ 374/2025 quy định 1%) | **Trần 20 × lương tối thiểu vùng** | Luật Việc làm 74/2025/QH15, Điều 33 khoản 1b, Điều 34 khoản 2, hiệu lực 01/01/2026 [S49]; NĐ 374/2025 (qua báo chí) [S50] |
| Kinh phí công đoàn (KPCĐ) | **2%** | "2% quỹ tiền lương làm căn cứ đóng bảo hiểm xã hội bắt buộc", tức theo trần BHXH | Luật Công đoàn 50/2024/QH15, Điều 29, hiệu lực 01/07/2025 [S51] |
| **Tổng** | **23,5%** (21,5% bảo hiểm + 2% KPCĐ) | | |

Mức trần áp dụng tại 2026-10-16:
- **Mức tham chiếu = lương cơ sở**, theo Luật BHXH 2024 Điều 141 khoản 13: "Khi chưa bãi bỏ mức lương cơ sở thì mức tham chiếu ... bằng mức lương cơ sở" [S46].
- Lương cơ sở từ **01/07/2026 là 2.530.000 VND** (Nghị định 161/2026/NĐ-CP, ban hành 15/05/2026) [S52].
  - → Trần BHXH, BHYT, KPCĐ = 20 × 2.530.000 = **50.600.000 VND/tháng** (suy ra).
  - Trước 01/07/2026 trần là 20 × 2.340.000 = 46.800.000.
- Lương tối thiểu vùng I từ **01/01/2026 là 5.310.000 VND** (Nghị định 293/2025/NĐ-CP) [S53].
  - → Trần BHTN = 20 × 5.310.000 = **106.200.000 VND/tháng** (suy ra).

Công thức (suy ra): **Phần công ty đóng = 22,5% × min(S; 50,6 tr) + 1% × min(S; 106,2 tr)**, với S là lương gross tháng. 22,5% = 17,5% BHXH + 3% BHYT + 2% KPCĐ.

### 4.2 Kịch bản

Giả định: lương đóng BHXH bằng lương gross; doanh nghiệp vùng I (Hà Nội/TP.HCM); TNLĐ-BNN 0,5%; chưa tính thưởng tháng 13, thưởng, phúc lợi (ITviec loại các khoản này).

| Kịch bản | FTE | S (gross, tr VND) | BHXH 17,5% | BHYT 3% | BHTN 1% | KPCĐ 2% | Công ty đóng | **Tổng/tháng** | ≈ USD/tháng | Tổng/năm (×12) | ≈ USD/năm |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Thấp | SRE (DevOps 3–4 năm) | 50,50 | 0,175×50,5 = 8,8375 | 1,515 | 0,505 | 1,010 | 11,8675 | **62,3675** | 2.411 | 748,41 tr | 28.930 |
| Thấp | AI/MLOps (AI Eng 3–4 năm) | 34,10 | 5,9675 | 1,023 | 0,341 | 0,682 | 8,0135 | **42,1135** | 1.628 | 505,36 tr | 19.535 |
| **Thấp – 2 FTE** | | | | | | | | **104,481** | **4.039** | **1.253,77 tr** | **48.464** |
| Cơ sở | SRE (DevOps 5–8 năm) | 53,85 | 0,175×50,6 = 8,855 | 1,518 | 0,5385 | 1,012 | 11,9235 | **65,7735** | 2.542 | 789,28 tr | 30.510 |
| Cơ sở | AI/MLOps (AI Eng 5–8 năm) | 55,20 | 8,855 | 1,518 | 0,552 | 1,012 | 11,937 | **67,137** | 2.595 | 805,64 tr | 31.142 |
| **Cơ sở – 2 FTE** | | | | | | | | **132,9105** | **5.138** | **1.594,93 tr** | **61.652** |
| Cao | SRE (DevOps >8 năm) | 84,40 | 8,855 | 1,518 | 0,844 | 1,012 | 12,229 | **96,629** | 3.735 | 1.159,55 tr | 44.822 |
| Cao | AI/MLOps (AI Eng >8 năm) | 70,40 | 8,855 | 1,518 | 0,704 | 1,012 | 12,089 | **82,489** | 3.189 | 989,87 tr | 38.263 |
| **Cao – 2 FTE** | | | | | | | | **179,118** | **6.924** | **2.149,42 tr** | **83.085** |

Ví dụ kiểm tra (SRE, kịch bản cơ sở):
- min(53,85; 50,6) = 50,6.
- 22,5% × 50,6 = 11,385; 1% × 53,85 = 0,5385. Công ty đóng = 11,9235.
- Tổng = 53,85 + 11,9235 = 65,7735 tr VND.
- 65.773.500 ÷ 25.870 ≈ 2.542 USD.

Nhận xét (suy ra): khi lương vượt 50,6 tr, phần công ty đóng gần như cố định (~11,9–12,2 tr/tháng), chỉ tương đương **14–22% của gross** thay vì 23,5%.

---

## 5. Nguồn

Tất cả truy cập ngày 2026-10-16. "Cập nhật" là ngày trang/văn bản tự ghi.

| ID | Tiêu đề | URL | Cập nhật |
|---|---|---|---|
| S1 | Metered APIs and services in Microsoft Graph | https://learn.microsoft.com/en-us/graph/metered-api-list | updated_at 2026-04-03 |
| S2 | Overview of metered APIs and services in Microsoft Graph | https://learn.microsoft.com/en-us/graph/metered-api-overview | ms.date 2024-11-07 |
| S3 | Microsoft Graph service-specific throttling limits | https://learn.microsoft.com/en-us/graph/throttling-limits | 2025-01-14 |
| S4 | Outlook service limits (include của S3) | https://github.com/microsoftgraph/microsoft-graph-docs-contrib/blob/main/includes/throttling-outlook.md | — |
| S5 | Microsoft Graph permissions reference | https://learn.microsoft.com/en-us/graph/permissions-reference | ms.date 2026-09-14 |
| S6 | Change notifications overview + subscription lifetime | https://learn.microsoft.com/en-us/graph/change-notifications-overview | 2024-12-27 |
| S7 | Configure how users consent to applications (Entra ID) | https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/configure-user-consent | updated_at 2026-08-04 |
| S8 | Gmail API usage limits | https://developers.google.com/workspace/gmail/api/reference/quota | 2026-09-10 |
| S9 | Drive API usage limits | https://developers.google.com/workspace/drive/api/guides/limits | 2026-09-11 |
| S10 | Calendar API quota | https://developers.google.com/workspace/calendar/api/guides/quota | 2026-09-11 |
| S11 | Docs / Sheets / Slides API limits | https://developers.google.com/workspace/docs/api/limits ; https://developers.google.com/workspace/sheets/api/limits ; https://developers.google.com/workspace/slides/api/limits | 2026-09-03 |
| S12 | Gmail API scopes | https://developers.google.com/workspace/gmail/api/auth/scopes | 2026-09-10 |
| S13 | Drive API scopes | https://developers.google.com/workspace/drive/api/guides/api-specific-auth | 2026-09-03 |
| S14 | When is verification not needed | https://support.google.com/cloud/answer/13464323 | không ghi |
| S14b | Restricted scope verification | https://support.google.com/cloud/answer/13464321 | không ghi |
| S15 | TAC Security – ESOF AppSec ADA CASA FAQs | https://tacsecurity.com/?p=18721 | không ghi |
| S16 | Leviathan Security – Google CASA | https://www.leviathansecurity.com/programs/google-casa-cloud-application-security-assessment | không ghi |
| S17 | Google Workspace standardized model for agent tools and APIs | https://developers.google.com/workspace/tools-safety | 2026-09-03 |
| S18 | Gmail push notifications | https://developers.google.com/workspace/gmail/api/guides/push | 2026-09-15 |
| S19 | Drive – Search for files and folders | https://developers.google.com/workspace/drive/api/guides/search-files | 2026-10-12 |
| S20 | Jira Cloud – Rate limiting | https://developer.atlassian.com/cloud/jira/platform/rate-limiting/ | 2026-10-15 |
| S21 | Confluence Cloud – Rate limiting | https://developer.atlassian.com/cloud/confluence/rate-limiting/ | 2026-10-15 |
| S22 | Drive push notifications | https://developers.google.com/workspace/drive/api/guides/push | — |
| S23 | Calendar push notifications | https://developers.google.com/workspace/calendar/api/guides/push | 2026-09-11 |
| S24 | Calendar API scopes | https://developers.google.com/workspace/calendar/api/auth | 2026-09-03 |
| S25 | Docs API scopes | https://developers.google.com/workspace/docs/api/auth | 2026-09-03 |
| S26 | Microsoft Search API overview (v1.0) | https://learn.microsoft.com/en-us/graph/api/resources/search-api-overview | ms.date 2024-05-13 |
| S27 | Notion – Request limits | https://developers.notion.com/reference/request-limits | không ghi |
| S28 | Prerequisites for deploying connectors – Microsoft 365 Copilot connectors | https://learn.microsoft.com/en-us/microsoft-365/copilot/connectors/prerequisites | updated_at 2026-09-25 |
| S29 | Avoid getting throttled or blocked in SharePoint Online | https://learn.microsoft.com/en-us/sharepoint/dev/general-development/how-to-avoid-getting-throttled-or-blocked-in-sharepoint-online | updated_at 2026-08-10 |
| S30 | Microsoft Teams service limits (include của S3) | https://github.com/microsoftgraph/microsoft-graph-docs-contrib/blob/main/includes/throttling-teams.md | — |
| S31 | Notion – Search by title | https://developers.notion.com/reference/post-search | API 2026-03-11 |
| S32 | Notion – Webhooks | https://developers.notion.com/reference/webhooks | không ghi |
| S33 | Notion – Authorization | https://developers.notion.com/docs/authorization | không ghi |
| S34 | Notion – Capabilities | https://developers.notion.com/reference/capabilities | không ghi |
| S35 | Jira – OAuth 2.0 (3LO) apps | https://developer.atlassian.com/cloud/jira/platform/oauth-2-3lo-apps/ | 2026-10-15 |
| S36 | Jira – Scopes for OAuth 2.0 (3LO) and Forge apps | https://developer.atlassian.com/cloud/jira/platform/scopes-for-oauth-2-3LO-and-forge-apps/ | 2026-10-15 |
| S37 | Jira – Webhooks | https://developer.atlassian.com/cloud/jira/platform/webhooks/ | 2026-10-15 |
| S38 | Confluence – Scopes for OAuth 2.0 (3LO) and Forge apps | https://developer.atlassian.com/cloud/confluence/scopes-for-oauth-2-3LO-and-forge-apps/ | 2026-10-15 |
| S39 | Confluence REST v1 – Search | https://developer.atlassian.com/cloud/confluence/rest/v1/api-group-search/ | — |
| S40 | Confluence – Webhook module | https://developer.atlassian.com/cloud/confluence/modules/webhook/ | 2026-10-15 |
| S41 | ITviec – Vietnam IT Salary & Recruitment Market 2024–2025 (PDF) | https://itviec.com/salary-reports/download/5c4723f6-a99a-4884-be8e-40f42d71fb0b (trang: https://itviec.com/report/vietnam-it-salary-and-recruitment-market-2024-2025) | khảo sát 09–10/2024 |
| S42 | Vietcombank – tỷ giá | https://www.vietcombank.com.vn/api/exchangerates?date=2026-10-16 | 2026-10-16 07:58 +07 |
| S43 | ITviec – Vietnam IT Salary & Recruitment Market 2025–2026 | https://itviec.com/report/vietnam-it-salary-and-recruitment-market | khảo sát 05–11/2025 |
| S44 | Tuổi Trẻ News – Vietnam's 2026 salaries set to surge (Robert Walters) | https://news.tuoitre.vn/vietnams-2026-salaries-set-to-surge-ai-professionals-seen-gaining-up-to-25-survey-103251129202137422.htm | 2025-11-30 |
| S45 | Navigos Search – Talent Guide 2025 | https://www.navigossearch.com/en/articles/talent-guide-2025-salary-and-labor-market-report-is-officially-launched | 2025-02-18 |
| S46 | Luật BHXH số 41/2024/QH15 (Công báo, bản PDF của Chính phủ) | https://datafiles.chinhphu.vn/cpp/files/vbpq/2024/9/41-2024-qh15.pdf | hiệu lực 01/07/2025 |
| S47 | Nghị định 58/2020/NĐ-CP (LuatVietnam) | https://luatvietnam.vn/lao-dong/nghi-dinh-58-2020-nd-cp-muc-dong-bao-hiem-tai-nan-benh-nghe-nghiep-183928-d1.html | hiệu lực 15/07/2020 |
| S48 | Thời báo Tài chính VN – Mức đóng BHYT vẫn bằng 4,5% (NĐ 188/2025) | https://thoibaotaichinhvietnam.vn/muc-dong-bao-hiem-y-te-van-bang-45-luong-co-so-179879.html | 2025-07-11 |
| S49 | Luật Việc làm số 74/2025/QH15 (bản PDF do ntt.edu.vn lưu; bản gốc vbpl.vn không truy cập được) | https://kl.ntt.edu.vn/wp-content/uploads/2025/07/LUAT-VIEC-LAM-2025.pdf | hiệu lực 01/01/2026 |
| S50 | Báo chí về NĐ 374/2025/NĐ-CP (BHTN 1%) | https://nhadautu.vn/tu-2026-nguoi-lao-dong-dong-bao-hiem-that-nghiep-bang-1-luong-thang-d102142.html | — |
| S51 | Toàn văn Luật Công đoàn 2024 (Cổng Nghệ An) | https://hcc.nghean.gov.vn/tin-tong-hop/toan-van-luat-cong-doan-1888.html | hiệu lực 01/07/2025 |
| S52 | Cổng TTĐT Hà Tĩnh – Chính thức tăng lương cơ sở lên 2.530.000 đồng/tháng từ 01/7/2026 | https://hatinh.gov.vn/vi/bai-viet/chinh-thuc-tang-luong-co-so-len-2530000-dongthang-tu-0172026 | 2026-05-17 |
| S53 | Báo Pháp luật VN – Tăng lương tối thiểu vùng từ 1/1/2026 (NĐ 293/2025) | https://baophapluat.vn/chinh-phu-quyet-dinh-tang-luong-toi-thieu-vung-tu-1-1-2026.html | 2025-11-10 |

---

## 6. Gaps

1. **Giá Google khi vượt ngưỡng ngày** (Gmail 80 tr unit, Drive 400 tr unit, Calendar 1 tr request): chưa công bố, "later in 2026" với ít nhất 90 ngày báo trước. Đã kiểm tra S8, S9, S10, S17.
2. **Calendar scope**: trang S24 không phân loại sensitive/restricted. Chưa đối chiếu tham số `q` của `events.list` trên trang reference.
3. **Notion**:
   - Không công bố số của giới hạn chung toàn workspace.
   - Public integration có cần review không: không tìm thấy.
   - Webhook áp dụng cho loại integration nào: không tìm thấy.
   - Không ghi ngày cập nhật trang (S27, S31–S34).
4. **Confluence**: chưa xác định app OAuth 2.0 (3LO) có đăng ký webhook được không (S40). Atlassian org admin có chặn hoặc duyệt app 3LO do user tự cài được không: chưa kiểm tra.
5. **Atlassian Tier 2**: điều kiện và thời gian review để được quota theo tenant chưa rõ. Edition và số user Jira/Confluence của tập đoàn: chưa có.
6. **Microsoft 365 Copilot add-on**: chưa thu thập giá. Chỉ cần nếu chọn federated Copilot connector, không thuộc thiết kế D4.
7. **Lương**:
   - Không lấy được số của Robert Walters (403), Navigos, TopDev, Adecco, Glassdoor, Talentnet.
   - ITviec 2025–2026 công khai không có DevOps/AI. Đang dùng ITviec 2024–2025 (khảo sát 09–10/2024), nên số có thể thấp hơn mặt bằng 2026: Robert Walters dự báo AI/data +15–25% [S44], nhưng không có số gốc để điều chỉnh.
   - ITviec không có nhãn "MLOps" hay "SRE"; đang dùng "AI Engineer/Blockchain Engineer" và "DevOps/DevSecOps Engineer" làm đại diện.
   - ITviec không định nghĩa hai đầu thấp/cao của khoảng trong biểu đồ.
8. **Văn bản pháp luật**:
   - Chưa tải được bản chính thức NĐ 188/2025 (BHYT), NĐ 374/2025 (BHTN), NĐ 158/2025 (sửa NĐ 58/2020): các máy chủ vbpl.vn, vbpl.moj.gov.vn, syt.khanhhoa.gov.vn không phản hồi; thuvienphapluat.vn trả 403.
   - Trần BHYT bằng trần BHXH là **suy ra** từ câu "tiền lương tháng làm căn cứ đóng BHXH bắt buộc".
   - Tỷ lệ TNLĐ-BNN 0,5% sau khi NĐ 158/2025 sửa đổi: chưa đọc văn bản gốc. Bộ Nội vụ đã đề xuất giảm xuống 0,3% đến hết 2027 (chỉ là đề xuất, nguồn báo chí).
9. **Thưởng tháng 13 và các khoản phúc lợi khác** (bảo hiểm sức khỏe tư, phụ cấp): không phải khoản bắt buộc theo luật nên chưa tính. Nếu tập đoàn có, tổng chi phí sẽ cao hơn mục 4.2.
