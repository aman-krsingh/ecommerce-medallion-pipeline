# Databricks notebook source
storage_account = "amanretailstorage"
account_key = dbutils.secrets.get(scope="cloud-scope", key="storage-key")
spark.conf.set(
    f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",
    account_key
)

# COMMAND ----------

#Read from silver Delta
df_silver = spark.read\
    .format("delta")\
        .load(f"abfss://silver@{storage_account}.dfs.core.windows.net/delta/online_retail_clean")

# COMMAND ----------

from pyspark.sql.functions import col, sum as _sum, month, year, date_format, round as _round

# Exclude Cancelled order

df_valid = df_silver.filter( col("is_cancelled") == False )

# COMMAND ----------

df_silver.display()

# COMMAND ----------

# Gold Table 1: Revenue by Country

gold_revenue_country = df_valid\
    .groupBy("Country")\
    .agg(_round(_sum("TotalAmount"), 2).alias("total_revenue") )\
    .orderBy("total_revenue", ascending = False) 

# COMMAND ----------

gold_revenue_country.display()

# COMMAND ----------

# Gold Table 2: Monthly Sales Trend

gold_monthly_trend = df_valid \
    .withColumn("year_month", date_format( col("InvoiceDate"), "yyyy-MM" ))\
    .groupBy("year_month")\
    .agg(_round(_sum("TotalAmount") , 2).alias("monthly_revenue"))\
    .orderBy("year_month")

# COMMAND ----------

gold_monthly_trend.display()

# COMMAND ----------

# Gold Table 3: Top 20 Products by Revenue

gold_top_products = df_valid\
    .groupBy("StockCode", "Description")\
    .agg(_round(_sum("TotalAmount"), 2).alias("total_revenue"))\
    .orderBy("total_revenue", ascending = False)\
    .limit(20)

# COMMAND ----------

gold_top_products.display()

# COMMAND ----------

print("=== Revenue by Country (Top 5) ===")
gold_revenue_country.show(5, truncate=False)

print("=== Monthly Trend (Top 5) ===")
gold_monthly_trend.show(5)

print("=== Top 5 Products ===")
gold_top_products.show(5)

# COMMAND ----------

# MAGIC %md
# MAGIC RFM (Recency, Frequency, Monetary)

# COMMAND ----------

# Finding refrence date

from pyspark.sql.functions import max as _max

df_valid.select(_max("InvoiceDate")).show()

# COMMAND ----------

from pyspark.sql.functions import max as _max, count, sum as _sum, datediff, lit, to_timestamp

reference_date = lit("2011-12-09").cast("timestamp")

df_rfm_raw = df_valid\
    .filter( col("CustomerID").isNotNull() )\
    .groupBy("CustomerID")\
    .agg(
        datediff(reference_date, _max("InvoiceDate")).alias("Recency"),
        count("Invoice").alias("Frequency"),
        _sum("TotalAmount").alias("Monetary")
    )

df_rfm_raw.show(5)

# COMMAND ----------

#Givinmg score

from pyspark.sql.functions import percentile_approx, when, round as _round

# round the Monetary 

df_rfm_raw = df_rfm_raw.withColumn("Monetary", _round( col("Monetary"), 2))

#Quartiles

r_tiles = df_rfm_raw.approxQuantile("Recency", [0.25, 0.50, 0.75], 0.01)

f_tiles = df_rfm_raw.approxQuantile("Frequency", [0.25, 0.50, 0.75], 0.01)

m_tiles = df_rfm_raw.approxQuantile("Monetary", [0.25, 0.50, 0.75], 0.01)

# COMMAND ----------

print(f"Recency quartiles: {r_tiles}")
print(f"Frequency quartiles: {f_tiles}")
print(f"Monetary quartiles: {m_tiles}")

# COMMAND ----------

# Allocating score to each customer

df_rfm_scored = df_rfm_raw\
    .withColumn("R_score",
    when( col("Recency") <= 26, 4)
    .when( col("Recency") <= 94, 3)
    .when( col("Recency") <= 376, 2)
    .otherwise(1)
    )\
    .withColumn("F_score",
    when( col("Frequency") <= 21, 1)
    .when( col("Frequency") <= 51, 2)
    .when( col("Frequency") <= 131, 4)
    .otherwise(4)
    )\
    .withColumn("M_score",
    when( col("Monetary") <= 343.62, 1)
    .when( col("Monetary") <= 848.81, 2)
    .when( col("Monetary") <= 2180.76, 3)
    .otherwise(4)
    )\
    .withColumn("RFM_Score",
                col("R_score") + col("F_score")+ col("M_score")            
    )

# COMMAND ----------

df_rfm_scored.show(5)

# COMMAND ----------

#table 4 rfm segmentation
#Assigning segment to customer / / categorizing customers based on RFM

df_rfm_final = df_rfm_scored\
    .withColumn("Segment",
             when(col("RFM_Score") >= 10, "Champion")
             .when(col("RFM_Score") >= 7, "Loyal")
             .when(col("RFM_Score") >= 5, "At Risk") 
             .otherwise("Lost")  
    )

# COMMAND ----------

#segment dristribution

df_rfm_final.groupBy("Segment")\
    .count()\
    .orderBy("count", ascending=False)\
    .display()

# COMMAND ----------

# writimg tables to gold table ADLS
gold_path = f"abfss://gold@{storage_account}.dfs.core.windows.net/delta"

# COMMAND ----------

# Table 1: Revenue by Country

gold_revenue_country.write\
    .format("delta")\
    .mode("overwrite")\
    .save(f"{gold_path}/revenue_by_country")

# COMMAND ----------

# Table 2: Monthly Sales Trend

gold_monthly_trend.write\
    .format("delta")\
    .mode("overwrite")\
    .save(f"{gold_path}/monthly_sales_trend")

# COMMAND ----------

# Table 3: Top 20 Products

gold_top_products.write\
    .format("delta")\
    .mode("overwrite")\
    .save(f"{gold_path}/top_products")

# COMMAND ----------

# Table 4: RFM Segmentation

df_rfm_final.write\
    .format("delta")\
    .mode("overwrite")\
    .save(f"{gold_path}/customer_rfm")


# COMMAND ----------

print("All Gold tables written successfully!")
