START=$(date +%s.%N)

task=statAP
directory=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/$task
evaldir=$directory/evals
fulleval=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/mtc/evals/indap
outdir=$directory/corrs
#if [ -d $outdir ]
#then
#	echo removing $outdir
#	rm -rf $outdir
#fi
mkdir -p $outdir/kendalltau $outdir/pearsonr
#measures=( bpref indap infap tmap )
measures=( statap )
(
for evalm in ${measures[@]}
do
	(
	echo $evaldir $evalm
	for evalf in `ls $evaldir/$evalm`
	do
		if [ `echo $evalf | awk -F- '{print NF}'` -lt 2 ]
		then
			continue
		fi
		if [ `head -n 1 $evaldir/$evalm/${evalf} | awk '{print NF}'` -le 1 ]
		then
			echo "ERROR: $evalm $evalf"
			continue
		fi
		year=$(echo $evalf | awk -F- '{print $1}')
		sid=$(echo $evalf | awk -F- '{print $3}')
		percent=$(echo $evalf | awk -F- '{print $2}')
		echo "INFO: Computing correlation for $evalm $evalf"
		corrres=$(
			python $PWD/pairwisecorr.py \
				-o $fulleval/${year}"-"${percent} \
				-x $evaldir/$evalm/${evalf})
		kendalltau=$(echo $corrres | awk '{print $1}')
		pearsonr=$(echo $corrres | awk '{print $2}')
		echo -e $evalf"\t"$kendalltau >> $outdir/kendalltau/mitmtc.corr
		echo -e $evalf"\t"$pearsonr >> $outdir/pearsonr/mitmtc.corr
	done
	)&

done
wait
)
		
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo "$year finished: "$DIFF
