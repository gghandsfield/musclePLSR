
# Define parameters,regions,and coordinate system
fem def para;r;DTI
fem def coord;r;DTI
fem def bases;r;DTI

$REG=1;

######################################################muscles

#Read in muscle
fem def nodes;r;def_gas_DTI  reg $REG
fem def elements;r;def_gas  reg $REG

fem ref xi 1 at 0.5 ntimes 2
fem ref xi 2 at 0.5 ntimes 2

fem export nodes;gas_target as gas


