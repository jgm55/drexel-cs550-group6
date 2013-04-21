

#!/usr/bin/python
#
# Parts of the implementation relevant to list processing
#
# Ryan Daugherty
# Tom Houman
# Joe Muoio

def p_list( p ) :
  'list : LSQUARE sequence RSQUARE'

def p_empty_list( p ) :
  'list : LSQUARE RSQUARE'

def p_sequence( p ):
  'sequence : list_element COMMA sequence'

def p_sequence_list_element( p ):
  'sequence : list_element'

def p_list_element( p ):
  'list_element : list'

def p_list_element_expr( p ):
  'list_element : expr'


