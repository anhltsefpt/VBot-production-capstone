"""Generate G03_slide.pptx from cost_model.py (GCP, DR B). Run with the venv python."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.oxml.ns import qn
import contextlib
from decimal import Decimal, ROUND_HALF_UP
import io

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
    text(s, 0.5, 7.0, 10, 0.4, "G03 · Lê Tuấn Anh (2A202602952) · Hồ Thái Hòa (2A202602915) · Nguyễn Đình Lâm Phúc (2A202602986)", size=10, color=GREY)
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
text(s, 0.8, 1.4, 11.5, 1.2, "VBot Workplace", size=48, color=WHITE, bold_first=True)
text(s, 0.8, 2.5, 11.5, 0.8, "Trợ lý AI văn phòng trên Google Cloud cho 2.000 người dùng mỗi ngày", size=24, color=WHITE)
text(s, 0.8, 3.6, 11.5, 1.2, ["Tổng chi phí: 6.821,44 USD/tháng, tức 3,41 USD cho mỗi người dùng hoạt động (DAU)",
                              "Track 2 · Production Capstone · Nhóm G03"], size=18, color=RGBColor(0xBF, 0xD7, 0xEA))
text(s, 0.8, 4.8, 11.5, 1.8, [("Thành viên", True), "Lê Tuấn Anh · MSSV 2A202602952", "Hồ Thái Hòa · MSSV 2A202602915",
                              "Nguyễn Đình Lâm Phúc · MSSV 2A202602986"], size=16, color=WHITE)

# ================================================================ 1 load
with contextlib.redirect_stdout(io.StringIO()):
    import sizing  # per-department task model (research/task-volume-by-role.md)
dept = [(k, n * sum(r[1] for r in rows), n, sum(r[1] for r in rows)) for k, (n, rows) in sizing.D.items()]
dept.sort(key=lambda d: -d[1])
tier_names = {1: "Email, hỏi đáp", 2: "Viết tài liệu", 3: "Dữ liệu, code", 4: "Agent dự án", 5: "Thiết kế, sinh ảnh"}
tiers = [(t, sizing.tot[t]) for t in range(1, 6)]
T = sizing.T
CAT = ["2a78d6", "eb6834", "1baf7a", "eda100", "e87ba4", "008300", "4a3aa7", "e34948"]  # dataviz categorical order, validated
ORD = ["104281", "1c5cab", "2a78d6", "5598e7", "86b6ef"]  # one-hue ordinal ramp: cấp 1 darkest


def pct(x):
    return f"{x * 100:.1f}".replace(".", ",") + "%"


def donut(slide, x, y, d, labels, values, colors, center):
    cd = CategoryChartData()
    cd.categories = labels
    cd.add_series("s", values)
    ch = slide.shapes.add_chart(XL_CHART_TYPE.DOUGHNUT, Inches(x), Inches(y), Inches(d), Inches(d), cd).chart
    ch.has_legend = False; ch.has_title = False
    plot = ch.plots[0]
    plot._element.find(qn("c:holeSize")).set("val", "58")
    for pt, col in zip(plot.series[0].points, colors):
        pt.format.fill.solid(); pt.format.fill.fore_color.rgb = RGBColor.from_string(col)
        pt.format.line.color.rgb = WHITE; pt.format.line.width = Pt(1.5)
    text(slide, x + d * 0.2, y + d / 2 - 0.42, d * 0.6, 0.8, center, size=13, color=NAVY, bold_first=True, align=PP_ALIGN.CENTER)


def legend(slide, x, y, rows, colors, name_w=2.15, val_w=1.05, row_h=0.31):
    for i, ((name, val), col) in enumerate(zip(rows, colors)):
        sw = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y + i * row_h + 0.08), Inches(0.16), Inches(0.16))
        sw.fill.solid(); sw.fill.fore_color.rgb = RGBColor.from_string(col); sw.line.fill.background()
        text(slide, x + 0.2, y + i * row_h, name_w, row_h, name, size=11)
        text(slide, x + 0.2 + name_w, y + i * row_h, val_w, row_h, val, size=11, align=PP_ALIGN.RIGHT)


def r2(x):
    return Decimal(str(x)).quantize(Decimal("0.01"), ROUND_HALF_UP)


def vn(x):
    return f"{r2(x)}".replace(".", ",")


def share(k):
    return f"{c[k] / TOTAL * 100:.0f}%"


def badge(slide, x, y, n):
    b = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(0.32), Inches(0.32))
    b.fill.solid(); b.fill.fore_color.rgb = TEAL; b.line.fill.background()
    tf = b.text_frame; tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.text = str(n); p.alignment = PP_ALIGN.CENTER
    for r in p.runs:
        r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = WHITE


light = (tiers[0][1] + tiers[1][1]) / T
heavy = (tiers[2][1] + tiers[3][1]) / T

# ================================================================ 1a load
s = header(f"1. Tải: {usd(T)} việc/ngày, {light * 100:.0f}% là việc nhẹ",
           "Đề cho 2.000 người dùng mỗi ngày (DAU). Nhóm ước lượng từng việc của 8 phòng ban: số việc = khối lượng thật × tỉ lệ giao cho AI", "1a")
text(s, 0.5, 1.5, 6.0, 0.4, "Ai tạo ra việc? Nhiệm vụ mỗi ngày theo phòng ban", size=14, color=NAVY, bold_first=True)
donut(s, 0.35, 2.0, 2.7, [d[0] for d in dept], [d[1] for d in dept], CAT, [usd(T), "nhiệm vụ/ngày"])
legend(s, 3.15, 2.0, [(f"{k} ({n})", f"{usd(v)} · {v / T * 100:.0f}%") for k, v, n, _ in dept], CAT, name_w=2.3, val_w=1.2)
top, lead = dept[0], max(dept, key=lambda d: d[3])
text(s, 0.5, 4.65, 6.0, 1.0, [
    f"{top[0]} tạo nhiều việc nhất ({top[1] / T * 100:.0f}%) vì đông người nhất. "
    f"{lead[0]} dùng nhiều nhất tính theo đầu người: {vn(lead[3])} nhiệm vụ/ngày (trung bình công ty: {vn(T / 2000)})."], size=12)
text(s, 7.0, 1.5, 6.0, 0.4, "Việc gì? Nhiệm vụ chia theo 5 cấp", size=14, color=NAVY, bold_first=True)
donut(s, 6.9, 1.95, 2.9, [f"Cấp {t}" for t, _ in tiers], [v for _, v in tiers], ORD, [pct(tiers[0][1] / T), "là cấp 1"])
legend(s, 9.85, 2.0, [(f"Cấp {t}: {tier_names[t]}", pct(v / T)) for t, v in tiers], ORD, name_w=2.1, val_w=0.85)
text(s, 7.0, 4.65, 6.0, 1.0, [f"{light * 100:.0f}% là việc nhẹ (cấp 1–2: email, hỏi đáp, tài liệu). Vì vậy một model rẻ đủ cho đa số (slide 4). "
                              f"Việc nặng (cấp 3–4: chạy code, agent nhiều bước) chỉ chiếm {pct(heavy)}."], size=12)
text(s, 0.5, 5.8, 12.3, 1.1, [
    ("Ví dụ: mỗi người gửi 9,9 email/ngày; nhóm giả định 30% số email nhờ AI soạn → 9,9 × 30% = 2,97 nhiệm vụ. "
     f"Cộng mọi việc của mọi phòng ra {usd(T)} nhiệm vụ/ngày.", True),
    "Chi tiết từng việc, từng phòng ban và nguồn số liệu: Phụ lục C và D."], size=12)

# ================================================================ 1b derived metrics
s = header("1. Từ số việc ra token và tải lúc cao điểm",
           "Hai con số quyết định chi phí: token mỗi tháng (tiền LLM) và lượt mỗi giây lúc cao điểm (số pod cần chạy)", "1b")
table(s, 0.5, 1.5, 12.3, [
    ["Chỉ số", "Giá trị", "Ảnh hưởng tới chi phí nào"],
    ["Nhiệm vụ mỗi tháng", f"310.644 ({usd(T)} × 22 ngày làm việc)", "Mọi khoản tính theo lượt dùng"],
    ["Lượt chat mỗi ngày", "27.098 (mỗi nhiệm vụ khoảng 2 lượt)", "Số lần gọi model"],
    ["Lượt/giây lúc cao điểm", "1,13 (giờ bận nhất = 15% lưu lượng cả ngày)", f"compute: số pod ({usd(c['compute'])} USD/tháng)"],
    ["Token mỗi tháng", "12,19 tỉ vào + 0,79 tỉ ra; 61% token vào đọc từ cache", f"llm: {usd(c['llm'])} USD/tháng; token đọc từ cache rẻ hơn 10 lần"],
    ["Lượt chạy code (sandbox)", "140.800 lượt/tháng, tối đa 2 phút/lượt", f"sandbox: {usd(c['sandbox'])} USD/tháng"],
    ["Ảnh sinh ra", "4.312 ảnh/tháng (chỉ cấp 5)", "Nằm trong llm: 147 USD/tháng"],
    ["Dung lượng workspace", "4 TB dùng thật (2.000 người × 2 GB)", f"object_storage: {usd(c['object_storage'])} USD/tháng"]],
    col_w=[3.0, 4.6, 4.7], size=13, row_h=0.5)
text(s, 0.5, 5.75, 12.3, 1.1, [
    ("Cách đọc: số việc → số lượt chat → số token. Token nhân với giá model ra tiền LLM.", True),
    "Số token mỗi lượt theo từng cấp lấy từ benchmark công khai (Azure On your data, DA-Code, MCP-Universe, MCPMark); chi tiết ở Phụ lục B."], size=12)

# ================================================================ 2 architecture
s = header("2. Kiến trúc: một region GCP, không có điểm lỗi đơn",
           f"GCP Singapore vì rẻ nhất trong 3 cloud (6.821 USD/tháng; AWS 8.643, Azure 14.484). Số tròn là bước ở slide 3; chữ xanh là mã dòng trong báo giá", 2)
box(s, 0.3, 1.7, 1.6, 0.9, "Nhân viên", "trình duyệt", fill=WHITE)
box(s, 2.2, 1.6, 2.0, 1.1, "Tường lửa web + cân bằng tải", "network · load_balancer")
box(s, 4.5, 1.6, 2.0, 1.1, "IAP + SSO tập đoàn (MFA)", "authn")
arrow(s, 1.9, 2.15, 2.2, 2.15); arrow(s, 4.2, 2.15, 4.5, 2.15)
g = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.4), Inches(6.2), Inches(3.1))
g.fill.background(); g.line.color.rgb = TEAL; g.line.dash_style = 4
text(s, 6.9, 1.42, 6, 0.3, "Cụm GKE Autopilot chạy trên 2 zone (prod; staging dùng chung cụm)", size=10, color=TEAL)
box(s, 7.0, 1.8, 1.8, 1.0, "Web/API (stream câu trả lời)", "compute")
box(s, 9.0, 1.8, 1.9, 1.0, "LiteLLM gateway (quota USD)", "gateway · authz")
box(s, 11.1, 1.8, 1.8, 1.0, "Worker: connector, agent", "connectors")
box(s, 9.0, 3.1, 1.9, 1.1, "Sandbox chạy code, không có mạng ra ngoài", "sandbox")
box(s, 11.1, 3.1, 1.8, 1.1, "Cloud NAT → 11 SaaS (OAuth của user)", "network")
box(s, 7.0, 3.1, 1.8, 1.1, "Model Armor (guardrail, che PII)", "governance")
arrow(s, 6.5, 2.15, 7.0, 2.3)
box(s, 0.3, 3.4, 2.1, 1.1, "Vertex AI qua kết nối riêng: Haiku 5.5, embedding, ảnh", "llm · embedding")
box(s, 2.6, 3.4, 2.0, 1.1, "Postgres HA + tìm kiếm vector", "database · vector_db")
box(s, 4.8, 3.4, 1.8, 1.1, "Cache + hàng đợi việc nền", "cache_queue")
box(s, 0.3, 4.9, 2.1, 1.0, "Lưu file workspace (2 region)", "object_storage")
box(s, 2.6, 4.9, 2.0, 1.0, "Khóa mã hóa, secret", "secrets_kms")
box(s, 4.8, 4.9, 1.8, 1.0, "Log, metric, trace", "monitoring")
box(s, 6.8, 4.9, 2.0, 1.0, "Backup + DR sang Jakarta", "backup_dr")
box(s, 9.0, 4.9, 1.9, 1.0, "Build, deploy", "cicd")
box(s, 11.1, 4.9, 1.8, 1.0, "2 kỹ sư vận hành", "ops_labor")
for n, (bx, by) in enumerate([(2.2, 1.6), (7.0, 3.1), (4.8, 3.4), (11.1, 1.8), (9.0, 1.8), (11.1, 3.1)], 1):
    badge(s, bx - 0.14, by - 0.14, n)
text(s, 0.3, 6.1, 12.7, 0.8, ["Mỗi thành phần có bản thứ hai ở zone khác (slide 9). Dữ liệu lưu tại Singapore; Vertex AI cam kết không lưu và không dùng dữ liệu để huấn luyện.",
                              "H1–H8 là 8 ràng buộc cứng của đề: H1 cloud · H2 phân quyền · H3 cô lập user · H4 AI governance · H5 data governance · H6 độ trễ · H7 HA, DR · H8 chất lượng, chi phí"], size=11)

# ================================================================ 3 request flow
s = header("3. Một request đi qua 3 cổng: SSO, guardrail, xác nhận",
           "Ví dụ: \"Tóm tắt thread email dự án X, rồi tạo 3 ticket Jira\". Số bước khớp với số tròn trên sơ đồ slide 2", 3)
steps = [
    ("1. Đăng nhập", True),
    "Request đi qua tường lửa web. IAP kiểm tra đăng nhập SSO và MFA của tập đoàn.",
    ("2. Kiểm tra đầu vào (cổng guardrail)", True),
    "Model Armor quét tin nhắn để chặn prompt injection và lộ dữ liệu cá nhân. Mọi bước đều ghi audit.",
    ("3. Chạy nền", True),
    "Việc nhiều bước (cấp 4) vào hàng đợi. User nhận \"đang chạy nền\" ngay, dưới 3 giây (H6).",
    ("4. Đọc email bằng quyền của chính user", True),
    "Worker dùng OAuth token của user để tìm email. Nội dung email được đánh dấu \"không tin cậy\", không phải chỉ dẫn.",
    ("5. Gọi model", True),
    "LiteLLM kiểm tra quota USD của user, rồi gọi Claude Haiku 5.5 trên Vertex AI. Agent đề xuất 3 ticket.",
    ("6. User xác nhận rồi mới ghi (cổng xác nhận)", True),
    "User duyệt 3 ticket trên một màn hình. Worker tạo ticket, ghi audit, báo \"xong\" (tối đa 10 phút, H6).",
]
text(s, 0.6, 1.6, 12.2, 5.3, steps, size=16)

# ================================================================ 4 model routing
s = header("4. Haiku 5.5 cho cả 5 cấp: 947 USD/tháng",
           "Dùng API model trên Vertex AI, không tự host GPU. Chỉ nâng một cấp lên Sonnet 5.5 khi eval của cấp đó dưới 95%", 4)
table(s, 0.5, 1.5, 12.3, [
    ["Cấp", "Model", "Chế độ", "Lượt/ngày", "USD/tháng", "Nếu eval < 95%: nâng lên"],
    ["1 Email, hỏi đáp", "Claude Haiku 5.5", "tắt reasoning (cần nhanh)", "20.507", "386", "Sonnet 5.5"],
    ["2 Tài liệu", "Claude Haiku 5.5", "tắt reasoning (cần nhanh)", "3.153", "288", "Sonnet 5.5"],
    ["3 Dữ liệu, code", "Claude Haiku 5.5", "reasoning thấp", "2.099", "161", "Sonnet 5.5: +2.939 USD"],
    ["4 Agent dự án", "Claude Haiku 5.5", "reasoning thấp, chạy nền", "1.042", "105", "Sonnet 5.5: +1.766 USD"],
    ["5 Thiết kế", "Haiku 5.5 + Gemini 3.1 Flash-Lite Image", "1 ảnh/lượt", "297", "7 + 147 ảnh", "—"],
    ["Embedding", "gemini-embedding-001", "tìm kiếm tài liệu", "—", "20", "—"]],
    col_w=[1.8, 2.9, 2.3, 1.2, 1.5, 2.6], size=12)
text(s, 0.5, 4.2, 6.0, 2.3, [
    ("Cách giữ chất lượng (eval gate, H8)", True),
    "Bộ kiểm tra: 100 nhiệm vụ thật cho mỗi cấp, đã che dữ liệu cá nhân",
    "Claude Opus 5.5 làm bài mẫu và chấm điểm; người chấm lại 10%",
    "Đạt khi điểm Haiku ≥ 95% điểm Opus. Chạy lại mỗi lần đổi model hoặc prompt (525 USD/tháng)"], size=12)
text(s, 6.8, 4.2, 6.0, 2.3, [
    ("Vì sao Haiku 5.5", True),
    "Rẻ: 0,10 USD/1M token vào, 0,50 USD/1M token ra; token đọc từ cache chỉ 0,01",
    "Điểm chất lượng cao nhất trong nhóm model cùng tầm giá (Artificial Analysis)",
    "Dùng Opus cho mọi cấp sẽ tốn 36.380 USD/tháng, gấp 38 lần",
    "Rủi ro: chưa có số đo độ trễ khi tắt reasoning → đo trong pilot"], size=12)
text(s, 0.5, 6.5, 12.3, 0.4, f"947 USD là tiền text. Cộng 147 USD tiền ảnh ≈ dòng llm {usd(c['llm'])} USD ở slide 11.", size=11)

# ================================================================ 5 tech choices
s = header("5. Mỗi lựa chọn đều rẻ hơn phương án thay thế",
           "Chọn phương án rẻ nhất mà vẫn đạt đủ ràng buộc H1–H8. Đơn vị: USD/tháng. Cách tính từng con số: slide 5b", "5a")
table(s, 0.5, 1.5, 12.3, [
    ["Quyết định", "Chọn", "Phương án so sánh", "Lý do"],
    ["Cloud chính", "GCP: 6.821 (tổng)", "AWS 8.643 · Azure 14.484", "Rẻ nhất; chênh lệch chủ yếu ở guardrail"],
    ["LLM gateway", "LiteLLM tự chạy: 0 tiền license", "Apigee ~1.595 · Azure APIM ~700", "Duy nhất có quota USD theo từng user và phòng ban (H8)"],
    ["Tìm kiếm vector", "pgvector trong Postgres: 0 thêm", "Vertex Vector Search ~84 · OpenSearch ~413", "Dữ liệu nhỏ; lọc quyền bằng SQL ngay trong database"],
    ["Cất token OAuth", "Mã hóa bằng KMS, lưu trong Postgres: ~4", "Secret Manager (12.000 secret) ~720", "Vẫn mã hóa và có audit, rẻ hơn 180 lần"],
    ["Sandbox", "GKE Sandbox (gVisor): 315", "Agent Engine 483 · AgentCore 509", "Có sẵn trên cụm GKE; chặn mạng ra ngoài bằng NetworkPolicy"],
    ["Guardrail", "Chỉ quét text mới: 281", "Quét toàn bộ token: 1.298", "Mỗi đoạn text chỉ quét một lần, khi vào hệ thống"],
    ["Connector", "Gọi API bằng OAuth của user", "Crawl toàn bộ dữ liệu vào index", "SaaS tự áp quyền gốc; không cần tài khoản quyền rộng"]],
    col_w=[1.7, 3.1, 3.3, 4.2], size=12, row_h=0.55)
text(s, 0.5, 6.4, 12.3, 0.5, "Giá niêm yết tại Singapore, đọc ngày 16/10/2026. Lựa chọn model: slide 4.", size=11)

s = header("5. Cách tính: đơn giá niêm yết × khối lượng tải",
           "Mỗi con số ở slide 5a = đơn giá của dịch vụ × khối lượng ước lượng ở slide 1b. Đơn vị: USD/tháng; 1 tháng = 730 giờ", "5b")
table(s, 0.5, 1.5, 12.3, [
    ["Quyết định", "Phương án chọn: cách tính", "Phương án so sánh: cách tính"],
    ["Cloud chính", "GCP 6.821 = tổng 20 dòng của báo giá (Phụ lục A)",
     "AWS 8.643, Azure 14.484: cùng khối lượng, tính theo giá của AWS, Azure. Nếu bỏ dòng governance, 3 cloud chênh nhau dưới 8%. "
     "Chênh lệch nằm ở guardrail + che PII: GCP 281, AWS ~1.910, Azure ~7.534"],
    ["LLM gateway", "LiteLLM là phần mềm miễn phí. 2 pod chạy trong cụm GKE, tiền máy đã nằm trong dòng compute",
     "Apigee: môi trường Intermediate 1.460 + phí theo lượt gọi model (100 USD/1 triệu lượt) ≈ 1.595. "
     "Azure APIM Standard v2: 0,96 USD/giờ × 730 giờ ≈ 700"],
    ["Tìm kiếm vector", f"pgvector là extension của Postgres, chạy trong database đã có ({usd(c['database'])} USD), chỉ tốn thêm ít dung lượng",
     "Vertex Vector Search: tối thiểu 1 máy e2-standard-2 chạy 24/7 ≈ 84. "
     "OpenSearch: tối thiểu 2 OCU × 0,283 USD/giờ × 730 giờ ≈ 413"],
    ["Cất token OAuth", "3 khóa KMS × 0,06 + 760.000 lần mã hóa/giải mã × 0,03 USD/10.000 lần + 20 secret hệ thống ≈ 4",
     "Mỗi token một secret: 2.000 user × 6 connector = 12.000 secret × 0,06 USD ≈ 720"],
    ["Sandbox", "140.800 lượt × 2 phút = 4.693 vCPU-giờ × 0,0549 + 9.386 GB-giờ × 0,0061 ≈ 315",
     "Cùng số giờ, theo giá Agent Engine (0,085 USD/vCPU-giờ) ≈ 483; AgentCore (0,0895 USD/vCPU-giờ) ≈ 509"],
    ["Guardrail", "Chỉ quét text mới: 2,81 tỉ token/tháng × 0,10 USD/1 triệu token ≈ 281",
     "Quét toàn bộ token: (12,19 + 0,79) tỉ token × 0,10 USD/1 triệu token ≈ 1.298"]],
    col_w=[1.7, 4.9, 5.7], size=12, row_h=0.62)
text(s, 0.5, 6.15, 12.3, 0.8, ["Giá niêm yết tại Singapore, đọc ngày 16/10/2026, chưa VAT. Sandbox tính theo trần 2 phút/lượt nên là cận trên.",
                               "Đơn giá và khối lượng của từng dòng: cột Ghi chú và Bằng chứng trong G03_baogia.xlsx."], size=11)

# ================================================================ 6 connectors & authz
s = header("6. Agent chỉ thấy những gì user được thấy (H2)",
           "Agent dùng 11 connector (Google, Microsoft, Atlassian, Notion) bằng quyền OAuth của chính user", 6)
text(s, 0.5, 1.6, 6.1, 4.8, [
    ("Đăng nhập", True),
    "SSO bằng tài khoản tập đoàn có sẵn, bắt buộc MFA",
    "Phân quyền chức năng theo nhóm (ví dụ: chỉ IT dùng sandbox hạng lớn)",
    ("Agent mượn quyền của user (OAuth)", True),
    "Mỗi user tự cho phép từng SaaS; mặc định chỉ quyền đọc",
    "Quyền ghi (gửi email, tạo ticket) chỉ xin khi cần",
    "Không dùng tài khoản dịch vụ có quyền rộng"], size=15)
text(s, 6.9, 1.6, 6.0, 4.8, [
    ("Token được cất an toàn", True),
    "Token OAuth được mã hóa bằng khóa trong Cloud KMS, lưu trong Postgres",
    "Chỉ worker được giải mã, và chỉ cho đúng user của request. Mỗi lần giải mã đều ghi audit",
    ("Tài liệu giữ quyền gốc", True),
    "Mail, lịch, Jira: agent gọi search API của SaaS bằng token của user, nên SaaS tự lọc quyền",
    "Tài liệu chung đã index: mỗi đoạn ghi nhóm được xem; mọi truy vấn lọc theo nhóm của user"], size=15)
text(s, 0.5, 6.4, 12.3, 0.5, "API của 11 SaaS không tính phí theo lượt; tập đoàn đã có license SaaS. Rate limit của SaaS: slide 12.", size=11)

# ================================================================ 7 workspace & sandbox
s = header("7. File của user A không lộ sang user B (H3)",
           "\"Agent của A có đọc được file của B không?\" Không, vì có 4 lớp chặn:", 7)
table(s, 0.5, 1.5, 6.2, [
    ["Lớp", "Cách chặn"],
    ["Lưu trữ", "Mỗi user một thư mục riêng; chỉ app có quyền vào bucket"],
    ["Database", "Postgres tự lọc dòng theo người sở hữu (Row-Level Security)"],
    ["Tìm kiếm", "Mọi truy vấn bắt buộc lọc theo người sở hữu hoặc nhóm"],
    ["Connector", "Dùng OAuth của chính user, nên không thấy dữ liệu người khác"]],
    col_w=[1.3, 4.9], size=14, row_h=0.7)
text(s, 7.0, 1.5, 5.9, 5.0, [
    ("Sandbox: code của agent chạy trong hộp kín", True),
    "gVisor ngăn code chạm trực tiếp vào kernel của máy chủ",
    "Không có mạng ra ngoài: không internet, không mạng nội bộ",
    "Chỉ thấy thư mục workspace của đúng user đó",
    "Tối đa 2 phút (hạng lớn 10 phút); chạy xong hoặc hết giờ thì hủy pod",
    ("Code cố thoát ra máy chủ?", True),
    "Bị gVisor chặn. Pod không có quyền đặc biệt và không gọi được API của cloud"], size=15)

# ================================================================ 8 governance
s = header("8. Lệnh ẩn trong email bị chặn ở 3 chỗ (H4, H5)",
           "\"Một email chứa lệnh ẩn: gửi toàn bộ hợp đồng ra ngoài.\" Lệnh này không chạy được, vì:", 8)
text(s, 0.5, 1.5, 6.1, 5.0, [
    ("1. Guardrail quét nội dung", True),
    "Model Armor quét tin nhắn mới, nội dung từ connector và câu trả lời cuối (281 USD/tháng)",
    ("2. Nội dung email chỉ là dữ liệu", True),
    "Nội dung từ connector được đánh dấu \"không tin cậy\". Chỉ yêu cầu của user mới kích hoạt được hành động ghi",
    ("3. User xác nhận trước khi ghi", True),
    "Gửi ra ngoài, xóa, chia sẻ quyền: xác nhận từng việc. Ticket, email nháp: duyệt một lần cho cả nhóm",
    "Thêm nữa: sandbox không có mạng ra ngoài, nên code cũng không gửi được dữ liệu"], size=14)
text(s, 6.9, 1.5, 6.0, 5.0, [
    ("Bảo vệ dữ liệu", True),
    "Mã hóa khi lưu và khi truyền",
    "Che dữ liệu cá nhân (PII) trước khi gửi cho model",
    "Vertex AI không lưu và không dùng dữ liệu để huấn luyện",
    "Audit log 12 tháng: ai, lúc nào, dùng tool nào, xác nhận hành động gì",
    ("Eval gate", True),
    "Đổi model hoặc prompt phải chạy lại bộ kiểm tra; dưới 95% thì không deploy (525 USD/tháng)"], size=14)
text(s, 0.5, 6.4, 12.3, 0.5, f"Dòng governance ở slide 11 = 281 USD guardrail + 525 USD eval = {usd(c['governance'])} USD/tháng. "
                             "Thời hạn lưu khác: chat 12 tháng, file tạm 30 ngày, prompt log 30 ngày (đã che PII).", size=11)

# ================================================================ 9 HA DR
s = header("9. Mất 1 zone: tự chuyển trong 1–2 phút (H7)",
           "Đề yêu cầu: chạy 99,5% giờ hành chính, khôi phục trong 4 giờ (RTO), mất tối đa 1 giờ dữ liệu (RPO)", 9)
table(s, 0.5, 1.5, 7.0, [
    ["Thành phần", "Chạy liên tục (HA)", "Backup, khôi phục (DR)"],
    ["Tường lửa, cân bằng tải", "Managed, đa zone", "—"],
    ["Cụm GKE", "Mỗi pod 2 bản ở 2 zone", "Dựng lại bằng Terraform"],
    ["LiteLLM, web, worker", "2 bản, 2 zone", "Image lưu trong Artifact Registry"],
    ["Postgres (Cloud SQL)", "Bản dự phòng ở zone khác, tự chuyển", "Backup hằng ngày, khôi phục về thời điểm bất kỳ; bản sao ở Jakarta"],
    ["Cache", "Bản chính + bản phụ", "Không cần (chỉ dữ liệu tạm)"],
    ["File workspace", "Đa zone", "Lưu ở 2 region"],
    ["Vertex AI", "Endpoint global", "Model dự phòng qua LiteLLM"]],
    col_w=[1.9, 2.4, 2.7], size=11, row_h=0.45)
text(s, 7.8, 1.5, 5.1, 5.2, [
    ("Khi mất 1 zone lúc 10:00", True),
    "Cân bằng tải chuyển traffic sang zone còn lại; GKE tạo thêm pod",
    "Postgres tự chuyển sang bản dự phòng trong vài chục giây đến 1–2 phút",
    "Vài request lỗi, user gửi lại được; dữ liệu đã lưu không mất",
    ("Khi mất cả region Singapore", True),
    "Dựng lại ở Jakarta bằng Terraform và backup đã sao chép: ≤ 4 giờ, mất ≤ 1 giờ dữ liệu",
    ("Diễn tập và chi phí", True),
    f"Thử khôi phục DB mỗi quý, dựng region DR mỗi 6 tháng. backup_dr: {usd(c['backup_dr'])} USD/tháng"], size=12)

# ================================================================ 10 monitoring finops
per_user = (c['llm'] + c['governance'] + c['sandbox']) / 2000
s = header("10. Mỗi user có quota USD; vượt thì hạ cấp (H8)",
           "LiteLLM ghi chi phí của từng user và phòng ban, nên mỗi tháng biết ai tiêu bao nhiêu và chặn được khi vượt", 10)
text(s, 0.5, 1.5, 6.1, 5.0, [
    ("Cảnh báo chính", True),
    "Chậm: p95 thời gian tới token đầu tiên > 3 giây trong 10 phút",
    "Agent chạy quá 10 phút; tỉ lệ lỗi > 2%",
    "Cache hit < 50%, tức chi phí LLM sắp tăng",
    "Chi tiêu trong ngày vượt dự báo 20%",
    ("Dashboard", True),
    "Token và USD theo user, phòng ban, model, cấp",
    "Số lần guardrail chặn, số hành động ghi bị user từ chối"], size=13)
table(s, 6.9, 1.5, 6.0, [
    ["Mức dùng quota tháng", "Hành động"],
    ["80%", "Cảnh báo user; báo trưởng phòng nếu là quota phòng"],
    ["100%", "Hạ cấp: cấp 1–2 chỉ dùng model rẻ nhất; khóa cấp 4–5"],
    ["120%", "Chặn đến đầu tháng sau, trừ khi trưởng phòng duyệt"],
    ["90% ngân sách hệ thống", "Cảnh báo nhóm FinOps và ban IT"]],
    col_w=[2.2, 3.8], size=12, row_h=0.5)
text(s, 6.9, 4.3, 6.0, 2.3, [
    ("Quota đặt bao nhiêu?", True),
    f"Chi phí theo lượt dùng (LLM + guardrail + sandbox) ≈ {vn(per_user)} USD/user/tháng",
    f"Quota mặc định: 3 USD/user/tháng, gần {3 / per_user:.0f} lần mức trung bình, đủ cho người dùng nhiều",
    "Báo cáo hằng tháng theo phòng ban"], size=12)

# ================================================================ 11a cost breakdown
top5 = sorted(c.items(), key=lambda kv: -kv[1])[:5]
assert [k for k, _ in top5] == ["ops_labor", "llm", "governance", "database", "sandbox"]
rest = sorted([(k, v) for k, v in c.items() if k not in dict(top5) and v > 0], key=lambda kv: -kv[1])
rest_sum = TOTAL - sum(v for _, v in top5)
s = header(f"11. Chi phí: một nửa là nhân sự, LLM chỉ {share('llm')}",
           f"Tổng 6.821,44 USD/tháng, tức 3,41 USD/DAU. Bảng dưới giải thích vì sao mỗi khoản ra con số này", "11a")
table(s, 0.5, 1.5, 12.3, [
    ["Khoản", "USD/tháng", "%", "Cách tính", "Vì sao lớn hay nhỏ"],
    ["ops_labor (nhân sự)", usd(c["ops_labor"]), share("ops_labor"),
     "2 kỹ sư trực luân phiên: SRE 5–8 năm (53,85 triệu VND) + AI/MLOps 3–4 năm (34,1 triệu VND) = 87,95 triệu VND ÷ 25.870 VND/USD",
     "Lớn nhất vì cố định: cần người trực để giữ 99,5% (H7), vận hành LiteLLM và eval. Không giảm khi ít người dùng"],
    ["llm", usd(c["llm"]), share("llm"),
     "Lượt × số lần gọi model × token × giá. Cấp 1: 386 · cấp 2: 288 · cấp 3: 161 · cấp 4: 105 · cấp 5: 7 + ảnh 147 (4.312 ảnh × 0,034)",
     "Nhỏ vì Haiku rẻ (0,10 USD/1M token vào) và 61% token vào đọc từ cache với giá 0,01"],
    ["governance", usd(c["governance"]), share("governance"),
     "Guardrail: 2,81 tỉ token × 0,10 USD/1M = 281. Eval gate: 4 lần/tháng × 5 cấp × 100 nhiệm vụ = 525",
     "Eval đắt hơn guardrail vì Opus 5.5 vừa làm bài mẫu vừa chấm điểm"],
    ["database", usd(c["database"]), share("database"),
     "Postgres HA 2 vCPU, 13 GB × 730 giờ = 355 · SSD 150 GB = 71 · database staging = 41",
     "Chạy 24/7, có bản dự phòng ở zone khác. Chứa luôn vector và token, nên không cần dịch vụ riêng"],
    ["sandbox", usd(c["sandbox"]), share("sandbox"),
     "140.800 lượt × 2 phút = 4.693 vCPU-giờ × 0,0549 + 9.386 GB-giờ × 0,0061",
     "Là cận trên: thời gian chạy thật chưa đo, nên mỗi lượt tính đủ 2 phút tối đa"],
    [f"{len(rest)} khoản còn lại", usd(rest_sum), f"{rest_sum / TOTAL * 100:.0f}%",
     " · ".join(f"{k} {usd(v)}" for k, v in rest[:5]) + " · …",
     "Hạ tầng gọn: 1 cụm GKE, 1 region, phần lớn chỉ chạy đủ trong giờ hành chính"]],
    col_w=[1.8, 1.1, 0.7, 4.7, 4.0], size=11, row_h=0.68)
text(s, 0.5, 6.45, 12.3, 0.5, "Đơn giá và bằng chứng từng dòng: Phụ lục A và G03_baogia.xlsx. Không dùng free tier, credit hay giá khuyến mãi.", size=11)

# ================================================================ 11b savings levers
s = header("11. Đòn bẩy: mỗi lựa chọn tiết kiệm bao nhiêu",
           "Tiết kiệm = chi phí của phương án thay thế − chi phí của phương án nhóm chọn. Đơn vị: USD/tháng", "11b")
table(s, 0.5, 1.5, 12.3, [
    ["Đòn bẩy", "Tiết kiệm", "Cách tính"],
    ["Haiku cho cả 5 cấp, thay Sonnet ở cấp 3–4", "4.705", "Sonnet cho cấp 3 tốn thêm 2.939, cấp 4 tốn thêm 1.766. Eval gate kiểm tra Haiku vẫn đạt ≥ 95% điểm Opus"],
    ["LiteLLM thay Apigee", "~1.595", "Apigee: môi trường Intermediate 1.460 + phí theo lượt gọi. LiteLLM miễn phí, chạy trong compute"],
    ["Guardrail chỉ quét text mới", "1.018", "Quét toàn bộ 12,98 tỉ token = 1.298 − quét 2,81 tỉ token mới = 281"],
    ["Cất token bằng KMS trong Postgres", "~716", "12.000 secret × 0,06 = 720 − KMS ≈ 4"],
    ["Prompt caching", "670", "7,44 tỉ token vào đọc từ cache × (0,10 − 0,01) USD/1M token"],
    ["Ngoài giờ chỉ chạy 1 pod mỗi loại", "109", "510 giờ ngoài giờ × 3 loại pod: 1.530 vCPU-giờ × 0,0549 + 4.080 GB-giờ × 0,0061"],
    ["pgvector trong Postgres", "~84", "Vertex Vector Search cần tối thiểu 1 máy chạy 24/7"],
    ["Staging dùng chung cụm GKE", "73", "Cụm riêng mất thêm phí quản lý: 0,10 USD/giờ × 730 giờ"]],
    col_w=[3.8, 1.3, 7.2], size=12, row_h=0.5)
text(s, 0.5, 6.1, 12.3, 0.8, ["Mỗi dòng so với một phương án thay thế riêng, nên không cộng dồn các dòng.",
                              "Chưa tính phí ghi cache của Claude (ước tính vài %). Không mua gói support. Không có dòng dự phòng."], size=11)


# ================================================================ 12 risk
s = header("12. Rủi ro lớn nhất: Haiku không đạt eval ở cấp 3–4",
           "Khi đó chi phí lên 11.526 USD/tháng. Nhóm đã tính sẵn; LiteLLM đổi model bằng 1 dòng cấu hình", 12)
table(s, 0.5, 1.5, 6.3, [
    ["Kịch bản", "USD/tháng", "USD/DAU"],
    ["Cơ sở (2.000 DAU)", "6.821", "3,41"],
    ["DAU gấp đôi = 4.000", "8.826", "2,21"],
    ["Giá token +30%", "7.263", "3,63"],
    ["Giá token −50%", "6.085", "3,04"],
    ["Cấp 3–4 phải nâng lên Sonnet 5.5", "11.526", "5,76"],
    ["Workspace đầy 20 TB", "+ ~704", "—"]],
    col_w=[3.3, 1.5, 1.5], size=12, row_h=0.42)
text(s, 0.5, 4.7, 6.3, 2.0, [
    ("Khi DAU gấp đôi, USD/DAU giảm", True),
    "Tăng theo lượt dùng: LLM, guardrail, sandbox, lưu trữ, log",
    "Gần như cố định: 2 kỹ sư, cụm GKE, database, cache, cân bằng tải",
    "Chỉ xét tự host GPU khi tiền token vượt chi phí chạy ≥ 2 GPU 24/7 cộng vận hành"], size=12)
text(s, 7.1, 1.5, 5.8, 5.2, [
    ("Các rủi ro khác và cách xử lý", True),
    "Token thực tế khác giả định: nhóm dùng 13 tỉ token/tháng, khoảng có thể là 4,6–42,8 tỉ → đo trong pilot 2–4 tuần",
    "Luật bảo vệ dữ liệu cá nhân (Nghị định 13/2023): Vertex AI dùng endpoint global → dữ liệu nhạy cảm dùng model chạy tại Singapore",
    "LiteLLM là open source, không có SLA → 2 kỹ sư trực, cố định phiên bản, test trên staging",
    "Rate limit Jira/Confluence dùng chung cho cả app (65.000 điểm/giờ) → hàng đợi và thử lại",
    "Google dự kiến tính phí API Workspace từ cuối 2026 (chưa công bố giá)"], size=12)

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
    "Token mỗi lượt chat (số lần gọi model × token vào / token ra): cấp 1: 2 × 5,5k / 250 · cấp 2: 2 × 18k / 2,5k · cấp 3: 3,5 × 12k / 1k · cấp 4: 8 × 15k / 300 · cấp 5: 1,5 × 4k / 600 + 1 ảnh",
    "Nguồn token: Azure OpenAI On your data defaults; Vertex RAG Engine; DA-Code; DABstep; MCP-Universe; MCPMark; OpenRouter State of AI 2025; Azure LLM inference trace 2024",
    "Chất lượng và tốc độ model: Artificial Analysis Intelligence Index v4.3.2",
    "Lương: ITviec Vietnam IT Salary & Recruitment Market 2024–2025; tỉ giá Vietcombank ngày 16/10/2026",
    "Connector: Microsoft Graph throttling, Atlassian rate limiting, Notion request limits, Google Workspace API limits",
    "Chi tiết nghiên cứu: thư mục research/ (usage-benchmarks, task-volume-by-role, token-per-task, r1, r2, r3, r5-r9, r8-r6) và cost_model.py"], size=13)

# ================================================================ appendix C: common tasks
s = header("Phụ lục C. Việc chung của mọi nhân viên: 6,26 nhiệm vụ/ngày", "Ai cũng làm 5 việc này. Số nhiệm vụ = khối lượng việc thật mỗi ngày × tỉ lệ giao cho AI", "C")
table(s, 0.5, 1.5, 12.3, [
    ["Việc", "Cấp", "Khối lượng thật/người/ngày", "Tỉ lệ giao AI", "Nhiệm vụ/người/ngày", "Căn cứ"],
    ["Soạn, trả lời email", "1", "9,9 email gửi", "30%", "2,97", "Trung bình nhân của 2,9 (Microsoft RCT 2025) và 34 (Radicati). 30% cao hơn mức 10–24% của Liang 2025 vì công ty triển khai chính thức"],
    ["Tóm tắt, phân loại email", "1", "32,2 email đọc", "5%", "1,61", "Microsoft RCT 2025: 160,8 email đọc/tuần. Tỉ lệ 5%: giả định của nhóm"],
    ["Hỏi đáp tài liệu nội bộ", "1", "4,0 lần tra cứu", "30%", "1,20", "Mỗi người mất 1,6–2 giờ/ngày tìm thông tin (McKinsey, Atlassian). 4 lần và 30%: giả định của nhóm"],
    ["Biên bản họp → DOCX", "2", "2,0 cuộc họp", "20%", "0,40", "Microsoft RCT 2025: 9,9 cuộc họp/tuần. Tỉ lệ 20%: giả định của nhóm"],
    ["Báo cáo, đề xuất → DOCX/PPTX", "2", "0,15 tài liệu", "50%", "0,08", "Microsoft RCT 2025: 0,76 tài liệu Word hoàn thành/tuần. Tỉ lệ 50%: giả định của nhóm"],
    ["Cộng", "", "", "", "6,26", ""]],
    col_w=[2.5, 0.6, 2.0, 1.1, 1.4, 4.7], size=11, row_h=0.55)
text(s, 0.5, 5.6, 12.3, 1.3, [
    ("Đọc bảng thế nào", True),
    "Ví dụ dòng đầu: mỗi người gửi khoảng 9,9 email/ngày. Nhóm giả định 30% số email đó nhờ AI soạn, nên 9,9 × 30% = 2,97 nhiệm vụ.",
    "Khối lượng việc lấy từ số đo thật (telemetry, khảo sát). Tỉ lệ giao AI phần lớn là giả định của nhóm; nhóm sẽ đo lại trong pilot 2–4 tuần."], size=12)

# ================================================================ appendix D: per-department tasks
rows = [["Phòng ban (số người)", "Phòng làm gì", "Việc riêng giao AI (nhiệm vụ/người/ngày)", "Mỗi người/ngày", "Cả phòng/ngày"]]
DEPT_INFO = {
    "Kinh doanh, CSKH": ("Bán hàng, chăm sóc khách hàng", "Phân tích doanh số trên Excel 0,10 · agent chuẩn bị gặp khách 0,10 · ảnh cho báo giá 0,03"),
    "Quản lý dự án, vận hành": ("Điều phối dự án, vận hành hằng ngày", "Agent tạo ticket Jira, trang Confluence 0,90 · phân tích dữ liệu vận hành 0,12 · báo cáo tuần 0,10 · sơ đồ quy trình 0,08"),
    "Kế toán": ("Sổ sách, thanh toán, báo cáo tài chính", "Phân tích bảng tính tài chính, đối soát 0,80 · tìm hóa đơn bất thường 0,30 · checklist khóa sổ 0,05"),
    "Nhân sự, HC, pháp chế": ("Tuyển dụng, chính sách, hợp đồng", "Rà soát hợp đồng 0,15 · soạn mô tả công việc, chính sách 0,09 · tổng hợp chấm công 0,08 · đặt lịch phỏng vấn 0,05"),
    "Marketing": ("Nội dung, chiến dịch, hình ảnh", "Viết bài đăng, thông cáo 0,80 · ảnh, banner 0,25 · số liệu chiến dịch 0,12 · cập nhật kế hoạch 0,08"),
    "IT": ("Phát triển phần mềm, hạ tầng, hỗ trợ", "Tra cứu, phân loại ticket hỗ trợ 0,60 · agent cập nhật Jira, runbook 0,20 · viết code 0,16 · review code 0,08 · sơ đồ 0,05"),
    "Mua hàng, SCM": ("Nhà cung cấp, đặt hàng, giao hàng", "So sánh báo giá nhà cung cấp 0,56 · agent cập nhật lịch giao hàng 0,05"),
    "Lãnh đạo, trợ lý": ("Ra quyết định, họp nhiều", "Họp 4,6 cuộc/ngày nên biên bản họp là 0,92 thay vì 0,40 · agent chuẩn bị briefing 0,92 · sắp lịch 0,20 · slide 0,10"),
}
base = Decimal("6.26")
for k, v, n, per in dept:
    total = r2(per)
    rows.append([f"{k} ({n})", DEPT_INFO[k][0], DEPT_INFO[k][1], f"6,26 + {vn(total - base)} = {vn(total)}", f"{n} × {vn(total)} = {usd(v)}"])
rows.append(["Toàn công ty (2.000)", "", "", f"{vn(T / 2000)} (trung bình)", usd(T)])
s = header("Phụ lục D. Việc riêng của từng phòng ban", "Mỗi người = 6,26 nhiệm vụ việc chung + việc riêng của phòng. Cả phòng = số người × nhiệm vụ mỗi người", "D")
table(s, 0.5, 1.45, 12.3, rows, col_w=[2.0, 2.1, 4.6, 1.7, 1.9], size=10, row_h=0.47)
text(s, 0.5, 6.45, 12.3, 0.5, "Số đã làm tròn 2 chữ số. Nguồn khối lượng việc riêng: APQC (hóa đơn, đơn mua hàng), Graphite (code), MetricNet (ticket IT), HBR 2017 (giờ họp của lãnh đạo); còn lại là giả định của nhóm.", size=10)

prs.save("G03_slide.pptx")
print("slides", len(prs.slides), "TOTAL", TOTAL)
