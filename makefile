# CS550 Group 6
# Ryan Daugherty
# Tom Houman
# Joe Muoio
# CS550 Spring 2013
# Assignment 2
#
# makefile
# Top-level makefile for assignment 2

MEMSIZE=20

view-part1 : ./Part1/implementation.py ./Part1/list_implementation.py ./Part1/structures.py ./Part1/list_structures.py
	more ./Part1/*.py

view-part2 : ./Part2/implementation.py ./Part2/structures.py ./Part2/list_structures.py ./Part2/list_memory.py
	more ./Part2/*.py

build : 
	echo "We are using python, so I guess it's built"
	
run-part1 : ./Part1/implementation.py ./Part1/list_implementation.py ./Part1/structures.py ./Part1/list_structures.py
	python ./Part1/implementation.py

run-part2 : ./Part2/implementation.py ./Part2/structures.py ./Part2/list_structures.py
	python ./Part2/implementation.py $(MEMSIZE)

view-func1 : listLengthIterative
	more ./listLengthIterative

view-func2 : listLengthRecursive
	more ./listLengthRecursive

clean :
	@rm -f ./parsetab.py
	@rm -f ./parsetab.pyc
	@rm -f ./parser.out
	@rm -f ./*.pyc
	@rm -f ./*/parsetab.py
	@rm -f ./*/parsetab.pyc
	@rm -f ./*/parser.out
	@rm -f ./*/*.pyc
