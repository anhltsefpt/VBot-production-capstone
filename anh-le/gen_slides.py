"""Generate G03_slide.pptx from cost_model.py (GCP, DR B). Run with the venv python."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

import cost_model as m

import openpyxl
_ws = openpyxl.load_workbook("G03_baogia.xlsx")["BaoGia"]
c, TOTAL = {}, None
for comp, _, _, cost, _ in _ws.iter_rows(min_row=2, values_only=True):
    if comp == "TOTAL":
        TOTAL = cost
    else:
        c[comp] = c.get(comp, 0) + cost
assert abs(TOTAL - sum(c.values())) < 0.01  # slide figures come straight from the quote file

NAVY, BLUE, TEAL, GREY, LIGHT, WHITE, RED = (RGBColor(0x1F, 0x3A, 0x5F), RGBColor(0x2E, 0x6F, 0xB7), RGBColor(0x1A, 0x8F, 0x7A),
                                             RGBColor(0x55, 0x5F, 0x6B), RGBColor(0xEE, 0xF3, 0xF8), RGBColor(0xFF, 0xFF, 0xFF), RGBColor(0xB8, 0x3B, 0x3B))
prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]


def usd(x):
    return f"{x:,.0f}".replace(",", ".")


def usd2(x):
    return f"{x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def text(slide, x, y, w, h, lines, size=14, color=GREY, bold_first=False, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, ln in enumerate(lines if isinstance(lines, list) else [lines]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        bold = False
        if isinstance(ln, tuple):
            ln, bold = ln
        p.text = ln
        p.alignment = align
        p.space_after = Pt(4)
        for r in p.runs:
            r.font.size = Pt(size)
            r.font.color.rgb = color
            r.font.bold = bold or (bold_first and i == 0)
    return tb


def header(title, sub=None, num=None):
    s = prs.slides.add_slide(BLANK)
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(0.95))
    bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()
    text(s, 0.5, 0.15, 11.5, 0.7, title, size=26, color=WHITE, bold_first=True)
    if sub:
        text(s, 0.5, 1.0, 12.3, 0.5, sub, size=13, color=BLUE)
    if num:
        text(s, 12.3, 7.0, 0.9, 0.4, str(num), size=11, color=GREY, align=PP_ALIGN.RIGHT)
    text(s, 0.5, 7.0, 8, 0.4, "G03 · VBot Workplace · GCP asia-southeast1", size=10, color=GREY)
    return s


def table(slide, x, y, w, rows, col_w=None, size=11, head_fill=BLUE, row_h=0.32):
    nr, nc = len(rows), len(rows[0])
    shp = slide.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(row_h * nr))
    t = shp.table
    if col_w:
        for j, cw in enumerate(col_w):
            t.columns[j].width = Inches(cw)
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            cell = t.cell(i, j)
            cell.text = str(v)
            cell.margin_left = cell.margin_right = Inches(0.05)
            cell.margin_top = cell.margin_bottom = Inches(0.02)
            for p in cell.text_frame.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(size)
                    run.font.bold = i == 0
                    run.font.color.rgb = WHITE if i == 0 else GREY
            cell.fill.solid()
            cell.fill.fore_color.rgb = head_fill if i == 0 else (LIGHT if i % 2 else WHITE)
    return t


def box(slide, x, y, w, h, title, code, fill=LIGHT, line=BLUE, size=11):
    b = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    b.fill.solid(); b.fill.fore_color.rgb = fill
    b.line.color.rgb = line; b.line.width = Pt(1.25)
    tf = b.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Inches(0.05)
    p = tf.paragraphs[0]; p.text = title; p.alignment = PP_ALIGN.CENTER
    for r in p.runs:
        r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = NAVY
    p2 = tf.add_paragraph(); p2.text = code; p2.alignment = PP_ALIGN.CENTER
    for r in p2.runs:
        r.font.size = Pt(size - 2); r.font.color.rgb = TEAL; r.font.bold = True
    return b


def arrow(slide, x1, y1, x2, y2):
    ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    ln.line.color.rgb = GREY; ln.line.width = Pt(1.5)
    ln.line._get_or_add_ln().append(ln.line._get_or_add_ln().makeelement(
        "{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd", {"type": "triangle"}))


# ================================================================ 0 title
s = prs.slides.add_slide(BLANK)
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid(); bg.fill.fore_color.rgb = NAVY; bg.line.fill.background()
text(s, 0.8, 2.0, 11.5, 1.2, "VBot Workplace", size=48, color=WHITE, bold_first=True)
text(s, 0.8, 3.1, 11.5, 0.8, "Trợ lý AI văn phòng trên Google Cloud cho 2.000 người dùng mỗi ngày", size=24, color=WHITE)
text(s, 0.8, 4.3, 11.5, 1.2, ["Tổng chi phí: 6.821,44 USD/tháng, tức 3,41 USD cho mỗi người dùng hoạt động (DAU)",
                              "Track 2 · Production Capstone · Nhóm G03"], size=18, color=RGBColor(0xBF, 0xD7, 0xEA))

# ================================================================ 1 load
s = header("1. Giả định và ước lượng tải", "Đề cho sẵn 2.000 DAU. Nhóm ước lượng mọi khối lượng còn lại từ dưới lên, theo 8 phòng ban, có nguồn", 1)
table(s, 0.5, 1.5, 6.2, [
    ["Phòng ban", "Số người", "Nhiệm vụ/người/ngày"],
    ["Kinh doanh, CSKH", "500", "6,49"], ["Kế toán", "240", "7,41"], ["Nhân sự, hành chính, pháp chế", "260", "6,63"],
    ["Marketing", "200", "7,50"], ["Quản lý dự án, vận hành", "300", "7,46"], ["Mua hàng, SCM", "200", "6,87"],
    ["IT", "200", "7,35"], ["Lãnh đạo, trợ lý", "100", "8,00"], ["Toàn công ty", "2.000", "7,06"]],
    col_w=[3.0, 1.0, 2.2], size=11)
text(s, 0.5, 5.0, 6.3, 1.9, [
    ("Công thức: số nhiệm vụ = khối lượng việc thực tế × tỉ lệ giao cho AI", True),
    "Khối lượng việc: Microsoft RCT 2025 (32 email đọc và 2 cuộc họp mỗi ngày), Radicati, APQC, NBER, Graphite",
    "Tỉ lệ giao cho AI: Liang 2025 (10–24% văn bản có dùng LLM); email nâng lên 30% vì công ty triển khai chính thức",
    "Chỉ tính tác vụ đi qua 11 connector của đề"], size=11)
table(s, 7.0, 1.5, 5.8, [
    ["Chỉ số", "Giá trị"],
    ["Nhiệm vụ/ngày · /tháng (22 ngày)", "14.120 · 310.644"],
    ["Lượt chat mỗi ngày", "27.098 (13,55 lượt/người)"],
    ["Tỉ lệ cấp 1/2/3/4/5", "84,0 / 7,4 / 3,9 / 3,9 / 0,7%"],
    ["Cao điểm (15% lưu lượng ngày)", "0,59 nhiệm vụ/s · 1,13 lượt/s"],
    ["Token mỗi tháng", "12,19 tỉ vào (61% từ cache) + 0,79 tỉ ra"],
    ["Sandbox", "140.800 lượt, tối đa 2 phút/lượt"],
    ["Ảnh sinh ra", "4.312 ảnh/tháng"],
    ["Workspace", "2.000 × 2 GB = 4 TB; quota 10 GB/người"],
    ["Thời hạn lưu audit · lịch sử chat", "12 tháng · 12 tháng"]], col_w=[2.6, 3.2], size=11)
text(s, 7.0, 5.0, 5.8, 1.9, [
    ("Token mỗi lượt: số lần gọi model × token vào / token ra", True),
    "C1: 2 × 5,5k / 250 · C2: 2 × 18k / 2,5k · C3: 3,5 × 12k / 1k",
    "C4: 8 × 15k / 300 · C5: 1,5 × 4k / 600 + 1 ảnh (C1–C5 = cấp 1–5)",
    "Nguồn: Azure On your data (5 × 1.024 token), DA-Code, MCP-Universe, MCPMark"], size=11)

# ================================================================ 2 architecture
s = header("2. Kiến trúc tổng thể", "Một cloud chính: GCP asia-southeast1 (Singapore), GKE Autopilot regional trên 2 zone. Mỗi hộp ghi mã component trong báo giá", 2)
box(s, 0.3, 1.7, 1.6, 0.9, "Nhân viên", "trình duyệt", fill=WHITE)
box(s, 2.2, 1.6, 2.0, 1.1, "Cloud Armor WAF + HTTPS LB", "network · load_balancer")
box(s, 4.5, 1.6, 2.0, 1.1, "IAP + IdP tập đoàn (SSO, MFA)", "authn")
arrow(s, 1.9, 2.15, 2.2, 2.15); arrow(s, 4.2, 2.15, 4.5, 2.15)
g = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.4), Inches(6.2), Inches(3.1))
g.fill.background(); g.line.color.rgb = TEAL; g.line.dash_style = 4
text(s, 6.9, 1.42, 6, 0.3, "GKE Autopilot regional, 2 zone · compute (prod; staging là namespace riêng)", size=10, color=TEAL)
box(s, 7.0, 1.8, 1.8, 1.0, "Web/API, SSE", "compute")
box(s, 9.0, 1.8, 1.9, 1.0, "LiteLLM gateway (quota USD)", "gateway · authz")
box(s, 11.1, 1.8, 1.8, 1.0, "Worker connector, agent", "connectors")
box(s, 9.0, 3.1, 1.9, 1.1, "Sandbox gVisor, chặn egress", "sandbox")
box(s, 11.1, 3.1, 1.8, 1.1, "Cloud NAT → 11 SaaS (OAuth của user)", "network")
box(s, 7.0, 3.1, 1.8, 1.1, "Model Armor (guardrail, DLP)", "governance")
arrow(s, 6.5, 2.15, 7.0, 2.3)
box(s, 0.3, 3.4, 2.1, 1.1, "Vertex AI qua PSC: Haiku 5.5, embedding, ảnh", "llm · embedding")
box(s, 2.6, 3.4, 2.0, 1.1, "Cloud SQL PG HA + pgvector + RLS", "database · vector_db")
box(s, 4.8, 3.4, 1.8, 1.1, "Valkey HA + Cloud Tasks", "cache_queue")
box(s, 0.3, 4.9, 2.1, 1.0, "GCS workspace dual-region", "object_storage")
box(s, 2.6, 4.9, 2.0, 1.0, "Cloud KMS + Secret Manager", "secrets_kms")
box(s, 4.8, 4.9, 1.8, 1.0, "Logging, Prometheus, Trace", "monitoring")
box(s, 6.8, 4.9, 2.0, 1.0, "Backup + DR Jakarta", "backup_dr")
box(s, 9.0, 4.9, 1.9, 1.0, "Cloud Build + Artifact Registry", "cicd")
box(s, 11.1, 4.9, 1.8, 1.0, "2 FTE SRE + MLOps", "ops_labor")
text(s, 0.3, 6.1, 12.7, 0.8, ["Không có điểm lỗi đơn: LB managed chạy đa zone; mỗi pod có 2 replica ở 2 zone; Cloud SQL có standby ở zone khác; Valkey có primary và replica. "
                              "Dữ liệu lưu tại Singapore. Suy luận đi qua endpoint global của Vertex AI, có cam kết không lưu dữ liệu (zero-retention) và không dùng dữ liệu để huấn luyện."], size=11)

# ================================================================ 3 request flow
s = header("3. Luồng một request: \"Tóm tắt thread email dự án X, rồi tạo 3 ticket Jira\"", None, 3)
steps = [
    "1. Trình duyệt gửi request qua Cloud Armor (WAF) và HTTPS LB. IAP kiểm tra phiên SSO với IdP tập đoàn (có MFA).",
    "2. Web/API lấy user_id và group từ token, rồi ghi audit. Model Armor quét tin nhắn mới để tìm prompt injection và PII.",
    "3. Router xếp request vào cấp 4, đẩy job vào Cloud Tasks và trả ngay \"đang chạy nền\" (thời gian đến token đầu tiên, TTFT, < 3 s).",
    "4. Worker giải mã OAuth token của chính user (KMS envelope), rồi tìm email qua Gmail/Graph API bằng quyền của user đó.",
    "5. Worker đánh dấu nội dung email là \"không tin cậy\", cho Model Armor quét, và tách nội dung này khỏi chỉ dẫn hệ thống.",
    "6. LiteLLM kiểm tra quota USD của user và phòng ban, rồi gọi Claude Haiku 5.5 trên Vertex AI qua PSC. Agent chạy 8 bước.",
    "7. Agent đề xuất 3 ticket. User xem người nhận và nội dung trên một màn hình duyệt chung, rồi bấm xác nhận.",
    "8. Worker tạo ticket bằng OAuth của user, ghi audit, và báo \"xong\" qua web và email (tối đa 10 phút).",
    "Nếu cần chạy code (cấp 3): worker tạo pod sandbox gVisor, chỉ mount thư mục workspace của user, chặn egress, giới hạn 2–10 phút, và hủy pod ngay sau khi chạy.",
]
text(s, 0.6, 1.3, 12.2, 5.5, steps, size=14)

# ================================================================ 4 model routing
s = header("4. Model và routing", "Dùng API model managed trên Vertex AI, không tự host GPU. Mặc định dùng một model rẻ; eval gate quyết định khi nào nâng cấp", 4)
table(s, 0.5, 1.5, 12.3, [
    ["Cấp", "Model", "Chế độ", "Lượt/ngày", "USD/tháng", "Nâng lên khi eval < 95%"],
    ["1 Email, hỏi đáp", "Claude Haiku 5.5", "không reasoning (H6)", "20.507", "386", "Sonnet 5.5"],
    ["2 Tài liệu", "Claude Haiku 5.5", "không reasoning (H6)", "3.153", "288", "Sonnet 5.5"],
    ["3 Dữ liệu, code", "Claude Haiku 5.5", "reasoning thấp", "2.099", "161", "Sonnet 5.5 (+2.939)"],
    ["4 Agent dự án", "Claude Haiku 5.5", "reasoning thấp, chạy nền", "1.042", "105", "Sonnet 5.5 (+1.766)"],
    ["5 Thiết kế", "Haiku 5.5 + Gemini 3.1 Flash-Lite Image", "1 ảnh/lượt", "297", "7 + 147 ảnh", "—"],
    ["Embedding", "gemini-embedding-001", "KB chung + workspace", "—", "20", "—"]],
    col_w=[1.8, 2.9, 2.2, 1.3, 1.6, 2.5], size=12)
text(s, 0.5, 4.2, 6.0, 2.7, [
    ("Model tham chiếu theo H8: Claude Opus 5.5", True),
    "Golden set: 100 nhiệm vụ thật cho mỗi cấp, đã che PII",
    "Chấm điểm: Opus làm giám khảo (LLM-as-judge), người chấm lại 10%; cấp 3 kiểm tra thêm code có chạy đúng không",
    "Đạt khi điểm của Haiku ≥ 95% điểm của Opus. Chạy lại mỗi lần đổi model hoặc prompt (4 lần/tháng: 525 USD)"], size=12)
text(s, 6.8, 4.2, 6.0, 2.7, [
    ("Lý do chọn Haiku 5.5", True),
    "Giá 0,10 / 0,50 USD mỗi 1M token vào / ra, đọc cache 0,01; giá như nhau trên GCP, AWS và Azure",
    "AA Intelligence Index 43 (chế độ max), cao nhất trong nhóm cùng mức giá (GPT-6 Luna: 38)",
    "Tốc độ 182–238 token/giây. Cả 5 cấp chỉ tốn 947 USD/tháng (dùng Opus cho mọi cấp: 36.380)",
    "Rủi ro: chưa có số đo TTFT khi tắt reasoning → đo trong giai đoạn pilot"], size=12)

# ================================================================ 5 tech choices
s = header("5. Lý do chọn công nghệ: so sánh có số liệu", "Giá niêm yết tại Singapore, đọc ngày 16/10/2026 (USD/tháng)", 5)
table(s, 0.5, 1.5, 12.3, [
    ["Quyết định", "Chọn", "Phương án so sánh", "Lý do"],
    ["Cloud chính", "GCP: 6.821", "AWS 8.643 · Azure 14.484", "Rẻ nhất; chênh lệch chủ yếu ở guardrail (Model Armor: 0,10 USD/1M token)"],
    ["LLM gateway", "LiteLLM tự chạy: 0 license", "Apigee ~1.595 · Azure APIM Std v2 ~700", "Phương án duy nhất có quota theo USD cho từng user và phòng ban (H8)"],
    ["Model", "Haiku 5.5 cả 5 cấp: 947", "Sonnet cấp 3–4: 5.652 · Opus: 36.380", "Routing theo cấp + eval gate; chỉ nâng cấp khi eval không đạt"],
    ["Vector DB", "pgvector trong Cloud SQL: 0", "Vertex Vector Search ~84 · OpenSearch ~413", "Index nhỏ (KB chung + workspace); lọc ACL bằng SQL"],
    ["Token vault", "KMS envelope trong Postgres: ~4", "Secret Manager 12.000 secret ~720", "Vẫn mã hóa và có audit, nhưng rẻ hơn 180 lần"],
    ["Sandbox", "GKE Sandbox gVisor: 315", "Agent Engine 483 · AgentCore 509", "Có sẵn trên Autopilot; NetworkPolicy chặn egress"],
    ["Guardrail", "Chỉ quét text mới: 281", "Quét toàn bộ token: 1.298", "Mỗi đoạn text chỉ quét một lần, khi vào hệ thống"],
    ["Connector", "Hybrid: gọi API bằng OAuth của user", "Crawl toàn bộ vào index", "SaaS tự áp quyền gốc; không cần service account quyền rộng"]],
    col_w=[1.7, 2.9, 3.4, 4.3], size=11, row_h=0.5)

# ================================================================ 6 connectors & authz
s = header("6. Connector và phân quyền (H2)", "11 connector: Gmail, Drive, Calendar, Docs/Sheets/Slides, Outlook, M365, OneDrive/SharePoint, Teams, Notion, Jira, Confluence", 6)
text(s, 0.5, 1.6, 6.1, 5.2, [
    ("Định danh", True),
    "SSO qua OIDC/SAML với IdP sẵn có của tập đoàn; IdP bật MFA; IAP + Workforce Identity Federation",
    "RBAC theo group trong token (ví dụ: chỉ nhóm IT dùng sandbox hạng mở rộng)",
    ("OAuth ủy quyền với scope tối thiểu", True),
    "Mỗi user tự cấp quyền cho từng SaaS. Quyền đọc: gmail.readonly, Files.Read, read:jira-work…",
    "Chỉ xin quyền ghi khi cần (gmail.send, write:jira-work); không dùng service account quyền rộng",
    "Google OAuth app ở chế độ Internal, nên không cần đánh giá CASA",
    ("Token vault", True),
    "Data key mã hóa refresh token; Cloud KMS mã hóa data key (envelope encryption)",
    "Chỉ service account của worker được giải mã, và chỉ cho user của request đang chạy. Mỗi lần giải mã đều ghi audit"], size=12)
text(s, 6.9, 1.6, 6.0, 5.2, [
    ("ACL tài liệu theo quyền gốc", True),
    "Dữ liệu cá nhân (mail, lịch, Jira): worker gọi search API của SaaS bằng token của user, nên SaaS tự áp quyền",
    "KB chung đã index: mỗi chunk có allowed_groups; mọi truy vấn pgvector đều lọc theo group của user (WHERE)",
    "Workspace: cột owner_id + Row-Level Security (RLS) của Postgres",
    ("Rate limit đã kiểm tra", True),
    "Jira/Confluence 65.000 điểm/giờ/app · Notion 180 req/phút · Teams 1 req/s/user",
    "Worker dùng hàng đợi và backoff; ưu tiên webhook thay cho polling",
    ("Chi phí", True),
    "API của 11 SaaS không tính phí theo lượt gọi; tập đoàn đã có license SaaS"], size=12)

# ================================================================ 7 workspace & sandbox
s = header("7. Workspace riêng và sandbox (H3)", "\"Agent của A có đọc được file của B không?\" Không. Có 4 lớp chặn:", 7)
table(s, 0.5, 1.5, 6.2, [
    ["Lớp", "Cơ chế"],
    ["Lưu trữ", "Bucket GCS chia prefix theo user_id; IAM chỉ cấp quyền cho service account của app; app áp quota 10 GB/user"],
    ["Database", "RLS theo owner_id cho chat, bộ nhớ dài hạn và metadata của file"],
    ["Tìm kiếm", "Mọi truy vấn pgvector bắt buộc lọc theo owner_id hoặc allowed_groups"],
    ["Connector", "Dùng token OAuth của chính user, nên không thấy dữ liệu của người khác"]],
    col_w=[1.3, 4.9], size=11, row_h=0.55)
text(s, 7.0, 1.5, 5.9, 5.3, [
    ("Sandbox chạy code của agent", True),
    "GKE Sandbox (gVisor, kernel chạy ở userspace): mỗi lượt một pod, hủy pod sau khi chạy",
    "Hạng mặc định: 1 vCPU, 2 GB, 2 phút. Hạng mở rộng: 2 vCPU, 4 GB, 10 phút. Đĩa tạm 5 GB",
    "Chỉ mount thư mục workspace của đúng user; đọc/ghi qua sidecar dùng token ngắn hạn",
    "NetworkPolicy chặn mọi egress: không ra internet, không vào mạng nội bộ",
    "Chặn metadata server (Workload Identity với service account không có quyền); node không có quyền IAM",
    "Image dựng sẵn (pandas, openpyxl, python-docx/pptx, matplotlib, Node); không cài thư viện lúc chạy",
    ("Nếu code cố thoát ra node?", True),
    "Mọi syscall đi qua gVisor. Pod không chạy privileged, không mount hostPath, và bị kill khi hết thời gian"], size=12)

# ================================================================ 8 governance
s = header("8. AI governance và data governance (H4, H5)", "\"Một email chứa lệnh ẩn: gửi toàn bộ hợp đồng ra ngoài.\" Hệ thống xử lý thế nào?", 8)
text(s, 0.5, 1.5, 6.1, 5.3, [
    ("Chống prompt injection", True),
    "Model Armor quét tin nhắn mới, nội dung từ connector và output cuối (281 USD/tháng)",
    "Nội dung từ connector nằm trong khối \"dữ liệu không tin cậy\"; model không coi đó là chỉ dẫn",
    "Chỉ yêu cầu của user mới kích hoạt được hành động ghi; nội dung từ connector thì không",
    ("Xác nhận trước hành động ghi", True),
    "Rủi ro cao (gửi ra ngoài tập đoàn, xóa, chia sẻ quyền): user xác nhận từng hành động",
    "Rủi ro thấp (ticket, trang, email nháp): user duyệt cả nhóm một lần; màn hình hiện người nhận, nội dung và tệp đính kèm",
    "Sandbox chặn egress, nên code không gửi được dữ liệu ra ngoài",
    ("Eval gate", True),
    "Mỗi lần đổi model hoặc prompt, chạy golden set trên staging. Điểm < 95% thì không deploy"], size=12)
text(s, 6.9, 1.5, 6.0, 5.3, [
    ("Data governance", True),
    "Mã hóa khi lưu (Google-managed key; riêng token dùng KMS) và khi truyền (TLS, PSC)",
    "Sensitive Data Protection (đi kèm Model Armor) che PII",
    "Phân loại dữ liệu theo nhãn nguồn (HR, pháp chế: nhạy cảm cao)",
    "Thời hạn lưu: audit 12 tháng (truy vấn được 30 ngày, sau đó archive); chat 12 tháng; file tạm 30 ngày; prompt log 30 ngày, đã che PII",
    "Vertex AI không dùng dữ liệu để huấn luyện; tắt durable cache để không lưu dữ liệu (zero-retention)",
    ("Audit log", True),
    "Ghi ai, lúc nào, tool và connector nào, hành động ghi nào đã được xác nhận. Chỉ nhóm bảo mật được đọc"], size=12)

# ================================================================ 9 HA DR
s = header("9. HA, backup và DR (H7)", "Mục tiêu: 99,5% trong giờ hành chính · RTO 4 giờ · RPO 1 giờ", 9)
table(s, 0.5, 1.5, 7.0, [
    ["Thành phần", "HA", "Backup / DR"],
    ["LB, Cloud Armor", "Managed, đa zone", "—"],
    ["GKE Autopilot", "Regional; mỗi pod 2 replica ở 2 zone", "Dựng lại bằng Terraform"],
    ["LiteLLM, web, worker", "2 replica, 2 zone", "Image lưu trong Artifact Registry"],
    ["Cloud SQL", "Standby ở zone khác, failover tự động", "Backup hằng ngày + PITR; bản sao ở Jakarta"],
    ["Valkey", "Primary + replica", "Không cần (chỉ chứa dữ liệu tạm)"],
    ["GCS workspace", "Regional, đa zone", "Dual-region"],
    ["Vertex AI", "Endpoint global", "Model dự phòng qua LiteLLM"]],
    col_w=[1.9, 2.5, 2.6], size=11, row_h=0.42)
text(s, 7.8, 1.5, 5.1, 5.3, [
    ("Khi mất 1 zone lúc 10:00", True),
    "LB ngừng gửi traffic vào zone hỏng. Pod ở zone còn lại nhận tải; Autopilot tạo thêm pod",
    "Cloud SQL failover sang standby, thường trong vài chục giây đến 1–2 phút. Chỉ mất các giao dịch đang chạy",
    "Một số request bị lỗi; user gửi lại được. Dữ liệu đã commit không mất",
    ("Khi mất cả region Singapore", True),
    "Dựng lại ở Jakarta bằng Terraform, backup DB đã sao chép và bucket dual-region. Mất ≤ 4 giờ và ≤ 1 giờ dữ liệu",
    ("Diễn tập", True),
    "Khôi phục DB từ backup mỗi quý. Diễn tập dựng region DR mỗi 6 tháng",
    ("Chi phí", True),
    "backup_dr: 164 USD/tháng (gồm 153 USD cho DR sang Jakarta)"], size=12)

# ================================================================ 10 monitoring finops
s = header("10. Monitoring và FinOps (H8)", "Đo gì, cảnh báo khi nào, và chi phí theo từng user và phòng ban", 10)
text(s, 0.5, 1.5, 6.1, 5.3, [
    ("Chỉ số đo", True),
    "SLO: tỉ lệ thành công, p95 TTFT theo cấp, thời gian chạy agent nền, lỗi connector theo từng SaaS",
    "LiteLLM: token vào/ra/cache; USD theo user, phòng ban, model và cấp",
    "Hạ tầng: CPU/RAM của pod, Cloud SQL, hàng đợi Cloud Tasks, số lượt sandbox",
    "An toàn: số lần Model Armor chặn, số hành động ghi bị user từ chối",
    ("Cảnh báo", True),
    "p95 TTFT > 3 s trong 10 phút · agent chạy > 10 phút · tỉ lệ lỗi > 2% · Cloud SQL failover",
    "Cache hit < 50% (chi phí sẽ tăng) · chi tiêu trong ngày vượt dự báo 20%"], size=12)
table(s, 6.9, 1.5, 6.0, [
    ["Ngưỡng quota (USD/tháng)", "Hành động"],
    ["80%", "Cảnh báo user; báo trưởng phòng nếu là quota phòng"],
    ["100%", "Hạ cấp: cấp 1–2 chỉ dùng model rẻ nhất; khóa cấp 4–5"],
    ["120%", "Chặn đến đầu tháng sau, trừ khi trưởng phòng duyệt"],
    ["90% ngân sách hệ thống", "Cảnh báo nhóm FinOps và ban IT"]],
    col_w=[2.2, 3.8], size=11, row_h=0.5)
text(s, 6.9, 4.3, 6.0, 2.5, [
    ("Chi phí theo đầu người", True),
    "LLM + guardrail + sandbox ≈ " + usd(c['llm'] + c['governance'] + c['sandbox']) + " USD/tháng, tức " + f"{(c['llm'] + c['governance'] + c['sandbox'])/2000:.2f}".replace(".", ",") + " USD/user/tháng",
    "Quota mặc định đề xuất: 3 USD/user/tháng (khoảng 2 lần mức trung bình)",
    "Báo cáo hằng tháng theo phòng ban, lấy từ log chi tiêu của LiteLLM"], size=12)

# ================================================================ 11 cost
s = header("11. Chi phí", "Tổng trên slide bằng dòng TOTAL của G03_baogia.xlsx", 11)
text(s, 0.5, 1.5, 4.0, 1.6, ["6.821,44 USD/tháng", "3,41 USD/DAU/tháng"], size=26, color=NAVY, bold_first=True)
top = sorted(c.items(), key=lambda kv: -kv[1])[:5]
table(s, 0.5, 3.1, 5.0, [["5 hạng mục lớn nhất", "USD/tháng", "%"]] +
      [[k, usd(v), f"{v/TOTAL*100:.0f}%"] for k, v in top], col_w=[2.4, 1.4, 1.2], size=12, row_h=0.42)
table(s, 6.0, 1.5, 6.9, [
    ["Đòn bẩy tiết kiệm (so với phương án thay thế)", "Tiết kiệm (USD/tháng)"],
    ["Haiku cho cả 5 cấp, thay Sonnet ở cấp 3–4 (eval gate giữ chất lượng)", "4.705"],
    ["LiteLLM thay Apigee", "~1.595"],
    ["Guardrail chỉ quét text mới, thay vì quét toàn bộ token", "1.018"],
    ["Token vault bằng KMS envelope, thay Secret Manager", "~716"],
    ["Prompt caching (61% token vào đọc từ cache)", "670"],
    ["Ngoài giờ chỉ chạy 1 pod, thay vì 2 pod 24/7", "109"],
    ["pgvector trong DB, thay Vertex Vector Search", "~84"],
    ["Staging là namespace, thay vì cluster riêng", "73"]],
    col_w=[5.1, 1.8], size=11, row_h=0.42)
text(s, 6.0, 5.5, 6.9, 1.4, ["Không dùng free tier, credit hay giá khuyến mãi (ví dụ: không tính đợt giảm giá tạm thời của Gemini 3.8 Flash).",
                             "Chưa tính phí ghi cache của Claude (ước tính vài %). Không mua gói support. Không có dòng dự phòng."], size=11)

# ================================================================ 12 risk
s = header("12. Rủi ro và mở rộng", None, 12)
table(s, 0.5, 1.4, 6.3, [
    ["Kịch bản", "USD/tháng", "USD/DAU"],
    ["Cơ sở (2.000 DAU)", "6.821", "3,41"],
    ["DAU ×2 = 4.000", "8.826", "2,21"],
    ["Giá token +30%", "7.263", "3,63"],
    ["Giá token −50%", "6.085", "3,04"],
    ["Cấp 3–4 phải nâng lên Sonnet 5.5", "11.526", "5,76"],
    ["Workspace đầy 20 TB", "+ ~704", "—"]],
    col_w=[3.3, 1.5, 1.5], size=12, row_h=0.42)
text(s, 0.5, 4.6, 6.3, 2.3, [
    ("Khi DAU tăng gấp đôi", True),
    "Tăng tuyến tính: LLM, guardrail, sandbox, storage, log",
    "Gần như cố định: 2 FTE, cluster, Cloud SQL, Valkey, LB. Vì vậy USD/DAU giảm",
    "Chỉ xét tự host GPU khi chi phí token vượt chi phí chạy ≥ 2 GPU HA 24/7 cộng chi phí vận hành"], size=11)
text(s, 7.1, 1.4, 5.8, 5.4, [
    ("Rủi ro lớn nhất", True),
    "Haiku không đạt 95% ở cấp 3–4: thêm 4.705 USD/tháng. Đã tính sẵn; LiteLLM đổi model bằng 1 dòng cấu hình",
    "Token agent thực tế có thể cao hơn giả định (khoảng 4,6–42,8 tỉ token/tháng). Đo trong pilot 2–4 tuần",
    "Chưa có số đo chính thức về TTFT của Haiku khi tắt reasoning",
    "Phụ thuộc endpoint global của Vertex AI và quy định về dữ liệu (Nghị định 13/2023). Phương án hybrid: dữ liệu nhạy cảm dùng model chạy tại Singapore",
    "Rate limit Jira/Confluence tính chung cho cả app (65.000 điểm/giờ)",
    "Google dự kiến tính phí API Workspace khi vượt ngưỡng, từ cuối 2026 (chưa công bố giá)",
    "LiteLLM là open source, không có SLA. Cách giảm rủi ro: 2 FTE trực, pin phiên bản, test trên staging"], size=11)

# ================================================================ appendix A
s = header("Phụ lục A. Báo giá theo component (USD/tháng)", "Chi tiết từng dòng (đơn giá × số lượng, kèm bằng chứng) nằm trong G03_baogia.xlsx", "A")
order = ["compute", "llm", "embedding", "gateway", "load_balancer", "authn", "authz", "database", "vector_db", "object_storage",
         "cache_queue", "sandbox", "connectors", "secrets_kms", "backup_dr", "monitoring", "governance", "network", "cicd", "ops_labor"]
half = (len(order) + 1) // 2
for k, part in enumerate((order[:half], order[half:])):
    rows = [["Component", "USD/tháng"]] + [[x, usd2(c[x])] for x in part]
    if k == 1:
        rows.append(["TOTAL", usd2(TOTAL)])
    table(s, 0.5 + k * 6.4, 1.5, 6.0, rows, col_w=[3.5, 2.5], size=12, row_h=0.42)

# ================================================================ appendix B
s = header("Phụ lục B. Nguồn số liệu", None, "B")
text(s, 0.5, 1.3, 12.3, 5.6, [
    "Giá: trang giá chính thức của Google Cloud (GKE, Vertex AI, Cloud SQL, Cloud Storage, Memorystore, Cloud Tasks, KMS, Secret Manager, Observability, Security Command Center, Cloud Armor, VPC network, Cloud Build, Artifact Registry, IAP), đọc ngày 16/10/2026",
    "So sánh với AWS và Azure: AWS Price List API, Azure Retail Prices API (region ap-southeast-1, southeastasia)",
    "Tải: Microsoft WorkLab 2025; Dillon et al., Shifting Work Patterns with Generative AI (2025); Radicati 2015; APQC; Brynjolfsson et al. NBER 31161; Graphite Research; Liang et al. 2025; UK DBT Copilot evaluation 2025",
    "Token: Azure OpenAI On your data defaults; Vertex RAG Engine; DA-Code; DABstep; MCP-Universe; MCPMark; OpenRouter State of AI 2025; Azure LLM inference trace 2024",
    "Chất lượng và tốc độ model: Artificial Analysis Intelligence Index v4.3.2",
    "Lương: ITviec Vietnam IT Salary & Recruitment Market 2024–2025; tỉ giá Vietcombank ngày 16/10/2026",
    "Connector: Microsoft Graph throttling, Atlassian rate limiting, Notion request limits, Google Workspace API limits",
    "Chi tiết nghiên cứu: thư mục research/ (usage-benchmarks, task-volume-by-role, token-per-task, r1, r2, r3, r5-r9, r8-r6) và cost_model.py"], size=13)

prs.save("G03_slide.pptx")
print("slides", len(prs.slides), "TOTAL", TOTAL)
