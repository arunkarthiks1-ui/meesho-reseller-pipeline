# Reseller Performance Analytics & Quality Guardrail Pipeline

An end-to-end data analytics and quality engine built for a reseller e-commerce ecosystem. The pipeline automates data generation, SQL relational queries, growth detection guardrails, and executive narrative reporting with data anonymization.

---

## Project Structure

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
│       ├── corrupted_feed.csv
│       └── monthly_category_revenue.csv
├── part3_narrative/
│   ├── prompt_pack.md
│   ├── narrative_report.md
│   └── masking.py
└── README.md