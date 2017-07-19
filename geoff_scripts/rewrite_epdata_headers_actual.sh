# this file for replace header of each exdata file with header from test.exdata

cd ~/musclePLSR/ju_scripts/data/nonlinplsr_actual_strain

for L_index in {1..6}
do

for A_index in {1..5}
do

( head -44 test.exdata; tail -n+43 actual_strainL${L_index}A${A_index}.exdata) > temp.exdata
( head -1 actual_strainL${L_index}A${A_index}.exdata; tail -n+2 temp.exdata) > dummy.exdata 
mv dummy.exdata actual_strainL${L_index}A${A_index}.exdata

done
done
