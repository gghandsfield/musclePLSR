""" functions and/or classes for reading and writing cmiss files:
ip/ex data
ip/ex node

Ju Zhang
06-Jan-2010
"""

import os
from numpy import array, arange

#======================================================================#
def readIpdata( fileName ):
	""" reads ipdata file and returns the x y z coords on data points
	and the header if there is one
	"""
	
	try:
		file = open( fileName, 'r' )
	except IOError:
		print 'ERROR: readIpdata: unable to open', fileName
		return
	
	header = None
	lines = file.readlines()
	if lines[0][0] != ' ':
		header = lines[0]
		del lines[0]
	
	coords = []
	nodeNumbers = []
	for l in lines:
		words = l.split()
		coords.append(array(words[1:4], dtype=float))
		nodeNumbers.append(int(words[0]))
	coords = array(coords)
	nodeNumbers = array(nodeNumbers)	

	return coords, nodeNumbers, header

#======================================================================#
def writeIpdata(d, filename, header=None, nodeNumbers=None):
	""" write the coordinates of points in 3D space to ipdata file. Each
	row in d is [x,y,z] of a datapoint. filename is a string, header is
	a string. if ex!=False, uses cmConvert to conver to ex formates. ex 
	can be 'data', 'node' or 'both'
	"""
	
	outputFile = open( filename, 'w')
	if header:
		outputFile.write( header+'\n' )
	
	if nodeNumbers is None:
		nodeNumbers = arange(len(d))

	for i, di in enumerate(d):
		outputFile.write("%10i %3.10f %3.10f %3.10f 1.0 1.0 1.0\n"%(nodeNumbers[i], di[0], di[1], di[2]))
	outputFile.close()

	return

#======================================================================#
def readIpnode( fileName, extra=False ):
	""" reads ipnode node files and returns a list of node parameters,
	if extra=True, also returns a list of whether each parameter is a 
	value or derivative, and a list of the node number of parameter
	"""
	
	try:
		file = open( fileName, 'r' )
	except IOError:
		print 'ERROR: ipnode_reader: unable to open', fileName
		return
	
	parameters = []
	parameterType = []
	node = []
	currentNode = None
	
	if extra:
		for line in file.readlines():
			if line.find('Node number')!=-1:
				currentNode = int( line.strip().split()[-1] )
				
			if line.find('Xj')!=-1: 
				parameters.append( float(line.strip().split()[-1]) )
				parameterType.append( 'value' )
				node.append( currentNode )
			elif line.find('The derivative')!=-1:
				parameters.append( float(line.strip().split()[-1]) )
				parameterType.append( 'derivative' )
				node.append( currentNode )
	else:
		for line in file.readlines():
			if ( line.find('Xj')!=-1 ) or ( line.find('The derivative')!=-1 ):
				parameters.append( float(line.strip().split()[-1]) )
				
	file.close()
	
	if extra:	
		return array(parameters), parameterType, node
	else:
		return array(parameters)
	
#======================================================================#
def writeIpnode(templateName, writeName, header, data):
	""" writes mesh parameters in data to an ipnode file based on a 
	template ipnode file
	"""
	
	s = '%21.14f'

	try:
		template = open( templateName, 'r' )
	except IOError:
		print 'ERROR: writeIpnode: unable to open template file', templateName
		return
	
	try:
		writeFile = open( writeName, 'w' )
	except IOError:
		print 'ERROR: writeIpnode: unable to open write file', writeName
		return
		
	dataCount = 0
	for line in template.readlines():
		if line.find('Heading')!=-1:
			writeFile.write( line.split(':')[0] + ': ' + header + '\n' )
		elif ( line.find('Xj')!=-1 ) or ( line.find('The derivative')!=-1 ):
			writeFile.write( line.split(':')[0] + ': ' + s%(data[dataCount]) + '\n' )
			dataCount += 1
		else:
			writeFile.write( line )
	
	template.close()
	writeFile.close()
	
	return

#======================================================================#
def readExdata(filename, fieldsToRead=None):
	"""Reads exdata file and returns the descriptions of fields and the 
	field values themselves for each data point. If the fieldsToRead are not
	defined as input list, all fields are returned.
	"""

	try:
		f = open(filename, 'r')
	except IOError:
		print 'ERROR: unable to open', filename
		return

	# read header
	header = f.readline()

	# read number of fields
	nFieldsLine = f.readline()
	nFields = int(nFieldsLine.strip().split('=')[-1])

	# read fields
	fields = []
	readingFields = True
	while readingFields:
		l = f.readline()
		if 'Node:' in l:
			readingFields = False
			readingValues = True
		elif ')' in l:
			fields.append(l)
		else:
			fields[-1] = fields[-1]+l

	if fieldsToRead is None:
		fieldsToRead = set(range(1,nFields+1))
	else:
		fieldsToRead = set(fieldsToRead)

	# read field values
	values = []
	nodes = []
	currentField = nFields+1
	while readingValues:
		if 'Node:' in l:
			nodes.append(int(l.strip().split(':')[-1]))
			currentField = 1
			values.append([])
		elif currentField<=nFields:
			if currentField in fieldsToRead:
				v = [float(x) for x in l.strip().split()]
				if len(v)>1:
					values[-1].append(v)
				else:
					values[-1].append(v[0])
			currentField+=1
		
		try:
			l = f.next()
		except StopIteration:
			readingValues = False


	return header, fields, nodes, values

#======================================================================#
def writeXYZ( data, filename, header=None ):
	""" writes 3D coords of point to file. Each line contains the x, y,
	and z coords of a point. Optional head in the 1st line
	"""
	
	fOut = open( filename, 'w' )
	if header:
		fOut.write( header+'\n' )
		
	for d in data:
		fOut.write( "%(x)10.6f\t%(y)10.6f\t%(z)10.6f\n" %{'x':d[0], 'y':d[1], 'z':d[2]})

	fOut.close()
	
	return 1
