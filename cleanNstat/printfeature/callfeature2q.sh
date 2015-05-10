START=$(date +%s.%N)
echo "current pid:" $$
qreld=/GW/D5data-2/khui/qrel/completeqrel/adhoc/perquery
featurefile=/GW/D5data-2/khui/features/termweight/adhocn/tfidffeaturecw12.out
outdir=/GW/D5data-2/khui/features/termweight/adhocn/perqueryn
mkdir -p $outdir
(
for qid in {201..300}
do
	if [ -e $qreld/$qid ]
	then
		python feature2query.py -f $featurefile -q $qid  -j $qreld/$qid -o $outdir &
	fi
done
wait
)
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo output stat finished: $DIFF
