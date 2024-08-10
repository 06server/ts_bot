from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

import os
import tempfile
import time
import findspark

findspark.init('C:\Spark\spark-3.5.1-bin-hadoop3')

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 pyspark-shell'

spark = (
    SparkSession
    .builder
    .appName("Streaming from kafka")
    .config("spark.streaming.stopGracefullyOnShutdown", True)
    .config('spark.jars.packages', 'org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1')
    .config("spark.sql.shuffle.partitions", 4)
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

df = (
    spark
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9101") \
    .option("subscribe", "cdc.public.orders") \
    .option("startingOffsets", "earliest") \
    .load() \
    .selectExpr("CAST(value AS STRING)") 
)

df.printSchema()

query = df.writeStream.format("console") \
            .option("truncate", "false") \
            .outputMode("append") \
            .start() \
            .awaitTermination()

orders_schema = StructType() \
        .add("order_id", StringType()) \
        .add("order_phone", StringType()) \
        .add("order_city", StringType()) \
        .add("order_address", StringType()) \
        .add("order_problem", StringType()) \
        .add("order_description", StringType()) \
        .add("order_all_section_time", StringType())



print("Stream Data Processing Application Completed.")

"""
transaction_detail_df1 = df.selectExpr("CAST(value AS STRING)", "timestamp")

# Define a schema for the transaction_detail data
transaction_detail_schema = StructType() \
        .add("transaction_id", StringType()) \
        .add("transaction_card_type", StringType()) \
        .add("transaction_amount", StringType()) \
        .add("transaction_datetime", StringType())

transaction_detail_df2 = transaction_detail_df1\
        .select(from_json(col("value"), transaction_detail_schema).alias("transaction_detail"), "timestamp")

transaction_detail_df3 = transaction_detail_df2.select("transaction_detail.*", "timestamp")

# Simple aggregate - find total_transaction_amount by grouping transaction_card_type
transaction_detail_df4 = transaction_detail_df3.groupBy("transaction_card_type")\
        .agg({'transaction_amount': 'sum'}).select("transaction_card_type", \
        col("sum(transaction_amount)").alias("total_transaction_amount"))

print("Printing Schema of transaction_detail_df4: ")
transaction_detail_df4.printSchema()


transaction_detail_df5 = transaction_detail_df4.withColumn("key", lit(100))\
                                                    .withColumn("value", concat(lit("{'transaction_card_type': '"), \
                                                    col("transaction_card_type"), lit("', 'total_transaction_amount: '"), \
                                                    col("total_transaction_amount").cast("string"), lit("'}")))

print("Printing Schema of transaction_detail_df5: ")
transaction_detail_df5.printSchema()

"""

"""
spark = (SparkSession
         .builder \
         .appName('Streaming-kafka-to-ClickHouse') \
         .master('local[*]') \
         .getOrCreate()) 

source = (spark
          .readStream \
          .format('kafka') \
          .option('kafka.bootstrap.servers', 'localhost:9092') \
          .option('subscribe', 'cdc.public.orders') \
          .load())

df = (source
          .selectExpr('CAST(key AS STRING)', 'CAST(value AS STRING)'))

stream_df = df.select(col('key'), col('value'))

console = (df
            .writeStream
            .format('console')
            .queryName('console output')
            .start()
            .awaitTermination())

console.show()
"""

"""
# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 spark-kafka.py

def main():
   spark = SparkSession.builder.appName("dataproc-kafka-read-batch-app").getOrCreate()

   df = spark.read.format("kafka") \
      .option("kafka.bootstrap.servers", "localhost:9092") \
      .option("subscribe", "cdc.public.orders") \
      .option("kafka.security.protocol", "SASL_SSL") \
      .option("kafka.sasl.mechanism", "SCRAM-SHA-512") \
      .option("startingOffsets", "earliest") \
      .load() \
      .selectExpr("CAST(value AS STRING)") \
      .where(col("value").isNotNull())


if __name__ == "__main__":
   main()
   
"""