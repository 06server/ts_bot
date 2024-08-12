import os
import findspark
import pyspark.sql.functions as F
import pyspark.sql.types as T
import values_for_df as v

from clickhouse_driver import Client
from pyspark.sql.functions import col,from_json
from pyspark.sql import SparkSession

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-10_2.12:3.5.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1 pyspark-shell'
findspark.init('C:\Spark\spark-3.5.1-bin-hadoop3')

def show_schema(showing_df):
    print("\n" + "-"*10 + "SCHEMA" + "-"*10 + "\n")
    showing_df.printSchema()
    
client = Client(host='localhost', port=9000, user='default', password='password', database='default', settings={"use_numpy":True})

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

payload_df = df.withColumn("data", from_json(col("value"), v.main_schema)).select("data.payload")
# show_schema(payload_df)

after_df = payload_df.withColumn("data", from_json(col("payload"), v.payload_schema)).select("data.after")
# show_schema(after_df)

def process_batch(batch_df, batch_id):
    citys_df = batch_df.withColumn("data", from_json(col("after"), v.citys_schema)) \
                          .select(v.columns_citys_df) \
                          .dropna(how='any')
    # show_schema(citys_df)
    citys_df.show()
    
    address_df = batch_df.withColumn("data", from_json(col("after"), v.address_schema)) \
                              .select(v.columns_address_df) \
                              .dropna(how='any')
    # show_schema(address_df)
    address_df.show()

    timing_df = batch_df.withColumn("data", from_json(col("after"), v.timing_schema)) \
                              .select(v.columns_timing_df) \
                              .dropna(how='any')
    # show_schema(timing_df)
    timing_df.show()

    full_df = batch_df.withColumn("data", from_json(col("after"), v.full_schema)) \
                              .select(v.columns_full_df) \
                              .dropna(how='any')
    # show_schema(full_df)
    full_df.show()

    pd_citys_df = citys_df.toPandas()
    pd_address_df = address_df.toPandas()
    pd_timing_df = timing_df.toPandas()
    pd_full_df = full_df.toPandas()

    client.insert_dataframe('INSERT INTO citys (city) VALUES', pd_citys_df)
    client.insert_dataframe('INSERT INTO default.address (address) VALUES', pd_address_df)
    client.insert_dataframe('INSERT INTO timings (main_section_time, equip_section_time, cabel_section_time, router_section_time, internet_section_time, lan_section_time, speed_section_time, wifi_section_time, connection_section_time, tariff_section_time, offs_section_time, errors_section_time, my_tariff_section_time, change_tariff_section_time, all_section_time) VALUES', pd_timing_df)
    client.insert_dataframe('INSERT INTO full_data (city, address, main_section_time, equip_section_time, cabel_section_time, router_section_time, internet_section_time, lan_section_time, speed_section_time, wifi_section_time, connection_section_time, tariff_section_time, offs_section_time, errors_section_time, my_tariff_section_time, change_tariff_section_time, all_section_time) VALUES', pd_full_df)

    print("\n\n\n" + "-"*10 + "DATA IN TABLES" + "-"*10 + "\n\n\n")
    
query = after_df.writeStream \
    .foreachBatch(process_batch) \
    .start()

query.awaitTermination()