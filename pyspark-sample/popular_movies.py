from pyspark import SparkConf, SparkContext

sc = SparkContext.getOrCreate()
my_lines = sc.textFile('popular_movies.txt')
my_lines.take(10)

my_movies = my_lines.map(lambda x: (int(x.split()[1]), 1))
my_movies.take(10)

movie_counts = my_movies.reduceByKey(lambda x, y: x + y)
movie_counts.take(10)

flipped_op = movie_counts.map(lambda x: (x[1], x[0]))
flipped_op.take(10)

sorted_movies = flipped_op.sortByKey(ascending=True)
sorted_movies.take(10)

final_results = sorted_movies.collect()
len(final_results)
