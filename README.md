<p align="center">
  <img src="images/banner.png" width="100%">
</p>

<h1 align="center">E-Commerce Medallion Pipeline</h1>

<p align="center">
Azure Data Factory • Databricks • PySpark • Delta Lake • ADLS Gen2
</p>

<p align="center">

![Azure](https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white)
![PySpark](https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Delta Lake](https://img.shields.io/badge/Delta_Lake-003366?style=for-the-badge)
![ADLS Gen2](https://img.shields.io/badge/ADLS_Gen2-0089D6?style=for-the-badge)
![ADF](https://img.shields.io/badge/Azure_Data_Factory-0078D4?style=for-the-badge)

</p>

---

## 🚀 Overview

A modern Azure Data Engineering project implementing the Medallion Architecture (Bronze → Silver → Gold) to process over **1 million retail transactions** and deliver business-ready analytics.

### Key Achievements

- ✅ Processed **1,067,371** retail transactions
- ✅ Built Bronze → Silver → Gold architecture
- ✅ Automated execution using Azure Data Factory
- ✅ Implemented data quality framework
- ✅ Generated business analytics tables
- ✅ Performed customer RFM segmentation
- ✅ Secured secrets using Azure Key Vault

---

## 📊 Project Snapshot

| Metric | Value |
|----------|----------|
| Dataset Size | 1,067,371 Rows |
| Architecture | Bronze → Silver → Gold |
| Processing Engine | Databricks + PySpark |
| Storage | ADLS Gen2 |
| Orchestration | Azure Data Factory |
| Storage Format | Delta Lake |
| Security | Azure Key Vault |
| Schedule | Daily 6:00 AM IST |

---

## 🏗️ Architecture

<p align="center">
  <img src="images/ecommerce_medallion_architecture.png" width="100%">
</p>

---

## ⚙️ Tech Stack

| Layer | Technology |
|---------|---------|
| Storage | Azure Data Lake Storage Gen2 |
| Ingestion | Azure Data Factory |
| Processing | Azure Databricks |
| Transformation | PySpark |
| Table Format | Delta Lake |
| Security | Azure Key Vault |
| Scheduling | ADF Trigger |

---

## 🔄 Pipeline Execution

<p align="center">
  <img src="images/adf_pipeline_success.PNG" width="100%">
</p>

### Workflow

```text
Raw CSV
   ↓
Bronze Layer
   ↓
Silver Layer
   ↓
Gold Layer
```

### Pipeline Activities

```text
Copy_Raw_to_Bronze
        ↓
Run_Bronze_Notebook
        ↓
Run_Silver_Notebook
        ↓
Run_Gold_Notebook
```

---

## 🧹 Data Quality Decisions

| Issue Found | Resolution | Business Reason |
|-------------|------------|-----------------|
| 243,007 Null Customer IDs | Flagged as Guest Orders | Revenue remains valid |
| 19,494 Cancellation Invoices | Added is_cancelled flag | Preserve transaction history |
| Negative / Zero Prices | Removed | Invalid revenue values |
| Customer ID Formatting Issues | Standardized | Consistent joins |
| Missing Product Descriptions | Retained | StockCode identifies product |

---

## 📈 Gold Layer Outputs

### 🌍 Revenue by Country

<p align="center">
  <img src="images/revenue_by_country.png" width="100%">
</p>

### 👥 Customer RFM Segmentation

<p align="center">
  <img src="images/customer_rfm.png" width="100%">
</p>

---

## 🎯 Business Outcomes

The Gold Layer delivers business-ready datasets for reporting, analytics, and customer intelligence.

### Generated Tables

| Table | Description |
|---------|---------|
| revenue_by_country | Country-wise revenue analysis |
| monthly_sales_trend | Monthly sales performance |
| top_products | Top-performing products |
| customer_rfm | Customer segmentation |

### RFM Segment Distribution

| Segment | Customers |
|---------|-----------|
| Champions | 2,116 |
| Loyal | 1,499 |
| At Risk | 1,119 |
| Lost | 1,144 |

---

## 🔐 Security

- Azure Key Vault for secret management
- No credentials hardcoded in notebooks
- Secure ADLS Gen2 access
- Managed authentication between Azure services

---

## 📁 Repository Structure

```text
ecommerce-medallion-pipeline/
│
├── notebooks/
│   ├── 01_bronze_ingest.py
│   ├── 02_silver_transform.py
│   └── 03_gold_aggregate.py
│
├── images/
│   ├── banner.png
│   ├── ecommerce_medallion_architecture.png
│   ├── adf_pipeline_success.png
│   ├── revenue_by_country.png
│   └── customer_rfm.png
│
└── README.md
```

---

## 🚀 How To Run

1. Upload source dataset to ADLS Gen2
2. Configure Azure Key Vault secrets
3. Import notebooks into Databricks
4. Create Bronze, Silver, and Gold storage paths
5. Configure Azure Data Factory pipeline
6. Add schedule trigger
7. Execute pipeline

---

## 📊 Dataset

**Online Retail II Dataset**

- Source: UCI Machine Learning Repository
- 1,067,371 Transactions
- UK-based Online Retail Business
- Period: 2009–2011
- Transaction-Level Data

---

## ⭐ Features

- Azure Data Factory Orchestration
- Azure Databricks Processing
- PySpark Transformations
- Delta Lake Storage
- Medallion Architecture
- Data Quality Framework
- Customer RFM Segmentation
- Automated Daily Execution
- Business Analytics Tables

---

## 👨‍💻 Author

### Aman Singh

Data Engineering | Azure | Databricks | PySpark | SQL | Delta Lake

---

<p align="center">
⭐ If you found this project useful, consider giving it a star.
</p>