START=$(date +%s.%N)
echo "current pid:" $$ `hostname`

timestamp=`date +%y%m%d%H%M`
#statAP statAPl
task=statAPl
trecrun=/GW/D5data-2/khui/trecrun/adhoc/normrun30qrel/perquery
qrelf=/GW/D5data-2/khui/qrel/completeqrel/adhoc/perquery
outputfolder=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/$task/qrels
outipfolder=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/$task/prels
samplerates="0.01 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0.15 0.25 0.35 0.45 0.55 0.65 0.75 0.85 0.95"
#"0.01 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95"

#if [ -d $outputfolder ];
#then
#	echo 'removing ' $outputfolder
#	rm -rf $outputfolder
#fi
#if [ -d $outipfolder ];
#then
#	echo 'removing ' $outipfolder
#	rm -rf $outipfolder
#fi

step=50
for percent in $samplerates
do
	for sid in `seq 1 30`
	do
		mkdir -p $outputfolder/$percent/$sid
		mkdir -p $outipfolder/$percent/$sid
		for sq in `seq 201 $step 300`
        	do
			if [ $sq -gt 300 ]
			then
				break
			fi
                (
                        for (( qid=$sq;qid-$sq<$step;qid++ ))
                        do
				if [ $sq -gt 300 ]
				then
					break
				fi
				(
				python $PWD/${task}.py \
					-q $qid \
					-r $trecrun/$qid \
					-o $outputfolder/$percent/$sid \
					-j $qrelf/$qid \
					-p $percent \
					-i $outipfolder/$percent/$sid \
					-a 0.5
				)&
			done
			wait
			echo finished `hostname` from $sq to $qid, with $percent $sid
		)
		done
	done
done

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo "finished: "$DIFF
