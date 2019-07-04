import json
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext


sc = SparkContext.getOrCreate()
my_lines = sc.textFile('branlytic1.csv')
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
    tags = fields[8]
    present = 1
    results = []
    for tag in tags.split(' '):
        if tag == '':
            continue
        results.append((tag, [post_like, post_view, post_comment, post_share, present]))
    return tuple(results)


parsed_res = my_lines.map(parsed_line)
parsed_res.take(3)
print(json.dumps(parsed_res.take(2), indent=4, sort_keys=True))


tags = parsed_res.flatMap(lambda x: x)
tags.take(10)


def f(x, y):
    return (
        x[0] + y[0],
        x[1] + y[1],
        x[2] + y[2],
        x[3] + y[3],
        x[4] + y[4]
    )


totals_tag = tags.reduceByKey(f)
totals_tag.take(10)


lc = {
    'like': 0,
    'view': 1,
    'comment': 2,
    'share': 3,
    'present': 4
}

totals_tag.sortBy(lambda x: x[1][lc['like']], ascending=False).collect()
totals_tag.sortBy(lambda x: x[1][lc['view']], ascending=False).collect()
totals_tag.sortBy(lambda x: x[1][lc['comment']], ascending=False).collect()
totals_tag.sortBy(lambda x: x[1][lc['share']], ascending=False).collect()
totals_tag.sortBy(lambda x: x[1][lc['present']], ascending=False).collect()


totals_tag.sortBy(lambda x: x[1][lc['like']], ascending=False).take(3)
totals_tag.sortBy(lambda x: x[1][lc['view']], ascending=False).take(3)
totals_tag.sortBy(lambda x: x[1][lc['comment']], ascending=False).take(3)
totals_tag.sortBy(lambda x: x[1][lc['share']], ascending=False).take(3)
totals_tag.sortBy(lambda x: x[1][lc['present']], ascending=False).take(3)


# tmp = [('a', 1), ('b', 2), ('1', 3), ('d', 4), ('2', 5)]
# sc.parallelize(tmp).sortBy(lambda x: x[0]).collect()
# [('1', 3), ('2', 5), ('a', 1), ('b', 2), ('d', 4)]
# sc.parallelize(tmp).sortBy(lambda x: x[1]).collect()
# [('a', 1), ('b', 2), ('1', 3), ('d', 4), ('2', 5)]