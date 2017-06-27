

# Define parameters,regions,and coordinate system
fem def para;r;DTI
fem def coord;r;DTI
fem def bases;r;DTI

$REG=1;

#Read in muscle
#fem def nodes;r;def_gas 
#fem def elements;r;def_gas
#fem export nodes;orig_gas as gas 
#fem export elem;orig_gas as gas 

fem def nodes;r;pred_gasL3A3 
fem export nodes;pred_gas as gas 
