---
aliases: []
tags: []
title: "**Architectural Audit of Compute Substrates for High-Performance Kubernetes Data Planes**"
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2025-12-31T16:56:11+00:00
modified: 2026-01-03T10:18:48+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

# **Architectural Audit of Compute Substrates for High-Performance Kubernetes Data Planes**

## **1. Executive Summary**

This document serves as a comprehensive architectural audit of the physical and virtualized compute infrastructure provided by Amazon Web Services (AWS) and Microsoft Azure, specifically targeting the AWS m6i/m7i/m7g and Azure D_v5/D_v6 instance families. This investigation was commissioned to inform the optimization of a Kubernetes data plane where instruction throughput, deterministic latency, and cache locality are the primary performance indicators. Utilizing Data-Oriented Design (DOD) principles requires a rigorous "hardware reality" audit to bridge the abstraction gap between the virtualized control plane and the underlying silicon.

The analysis reveals a pivotal shift in cloud infrastructure topology. The industry is transitioning from monolithic die designs characterized by uniform memory access (such as the Ice Lake architecture found in m6i and D_v5) to disaggregated, multi-tile "chiplet" architectures present in Sapphire Rapids (m7i) and Emerald Rapids (D_v6). While these newer architectures offer substantial gains in raw throughput via DDR5 memory subsystems and specialized vector acceleration (AMX/AVX-512), they introduce complex, non-uniform latency maps that challenge traditional "flat" memory assumptions.

Crucially, the audit identifies the Azure D_v6 family (powered by Intel Emerald Rapids) as a superior candidate for cache-sensitive workloads due to a massive increase in Last Level Cache (L3) to 5 MB per core, effectively creating a 320 MB shared instruction and data pool on large instances. Conversely, the AWS m7i family (Sapphire Rapids) and the Nitro System offer a more transparent, "near-metal" hypervisor implementation that minimizes the "lie-to-guest" phenomenon regarding NUMA topology, making it potentially more predictable for strictly pinned Kubernetes workloads utilizing static CPU management policies.

This report dissects the hypervisor mechanisms, processor microarchitectures, interconnect topologies, and necessary Operating System/Kubernetes configurations to align the software data plane with the physical reality of the hardware.

## **2. The Hypervisor Substrate & Execution Environment**

The hypervisor acts as the primary abstraction layer between the Kubernetes node and the physical silicon. For a high-performance data plane, the hypervisor is often the source of non-deterministic latency injection (jitter), "steal time," and topology obfuscation. Understanding the distinct architectural philosophies of AWS and Azure is prerequisite to interpreting performance telemetry.

### **2.1. AWS Nitro System: The Decoupled Architecture**

The AWS Nitro System represents a fundamental departure from traditional software-defined virtualization. By offloading virtualization functions—I/O, networking, storage, and security—to dedicated ASIC-based Nitro Cards, AWS minimizes the footprint of the hypervisor on the main system board.1 This architectural decision has profound implications for data plane performance.

The Nitro Hypervisor is a lightweight, KVM-based implementation that performs minimal scheduling work. Crucially for data plane performance, Nitro instances (specifically m6i and m7i) typically map vCPUs to physical threads in a static manner. "Steal time," the metric indicating cycles a vCPU was ready to run but the hypervisor was servicing another thread, is virtually eliminated in non-burstable Nitro instances.3 In the context of Data-Oriented Design, this static mapping is vital. DOD relies on predictable cache access patterns. If a vCPU is rescheduled to a different physical core (pcpu) by an overactive hypervisor scheduler, the L1 and L2 caches are effectively cold, destroying the performance benefits of data locality optimizations. Nitro’s architecture strongly favors static pinning, meaning that once an instance is launched, its vCPUs are pinned to specific physical cores for the lifetime of the instance.5 This behavior allows the guest OS—and subsequently the Kubernetes CPU Manager—to make reliable assumptions about core affinity.

A distinct advantage of the Nitro system for NUMA-aware applications is its high-fidelity topology pass-through. Nitro exposes the underlying L3 cache and NUMA topology directly to the instance.5 When an m7i.48xlarge reports two NUMA nodes, these correspond strictly to the physical sockets or sub-NUMA clusters (SNC) of the underlying Sapphire Rapids hardware. There is no "virtual NUMA" layer obfuscating the physical reality, allowing numactl and Kubernetes Topology Manager to function with deterministic results.6 Furthermore, the Nitro security model ensures that customer instances never share core-specific resources like L1/L2 caches or execution threads with other tenants, eliminating a major class of "noisy neighbor" interference and side-channel risks.5

### **2.2. Azure Hyper-V: The Root Partition Model**

Azure utilizes a customized version of Microsoft Hyper-V. Unlike Nitro’s hardware offload model, Hyper-V relies on a "Root Partition" (running a stripped-down Windows kernel) to manage I/O and scheduling. While Azure has introduced "Azure Boost" (similar to Nitro cards) in newer generations like the D_v6 to offload storage and networking, the scheduling mechanics retain the characteristics of a Type-1 hypervisor managing a root partition.

The handling of NUMA on Azure is complex due to the use of "Virtual NUMA" (vNUMA). Hyper-V projects a topology to the guest that attempts to mirror the physical hardware, but deviations can occur based on how the Virtual Machine (VM) is packed onto the host. For VM sizes that fit within a single physical NUMA node (e.g., Standard_D16s_v5), Hyper-V may present a single node. However, for larger VMs that span physical sockets (e.g., Standard_D96s_v6), vNUMA topology is projected. A critical risk here is the potential misalignment between vNUMA and pNUMA (physical NUMA). If the underlying host is fragmented, Hyper-V might construct a VM from non-contiguous physical cores but present them as a single vNUMA node to the guest if NUMA spanning is enabled. For a cache-sensitive data plane, this is catastrophic: a thread might access a memory address it believes is local (based on vNUMA), but physically, that request traverses the UPI (Ultra Path Interconnect) link to a remote socket, incurring a 1.5x to 2.5x latency penalty.

Recent Azure generations (v5, v6) and "Dedicated Host" options mitigate this by enforcing stricter alignment, but the "noisy neighbor" effect in the root partition remains a factor that is statistically more significant than on Nitro. The root partition itself requires CPU cycles for cluster management and health monitoring, which can manifest as micro-latency spikes in the guest workload. Azure employs "Fair Share" CPU scheduling and strict throttling on disk/network IOPS to prevent one tenant from monopolizing resources, but these throttles themselves can act as performance limiters for bursty data plane traffic.

### **2.3. Noisy Neighbor Mitigation and Resource Isolation**

Both platforms utilize Intel Resource Director Technology (RDT) to enforce isolation at the silicon level, specifically utilizing Cache Allocation Technology (CAT) and Memory Bandwidth Allocation (MBA).

On AWS Nitro, the system uses these hardware controls to strictly partition Last Level Cache (LLC) ways and memory bandwidth between instances on the same socket. This prevents a "noisy neighbor" (e.g., a streaming video encoder) from thrashing the L3 cache lines required by the data plane.5 The isolation is robust enough that AWS claims instances never share system resources such as L1/L2 cache or threads running on the same CPU complex.

Azure similarly uses strict resource governance to prevent noisy neighbors. However, the mechanism relies heavily on the Azure Fabric Controller and the hypervisor to enforce memory and process separation. While Azure guarantees compute isolation for "Isolated" VM sizes, general-purpose sizes like D_v5 share the host with other tenants. The "noisy neighbor" problem in Azure is often managed through throttling patterns and resource governance policies rather than the hard hardware partitioning seen in Nitro's bare-metal-like approach.8 The introduction of Azure Boost in D_v6 aims to close this gap by offloading more virtualization tasks to dedicated hardware, improving jitter characteristics.

---

**3. Processor Microarchitecture: The Metal**

The efficacy of Data-Oriented Design is inextricably linked to the specific microarchitecture of the execution engine. The transition from Ice Lake (m6i/D_v5) to Sapphire Rapids (m7i) and Emerald Rapids (D_v6) introduces radical changes in cache hierarchy and vector processing capabilities.

### **3.1. Intel Ice Lake (3rd Gen Xeon Scalable)**

Instances: AWS m6i, Azure D_v5

Microarchitecture: Sunny Cove

Process: 10nm (Intel 7)

The Sunny Cove core represented Intel's first major IPC (Instructions Per Clock) uplift in years. A critical feature for data planes is the **L2 cache size**, which increased to 1.25 MB per core in the server implementation.18 Crucially, the L2 cache in Ice Lake is **non-inclusive**. Unlike previous generations where the L3 cache strictly contained a copy of all data in the L2 (inclusive), a non-inclusive policy allows the L2 and L3 to effectively sum their capacities, maximizing the total unique data capable of being held on-die. This is beneficial for data planes with large working sets, as lines evicted from L2 can be allocated in L3 without forcing invalidations in L2.

However, Ice Lake is constrained by **AVX-512 downclocking**. While less severe than in Skylake or Cascade Lake, heavy utilization of 512-bit registers (e.g., for SIMD-accelerated packet processing or cryptographic offload) triggers a "license" transition in the power management unit. This results in a reduction of the core frequency (and potentially the frequency of other cores on the same socket) to maintain thermal limits.19 For a data plane, this introduces a "performance cliff" where enabling vector optimizations might paradoxically lower overall throughput if the frequency penalty outweighs the IPC gain.

### **3.2. Intel Sapphire Rapids (4th Gen Xeon Scalable)**

Instances: AWS m7i, m7i-flex

Microarchitecture: Golden Cove

Process: Intel 7

Sapphire Rapids (SPR) introduces the "Golden Cove" core, which is significantly wider and deeper than Sunny Cove. The **L2 cache doubles to 2 MB per core**, which is a massive boon for data planes, allowing substantially larger instruction windows and packet buffers to reside close to the execution ports.

The most significant architectural shift in SPR is the move to a **chiplet (multi-tile) design** for high-core-count (XCC) configurations. An XCC processor (likely used in m7i.48xlarge and metal-48xl) consists of four compute tiles connected by an Embedded Multi-die Interconnect Bridge (EMIB).22 This introduces a "mesh" topology where accessing L3 cache slices located on a different tile—even within the same socket—incurs higher latency than accessing a local slice. The concept of "Uniform Memory Access" within a socket is effectively broken; the hardware presents a single socket to the OS, but physically, it functions as a "Sub-NUMA" cluster.

SPR also introduces **Advanced Matrix Extensions (AMX)**. While primarily marketed for AI/ML, AMX can be exploited for specific data plane operations involving matrix math (e.g., Reed-Solomon coding, complex checksums, or signal processing). AMX operates on dedicated tile hardware, offering throughput far exceeding AVX-512 without the same severe frequency throttling penalties associated with wide vector units.25 Additionally, SPR includes built-in accelerators like **Data Streaming Accelerator (DSA)** and **QuickAssist Technology (QAT)**, which are exposed on bare-metal m7i instances but may be unavailable or emulated on virtualized sizes depending on the hypervisor configuration.

### **3.3. Intel Emerald Rapids (5th Gen Xeon Scalable)**

Instances: Azure D_v6

Microarchitecture: Raptor Cove

Process: Intel 7

Emerald Rapids (EMR) acts as a refinement ("Tock") to Sapphire Rapids. The headline feature for data plane architects is the **L3 Cache explosion**. EMR increases the shared L3 cache to **5 MB per core**, up from 1.875 MB in SPR.27 For a 64-core instance, this results in a massive 320 MB shared pool (compared to ~112 MB on SPR).

For a Kubernetes data plane, this L3 capacity is game-changing. It allows the entire instruction text segment and significant packet buffer pools (flow tables, connection tracking entries) to sit resident in L3, drastically reducing expensive trips to DRAM. This "Cache Locality King" status makes the D_v6 family exceptionally resilient to memory latency stalls.

Architecturally, EMR consolidates the 4-tile design of SPR into a **2-tile XCC design**. This reduction in tile count reduces the "hops" required to traverse the mesh interconnect, improving the worst-case intra-socket latency compared to SPR. Furthermore, EMR supports **DDR5-5600** memory (up from DDR5-4800 in SPR), providing a tangible bandwidth uplift critical for throughput-bound packet processing.

### **3.4. AWS Graviton3 (m7g)**

Instances: AWS m7g

Microarchitecture: ARM Neoverse V1

L2 Cache: 1 MB private per core

L3 Cache: ~32 MB shared per socket

While x86 dominates the high-performance data plane market, the Graviton3 (m7g) warrants analysis. The Neoverse V1 core utilizes SVE (Scalable Vector Extensions) with a 256-bit width, which is narrower than AVX-512. However, the Graviton3 memory subsystem is monolithic, avoiding the complex tile-to-tile latency penalties found in SPR/EMR. For data planes that cannot effectively saturate AVX-512 or AMX, the m7g offers superior performance-per-watt and consistency, though generally lower peak instruction throughput for vector-heavy code.

### **3.5. Processor Comparison Table**

| Feature | AWS m6i / Azure D_v5 | AWS m7i | Azure D_v6 | AWS m7g |
|:---- |:---- |:---- |:---- |:---- |
| **Processor** | Intel Ice Lake | Intel Sapphire Rapids | Intel Emerald Rapids | AWS Graviton3 |
| **Core Architecture** | Sunny Cove | Golden Cove | Raptor Cove | Neoverse V1 |
| **L2 Cache / Core** | 1.25 MB | 2 MB | 2 MB | 1 MB |
| **L3 Cache / Core** | 1.5 MB | 1.875 MB | **5 MB** | ~0.5 MB (Shared Slice) |
| **Memory** | DDR4-3200 | DDR5-4800 | **DDR5-5600** | DDR5-4800 |
| **AVX-512** | Yes (Throttles) | Yes (AMX Support) | Yes (AMX Support) | No (SVE 256-bit) |
| **Topology** | Monolithic (MCC) | 4-Tile Chiplet (XCC) | 2-Tile Chiplet (XCC) | Monolithic |

## **4. NUMA & Memory Interconnects: The Latency Map**

Optimizing for cache locality requires mapping the physical territory of data movement. The "Flat" memory model is a fiction in modern cloud servers; the reality is a tiered landscape of latencies defined by interconnects.

### **4.1. Interconnect Topology and Latency**

The communication between sockets and tiles is governed by Intel's **Ultra Path Interconnect (UPI)**.

* **Sapphire Rapids (m7i):** Utilizes UPI 2.0 with speeds up to 16 GT/s. In a dual-socket configuration (e.g., m7i.48xlarge), accessing remote memory adds approximately **130-140ns** of latency over the ~80-90ns local latency.
* **Emerald Rapids (D_v6):** Boosts UPI speeds to 20 GT/s. While bandwidth improves, the latency penalty for crossing sockets remains constrained by physical distance and serialization overhead, hovering around **140-150ns** for remote access.

The Chiplet Penalty (XCC vs. MCC):

The m7i family likely mixes MCC (monolithic) dies for smaller sizes and XCC (tiled) for larger sizes. If a Kubernetes pod lands on an m7i.24xlarge (likely XCC), it operates on a 4-tile mesh. A thread on Tile 0 accessing memory controlled by Tile 3 incurs latency not just from DRAM, but from traversing two EMIB bridges. This intra-socket latency variance is masked by the OS but impacts the tail latency of high-frequency trading or real-time data processing applications. lscpu output on these instances is the source of truth: if it reports multiple NUMA nodes per socket (indicating Sub-NUMA Clustering is enabled), the OS is aware of the tiles. If it reports 1 node per socket on an XCC part, the hardware is interleaving memory across tiles, averaging latency but destroying locality optimizations.

### **4.2. Sub-NUMA Clustering (SNC)**

Sub-NUMA Clustering partitions a single socket into 2 (SNC2) or 4 (SNC4) logical NUMA domains to localize memory traffic.

* **AWS Strategy:** AWS typically disables SNC on general-purpose instances (m7i) to simplify scheduling, presenting 1 NUMA node per socket. This "averages" performance but raises the latency floor because memory requests are hashed across all memory controllers in the socket, regardless of distance.7
* **Azure Strategy:** Azure often exposes SNC on larger sizes (e.g., Standard_D96s_v6 might show 4 NUMA nodes total—2 per socket). This allows the OS to allocate memory closer to the core *if* the application is NUMA-aware. However, relying on this requires the application to explicitly bind memory using libnuma or numactl, otherwise, the OS scheduler might migrate threads across SNC domains, incurring severe latency penalties.

### **4.3. Memory Bandwidth and Latency Benchmarks**

Synthesizing data from Intel Memory Latency Checker (MLC) benchmarks provides a comparative baseline:

| Metric | m6i (Ice Lake) | m7i (Sapphire Rapids) | D_v6 (Emerald Rapids) |
|:---- |:---- |:---- |:---- |
| **Local Latency (Idle)** | ~85 ns | ~95-100 ns (mesh penalty) | ~95 ns |
| **Remote Latency (Idle)** | ~145 ns | ~150-160 ns | ~150 ns |
| **L3 Access Latency** | ~20 ns | ~30-35 ns (mesh penalty) | ~30 ns |
| **Memory BW (Per Socket)** | ~200 GB/s (DDR4) | ~300 GB/s (DDR5) | ~330 GB/s (DDR5) |
| **Interconnect BW** | ~40 GB/s | ~60 GB/s | ~75 GB/s |

**Insight:** Sapphire Rapids exhibits *higher* idle latency than Ice Lake due to the complexity of the mesh and tile architecture. However, its loaded latency curve is flatter due to the massive bandwidth headroom of DDR5. For a data plane, this means m7i and D_v6 will handle burst traffic significantly better, even if single-packet latency at idle is slightly worse.

## **5. Kubernetes & OS Configuration Efficacy**

> **Refactored:** See [[SoT - High-Performance Kubernetes Node Tuning]] for the definitive configuration guide.

The hardware reality described above is rendered moot if the software stack ignores it. Optimizing Kubernetes for this infrastructure requires precise configuration to map logical pods to physical topology.

### **5.1. Topology Manager Policies**

The standard best-effort policy in Kubernetes is insufficient for high-performance data planes on tiled CPUs.

* **Recommendation:** Use the single-numa-node policy.
* **Mechanism:** This policy restricts a pod's resource allocation (CPU + Memory) to a single NUMA node. On an m7i.48xlarge (2 sockets), this ensures the pod does not straddle the UPI link, preventing catastrophic cache thrashing where a thread on Socket 0 constantly snoops L3 lines on Socket 1.35
* **Advanced Insight:** On XCC parts (Sapphire/Emerald) where SNC might be exposed (Azure), single-numa-node aligns the pod to a specific quadrant or hemisphere of the socket. This minimizes intra-socket mesh traversal. However, if the instance presents a unified socket (AWS default), this policy only guarantees socket affinity, not tile affinity.

### **5.2. Huge Pages: Transparent vs. Explicit**

Data planes utilize huge pages to reduce Translation Lookaside Buffer (TLB) misses, which are costly on modern workloads with large memory footprints.

* **Hardware Reality:** Sapphire and Emerald Rapids have larger TLBs (2048 entries for Second Level TLB) 18, making them more tolerant of 4K pages than older generations, but huge pages remain critical for GB-scale heaps.
* **Transparent Huge Pages (THP):** The khugepaged daemon introduces non-deterministic jitter as it defragments memory in the background. For a latency-sensitive data plane, this "stop-the-world" behavior is unacceptable.
* **Explicit Huge Pages:** Configuring 1GB huge pages via kernel boot parameters (hugepagesz=1G hugepages=N) is the gold standard. It locks physical memory, prevents swapping, and ensures the TLB mapping is static. Kubernetes supports this natively via hugepages-1Gi resource limits. This must be configured at the boot loader level (Grub) on the node before Kubelet starts.

### **5.3. CPU Pinning and Isolation**

To prevent the Linux CFS scheduler from migrating critical threads, strict pinning is required.

* **CPU Manager:** Use the static policy. This grants exclusive cores to the container, removing them from the shared pool used by other pods and system processes.
* **Hyper-Threading (SMT):** On Hyper-V (Azure), a "core" in K8s is a thread. Pinning two threads that map to the same physical core is beneficial for L1/L2 sharing (cache coherency) but detrimental if both threads contend for the same execution ports (e.g., both doing heavy AVX-512 math). On AWS, lscpu reveals that vCPU 0 and vCPU 1 are typically sibling threads of the same physical core.42 "Gang scheduling" logic should be used to place cooperative threads (e.g., a worker and a helper) on siblings, while separating contentious threads.
* **Isolation:** For extreme sensitivity, use kernel boot parameters isolcpus to remove data plane cores from the general kernel scheduler entirely, managing them manually via taskset or cgroups inside the application.

### **5.4. Noisy Neighbor Isolation with RDT**

To mitigate interference from other tenants or system processes, utilizing Intel RDT features is recommended where exposed.

* **Cache Allocation Technology (CAT):** Can be used to partition the L3 cache, dedicating specific ways to high-priority containers. This is accessible via the resctrl filesystem if the host/hypervisor exposes it (more likely on bare metal metal instances or dedicated hosts).
* **Memory Bandwidth Allocation (MBA):** Throttles the memory bandwidth of lower-priority workloads to ensure the data plane has sufficient access to the DRAM controllers.

## **6. Recommendations & Synthesis**

### **6.1. Instance Selection Matrix**

| Workload Characteristic | Recommended Instance | Reasoning |
|:---- |:---- |:---- |
| **Latency Sensitive, Cache Heavy** | **Azure D_v6 (Emerald Rapids)** | **5 MB L3/core** allows massive lookup tables to stay on-die, masking DRAM latency. Best-in-class cache per core. |
| **Throughput Intensive, Vector Math** | **AWS m7i (Metal)** | DDR5 bandwidth feeds vector units. Metal avoids hypervisor overhead. AMX accelerates specific data operations. Nitro provides predictable topology. |
| **General Purpose Data Plane** | **AWS m6i / Azure D_v5** | Monolithic die (Ice Lake) offers lower core-to-core latency variance than tiled SPR/EMR. Mature platform with lower cost. |
| **Cost-Sensitive** | **AWS m7g (Graviton3)** | Monolithic mesh avoids tile penalties. Excellent perf/watt, provided the workload does not strictly require AVX-512 instructions. |

### **6.2. The "Golden Config" for Data Planes**

To bridge the gap between virtual abstraction and silicon reality, the following configuration is defined as optimal for a Kubernetes node on m7i or D_v6:

1. **BIOS/Instance:** Disable "Node Interleaving" (Enable NUMA) if accessible (Metal instances).
2. **Kernel Boot Parameters:**
   * isolcpus=<data_plane_cores> to remove OS interrupts.
   * default_hugepagesz=1G hugepagesz=1G hugepages=N to pre-allocate memory.
   * transparent_hugepage=never to eliminate compaction jitter.
1. **Kubernetes Configuration:**
   * --topology-manager-policy=single-numa-node to enforce socket affinity.
   * --cpu-manager-policy=static to enforce exclusive core usage.
   * Pod Spec: resources: limits: memory: "10Gi", hugepages-1Gi: "10Gi", cpu: "8" (Guaranteed QoS class).
4. **Application (DOD):**
   * Align data structures to **64-byte** cache lines.
   * Size hot working sets to fit within **2 MB** (the L2 size of m7i/D_v6) per thread.
   * Use sched_setaffinity to bind critical threads to sibling hyper-threads of the same core to maximize L1/L2 reuse.

### **6.3. Conclusion**

The "Hardware Reality" is that cloud instances are no longer generic compute units; they are specialized execution environments defined by their cache topology and neighbor relations. For optimization goals prioritizing **cache locality**, **Azure's D_v6 (Emerald Rapids)** is the superior choice due to its massive 320 MB L3 cache, provided the vNUMA configuration is managed correctly. For workloads requiring **deterministic throughput** and "near-metal" behavior, **AWS m7i** on the Nitro System offers a more transparent and predictable substrate.

Transitioning to Data-Oriented Design in the cloud requires treating the Instance Type not as a commodity, but as a specific silicon SKU with a known latency map. By aligning data structures to the 2MB L2 of Sapphire/Emerald Rapids and strictly pinning pods to physical NUMA boundaries, performance parity with on-premise hardware is achievable.
