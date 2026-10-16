# Sizing tải theo phòng ban (đã chốt)

Đơn vị: **nhiệm vụ/người/ngày** (D11) = khối lượng thật × % giao AI. Lượt/nhiệm vụ chỉ dùng để tính token.
Nguồn và mã W/D: `research/task-volume-by-role.md`. "GT" = giả định của nhóm.

## Quy tắc chung đã chốt

- Soạn, trả lời email: % giao AI = **30%** (thay vì 16% thị trường chung), lý do: VBot triển khai chính thức kèm đào tạo.
- Chỉ tính tác vụ đi qua 11 connector của đề. Kênh ngoài phạm vi (CRM, Zalo, hệ thống chat khách hàng) không tính.

## 1. Kinh doanh và CSKH (500 người) — ĐÃ CHỐT

| # | Tác vụ | Cấp | Khối lượng/ngày | Nguồn | % AI | Nguồn % | Nhiệm vụ/ngày | Lượt/nhiệm vụ |
|---|---|---|---|---|---|---|---|---|
| 1 | Soạn, trả lời email | 1 | 9,9 | W5 | 30% | GT (neo D1: 10–24%) | 2,97 | 2 |
| 2 | Tóm tắt, phân loại email | 1 | 32,2 | W3 | 5% | GT | 1,61 | 1 |
| 3 | Hỏi đáp tài liệu nội bộ | 1 | 4,0 | W9–W11 | 30% | GT | 1,20 | 2 |
| 4 | Biên bản họp → DOCX | 2 | 2,0 | W6 | 20% | GT | 0,40 | 3 |
| 5 | Báo cáo, đề xuất → DOCX/PPTX | 2 | 0,15 | W8 | 50% | GT | 0,08 | 3 |
| 6 | Phân tích pipeline, doanh số trên Excel | 3 | 0,2 | GT | 50% | GT | 0,10 | 4 |
| 7 | Agent chuẩn bị gặp khách: đọc Calendar, Drive, tạo task Jira | 4 | 1,0 | GT | 10% | GT | 0,10 | 2 |
| 8 | Ảnh, visual cho báo giá, slide | 5 | 0,1 | GT | 30% | GT | 0,03 | 3 |
| | **Tổng** | | | | | | **6,49** | |

Đã bỏ: gợi ý trả lời chat khách hàng (kênh không thuộc connector).

## 2. Kế toán (240 người) — ĐÃ CHỐT

| # | Tác vụ | Cấp | Khối lượng/ngày | Nguồn | % AI | Nguồn % | Nhiệm vụ/ngày | Lượt/nhiệm vụ |
|---|---|---|---|---|---|---|---|---|
| 1 | Soạn, trả lời email | 1 | 9,9 | W5 | 30% | GT | 2,97 | 2 |
| 2 | Tóm tắt, phân loại email | 1 | 32,2 | W3 | 5% | GT | 1,61 | 1 |
| 3 | Hỏi đáp tài liệu nội bộ | 1 | 4,0 | W9–W11 | 30% | GT | 1,20 | 2 |
| 4 | Biên bản họp → DOCX | 2 | 2,0 | W6 | 20% | GT | 0,40 | 3 |
| 5 | Báo cáo → DOCX/PPTX | 2 | 0,15 | W8 | 50% | GT | 0,08 | 3 |
| 6 | Phân tích bảng tính FP&A, đối soát | 3 | 2,0 | W18 (tin cậy C) | 40% | GT | 0,80 | 4 |
| 7 | Hóa đơn bất thường AP (⅓ phòng; chỉ tính hóa đơn user tải lên workspace) | 3 | 15,2 | W16 × ⅓ | 2% | GT | 0,30 | 1 |
| 8 | Agent tạo checklist khóa sổ trên Calendar hoặc Notion | 4 | 0,5 | GT | 10% | GT | 0,05 | 2 |
| | **Tổng** | | | | | | **7,41** | |

## 3. Nhân sự, hành chính, pháp chế (260 người) — ĐÃ CHỐT

| # | Tác vụ | Cấp | Khối lượng/ngày | Nguồn | % AI | Nguồn % | Nhiệm vụ/ngày | Lượt/nhiệm vụ |
|---|---|---|---|---|---|---|---|---|
| 1–5 | Tác vụ chung (như phòng 1, 2) | 1–2 | | | | | 6,26 | |
| 6 | Soạn JD, thông báo tuyển dụng, chính sách | 1 | 0,3 | GT | 30% | GT (neo D1) | 0,09 | 2 |
| 7 | Rà soát hợp đồng, văn bản pháp lý → nhận xét/redline DOCX | 2 | 0,5 | GT | 30% | GT | 0,15 | 3 |
| 8 | Tổng hợp chấm công, nhân sự trên Excel (chỉ file user tải lên) | 3 | 0,2 | GT | 40% | GT | 0,08 | 4 |
| 9 | Agent đặt lịch phỏng vấn, onboarding (Calendar) | 4 | 0,5 | GT | 10% | GT | 0,05 | 2 |
| | **Tổng** | | | | | | **6,63** | |

Ghi chú: dữ liệu PII cao (hợp đồng, hồ sơ nhân sự) → mọi tác vụ qua DLP (H5).

## 4. Marketing (200 người) — ĐÃ CHỐT

| # | Tác vụ | Cấp | Khối lượng/ngày | Nguồn | % AI | Nguồn % | Nhiệm vụ/ngày | Lượt/nhiệm vụ |
|---|---|---|---|---|---|---|---|---|
| 1–5 | Tác vụ chung (như phòng 1, 2) | 1–2 | | | | | 6,26 | |
| 6 | Viết nội dung (bài đăng, thông cáo báo chí, landing copy) | 1 | 2,0 | GT | 40% | GT (neo D1: 24%) | 0,80 | 2 |
| 7 | Ảnh, mockup, banner (mặc định 1 ảnh/lượt; "sinh thêm" = 1 lượt) | 5 | 1,0 | GT | 25% | GT | 0,25 | 3 |
| 8 | Phân tích số liệu campaign trên Excel | 3 | 0,3 | GT | 40% | GT | 0,12 | 4 |
| 9 | Agent cập nhật kế hoạch trên Notion/Confluence | 4 | 0,5 | GT | 15% | GT | 0,08 | 2 |
| | **Tổng** | | | | | | **7,51** | |

## 5. Quản lý dự án, vận hành (300 người) — ĐÃ CHỐT

| # | Tác vụ | Cấp | Khối lượng/ngày | Nguồn | % AI | Nguồn % | Nhiệm vụ/ngày | Lượt/nhiệm vụ |
|---|---|---|---|---|---|---|---|---|
| 1–5 | Tác vụ chung (như phòng 1, 2) | 1–2 | | | | | 6,26 | |
| 6 | Agent tạo/cập nhật ticket Jira, trang Confluence | 4 | 3,0 | GT | 30% | GT | 0,90 | 2 |
| 7 | Agent báo cáo tiến độ tuần (đọc Jira/Confluence → DOCX/PPTX) | 4 | 0,2 | GT (1/tuần) | 50% | GT | 0,10 | 3 |
| 8 | Sơ đồ quy trình, Gantt (sinh bằng code Mermaid/HTML, render trong sandbox) | 5 | 0,2 | GT | 40% | GT | 0,08 | 3 |
| 9 | Phân tích dữ liệu vận hành trên Excel | 3 | 0,3 | GT | 40% | GT | 0,12 | 4 |
| | **Tổng** | | | | | | **7,46** | |

## 6. Mua hàng, chuỗi cung ứng (200 người) — ĐÃ CHỐT

| # | Tác vụ | Cấp | Khối lượng/ngày | Nguồn | % AI | Nguồn % | Nhiệm vụ/ngày | Lượt/nhiệm vụ |
|---|---|---|---|---|---|---|---|---|
| 1–5 | Tác vụ chung (như phòng 1, 2) | 1–2 | | | | | 6,26 | |
| 6 | So sánh báo giá, đánh giá NCC (file đính kèm email → sandbox) | 3 | 2,8 | W17 | 20% | GT | 0,56 | 4 |
| 7 | Agent đọc email NCC, cập nhật lịch giao hàng trên Calendar, tạo nhắc việc | 4 | 0,5 | GT | 10% | GT | 0,05 | 2 |
| | **Tổng** | | | | | | **6,87** | |

Đã bỏ: soạn RFQ/email NCC (trùng dòng 1 — email gửi đã gồm email NCC).

## 7. IT (200 người) — ĐÃ CHỐT

Giả định trong phòng: ⅔ dev/QA, ⅓ hạ tầng/support (GT). Không có connector kho code → code do user dán hoặc tải lên.

| # | Tác vụ | Cấp | Khối lượng/ngày | Nguồn | % AI | Nguồn % | Nhiệm vụ/ngày | Lượt/nhiệm vụ |
|---|---|---|---|---|---|---|---|---|
| 1–5 | Tác vụ chung (như phòng 1, 2) | 1–2 | | | | | 6,26 | |
| 6 | Viết, sửa code trong sandbox | 3 | 0,27 | W14 × ⅔ | 59% | D7, D8, D11 | 0,16 | 8 |
| 7 | Review code (user dán hoặc tải lên) | 3 | 0,40 | W15 × ⅔ | 20% | GT | 0,08 | 2 |
| 8 | Tra cứu, phân loại ticket hỗ trợ IT (Jira) | 1 | 1,5 | W13 × ⅓ | 40% | GT | 0,60 | 2 |
| 9 | Agent tạo/cập nhật ticket Jira, runbook Confluence | 4 | 1,0 | GT | 20% | GT | 0,20 | 2 |
| 10 | Diagram kiến trúc, flow (sinh bằng code) | 5 | 0,1 | GT | 50% | GT | 0,05 | 3 |
| | **Tổng** | | | | | | **7,35** | |

## 8. Lãnh đạo và trợ lý (100 người) — ĐÃ CHỐT

Họp 4,6 cuộc/ngày (W7, giả định 1 giờ/cuộc) → dòng biên bản họp thay đổi; tác vụ chung = 6,78.

| # | Tác vụ | Cấp | Khối lượng/ngày | Nguồn | % AI | Nguồn % | Nhiệm vụ/ngày | Lượt/nhiệm vụ |
|---|---|---|---|---|---|---|---|---|
| 1–3, 5 | Tác vụ chung (trừ dòng 4) | 1–2 | | | | | 5,86 | |
| 4* | Biên bản họp → DOCX | 2 | 4,6 | W7 | 20% | GT | 0,92 | 3 |
| 6 | Agent chuẩn bị briefing: đọc Calendar, email, tài liệu liên quan | 4 | 4,6 | W7 | 20% | GT | 0,92 | 1 |
| 7 | Agent sắp lịch trên Calendar (trợ lý) | 4 | 1,0 | GT | 20% | GT | 0,20 | 2 |
| 8 | Slide trình bày → PPTX | 2 | 0,2 | GT | 50% | GT | 0,10 | 3 |
| | **Tổng** | | | | | | **8,00** | |


## Tổng hợp toàn công ty

Số trong các bảng phòng ban là **mỗi người mỗi ngày**. Cả phòng = × số người. Script tính: `sizing.py`.

| Phòng | Người | Nhiệm vụ/người/ngày | Nhiệm vụ/phòng/ngày |
|---|---|---|---|
| Kinh doanh, CSKH | 500 | 6,49 | 3.242 |
| Kế toán | 240 | 7,41 | 1.777 |
| Nhân sự, HC, pháp chế | 260 | 6,63 | 1.723 |
| Marketing | 200 | 7,50 | 1.500 |
| Quản lý dự án, vận hành | 300 | 7,46 | 2.237 |
| Mua hàng, chuỗi cung ứng | 200 | 6,87 | 1.373 |
| IT | 200 | 7,35 | 1.469 |
| Lãnh đạo, trợ lý | 100 | 8,00 | 800 |
| **Toàn công ty** | **2.000** | **7,06** | **14.120** |

- **Nhiệm vụ/tháng:** 14.120 × 22 = **310.644**
- **Lượt chat/ngày:** 27.098 (13,55 lượt/người)

| Cấp | Nhiệm vụ/ngày | % nhiệm vụ | Lượt/ngày | % lượt |
|---|---|---|---|---|
| 1 Email, hỏi đáp | 11.863 | 84,0% | 20.507 | 75,7% |
| 2 Tài liệu | 1.051 | 7,4% | 3.153 | 11,6% |
| 3 Dữ liệu, code | 555 | 3,9% | 2.099 | 7,7% |
| 4 Agent | 552 | 3,9% | 1.042 | 3,8% |
| 5 Thiết kế | 99 | 0,7% | 297 | 1,1% |

Giờ cao điểm (chưa chốt tỉ lệ; research đề xuất 12 / 15 / 20% traffic ngày):

| % traffic ngày ở giờ cao điểm | Nhiệm vụ/giờ | Nhiệm vụ/giây | Lượt/giây |
|---|---|---|---|
| 12% | 1.694 | 0,47 | 0,90 |
| 15% | 2.118 | 0,59 | 1,13 |
| 20% | 2.824 | 0,78 | 1,51 |
