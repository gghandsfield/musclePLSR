# use this script to copy fitted_TD_DTI.ipfibr to all folders L1A1, L1A2,etc

for L_index in {1..6}
do

for A_index in {1..6}
do

cp fitted_TD_DTI.ipfibr gasL${L_index}A${A_index}

done
done
