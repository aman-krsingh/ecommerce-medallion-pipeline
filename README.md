🛒 E-Commerce Medallion Pipeline

An end-to-end Azure Data Engineering pipeline processing 1M+ rows of online retail transaction data using Medallion Architecture (Bronze → Silver → Gold), orchestrated via Azure Data Factory and built on Databricks + PySpark.


🏗️ Architecture

Raw CSV (ADLS Gen2)
      │
      ▼
┌─────────────┐
│   BRONZE    │  ← ADF Copy Activity: Raw ingestion, Delta format
│  1,067,371  │
│    rows     │
└──────┬──────┘
       │ PySpark transformations
       ▼
┌─────────────┐
│   SILVER    │  ← Data Quality: Flagging, type casting, deduplication
│  1,015,458  │
│    rows     │
└──────┬──────┘
       │ Business aggregations
       ▼
┌─────────────┐
│    GOLD     │  ← Business-ready tables: Revenue, Trends, RFM Segments
│  4 tables   │
└─────────────┘


🛠️ Tech Stack

Show Image
Show Image
Show Image
Show Image
Show Image

LayerTechnologyStorageAzure Data Lake Storage Gen2IngestionAzure Data FactoryProcessingDatabricks + PySparkTable FormatDelta LakeSecretsAzure Key VaultOrchestrationADF Pipeline + Schedule Trigger


📁 Repository Structure

ecommerce-medallion-pipeline/
├── 01_bronze_ingest.py       ← Raw CSV → Delta Lake (Bronze)
├── 02_silver_transform.py    ← Data quality, flagging, cleaning (Silver)
├── 03_gold_aggregate.py      ← Business aggregations + RFM (Gold)
└── README.md


🔄 Pipeline Flow

ADF pipeline pl_ecommerce_medallion chains 4 activities in sequence:

Copy_Raw_to_Bronze → Run_Bronze_Notebook → Run_Silver_Notebook → Run_Gold_Notebook

Scheduled trigger runs daily at 6:00 AM IST.


🧹 Silver Layer — Data Quality Decisions

Real-world cleaning approach — investigate first, then fix:

Issue FoundDecisionReason2,43,007 null Customer IDsFlagged as is_guest_orderGuest checkouts — revenue is valid19,494 "C" prefix invoicesFlagged as is_cancelledReversal entries, not errors6,207 zero/negative price rowsExcludedNo business valueCustomer_ID as double typeCast: double → long → stringAvoid "13085.0" string format4,382 null DescriptionsRetainedStockCode identifies product


📊 Gold Layer — Business Tables

TableDescriptionrevenue_by_countryTotal revenue aggregated by countrymonthly_sales_trendMonth-wise revenue trend (2009–2011)top_productsTop 20 products by total revenuecustomer_rfmRFM segmentation — Champions, Loyal, At Risk, Lost

RFM Segment Distribution

SegmentCustomersChampions2,116Loyal1,499Lost1,144At Risk1,119


🔐 Security

Storage Account keys are managed via Azure Key Vault — no credentials hardcoded in notebooks.

pythonaccount_key = dbutils.secrets.get(scope="cloud-scope", key="storage-key")


📈 Business Outcome


Processes 1M+ rows of retail transaction data into actionable revenue metrics and customer segments across Bronze → Silver → Gold Delta layers using ADF and Databricks — reducing manual data handling to zero via scheduled ADF triggers and PySpark transformation notebooks.




🗂️ Dataset

Online Retail II — UCI Machine Learning Repository

Transactions from a UK-based online retailer (2009–2011)

1,067,371 rows × 8 columns
