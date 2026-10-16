# R1 + R9 (phần network): đơn giá compute, sandbox và mạng — GCP / AWS / Azure

> Ngày truy cập mọi nguồn: **2026-10-16**. Region: GCP `asia-southeast1`, AWS `ap-southeast-1`, Azure `southeastasia` (Southeast Asia, Singapore). Tiền tệ: USD.
>
> Quy ước:
> - Chỉ ghi **giá niêm yết pay-as-you-go** lấy từ trang giá chính thức hoặc API/feed giá chính thức của nhà cung cấp. **Không** tính free tier, trial, credit, "always free", giá đàm phán. Khi nguồn có bậc miễn phí, bảng ghi giá của bậc **trả tiền** và chú thích bậc miễn phí bị loại.
> - Reserved / Savings Plan / CUD ghi **riêng** (1 năm, 3 năm). Spot/preemptible ghi riêng.
> - "(suy ra)" = phép tính của người tổng hợp từ số gốc (ví dụ đổi giá trọn kỳ reservation ra giá/giờ). Không phải số do nguồn công bố.
> - Không tìm được → ghi **KHÔNG TÌM THẤY** kèm URL đã kiểm tra.
>
> Nguồn máy đọc được (official), dùng cho hầu hết số liệu:
> - **AWS Price List API** (bulk offer files): `https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/<OfferCode>/current/ap-southeast-1/index.json` (EC2 dùng `index.csv`; publicationDate EC2 = 2026-10-15). Savings Plans: `https://pricing.us-east-1.amazonaws.com/savingsPlan/v1.0/aws/AWSComputeSavingsPlan/20261013035015/ap-southeast-1/index.json`. Spot: feed của trang https://aws.amazon.com/ec2/spot/pricing/ (`https://website.spot.ec2.aws.a2z.com/spot.js`).
> - **Azure Retail Prices API**: `https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&$filter=armRegionName eq 'southeastasia' and serviceName eq '<Service>'` (meter `Consumption` = PAYG; `Reservation` = giá trọn kỳ).
> - **GCP**: bảng giá nhúng trong trang giá chính thức, đọc theo lựa chọn region "Singapore (asia-southeast1)".

---

## 1. Phí control plane Kubernetes

| Hạng mục | GCP (GKE) | AWS (EKS) | Azure (AKS) |
|---|---|---|---|
| Phí cluster chuẩn | **$0.10 / cluster-giờ** — áp dụng như nhau cho zonal, regional, Autopilot ("flat cluster management fee… irrespective of the mode of operation, cluster size, or topology") | **$0.10 / cluster-giờ** (`APS1-AmazonEKS-Hours:perCluster`) | Free tier: **$0** phí quản lý (không SLA) · **Standard: $0.10 / cluster-giờ** (`Standard Uptime SLA`) · **Premium (Standard + LTS): $0.60 / cluster-giờ** (`Standard Long Term Support`; trang giá: $438/cluster/tháng) |
| Chế độ "managed hơn" | Autopilot: cùng $0.10/cluster-giờ; compute tính theo Pod (mục 2) | **EKS Auto Mode**: phí quản lý cộng thêm theo từng instance, ví dụ `m7i.xlarge` **$0.03024/giờ**, `m7i.2xlarge` **$0.06048/giờ**, `c7i.xlarge` **$0.0247/giờ**, `m8i.xlarge` **$0.03175/giờ** (ngoài giá EC2) | **AKS Automatic**: Hosted Control Plane **$0.16 / cluster-giờ** (trang giá: $116.80/tháng) + phụ phí theo vCPU: General Purpose **$0.010193 / vCPU-giờ**, Compute Optimized **$0.015855**, Memory Optimized **$0.016155** (Southeast Asia, Retail API) |
| Extended / long-term support | Extended channel sau hết standard support: **+$0.50 / cluster-giờ** (tổng $0.60) | Extended support: **$0.60 / cluster-giờ** = $0.10 + **$0.50** (`APS1-AmazonEKS-Hours:extendedSupport`; trang giá: "Standard Kubernetes version support + $0.50 per cluster per hour") | Premium tier (bắt buộc kèm LTS) **$0.60 / cluster-giờ** |
| Control plane cấp cao hơn | — | **Provisioned Control Plane**: XL **$1.65/giờ**, 2XL $3.40, 4XL $6.90, 8XL $13.90 | — |
| Meter mới cần lưu ý | — | — | `FreeTierInfrastructureCost Uptime SLA` **$0.05/giờ**, hiệu lực từ **2026-10-01** (Retail API). Trang giá và tài liệu tier **không giải thích** meter này → xem gap G1 |
| **SLA control plane** | Autopilot & regional Standard: **99.95%** · zonal Standard: **99.5%** · Autopilot Pods đa zone: **99.9%** | Standard control plane: **99.95%** (5 phút/khoảng đo) · Provisioned: **99.99%** | Free: **không có SLA tài chính** ("best-effort") · Standard/Premium: **99.95%** khi có availability zones, **99.9%** khi không AZ · Automatic: Standard tier + pod readiness SLA |
| Nguồn | https://cloud.google.com/kubernetes-engine/pricing | Price List API `AmazonEKS`; https://aws.amazon.com/eks/pricing/ ; SLA: https://aws.amazon.com/eks/sla/ (cập nhật 2026-03-20) | Retail API `serviceName eq 'Azure Kubernetes Service'`; https://azure.microsoft.com/en-us/pricing/details/kubernetes-service/ ; https://learn.microsoft.com/en-us/azure/aks/free-standard-pricing-tiers (cập nhật 2026-09-01) |

**Ghi chú SLA:** Đề yêu cầu 99,5% trong giờ hành chính. AKS Free tier không có SLA tài chính và tài liệu chỉ khuyến nghị cho dev/test (<10 node) → **prod phải dùng Standard ($0.10/giờ)**. GKE free tier credit ($74.40/tháng/billing account) **bị loại** theo quy tắc; credit này cũng không áp dụng cho regional cluster.

Phí control plane theo tháng (suy ra, 730 giờ, không tính credit): GKE/EKS/AKS Standard ≈ **$73/cluster**; staging ~40 giờ/tháng (D16) nếu xóa cluster khi tắt ≈ $4 — nhưng thường giữ cluster 24/7 và chỉ scale node về 0.

---

## 2. Compute cho worker

### 2.1 Instance phổ biến — on-demand (Linux, $/giờ)

| Cấu hình | GCP (asia-southeast1) | AWS (ap-southeast-1) | Azure (Southeast Asia) |
|---|---|---|---|
| **4 vCPU / 16 GB** | `n2-standard-4` **$0.239612** · `n4-standard-4` **$0.223793** · `n2d-standard-4` **$0.208468** · `e2-standard-4` **$0.165332** | `m7i.xlarge` **$0.2520** · `m6i.xlarge` **$0.2400** · `m8i.xlarge` **$0.2646** · `m7i-flex.xlarge` **$0.2394** · `m7g.xlarge` (Arm) **$0.2040** | `Standard_D4s_v5` **$0.24** · `D4s_v6` **$0.252** · `D4as_v5` **$0.216** · `D4s_v3` **$0.25** · `D4ds_v5` **$0.282** |
| **8 vCPU / 32 GB** | `n2-standard-8` **$0.479224** · `n4-standard-8` **$0.447586** · `e2-standard-8` **$0.330665** | `m7i.2xlarge` **$0.5040** · `m6i.2xlarge` **$0.4800** · `m8i.2xlarge` **$0.5292** | `D8s_v5` **$0.48** · `D8s_v6` **$0.504** |
| **Compute-optimized 4 vCPU / 8 GB** | `c4-highcpu-4` **$0.209857** · `c3-highcpu-4` **$0.209857** · `n4-highcpu-4` **$0.188855** | `c7i.xlarge` **$0.2058** · `c6i.xlarge` **$0.1960** · `c8i.xlarge` **$0.2161** | `F4s_v2` **$0.196** · `F4as_v6` **$0.343** |
| Nguồn | https://cloud.google.com/products/compute/pricing/general-purpose (c3/c4/n4 cũng nằm ở trang này) | Price List API `AmazonEC2` (CSV, 2026-10-15) + https://aws.amazon.com/ec2/pricing/on-demand/ | Retail API `serviceName eq 'Virtual Machines'` + https://azure.microsoft.com/en-us/pricing/details/virtual-machines/linux/ |

Đơn giá per-vCPU / per-GB (để ước lượng custom size):

| | GCP | AWS | Azure |
|---|---|---|---|
| Theo vCPU-giờ / GB-giờ (VM) | N2 custom: **$0.04040368 / vCPU-giờ**, **$0.004585663 / GiB-giờ** (custom có phụ phí so với predefined; dòng predefined không tách được — gap G9) | EC2 không bán theo vCPU/GB; dùng Fargate (mục 2.3) | Không bán theo vCPU/GB; dùng ACI/ACA (mục 2.3) |

### 2.2 Cam kết dài hạn ($/giờ tương đương)

| Instance | On-demand | 1 năm | 3 năm | Loại cam kết |
|---|---|---|---|---|
| GCP `n2-standard-4` | 0.239612 | Flex CUD **0.172521** · Resource CUD **0.15094** | Flex CUD **0.129390** · Resource CUD **0.107824** | Compute Flexible CUD (theo $ chi tiêu, đổi được series) / Resource-based CUD (cam kết vCPU+RAM) |
| GCP `n4-standard-4` | 0.223793 | Flex 0.161131 · Resource 0.140987 | Flex 0.120848 · Resource 0.100709 | như trên |
| GCP `e2-standard-4` | 0.165332 | Flex 0.119039 · Resource 0.104159 | Flex 0.089279 · Resource 0.074400 | như trên |
| GCP `n2-standard-8` | 0.479224 | Flex 0.345041 · Resource 0.30188 | Flex 0.258781 · Resource 0.215648 | như trên |
| GCP `c4-highcpu-4` | 0.209857 | Flex 0.151097 · Resource 0.132213 | Flex 0.113323 · Resource 0.094437 | như trên |
| AWS `m7i.xlarge` | 0.2520 | Standard RI No Upfront **0.1667** · Convertible RI **0.18765** · EC2 Instance SP **0.1667** · Compute SP **0.18765** | Std RI **0.11431** · Conv RI **0.1278** · EC2 Instance SP 0.11431 · Compute SP 0.1278 | RI / Savings Plans, No Upfront |
| AWS `m7i.2xlarge` | 0.5040 | Std RI 0.3334 · Conv RI / Compute SP 0.37529 | Std RI 0.22861 · Conv RI / Compute SP 0.2556 | như trên |
| AWS `m6i.xlarge` | 0.2400 | Std RI 0.15876 · Conv RI 0.17871 | Std RI 0.10886 · Conv RI 0.12172 | RI No Upfront |
| AWS `c7i.xlarge` | 0.2058 | Std RI / EC2 SP 0.1366 · Conv RI / Compute SP 0.1562 | Std RI 0.09335 · Conv RI / Compute SP 0.1066 | như trên |
| Azure `D4s_v5` | 0.24 | Reservation **$1,297 trọn kỳ** ⇒ ≈ **0.1481/giờ** (suy ra) | **$2,491 trọn kỳ** ⇒ ≈ **0.0948/giờ** (suy ra) | Reserved VM Instances |
| Azure `D8s_v5` | 0.48 | $2,594 ⇒ ≈ 0.2961/giờ (suy ra) | $4,983 ⇒ ≈ 0.1896/giờ (suy ra) | như trên |
| Azure `D4s_v6` | 0.252 | $1,369 ⇒ ≈ 0.1563/giờ (suy ra) | $2,583 ⇒ ≈ 0.0983/giờ (suy ra) | như trên |
| Azure `D4as_v5` | 0.216 | $1,167 ⇒ ≈ 0.1332/giờ (suy ra) | $2,242 ⇒ ≈ 0.0853/giờ (suy ra) | như trên |
| Azure `F4as_v6` | 0.343 | $1,864 ⇒ ≈ 0.2128/giờ (suy ra) | $3,518 ⇒ ≈ 0.1339/giờ (suy ra) | như trên |
| Azure `F4s_v2`, `D4s_v3` | 0.196 / 0.25 | **KHÔNG TÌM THẤY** meter reservation trong Retail API | — | — |

**Lưu ý D3:** app chạy đầy đủ ~220 giờ/tháng. Cam kết 1–3 năm tính tiền 730 giờ/tháng dù tắt máy, nên chỉ có lợi cho phần chạy 24/7 (baseline ngoài giờ). Tỉ lệ hòa vốn (suy ra): ví dụ AWS `m7i.xlarge` Std RI 3 năm = 0.11431/0.252 ≈ 45% on-demand ⇒ chỉ lợi khi máy chạy > ~330 giờ/tháng.

### 2.3 Pod / container serverless (trả theo tài nguyên)

| Dịch vụ | GCP — GKE Autopilot (Pod-based) | AWS — Fargate (EKS/ECS) | Azure — ACI / Container Apps |
|---|---|---|---|
| vCPU-giờ | Container-optimized (mặc định): **$0.0549** · Balanced: **$0.0796** · Scale-Out x86: **$0.0692** · Scale-Out Arm: $0.0439 | x86: **$0.05056** · Arm: $0.04045 | ACI: **$0.0506** · ACA Dedicated: **$0.080859** |
| GiB-giờ | Container-optimized: **$0.0060729** · Balanced: $0.0092047 → **$0.008803** (xem ghi chú) · Scale-Out x86: **$0.0076518** | x86: **$0.00553** · Arm: $0.00442 | ACI: **$0.00553** · ACA Dedicated: **$0.006638** |
| Ephemeral storage | $0.0001713 / GiB-giờ | $0.000133 / GB-giờ (20 GB đầu đã gồm trong giá — theo trang Fargate) | — |
| Cam kết 1 năm | Container-optimized: Flex CUD $0.039528 vCPU / $0.004372 GiB · Kubernetes Engine CUD $0.04392 / $0.004858 | Compute Savings Plan No Upfront: **$0.040448** vCPU-giờ / **$0.004424** GB-giờ | ACA: savings plan ≈ 15% (trang giá) |
| Cam kết 3 năm | Flex CUD $0.029646 / $0.003279 · Kubernetes Engine CUD $0.030195 / $0.003340 | Compute SP: **$0.027808** / **$0.0030415** | ACA: ≈ 17% |
| Spot | Container-optimized Spot: **$0.0165** vCPU / $0.0018219 GiB · Scale-Out x86 Spot $0.0208 / $0.0022956 | Fargate Spot **chỉ cho ECS**; "Amazon EKS doesn't support Fargate Spot" | ACI: KHÔNG TÌM THẤY spot |
| Phụ phí khác | Phí cluster $0.10/giờ | Phí cluster EKS $0.10/giờ | ACA Dedicated: Plan Management $0.10/giờ; meter "Environment Management Hour" $0.14/giờ (từ 2026-09-01, áp cho Dedicated plan / private endpoint / planned maintenance) — xem gap G4 |
| Nguồn | https://cloud.google.com/kubernetes-engine/pricing | Price List API `AmazonEKS`/`AmazonECS`; https://aws.amazon.com/fargate/pricing/ ; https://docs.aws.amazon.com/eks/latest/userguide/fargate.html | Retail API `Container Instances`, `Azure Container Apps`; https://azure.microsoft.com/en-us/pricing/details/container-apps/ |

Ghi chú: Bảng GKE Balanced có 2 bộ số trong dữ liệu trang; bộ khớp với giá us-central1 ($0.0645 × hệ số Singapore 1,2337 = $0.0796) là **$0.0796 vCPU / $0.008803 GiB** — dùng bộ này. Autopilot workload chọn phần cứng cụ thể (machine series, GPU) tính theo **node-based** = giá Compute Engine + Autopilot premium.

### 2.4 Spot / preemptible VM (giá tại thời điểm truy cập, biến động)

| Cấu hình | GCP Spot VM | AWS EC2 Spot (Linux) | Azure Spot VM |
|---|---|---|---|
| 4 vCPU / 16 GB | `n2-standard-4` **$0.096096** · `e2-standard-4` $0.042528 · `n4-standard-4` $0.1342 · `n2d-standard-4` $0.046704 | `m7i.xlarge` **$0.0979** · `m6i.xlarge` $0.0947 | `D4s_v5` Spot **$0.044496** · `D4s_v6` $0.04657 · `D4s_v3` $0.0462 |
| 8 vCPU / 32 GB | `n2-standard-8` $0.192192 · `e2-standard-8` $0.085056 | `m7i.2xlarge` $0.2387 · `m6i.2xlarge` $0.2216 | `D8s_v5` Spot $0.088992 |
| 4 vCPU / 8 GB | `c4-highcpu-4` $0.10124 · `n4-highcpu-4` $0.11324 | `c7i.xlarge` $0.0697 · `c6i.xlarge` $0.0892 | `F4s_v2` Spot $0.036221 |
| Nguồn | https://cloud.google.com/spot-vms/pricing | https://aws.amazon.com/ec2/spot/pricing/ (feed spot.js) | Retail API (meter "… Spot") |

Spot có thể bị thu hồi bất kỳ lúc nào → chỉ hợp cho sandbox job ngắn có retry, **không** dùng cho app tier giữ SLA.

---

## 3. Serverless cho app tier

| Hạng mục | GCP — Cloud Run (asia-southeast1) | AWS — Lambda / App Runner (ap-southeast-1) | Azure — Container Apps Consumption (Southeast Asia) |
|---|---|---|---|
| vCPU | Instance-based: **$0.0000216 / vCPU-s** · Request-based: active **$0.0000336 / vCPU-s**, idle (min instance) **$0.0000035 / vCPU-s** · Jobs: $0.0000216 · Worker pools: $0.000013493 | Lambda: tính theo GB-s (CPU tỉ lệ theo RAM) · App Runner: **$0.0809 / vCPU-giờ** | Active **$0.000034 / vCPU-s** · Idle **$0.000004 / vCPU-s** |
| Bộ nhớ | Instance-based: **$0.0000024 / GiB-s** · Request-based: active/idle **$0.0000035 / GiB-s** | Lambda x86: **$0.0000166667 / GB-s** (tier 1, 0–6 tỷ GB-s), $0.000015 (tier 2), $0.0000133334 (tier 3) · Arm: $0.0000133334 · App Runner: **$0.00885 / GB-giờ** | Active và idle **$0.000004 / GiB-s** |
| Request | Request-based: **$0.40 / 1 triệu** | Lambda: **$0.20 / 1 triệu** · Provisioned Concurrency: $0.0000051991 / GB-s (+ compute $0.0000121313 / GB-s) | **$0.40 / 1 triệu** |
| Cam kết | Cloud Run CUD 1y/3y: CPU instance-based $0.000017928; request-based active $0.000027888 · Compute Flexible CUD 1y $0.000015552 / 3y $0.000011664 (instance-based) | Compute SP 1y/3y cho Lambda: $0.000015 / GB-s | Savings plan 1y ≈ 15%, 3y ≈ 17% (ví dụ request $0.34 / $0.332 per million) |
| Bậc miễn phí bị loại | Cloud Run free tier | Lambda free tier | ACA: 180.000 vCPU-s, 360.000 GiB-s, 2 triệu request / subscription / tháng |
| Nguồn | https://cloud.google.com/run/pricing | Price List API `AWSLambda`, `AWSAppRunner`; https://aws.amazon.com/lambda/pricing/ ; https://aws.amazon.com/apprunner/pricing/ | Retail API `Azure Container Apps`; https://azure.microsoft.com/en-us/pricing/details/container-apps/ |

**Cảnh báo AWS App Runner:** AWS công bố App Runner **không nhận khách hàng mới từ 30/04/2026**, không phát triển tính năng mới (https://docs.aws.amazon.com/apprunner/latest/relnotes/relnotes.html). Không nên chọn cho dự án mới; app tier trên AWS nên so Fargate/EKS hoặc Lambda.

Quy đổi (suy ra) để so với Autopilot/Fargate: Cloud Run instance-based 1 vCPU + 2 GiB chạy 1 giờ = 3600 × (0.0000216 + 2 × 0.0000024) = **$0.0950/giờ**; ACA active cùng cấu hình = 3600 × (0.000034 + 2 × 0.000004) = **$0.1512/giờ**.

---

## 4. Sandbox cách ly (gVisor / Firecracker / Kata) và dịch vụ sandbox managed

### 4.1 Công nghệ cách ly trên Kubernetes

| | GCP — GKE Sandbox (gVisor) | AWS — EKS | Azure — AKS Pod Sandboxing (Kata) |
|---|---|---|---|
| Hỗ trợ | "Available in any Standard node pools and Autopilot nodes. Enabled by default in Autopilot clusters." Pod dùng `runtimeClassName: gvisor` | (a) **Fargate**: mỗi Pod một VM riêng, "don't share the underlying kernel, CPU resources, memory resources, or elastic network interface". (b) **Kata/Firecracker tự cài** trên node EC2: cần KVM ⇒ trước 02/2026 chỉ chạy được trên **bare metal**; từ 02/2026 EC2 hỗ trợ **nested virtualization** trên M7i, M7i-flex, M8i, C7i, C8i, R7i, R8i… (hypervisor L1: KVM, Hyper-V; không thu thêm phí) | GA; Kata + Cloud Hypervisor trên Hyper-V; `runtimeClassName: kata-vm-isolation` |
| Yêu cầu node | Container-Optimized OS; hỗ trợ đa số CPU, Arm, accelerator | Bare metal (vd `m5.metal` $5.76/giờ, `c5.metal` $4.704, `m7i.metal-24xl` $6.048, `c7i.metal-24xl` $4.9392 — 96 vCPU) **hoặc** VM có nested virtualization (vd `m7i.xlarge` $0.252). AWS khuyến nghị bare metal cho workload nhạy hiệu năng | **Azure Linux** OS SKU (không Ubuntu/Windows), **VM Gen2 hỗ trợ nested virtualization** (tài liệu lấy ví dụ `Standard_D4s_v3` $0.25/giờ; Dsv5 ghi "Nested Virtualization: Supported" ⇒ `D4s_v5` $0.24/giờ), không Arm64, không FIPS/Trusted Launch, K8s ≥ 1.27 |
| Phí thêm | Tài liệu không nêu phí riêng cho gVisor (trả theo node/pod thường) | Nested virtualization: "There is no additional cost". Fargate: giá Fargate (mục 2.3) | Không có meter riêng; trả theo VM node |
| Hệ quả chi phí | Có overhead bộ nhớ userspace kernel ("low base memory"), khởi động < 200 ms. Autopilot: sandbox có thể chạy trực tiếp trên Pod-based billing → không cần node pool riêng | Fargate: mỗi sandbox là 1 Pod ⇒ trả đúng 1 vCPU/2 GB × thời gian chạy; cold start Pod Fargate dài hơn container thường (chưa có số chính thức – gap G8). Fargate Pod chỉ chạy private subnet, không DaemonSet, không privileged | Mỗi Kata pod là 1 pod VM: RAM cố định theo memory limit (mặc định 512Mi), CPU limit làm tròn lên vCPU nguyên ⇒ cần node pool riêng, khó scale về 0 nhanh |
| Nguồn | https://docs.cloud.google.com/kubernetes-engine/docs/concepts/sandbox-pods (cập nhật 2026-10-13) | https://docs.aws.amazon.com/eks/latest/userguide/fargate.html ; https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/amazon-ec2-nested-virtualization.html ; https://aws.amazon.com/about-aws/whats-new/2026/02/amazon-ec2-nested-virtualization-on-virtual/ ; https://aws.amazon.com/blogs/containers/enhancing-kubernetes-workload-isolation-and-security-using-kata-containers/ | https://learn.microsoft.com/en-us/azure/aks/use-pod-sandboxing (cập nhật 2026-10-02) ; https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/general-purpose/dsv5-series |

Bare metal EC2 Reserved (No Upfront, $/giờ): `m5.metal` 1y Std 3.629 / 3y 2.488; `c5.metal` 2.964 / 2.032; `m7i.metal-24xl` 4.00075 / 2.74337; `c7i.metal-24xl` 3.27838 / 2.24042.

### 4.2 Dịch vụ sandbox managed cho agent / code interpreter

| | GCP — Agent Engine (Gemini Enterprise Agent Platform) Code Execution / Sandbox | AWS — Bedrock AgentCore Code Interpreter | Azure — Container Apps Dynamic Sessions |
|---|---|---|---|
| Đơn vị tính | **Agent Compute $0.085 / vCPU-giờ** + **Agent Memory $0.009 / GiB-giờ**, làm tròn theo giây | **$0.0895 / vCPU-giờ** + **$0.00945 / GB-giờ** (`APS1-CodeInterpreter:Consumption-based:*`) | Built-in container (Python, Node.js, Shell): **$0.03 / session-giờ** (meter "Dynamic Sessions", Southeast Asia) · Custom container session: tính theo ACA Dedicated plan, "no premium or additional charges" |
| Cam kết | Gemini Enterprise Flexible Savings Plan 1y: $0.0765 vCPU / $0.0081 GiB · 3y: $0.068 / $0.0072 | KHÔNG TÌM THẤY savings plan riêng | Savings plan 1y $0.026, 3y $0.025 / session-giờ |
| Bậc miễn phí bị loại | 50 vCPU-giờ và 100 GiB-giờ / tháng / account | — | — |
| Region | Trang giá **không tách theo region** (một bảng chung) — gap G7 | Singapore (giá region) | Southeast Asia (Retail API) |
| Quy đổi 1 phiên sandbox 1 vCPU / 2 GB × 10 phút (suy ra) | (0.085 + 2×0.009) / 6 = **$0.0172** | (0.0895 + 2×0.00945) / 6 = **$0.0181** | 0.03 / 6 = **$0.0050** (cấu hình tài nguyên của built-in session do nền tảng quy định — cần đối chiếu D13) |
| Nguồn | https://cloud.google.com/vertex-ai/pricing (chuyển hướng tới https://cloud.google.com/products/gemini-enterprise-agent-platform/pricing) | Price List API `AmazonBedrockAgentCore` (2026-10-14); https://aws.amazon.com/bedrock/agentcore/pricing/ | Retail API; https://azure.microsoft.com/en-us/pricing/details/container-apps/ |

---

## 5. Network (phần R9)

### 5.1 Load balancer L7 (Application LB)

| | GCP | AWS | Azure |
|---|---|---|---|
| SKU | Global external Application LB / regional external ALB (forwarding rule) · Internal/regional Envoy-based ALB (proxy instance) | Application Load Balancer | Application Gateway Standard v2 · WAF v2 · Application Gateway for Containers (AGC) |
| Phí cố định | Global forwarding rule: **$0.025/giờ** (5 rule đầu), $0.01/giờ mỗi rule thêm · Regional forwarding rule (Singapore): **$0.028/giờ** (5 rule đầu), **$0.011/giờ** mỗi rule thêm · Internal ALB: **$0.025 / proxy instance-giờ** | **$0.0252 / ALB-giờ** | Std v2: **$0.26/giờ** (Fixed) · WAF v2: **$0.468/giờ** · Basic v2: $0.0252/giờ · AGC: $0.022/giờ (AGC) + $0.013/giờ (Frontend) + $0.156/giờ (Association) |
| Phí theo tải | Data processed (Singapore): **$0.009 / GiB** inbound và **$0.009 / GiB** outbound · Internal ALB: $0.008 / GiB | **$0.008 / LCU-giờ** | Std v2: **$0.008 / Capacity Unit-giờ** · WAF v2: **$0.0144 / CU-giờ** · AGC: $0.0104 / CU-giờ |
| Nguồn | https://cloud.google.com/vpc/network-pricing (mục Cloud Load Balancing) | Price List API `AWSELB`; https://aws.amazon.com/elasticloadbalancing/pricing/ | Retail API `Application Gateway`; https://azure.microsoft.com/en-us/pricing/details/application-gateway/ |

### 5.2 WAF

| | GCP — Cloud Armor | AWS — AWS WAF | Azure — WAF |
|---|---|---|---|
| Standard (PAYG) | Policy **$5/tháng** · Rule **$1/tháng** · Request **$0.75 / triệu** (policy global) hoặc **$0.60 / triệu** (policy regional) · không phí data processing | Web ACL **$5/tháng** · Rule **$1/tháng** · Request **$0.60 / triệu** (tới 1.500 WCU; bậc WCU cao hơn $0.80–$2.00 / triệu) · Bot Control rule group $10/tháng | Trên Application Gateway: dùng SKU **WAF v2** ($0.468/giờ + $0.0144/CU-giờ, mục 5.1) · Front Door **Premium** đã gồm WAF managed rules: base **$330/tháng** + request Zone 2 **$0.0168 / 10.000** (250 triệu đầu) · Front Door **Standard**: base **$35/tháng** + $0.0108 / 10.000 request |
| Gói cao hơn | Cloud Armor Enterprise Paygo: **$200/tháng** (gồm 2 protected resource) + $200/resource thêm + data processing · Annual $3.000/tháng (cam kết 1 năm) | Shield Advanced (không thu thập) | — |
| Nguồn | https://cloud.google.com/armor/pricing (nội dung nằm trong trang network-pricing) | Price List API `awswaf`; https://aws.amazon.com/waf/pricing/ | Retail API `Azure Front Door Service`; https://azure.microsoft.com/en-us/pricing/details/frontdoor/ |

Meter "Application Gateway WAF v2 - Discounted" (Fixed $0.26/giờ, CU $0.008/giờ, từ 2025-10-01) có trong Retail API — **không dùng** vì có thể là giá ưu đãi; chưa xác minh điều kiện (gap G5).

### 5.3 NAT gateway

| | GCP — Cloud NAT | AWS — NAT Gateway | Azure — NAT Gateway |
|---|---|---|---|
| Phí giờ | **$0.0014 / VM instance-giờ** (tối đa tính 32 VM; > 32 VM: **$0.044/giờ**) | **$0.059 / NAT gateway-giờ** (zonal và Regional NAT Gateway cùng giá) | **$0.045 / giờ** (Standard) |
| Phí data | **$0.045 / GiB** (in + out, giá như nhau mọi region) | **$0.059 / GB** | **$0.045 / GB** |
| IP public đi kèm | **$0.005 / IP-giờ** | Public IPv4: **$0.005 / IP-giờ** | Standard static IPv4: **$0.005 / giờ** |
| Nguồn | https://cloud.google.com/vpc/network-pricing (mục Cloud NAT) | Price List API `AmazonEC2` (product family NAT Gateway), `AmazonVPC`; https://aws.amazon.com/vpc/pricing/ | Retail API `NAT Gateway` (meter Global), `IP Addresses`; https://azure.microsoft.com/en-us/pricing/details/azure-nat-gateway/ |

Với sandbox **không egress** (D13), NAT chỉ phục vụ app/connector gọi SaaS (D4). Fargate Pod bắt buộc private subnet có NAT hoặc VPC endpoint để kéo image.

### 5.4 Private endpoint

| | GCP — Private Service Connect | AWS — PrivateLink interface endpoint | Azure — Private Endpoint |
|---|---|---|---|
| Phí giờ | **$0.01 / endpoint-giờ** | **$0.013 / endpoint-giờ / AZ** | **$0.01 / endpoint-giờ** |
| Phí data | Endpoint tới **Google APIs** (vd Vertex AI): **"No data charge"** · Endpoint tới published service: **$0.01 / GiB** (0–1 PiB), $0.006 (1–5 PiB), $0.004 (> 5 PiB) | **$0.01 / GB** (tới 1 PB), $0.006, $0.004 | **$0.01 / GB** inbound và **$0.01 / GB** outbound (bậc 0–1 PB), $0.006, $0.004 |
| Nguồn | https://cloud.google.com/vpc/network-pricing (mục Private Service Connect) | Price List API `AmazonVPC` (`APS1-VpcEndpoint-Hours`, `APS1-VpcEndpoint-Bytes`); https://aws.amazon.com/privatelink/pricing/ | Retail API `Virtual Network Private Link` (meter Global; SGX Singapore 1 cùng giá); https://azure.microsoft.com/en-us/pricing/details/private-link/ |

AWS tính theo **mỗi AZ** của endpoint ⇒ endpoint 2 AZ = 2 × $0.013/giờ (theo trang PrivateLink; số AZ do kiến trúc quyết định).

### 5.5 Internet egress và inter-zone

| | GCP (từ asia-southeast1) | AWS (từ ap-southeast-1) | Azure (từ Southeast Asia) |
|---|---|---|---|
| Egress Internet tới châu Á / Việt Nam | Premium Tier, đích "Asia Excl Korea, Indonesia": **$0.12 / GiB** (0–1 TiB), **$0.11** (1–10 TiB), $0.085 (> 10 TiB) · Standard Tier: $0.11 (200 GiB–10 TiB; 200 GiB đầu miễn phí — loại), $0.075, $0.07 | **$0.12 / GB** (10 TB đầu, "beyond the global free tier" — 100 GB free bị loại), $0.085 (40 TB tiếp), $0.082, $0.080 | Microsoft Global Network: **$0.12 / GB** (sau 100 GB đầu miễn phí — loại; tới 10 TB), $0.085, $0.082, $0.08 · Routing preference Internet: $0.11, $0.075, $0.07, $0.06 |
| Inter-zone cùng region | **$0.01 / GiB** | **$0.01 / GB** mỗi chiều (`APS1-DataTransfer-Regional-Bytes`, "in/out/between AZs") | Retail API: **$0.01 / GB** "Inter-Availability Zone Data Transfer Out" và **$0.01 / GB** "… In" — trang Bandwidth chỉ ghi "same AZ: Free", không liệt kê phí inter-AZ (gap G2) |
| Nguồn | https://cloud.google.com/vpc/network-pricing | Price List API `AWSDataTransfer`, `AmazonEC2`; https://aws.amazon.com/ec2/pricing/on-demand/#Data_Transfer | Retail API `Bandwidth`; https://azure.microsoft.com/en-us/pricing/details/bandwidth/ |

---

## 6. Ghi chú SLA và công nghệ cách ly (tóm tắt cho slide)

- **Control plane:** cả ba đều đạt 99,95% ở cấu hình trả phí $0.10/giờ (GKE regional/Autopilot, EKS standard, AKS Standard có AZ). Không dùng: GKE zonal (99,5% – chỉ ngang ngưỡng đề, không có biên), AKS Free (không SLA).
- **Autopilot Pods đa zone: 99,9%** — đáp ứng 99,5% giờ hành chính.
- **Cách ly sandbox:**
  - GCP: gVisor (userspace kernel) có sẵn trên Autopilot ⇒ sandbox trả tiền theo Pod, scale về 0 tự nhiên, không cần node pool riêng.
  - AWS: Fargate cho mỗi Pod một VM riêng (Firecracker-class isolation theo mô tả "VM boundary") ⇒ trả theo Pod; hoặc Kata/Firecracker tự quản trên M7i/M8i/C7i nested virtualization hoặc bare metal (đắt, ≥ 96 vCPU/node).
  - Azure: Kata (pod VM) cần node pool Azure Linux, Gen2 nested-virt (Dsv3/Dsv5…); trả theo VM ⇒ cần autoscaler về 0 ngoài giờ. Phương án managed: ACA Dynamic Sessions ($0.03/session-giờ).
- **No egress (D13):** cần NetworkPolicy/egress deny ở mọi phương án; với dịch vụ managed (Agent Engine, AgentCore, Dynamic Sessions) cần kiểm tra khả năng tắt mạng — chưa thuộc phạm vi giá.

---

## 7. Gaps (cần bổ sung / xác minh)

| # | Gap | URL đã kiểm tra |
|---|---|---|
| G1 | Azure meter `FreeTierInfrastructureCost Uptime SLA` **$0.05/giờ** hiệu lực 2026-10-01: không có giải thích trên trang giá AKS và tài liệu tier. Chưa biết có áp cho Free tier hay không | https://prices.azure.com/api/retail/prices (filter AKS) ; https://azure.microsoft.com/en-us/pricing/details/kubernetes-service/ ; https://learn.microsoft.com/en-us/azure/aks/free-standard-pricing-tiers |
| G2 | Azure inter-AZ data transfer: Retail API có meter $0.01/GB mỗi chiều, trang Bandwidth không liệt kê — cần xác minh có đang tính phí không | https://azure.microsoft.com/en-us/pricing/details/bandwidth/ |
| G3 | Azure reservation cho `F4s_v2`, `D4s_v3`: **KHÔNG TÌM THẤY** trong Retail API | https://prices.azure.com/api/retail/prices (armSkuName eq 'Standard_F4s_v2' / 'Standard_D4s_v3') |
| G4 | ACA: Retail API Southeast Asia có cả "Dedicated Plan Management" $0.10/giờ (2023) và "Environment Management Hour" $0.14/giờ (2026-09-01); trang giá (region mặc định) chỉ ghi Management $0.10/giờ. Chưa rõ meter nào áp cho SEA | https://azure.microsoft.com/en-us/pricing/details/container-apps/ |
| G5 | "Application Gateway WAF v2 - Discounted" — chưa rõ điều kiện; không dùng | Retail API `Application Gateway` |
| G6 | (Đã xử lý) EKS extended support = $0.10 + $0.50 = $0.60 / cluster-giờ, đối chiếu trang giá | https://aws.amazon.com/eks/pricing/ |
| G7 | GCP Agent Engine (Agent Compute/Memory): trang giá không tách theo region; chưa xác nhận có chạy ở asia-southeast1 với cùng giá | https://cloud.google.com/products/gemini-enterprise-agent-platform/pricing |
| G8 | Thời gian cold start chính thức của Fargate Pod, Kata pod VM (AKS), Agent Engine sandbox, Dynamic Sessions — chưa có số liệu chính thức | — |
| G9 | GCP đơn giá predefined vCPU/GiB (N2, N4, E2) cho asia-southeast1 không tách được từ dữ liệu trang; chỉ có giá machine type và giá custom | https://cloud.google.com/products/compute/pricing/general-purpose |
| G10 | SLA của Cloud Run, Lambda, ACA, ACI, Fargate, Agent Engine, AgentCore, Dynamic Sessions chưa thu thập | — |
| G11 | Fargate Spot (ECS) giá Singapore: trang hiển thị động, không trích được; dù sao EKS không hỗ trợ | https://aws.amazon.com/fargate/pricing/ |
| G12 | Spot giá biến động (snapshot 2026-10-16); GCP/Azure/AWS đều có thể đổi giá spot | các URL spot ở mục 2.4 |
| G13 | Kata/Firecracker trên EKS với nested virtualization: AWS chỉ tài liệu hóa KVM/Hyper-V L1, không có hướng dẫn EKS chính thức cho Kata trên VM nested — cần PoC | https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/amazon-ec2-nested-virtualization.html |
