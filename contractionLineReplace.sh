# this file for replace DTI_gastroc_fibre with fitted_TD_DTI in contraction.com file

for L_index in {1..6}
do

for A_index in {1..6}
do

cd gasL${L_index}A${A_index}
sed -i -e 's/DTI_gastroc_fibre/fitted_TD_DTI/g' contraction.com;

cd ..

done
done
