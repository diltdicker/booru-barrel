pip_txt:= requirements-pip.txt
venv:= ./env/bin/activate
build_dir := build
dist_dir := dist
egg_dir:= booru_barrel.egg-info

virtualenv:
	python3 -m virtualenv env

install:
	. ${venv}; pip install -r ${pip_txt}

clean:
	rm -rf ${egg_dir} ${dist_dir} ${build_dir}

build: clean
	. ${venv}; python3 setup.py sdist bdist_wheel