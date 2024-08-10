import os

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 pyspark-shell'

import findspark
findspark.init('C:\Spark\spark-3.5.1-bin-hadoop3')

from pyspark.sql import SparkSession

spark = (SparkSession
        .builder
        .appName("consumer_structured_streaming_ex_1_1")
        .getOrCreate())

adViewsDF = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "cdc.public.orders") \
            .option("startingOffsets", "earliest") \
            .load() \
            .selectExpr("CAST(value AS STRING)") 

query = adViewsDF.writeStream.format("console") \
            .option("truncate", "false") \
            .outputMode("append") \
            .start() \
            .awaitTermination()


"""
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('Test').getOrCreate()

df = spark.read.csv('Mall_Customers.csv', header=True, inferSchema=True)

print("-"*10 + "TABLE" + "-"*10)
df.show()

print("-"*10 + "HEAD" + "-"*10)
df.head(3)

print("-"*10 + "SCHEMA" + "-"*10)
df.printSchema()

print("-"*10 + "NEW COLUMN" + "-"*10)
df.withColumn('x2 Spending Score', df['Spending Score (1-100)']*2).show()

print("-"*10 + "ONLY ID AND GENRE" + "-"*10)
df.select(['CustomerID', 'Genre']).show()

print("-"*10 + "GROUP BY GENRE" + "-"*10)
df.select(['Genre', 'Age']).groupBy('Genre').max().show()
"""

