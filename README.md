# Meesho Reseller Growth & Alert Intelligence Pipeline

## Project Overview

This project implements a four-part offline intelligence workflow for monitoring Meesho reseller and category revenue performance.

The pipeline follows this order:

1. Part 1 — Compute reliable revenue metrics using SQL.
2. Part 2 — Validate the feed and calculate month-on-month growth and alert status.
3. Part 3 — Convert validated results into a masked stakeholder narrative.
4. Part 4 — Run a monitoring-agent workflow that validates inputs, computes growth, drafts messages, suppresses excess alerts, and holds all drafts for human approval.

The complete pipeline runs locally with **zero API keys, zero external network calls, and no email service**.

---

## Project Structure

```text
Meesho_Capstone/
├── data/
│   ├── generate_dataset.py
│   ├── resellers.csv
│   ├── orders.csv
│   └── meesho_reseller.db
│
├── part1_sql/
│   ├── queries.sql
│   ├── run_query.py
│   └── output/
│       ├── monthly_category_revenue.csv
│       ├── region_revenue_orders.csv
│       ├── top_5_resellers.csv
│       ├── zero_order_resellers.csv
│       ├── count_star_vs_count_order_id.csv
│       └── june_delivered_aov.csv
│
├── part2_engine/
│   ├── growth_engine.py
│   ├── test_growth_engine.py
│   └── fixtures/
│       ├── corrupted_feed.csv
│       └── monthly_category_revenue.csv
│
├── part3_narrative/
│   ├── prompt_pack.md
│   ├── narrative_report.md
│   ├── masking.py
│   └── test_masking.py
│
├── part4_agent/
│   ├── agent_spec.md
│   └── mock_agent_runner.py
│
└── README.md