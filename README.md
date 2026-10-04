# Meesho Reseller Growth & Alert Intelligence Pipeline

## Project Overview

The **Meesho Reseller Growth & Alert Intelligence Pipeline** is an end-to-end, reproducible analytics and agentic monitoring system built for Meesho's reseller-operations team. 

In e-commerce reseller operations, monitoring tens of thousands of individual resellers and category shifts manually is slow, error-prone, and inconsistent. Category managers need to know immediately which product categories moved significantly month-on-month (MoM), which regions drive revenue, and which top resellers require operational focus — without relying on manual spreadsheet recalculations or risk hallucinated figures from un-guarded AI drafts.

This project converts "significant change" from a vague phrase into a testable, numeric business rule (`abs(MoM) > 8.0%`), enforces strict input data guardrails, masks reseller identities for privacy compliance, and orchestrates an offline, human-in-the-loop monitoring agent.

---

## Zero API Keys & Offline Execution Guarantee

- **Zero Paid or Account-Gated Services Required**: This entire repository runs 100% offline using standard Python standard-library modules and SQLite.
- **Zero API Keys Required**: No OpenAI, Anthropic, or external LLM API keys are needed or required.
- **Zero Network Calls**: All AI narrative generation steps use deterministic, offline template-fill functions.
- **Complete Reproducibility**: The dataset is generated using a fixed seed (`42`), ensuring exact numerical alignment with all acceptance criteria.

---

## Project Structure

```text
Meesho_Capstone/
├── data/
│   ├── generate_dataset.py       # Seeded dataset generator script (Seed = 42)
│   ├── resellers.csv             # Reseller demographic table (24 resellers)
│   ├── orders.csv                # Order transaction table (900 orders across 3 months)
│   └── meesho_reseller.db        # SQLite database containing resellers and orders tables
│
├── part1_sql/
│   ├── queries.sql               # Clean SQL queries for all 5 business questions
│   ├── run_query.py              # Execution script for SQLite queries exporting CSV outputs
│   └── output/
│       ├── monthly_category_revenue.csv    # Q1: Monthly revenue by category (15 rows)
│       ├── region_revenue_orders.csv       # Q2: Region-wise revenue & order totals
│       ├── top_5_resellers.csv             # Q3: Top 5 spend resellers (> INR 50,000)
│       ├── zero_order_resellers.csv        # Q4: Resellers with 0 orders (RS024)
│       ├── count_star_vs_count_order_id.csv# Q4B: Demo of COUNT(*) vs COUNT(order_id)
│       ├── june_delivered_aov.csv          # Q5: June Delivered AOV (INR 1267.69)
│       └── README.md                       # Detailed SQL analysis & COUNT(*) explanation
│
├── part2_engine/
│   ├── growth_engine.py          # Core engine: mom_growth, is_flagged, validate_feed
│   ├── test_growth_engine.py     # Unit test suite verifying MoM rules & validation
│   └── fixtures/
│       ├── corrupted_feed.csv              # Corrupted feed fixture for guardrail test
│       └── monthly_category_revenue.csv    # Validated Part 1 revenue feed fixture
│
├── part3_narrative/
│   ├── prompt_pack.md            # Reusable 4-part prompt template & validation checklist
│   ├── narrative_report.md       # Worked narratives, self-scores & chart choice justifications
│   ├── masking.py                # PII protection: alias_for & assert_no_raw_names_leak
│   └── test_masking.py           # Unit tests for PII masking policy
│
├── part4_agent/
│   ├── agent_spec.md             # Complete specification of 5 core agent components
│   └── mock_agent_runner.py      # Executable monitoring agent runner (Scenarios 1, 2, 3)
│
└── README.md                     # Comprehensive project documentation (this file)
```

---

## Step-by-Step Pipeline Execution Guide

To run the complete pipeline from scratch, execute the following commands in order from the project root directory:

### Step 1: Regenerate the Seeded Dataset
Generates `data/resellers.csv` (24 rows), `data/orders.csv` (900 rows), and `data/meesho_reseller.db`.
```bash
python data/generate_dataset.py
```

### Step 2: Execute SQL Business Queries
Runs `part1_sql/run_query.py` against `data/meesho_reseller.db` and updates all CSV files under `part1_sql/output/`.
```bash
python part1_sql/run_query.py
```

### Step 3: Run Part 2 Growth Engine Tests
Executes unit tests verifying MoM calculations, exact-boundary handling (`8.0%`), and feed guardrails.
```bash
python part2_engine/test_growth_engine.py
```

### Step 4: Run Part 3 Narrative & Masking Tests
Executes unit tests verifying PII masking (`alias_for`) and leak prevention (`assert_no_raw_names_leak`).
```bash
python part3_narrative/test_masking.py
```

### Step 5: Run Part 4 Monitoring Agent Runner
Executes the mock agent runner across May (April → May), June (May → June), and Corrupted Feed scenarios.
```bash
python part4_agent/mock_agent_runner.py
```

---

## Pipeline Data Flow & Connection between Parts

The pipeline operates as a single connected system:

```text
[data/generate_dataset.py]
         │
         ▼
[data/meesho_reseller.db]
         │
         ▼ (Part 1 SQL Queries)
[part1_sql/output/monthly_category_revenue.csv]
         │
         ▼ (Part 2 Guardrail & Engine)
[part2_engine/growth_engine.py] ─── (Validates feed, computes MoM %, flags > 8% shifts)
         │
         ├───► [part3_narrative/prompt_pack.md] ── (Fills template with exact numbers)
         │
         ▼
[part4_agent/mock_agent_runner.py] ─── (Orchestrates Intake -> Rank -> Draft -> Suppress -> Hold)
```

1. **Part 1 → Part 2**: SQL queries aggregate raw order transactions into `part1_sql/output/monthly_category_revenue.csv`. This CSV is passed directly as input to Part 2's validation and growth engine.
2. **Part 2 → Part 3**: `growth_engine.py` provides verified revenue figures, MoM percentages, and flagged statuses. Part 3's prompt pack consumes these exact values without inventing figures.
3. **Part 2 & Part 3 → Part 4**: The mock agent runner imports `growth_engine.py` unmodified, executes `validate_feed`, computes growth via `mom_growth`, classifies via `is_flagged`, sorts flagged items by magnitude, drafts top-3 stakeholder updates using Part 3's template, suppresses excess alerts beyond the top 3, and holds all drafts for human approval.

---

## Mapping Parts to System Workflow Patterns

Each Part implements a standard industry analytics and agentic software pattern:

- **Part 1 → Part 2**: Mirrors the **"Compute real numbers via SQL first, then hand off"** pattern. Raw transactions are processed in the database layer before passing clean metrics to application logic.
- **Part 2**: Mirrors the **"Input Validation Guardrails & Deterministic Business Rules"** pattern. Data quality is verified before computation, and ambiguous terms like "significant change" are replaced with strict numeric thresholds (`8.0%`).
- **Part 3**: Mirrors the **"Template-Filled AI Narrative & Privacy Protection"** pattern. Stakeholder reports use structured Context → Insight → Implication framing and enforce PII masking for external communication.
- **Part 4**: Mirrors the **"Intake → Validate → Calculate → Rank → Draft → Suppress → Hold for Approval"** agentic reporting flow pattern. Demonstrates guarded automation where alerts are ranked, capped to prevent notification fatigue, and held behind a human feedback checkpoint.

---

## Python Standard Library Documentation Referenced

As permitted under academic integrity guidelines, the following official Python standard library documentation topics were referenced:

1. **`sqlite3`**: Database connection management, table creation DDL, parameterized query execution (`executemany`), cursor navigation, and type conversions.
2. **`csv`**: `DictWriter` and `DictReader` for structured CSV I/O, `csv.writer` for query export, header handling, and line number tracking (`reader.line_num`).
3. **`os` & `pathlib`**: File path normalization (`os.path.abspath`), cross-platform path joining, parent directory navigation (`Path.resolve().parent`), and directory listing.
4. **`json`**: Structured object serialization and formatted printing (`json.dumps(obj, indent=2)`).
5. **`random`**: Pseudorandom number generation using seeded instances (`random.Random(42)`), weighted sampling (`random.choices`), floating-point range sampling (`random.uniform`), and integer selection (`random.randint`).
6. **`sys`**: Module search path manipulation (`sys.path.insert`) for cross-directory imports.

---

## Acceptance Criteria & Numerical Summary

### Part 1 — SQL Business Query Engine
- **Grand Total Revenue**: **INR 1,262,066.92** across 900 orders.
- **Regional Revenue**:
  - **North**: INR 337,125.46 (231 orders)
  - **West**: INR 333,106.33 (232 orders)
  - **South**: INR 316,736.68 (216 orders)
  - **East**: INR 275,098.45 (221 orders)
- **Top 5 Spend Resellers**:
  1. `RS019` ("Mumbai Reseller 1"): INR 75,295.09
  2. `RS022` ("Mumbai Reseller 4"): INR 73,882.33
  3. `RS012` ("Hyderabad Reseller 6"): INR 69,936.46
  4. `RS006` ("Lucknow Reseller 6"): INR 64,238.97
  5. `RS005` ("Jaipur Reseller 5"): INR 61,825.02
- **Zero-Order Reseller**: `RS024` ("Ahmedabad Reseller 6", West region).
- **LEFT JOIN COUNT(*) Demonstration**: For `RS024`, `COUNT(*) = 1` while `COUNT(order_id) = 0`.
- **June Delivered AOV**: **INR 1,267.69**.

### Part 2 — Python Guardrail & Growth Engine
- **Corrupted Feed Guardrail**: `validate_feed("part2_engine/fixtures/corrupted_feed.csv")` returns `False` and exactly 3 error strings:
  1. `"line 3: negative revenue (-4200.0) for category=Western Wear"`
  2. `"line 4: missing category (month=July)"`
  3. `"line 6: missing revenue (category=Home & Kitchen)"`
- **May vs. April MoM**: All 5 categories flagged:
  - Ethnic Wear: **+77.1%** (flagged)
  - Western Wear: **-23.6%** (flagged)
  - Kids Wear: **-23.48%** (flagged)
  - Home & Kitchen: **-9.25%** (flagged)
  - Beauty & Personal Care: **-12.75%** (flagged)
- **June vs. May MoM**: 4 of 5 categories flagged:
  - Ethnic Wear: **-58.74%** (flagged)
  - Home & Kitchen: **+42.59%** (flagged)
  - Kids Wear: **+23.9%** (flagged)
  - Western Wear: **+11.97%** (flagged)
  - Beauty & Personal Care: **+5.67%** (not flagged)
- **Exact Boundary Case**: Previous = 100000, Current = 108000 yields MoM = `8.0%` and status `"escalate_exact_boundary"`.

### Part 3 — AI Narrative & Masking Policy
- **Masking Verification**: `alias_for("RS019") == "ALIAS-19"`. `assert_no_raw_names_leak` returns `True` for masked narrative and `False` if raw reseller name ("Mumbai Reseller 1") is present.
- **Chart Choice Justifications**: Written justifications using univariate/bivariate framework, zero-based y-axes, avoiding 3D, and omitting unnecessary legends.

### Part 4 — Agent Specification & Mock Runner
- **May Scenario**: Produces `validation_status = "valid"`, 3 drafted flagged entries in order (Ethnic Wear +77.1%, Western Wear -23.6%, Kids Wear -23.48%), 2 suppressed entries (Beauty & Personal Care, Home & Kitchen), and `action_taken = "drafted_and_held_for_approval"`.
- **June Scenario**: Produces `validation_status = "valid"`, 3 drafted flagged entries in order (Ethnic Wear -58.74%, Home & Kitchen +42.59%, Kids Wear +23.9%), 1 suppressed entry (Western Wear +11.97%), Beauty & Personal Care excluded, and `action_taken = "drafted_and_held_for_approval"`.
- **Corrupted Scenario**: Produces `validation_status = "invalid"`, `action_taken = "hard_stop"`, and surfaces the 3 exact validation errors.