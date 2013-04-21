#####################################################################
###############       list    functions              ################
#####################################################################
	
def cons( e, L ):
	'''returns a new list, with element e prepended to the front of list L '''
	L.insert(0, e)
	return L
	
def car( L ):
	''' returns the first element in the list '''
	try:
		return L[0]
	except:
		print "No elements left in the list to return"

def cdr( L ):
	''' returns the rest of the list (minus the first element) '''
	try:
		return L[1:]
	except:
		print "There is 1 or 0 elements in the list."

def nullp( L ):
	''' returns 1 if L is null, 0 otherwise '''
	if len(L) > 0:
		return 1
	return 0
	
def intp( e ):
	'''returns 1 if e is an integer, 0 otherwise '''
	if isinstance( e, int ):
		return 1
	return 0
	
def listp( e ):
	'''returns 1 if e is a list, 0 otherwise'''
	if isinstance( e, list ):
		return 1
	return 0
