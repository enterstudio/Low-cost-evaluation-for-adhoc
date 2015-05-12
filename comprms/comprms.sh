START=$(date +%s.%N)

task=$1
directory=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/$task
evaldir=$directory/evals
fulleval=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/fullqrel
outdir=$directory/rmse
if [ -d $outdir ]
then
	echo removing $outdir
#	rm -rf $outdir
fi
mkdir -p $outdir
measures=( bpref indap infap tmap )
#measures=( statap )
#measures=( uniemap )
#measures=( pmapn )

(
for evalm in ${measures[@]}
do
	if [ ! -d $evaldir/$evalm ]
	then
		echo $evaldir $evalm not exist and skip
		continue
	fi
	(
	echo $evaldir $evalm
	for evalf in `ls $evaldir/$evalm`
	do
		if [ `echo $evalf | awk -F- '{print NF}'` -lt 2 ]
		then
			continue
		fi
		year=$(echo $evalf | awk -F- '{print $1}')
#		if [ $year != 14 ]
#		then
#			continue
#		fi
		echo "INFO: Computing RMSE for $evalm $evalf"
		if [ `head -n 1 $evaldir/$evalm/${evalf} | awk '{print NF}'` -le 1 ]
		then
			echo "ERROR: $evalm $evalf"
			continue
		fi
		rmse=$(
			python $PWD/pairwiserms.py \
				-o $fulleval/${year}map \
				-x $evaldir/$evalm/${evalf})
		echo -e $evalf"\t"$rmse >> $outdir/$evalm.rms
	done
	)&

done
wait
)
		
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo "$year finished: "$DIFF
