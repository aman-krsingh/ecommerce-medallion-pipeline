# Databricks notebook source
# DBTITLE 1,Cell 1
storage_account = "amanretailstorage"
account_key = dbutils.secrets.get(scope="cloud-scope", key="storage-key")


# COMMAND ----------


spark.conf.set(
    f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",
    account_key
)

# COMMAND ----------

#Read from Bronze Delta
df_bronze = spark.read\
    .format("delta")\
        .load(f"abfss://bronze@{storage_account}.dfs.core.windows.net/delta/online_retail")

# COMMAND ----------

#  Profiling

print("=== Shape ===")
print(f"Rows: {df_bronze.count()}, Columns: {len(df_bronze.columns)}")

# COMMAND ----------

#Schema
df_bronze.printSchema()

# COMMAND ----------

#sample data

df_bronze.show(5, truncate = False)

# COMMAND ----------

#Null couunt per columun

from pyspark.sql.functions import col, sum as _sum
df_bronze.select([
    _sum(col(c).isNull().cast("int")).alias(c)
    for c in df_bronze.columns
]).show()

# COMMAND ----------

#Investigation 1: need to find the chraestics of rows having null customer id.

df_bronze.filter(col("customer_ID").isNull()).show(10, truncate = False)

# COMMAND ----------

#investigation 2: need to find negative or zero data in quantify and price columns and need to find any cancellation_invoices.

from pyspark.sql.functions import count, when

df_bronze.select(
    count( when( col("Quantity") <= 0, True ) ).alias("Zero_or_neg_quantity"),

    count( when( col("Price") <= 0, True ) ).alias("Zero_or_neg_price"),
    

    count( when( col("Invoice").startswith("C"), True ) ).alias("cancellation_invoices")

).show()

# COMMAND ----------

#investigation 3: need to check invoice with <=0 is always having C or not at starting.

df_bronze.filter(col("Quantity") <=0) \
    .select("Invoice", "Quantity", "Price", "Customer_ID" )\
        .show(20, truncate=False)


# COMMAND ----------

# Flags

from pyspark.sql.functions import col, when, lit

df_flagged = df_bronze\
     .withColumn(
         "is_cancelled",
         when  (col("Invoice").startswith("C"),lit(True)).otherwise(lit(False))
     )\
         .withColumn(
         "is_guest_order",
         when( col("Customer_ID").isNull() ,lit(True)).otherwise(lit(False))
         )\
             .withColumn(
         "is_Price_anomaly",
         when( col("Price") <= 0 ,lit(True)).otherwise(lit(False))
         )
             
#Checking distribution


df_flagged.groupBy("is_cancelled", "is_guest_order", "is_Price_anomaly")\
    .count()\
        .orderBy("count", ascending = False)\
            .show()

# COMMAND ----------

# As per our investigation and observation we will keep other records and will remove price anamonly as it not relevent for business value. 

# COMMAND ----------

# Data Cleansing
# Fix 1: Customer_ID double → string
# Fix 2: Price anomaly rows excluded
# Fix 3: Duplicates droped (same Invoice + StockCode)

from pyspark.sql.functions import col, when, lit

df_silver = df_flagged\
    .withColumn(
        "CustomerID",
        col("Customer_ID").cast("long").cast("String")
    )\
        .drop("Customer_ID")\
        .filter(col("is_price_anomaly") == False)\
        .withColumn("TotalAmount", col("Quantity") * col("Price") )\
        .dropDuplicates(["Invoice", "StockCode"])

print(f"Silver row count: {df_silver.count()}")
df_silver.printSchema()



# COMMAND ----------

# Write silver table to ADLS

df_silver.write\
    .format("delta")\
    .mode("overwrite")\
    .save(f"abfss://silver@{storage_account}.dfs.core.windows.net/delta/online_retail_clean")

print("Silver Delta table written Sucessfully.")
