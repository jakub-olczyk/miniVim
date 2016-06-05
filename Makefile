# Copyright (c) Jakub Olczyk

all: test clean

run:
	python main.py 

test:
	python src/TestCommand.py

clean:
	rm -f src/*.pyc
