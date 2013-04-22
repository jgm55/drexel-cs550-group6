#!/usr/bin/python
#
# Ryan Daugherty
# Tom Houman
# Joe Muoio

import structures
from structures import Expr

tabstop = '  ' # 2 spaces

class Concat( Expr ):
	'''expression for concating two lists'''

	def __init__(self, lhs, rhs ) :
		if not isinstance(lhs, List) or not isinstance(rhs, List):
			raise Exception("Operation only applies to lists")
		self.lhs = lhs
		self.rhs = rhs

	def eval( self, nt, ft ) :
		return self.lhs.eval( nt, ft ) + self.rhs.eval( nt, ft )

	def display( self, nt, ft, depth=0 ) :
		print "%sCONCAT" %(tabstop*depth)
		self.lhs.display( nt, ft, depth+1 )
		self.rhs.display( nt, ft, depth+1 )

class Element( Expr ) :
  '''Lists and numbers inheret from this'''

  def __init__( self ) :
    raise NotImplementedError('Cannot have an element object')

  def eval( self, nt, ft ) :
    raise NotImplementedError(
      'Expr.eval: virtual method.  Must be overridden.' )

  def display( self, nt, ft, depth=0 ) :
    raise NotImplementedError(
      'Expr.display: virtual method.  Must be overridden.' )


class List( Element ) :
	'''Lists of expressions'''

	def __init__( self, v=[] ) :
		self.contents = v

	def eval( self, nt, ft ) :
		return self.contents

	def display( self, nt, ft, depth=0) :
		if len(self.contents) < 1:
			print "%s*empty list*" % (tabstop*depth)
		for i in self.contents :
			if isinstance(i, List):
				i.display( nt, ft, depth+1)
			else:
				i.display( nt, ft, depth)
	def isList(self):
		return True
class Number( Element ) :
	'''Just integers'''

	def __init__( self, v=0 ) :
		self.value = v

	def eval( self, nt, ft ) :
		return self.value

	def display( self, nt, ft, depth=0 ) :
		print "%s%i" % (tabstop*depth, self.value)
	def isInt():
		return True

class Car( Expr ) :
	'''first entry'''
	
	def __init__( self, v="") :
		self.label = v
		
	def eval( self, nt, ft ) :	
		L = nt[ self.label ]
	
		if not isinstance(L, list):
			print "Argument must be a list"
			return
		try:
			print "L0 is ", L[0]
			return L[0]
		except:
			print "No elements left in the list to return"
	
	def display( self, nt, ft, depth=0 ) :
		L = nt[ self.label ]
		if len(L) > 0:
			L[0].display( nt, ft, depth)

class Cdr( Expr ) :
	'''All entries but the first'''
	
	def __init__( self, v="") :
		self.label = v
		
	def eval( self, nt, ft ) :	
		''' returns the rest of the list (minus the first element) '''
		L = nt[ self.label ]
		if not isinstance(L, list):
			print "Argument must be a list"
			return
		try:
			return L[1:]
		except:
			print "There are less than two elements in the list."
		
	def display( self, nt, ft, depth=0 ) :
		L = nt[ self.label ]
		for i in range(1, len(L)):
			L[i].display( nt, ft, depth)

class Cons( Expr ) :
	'''first entry'''
	
	def __init__( self, v_e="", v_l="") :
		self.label_e = v_e
		self.label_l = v_l
		
	def eval( self, nt, ft ) :	
		'''returns a new list, with element e prepended to the front of list L '''
		
		e = nt[ self.label_e ]
		L = nt[ self.label_l ]
		
		
		if not isinstance(L, list):
			print "Second argument must be a list"
			return
		C = [e] + L
		return L
		
	def display( self, nt, ft, depth=0 ) :
		e = nt[ self.label_e ]
		L = nt[ self.label_l ]
		if isinstance(e, list):
			for i in e:
				i.display( nt, ft, depth )
		else :
			e.display( nt, ft, depth )
		for i in L:
			i.display( nt, ft, depth )
			
class Nullp( Expr ) :
	'''first entry'''
	
	def __init__( self, v="") :
		self.label = v
		
	def eval( self, nt, ft ) :	
		''' returns 1 if L is null, 0 otherwise '''
		L = nt[ self.label ]
		if not isinstance(L, list):
			print "Argument must be a list"
			return
		if len(L) > 0:
			return 1
		return 0
		
	def display( self, nt, ft, depth=0 ) :
		L = nt[ self.label ]
		if len(L) > 0:
			L[0].display( nt, ft, depth)
			
class Intp( Expr ) :
	'''first entry'''
	
	def __init__( self, v="") :
		self.label = v
		
	def eval( self, nt, ft ) :	
		'''returns 1 if e is an integer, 0 otherwise '''
		e = nt[ self.label ]
		if e.isInt():
			return 1
		return 0
		
	def display( self, nt, ft, depth=0 ) :
		L = nt[ self.label ]
		if len(L) > 0:
			L[0].display( nt, ft, depth)
			
class Listp( Expr ) :
	'''first entry'''
	
	def __init__( self, v="") :
		self.label = v
		
	def eval( self, nt, ft ) :	
		'''returns 1 if e is a list, 0 otherwise'''
		e = nt[ self.label ]
		if e.isList():
			return 1
		return 0
		
	def display( self, nt, ft, depth=0 ) :
		L = nt[ self.label ]
		if len(L) > 0:
			L[0].display( nt, ft, depth)

