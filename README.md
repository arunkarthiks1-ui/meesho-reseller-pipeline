# Meesho Reseller Performance Analytics & Quality Guardrail Pipeline

An end-to-end, reproducible data analytics, SQL BI, growth guardrail, and agentic monitoring engine built for a reseller e-commerce platform.

---

## 1. Execution Guide (Regenerate Dataset & Run All Parts)

Execute all parts sequentially from the project root using PowerShell or Terminal:

```powershell
# Ingestion & Database Regeneration
python data/generate_dataset.py

# Part 1: SQL BI Queries & CSV Output Export
python part1_sql/run_queries.py

# Part 2: Growth Guardrails & Quality Validation Tests
python part2_engine/test_growth_engine.py

# Part 3: Privacy Anonymization & Alias Masking Tests
python part3_narrative/masking.py

# Part 4: Agentic Workflow & Mock Agent Runner
python part4_agent/test_agent_runner.py

---

## 2. Zero API Keys Guarantee

**Zero API keys or external services are required.** This entire pipeline executes 100% locally using standard Python libraries, SQLite, dynamic string interpolation templates, and offline validation fixtures. It operates cleanly without network dependencies, paid models, or environment variables.

---

## 3. Workflow Pattern Mapping

Each part of this repository directly mirrors a production architectural pattern:

* **Part 1 → Part 2 (SQL BI to Guardrails Engine)**: Mirrors the **"Compute real numbers via SQL first, then hand off"** order of operations. Raw transactions are aggregated deterministically in SQLite before passing sanitized metrics into Python growth functions.
* **Part 2 (Growth Engine & Validation)**: Mirrors the **"Deterministic Input Guardrail"** pattern. Raw CSV feeds are checked for negative numbers, missing categories, and corrupted floats prior to metric processing.
* **Part 3 (Narrative & Anonymization)**: Mirrors the **"Privacy-Preserving Reporting"** pattern. Raw reseller names and IDs are masked with systematic aliases (`RS019` → `ALIAS-19`) before drafting updates.
* **Part 4 (Agentic Workflow & Mock Runner)**: Mirrors an **"Intake → Summary → Report Draft → Validate"** human-in-the-loop reporting flow. It ingests monthly feeds, validates data integrity, computes MoM variance, caps drafts at 3 to prevent notification flooding, and holds all outputs for approval.

---

## 4. Repository Structure Checklist

```text
meesho-reseller-pipeline/
├── data/
│   ├── generate_dataset.py
│   ├── resellers.csv
│   ├── orders.csv
│   └── meesho_reseller.db
├── part1_sql/
│   ├── run_queries.py
│   └── output/
│       ├── monthly_category_revenue.csv
│       ├── region_revenue.csv
│       ├── top_resellers.csv
│       ├── zero_order_resellers.csv
│       ├── zero_order_count_demo.csv
│       └── june_delivered_aov.csv
├── part2_engine/
│   ├── growth_engine.py
│   ├── test_growth_engine.py
│   └── fixtures/
│       ├── april_feed.csv
│       ├── corrupted_feed.csv
│       └── monthly_category_revenue.csv
├── part3_narrative/
│   ├── prompt_pack.md
│   ├── narrative_report.md
│   └── masking.py
├── part4_agent/
│   ├── agent_spec.md
│   ├── mock_agent_runner.py
│   └── test_agent_runner.py
└── README.md
