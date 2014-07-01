coverage run --source ../src/BanzaiDB test_config.py
coverage run -a --source ../src/BanzaiDB test_converters.py
coverage run -a --source ../src/BanzaiDB test_misc.py
coverage run -a --source ../src/BanzaiDB test_core.py

coverage report -m
