START=$(date +%s.%N)

#statAP statAPool
task=statAP
completeqrel=/GW/D5data-2/khui/qrel/completeqrel/adhoc/perquery
directory=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/$task
qrelfs=$directory/qrels
directorytojud=$(find $qrelfs -name "*.bqrel" -printf "%h\n" | sort -u)
outdir=$directory/evals
echo "current pid:" $$ `hostname`

for qreld in $directorytojud;
do
	(
	for qid in {201..300}
	do
		(
#		if [ -e $qid.bqrel ]
#		then
			python existcwids.py -i $qreld/$qid -q $qid -j $completeqrel/$qid
#		else
#			echo $qid.bqrel not exist
#		fi
		)&
	done
       	wait
	echo $qreld finished
	)
done
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo "$year finished: "$DIFF
