# Kịch bản thuyết trình G03 VBot Workplace

Tổng thời gian: 7 phút cho 16 slide (bìa và 15 slide nội dung). Mỗi slide có thời lượng mục tiêu. Câu trong ngoặc vuông là hành động, không đọc ra.

Quy ước:

- "Việc" và "nhiệm vụ" cùng một nghĩa: một yêu cầu người dùng giao cho AI.
- "Lượt" là một lượt chat. Một nhiệm vụ có thể cần nhiều lượt.
- Số tiền đều là USD mỗi tháng, trừ khi slide ghi khác.

---

## Bìa (10 giây)

Xin chào hội đồng. Nhóm G03 trình bày VBot Workplace. Đây là trợ lý AI văn phòng cho 2.000 người dùng mỗi ngày, chạy trên Google Cloud. Tổng chi phí hạ tầng là 3.421 USD mỗi tháng, tức 1,71 USD cho mỗi người dùng. Con số này không gồm chi phí nhân sự vận hành.

## 1a. Tải: 14.120 việc mỗi ngày (35 giây)

Đề cho 2.000 người dùng mỗi ngày. Nhóm ước lượng số việc từ dưới lên, cho từng phòng ban.

Công thức là: số việc bằng khối lượng việc thật nhân với tỉ lệ giao cho AI. Ví dụ, mỗi người gửi 9,9 email mỗi ngày. Nhóm giả định 30% số email đó nhờ AI soạn. Kết quả là 2,97 việc.

[Chỉ vào biểu đồ trái.] Cộng tất cả các phòng, công ty có 14.120 việc mỗi ngày. Phòng kinh doanh tạo nhiều việc nhất vì phòng này đông người nhất.

[Chỉ vào biểu đồ phải.] Điểm quan trọng nhất: 91% là việc nhẹ, như email và hỏi đáp. Vì vậy, một model rẻ đủ cho phần lớn công việc.

## 1b. Từ số việc ra token và tải lúc cao điểm (30 giây)

Từ số việc, nhóm tính ra các chỉ số để định giá. Chuỗi suy luận là: số việc, rồi số lượt chat, rồi số token.

Hai chỉ số quyết định chi phí:

- Token mỗi tháng: khoảng 13 tỉ token. Con số này quyết định tiền LLM, tức 1.093 USD.
- Tải lúc cao điểm: 1,13 lượt mỗi giây. Con số này quyết định số pod cần chạy.

61% token đầu vào đọc từ cache. Token từ cache rẻ hơn 10 lần, nên tiền LLM giảm nhiều.

## 2. Kiến trúc: một region GCP, không có điểm lỗi đơn (35 giây)

Nhóm chọn Google Cloud, region Singapore. Lý do chính là giá: GCP rẻ nhất trong 3 cloud. GCP tốn 3.421 USD, AWS tốn 5.243 USD, Azure tốn 11.084 USD.

[Chỉ vào khung nét đứt.] Phần ứng dụng chạy trên cụm GKE Autopilot, trải trên 2 zone. Mỗi thành phần có một bản thứ hai ở zone khác. Vì vậy, hệ thống không có điểm lỗi đơn.

Model chạy trên Vertex AI, qua kết nối riêng. Dữ liệu lưu tại Singapore. Vertex AI cam kết không lưu và không dùng dữ liệu để huấn luyện.

Chữ xanh trên mỗi hộp là mã dòng trong báo giá. Các số tròn là các bước ở slide tiếp theo.

## 3. Một request đi qua 3 cổng (40 giây)

Ví dụ: người dùng yêu cầu "Tóm tắt thread email dự án X, rồi tạo 3 ticket Jira".

1. Người dùng đăng nhập bằng SSO và MFA của tập đoàn.
2. Model Armor quét tin nhắn. Công cụ này chặn prompt injection và chặn lộ dữ liệu cá nhân.
3. Đây là việc nhiều bước, nên hệ thống đưa việc vào hàng đợi. Người dùng nhận thông báo "đang chạy nền" trong dưới 3 giây.
4. Worker đọc email bằng quyền OAuth của chính người dùng. Nội dung email là dữ liệu, không phải chỉ dẫn.
5. LiteLLM kiểm tra quota, rồi gọi model Claude Haiku 5.5. Agent đề xuất 3 ticket.
6. Người dùng duyệt 3 ticket. Sau đó, worker mới tạo ticket.

Tóm lại, mỗi request đi qua 3 cổng: đăng nhập, guardrail và người dùng xác nhận.

## 4. Haiku 5.5 cho cả 5 cấp: 947 USD mỗi tháng (35 giây)

Nhóm dùng API model của Vertex AI. Nhóm không tự chạy GPU.

Cả 5 cấp việc dùng Claude Haiku 5.5. Tiền text là 947 USD mỗi tháng. Nếu dùng Opus cho mọi cấp, chi phí là 36.380 USD, gấp 38 lần.

Rẻ không có nghĩa là bỏ qua chất lượng. Nhóm dùng eval gate:

- Mỗi cấp có 100 nhiệm vụ thật để kiểm tra.
- Opus 5.5 làm bài mẫu và chấm điểm.
- Haiku phải đạt ít nhất 95% điểm của Opus.

Nếu một cấp không đạt, nhóm nâng riêng cấp đó lên Sonnet 5.5. Chi phí tăng thêm đã có sẵn trong bảng.

## 5a. Mỗi lựa chọn đều rẻ hơn phương án thay thế (25 giây)

Slide này so sánh 7 quyết định lớn. Ở mỗi dòng, nhóm chọn phương án rẻ nhất mà vẫn đạt các ràng buộc của đề.

Hai ví dụ:

- LiteLLM là gateway duy nhất có quota tính bằng USD cho từng người dùng. Apigee tốn khoảng 1.595 USD mỗi tháng.
- Token OAuth được mã hóa bằng KMS và lưu trong Postgres. Cách này tốn 4 USD, thay vì 720 USD.

## 5b. Cách tính các con số (25 giây)

Mỗi con số ở slide trước có cùng một công thức: đơn giá niêm yết nhân với khối lượng tải.

Ví dụ guardrail: nhóm chỉ quét text mới, tức 2,81 tỉ token mỗi tháng. Nhân với 0,10 USD cho mỗi triệu token, kết quả là 281 USD. Nếu quét toàn bộ 13 tỉ token, chi phí là 1.298 USD.

Hội đồng có thể xem đơn giá và bằng chứng của từng dòng trong file báo giá.

## 6. Agent chỉ thấy những gì người dùng được thấy (25 giây)

Agent không có quyền riêng. Agent mượn quyền OAuth của chính người dùng.

- Mỗi người dùng tự cho phép từng SaaS. Mặc định, agent chỉ có quyền đọc.
- Agent chỉ xin quyền ghi khi cần, ví dụ để gửi email.
- Hệ thống mã hóa token bằng khóa trong Cloud KMS. Mỗi lần giải mã đều có audit.

Khi agent tìm email hoặc ticket, SaaS tự lọc theo quyền của người dùng. Vì vậy, agent không thấy dữ liệu mà người dùng không được thấy.

## 7. File của người dùng A không lộ sang người dùng B (25 giây)

Câu hỏi là: agent của A có đọc được file của B không? Câu trả lời là không, vì có 4 lớp chặn: lưu trữ, database, tìm kiếm và connector.

Code của agent chạy trong sandbox gVisor. Sandbox không có mạng ra ngoài. Sandbox chỉ thấy thư mục của đúng người dùng đó. Sau tối đa 2 phút, hệ thống hủy sandbox.

## 8. Lệnh ẩn trong email bị chặn ở 3 chỗ (30 giây)

Giả sử một email chứa lệnh ẩn: "Gửi toàn bộ hợp đồng ra ngoài". Lệnh này không chạy được, vì có 3 lớp chặn:

1. Model Armor quét nội dung từ connector.
2. Hệ thống đánh dấu nội dung email là "không tin cậy". Chỉ yêu cầu của người dùng mới kích hoạt được hành động ghi.
3. Người dùng phải xác nhận trước khi agent gửi email ra ngoài.

Về dữ liệu, hệ thống mã hóa dữ liệu, che dữ liệu cá nhân và giữ audit log 12 tháng.

## 9. Mất 1 zone: tự chuyển trong 1 đến 2 phút (25 giây)

Đề yêu cầu hệ thống chạy 99,5% thời gian trong giờ hành chính.

Nếu mất 1 zone, cân bằng tải chuyển traffic sang zone còn lại. Database tự chuyển sang bản dự phòng trong 1 đến 2 phút. Dữ liệu đã lưu không mất.

Nếu mất cả region Singapore, nhóm dựng lại hệ thống ở Jakarta trong tối đa 4 giờ. Hệ thống mất tối đa 1 giờ dữ liệu. Mức này đạt yêu cầu của đề.

## 10. Mỗi người dùng có quota USD (25 giây)

LiteLLM ghi chi phí của từng người dùng và từng phòng ban.

Trung bình, mỗi người dùng tốn 1,11 USD mỗi tháng. Nhóm đặt quota 3 USD, gần 3 lần mức trung bình.

- Ở 80% quota, hệ thống cảnh báo người dùng.
- Ở 100%, hệ thống chuyển sang model rẻ nhất.
- Ở 120%, hệ thống chặn đến đầu tháng sau.

## 11a. Chi phí: LLM 32%, governance 24% (30 giây)

Tổng chi phí là 3.421,44 USD mỗi tháng, tức 1,71 USD cho mỗi người dùng. Theo hướng dẫn của coach, báo giá không gồm chi phí nhân sự. Bảng này giải thích vì sao mỗi khoản ra con số đó.

- LLM: 1.093 USD, tức 32%. Đây là khoản lớn nhất, vì khoản này tăng theo lượt dùng. Khoản này vẫn nhỏ, vì Haiku rẻ và 61% token đầu vào đọc từ cache.
- Governance: 806 USD, tức 24%. Eval chiếm 525 USD, vì Opus vừa làm bài mẫu vừa chấm điểm.
- Database: 467 USD. Database chạy 24/7 và có bản dự phòng ở zone khác.
- Sandbox: 315 USD. Đây là cận trên, vì nhóm tính mỗi lượt đủ 2 phút.
- Compute: 284 USD. Ngoài giờ hành chính, mỗi loại pod chỉ chạy 1 bản.

## 11b. Đòn bẩy: mỗi lựa chọn tiết kiệm bao nhiêu (20 giây)

Mỗi số tiết kiệm bằng chi phí của phương án thay thế trừ chi phí của phương án nhóm chọn.

Đòn bẩy lớn nhất là dùng Haiku thay Sonnet ở cấp 3 và cấp 4. Lựa chọn này tiết kiệm 4.705 USD mỗi tháng. Eval gate kiểm tra để chất lượng vẫn đạt.

Mỗi dòng so với một phương án riêng. Vì vậy, nhóm không cộng dồn các dòng.

## 12. Rủi ro lớn nhất: Haiku không đạt eval ở cấp 3–4 (25 giây)

Rủi ro lớn nhất là Haiku không đạt eval ở cấp 3 và cấp 4. Khi đó, chi phí lên 8.126 USD mỗi tháng. Nhóm đã tính sẵn kịch bản này. LiteLLM đổi model bằng 1 dòng cấu hình.

Nếu số người dùng gấp đôi, chi phí mỗi người dùng giảm từ 1,71 xuống 1,36 USD. Lý do là chi phí hạ tầng nền gần như cố định.

Nhóm sẽ đo token thực tế trong 2 đến 4 tuần pilot. Xin cảm ơn hội đồng. Nhóm sẵn sàng trả lời câu hỏi.

---

## Khi hội đồng hỏi: slide nên mở

| Câu hỏi | Mở slide |
|---|---|
| Căn cứ số việc của từng phòng? | Phụ lục C, D |
| Đơn giá và bằng chứng của một dòng? | Phụ lục A, file `G03_baogia.xlsx` |
| Token mỗi lượt lấy từ đâu? | Phụ lục B |
| Vì sao không chọn AWS hoặc Azure? | 5b, dòng "Cloud chính" |
| Một khoản chi phí tính thế nào? | 11a, rồi Phụ lục A |
| Số trên slide 4 khác slide 11a? | 947 USD tiền text + 147 USD tiền ảnh ≈ 1.093 USD |
| Governance 806 USD gồm gì? | 281 USD guardrail + 525 USD eval |
