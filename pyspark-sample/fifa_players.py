from pyspark import SparkContext
from pyspark.sql import SQLContext

sc = SparkContext.getOrCreate()
spark = SQLContext(sc)
fifa_df = spark.read.csv("fifa_players.csv", inferSchema=True, header=True)

fifa_df.show(10)
fifa_df.show(2,truncate= True)

fifa_df.printSchema()

fifa_df.columns

fifa_df.count()

len(fifa_df.columns)

fifa_df.describe('Vision').show()
fifa_df.describe('Name').show()
fifa_df.describe('Photo').show()

fifa_df.select('Name','Photo').show(5)
fifa_df.select('Name','Photo').distinct().show()
fifa_df.select('Name').distinct().count()

fifa_df.crosstab('Name', 'Vision').show()
