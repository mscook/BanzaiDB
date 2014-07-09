VERSION=0.1.1

# Do all the versioning stuff here..


# Clean, test, build the source distribution & pip install it
# Need to get exit statuses here...
python setup.py clean

python setup.py test
STATUS=`echo $?`
if [ $STATUS -eq 0 ]; then
    echo ""
else
    echo "Tests failed. Will not release"
    exit
fi 

python setup.py sdist
pip install dist/BanzaiDB-$VERSION.tar.gz
STATUS=`echo $?`
if [ $STATUS -eq 0 ]; then
    echo ""
else
    echo "Package is not pip installable. Will not release"
    exit
fi 


# Docs
# Need to get exit statuses here...
cd docs
make clean
sphinx-apidoc -o API ../src/BanzaiDB
mv API/* .
rmdir API
make html


# tag & push the tag to github
GIT=`git status`
CLEAN='# On branch master nothing to commit, working directory clean'
if [ "$s1" == "$s2" ]; then
    git tag v$VERSION
    git push --tags
else
    echo "Git not clean. Will not release"
    exit
fi 



# Upload to PyPI

