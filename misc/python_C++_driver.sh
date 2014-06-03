# These worked on Ubuntu 14.04 LTS
sudo apt-get remove libprotobuf-dev protobuf-compiler
sudo apt-get remove libprotobuf-lite8 libprotoc8
sudo apt-get remove python-protobuf

sudo pip uninstall protobuf

sudo apt-get install libprotobuf-dev protobuf-compiler
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp
sudo apt-get install python-protobuf
sudo pip uninstall rethinkdb
sudo PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp pip install rethinkdb
 
cd /tmp/
wget http://protobuf.googlecode.com/files/protobuf-2.5.0.tar.gz
cd protobuf-2.5.0/python/
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp python setup.py build
sudo PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp python setup.py install
sudo apt-get remove python-protobuf
