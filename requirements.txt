sudo apt-get install python-qt4 -y
sudo apt-get install libxml2-dev libxslt1-dev python-dev -y
sudo apt-get install python-lxml -y

virtualenv ~/.python_dev_env
source ~/.python_dev_env/bin/activate

sudo -H pip install pygame
sudo -H pip install pyglet
sudo -H pip install requests
