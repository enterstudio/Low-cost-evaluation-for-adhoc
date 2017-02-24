for wn in aones entropy kld srk
do
	for kn in cosine linear rbf
	do
		(python compqrels.greedysimi.py $wn $kn)&
		arr+=($!)
	done
done
echo wait for everything finish
for i in ${arr[@]}
do
	echo wait for $i
	wait $i
done
echo everything finished



