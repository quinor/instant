all: venv

venv:
	python3 -m venv venv && . ./venv/bin/activate && pip3 install -r requirements.txt
	ln -s ./venv/bin/activate

install:
	echo "screw you"
