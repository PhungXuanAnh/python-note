import json
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.types import StructField, TimestampType, IntegerType, StringType, StructType

sc = SparkContext.getOrCreate()
whole_log = sc.textFile('click_data_sample.csv')
whole_log.take(3)

fields = [
    StructField('access_time', TimestampType(), True),
    StructField('user_id', IntegerType(), True),
    StructField('campaign_id', StringType(), True)
]

schema = StructType(fields)

whole_log_df = SQLContext.createDataFrame(whole_log, schema)
whole_log_df = whole_log.toDF(schema)

print(whole_log_df.count())
print(whole_log_df.printSchema())
print(whole_log_df.dtypes)
print(whole_log_df.show(5))