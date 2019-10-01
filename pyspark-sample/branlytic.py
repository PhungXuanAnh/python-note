import json
from pyspark import SparkConf, SparkContext

sc = SparkContext.getOrCreate()
my_lines = sc.textFile('branlytic.csv')
my_lines.take(3)


posts = my_lines.map(lambda x: x.split(','))
posts.take(2)
print(json.dumps(posts.take(2), indent=4, sort_keys=True))


def parsed_line(line):
    fields = line.split(',')
    post_like = int(fields[1])
    post_view = int(fields[2])
    post_comment = int(fields[3])
    post_share = int(fields[6])
    tag_name = fields[8]
#     color_green = int(fields[8])
#     color_red = int(fields[9])
#     color_blue = int(fields[10])
#     return (post_like, post_view, post_comment, post_share, color_green, color_red, color_blue)
    present = 1
    return (tag_name, [post_like, post_view, post_comment, post_share, present])


parsed_res = my_lines.map(parsed_line)
parsed_res.take(3)


def f(x, y):
    return (
        x[0] + y[0],
        x[1] + y[1],
        x[2] + y[2],
        x[3] + y[3],
        x[4] + y[4]
    )


totals_tag = parsed_res.reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1]))

totals_tag = parsed_res.reduceByKey(f)
totals_tag.take(10)


lc = {
    'like': 0,
    'view': 1,
    'comment': 2,
    'share': 3,
    'present': 4
}

totals_tag.sortBy(lambda x: x[1][lc['like']]).collect()
totals_tag.sortBy(lambda x: x[1][lc['view']]).collect()
totals_tag.sortBy(lambda x: x[1][lc['comment']]).collect()
totals_tag.sortBy(lambda x: x[1][lc['share']]).collect()
totals_tag.sortBy(lambda x: x[1][lc['present']]).collect()


# tmp = [('a', 1), ('b', 2), ('1', 3), ('d', 4), ('2', 5)]
# sc.parallelize(tmp).sortBy(lambda x: x[0]).collect()
# [('1', 3), ('2', 5), ('a', 1), ('b', 2), ('d', 4)]
# sc.parallelize(tmp).sortBy(lambda x: x[1]).collect()
# [('a', 1), ('b', 2), ('1', 3), ('d', 4), ('2', 5)]

# #-------------------------------------------------------------
# x = sc.parallelize([("a", ["apple", "banana", "lemon"]), ("b", ["grapes"])])
# def f(x): return len(x)
# x.mapValues(f).collect()
# x.mapValues(lambda x: len(x)).collect()
# x.mapValues(lambda x: x[0]).collect()

# reduceByKey: merge element which have same key using
from operator import add
rdd = sc.parallelize([("a", 1), ("b", 1), ("a", 1)])
rdd.reduceByKey(add).collect()
rdd.reduceByKey(add).collect()
sorted(rdd.reduceByKey(add).collect())

lst1 = [('a', 1), ('b', 2), ('c', 3)]
lst2 = [('a', 1), ('b', 2)]
rdd = sc.parallelize(lst1 + lst2)
sorted(rdd.reduceByKey(lambda x, y: [x, y]).collect())


# UNION: nối 2 rdd với nhau
empty_rdd = sc.emptyRDD()
rdd1 = sc.parallelize([1, 2, 3])
rdd2 = sc.parallelize([4, 5, 6])
_rdd = empty_rdd.union(rdd1)
rdd = _rdd.union(rdd2)
rdd.collect()

rdd1 = sc.parallelize([('a', 1), ('b', 2), ('c', 3)])
rdd2 = sc.parallelize([('a', 1), ('b', 2), ('c', 3)])
rdd1.union(rdd2).collect()

rdd1 = sc.parallelize([1, 2, 3])
rdd2 = sc.parallelize([4, 5, 6])
rdd = sc.union([rdd1, rdd2])
rdd.collect()

rdd1 = sc.parallelize([('a', 1), ('b', 2), ('c', 3)])
rdd2 = sc.parallelize([('a', 1), ('b', 2), ('c', 3)])
rdd = sc.union([rdd1, rdd2])
rdd.collect()


# join 2 RDD with element have same key
rdd1 = sc.parallelize([('a', 1), ('b', 2), ('c', 3)])
rdd2 = sc.parallelize([('a', 1), ('b', 2), ('c', 3)])
rdd1.join(rdd2).collect()

rdd1 = sc.parallelize([('a', 1), ('b', 2), ('c', 3)])
rdd2 = sc.parallelize([('b', 5)])
rdd1.join(rdd2).collect()

# remove duplicated element in rdd
sorted(sc.parallelize([1, 1, 2, 3]).distinct().collect())
sorted(sc.parallelize([(1, 1), (1, 1), (2, 2), (3, 3)]).distinct().collect())
sorted(sc.parallelize([('a', 1), ('a', 1), ('b', 2), ('c', 3)]).distinct().collect())
sorted(sc.parallelize([(1, 'a'), (1, 'a'), (2, 'b'), (3, 'c')]).distinct().collect())
