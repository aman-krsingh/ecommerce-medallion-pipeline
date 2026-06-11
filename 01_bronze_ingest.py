# Databricks notebook source
# MAGIC %md
# MAGIC creating Spark session and linked it with azure storage account.

# COMMAND ----------

from pyspark.sql import SparkSession

# COMMAND ----------

storage_account = "amanretailstorage"
account_key = dbutils.secrets.get(scope="cloud-scope", key="storage-key")


# COMMAND ----------


# connection using key

spark.conf.set(
    f"fs.azure.account.key.{storage_account}.dfs.core.windows.net",
    account_key
)

# COMMAND ----------

# Read raw data from bronze layer

df_raw = spark.read\
    .option("header", True)\
        .option("inferSchema", True)\
            .csv(f"abfss://bronze@{storage_account}.dfs.core.windows.net/online_retail/online_retail.csv")



# COMMAND ----------

# checked data file and Schema

print(f"Row count: {df_raw.count()}")
df_raw.printSchema()

# COMMAND ----------

# DBTITLE 1,Cell 7
# Save data as Delta table to Bronze layer
# we fix collomn name because space in collomn name is not allowed by delta table. 

df_raw.withColumnRenamed("Customer ID", "Customer_ID")\
    .write\
    .format("delta")\
        .mode("overwrite")\
            .save(f"abfss://bronze@{storage_account}.dfs.core.windows.net/delta/online_retail")

print("Bronze Delta table written sucessfully.")
