# this file for testing head and tail commands

cd ~/musclePLSR/ju_scripts/data/nonlinplsr_actual_strain
#head -n42 actual_strainL1A3.exdata | tail -n41 # this is the 2-42 lines of file

#(head -n44 test.exdata | tail -n43)

( head -44 test.exdata; tail -n+43 actual_strainL1A3.exdata) > temp.exdata
( head -1 actual_strainL1A3.exdata; tail -n+2 temp.exdata) > dummy.exdata && mv dummy.exdata actual_strainL1A3.exdata




