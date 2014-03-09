clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" | xargs rm -rf

release:
	python setup.py sdist bdist_wheel upload
