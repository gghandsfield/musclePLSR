for L_index in {1..6}
do

for A_index in {1..6}
do

cd gasL${L_index}A${A_index}

eval "cm contraction.com"

cd ..

done
done
