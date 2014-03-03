clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" | xargs rm -rf
