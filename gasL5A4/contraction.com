

# Define parameters,regions,and coordinate system
fem def para;r;DTI
fem def coord;r;DTI
fem def bases;r;DTI

$REG=1;

######################################################muscles
# muscle_list
@muscle_list = ('gas');
foreach $component (@muscle_list)
{ 
#Read in muscle
fem def nodes;r;simulate_$component  reg $REG
fem def elements;r;simulate_$component  reg $REG

# Define muscle fibre field (nj 4,5,6)
fem def fibre;r;fitted_TD_DTI reg $REG
fem def elements;r;simulate_$component fibre reg $REG

fem export nodes;init_gas as gas reg 1
fem export elements;init_gas as gas reg 1

if ($REG==1){fem group nodes 1..24,61..68,73,75,81,83 as FIXED reg $REG}
if ($REG==1){fem group nodes 1..96 as ALL reg $REG}

fem group elements 1,2,5..8,31..42 as TEN
fem group elements 3,4,9..30 as MUS

fem group nodes 25..27,35..40,48..49,57..60,69..72,84..89 as BNDRY

fem group nodes 61..68,73,75,81,83 as BTM

# Muscle (active contraction + contact option)
fem def equa;r;simulate_$component reg $REG
fem def mapping;r;gastroc reg $REG
fem def mate;r;simulate_$component reg $REG
fem def init;r;simulate_$component reg $REG
fem def acti;r;simulate_$component reg $REG 
fem def solve;r;contraction reg $REG

# Export initial muscle
fem exp nodes;init_simulate_$component as $component reg $REG
fem exp elements;init_simulate_$component as $component reg $REG

}

# lengthen tendon
fem def init;r;len20 reg $REG
for($k=1;$k<=8;$k++)
{
fem solve error 1.0D-03 increment 0.1 iterate 8 reg $REG
}

# solve contraction
for($k=1;$k<=6;$k++)
{
fem def acti;r;simulate_gas$k reg $REG 
fem solve error 1.0D-03 increment 0 iterate 8 reg $REG
}

# outputs opstre
fem list stress;gastroc_stress full
fem list Strain;gastroc_Strain full

# update XP from YP
FEM up geom from sol to 1..3 reg $REG

# Export final deformed mesh 

# solution_list
@solution_list = ('gas');
foreach $component(@solution_list)
{
fem exp nodes;def_$component as $component region $REG
fem exp elem;def_$component as $component region $REG
}

fem def nodes;w;def_gas
fem def elements;w;def_gas

fem list nodes reaction nodes FIXED
fem list nodes;node_reaction reaction 

exit

