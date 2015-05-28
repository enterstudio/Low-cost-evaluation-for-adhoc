START=$(date +%s.%N)

#statAP statAPool
task=$1
trecrun=/GW/D5data-2/khui/trecrun/adhoc/normrun30qrel/perquery
featurefile=/GW/D5data-2/khui/features/termweight/adhocn/perquery
completeqrel=/GW/D5data-2/khui/qrel/completeqrel/adhoc/perquery
directory=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/$task
qrelfs=$directory/qrels
directorytojud=$(find $qrelfs -name "*.bqrel" -printf "%h\n" | sort -u)
outdir=$directory/evals
echo "current pid:" $$ `hostname`

step=25
for qreld in $directorytojud;
do
	for sqid in `seq 201 $step 300`
        do
                (
                for (( qid=$sqid; qid-$sqid<$step; qid++ ))
                do
			(
			python existcwids.py -i $qreld/$qid -q $qid -j $completeqrel/$qid
			python $PWD/pred.py \
				-f $featurefile/$qid \
				-q $qid \
				-o $qreld \
				-j $qreld/$qid".bqrel" \
				-r $trecrun/$qid
			)&
		done
		wait
		echo $qreld $sqid $step finished
		)
	done
done
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo "$year finished: "$DIFF
