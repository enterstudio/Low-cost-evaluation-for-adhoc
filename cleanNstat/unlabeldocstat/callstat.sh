START=$(date +%s.%N)
echo "current pid:" $$
qreld=/GW/D5data-2/khui/qrel/completeqrel/adhoc/perquery
trecruns=/GW/D5data-2/khui/trecrun/adhoc/orignialruns/perquery
featurefile=/GW/D5data-2/khui/features/termweight/adhoc/perquery
outdir=/home/khui/workspace/script/pythonscript/2stagecluster/main/comparativestudy/cleanNstat/outdir
(
for qid in {201..250}
do
	if [ -e $qreld/$qid ] && [ -e $trecruns/$qid ]
		#[ -e $featurefile/$qid ] && [ -e $qreld/$qid ] && [ -e $trecruns/$qid ]
	then
	#	python statmisscwid.py -f $featurefile/$qid -q $qid -r $trecruns/$qid -j $qreld/$qid >> $PWD/misscwidINfeature.out
		python statunlabel.py -q $qid -r $trecruns/$qid -j $qreld/$qid -o $outdir/unlabeledcwidsnn.out >> \
			$outdir/statnonlabeln.out &
	fi
done
wait
)
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo output stat finished: $DIFF
