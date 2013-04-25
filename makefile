#
# Assignment 2 makefile
#
# Spring 2012
# Drexel CS550 Group 6
# Ryan Daugherty
# Tom Houman
# Joe Muoio

view-part1 : ./Part1/implementation.py ./Part1/list_implementation.py ./Part1/structures.py ./Part1/list_structures.py
	more ./Part1/*.py

view-part2 : ./Part2/implementation.py ./Part2/structures.py ./Part2/list_structures.py
	more ./Part2/*.py

build : 
	echo "We are using python, so I guess it's built"
	
run-part1 : ./Part1/implementation.py ./Part1/list_implementation.py ./Part1/structures.py ./Part1/list_structures.py
	python ./Part1/implementation.py

run-part2 : ./Part2/implementation.py ./Part2/structures.py ./Part2/list_structures.py
	python ./Part2/implementation.py

view-func1 : 
	echo ""

view-func2 : 
	echo ""

clean :
	@rm -f ./parsetab.py
	@rm -f ./parsetab.pyc
	@rm -f ./parser.out
	@rm -f ./*.pyc
	@rm -f ./*/parsetab.py
	@rm -f ./*/parsetab.pyc
	@rm -f ./*/parser.out
	@rm -f ./*/*.pyc
