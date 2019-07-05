import json
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.streaming import StreamingContext


# create spark context
spark_context = SparkContext.getOrCreate()
# create streaming context
streaming_context = StreamingContext(spark_context, batchDuration=60)
# connect to kafka
kafka_stream = KafkaUtils.createStream(
    ssc=streaming_context,
    zkQuorum='localhost:2181',
    groupId='brandlytic',
    topics={'facebook-items': 1}
)


def parsed_item(items):
    # fields = line.split(',')
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    print(type(items))
    print(items)
    present = 1
    results = []
    for item in items:
        if not item:
            continue
        item = json.loads(item)
        post_like = item['post_like']
        post_view = item['post_view']
        post_comment = item['post_comment']
        post_share = item['post_share']
        # tags = item['tags']
        # for tag in tags.split(' '):
        #     if tag == '':
        #         continue
        #     results.append((tag, [post_like, post_view, post_comment, post_share, present]))
        results.append((post_like, post_view, post_comment, post_share, present))
    return tuple(results)


item = kafka_stream.map(parsed_item)
item.count()
item.pprint()
streaming_context.start()
streaming_context.awaitTermination()


# ==================== Message processing
# parse the inbound message as json
parsed = kafka_stream.map(lambda v: json.loads(v[1]))
parsed.count()
parsed.pprint()

streaming_context.start()
streaming_context.awaitTermination()
streaming_context.stop()

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
    post_share = int(fields[4])
    tags = fields[8]
    present = 1
    results = []
    for tag in tags.split(' '):
        if tag == '':
            continue
        results.append((tag, post_like, post_view, post_comment, post_share, present))
    return tuple(results)


parsed_res = my_lines.map(parsed_line)
parsed_res.take(3)
print(json.dumps(parsed_res.take(2), indent=4, sort_keys=True))


tags = parsed_res.flatMap(lambda x: x)
tags.take(3)

post_df = tags.toDF(['tag', 'post_like', 'post_view', 'post_comment', 'post_share', 'present'])


post_df.show(10)
post_df.show(2, truncate=True)

post_df.printSchema()

post_df.columns
len(post_df.columns)

post_df.count()

post_df.describe('tag').show()
post_df.describe('post_like').show()
post_df.describe('username').show()

post_df.select('tag', 'post_like').show(5)
post_df.select('tag', 'post_like').distinct().show()
post_df.select('tag').distinct().count()

post_df.crosstab('timestamp', 'post_like').show()

post_df.select('tag', 'post_like').dropDuplicates().show()

# rows in train which has post_like more than 150
post_df.filter(post_df.post_like > 5).count()
post_df.filter(post_df.post_like > 5).show(10)

post_df.select('Product_ID').subtract(train.select('Product_ID'))

post_df.crosstab('tag', 'post_like').show(1)

# drop the all rows with null value
post_df.dropna().count()

# fill the null values in DataFrame with constant number?
post_df.fillna(-1).show(2)

# find the mean(average) of each age group
post_df.groupby('tag').agg({'post_like': 'mean'}).show()
post_df.groupby('post_like').agg({'tag': 'mean'}).show()

post_df.groupby('tag').count().show()

# apply map operation on DataFrame columns?
post_df.select('post_like').rdd.map(lambda x: (x, 1)).take(5)

# sort the DataFrame based on column(s)?
post_df.orderBy(post_df.post_like.desc()).show(5)
post_df.orderBy(post_df.post_share.desc()).show(5)
post_df.orderBy(post_df.post_comment.desc()).show(5)
post_df.orderBy(post_df.post_view.desc()).show(5)

#  add the new column in DataFrame?
post_df_new = post_df.withColumn('post_like_new', post_df.post_like / 2.0)
post_df_new.select('post_like', 'post_like_new').show(5)
post_df_new.columns

# drop a column in DataFrame?
post_df_new.drop('post_like_new').columns

# remove some categories of Product_ID column in test that are not present in Product_ID column in train?
diff_cat_in_train_test = test.select('Product_ID').subtract(train.select('Product_ID'))
diff_cat_in_train_test.distinct().count()  # For distict count

# Apply SQL Queries on DataFrame?
sqlContext.registerDataFrameAsTable(post_df, "post_table")

sqlContext.sql('select tag from post_table').show(5)
sqlContext.sql('select post_like from post_table').show(5)

sqlContext.sql('select tag, max(post_like) from post_table group by tag').show()

# -------------------------------------------------------


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
