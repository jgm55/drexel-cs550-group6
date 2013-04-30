view : implementation.py list_structures.py structures.py
	more *.py
compile : implementation.py list_structures.py structures.py
	python ./implementation.py true
	
view-trans : symbolic.out
	cat ./symbolic.out
view-link : linkedNonOpt.out
	cat ./linkedNonOpt.out
view-op : linkedOptimized.out
	cat ./linkedOptimized.out
	
run : ./linkedNonOpt.out ./symbolTable.out
	~jjohnson/bin/ram linkedNonOpt.out symbolTable.out
run-op: ./linkedOptimized.out ./symbolTable.out
	~jjohnson/bin/ram linkedNonOpt.out symbolTable.out
	
clean : 
	rm ./*.out
	rm./*.pyc
	
	