# Can Erturk

Systems engineer building shared intelligence infrastructure for context-aware, privacy-first applications.

I work at the intersection of platform engineering, real-time systems, and applied AI — designing the reusable layers that make complex products possible without reinventing core logic every time.

## PARM — Shared Intelligence Layer

[PARM](https://github.com/ErturkCan/parm) is the platform I'm building: an agent orchestration and workflow automation layer that provides context handling, decision pipelines, timing intelligence, and privacy-aware data processing. Instead of each product implementing its own logic, PARM provides the infrastructure.

Three real-world products run on PARM today:

**[CanDelivers](https://github.com/ErturkCan/candelivers)** — Last-mile logistics for bulky items in dense urban environments. Routing optimization, constraint modeling, and operational simulation for local delivery coordination.

**[Clueat](https://github.com/ErturkCan/clueat)** — Food ingredient parsing and allergen intelligence. Makes food choices clearer by analyzing labels, resolving ingredient synonyms, and surfacing allergen risks with explainable scoring.

**[KeepClos](https://github.com/ErturkCan/keepclos)** — Context-aware relationship intelligence. Models timing and context to support meaningful communication, with privacy-first personal data handling.

Each product solves a focused problem while contributing infrastructure improvements back to the platform.

## Systems & Performance Work

Beyond the PARM ecosystem, I build low-level systems and performance tools:

- **[lockfree-orderbook](https://github.com/ErturkCan/lockfree-orderbook)** — Lock-free order matching engine in Rust with sub-microsecond match latency
- **[stream-pipeline](https://github.com/ErturkCan/stream-pipeline)** — Backpressure-aware stream processing with lock-free ring buffers
- **[feed-handler](https://github.com/ErturkCan/feed-handler)** — Zero-copy market data feed processor and order book builder
- **[mempool-engine](https://github.com/ErturkCan/mempool-engine)** — Custom slab/arena memory allocator, 7x faster than system malloc
- **[monte-carlo-risk](https://github.com/ErturkCan/monte-carlo-risk)** — SIMD-accelerated Monte Carlo simulation engine
- **[syscall-bench](https://github.com/ErturkCan/syscall-bench)** — Linux syscall latency profiler with CPU pinning and NUMA awareness
- **[telemetry-core](https://github.com/ErturkCan/telemetry-core)** — Lock-free observability library with <1% CPU overhead at 100K events/sec
- **[netprobe](https://github.com/ErturkCan/netprobe)** — Network latency diagnostics with jitter analysis and bufferbloat detection

## Engineering Focus

Real-time data pipelines and backpressure · Low-latency system design and benchmarking · Lock-free concurrency and memory management · Agent orchestration and workflow automation · Privacy-aware data infrastructure · Observability with minimal overhead

## Open to Collaboration

I'm interested in systems problems — especially latency-sensitive infrastructure, platform engineering, and real-time processing. If you're building something where architecture decisions matter, let's talk.

📍 Netherlands · [LinkedIn](https://linkedin.com/in/canetrk)
