from pyspark import SparkContext
import json


def parse_Line(my_lines):
    my_fields = my_lines.split(',')
    user_age = int(my_fields[2])
    number_friends = int(my_fields[3])
    return (user_age, number_friends)

sc = SparkContext.getOrCreate()
my_lines = sc.textFile('social_friends.csv')
my_lines.take(10)
print(json.dumps(my_lines.take(10), indent=4, sort_keys=True))

my_rdd = my_lines.map(parse_Line)
my_rdd.take(10)

x = my_rdd.mapValues(lambda x: (x, 1))
x.take(10)
print(json.dumps(my_lines.take(10), indent=4, sort_keys=True))

totals_age = x.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))
totals_age.take(10)
print(json.dumps(my_lines.take(10), indent=4, sort_keys=True))

averages_age = totals_age.mapValues(lambda x: x[0] / x[1])
my_results = averages_age.collect()
print(json.dumps(my_lines.take(10), indent=4, sort_keys=True))
