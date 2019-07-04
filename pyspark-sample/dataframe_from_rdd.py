from pyspark.sql import Row
from pyspark import SparkContext
from pyspark.sql import SQLContext

sc = SparkContext.getOrCreate()
l = [('Ankit', 25), ('Jalfaizy', 22), ('saurabh', 20), ('Bala', 26)]
rdd = sc.parallelize(l)
people = rdd.map(lambda x: Row(name=x[0], age=int(x[1])))

sqlContext = SQLContext(sc)
schemaPeople = sqlContext.createDataFrame(people)
schemaPeople.show(10)
