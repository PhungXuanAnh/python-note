from pyspark import SparkContext, SparkConf

sc = SparkContext.getOrCreate()
lines = sc.textFile('Temperature.csv')
lines.take(10)


def parsed_line(line):
    fields = line.split(',')
    station_id = fields[0]
    entry_type = fields[2]
    temperature = float(fields[3]) * 0.1 * (9.0 / 5.0) + 32.0
    return (station_id, entry_type, temperature)

parsed_res = lines.map(parsed_line)
parsed_res.take(10)

tmin_filtered = parsed_res.filter(lambda x: 'TMIN' in x[1])
tmin_filtered.take(10)

temp_station = tmin_filtered.map(lambda x: (x[0], x[2]))
temp_station.take(10)

temp_min = temp_station.reduceByKey(lambda x, y: min(x, y))
temp_min.take(10)
