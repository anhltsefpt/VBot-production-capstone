# VBot – Danh sách tính năng (trích từ đề)

Mỗi tính năng ghi component liên quan, để biết tính năng nào kéo theo chi phí nào.

## A. Tính năng người dùng (5 cấp tác vụ)

| ID | Tính năng | Ví dụ | Component kéo theo |
|---|---|---|---|
| F1.1 | Soạn, trả lời email | "Trả lời email của khách, giọng lịch sự" | llm, connectors (Gmail, Outlook), governance (xác nhận trước khi gửi) |
| F1.2 | Tóm tắt thread email / chat Teams | "Tóm tắt 30 email về dự án X" | llm, connectors |
| F1.3 | Hỏi đáp tài liệu nội bộ (RAG) | "Chính sách nghỉ phép 2026 là gì?" | llm, embedding, vector_db (lọc theo ACL), connectors (Drive, SharePoint, Confluence, Notion) |
| F2.1 | Viết báo cáo, biên bản, tờ trình | "Viết biên bản họp từ ghi chú này" | llm |
| F2.2 | Xuất file DOCX, XLSX, PPTX | "Làm slide 10 trang từ báo cáo" | llm, sandbox (tạo file), object_storage |
| F3.1 | Phân tích bảng tính | "Doanh thu theo quý từ file Excel này" | llm, sandbox (chạy Python), object_storage |
| F3.2 | Viết, sửa lỗi, review code | "Sửa lỗi script này" | llm, sandbox |
| F4.1 | Agent dự án đọc Jira, Confluence, Notion | "Tổng hợp tiến độ sprint" | llm (nhiều bước), connectors, cache_queue (chạy nền) |
| F4.2 | Agent lập kế hoạch, tạo ticket, cập nhật trang | "Tạo 10 ticket từ tài liệu yêu cầu" | llm, connectors (ghi), governance (xác nhận), cache_queue, thông báo khi xong (≤ 10 phút) |
| F5.1 | Mockup giao diện, sơ đồ | "Vẽ sơ đồ luồng đăng nhập" | llm (sinh code HTML/Mermaid), sandbox (render) |
| F5.2 | Ảnh minh họa cho tài liệu, slide | "Ảnh bìa cho báo cáo" | llm (model sinh ảnh, ví dụ Imagen) |

## B. Không gian riêng của từng người

| ID | Tính năng | Component |
|---|---|---|
| W1 | Tải file lên, lưu file agent tạo ra (quota 10 GB/người) | object_storage |
| W2 | Lịch sử chat | database |
| W3 | Bộ nhớ dài hạn (agent nhớ sở thích, bối cảnh) | database, vector_db |
| W4 | Người khác và agent của người khác không đọc được | authz, object_storage (tách theo user), vector_db (lọc theo user) |

## C. Kết nối SaaS (11 connector)

Gmail, Google Drive, Google Calendar, Docs/Sheets/Slides, Outlook, Microsoft 365, OneDrive/SharePoint, Teams, Notion, Jira, Confluence.

| ID | Tính năng | Component |
|---|---|---|
| C1 | User đăng nhập OAuth vào từng SaaS, scope tối thiểu | connectors, authz |
| C2 | Lưu OAuth token có mã hóa | secrets_kms |
| C3 | Đọc dữ liệu: gọi trực tiếp khi cần, hoặc đồng bộ trước vào index | connectors, embedding, vector_db, cache_queue |
| C4 | Ghi dữ liệu (gửi mail, tạo ticket, sửa trang) sau khi user xác nhận | connectors, governance |

## D. Sandbox chạy code

| ID | Tính năng | Component |
|---|---|---|
| S1 | Chạy code agent viết trong container hoặc microVM cô lập (gVisor, Firecracker, Kata) | sandbox, compute |
| S2 | Chỉ mount workspace của đúng user | sandbox, object_storage |
| S3 | Mặc định không có egress, không vào mạng nội bộ, chặn metadata endpoint | network |
| S4 | Giới hạn CPU, RAM, thời gian; hủy sau khi chạy | sandbox |

## E. Nền tảng (người dùng không thấy trực tiếp)

| ID | Tính năng | Component |
|---|---|---|
| P1 | SSO tập đoàn (OIDC/SAML) + MFA | authn |
| P2 | Phân quyền chức năng RBAC/ABAC | authz |
| P3 | LLM gateway: routing model, quota theo người/đơn vị, rate limit, retry, fallback, ghi log token | gateway |
| P4 | Guardrail đầu vào/ra, chống prompt injection từ email và tài liệu | governance |
| P5 | DLP che PII, phân loại dữ liệu, thời hạn lưu | governance |
| P6 | Audit log 12 tháng | monitoring, object_storage |
| P7 | Eval gate trước khi đổi model hoặc prompt | governance, cicd |
| P8 | Monitoring, cảnh báo, chi phí theo user và đơn vị (FinOps) | monitoring |
| P9 | Cảnh báo ngân sách, cắt khi vượt quota | gateway, monitoring |
| P10 | Hàng đợi agent chạy nền, retry, hủy, thông báo khi xong | cache_queue |
| P11 | HA 99,5% giờ hành chính, không có điểm lỗi đơn ở LB, gateway, DB | load_balancer, database, compute |
| P12 | Backup, DR (RTO 4 giờ, RPO 1 giờ), diễn tập khôi phục | backup_dr |
| P13 | Môi trường staging, CI/CD, IaC, registry | cicd |
| P14 | WAF, VPC, NAT, private endpoint tới Vertex AI | network |

## Câu hỏi phạm vi để chốt

- Tính năng nào **bắt buộc chạy ngoài giờ hành chính**? Đề chỉ yêu cầu 99,5% trong giờ hành chính.
- Bộ nhớ dài hạn (W3) làm mức nào: tóm tắt văn bản lưu trong DB, hay vector?
- Connector: đồng bộ trước vào index hay gọi trực tiếp khi cần (C3)?
