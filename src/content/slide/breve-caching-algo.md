---
title: "Breve: FIFO-like Learned Cache"
description: "A comprehensive study of the Breve caching algorithm"
publishDate: "06 May 2025"
theme: ["default", "/styles/breve-theme.css"]
tags: ["cache", "machine-learning", "storage", "algorithm"]
draft: false
---

<div class="title-slide">
<div class="main-title">Breve: FIFO-like Learned Cache</div>
<div class="subtitle">A Lightweight and Scalable Caching Solution</div>
</div>

---

## Outline

<div class="columns">
<div class="column">

<div class="agenda-item">
<h4>1. Introduction</h4>
<ul>
<li>Background & Motivation</li>
<li>Problem Statement</li>
<li>Key Insights</li>
</ul>
</div>

<div class="agenda-item">
<h4>2. Related Work</h4>
<ul>
<li>Algorithm Evolution</li>
<li>Efficiency Strategies</li>
<li>Lightweight Design</li>
</ul>
</div>

</div>
<div class="column">

<div class="agenda-item">
<h4>3. Breve Algorithm</h4>
<ul>
<li>System Overview</li>
<li>UnoSketch & UnoLearner</li>
<li>2-level FIFO Structure</li>
</ul>
</div>

<div class="agenda-item">
<h4>4. Evaluation & Results</h4>
<ul>
<li>Memory & Performance</li>
<li>Hit Ratio Analysis</li>
<li>Write Reduction</li>
</ul>
</div>

</div>
</div>

---

# 1. Introduction

<div class="section-outline">
<div class="outline-item">Background & Motivation</div>
<div class="outline-item">Problem Statement</div>
<div class="outline-item">Key Insights</div>
</div>

---

## Background & Motivation

<div class="problem-statement">
<strong>Challenge</strong>: Tiered storage systems require different caching algorithms for different media types
</div>

<div class="two-column">
<div class="column-left">

### Current Approach

- **Memory Tier**: LRU-based
  - Alluxio, GridGain
- **Flash Tier**: FIFO-based
  - CacheLib, Colossus

### Pain Points

- Multiple algorithms to maintain
- Poor scalability with locks
- Complex integration overhead

</div>
<div class="column-right">

### Learned Caching Promise

- **Object-level**: LRB
- **Expert-based**: LeCaR, CACHEUS
- **Distribution-based**: LHD

### Reality Check

- Performance overhead
- Implementation complexity
- Inadequate admission control

</div>
</div>

---

## Problem Statement

<div class="problem-box">
<strong>Core Challenge</strong>: We need a unified caching paradigm that addresses:

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 20px;">
<div style="text-align: center;">
<h4 style="color: var(--accent-danger); margin: 0;">Scalability</h4>
<p style="font-size: 0.9em; margin: 5px 0;">Poor performance at scale</p>
</div>
<div style="text-align: center;">
<h4 style="color: var(--accent-warning); margin: 0;">Complexity</h4>
<p style="font-size: 0.9em; margin: 5px 0;">Difficult implementation</p>
</div>
<div style="text-align: center;">
<h4 style="color: var(--accent-primary); margin: 0;">Admission</h4>
<p style="font-size: 0.9em; margin: 5px 0;">Lack of intelligence</p>
</div>
</div>
</div>

<div class="insight-box">
<strong>Our Vision</strong>: A single learned algorithm that works effectively across all storage tiers
</div>

---

## Key Insights

<div class="insights-grid">
<div class="insight-card">
<h4>Unified Design</h4>
<p>One algorithm for all tiers</p>
</div>

<div class="insight-card">
<h4>Sketch-based</h4>
<p>Efficient feature collection</p>
</div>

<div class="insight-card">
<h4>ML + Heuristics</h4>
<p>Best of both worlds</p>
</div>

<div class="insight-card">
<h4>FIFO-like</h4>
<p>Scalable & flash-friendly</p>
</div>
</div>

<div class="center-image">
<img src="/images/breve-caching-algo/typical-object-level.png" alt="Object-Level Learning Approach" style="width: 55%; height: auto;" />
</div>

---

# 2. Related Work

<div class="section-outline">
<div class="outline-item">Algorithm Evolution</div>
<div class="outline-item">Efficiency Strategies</div>
<div class="outline-item">Lightweight Design</div>
</div>

---

## Algorithm Evolution: LRU → FIFO

<div style="display: flex; align-items: center; gap: 30px; margin: 20px 0;">

<div style="flex: 1;">
<div class="comparison-table">

| Type          | Examples      | Scalable | Flash-Friendly |
| :------------ | :------------ | :------- | :------------- |
| **LRU-like**  | LRU, ARC, LFU | ❌       | ❌             |
| **FIFO-like** | CLOCK, S3FIFO | ✅       | ✅             |

</div>
</div>

<div style="flex: 1;">
<div class="key-benefits">

### Why FIFO-like?

<div class="benefit-item">
<strong>Lock-free</strong> → Better scalability
</div>

<div class="benefit-item">
<strong>Sequential</strong> → Disk-friendly
</div>

<div class="benefit-item">
<strong>Consistent</strong> → Stable throughput
</div>

</div>
</div>

</div>

---

## Efficiency Strategies

<div class="center-image">
<img src="/images/breve-caching-algo/LP-QD.png" alt="Lazy Promotion & Quick Demotion" style="width: 60%; height: auto;" />
</div>

<div class="strategy-grid">
<div class="strategy-card">
<h4>Lazy Promotion</h4>
<p>Promote only when about to evict</p>
<p><em>→ Reduces metadata overhead</em></p>
</div>

<div class="strategy-card">
<h4>Quick Demotion</h4>
<p>Fast removal of low-value items</p>
<p><em>→ Lowers opportunity cost</em></p>
</div>
</div>

---

## Frequency vs. Recency

<div class="analysis-text">
<strong>Real-world workloads show diverse access patterns requiring both frequency and recency</strong>
</div>

<div class="image-comparison">
<div class="image-item">
<img src="/images/breve-caching-algo/wiki-2019-access.png" alt="Wiki Access Patterns" style="width: 100%; height: auto;" />
<em>Wikipedia: Mixed patterns</em>
</div>

<div class="image-item">
<img src="/images/breve-caching-algo/meta_rprn_reuse_heatmap_vt.png" alt="Meta Reuse Heatmap" style="width: 100%; height: auto;" />
<em>Meta: Reuse distance heatmap</em>
</div>
</div>

---

## Sketch-based Lightweight Design

<div style="display: flex; align-items: center; gap: 30px; margin: 20px 0;">

<div style="flex: 1;">
<div class="definition-box">
<strong>Sketch</strong>: Space-efficient data structure trading accuracy for space
</div>

<div class="evolution-chain">
<strong>Evolution</strong>: LFU → TinyLFU → W-TinyLFU → <strong>Breve</strong>
</div>
</div>

<div style="flex: 1;">
<img src="/images/breve-caching-algo/moka-tiny-lfu.png" alt="TinyLFU Architecture" style="width: 100%; height: auto;" />
</div>

</div>

---

# 3. Breve Algorithm

<div class="section-outline">
<div class="outline-item">System Overview</div>
<div class="outline-item">UnoSketch & UnoLearner</div>
<div class="outline-item">2-level FIFO Structure</div>
</div>

---

## System Overview

<div class="system-components">
<div class="component-card">
<h4>UnoSketch</h4>
<p>Frequency & recency tracking</p>
</div>

<div class="component-card">
<h4>UnoLearner</h4>
<p>ML-based admission control</p>
</div>

<div class="component-card">
<h4>2-level FIFO</h4>
<p>Scalable cache structure</p>
</div>
</div>

<div class="center-image">
<img src="/images/breve-caching-algo/breve-overview.png" alt="Breve System Architecture" style="width: 75%; height: auto;" />
</div>

---

## UnoSketch: Efficient Tracking

<div style="display: flex; align-items: flex-start; gap: 30px; margin: 20px 0;">

<div style="flex: 1;">
<div class="design-principles">

### Design Principles

- **Lightweight**: Two Count-Min Sketches
- **Write-based**: Track misses, not hits
- **Quick decay**: Space & accuracy optimization

### Algorithm Details

- **Miss Frequency**: Decay by 0.8× when doubled
- **Write Recency**: Bit-shift on window limit

</div>
</div>

<div style="flex: 1;">
<img src="/images/breve-caching-algo/unosketch-overview.png" alt="UnoSketch Design" style="width: 100%; height: auto;" />
</div>

</div>

<div class="formula-box">
<strong>Write Recency Formula</strong>:
<code>write_recency = (window_limit + window_clock) / actual_write_frequency</code>
</div>

---

## UnoLearner: ML-based Admission

<div class="center-image">
<img src="/images/breve-caching-algo/unolearner-workflow.png" alt="UnoLearner Workflow" style="width: 80%; height: auto;" />
</div>

<div style="display: flex; gap: 20px; margin: 20px 0;">

<div class="formula-box" style="flex: 1;">
<strong>Score Calculation</strong>:
<code>score = bias + w_freq × miss_freq + w_rec × (write_rec / scale)</code>
</div>

<div class="formula-box" style="flex: 1;">
<strong>Online Learning</strong>:
<code>w_freq ← w_freq + η × error × miss_freq</code>
<code>w_rec ← w_rec + η × error × write_rec</code>
</div>

</div>

---

## 2-level FIFO Structure

<div class="center-image">
<img src="/images/breve-caching-algo/2-level-fifo.png" alt="2-level FIFO Architecture" style="width: 85%; height: auto;" />
</div>

<div class="level-details">
<div class="level-card">
<h4>Small Cache (10%)</h4>
<ul>
<li>Admission buffer</li>
<li>One-hit wonder filter</li>
<li>Quick demotion</li>
</ul>
</div>

<div class="level-card">
<h4>Main Cache (90%)</h4>
<ul>
<li>2-bit CLOCK variant</li>
<li>Lazy promotion</li>
<li>ML-guided admission</li>
</ul>
</div>
</div>

---

## Admission Strategy

<div class="center-image">
<img src="/images/breve-caching-algo/breve-admit.png" alt="Admission Decision Flow" style="width: 85%; height: auto;" />
</div>

<div class="decision-criteria">
<h4>Decision Logic</h4>
<ol>
<li><strong>Scan Resistance</strong>: Access count > 1</li>
<li><strong>ML Score</strong>: Learned threshold > 0</li>
<li><strong>Combined Features</strong>: Frequency + recency</li>
</ol>
</div>

---

# 4. Evaluation

<div class="section-outline">
<div class="outline-item">Memory & Performance</div>
<div class="outline-item">Hit Ratio Analysis</div>
<div class="outline-item">Write Reduction</div>
</div>

---

## Memory Efficiency

<div style="display: flex; align-items: center; gap: 30px; margin: 20px 0;">

<div style="flex: 1;">
<div class="efficiency-metrics">

### Memory Savings

| Cache Size  | vs Moka    | vs Moka (Compact) |
| :---------- | :--------- | :---------------- |
| 1K objects  | **-40.7%** | **-75.0%**        |
| 10K objects | **-18.4%** | **-67.0%**        |

</div>

<div class="efficiency-note">
<strong>Result</strong>: Significant memory savings while maintaining performance
</div>
</div>

<div style="flex: 1;">
<img src="/images/breve-caching-algo/memory-usage.png" alt="Memory Usage Comparison" style="width: 100%; height: auto;" />
</div>

</div>

---

## Scalability Performance

<div class="performance-summary">
<strong>Breve achieves ~2× better throughput than Moka with similar hit ratios</strong>
</div>

<div class="performance-comparison">
<div class="perf-item">
<img src="/images/breve-caching-algo/read-only.png" alt="Read-Only Performance" style="width: 100%; height: auto;" />
<em>Read-Only Workload</em>
</div>

<div class="perf-item">
<img src="/images/breve-caching-algo/read-write.png" alt="Read-Write Performance" style="width: 100%; height: auto;" />
<em>Mixed Workload (Zipf=1.05)</em>
</div>
</div>

---

## Hit Ratio Analysis

<div style="display: flex; align-items: center; gap: 30px; margin: 20px 0;">

<div style="flex: 1;">
<img src="/images/breve-caching-algo/zipf-workload.png" alt="Zipf Workload Results" style="width: 100%; height: auto;" />
</div>

<div style="flex: 1;">
<div class="improvement-metrics">

### Performance Gains

| Workload | vs LRU      | vs S3FIFO   |
| :------- | :---------- | :---------- |
| S1       | **+6.16%**  | **+5.30%**  |
| S2       | **+11.45%** | **+5.70%**  |
| S3       | **+11.66%** | **+5.77%**  |
| DS1      | **+20.63%** | **+12.72%** |
| SPC1     | **+12.07%** | **+1.28%**  |

</div>

<div class="hit-ratio-summary">
<strong>29/30 test cases better than S3FIFO</strong>
</div>
</div>

</div>

---

## Write Reduction Analysis

<div class="write-reduction-summary">
<strong>Intelligent admission reduces unnecessary writes by up to 58%</strong>
</div>

<div class="reduction-table">

| Workload | Cache Size | Requested  | Actual     | Reduction   |
| :------- | :--------- | :--------- | :--------- | :---------- |
| S1       | 800K       | 1,762,766  | 1,193,533  | **-32.29%** |
| S2       | 800K       | 5,466,459  | 2,575,054  | **-52.89%** |
| S3       | 800K       | 5,207,651  | 2,474,058  | **-52.49%** |
| DS1      | 8M         | 15,863,008 | 12,895,059 | **-18.70%** |
| SPC1     | 2M         | 25,028,988 | 10,393,675 | **-58.47%** |

</div>

<div class="flash-friendly">
<strong>Flash-Friendly</strong>: Up to 82.84% write reduction in low hit-ratio scenarios
</div>

---

# 5. Conclusion

<div class="section-outline">
<div class="outline-item">Key Contributions</div>
<div class="outline-item">Future Directions</div>
</div>

---

## Key Contributions

<div class="contributions-grid">
<div class="contribution-card">
<h4>Unified Tracking</h4>
<p>Single sketch for frequency & recency across all tiers</p>
</div>

<div class="contribution-card">
<h4>Online Learning</h4>
<p>Lightweight perceptron with feedback-based updates</p>
</div>

<div class="contribution-card">
<h4>Scalable Design</h4>
<p>Lock-free FIFO-like architecture for performance</p>
</div>

<div class="contribution-card">
<h4>Smart Admission</h4>
<p>Balanced hit ratio with reduced write operations</p>
</div>
</div>

<div class="contribution-summary">
<strong>A unified learned caching algorithm that works across different storage tiers</strong>
</div>

---

## Future Directions

<div class="future-work">
<div class="future-item">
<h4>Enhanced Models</h4>
<ul>
<li>Object relationship modeling</li>
<li>Advanced ML architectures</li>
<li>Temporal pattern recognition</li>
</ul>
</div>

<div class="future-item">
<h4>Real-world Impact</h4>
<ul>
<li>Kafka tiered storage</li>
<li>Distributed cache systems</li>
<li>Production deployment</li>
</ul>
</div>
</div>

<div class="research-impact">
<strong>Impact</strong>: Bridging the gap between research advances and practical deployment
</div>

---

## Thank You!

<div style="text-align: center; margin: 30px 0;">
<p style="font-size: 1.3em; font-weight: 600; color: var(--accent-primary);">Breve: FIFO-like Learned Cache</p>
<p style="font-size: 1.1em; color: var(--text-muted); font-style: italic;">A Lightweight and Scalable Caching Solution</p>
</div>

<div class="key-takeaway">
<strong>Key Takeaway</strong>: One algorithm to rule them all - combining the best of learned and heuristic approaches for unified tiered storage caching
</div>
