# tar xvf spark-2.4.2-bin-hadoop2.7.tgz
# sudo mv spark-2.4.2-bin-hadoop2.7/ /opt/spark 
# start-master.sh 
# ss -tunelp | grep 8080
# start-slave.sh spark://sigma-PC:7077

# sudo update-alternatives --install  /usr/bin/python python /usr/bin/python3.6 1

# export SPARK_HOME='/{YOUR_SPARK_DIRECTORY}/spark-2.3.1-bin-hadoop2.7'
# export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
# export PYSPARK_DRIVER_PYTHON="jupyter"
# export PYSPARK_DRIVER_PYTHON_OPTS="notebook"
# export PYSPARK_PYTHON=python3
# export PATH=$SPARK_HOME:$PATH:~/.local/bin:$JAVA_HOME/bin:$JAVA_HOME/jre/bin

# cd /opt/spark
# git clone https://github.com/databricks/spark-csv.git

# pyspark --packages com.databricks:spark-csv_2.11:1.5.0

pyspark --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.0
# A solution is to remove related dir in .ivy2/cache, ivy2/jars and .m2/repository/
# https://github.com/databricks/spark-redshift/issues/244#issuecomment-347082455


# spark-submit --name "YourAppNameHere" --class com.path.to.main --master spark://localhost:7077  --driver-memory 1G --conf spark.executor.memory=4g --conf spark.cores.max=100 theUberJar.jar
# spark-submit --name "temperature" --class org.apache.spark.deploy.master.Master --master spark://spark-stand-alone:7077  --driver-memory 1G --conf spark.executor.memory=1g --conf spark.cores.max=1 Temperature.py
# spark-submit --master yarn --deploy-mode cluster  py_files.py 
# export SPARK_LOCAL_IP=192.168.1.223