# CS550 Group 6
# Tom Houman (A4 Leader)
# Ryan Daugherty
# Joe Muoio
# CS550 Spring 2013
# Assignment 4
#
# makefile
# Top-level makefile for assignment 4

RAM=~jjohnson/bin/ram
#RAM=simulator/ram

SRC = \
    implementation.py \
    structures.py \
    list_structures.py

view : $(SRC)
	more $(SRC)
compile : $(SRC)
	python ./implementation.py true
	
view-trans : symbolic.out
	cat ./symbolic.out
view-link : linkedNonOpt.out
	cat ./linkedNonOpt.out
view-op : linkedOptimized.out
	cat ./linkedOptimized.out
	
run : ./linkedNonOpt.out ./symbolTable.out
ifdef RAM_MEM
	$(RAM) -m $(RAM_MEM) linkedNonOpt.out symbolTable.out
else
	$(RAM) linkedNonOpt.out symbolTable.out
endif

run-op: ./linkedOptimized.out ./symbolTable.out
ifdef RAM_MEM
	$(RAM) -m $(RAM_MEM) linkedOptimized.out symbolTable.out
else
	$(RAM) linkedOptimized.out symbolTable.out
endif
	
clean : 
	@rm -f parsetab.py
	@rm -f *.out
	@rm -f *.pyc
	
