#!/usr/bin/python
#
# Parts of the implementation relevant to list processing
#
# Ryan Daugherty
# Tom Houman
# Joe Muoio

# Grammar

import ply.yacc as yacc

def p_list( p ) :
	'list : LSQUARE sequence RSQUARE'
	p[0] = List(p[2])
	#print "to [seq]",p[0]

def p_empty_list( p ) :
	'list : LSQUARE RSQUARE'
	p[0] = List([])
	#print "to empty", p[0]

def p_sequence( p ):
	'sequence : list_element COMMA sequence'
	p[0] = [p[1]] + p[3]
	#print "to list , seq", p[0]

def p_sequence_list_element( p ):
	'sequence : list_element'
	p[0] = [p[1]]
	#print "tolistElem", p[0]

def p_list_element_element( p ):
	'list_element : element'
	p[0] = p[1]
	#print "toexpr", p[0]

def p_element_number( p ):
	'element : NUMBER'
	p[0] = Number(p[1])
	#print "tonumber", p[0]

def p_element_list( p ):
	'element : list'
	p[0] = p[1]
	#print " tolist", p[0]


def func_call_cons( p ):
  'func_call : CONS LPAREN element COMMA  list RPAREN'
  p[0] = def_cons(p[2],p[3])

def func_call_car( p ):
  'func_call : CAR LPAREN list RPAREN'
  p[0] = def_car(p[2],p[3])

def func_call_cdr( p ):
  'func_call : CDR LPAREN list RPAREN'
  p[0] = def_cdr(p[2],p[3])

def func_call_nullp( p ):
  'func_call : NULLP LPAREN list RPAREN'
  p[0] = def_nullp(p[2],p[3])

def func_call_intp( p ):
  'func_call : INTP LPAREN element RPAREN'
  p[0] = def_intp(p[2],p[3])

def func_call_listp( p ):
  'func_call : LISTP LPAREN element RPAREN'
  p[0] = def_listp(p[2],p[3])

yacc.yacc()
