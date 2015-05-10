START=$(date +%s.%N)
echo "current pid:" $$
qreld=/GW/D5data-2/khui/qrel/completeqrel/adhoc/perquery
trecruns=/GW/D5data-2/khui/trecrun/adhoc/orignialruns/perquery
featurefile=/GW/D5data-2/khui/features/termweight/adhoc/perquery
outdir=/GW/D5data-2/khui/trecrun/adhoc/normrun30qrel/perqueryn
if [ -d $outdir ]
then
	echo removing $outdir
	rm -rf $outdir
fi
mkdir -p $outdir
(
for qid in {201..250}
do
	if [ -e $qreld/$qid ] && [ -e $trecruns/$qid ]
	then
		python condensetrecrun.py -q $qid -r $trecruns/$qid -j $qreld/$qid -o $outdir/$qid &
		echo $qid finished
	fi
done
wait
)
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo output stat finished: $DIFF
