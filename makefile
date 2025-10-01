
# install 内部包
# pip install -e .

install:
	pip install -e .

# cloc . --exclude-dir=pyside --include-ext=py

count:
	cd src && cloc . --exclude-dir=pyside --include-ext=py