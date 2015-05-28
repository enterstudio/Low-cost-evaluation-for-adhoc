START=$(date +%s.%N)
echo "current pid:" $$

task=$1
directory=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/$task
#qrelfs=$directory/qrels
directorytojud=$(find $directory -name "*.bqrel" -printf "%h\n" | sort -u)
mtceval='/home/khui/workspace/evaltool/mtc-eval'
trecruns=/GW/D5data-2/khui/trecrun/adhoc/normrun30qrel/perquery
featurefile=/GW/D5data-2/khui/features/termweight/adhocn/perquery
step=25
for qreld in $directorytojud;
do
	for sqid in `seq 251 $step 300`
	do
		(
			for (( qid=$sqid;qid-$sqid<$step;qid++ ))
			do
				if [ -e $featurefile/$qid ] && [ -e $qreld/$qid".bqrel" ] && [ -e $trecruns/$qid ]
				then
					fname=$qid".bqrel"
				elif [ $task == "mtc" ]
				then
					percent=$(echo $qreld | awk -F/ '{print $NF}')
					if [ `echo $percent'=='1|bc -l` -eq 1 ]
					then
						doneqid=$(find $qreld -name "$qid-*.bqrel")
						if [ `echo $doneqid|wc -l` -eq 1 ]
						then
							fname=$(basename $doneqid)
						else
							echo skip qid:$qid for $qreld
							continue
						fi

					else
						echo skip qid:$qid for $qreld
						continue
					fi
				else
					echo skip qid:$qid for $qreld
					continue
				fi
				python $PWD/pred.py \
					-f $featurefile/$qid \
					-q $qid \
					-o $qreld \
					-j $qreld/$qid".bqrel" \
					-r $trecruns/$qid &
			done
			wait
		)
	done
	echo $qreld finished
done

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo output predict $task finished: $DIFF
