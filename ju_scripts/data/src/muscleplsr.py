"""
script for training and using PLSR models of muscle contraction

Ju Zhang
"""

import numpy as np
from sklearn.pls import PLSRegression
import cmissio

#=========================================================================#
# constants
ACTIVATIONS = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
LENGTHS = (380, 384, 388, 392, 396, 400)
SHAPEFILESTR = '../shape_ipnode/gasL%dA%d.ipnode'
PREDSHAPEFILESTR = '../pred_shape_ipnode/pred_gasL%dA%d.ipnode'
STRAINFILESTR = '../strain/strainL%dA%d.exdata'
PREDSTRAINFILESTR = '../pred_strain/pred_strainL%dA%d.exdata'
STRESSFILESTR = '../stress/stressL%dA%d.exdata'
PREDSTRESSFILESTR = '../pred_stress/pred_stressL%dA%d.exdata'
STRESSFIELDS = [8,9,10,11,12,13,14,15,16]
STRAINFIELDS = [8,9,10,11,12,13,14,15,16]

# parameters
plsrK = 2 	# number of plsr modes (1 or 2)
responseName = 'geometry'	#'geometry', 'stress', or 'strain'
xvalK = 36 	# number of folds for k-fold cross validation. 36 folds = leave one out

#=========================================================================#
def _loadGeometry(filename):
	"""Load coordinates field values and derivatives from ipnode file.
	"""
	X, XType, nodes = cmissio.readIpnode(filename, extra=True)
	return X

def _loadStress(filename):
	"""Load stress variables from exdata file. Fields loaded are
	principal stresses, principal directions, 3 scalar stresses
	"""
	header, fields, nodes, values = cmissio.readExdata(
										filename, STRESSFIELDS)
	X = np.hstack([np.hstack(x) for x in values])
	return X

def _loadStrain(filename):
	"""Load strain variables from exdata file. Fields loaded are
	principal strains, principal directions, 3 scalar strains
	"""
	header, fields, nodes, values = cmissio.readExdata(
										filename, STRAINFIELDS)
	X = np.hstack([np.hstack(x) for x in values])
	return X

def makeXY(reponseName):
	"""Returns the X matrix of all muscle lengths and activation
	Returns the Y matrix of either muscles geometry, stress, or strain.

	responseName is either 'geometry', 'stress', or 'strain'
	"""
	if responseName not in ['geometry', 'stress', 'strain']:
		raise ValueError, 'unsupported responseName'

	X = []
	Y = []
	for i, l in enumerate(LENGTHS):
		for j, a in enumerate(ACTIVATIONS):
			X.append([l, a])
			if responseName=='geometry':
				Y.append(_loadGeometry(SHAPEFILESTR%(i+1, j+1)))
			elif responseName=='stress':
				Y.append(_loadStress(STRESSFILESTR%(i+1, j+1)))
			else:
				Y.append(_loadStrain(STRAINFILESTR%(i+1, j+1)))

	return np.array(X), np.array(Y)

def plsTrain(X, Y, k):
	"""Train PLSR model with k modes for predicting Y given X
	"""
	pls = PLSRegression(n_components=k)
	pls.fit(X, Y)
	return pls

def plsPredict(pls, X, realY):
	"""Given a PLSR model pls, and independent variables X, predict
	Y, and calculated difference to realY
	"""
	predY = pls.predict(X)
	dY = realY - predY
	return predY, dY

def makeKFoldIndices(I, k):
	"""Generate testing and training observation indices for k-fold 
	cross validation.
	
	I is a list of observation numbers, k is the number of folds.
	If k==len(I), the indices generated for be for a leave-one-out
	test

	Returns a list of length k of testing and training indices:
	[(testing indices, training indices), ...]
	"""
	inds = []
	I = np.array(I)
	valSize = len(I)/k
	for ki in xrange(k):
		val = I[ki*valSize:(ki+1)*valSize].copy()
		train = np.hstack([I[:ki*valSize], I[(ki+1)*valSize:]]).copy()
		inds.append((val, train))

	return inds

def _writeGeometry(X, l, a):
	"""Write predicted coordinates field values X to an ipnode file
	"""
	headerStr = 'predicted geometry L%dA%d'
	cmissio.writeIpnode(SHAPEFILESTR%(l, a),
						PREDSHAPEFILESTR%(l, a),
						headerStr%(l, a),
						X)


def writePredictions(X, responseName, LA):
	"""Write predicted data X to file.
	"""

	for x, (l, a) in zip(X,LA):
		if responseName=='geometry':
			_writeGeometry(x,
						   LENGTHS.index(l)+1,
						   ACTIVATIONS.index(a)+1
						   )
		elif responseName=='stress':
			_writeStress(x,
						 LENGTHS.index(l)+1,
						 ACTIVATIONS.index(a)+1
						 )
		elif responseName=='strain':
			_writeStrain(x,
						 LENGTHS.index(l)+1,
						 ACTIVATIONS.index(a)+1
						 )
		else:
			raise ValueError, 'unsupported responseName'

#=========================================================================#
# load data
X, Y = makeXY(responseName)

# do leave-one-out prediction test
xvalInds = makeKFoldIndices(range(36), xvalK)
for testInd, trainInd in xvalInds:
	trainX = X[trainInd,:]
	trainY = Y[trainInd,:]
	testX = X[testInd,:]	
	testY = Y[testInd,:]

	pls = plsTrain(trainX, trainY,plsrK)
	pY, dY = plsPredict(pls, testX, testY)

	writePredictions(pY, responseName, testX)