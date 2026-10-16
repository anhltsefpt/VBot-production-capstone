"""VBot R0 cost model: GCP vs AWS vs Azure (Singapore), USD/month, list price.

Run: python3 cost_model.py            -> table + totals
     python3 cost_model.py --json     -> machine-readable output

Every unit price cites the research file (research/*.md) and SKU.
Every quantity cites a decision (PLAN.md D*) or is marked "GIẢ ĐỊNH CHƯA CHỐT".
"""
import json
import math
import sys

H_MONTH = 730          # 24/7 hours per month (đề)
H_OFFICE = 220         # 22 days x 10 h (đề)
H_OFF = H_MONTH - H_OFFICE   # 510 h off-hours (D3)
DAYS = 22

# ============================================================ ASSUMPTIONS
A = {
    # --- load (D21, D27, D29) ---
    "turns_per_day": {1: 20507, 2: 3153, 3: 2099, 4: 1042, 5: 297},           # D21 / sizing-load.md
    # tier: (LLM calls per turn, input tok/call, output tok/call, cached share)  D27
    "tokens": {1: (2, 5500, 250, .50), 2: (2, 18000, 2500, .60), 3: (3.5, 12000, 1000, .65),
               4: (8, 15000, 300, .80), 5: (1.5, 4000, 600, 0.0)},
    "image_share_t5": 0.66,          # 34% of T5 turns are code diagrams, no image (research/token-per-task.md, D27)
    # --- compute (D30) ---
    "app_pod_types": 3,              # web/API, LiteLLM, workers (D30)
    "pod_vcpu": 1, "pod_gb": 2,      # D30
    "pod_gb_litellm": 4,             # D30 updated: LiteLLM docs recommend >= 4 GiB per instance
    "staging_hours": 40,             # D16
    "azure_node_vcpu": 4, "azure_node_gb": 16,       # D4s_v5 (r1 §2.1)
    "azure_pack_eff": 0.70,          # GIẢ ĐỊNH CHƯA CHỐT: node bin-packing efficiency for autoscaled AKS pools
    # --- sandbox (D29) ---
    "sandbox_runs_month": (1051 + 2099 * 2.5 + 297 * 0.34) * DAYS,   # D29
    "sandbox_min_per_run": 2.0, "sandbox_vcpu": 1, "sandbox_gb": 2,  # D29 / D13 cap
    # --- embedding ---
    "kb_monthly_change_tok": 10e6,   # GIẢ ĐỊNH CHƯA CHỐT: shared KB 100M tokens, 10%/month re-embedded
    "ws_new_tok_per_user": 60e3,     # GIẢ ĐỊNH CHƯA CHỐT: 20 files x 3k tokens per user per month
    "kb_initial_tok": 100e6,         # GIẢ ĐỊNH CHƯA CHỐT: one-off initial index (not in monthly total)
    # --- storage (D5) ---
    "ws_gb_per_user": 2.0,           # GIẢ ĐỊNH CHƯA CHỐT: R4 proxies 1–5.4 GB/user (research/r2-data.md §5)
    "users": 2000,
    "obj_writes_month": 400e3, "obj_reads_month": 2e6,   # GIẢ ĐỊNH CHƯA CHỐT
    # --- database ---
    "db_storage_gb": 150,            # GIẢ ĐỊNH CHƯA CHỐT: chat 12 mo ~60 GB + ~3M vectors ~18 GB + LiteLLM spend logs ~16 GB + headroom
    "db_backup_gb": 100,             # GIẢ ĐỊNH CHƯA CHỐT: backup footprint ~ used data
    "staging_db_gb": 20,             # GIẢ ĐỊNH CHƯA CHỐT
    # --- queue / KMS ---
    "queue_ops_month": 1.1e6,        # GIẢ ĐỊNH CHƯA CHỐT: ~50k ops/day
    "kms_keys": 3, "kms_ops_month": 760e3,   # GIẢ ĐỊNH CHƯA CHỐT: ~30k token decrypts/day + misc
    "app_secrets": 20, "secret_access_month": 100e3,  # GIẢ ĐỊNH CHƯA CHỐT
    # --- network ---
    "lb_gb_month": 500,              # GIẢ ĐỊNH CHƯA CHỐT: traffic through LB (in+out each)
    "lb_avg_lcu": 1,                 # GIẢ ĐỊNH CHƯA CHỐT
    "http_req_month": 6.2e6,         # GIẢ ĐỊNH CHƯA CHỐT: 14,120 tasks/day x ~20 HTTP req x 22
    "waf_rules": 10,                 # GIẢ ĐỊNH CHƯA CHỐT
    "nat_gb_month": 100,             # GIẢ ĐỊNH CHƯA CHỐT: connector calls to SaaS
    "nat_vms_gcp": 4,                # GIẢ ĐỊNH CHƯA CHỐT: avg Autopilot nodes billed by Cloud NAT
    "llm_gb_month": 60,              # GIẢ ĐỊNH CHƯA CHỐT: ~13B tokens x ~4 bytes + overhead
    "egress_gb_month": 200,          # GIẢ ĐỊNH CHƯA CHỐT: responses + file downloads to users in VN
    "interzone_gb_month": 200,       # GIẢ ĐỊNH CHƯA CHỐT
    # --- monitoring (D12) ---
    "app_log_gb": 30,                # GIẢ ĐỊNH CHƯA CHỐT
    "audit_gb": 4,                   # GIẢ ĐỊNH CHƯA CHỐT: ~87k audit events/day x 2 KB
    "prompt_log_gb": 52,             # derived: ~13B tokens x 4 bytes, kept 30 days (D12)
    "metric_samples": 50e6, "custom_metrics_aws": 50, "alarms": 20,  # GIẢ ĐỊNH CHƯA CHỐT
    "trace_spans": 7e6,              # GIẢ ĐỊNH CHƯA CHỐT: ~5 spans per LLM call
    "azure_basic_log_scan_gb": 300, "azure_appinsights_gb": 5, "azure_log_alerts": 10,  # GIẢ ĐỊNH CHƯA CHỐT
    # --- governance (D24) ---
    # tokens scanned per turn: (new untrusted input, final output)  GIẢ ĐỊNH CHƯA CHỐT
    "scan_per_turn": {1: (3000, 250), 2: (10000, 2500), 3: (3000, 1000), 4: (12000, 300), 5: (200, 600)},
    "chars_per_token": 4,            # GIẢ ĐỊNH CHƯA CHỐT (Vietnamese/English mix)
    "eval_tasks_per_tier": 100, "eval_runs_month": 4,   # GIẢ ĐỊNH CHƯA CHỐT (D28 eval gate)
    "eval_ref_runs_month": 1,        # D35: Opus reference answers are stored and refreshed once a month
    "eval_judge_tok": (3000, 300),   # GIẢ ĐỊNH CHƯA CHỐT: judge input/output per task
    # --- CI/CD ---
    "build_min_month": 2000, "registry_gb": 20,   # GIẢ ĐỊNH CHƯA CHỐT
    # --- DR (Q9 pending) ---
    "dr_db_transfer_gb": 300, "dr_new_obj_gb": 200,   # GIẢ ĐỊNH CHƯA CHỐT
    # --- labor (D8) --- excluded from the quote per coach guidance (2026-10-16); was 3400
    "ops_labor_usd": 0,
}

# ============================================================ PRICES (USD)
P = {
 "llm": {  # research/r3-models.md §1.2 / §2.1 / §3.2 — Claude Haiku 5.5 global, same on 3 clouds
    "in": 0.10, "cache": 0.01, "out": 0.50,                 # per 1M tokens
    "opus_in": 4.00, "opus_out": 20.00,                     # eval reference (D28)
 },
 "gcp": {
    "cluster_h": 0.10,                        # r1 §1 GKE
    "pod_vcpu_h": 0.0549, "pod_gb_h": 0.0060729,   # r1 §2.3 Autopilot container-optimized
    "image": 0.034,                           # r3 §1.4 Gemini 3.1 Flash-Lite Image 1K
    "embed_per_1m": 0.15,                     # r3 §1.5 gemini-embedding-001 (0.00015/1k count; count=token NOT confirmed)
    "lb_rule_h": 0.028, "lb_gb": 0.009,       # r1 §5.1 regional forwarding rule, data processed in & out
    "waf_policy": 5, "waf_rule": 1, "waf_req_1m": 0.60,   # r1 §5.2 Cloud Armor regional
    "nat_vm_h": 0.0014, "nat_gb": 0.045, "ip_h": 0.005,   # r1 §5.3
    "pe_h": 0.01, "pe_gb": 0.0,               # r1 §5.4 PSC to Google APIs, no data charge
    "egress_gb": 0.12, "iz_gb": 0.01,         # r1 §5.5
    "db_vcpu_ha_h": 0.1156, "db_gb_ha_h": 0.0196,   # r2 §1.1 Cloud SQL Enterprise HA
    "db_vcpu": 2, "db_ram": 13,               # custom 2 vCPU / 13 GB (max 6.5 GB/vCPU)
    "db_ssd_ha_gb": 0.476, "db_backup_gb": 0.112,   # r2 §1.1
    "stg_db_h": 0.049, "stg_ssd_gb": 0.238,   # r2 §1.1 db-g1-small (no SLA, staging only)
    "obj_gb": 0.020, "obj_w_1k": 0.005, "obj_r_1k": 0.0004,   # r2 §4 GCS Standard regional
    "cache_node_h": 0.037884, "cache_nodes": 2,   # r2 §3.1 Memorystore Valkey custom-pico, primary+replica
    "queue_1m": 0.40,                         # r2 §3.2 Cloud Tasks
    "kms_key": 0.06, "kms_op_10k": 0.03, "secret_ver": 0.06, "secret_op_10k": 0.03,  # r5 §3
    "log_gb": 0.50, "archive_gb": 0.0015, "std_gb": 0.020,   # r5 §5.1/5.3
    "prom_1m": 0.06, "trace_1m": 0.20,        # r5 §5.2
    "guard_1m_tok": 0.10,                     # r5 §4.1 Model Armor (DLP included)
    "build_min": 0.006, "registry_gb": 0.10,  # r5 §7 Cloud Build e2-standard-2, Artifact Registry
    # DR option B
    "dr_xfer_gb": 0.10, "dr_db_store_gb": 0.112,   # r2 §6.2 SG->Jakarta; Jakarta backup price THIẾU GIÁ -> SG price as proxy
    "dual_region_gb": 0.022 * 2, "repl_gb": 0.08,  # r2 §6.2 dual-region Standard per region x2, replication
 },
 "aws": {
    "cluster_h": 0.10,                        # r1 §1 EKS
    "pod_vcpu_h": 0.05056, "pod_gb_h": 0.00553,    # r1 §2.3 Fargate x86
    "image": 0.04,                            # r3 §2.5 Stable Image Core (us-west-2); Titan v2 status unclear
    "embed_per_1m": 0.10,                     # r3 §2.6 Cohere Embed Multilingual v3 In-Region SG
    "alb_h": 0.0252, "lcu_h": 0.008,          # r1 §5.1
    "waf_acl": 5, "waf_rule": 1, "waf_req_1m": 0.60,   # r1 §5.2
    "nat_h": 0.059, "nat_gb": 0.059, "ip_h": 0.005, "nat_count": 2,   # r1 §5.3, 1 NAT per AZ (no SPOF)
    "pe_h_az": 0.013, "pe_az": 2, "pe_gb": 0.01,   # r1 §5.4 PrivateLink
    "egress_gb": 0.12, "iz_gb": 0.01 * 2,     # r1 §5.5 (charged each direction)
    "db_ha_h": 0.574,                         # r2 §1.1 RDS db.r7g.large Multi-AZ (2 vCPU / 16 GB)
    "db_gp3_ha_gb": 0.276,                    # r2 §1.1 gp3 Multi-AZ; backup included up to provisioned size
    "stg_db_h": 0.102, "stg_gp3_gb": 0.138,   # r2 §1.1 db.t4g.medium Single-AZ (smallest priced in research)
    "obj_gb": 0.025, "obj_w_1k": 0.005, "obj_r_10k": 0.004,   # r2 §4 S3 Standard
    "cache_node_h": 0.0384, "cache_nodes": 2,      # r2 §3.1 ElastiCache Valkey t4g.small Multi-AZ
    "queue_1m": 0.40,                         # r2 §3.2 SQS Standard
    "kms_key": 1.0, "kms_op_10k": 0.03, "secret": 0.40, "secret_op_10k": 0.05,   # r5 §3
    "cw_log_gb": 0.70, "cw_store_gb": 0.03, "s3_std_gb": 0.025, "gda_gb": 0.002,  # r5 §5.1/5.3
    "metric": 0.30, "alarm": 0.10, "xray_1m": 5.0,     # r5 §5.2
    "guard_prompt_1k_units": 0.08, "guard_pii_1k_units": 0.10,   # r5 §4.1 InvokeGuardrailChecks (page price, no APS1 SKU) + PII filter
    "build_min": 0.005, "registry_gb": 0.10,  # r5 §7 CodeBuild general1.small, ECR
    # DR option B (Tokyo)
    "dr_xfer_gb": 0.09, "dr_db_store_gb": 0.095, "crr_xfer_gb": 0.09, "crr_dest_gb": 0.025,  # r2 §6.1/6.2
 },
 "azure": {
    "cluster_h": 0.10,                        # r1 §1 AKS Standard
    "node_h": 0.24,                           # r1 §2.1 D4s_v5 (4 vCPU / 16 GB) on-demand
    "image": 0.011,                           # r3 §3.4 gpt-image-1-mini medium 1024² (US regions)
    "embed_per_1m": 0.024,                    # r3 §3.5 text-embedding-3-small DZ SG
    "agw_waf_h": 0.468, "agw_waf_cu_h": 0.0144,   # r1 §5.1/5.2 Application Gateway WAF v2 (LB + WAF)
    "nat_h": 0.045, "nat_gb": 0.045, "ip_h": 0.005, "nat_count": 2,   # r1 §5.3, zonal NAT x2
    "pe_h": 0.01, "pe_gb": 0.01 * 2,          # r1 §5.4 in + out
    "egress_gb": 0.12, "iz_gb": 0.01 * 2,     # r1 §5.5 Retail API inter-AZ in + out
    "db_ha_h": 0.15 * 2 * 2,                  # r2 §1.1 Memory Optimized Edsv5 0.15/vCore-h, 2 vCore, x2 HA (E2ds_v5 2/16)
    "db_ssd_gb": 0.138 * 2,                   # r2 §1.1 Premium SSD per node x2; backup included = 100% provisioned
    "stg_db_h": 0.026, "stg_ssd_gb": 0.138,   # r2 §1.1 Burstable B1ms (no HA)
    "obj_gb": 0.025, "obj_w_10k": 0.0625, "obj_r_10k": 0.004,   # r2 §4 Blob Hot ZRS
    "cache_h": 0.02,                          # r2 §3.1 Azure Managed Redis B0 (HA 2-node price NOT confirmed)
    "queue_10k": 0.004,                       # r2 §3.2 Storage Queues
    "kv_op_10k": 0.03,                        # r5 §3 Key Vault Standard
    "basic_log_gb": 0.65, "log_scan_gb": 0.0065, "analytics_gb": 2.99,   # r5 §5.1
    "hot_gb": 0.02, "archive_gb": 0.002,      # r5 §5.3
    "metric_10m": 0.11, "log_alert": 1.50,    # r5 §5.2
    "cs_commit": 338.0, "cs_commit_records": 1e6, "cs_over_1k": 0.338,   # r5 §4.1 Content Safety SEA commitment
    "pii_tiers": [(0.5e6, 1.0), (2.0e6, 0.75), (7.5e6, 0.30), (math.inf, 0.25)],   # r5 §4.2 Azure Language per 1k records
    "pipeline_job": 40.0, "acr_basic_day": 0.1666,   # r5 §7
    # DR option B
    "geo_backup_gb": 0.095, "gzrs_gb": 0.049, "geo_xfer_gb": 0.09,   # r2 §1.1/§6.2
 },
}


# ============================================================ HELPERS
def llm_tokens():
    out = {}
    for t, (calls, i, o, cs) in A["tokens"].items():
        n = A["turns_per_day"][t] * DAYS * calls
        out[t] = (n * i, n * o, cs)
    return out


def llm_text_cost():
    p = P["llm"]
    total = 0.0
    for t, (I, O, cs) in llm_tokens().items():
        total += (I * (1 - cs) * p["in"] + I * cs * p["cache"] + O * p["out"]) / 1e6
    return total


def images_month():
    return A["turns_per_day"][5] * DAYS * A["image_share_t5"]


def eval_cost():
    """Eval gate: candidate Haiku + Opus judge every run; stored Opus reference refreshed monthly (no cache)."""
    p = P["llm"]
    jin, jout = A["eval_judge_tok"]
    per_run = ref = 0.0
    for t, (calls, i, o, _) in A["tokens"].items():
        tasks_turns = A["eval_tasks_per_tier"]  # 1 turn per golden task
        ti, to = calls * i, calls * o
        haiku = tasks_turns * (ti * p["in"] + to * p["out"]) / 1e6
        opus = tasks_turns * (ti * p["opus_in"] + to * p["opus_out"]) / 1e6
        # judge scores both candidate and reference
        judge = tasks_turns * 2 * (jin * p["opus_in"] + jout * p["opus_out"]) / 1e6
        per_run += haiku + judge
        ref += opus
    return per_run * A["eval_runs_month"] + ref * A["eval_ref_runs_month"]


def scanned_tokens():
    tin = tout = 0
    for t, (si, so) in A["scan_per_turn"].items():
        n = A["turns_per_day"][t] * DAYS
        tin += n * si
        tout += n * so
    return tin, tout


def tiered(units, tiers):
    cost, prev = 0.0, 0.0
    for upto, price in tiers:
        take = max(0.0, min(units, upto) - prev)
        cost += take / 1000 * price
        prev = upto
        if units <= upto:
            break
    return cost


def app_pod_hours():
    n = A["app_pod_types"]
    per_type = 2 * H_OFFICE + 1 * H_OFF + 1 * A["staging_hours"]
    pods_h = n * per_type
    gb_h = (n - 1) * per_type * A["pod_gb"] + per_type * A["pod_gb_litellm"]
    return pods_h * A["pod_vcpu"], gb_h


def sandbox_hours():
    h = A["sandbox_runs_month"] * A["sandbox_min_per_run"] / 60
    return h * A["sandbox_vcpu"], h * A["sandbox_gb"]


def embed_tokens():
    return A["kb_monthly_change_tok"] + A["ws_new_tok_per_user"] * A["users"]


# ============================================================ PER-CLOUD
def gcp():
    p, c = P["gcp"], {}
    vh, gh = app_pod_hours()
    c["compute"] = p["cluster_h"] * H_MONTH + vh * p["pod_vcpu_h"] + gh * p["pod_gb_h"]
    c["llm"] = llm_text_cost() + images_month() * p["image"]
    c["embedding"] = embed_tokens() / 1e6 * p["embed_per_1m"]
    c["gateway"] = 0.0  # nằm trong compute (LiteLLM pods)
    c["load_balancer"] = p["lb_rule_h"] * H_MONTH + A["lb_gb_month"] * 2 * p["lb_gb"]
    c["authn"] = 0.0   # IAP + Workforce Identity Federation: no charge, nằm trong load_balancer
    c["authz"] = 0.0   # nằm trong database (RLS) + gateway
    db = (p["db_vcpu"] * p["db_vcpu_ha_h"] + p["db_ram"] * p["db_gb_ha_h"]) * H_MONTH
    db += A["db_storage_gb"] * p["db_ssd_ha_gb"]
    db += p["stg_db_h"] * H_MONTH + A["staging_db_gb"] * p["stg_ssd_gb"]
    c["database"] = db
    c["vector_db"] = 0.0  # nằm trong database (pgvector)
    gb = A["ws_gb_per_user"] * A["users"]
    c["object_storage"] = gb * p["obj_gb"] + A["obj_writes_month"] / 1e3 * p["obj_w_1k"] + A["obj_reads_month"] / 1e3 * p["obj_r_1k"]
    c["cache_queue"] = p["cache_node_h"] * p["cache_nodes"] * H_MONTH + A["queue_ops_month"] / 1e6 * p["queue_1m"]
    sv, sg = sandbox_hours()
    c["sandbox"] = sv * p["pod_vcpu_h"] + sg * p["pod_gb_h"]
    c["connectors"] = 0.0  # nằm trong compute (worker pods); API fees 0 (r8)
    c["secrets_kms"] = (A["kms_keys"] * p["kms_key"] + A["kms_ops_month"] / 1e4 * p["kms_op_10k"]
                        + A["app_secrets"] * p["secret_ver"] + A["secret_access_month"] / 1e4 * p["secret_op_10k"])
    c["backup_dr"] = A["db_backup_gb"] * p["db_backup_gb"]
    dr_b = (A["dr_db_transfer_gb"] * p["dr_xfer_gb"] + A["db_backup_gb"] * p["dr_db_store_gb"]
            + gb * (p["dual_region_gb"] - p["obj_gb"]) + A["dr_new_obj_gb"] * p["repl_gb"])
    c["monitoring"] = (A["app_log_gb"] * p["log_gb"] + A["audit_gb"] * p["log_gb"]
                       + A["audit_gb"] * 12 * p["archive_gb"] + A["prompt_log_gb"] * p["std_gb"]
                       + A["metric_samples"] / 1e6 * p["prom_1m"] + A["trace_spans"] / 1e6 * p["trace_1m"])
    tin, tout = scanned_tokens()
    c["governance"] = (tin + tout) / 1e6 * p["guard_1m_tok"] + eval_cost()
    c["network"] = (p["waf_policy"] + A["waf_rules"] * p["waf_rule"] + A["http_req_month"] / 1e6 * p["waf_req_1m"]
                    + A["nat_vms_gcp"] * H_MONTH * p["nat_vm_h"] + A["nat_gb_month"] * p["nat_gb"] + H_MONTH * p["ip_h"]
                    + H_MONTH * p["pe_h"] + A["egress_gb_month"] * p["egress_gb"] + A["interzone_gb_month"] * p["iz_gb"])
    c["cicd"] = A["build_min_month"] * p["build_min"] + A["registry_gb"] * p["registry_gb"]
    return c, dr_b


def aws():
    p, c = P["aws"], {}
    vh, gh = app_pod_hours()
    c["compute"] = p["cluster_h"] * H_MONTH + vh * p["pod_vcpu_h"] + gh * p["pod_gb_h"]
    c["llm"] = llm_text_cost() + images_month() * p["image"]
    c["embedding"] = embed_tokens() / 1e6 * p["embed_per_1m"]
    c["gateway"] = 0.0
    c["load_balancer"] = p["alb_h"] * H_MONTH + A["lb_avg_lcu"] * p["lcu_h"] * H_MONTH
    c["authn"] = 0.0   # ALB authenticate-oidc, nằm trong load_balancer
    c["authz"] = 0.0
    c["database"] = (p["db_ha_h"] * H_MONTH + A["db_storage_gb"] * p["db_gp3_ha_gb"]
                     + p["stg_db_h"] * H_MONTH + A["staging_db_gb"] * p["stg_gp3_gb"])
    c["vector_db"] = 0.0
    gb = A["ws_gb_per_user"] * A["users"]
    c["object_storage"] = gb * p["obj_gb"] + A["obj_writes_month"] / 1e3 * p["obj_w_1k"] + A["obj_reads_month"] / 1e4 * p["obj_r_10k"]
    c["cache_queue"] = p["cache_node_h"] * p["cache_nodes"] * H_MONTH + A["queue_ops_month"] / 1e6 * p["queue_1m"]
    sv, sg = sandbox_hours()
    c["sandbox"] = sv * p["pod_vcpu_h"] + sg * p["pod_gb_h"]
    c["connectors"] = 0.0
    c["secrets_kms"] = (A["kms_keys"] * p["kms_key"] + A["kms_ops_month"] / 1e4 * p["kms_op_10k"]
                        + A["app_secrets"] * p["secret"] + A["secret_access_month"] / 1e4 * p["secret_op_10k"])
    c["backup_dr"] = 0.0  # RDS automated backup nằm trong database (≤ provisioned storage); S3 multi-AZ by default
    dr_b = (A["dr_db_transfer_gb"] * p["dr_xfer_gb"] + A["db_storage_gb"] * p["dr_db_store_gb"]
            + gb * p["crr_dest_gb"] + A["dr_new_obj_gb"] * p["crr_xfer_gb"])
    c["monitoring"] = (A["app_log_gb"] * (p["cw_log_gb"] + p["cw_store_gb"])
                       + A["audit_gb"] * p["s3_std_gb"] + A["audit_gb"] * 11 * p["gda_gb"]
                       + A["prompt_log_gb"] * p["s3_std_gb"]
                       + A["custom_metrics_aws"] * p["metric"] + A["alarms"] * p["alarm"]
                       + A["trace_spans"] / 5 / 1e6 * p["xray_1m"])   # X-Ray billed per trace (~1 trace per LLM call)
    tin, tout = scanned_tokens()
    cpt = A["chars_per_token"]
    units_in, units_all = tin * cpt / 1000, (tin + tout) * cpt / 1000
    c["governance"] = (units_in / 1000 * p["guard_prompt_1k_units"] + units_all / 1000 * p["guard_pii_1k_units"]
                       + eval_cost())
    c["network"] = (p["waf_acl"] + A["waf_rules"] * p["waf_rule"] + A["http_req_month"] / 1e6 * p["waf_req_1m"]
                    + p["nat_count"] * (p["nat_h"] + p["ip_h"]) * H_MONTH + A["nat_gb_month"] * p["nat_gb"]
                    + p["pe_az"] * p["pe_h_az"] * H_MONTH + A["llm_gb_month"] * p["pe_gb"]
                    + A["egress_gb_month"] * p["egress_gb"] + A["interzone_gb_month"] * p["iz_gb"])
    c["cicd"] = A["build_min_month"] * p["build_min"] + A["registry_gb"] * p["registry_gb"]
    return c, dr_b


def azure():
    p, c = P["azure"], {}
    # app pool: 2 nodes (2 zones) office hours, 1 node off-hours, +1 node during staging hours
    app_node_h = 2 * H_OFFICE + 1 * H_OFF + 1 * A["staging_hours"]
    c["compute"] = p["cluster_h"] * H_MONTH + app_node_h * p["node_h"]
    c["llm"] = llm_text_cost() + images_month() * p["image"]
    c["embedding"] = embed_tokens() / 1e6 * p["embed_per_1m"]
    c["gateway"] = 0.0
    c["load_balancer"] = p["agw_waf_h"] * H_MONTH + A["lb_avg_lcu"] * p["agw_waf_cu_h"] * H_MONTH  # includes WAF
    c["authn"] = 0.0   # Entra workforce app registration + OIDC proxy pod, nằm trong compute
    c["authz"] = 0.0
    c["database"] = (p["db_ha_h"] * H_MONTH + A["db_storage_gb"] * p["db_ssd_gb"]
                     + p["stg_db_h"] * H_MONTH + A["staging_db_gb"] * p["stg_ssd_gb"])
    c["vector_db"] = 0.0
    gb = A["ws_gb_per_user"] * A["users"]
    c["object_storage"] = gb * p["obj_gb"] + A["obj_writes_month"] / 1e4 * p["obj_w_10k"] + A["obj_reads_month"] / 1e4 * p["obj_r_10k"]
    c["cache_queue"] = p["cache_h"] * H_MONTH + A["queue_ops_month"] / 1e4 * p["queue_10k"]
    sv, _ = sandbox_hours()
    node_h = sv / A["azure_node_vcpu"] / A["azure_pack_eff"]   # Kata pool on D4s_v5 (nested virt)
    c["sandbox"] = node_h * p["node_h"]
    c["connectors"] = 0.0
    c["secrets_kms"] = (A["kms_ops_month"] + A["secret_access_month"]) / 1e4 * p["kv_op_10k"]
    c["backup_dr"] = 0.0  # backup = 100% provisioned storage included
    dr_b = (max(0, 2 * A["db_backup_gb"] * 1.5 - A["db_storage_gb"]) * p["geo_backup_gb"]
            + gb * (p["gzrs_gb"] - p["obj_gb"]) + A["dr_new_obj_gb"] * p["geo_xfer_gb"])
    c["monitoring"] = (A["app_log_gb"] * p["basic_log_gb"] + A["azure_basic_log_scan_gb"] * p["log_scan_gb"]
                       + A["azure_appinsights_gb"] * p["analytics_gb"]
                       + A["audit_gb"] * p["hot_gb"] + A["audit_gb"] * 11 * p["archive_gb"]
                       + A["prompt_log_gb"] * p["hot_gb"]
                       + A["metric_samples"] / 1e7 * p["metric_10m"] + A["azure_log_alerts"] * p["log_alert"])
    tin, tout = scanned_tokens()
    cpt = A["chars_per_token"]
    rec_in, rec_all = tin * cpt / 1000, (tin + tout) * cpt / 1000
    cs = p["cs_commit"] + max(0, rec_in - p["cs_commit_records"]) / 1000 * p["cs_over_1k"]
    c["governance"] = cs + tiered(rec_all, p["pii_tiers"]) + eval_cost()
    c["network"] = (p["nat_count"] * (p["nat_h"] + p["ip_h"]) * H_MONTH + A["nat_gb_month"] * p["nat_gb"]
                    + H_MONTH * p["pe_h"] + A["llm_gb_month"] * p["pe_gb"]
                    + A["egress_gb_month"] * p["egress_gb"] + A["interzone_gb_month"] * p["iz_gb"])  # WAF nằm trong LB
    c["cicd"] = p["pipeline_job"] + p["acr_basic_day"] * H_MONTH / 24
    return c, dr_b


COMPONENTS = ["compute", "llm", "embedding", "gateway", "load_balancer", "authn", "authz", "database",
              "vector_db", "object_storage", "cache_queue", "sandbox", "connectors", "secrets_kms",
              "backup_dr", "monitoring", "governance", "network", "cicd", "ops_labor", "licenses"]


def run():
    res = {}
    for name, fn in (("GCP", gcp), ("AWS", aws), ("Azure", azure)):
        c, dr_b = fn()
        c["ops_labor"] = A["ops_labor_usd"]
        c["licenses"] = 0.0   # D19: no support plan
        res[name] = {"lines": c, "total": sum(c.values()), "dr_b_delta": dr_b}
    return res


if __name__ == "__main__":
    r = run()
    if "--json" in sys.argv:
        print(json.dumps(r, indent=2))
        sys.exit()
    print(f"{'component':16}" + "".join(f"{k:>12}" for k in r))
    for comp in COMPONENTS:
        print(f"{comp:16}" + "".join(f"{r[k]['lines'][comp]:12.2f}" for k in r))
    print(f"{'TOTAL (DR A)':16}" + "".join(f"{r[k]['total']:12.2f}" for k in r))
    print(f"{'USD/DAU':16}" + "".join(f"{r[k]['total'] / A['users']:12.2f}" for k in r))
    print(f"{'DR B delta':16}" + "".join(f"{r[k]['dr_b_delta']:12.2f}" for k in r))
    print(f"{'TOTAL (DR B)':16}" + "".join(f"{r[k]['total'] + r[k]['dr_b_delta']:12.2f}" for k in r))
    ti, to = scanned_tokens()
    print("LLM text", round(llm_text_cost(), 2), "images/mo", round(images_month()), "eval", round(eval_cost(), 2),
          "scanned tok (B)", round((ti + to) / 1e9, 2), "sandbox runs", round(A["sandbox_runs_month"]),
          "embed tok (M)", embed_tokens() / 1e6)
