test:
	pytest -vv

build:
	python3 -m build --sdist .
	python3 -m build --wheel .

publish:
	twine upload dist/propgraph-0.1.0.tar.gz dist/propgraph-0.1.0-py2.py3-none-any.whl --verbose