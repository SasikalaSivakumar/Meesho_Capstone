# Meesho Reseller Growth & Alert Intelligence Pipeline

## Project Overview

The **Meesho Reseller Growth & Alert Intelligence Pipeline** is an end-to-end, reproducible analytics and agentic monitoring system built for Meesho's reseller-operations team. 

In e-commerce reseller operations, monitoring tens of thousands of individual resellers and category shifts manually is slow, error-prone, and inconsistent. Category managers need to know immediately which product categories moved significantly month-on-month (MoM), which regions drive revenue, and which top resellers require operational focus — without relying on manual spreadsheet recalculations or risk hallucinated figures from un-guarded AI drafts.

This project converts "significant change" from a vague phrase into a testable, numeric business rule (`abs(MoM) > 8.0%`), enforces strict input data guardrails, masks reseller identities for privacy compliance, and orchestrates an offline, human-in-the-loop monitoring agent.

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

## Python Standard Library Documentation Referenced

As permitted under academic integrity guidelines, the following official Python standard library documentation topics were referenced:

1. **`sqlite3`**: Database connection management, table creation DDL, parameterized query execution (`executemany`), cursor navigation, and type conversions.
2. **`csv`**: `DictWriter` and `DictReader` for structured CSV I/O, `csv.writer` for query export, header handling, and line number tracking (`reader.line_num`).
3. **`os` & `pathlib`**: File path normalization (`os.path.abspath`), cross-platform path joining, parent directory navigation (`Path.resolve().parent`), and directory listing.
4. **`json`**: Structured object serialization and formatted printing (`json.dumps(obj, indent=2)`).
5. **`random`**: Pseudorandom number generation using seeded instances (`random.Random(42)`), weighted sampling (`random.choices`), floating-point range sampling (`random.uniform`), and integer selection (`random.randint`).
6. **`sys`**: Module search path manipulation (`sys.path.insert`) for cross-directory imports.