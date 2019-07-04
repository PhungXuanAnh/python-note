from pyspark import SparkContext
from pyspark.sql import SQLContext

sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)
post_df = sqlContext.read.csv("branlytic9.csv", inferSchema=True, header=True)

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
post_df.filter(post_df.post_like > 150).count()
post_df.filter(post_df.post_like > 150).show(10)

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
