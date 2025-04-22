[pytest]
testpaths = tests
addopts = --browser=firefox --headless --html=reports/report.html --self-contained-html --alluredir=reports/allure-results --reruns 2
python_files = test_*.py
python_functions = test_*