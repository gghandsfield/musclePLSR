"""
script for training and using SVR models of muscle contraction

Geoff Handsfield,
adapted from muscleplsr code written by Ju Zhang
"""

import numpy as np
from sklearn.pls import PLSRegression
from sklearn.svm import SVR # add line to import support vector regression functions -gh
import cmissio
import PCA

reload(cmissio)
#=========================================================================#
# constants
ACTIVATIONS = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
LENGTHS = (380, 384, 388, 392, 396, 400)
SHAPEFILESTR = '../data/shape_ipnode/gasL%dA%d.ipnode'
PREDSHAPEFILESTR = '../data/pred_shape_ipnode/pred_gasL%dA%d.ipnode'
STRAINFILESTR = '../data/strain/strainL%dA%d.exdata'
PREDSTRAINFILESTR = '../data/pred_strain/pred_strainL%dA%d.exdata'
STRESSFILESTR = '../data/stress/stressL%dA%d.exdata'
PREDSTRESSFILESTR = '../data/pred_stress/pred_stressL%dA%d.exdata'
STRESSFIELDS = [8,9,10,11,12,13,14,15,16]
STRAINFIELDS = [8,9,10,11,12,13,14,15,16]
STRESSFIELDCOMPONENTS = [1,1,1,1,1,1,3,3,3]
STRAINFIELDCOMPONENTS = [1,1,1,1,1,1,3,3,3]

# parameters
skips = [(400, 1.0),(396, 1.0),(392, 1.0),(388, 1.0), (384, 1.0),(380, 1.0)]	# observations to skip, outliers
svrK = 2 				# number of svr modes (1 or 2)
responseName = 'geometry'	#'geometry', 'stress', or 'strain'
xvalK = 36 - len(skips) # number of folds for k-fold cross validation. For leave 1 out, this 
						# should be the number of observations

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
	header, fields, nodes, values = cmissio.readExdata(filename, STRESSFIELDS)
	X = np.hstack([np.hstack(x) for x in values])
	return X

def _loadStrain(filename):
	"""Load strain variables from exdata file. Fields loaded are
	principal strains, principal directions, 3 scalar strains
	"""
	header, fields, nodes, values = cmissio.readExdata(filename, STRAINFIELDS)
	X = np.hstack([np.hstack(x) for x in values])
	return X

def makeXY(reponseName, skips=None):
	"""Returns the X matrix of all muscle lengths and activation
	Returns the Y matrix of either muscles geometry, stress, or strain.

	responseName is either 'geometry', 'stress', or 'strain'
	"""

	if skips is None:
		skips = []

	if responseName not in ['geometry', 'stress', 'strain']:
		raise ValueError, 'unsupported responseName'

	X = []
	Y = []
	for i, l in enumerate(LENGTHS):
		for j, a in enumerate(ACTIVATIONS):
			if (l, a) not in skips:
				X.append([l, a])
				if responseName=='geometry':
					Y.append(_loadGeometry(SHAPEFILESTR%(i+1, j+1)))
				elif responseName=='stress':
					Y.append(_loadStress(STRESSFILESTR%(i+1, j+1)))
				else:
					Y.append(_loadStrain(STRAINFILESTR%(i+1, j+1)))

	return np.array(X), np.array(Y)

#svr training (work in progress)
def svrTrain(X, Y, k):
	"""Train SVR model with k modes for predicting Y given X
	"""
	clf = SVR(C = 1.0, epsilon=0.2)
	clf.fit(X,Y)
	return clf

#svr prediction (work in progress)
def svrPredict(clf, X, realY):
	"""Given a SVR model clf, and independent variables X, predict
	Y, and calcualted difference to realY
	"""
	predY = clf.predict(X)
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

def _wrapExdata(X, fieldComponents):
	# wrap X into list of fields
	fields = []
	nFields = len(fieldComponents)
	fi = 0
	xi = 0
	while xi <= len(X):
		if fi==0:
			fields.append([])

		nComps = fieldComponents[fi]
		fields[-1].append(X[xi:xi+nComps])
		xi += nComps
		fi += 1

		if fi==nFields:
			fi = 0

	return fields

def _writeStress(X, l ,a):
	headerStr = 'predicted_stress_L%dA%d'
	fields = _wrapExdata(X, STRESSFIELDCOMPONENTS)
	cmissio.writeExdata(STRESSFILESTR%(l, a),
						PREDSTRESSFILESTR%(l, a),
						headerStr%(l, a),
						fields,
						STRESSFIELDS)

def _writeStrain(X, l ,a):
	headerStr = 'predicted_strain_L%dA%d'
	fields = _wrapExdata(X, STRAINFIELDCOMPONENTS)
	cmissio.writeExdata(STRAINFILESTR%(l, a),
						PREDSTRAINFILESTR%(l, a),
						headerStr%(l, a),
						fields,
						STRAINFIELDS)

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
X, Y = makeXY(responseName, skips)

#=================#
# Exploratory PCA #
#=================#
# do PCA
p = PCA.PCA()
p.setData(Y.T)
p.svd_decompose()
pc = p.PC

PCA.plotSpectrum(pc, 10, responseName)
labels = ['L%dA%2.1f'%(l,a) for (l,a) in X]
PCA.plotModeScatter(pc, 0, 1, None, labels, nTailLabels='all')

# cross validation
# cv = PCA.CrossValidator(Y.T, 5)
# l1o = cv.leaveOneOut()
# l1oRMSES = [np.sqrt((e**2.0).mean()) for e in l1o]
# meanRMSE = np.mean(l1oRMSES)

#=========================#
# SVR with leave one out #
#=========================#
rmses = []
xvalInds = makeKFoldIndices(range(X.shape[0]), xvalK)
for testInd, trainInd in xvalInds:
	trainX = X[trainInd,:]
	trainY = Y[trainInd,:]
	testX = X[testInd,:]	
	testY = Y[testInd,:]

	# train svr model
	clf = svrTrain(trainX, trainY,svrK)
	# make prediction
	pY, dY = svrPredict(clf, testX, testY)
	rmses.append(np.sqrt((dY**2.0).mean()))
	# write prediction to file
	writePredictions(pY, responseName, testX)

print 'SVR L1O Mean RMSE:', np.mean(rmses)
