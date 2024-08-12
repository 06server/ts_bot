import pyspark.sql.types as T
from pyspark.sql.functions import col,from_json

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

full_schema = T.StructType(
  [
    T.StructField('city', T.StringType(), True),
    T.StructField('address', T.StringType(), True),
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
columns_full_df = [  col("data.city"), col("data.address"),
                     col("data.main_section_time"), col("data.equip_section_time"), col("data.cabel_section_time"), 
                     col("data.router_section_time"), col("data.internet_section_time"), col("data.lan_section_time"), 
                     col("data.speed_section_time"), col("data.wifi_section_time"), col("data.connection_section_time"), 
                     col("data.tariff_section_time"), col("data.offs_section_time"), col("data.errors_section_time"), 
                     col("data.my_tariff_section_time"), col("data.change_tariff_section_time"), col("data.all_section_time")]
