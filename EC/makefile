# CS550 Group 6
# Ryan Daugherty
# Tom Houman
# Joe Muoio
# CS550 Spring 2013
#
# makefile


view : implementation.py structures.py list_structures.py
	more *.py

compile-static : implementation.py structures.py list_structures.py
	echo "We are using python, so I guess it's built"

compile-dynamic : implementation.py structures.py list_structures.py
	echo "We are using python, so I guess it's built"
	
run-static : implementation.py structures.py list_structures.py
	python ./implementation.py "static"

run-dynamic : implementation.py structures.py list_structures.py
	python ./implementation.py "dynamic"

clean :
	@rm -f ./*.out
	@rm -f ./*.pyc
