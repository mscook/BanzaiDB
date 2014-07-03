coverage run --source ../src/BanzaiDB test_config.py
coverage run -a --source ../src/BanzaiDB test_converters.py
coverage run -a --source ../src/BanzaiDB test_misc.py
coverage run -a --source ../src/BanzaiDB test_core.py
coverage run -a --source ../src/BanzaiDB test_database.py
coverage run -a --source ../src/BanzaiDB test_errors.py
coverage run -a --source ../src/BanzaiDB test_banzaidb.py

coverage report -m
