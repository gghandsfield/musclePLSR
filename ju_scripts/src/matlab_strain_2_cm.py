"""
Script to convert Matlab-generate strain files to cmiss files

To be used by data in strain_pred_20170712

In each row, each group of 15 data entries correspond to the following for a node

    Principal_1
    Principal_2
    Principal_3
    VonMises
    Hydrostatic
    Octahedral
    PrincipalVector1 x
    PrincipalVector1 y
    PrincipalVector1 z
    PrincipalVector2 x
    PrincipalVector2 y
    PrincipalVector2 z
    PrincipalVector3 x
    PrincipalVector3 y
    PrincipalVector3 z

"""

import numpy as np
import cmissio

#=========================================================================#
# constants
ACTIVATIONS = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
LENGTHS = (380, 384, 388, 392, 396, 400)
STRAIN_TEMPLATE_FILESTR = '../data/strain/strainL{}A{}.exdata'
STRAIN_FIELDS = [8,9,10,11,12,13,14,15,16]
STRAIN_FIELD_COMPONENTS = [1,1,1,1,1,1,3,3,3]

# parameters
skips = [(400, 1.0),(396, 1.0),(392, 1.0),(388, 1.0), (384, 1.0),(380, 1.0)]    # observations to skip, outliers
plsrK = 2               # number of plsr modes (1 or 2)
responseName = 'geometry'   #'geometry', 'stress', or 'strain'
xvalK = 36 - len(skips) # number of folds for k-fold cross validation. For leave 1 out, this 
                        # should be the number of observations

#=========================================================================#
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

def writeStrain(X, fname, header):
    fields = _wrapExdata(X, STRAIN_FIELD_COMPONENTS)
    cmissio.writeExdata(STRAIN_TEMPLATE_FILESTR.format(l, a),
                        fname,
                        header,
                        fields,
                        STRAIN_FIELDS)

#=========================================================================#
# input_fn = '../../strain_pred_20170712/pred_strain.txt'
# out_fn = '../../strain_pred_20170712/pred_exdata/pred_strainL{}A{}.exdata'
# out_header = 'predicted_strain_L{}A{}'

input_fn = '../../strain_pred_20170712/strain.txt'
out_fn = '../../strain_pred_20170712/actual_exdata/actual_strainL{}A{}.exdata'
out_header = 'actual_strain_L{}A{}'

file_data = np.loadtxt(input_fn, delimiter=',') # shape 30,15*nodes

# generate length and activations for each simulation
LA = []
for i, l in enumerate(LENGTHS):
    for j, a in enumerate(ACTIVATIONS):
        if (l, a) not in skips:
            # LA.append([l, a])
            LA.append([i+1, j+1])

# for each row (simulation)
for i, d in enumerate(file_data):
    l, a = LA[i]
    writeStrain(d, out_fn.format(l, a), out_header.format(l, a))
