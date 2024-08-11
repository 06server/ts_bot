import os
import findspark
import pyspark.sql.functions as F
import pyspark.sql.types as T

from clickhouse_driver import Client
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

citys_schema = T.StructType(
  [
    T.StructField('city', T.StringType(), True)
  ]
)

address_schema = T.StructType(
  [
    T.StructField('address', T.StringType(), True)
  ]
)

timing_schema = T.StructType(
  [
    T.StructField('main_section_time', T.StringType(), True),
    T.StructField('equip_section_time', T.StringType(), True),
    T.StructField('cabel_section_time', T.StringType(), True),
    T.StructField('router_section_time', T.StringType(), True),
    T.StructField('internet_section_time', T.StringType(), True),
    T.StructField('lan_section_time', T.StringType(), True),
    T.StructField('speed_section_time', T.StringType(), True),
    T.StructField('wifi_section_time', T.StringType(), True),
    T.StructField('connection_section_time', T.StringType(), True),
    T.StructField('tariff_section_time', T.StringType(), True),
    T.StructField('offs_section_time', T.StringType(), True),
    T.StructField('errors_section_time', T.StringType(), True),
    T.StructField('my_tariff_section_time', T.StringType(), True),
    T.StructField('change_tariff_section_time', T.StringType(), True),
    T.StructField('all_section_time', T.StringType(), True)
  ]
)

a_columns_citys_df = [col("data.city").alias("City")]
a_columns_address_df = [col("data.address").alias("Address")]
a_columns_timing_df = [col("data.main_section_time").alias("Main"), col("data.equip_section_time").alias("Equip"), col("data.cabel_section_time").alias("Cabel"), 
                     col("data.router_section_time").alias("Router"), col("data.internet_section_time").alias("Internet"), col("data.lan_section_time").alias("LAN"), 
                     col("data.speed_section_time").alias("Speed"), col("data.wifi_section_time").alias("WIFI"), col("data.connection_section_time").alias("Conn"), 
                     col("data.tariff_section_time").alias("Tariff"), col("data.offs_section_time").alias("Offs"), col("data.errors_section_time").alias("Errors"), 
                     col("data.my_tariff_section_time").alias("My tariff"), col("data.change_tariff_section_time").alias("Change tariff"), col("data.all_section_time").alias("All time")]

columns_citys_df = [col("data.city")]
columns_address_df = [col("data.address")]
columns_timing_df = [col("data.main_section_time"), col("data.equip_section_time"), col("data.cabel_section_time"), 
                     col("data.router_section_time"), col("data.internet_section_time"), col("data.lan_section_time"), 
                     col("data.speed_section_time"), col("data.wifi_section_time"), col("data.connection_section_time"), 
                     col("data.tariff_section_time"), col("data.offs_section_time"), col("data.errors_section_time"), 
                     col("data.my_tariff_section_time"), col("data.change_tariff_section_time"), col("data.all_section_time")]


payload_df = df.withColumn("data", from_json(col("value"), main_schema)) \
                          .select("data.payload")
print("\n" + "-"*10 + "SCHEMA" + "-"*10 + "\n")
payload_df.printSchema()

after_df = payload_df.withColumn("data", from_json(col("payload"), payload_schema)) \
                          .select("data.after")
print("\n" + "-"*10 + "SCHEMA" + "-"*10 + "\n")
after_df.printSchema()

client = Client(host='localhost', port=9000, user='default', password='password', database='default', settings={"use_numpy":True})

def process_batch(batch_df, batch_id):
    citys_df = batch_df.withColumn("data", from_json(col("after"), citys_schema)) \
                          .select(columns_citys_df) \
                          .dropna(how='any')
    print("\n" + "-"*10 + "SCHEMA" + "-"*10 + "\n")
    citys_df.printSchema()
    citys_df.show()
    
    address_df = batch_df.withColumn("data", from_json(col("after"), address_schema)) \
                              .select(columns_address_df) \
                              .dropna(how='any')
    print("\n" + "-"*10 + "SCHEMA" + "-"*10 + "\n")
    address_df.printSchema()
    address_df.show()

    timing_df = batch_df.withColumn("data", from_json(col("after"), timing_schema)) \
                              .select(columns_timing_df) \
                              .dropna(how='any')
    print("\n" + "-"*10 + "SCHEMA" + "-"*10 + "\n")
    timing_df.printSchema()
    timing_df.show()

    pd_citys_df = citys_df.toPandas()
    pd_address_df = address_df.toPandas()
    pd_timing_df = timing_df.toPandas()

    client.insert_dataframe('INSERT INTO citys (city) VALUES', pd_citys_df)
    client.insert_dataframe('INSERT INTO default.address (address) VALUES', pd_address_df)
    client.insert_dataframe('INSERT INTO timings (main_section_time, equip_section_time, cabel_section_time, router_section_time, internet_section_time, lan_section_time, speed_section_time, wifi_section_time, connection_section_time, tariff_section_time, offs_section_time, errors_section_time, my_tariff_section_time, change_tariff_section_time, all_section_time) VALUES', pd_timing_df)

    print("\n\n\n" + "-"*10 + "DATA IN TABLES" + "-"*10)

    """
    citys_query = citys_df.writeStream.format("console") \
                .option("truncate", "false") \
                .outputMode("append") \
                .start()\
                .awaitTermination()

    address_query = address_df.writeStream.format("console") \
                .option("truncate", "false") \
                .outputMode("append") \
                .start()\
                .awaitTermination()

    timing_query = timing_df.writeStream.format("console") \
                .option("truncate", "false") \
                .outputMode("append") \
                .start() \
                .awaitTermination()
    """
    
query = after_df.writeStream \
    .foreachBatch(process_batch) \
    .start()

query.awaitTermination()

"""

write_timings = citys_df.writeStream \
  .format("jdbc") \
  .option("url", "jdbc:clickhouse://localhost:8123") \
  .option("driver", "ru.yandex.clickhouse.ClickHouseDriver") \
  .option("user", "default") \
  .option("password", "password") \
  .option("dbtable", "citys") \
  .outputMode("append") \
  .start()

citys_df.writeStream.foreachBatch(foreach_batch(citys_df, "citys")).start()  
address_df.writeStream.foreachBatch(foreach_batch(address_df, "address")).start()  
timing_df.writeStream.foreachBatch(foreach_batch(timing_df, "timings")).start().awaitTermination()  

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

