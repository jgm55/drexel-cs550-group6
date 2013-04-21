#!/usr/bin/python
#
# Ryan Daugherty
# Tom Houman
# Joe Muoio

import structures

class Element( Expr ) :
  '''Lists and numbers inheret from this'''

  def __init__( self ) :
    raise NotImplementedError('Cannot have an element object')

  ''''still need eval and display'''

class List( Element ) :
  '''Lists of expressions'''

  def __init__( self, v=[] ) :
    self.contents = []

  '''still needs an eval and display'''

class Number( Element ) :
  '''Just integers'''

  def __init__( self, v=0 ) :
    self.value = v

  def eval( self, nt, ft ) :
    return self.value

  def display( self, nt, ft, depth=0 ) :
    print "%s%i" % (tabstop*depth, self.value)


