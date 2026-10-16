"""Generate G03_baogia.xlsx (GCP, DR option B) from cost_model.py.

Run: <venv>/bin/python gen_baogia.py
"""
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation

import cost_model as m

A, P, L = m.A, m.P["gcp"], m.P["llm"]
H, HO, HF = m.H_MONTH, m.H_OFFICE, m.H_OFF
DATE = "2026-10-16"

EVID = [
    ("E01", "GKE pricing: phí cluster, Autopilot Pod (container-optimized) asia-southeast1", "https://cloud.google.com/kubernetes-engine/pricing"),
    ("E02", "Vertex AI pricing: Claude Haiku 5.5 global (input, cache read, output); Gemini Flash-Lite Image", "https://cloud.google.com/vertex-ai/generative-ai/pricing"),
    ("E03", "Vertex AI pricing: gemini-embedding-001", "https://cloud.google.com/vertex-ai/generative-ai/pricing"),
    ("E04", "Cloud Load Balancing + Cloud Armor + Cloud NAT + PSC + egress/inter-zone (VPC network pricing)", "https://cloud.google.com/vpc/network-pricing"),
    ("E05", "Identity-Aware Proxy pricing", "https://cloud.google.com/iap/pricing"),
    ("E06", "Cloud SQL for PostgreSQL pricing (Enterprise, HA, SSD, backup)", "https://cloud.google.com/sql/pricing"),
    ("E07", "Cloud Storage pricing (Standard, dual-region, operations, replication)", "https://cloud.google.com/storage/pricing"),
    ("E08", "Memorystore for Valkey pricing", "https://cloud.google.com/memorystore/docs/valkey/pricing"),
    ("E09", "Cloud Tasks pricing", "https://cloud.google.com/tasks/pricing"),
    ("E10", "Cloud KMS pricing", "https://cloud.google.com/kms/pricing"),
    ("E11", "Secret Manager pricing", "https://cloud.google.com/secret-manager/pricing"),
    ("E12", "Google Cloud Observability pricing (Logging, Managed Prometheus, Trace)", "https://cloud.google.com/stackdriver/pricing"),
    ("E13", "Security Command Center pricing: Model Armor (DLP đi kèm)", "https://cloud.google.com/security-command-center/pricing"),
    ("E14", "Cloud Armor pricing", "https://cloud.google.com/armor/pricing"),
    ("E15", "Cloud Build pricing", "https://cloud.google.com/build/pricing"),
    ("E16", "Artifact Registry pricing", "https://cloud.google.com/artifact-registry/pricing"),
    ("E17", "Cloud SQL extensions: pgvector (vector_db nằm trong database)", "https://cloud.google.com/sql/docs/postgres/extensions"),
    ("E18", "LiteLLM pricing: Open Source self-hosted, budgets + spend tracking (gateway, authz quota)", "https://www.litellm.ai/pricing"),
    ("E19", "Microsoft Graph throttling + Google Workspace API usage limits (connector không có phí API)", "https://learn.microsoft.com/en-us/graph/throttling"),
]

rows = []  # (component, y_nghia, ghi_chu, cost, evidence)


def add(comp, yn, gc, cost, ev):
    rows.append((comp, yn, gc, round(cost, 2), ev))


# ---- compute
per_type = 2 * HO + HF + A["staging_hours"]
add("compute", "Phí quản lý cluster GKE Autopilot regional (prod + staging namespace)",
    f"GKE regional, asia-southeast1, SLA 99,95%: 0,10 USD/giờ × {H} giờ. Staging là namespace riêng trong cùng cluster (D30)",
    P["cluster_h"] * H, "E01")
vh, gh = m.app_pod_hours()
add("compute", "Pod ứng dụng: web/API, LiteLLM gateway, worker connector/agent",
    f"Autopilot Pod container-optimized asia-southeast1. Mỗi loại 2 pod (2 zone, HA) × {HO} giờ hành chính + 1 pod × {HF} giờ ngoài giờ + 1 pod staging × {A['staging_hours']} giờ = {per_type} pod-giờ/loại. "
    f"3 loại × 1 vCPU = {vh:.0f} vCPU-giờ × 0,0549 + RAM {gh:.0f} GiB-giờ (web, worker 2 GiB; LiteLLM 4 GiB) × 0,0060729",
    vh * P["pod_vcpu_h"] + gh * P["pod_gb_h"], "E01")

# ---- llm
names = {1: "email, hỏi đáp", 2: "tài liệu", 3: "dữ liệu, code", 4: "agent dự án", 5: "thiết kế (text)"}
for t, (I, O, cs) in m.llm_tokens().items():
    calls, i, o, _ = A["tokens"][t]
    cost = (I * (1 - cs) * L["in"] + I * cs * L["cache"] + O * L["out"]) / 1e6
    add("llm", f"Claude Haiku 5.5 cấp {t} ({names[t]})",
        f"Vertex AI global, zero-retention, gọi qua PSC. {A['turns_per_day'][t]} lượt/ngày × 22 ngày × {calls} lần gọi × {i} token vào / {o} token ra. "
        f"Input {I/1e9:.3f} tỉ token: {1-cs:.0%} × 0,10 + {cs:.0%} cache × 0,01; output {O/1e9:.3f} tỉ × 0,50 USD/1M",
        cost, "E02")
img = m.images_month()
add("llm", "Sinh ảnh cấp 5 (Gemini 3.1 Flash-Lite Image)",
    f"Vertex AI global: {img:.0f} ảnh/tháng (297 lượt/ngày × 22 × 66% có ảnh) × 0,034 USD/ảnh 1K",
    img * P["image"], "E02")

# ---- embedding
add("embedding", "Embedding KB chung và workspace (gemini-embedding-001)",
    f"Vertex AI asia-southeast1: KB chung 100 triệu token × 10% thay đổi/tháng + 2.000 user × 60.000 token mới = {m.embed_tokens()/1e6:.0f} triệu token × 0,15 USD/1M. Index lần đầu 100 triệu token tính riêng (15 USD, một lần)",
    m.embed_tokens() / 1e6 * P["embed_per_1m"], "E03")

# ---- gateway / authn / authz
add("gateway", "LLM gateway LiteLLM open-source (quota USD, routing, fallback, log token)",
    "Bản open-source tự chạy, không phí license; chi phí nằm trong dòng compute (pod LiteLLM 2 replica ở 2 zone, 4 GiB)",
    0, "E18")
add("load_balancer", "Load balancer HTTPS regional trước web/API (TLS, health check)",
    f"Regional external Application LB asia-southeast1: forwarding rule 0,028 USD/giờ × {H} giờ + data {A['lb_gb_month']} GB vào + {A['lb_gb_month']} GB ra × 0,009 USD/GB. LB managed, đa zone",
    P["lb_rule_h"] * H + A["lb_gb_month"] * 2 * P["lb_gb"], "E04")
add("authn", "SSO với IdP tập đoàn (OIDC/SAML + MFA) qua Identity-Aware Proxy",
    "IAP + Workforce Identity Federation không tính phí riêng; chi phí nằm trong dòng load_balancer. MFA do IdP tập đoàn đảm nhận (D6)",
    0, "E05")
add("authz", "Phân quyền RBAC theo group SSO, ACL tài liệu, quota",
    "RLS + cột owner_id/allowed_groups trong Postgres và quota trong LiteLLM; chi phí nằm trong database và gateway (D25)",
    0, "E17; E18")

# ---- database
dbh = (P["db_vcpu"] * P["db_vcpu_ha_h"] + P["db_ram"] * P["db_gb_ha_h"]) * H
add("database", "Cloud SQL PostgreSQL HA prod (chat, metadata, token vault, pgvector)",
    f"Cloud SQL Enterprise, asia-southeast1, HA (standby ở zone khác): (2 vCPU × 0,1156 + 13 GB × 0,0196) USD/giờ × {H} giờ",
    dbh, "E06")
add("database", "Ổ SSD cho Cloud SQL HA prod",
    f"{A['db_storage_gb']} GB SSD HA × 0,476 USD/GB-tháng (chat 12 tháng, vector, spend log)",
    A["db_storage_gb"] * P["db_ssd_ha_gb"], "E06")
add("database", "Cloud SQL staging (không HA)",
    f"db-g1-small 0,049 USD/giờ × {H} giờ + {A['staging_db_gb']} GB SSD × 0,238; staging dữ liệu giả (D16)",
    P["stg_db_h"] * H + A["staging_db_gb"] * P["stg_ssd_gb"], "E06")
add("vector_db", "Vector search cho KB chung và workspace (pgvector)",
    "pgvector chạy trong Cloud SQL, lọc theo owner_id/allowed_groups; chi phí nằm trong dòng database",
    0, "E17")

# ---- object storage
gb = A["ws_gb_per_user"] * A["users"]
add("object_storage", "Workspace riêng từng user trên Cloud Storage",
    f"GCS Standard asia-southeast1: {gb:.0f} GB (2.000 user × 2 GB dùng thực tế, quota 10 GB) × 0,020 + {A['obj_writes_month']/1e3:.0f}k ghi × 0,005/1k + {A['obj_reads_month']/1e3:.0f}k đọc × 0,0004/1k",
    gb * P["obj_gb"] + A["obj_writes_month"] / 1e3 * P["obj_w_1k"] + A["obj_reads_month"] / 1e3 * P["obj_r_1k"], "E07")

# ---- cache_queue
add("cache_queue", "Memorystore for Valkey (cache phiên, rate limit LiteLLM)",
    f"Memorystore Valkey asia-southeast1, 2 node (primary + replica khác zone) × 0,037884 USD/giờ × {H} giờ",
    P["cache_node_h"] * P["cache_nodes"] * H, "E08")
add("cache_queue", "Cloud Tasks: hàng đợi agent chạy nền, retry",
    f"{A['queue_ops_month']/1e6:.1f} triệu thao tác/tháng × 0,40 USD/1M",
    A["queue_ops_month"] / 1e6 * P["queue_1m"], "E09")

# ---- sandbox
sv, sg = m.sandbox_hours()
add("sandbox", "Sandbox gVisor (GKE Sandbox) chạy code của agent",
    f"Autopilot Pod + runtimeClass gvisor, không egress, hủy sau khi chạy. {A['sandbox_runs_month']:.0f} lượt/tháng × trần 2 phút = {sv:.0f} vCPU-giờ × 0,0549 + {sg:.0f} GiB-giờ × 0,0060729",
    sv * P["pod_vcpu_h"] + sg * P["pod_gb_h"], "E01")

# ---- connectors
add("connectors", "Connector Google Workspace, M365, Notion, Jira, Confluence",
    "Chạy trong worker pod (nằm trong dòng compute); API của 11 SaaS không tính phí theo lượt với OAuth ủy nhiệm; license SaaS tập đoàn đã có (D18)",
    0, "E19")

# ---- secrets_kms
add("secrets_kms", "Cloud KMS (envelope encryption token OAuth) + Secret Manager",
    f"KMS {A['kms_keys']} key × 0,06 + {A['kms_ops_month']/1e3:.0f}k thao tác × 0,03/10k; Secret Manager {A['app_secrets']} secret × 0,06 + {A['secret_access_month']/1e3:.0f}k truy cập × 0,03/10k",
    A["kms_keys"] * P["kms_key"] + A["kms_ops_month"] / 1e4 * P["kms_op_10k"] + A["app_secrets"] * P["secret_ver"] + A["secret_access_month"] / 1e4 * P["secret_op_10k"],
    "E10; E11")

# ---- backup_dr (option B)
add("backup_dr", "Backup Cloud SQL tự động + PITR (RPO 1 giờ)",
    f"{A['db_backup_gb']} GB backup × 0,112 USD/GB-tháng, PITR bật, diễn tập khôi phục hằng quý",
    A["db_backup_gb"] * P["db_backup_gb"], "E06")
add("backup_dr", "DR sang region Jakarta: bản sao backup DB",
    f"Truyền {A['dr_db_transfer_gb']} GB × 0,10 USD/GB + lưu {A['db_backup_gb']} GB × 0,112 (giá SG làm proxy); RTO 4 giờ dựng lại bằng IaC",
    A["dr_db_transfer_gb"] * P["dr_xfer_gb"] + A["db_backup_gb"] * P["dr_db_store_gb"], "E04; E06")
add("backup_dr", "DR workspace: chuyển bucket sang dual-region",
    f"Phần chênh dual-region: {gb:.0f} GB × (0,044 − 0,020) + replication {A['dr_new_obj_gb']} GB mới × 0,08 USD/GB",
    gb * (P["dual_region_gb"] - P["obj_gb"]) + A["dr_new_obj_gb"] * P["repl_gb"], "E07")

# ---- monitoring
add("monitoring", "Cloud Logging, Managed Prometheus, Trace, audit log 12 tháng",
    f"Log ứng dụng {A['app_log_gb']} GB + audit {A['audit_gb']} GB × 0,50 USD/GiB (gồm 30 ngày); audit archive {A['audit_gb']}×12 GB × 0,0015; prompt log {A['prompt_log_gb']} GB × 0,020 (30 ngày, che PII); "
    f"metric {A['metric_samples']/1e6:.0f}M mẫu × 0,06/1M; trace {A['trace_spans']/1e6:.0f}M span × 0,20/1M",
    m.gcp()[0]["monitoring"], "E12; E07")

# ---- governance
tin, tout = m.scanned_tokens()
add("governance", "Model Armor: guardrail vào/ra, chống prompt injection, DLP che PII",
    f"Chỉ quét text mới và không đáng tin (D24): {tin/1e9:.2f} tỉ token vào + {tout/1e9:.2f} tỉ token ra = {(tin+tout)/1e9:.2f} tỉ × 0,10 USD/1M; Sensitive Data Protection đi kèm Model Armor",
    (tin + tout) / 1e6 * P["guard_1m_tok"], "E13")
add("governance", "Eval gate trước khi đổi model hoặc prompt",
    f"{A['eval_runs_month']} lần/tháng × 5 cấp × {A['eval_tasks_per_tier']} nhiệm vụ: Haiku 5.5 + Opus 5.5 tham chiếu + Opus chấm điểm (2 lần × 3.000/300 token)",
    m.eval_cost(), "E02")

# ---- network
add("network", "Cloud Armor (WAF) trước load balancer",
    f"1 policy × 5 + {A['waf_rules']} rule × 1 + {A['http_req_month']/1e6:.1f}M request × 0,60 USD/1M",
    P["waf_policy"] + A["waf_rules"] * P["waf_rule"] + A["http_req_month"] / 1e6 * P["waf_req_1m"], "E14")
add("network", "Cloud NAT cho connector gọi SaaS (sandbox không egress)",
    f"{A['nat_vms_gcp']} node × {H} giờ × 0,0014 + {A['nat_gb_month']} GB × 0,045 + 1 IP tĩnh × {H} giờ × 0,005",
    A["nat_vms_gcp"] * H * P["nat_vm_h"] + A["nat_gb_month"] * P["nat_gb"] + H * P["ip_h"], "E04")
add("network", "Private Service Connect tới Vertex AI (H1)",
    f"1 endpoint PSC × {H} giờ × 0,01 USD/giờ; dữ liệu qua PSC tới Google APIs không tính phí",
    H * P["pe_h"], "E04")
add("network", "Egress internet tới user tại VN + truyền giữa các zone",
    f"Egress {A['egress_gb_month']} GB × 0,12 USD/GB + inter-zone {A['interzone_gb_month']} GB × 0,01 USD/GB (HA 2 zone)",
    A["egress_gb_month"] * P["egress_gb"] + A["interzone_gb_month"] * P["iz_gb"], "E04")

# ---- cicd
add("cicd", "Cloud Build + Artifact Registry + IaC (Terraform), deploy staging rồi prod",
    f"{A['build_min_month']} phút build × 0,006 USD/phút + registry {A['registry_gb']} GB × 0,10 USD/GB; image sandbox dựng sẵn (D14); staging namespace (D16)",
    A["build_min_month"] * P["build_min"] + A["registry_gb"] * P["registry_gb"], "E15; E16")

# ---- ops_labor / licenses
add("ops_labor", "2 FTE vận hành: SRE senior + AI/MLOps mid, trực luân phiên",
    "Package gross 12 tháng, trung vị ITviec 2024–2025: DevOps 5–8 năm 53,85 tr + AI Engineer 3–4 năm 34,1 tr = 87,95 tr VND/tháng ÷ 25.870 VND/USD (Vietcombank 16/10/2026)",
    3400, "NA")

total = round(sum(r[3] for r in rows), 2)

# ============================================================ write xlsx
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "BaoGia"
ws.append(["Component", "Ý nghĩa", "Ghi chú", "Chi phí/tháng (USD)", "Bằng chứng"])
for r in rows:
    ws.append(list(r))
ws.append(["TOTAL", "Tổng chi phí hạ tầng + vận hành mỗi tháng", f"{len(rows)} dòng; USD/DAU = {total/2000:.2f}", total, ""])
for c in ws[1]:
    c.font = Font(bold=True, color="FFFFFF")
    c.fill = PatternFill("solid", fgColor="1F4E78")
for c in ws[ws.max_row]:
    c.font = Font(bold=True)
for col, w in zip("ABCDE", (16, 48, 90, 20, 18)):
    ws.column_dimensions[col].width = w
for row in ws.iter_rows(min_row=2):
    for c in row:
        c.alignment = Alignment(wrap_text=True, vertical="top")
    row[3].number_format = "0.00"
COMPS = [
    "compute", "llm", "embedding", "gateway", "load_balancer", "authn", "authz", "database", "vector_db",
    "object_storage", "cache_queue", "sandbox", "connectors", "secrets_kms", "backup_dr", "monitoring",
    "governance", "network", "cicd", "ops_labor", "licenses", "contingency", "other", "TOTAL"]
dv = DataValidation(type="list", formula1='"' + ",".join(COMPS) + '"', allow_blank=False)
ws.add_data_validation(dv)
dv.add(f"A2:A{ws.max_row}")

ev = wb.create_sheet("BangChung")
ev.append(["evidence_id", "Mô tả", "Link", "Ngày chụp", "Ảnh chụp màn hình (dán vào đây)"])
for e in EVID:
    ev.append([e[0], e[1], e[2], DATE, ""])
for c in ev[1]:
    c.font = Font(bold=True)
for col, w in zip("ABCDE", (12, 70, 60, 12, 40)):
    ev.column_dimensions[col].width = w

wb.save("G03_baogia.xlsx")
print("rows", len(rows), "TOTAL", total, "per DAU", round(total / 2000, 2))
