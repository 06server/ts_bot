import os
import findspark
import pyspark.sql.functions as F
import pyspark.sql.types as T

from pyspark.sql.functions import col,from_json
from pyspark.sql import SparkSession


os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 pyspark-shell'
findspark.init('C:\Spark\spark-3.5.1-bin-hadoop3')

spark = (SparkSession
        .builder
        .appName("consumer_structured_streaming_ex_1_1")
        .getOrCreate())

df = spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", "localhost:9092") \
            .option("subscribe", "cdc.public.orders") \
            .option("startingOffsets", "earliest") \
            .load() \
            .selectExpr("CAST(value AS STRING)") 

main_schema = T.StructType(
  [
    T.StructField('schema', T.StringType(), True),
    T.StructField('payload', T.StringType(), True)
  ]
)

payload_schema = T.StructType(
  [
    T.StructField('before', T.StringType(), True),
    T.StructField('after', T.StringType(), True)
  ]
)

table_schema = T.StructType(
  [
    T.StructField('id', T.StringType(), True),
    T.StructField('phone', T.StringType(), True),
    T.StructField('city', T.StringType(), True),
    T.StructField('address', T.StringType(), True),
    T.StructField('problem', T.StringType(), True)
  ]
)

payload_df = df.withColumn("data", from_json(col("value"), main_schema)) \
                          .select("data.payload")

print("\n" + "-"*10 + "SCHEMA" + "-"*10 + "\n")
payload_df.printSchema()

after_df = payload_df.withColumn("data", from_json(col("payload"), payload_schema)) \
                          .select("data.after")

print("\n" + "-"*10 + "SCHEMA" + "-"*10 + "\n")
after_df.printSchema()

table_df = after_df.withColumn("data", from_json(col("after"), table_schema)) \
                          .select(["data.id", "data.phone", "data.city", "data.address", "data.problem"]) \
                          .dropna(how='any')

print("\n" + "-"*10 + "SCHEMA" + "-"*10 + "\n")
table_df.printSchema()

query = table_df.writeStream.format("console") \
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

