pip uninstall protobuf
pip uninstall rethinkdb
sudo apt-get install libprotobuf-dev protobuf-compiler
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp
sudo apt-get install python-protobuf
tar -zxvf 3rdParty/protobuf-2.4.1.tar.gz
cd protobuf-2.4.1/python
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp 
python setup.py build
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=cpp 
python setup.py install
cd ..
cd ..
pip install 3rdParty/rethinkdb-1.11.0-1.tar.gz
python -c "import rethinkdb as r; print r.protobuf_implementation"
rm -rf protobuf-2.4.1
