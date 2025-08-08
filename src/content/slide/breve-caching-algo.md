---
title: "Breve: FIFO-like Learned Cache"
description: "A comprehensive study of the Breve caching algorithm"
publishDate: "06 May 2025"
theme: "@slidev/theme-default"
tags: ["cache", "machine-learning", "storage", "algorithm"]
draft: false
aspectRatio: "16:9"
---

# Breve: FIFO-like Learned Cache
## A Lightweight and Scalable Caching Solution

---

## Outline

- Introduction
  - Background & Motivation
  - Problem Statement
  - Key Insights
- Related Work
  - Algorithm Evolution
  - Efficiency Strategies
  - Lightweight Design
- Breve Algorithm
  - System Overview
  - UnoSketch & UnoLearner
  - 2-level FIFO Structure
- Evaluation & Results
  - Memory & Performance
  - Hit Ratio Analysis
  - Write Reduction

---

# 1. Introduction

- Background & Motivation
- Problem Statement
- Key Insights

---

## Background & Motivation

**Challenge**: Tiered storage systems require different caching algorithms for different media types

### Current Approach
- **Memory Tier**: LRU-based (Alluxio, GridGain)
- **Flash Tier**: FIFO-based (CacheLib, Colossus)

### Pain Points
- Multiple algorithms to maintain
- Poor scalability with locks
- Complex integration overhead

### Learned Caching Promise
- **Object-level**: LRB
- **Expert-based**: LeCaR, CACHEUS
- **Distribution-based**: LHD

### Reality Check
- Performance overhead
- Implementation complexity
- Inadequate admission control

---

## Problem Statement

**Core Challenge**: We need a unified caching paradigm that addresses:
- Scalability: Poor performance at scale
- Complexity: Difficult implementation
- Admission: Lack of intelligence

**Our Vision**: A single learned algorithm that works effectively across all storage tiers

---

## Key Insights

- **Unified Design**: One algorithm for all tiers
- **Sketch-based**: Efficient feature collection
- **ML + Heuristics**: Best of both worlds
- **FIFO-like**: Scalable & flash-friendly

![Object-Level Learning Approach](https://psiace.me/images/breve-caching-algo/typical-object-level.png){.w-3/4 .mx-auto}

---

# 2. Related Work

- Algorithm Evolution
- Efficiency Strategies
- Lightweight Design

---

## Algorithm Evolution: LRU → FIFO

| Type          | Examples      | Scalable | Flash-Friendly |
| :------------ | :------------ | :------- | :------------- |
| **LRU-like**  | LRU, ARC, LFU | ❌       | ❌             |
| **FIFO-like** | CLOCK, S3FIFO | ✅       | ✅             |

### Why FIFO-like?
- Lock-free → Better scalability
- Sequential → Disk-friendly
- Consistent → Stable throughput

---

## Efficiency Strategies

![Lazy Promotion & Quick Demotion](https://psiace.me/images/breve-caching-algo/LP-QD.png)

### Lazy Promotion
- Promote only when about to evict
- Reduces metadata overhead

### Quick Demotion
- Fast removal of low-value items
- Lowers opportunity cost

---

## Frequency vs. Recency

Real-world workloads show diverse access patterns requiring both frequency and recency

![Wiki Access Patterns](https://psiace.me/images/breve-caching-algo/wiki-2019-access.png){.w-3/4 .mx-auto}
_Wikipedia: Mixed patterns_

![Meta Reuse Heatmap](https://psiace.me/images/breve-caching-algo/meta_rprn_reuse_heatmap_vt.png){.w-3/4 .mx-auto}
_Meta: Reuse distance heatmap_

---

## Sketch-based Lightweight Design

**Sketch**: Space-efficient data structure trading accuracy for space

**Evolution**: LFU → TinyLFU → W-TinyLFU → Breve

![TinyLFU Architecture](https://psiace.me/images/breve-caching-algo/moka-tiny-lfu.png){.w-3/4 .mx-auto}

---

# 3. Breve Algorithm

- System Overview
- UnoSketch & UnoLearner
- 2-level FIFO Structure

---

## System Overview

- **UnoSketch**: Frequency & recency tracking
- **UnoLearner**: ML-based admission control
- **2-level FIFO**: Scalable cache structure

![Breve System Architecture](https://psiace.me/images/breve-caching-algo/breve-overview.png){.w-3/4 .mx-auto}

---

## UnoSketch: Efficient Tracking

### Design Principles
- **Lightweight**: Two Count-Min Sketches
- **Write-based**: Track misses, not hits
- **Quick decay**: Space & accuracy optimization

### Algorithm Details
- **Miss Frequency**: Decay by 0.8× when doubled
- **Write Recency**: Bit-shift on window limit

![UnoSketch Design](https://psiace.me/images/breve-caching-algo/unosketch-overview.png){.w-3/4 .mx-auto}

```
Write Recency Formula
write_recency = (window_limit + window_clock) / actual_write_frequency
```

---

## UnoLearner: ML-based Admission

![UnoLearner Workflow](https://psiace.me/images/breve-caching-algo/unolearner-workflow.png){.w-3/4 .mx-auto}

```
Score Calculation
score = bias + w_freq × miss_freq + w_rec × (write_rec / scale)
```

```
Online Learning
w_freq ← w_freq + η × error × miss_freq
w_rec ← w_rec + η × error × write_rec
```

---

## 2-level FIFO Structure

![2-level FIFO Architecture](https://psiace.me/images/breve-caching-algo/2-level-fifo.png){.w-3/4 .mx-auto}

### Small Cache (10%)
- Admission buffer
- One-hit wonder filter
- Quick demotion

### Main Cache (90%)
- 2-bit CLOCK variant
- Lazy promotion
- ML-guided admission

---

## Admission Strategy

![Admission Decision Flow](https://psiace.me/images/breve-caching-algo/breve-admit.png){width="70%"}

**Decision Logic**
- Scan Resistance: Access count > 1
- ML Score: Learned threshold > 0
- Combined Features: Frequency + recency

---

# 4. Evaluation

- Memory & Performance
- Hit Ratio Analysis
- Write Reduction

---

## Memory Efficiency

### Memory Savings
| Cache Size  | vs Moka    | vs Moka (Compact) |
| :---------- | :--------- | :---------------- |
| 1K objects  | **-40.7%** | **-75.0%**        |
| 10K objects | **-18.4%** | **-67.0%**        |

**Result**: Significant memory savings while maintaining performance

![Memory Usage Comparison](https://psiace.me/images/breve-caching-algo/memory-usage.png){.w-3/4 .mx-auto}

---

## Scalability Performance

**Breve achieves ~2× better throughput than Moka with similar hit ratios**

![Read-Only Performance](https://psiace.me/images/breve-caching-algo/read-only.png){.w-3/4 .mx-auto}
_Mixed Workload (Zipf=1.05)_

![Read-Write Performance](https://psiace.me/images/breve-caching-algo/read-write.png){.w-3/4 .mx-auto}

---

## Hit Ratio Analysis

![Zipf Workload Results](https://psiace.me/images/breve-caching-algo/zipf-workload.png){.w-3/4 .mx-auto}

### Performance Gains
| Workload | vs LRU      | vs S3FIFO   |
| :------- | :---------- | :---------- |
| S1       | **+6.16%**  | **+5.30%**  |
| S2       | **+11.45%** | **+5.70%**  |
| S3       | **+11.66%** | **+5.77%**  |
| DS1      | **+20.63%** | **+12.72%** |
| SPC1     | **+12.07%** | **+1.28%**  |

29/30 test cases better than S3FIFO

---

## Write Reduction Analysis

**Intelligent admission reduces unnecessary writes by up to 58%**

| Workload | Cache Size | Requested  | Actual     | Reduction   |
| :------- | :--------- | :--------- | :--------- | :---------- |
| S1       | 800K       | 1,762,766  | 1,193,533  | **-32.29%** |
| S2       | 800K       | 5,466,459  | 2,575,054  | **-52.89%** |
| S3       | 800K       | 5,207,651  | 2,474,058  | **-52.49%** |
| DS1      | 8M         | 15,863,008 | 12,895,059 | **-18.70%** |
| SPC1     | 2M         | 25,028,988 | 10,393,675 | **-58.47%** |

Flash-Friendly: Up to 82.84% write reduction in low hit-ratio scenarios

---

# 5. Conclusion

- Key Contributions
- Future Directions

---

## Key Contributions

- **Unified Tracking**: Single sketch for frequency & recency across all tiers
- **Online Learning**: Lightweight perceptron with feedback-based updates
- **Scalable Design**: Lock-free FIFO-like architecture for performance
- **Smart Admission**: Balanced hit ratio with reduced write operations

**Summary**: A unified learned caching algorithm that works across different storage tiers

---

## Future Directions

### Enhanced Models
- Object relationship modeling
- Advanced ML architectures
- Temporal pattern recognition

### Real-world Impact
- Kafka tiered storage
- Distributed cache systems
- Production deployment

**Impact**: Bridging the gap between research advances and practical deployment

---

## Thank You!

Breve: FIFO-like Learned Cache — A Lightweight and Scalable Caching Solution

**Key Takeaway**: One algorithm to rule them all — combining the best of learned and heuristic approaches for unified tiered storage caching

