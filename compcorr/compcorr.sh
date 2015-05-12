START=$(date +%s.%N)

task=$1
directory=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/$task
evaldir=$directory/evals
fulleval=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/fullqrel
outdir=$directory/corrs
if [ -d $outdir ]
then
	echo removing $outdir
#	rm -rf $outdir
fi
mkdir -p $outdir/kendalltau $outdir/pearsonr
measures=( bpref indap infap tmap )
#measures=( statap )
#measures=( uniemap )
#measures=( pmapn )

(
for evalm in ${measures[@]}
do
	(
	if [ ! -d $evaldir/$evalm ]
	then
		echo $evaldir $evalm not exist and skip
		continue
	fi
	echo $evaldir $evalm
	for evalf in `ls $evaldir/$evalm`
	do
		if [ `echo $evalf | awk -F- '{print NF}'` -lt 2 ]
		then
			continue
		fi
		year=$(echo $evalf | awk -F- '{print $1}')
#		if [ $year != 14 ]
#			#&& [ $year != 13 ] && [ $year != 14 ]
#		then
#			continue
#		fi
		echo "INFO: Computing correlation for $evalm $evalf"
		if [ `head -n 1 $evaldir/$evalm/${evalf} | awk '{print NF}'` -le 1 ]
		then
			echo "ERROR: $evalm $evalf"
			continue
		fi
		corrres=$(
			python $PWD/pairwisecorr.py \
				-o $fulleval/${year}map \
				-x $evaldir/$evalm/${evalf})
		kendalltau=$(echo $corrres | awk '{print $1}')
		pearsonr=$(echo $corrres | awk '{print $2}')
		echo -e $evalf"\t"$kendalltau >> $outdir/kendalltau/$evalm.corr
		echo -e $evalf"\t"$pearsonr >> $outdir/pearsonr/$evalm.corr
	done
	)&

done
wait
)
		
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo "$year finished: "$DIFF
