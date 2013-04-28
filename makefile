
view-part1 : ./Part1/implementation.py ./Part1/list_implementation.py ./Part1/structures.py ./Part1/list_structures.py
	more ./Part1/*.py

build : 
	echo "We are using python, so I guess it's built"
	
run-part1 : ./Part1/implementation.py ./Part1/list_implementation.py ./Part1/structures.py ./Part1/list_structures.py
	python ./Part1/implementation.py
	
view-func1 : listLengthIterative
	more ./listLengthIterative

view-func2 : listLengthRecursive
	more ./listLengthRecursive


clean :
	@rm -f ./*/parsetab.py
	@rm -f ./*/parsetab.pyc
	@rm -f ./*/parser.out
	@rm -f ./*/implementation.pyc
	@rm -f ./*/list_implementation.pyc
	@rm -f ./*/structures.pyc
	@rm -f ./*/list_structures.pyc
