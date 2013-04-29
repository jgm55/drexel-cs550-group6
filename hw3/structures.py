#!/usr/bin/python
#
# Classes to represent underlying data structures for the grammar
#
# Ryan Daugherty
# Tom Houman
# Joe Muoio
#
# Modified from code provided by Kurt Schmidt

import sys
#from list_structures import List

####  CONSTANTS   ################

	# the variable name used to store a proc's return value
returnSymbol = 'return'

tabstop = '  ' # 2 spaces

#####  Globals    #################

symbolCounter = 1
temporaryCounter = 1

symbolTable = {} # maps a symbolic key to a tuple containing (memory address, value)

code = '' # the compiled code


#########	Helper functions	############

def dumpSymbolTable():
	global symbolTable
	global symbolCounter
	table = ""
	allocations = [0]*symbolCounter
	for k, v in symbolTable.iteritems():
		allocations[int(v[0])] = k
	for i in range(1, symbolCounter):
		k = allocations[i]
		v = symbolTable[k]
		table += str(v[0]) + "  " + str(v[1]) + " ; "
		try:
			int(k)
			table += "constant " + k
		except ValueError:
			table += "variable " + k
		table += "\n"
	return table

def getAddressFromSymbolTable(key):
	try:
		address = symbolTable[key][0] 
	except:
		address = addToSymbolTable( key, 0 ) 
	
	return address
		

def addToSymbolTable(key, value):
	# adds the value at the location of key
	# key is the symbol in the program that was parsed
	# value is the numerical value of the thing being stored
	# returns the symbol table address.
	global symbolTable
	global symbolCounter
	
	if key not in symbolTable :
		symbolTable[key] = (str(symbolCounter), value)
		symbolCounter += 1
		
	return symbolTable[key][0]
	
def addTempToSymbolTable(value=0):
	# adds the value at the location of "temporary_#"
	# value is the numerical value of the key
	# returns the symbol table address.
	global symbolTable
	global symbolCounter
	global temporaryCounter
	
	key = "temporary_"+str(temporaryCounter)
	symbolTable[key] = (str(symbolCounter), value)
	symbolCounter += 1
	temporaryCounter += 1
				
	return symbolTable[key][0]	
	
######   CLASSES   ##################

class Expr :
	'''Virtual base class for expressions in the language'''

	def __init__( self ) :
		raise NotImplementedError(
			'Expr: pure virtual base class.  Do not instantiate' )

	def eval( self, nt, ft ) :
		'''Given an environment and a function table, evaluates the expression,
		returns the value of the expression (an int in this grammar)'''

		raise NotImplementedError(
			'Expr.eval: virtual method.  Must be overridden.' )
	def isList(self):
		return False
	def isInt(self):
		return False
	
	def display( self, nt, ft, depth=0 ) :
		'For debugging.'
		raise NotImplementedError(
			'Expr.display: virtual method.  Must be overridden.' )
	def translate( self, nt, ft ) :
		'For debugging.'
		raise NotImplementedError(
			'Expr.translate: virtual method.  Must be overridden.' )
	
class Ident( Expr ) :
	'''Stores the symbol'''

	def __init__( self, name ) :
		self.name = name
	
	def eval( self, nt, ft ) :
		return nt[ self.name ]

	def display( self, nt, ft, depth=0 ) :
		print "%s%s" % (tabstop*depth, self.name)
	def translate( self, nt, ft ):
		
		address = addToSymbolTable( str(self.name), 0 ) 
		#we use 0 since it will get its real value when it is assigned.
		return address

class Times( Expr ) :
	'''expression for binary multiplication'''

	def __init__( self, lhs, rhs ) :
		'''lhs, rhs are Expr's, the operands'''
		
		# test type here?
		# if type( lhs ) == type( Expr ) :
		if lhs.isList() or rhs.isList():
			raise Exception("Operation cannot apply to lists")
		self.lhs = lhs
		self.rhs = rhs
	
	def eval( self, nt, ft ) :
		return self.lhs.eval( nt, ft ) * self.rhs.eval( nt, ft )

	def display( self, nt, ft, depth=0 ) :
		print "%sMULT" % (tabstop*depth)
		self.lhs.display( nt, ft, depth+1 )
		self.rhs.display( nt, ft, depth+1 )
		#print "%s= %i" % (tabstop*depth, self.eval( nt, ft ))
	def translate(self,nt,ft):
		global symbolCounter
		
		code = self.lhs.translate(nt,ft)
		code += self.rhs.translate(nt,ft)
		c = 0
		code += "LD 0\n"
		if self.lhs > self.rhs:
			addr = "t"+str(symbolCounter - 2)
			lesserSide = self.rhs
		else:
			addr = "t"+str(symbolCounter - 1) 
			lesserSide = self.lhs
		while c < lesserSide:
			code += "ADD t" + addr + "\n"
		code += "STA t" + str(symbolCounter) + "\n"
		symbolCounter += 1
		return code

class Plus( Expr ) :
	'''expression for binary addition'''

	def __init__( self, lhs, rhs ) :
		if lhs.isList() or rhs.isList():
			raise Exception("Operation cannot apply to lists")
		self.lhs = lhs
		self.rhs = rhs
	
	def eval( self, nt, ft ) :
		return self.lhs.eval( nt, ft ) + self.rhs.eval( nt, ft )

	def display( self, nt, ft, depth=0 ) :
		print "%sADD" % (tabstop*depth)
		self.lhs.display( nt, ft, depth+1 )
		self.rhs.display( nt, ft, depth+1 )
		#print "%s= %i" % (tabstop*depth, self.eval( nt, ft ))
	def translate(self,nt,ft):
		global code
	
		addrl = self.lhs.translate(nt,ft)
		addrr = self.rhs.translate(nt,ft)
		addrresult = addTempToSymbolTable()
		
		code += "LDA " + addrl + "\n"
		code += "ADD " + addrr + "\n"
		
		code += "STA " + addrresult + "\n"
		
		return addrresult
		

class Minus( Expr ) :
	'''expression for binary subtraction'''

	def __init__( self, lhs, rhs ) :
		if lhs.isList() or rhs.isList():
			raise Exception("Operation cannot apply to lists")
		self.lhs = lhs
		self.rhs = rhs
	
	def eval( self, nt, ft ) :
		return self.lhs.eval( nt, ft ) - self.rhs.eval( nt, ft )

	def display( self, nt, ft, depth=0 ) :
		print "%sSUB" % (tabstop*depth)
		self.lhs.display( nt, ft, depth+1 )
		self.rhs.display( nt, ft, depth+1 )
		#print "%s= %i" % (tabstop*depth, self.eval( nt, ft ))
	def translate(self,nt,ft):
		#must call translate??
		global symbolCounter
		
		code = self.rhs.translate(nt,ft)
		code += self.lhs.translate(nt,ft)
		code += "LD t"+str(symbolCounter - 2) 
		code += "\nSUB t" + str(int(symbolCounter - 1)) + "\n"
		code += "STA t" + str(symbolCounter) + "\n"
		symbolCounter += 1
		return code

class FunCall( Expr ) :
	'''stores a function call:
	  - its name, and arguments'''
	
	def __init__( self, name, argList ) :
		self.name = name
		self.argList = argList
	
	def eval( self, nt, ft ) :
		return ft[ self.name ].apply( nt, ft, self.argList )

	def display( self, nt, ft, depth=0 ) :
		print "%sFunction Call: %s, args:" % (tabstop*depth, self.name)
		for e in self.argList :
			e.display( nt, ft, depth+1 )


#-------------------------------------------------------

class Stmt :
	'''Virtual base class for statements in the language'''

	def __init__( self ) :
		raise NotImplementedError(
			'Stmt: pure virtual base class.  Do not instantiate' )

	def eval( self, nt, ft ) :
		'''Given an environment and a function table, evaluates the expression,
		returns the value of the expression (an int in this grammar)'''

		raise NotImplementedError(
			'Stmt.eval: virtual method.  Must be overridden.' )

	def display( self, nt, ft, depth=0 ) :
		'For debugging.'
		raise NotImplementedError(
			'Stmt.display: virtual method.  Must be overridden.' )
	def translate ( self, nt, ft, depth=0):
		raise NotImplementedError(
			'Stmt.translate: virtual method.  Must be overridden.' )

class AssignStmt( Stmt ) :
	'''adds/modifies symbol in the current context'''

	def __init__( self, name, rhs ) :
		'''stores the symbol for the l-val, and the expressions which is the
		rhs'''
		self.name = name
		self.rhs = rhs
	
	def eval( self, nt, ft ) :
		nt[ self.name ] = self.rhs.eval( nt, ft )

	def display( self, nt, ft, depth=0 ) :
		print "%sAssign: %s :=" % (tabstop*depth, self.name)
		self.rhs.display( nt, ft, depth+1 )
	def translate( self, nt, ft ) :
		#print "%sAssign: %s :=" % (tabstop*depth, self.name)
		global code
		addrresult = self.rhs.translate( nt, ft )
		code += 'LDA ' + addrresult + "\n"
		code += 'STA ' + getAddressFromSymbolTable( self.name ) + "\n"
		getAddressFromSymbolTable( self.name )

class IfStmt( Stmt ) :

	def __init__( self, cond, tBody, fBody ) :
		'''expects:
		cond - expression (integer)
		tBody - StmtList
		fBody - StmtList'''
		
		self.cond = cond
		self.tBody = tBody
		self.fBody = fBody

	def eval( self, nt, ft ) :
		if self.cond.eval( nt, ft ) > 0 :
			self.tBody.eval( nt, ft )
		else :
			self.fBody.eval( nt, ft )

	def display( self, nt, ft, depth=0 ) :
		print "%sIF" % (tabstop*depth)
		self.cond.display( nt, ft, depth+1 )
		print "%sTHEN" % (tabstop*depth)
		self.tBody.display( nt, ft, depth+1 )
		print "%sELSE" % (tabstop*depth)
		self.fBody.display( nt, ft, depth+1 )


class WhileStmt( Stmt ) :

	def __init__( self, cond, body ) :
		self.cond = cond
		self.body = body

	def eval( self, nt, ft ) :
		while self.cond.eval( nt, ft ) > 0 :
			self.body.eval( nt, ft )

	def display( self, nt, ft, depth=0 ) :
		print "%sWHILE" % (tabstop*depth)
		self.cond.display( nt, ft, depth+1 )
		print "%sDO" % (tabstop*depth)
		self.body.display( nt, ft, depth+1 )

#-------------------------------------------------------

class StmtList :
	'''builds/stores a list of Stmts'''

	def __init__( self ) :
		self.sl = []
	
	def insert( self, stmt ) :
		self.sl.insert( 0, stmt )
	
	def eval( self, nt, ft ) :
		for s in self.sl :
			s.eval( nt, ft )
	
	def display( self, nt, ft, depth=0 ) :
		print "%sSTMT LIST" % (tabstop*depth)
		for s in self.sl :
			s.display( nt, ft, depth+1 )
	def translate( self, nt, ft ):
		for s in self.sl :
			s.translate( nt, ft )

class Program :
	
	def __init__( self, stmtList ) :
		self.stmtList = stmtList
		self.nameTable = {}
		self.funcTable = {}
	
	def eval( self ) :
		self.stmtList.eval( self.nameTable, self.funcTable )
	
	def dump( self ) :
		print "Dump of Symbol Table"
		print "Name Table"
		for k in self.nameTable :
			print "  %s -> %s " % ( str(k), str(self.nameTable[k]) )
		print "Function Table"
		for k in self.funcTable :
			print "  %s" % str(k)
		print ""

	def display( self, depth=0 ) :
		#print "%sPROGRAM :" % (tabstop*depth)
		self.stmtList.display( self.nameTable, self.funcTable )
	def translate(self):
		self.stmtList.translate( self.nameTable, self.funcTable )
		return code
