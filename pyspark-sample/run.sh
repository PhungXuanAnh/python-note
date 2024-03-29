# ===================================================================
# INSTALL JAVA 8
# ===================================================================
https://askubuntu.com/questions/56104/how-can-i-install-sun-oracles-proprietary-java-jdk-6-7-8-or-jre

# ===================================================================
# INSTALL SPARK
# ===================================================================
cd /opt
rm -rf spark
wget https://archive.apache.org/dist/spark/spark-3.1.1/spark-3.1.1-bin-hadoop2.7.tgz
tar xvf spark-3.1.1-bin-hadoop2.7.tgz
sudo mv spark-3.1.1-bin-hadoop2.7 spark

vim ~/.bashrc
export SPARK_HOME=/opt/spark
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

export SPARK_MASTER_HOST=67.205.158.186
export JAVA_HOME=/usr/lib/jvm/jdk1.8.0_211/bin/

# on master
export YOUR_IP=67.205.158.186
SPARK_LOCAL_IP=${YOUR_IP} SPARK_MASTER_HOST=${YOUR_IP} start-master.sh
ss -tunelp | grep 8080

# on slave
export YOUR_IP=67.205.158.186
SPARK_LOCAL_IP=${YOUR_IP} start-worker.sh spark://${YOUR_IP}:7077
ss -tunelp | grep 8081

start-master.sh         # default master ip is hostname
ss -tunelp | grep 8080
start-slave.sh spark://sigma:7077

sudo update-alternatives --install  /usr/bin/python python /usr/bin/python3.6 1

export SPARK_HOME='/{YOUR_SPARK_DIRECTORY}/spark-2.3.1-bin-hadoop2.7'
export PYTHONPATH=$SPARK_HOME/python:$PYTHONPATH
export PYSPARK_DRIVER_PYTHON="jupyter"
export PYSPARK_DRIVER_PYTHON_OPTS="notebook"

export PATH=$SPARK_HOME:$PATH:~/.local/bin:$JAVA_HOME/bin:$JAVA_HOME/jre/bin


# ===================================================================
# RUN SPARK
# ===================================================================
cd /opt/spark
git clone https://github.com/databricks/spark-csv.git

pyspark --packages com.databricks:spark-csv_2.11:1.5.0

export PYSPARK_PYTHON=/home/xuananh/data/repo/python-note/.venv/bin/python
pyspark --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.2.0

# A solution is to remove related dir in .ivy2/cache, ivy2/jars and .m2/repository/
# https://github.com/databricks/spark-redshift/issues/244#issuecomment-347082455


# ===================================================================
# ADD APPLICATION TO SPARK
# ===================================================================
spark-submit --name "YourAppNameHere" --class com.path.to.main --master spark://localhost:7077  --driver-memory 1G --conf spark.executor.memory=4g --conf spark.cores.max=100 theUberJar.jar
spark-submit --name "temperature" --class org.apache.spark.deploy.master.Master --master spark://spark-stand-alone:7077  --driver-memory 1G --conf spark.executor.memory=1g --conf spark.cores.max=1 Temperature.py
spark-submit --master yarn --deploy-mode cluster  py_files.py 
export SPARK_LOCAL_IP=192.168.1.223