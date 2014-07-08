VERSION=0.1.1

# Do all the versioning stuff here..


# Clean, test, build the source distribution & pip install it
# Need to get exit statuses here...
python setup.py clean
python setup.py test
python setup.py sdist
pip install dist/BanzaiDB-$VERSION.tar.gz

# Docs
# Need to get exit statuses here...
cd docs
make clean
sphinx-apidoc -o API ../src/BanzaiDB
mv API/* .
rmdir API
make html

# tag & push the tag to github

# Upload to PyPI

