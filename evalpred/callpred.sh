START=$(date +%s.%N)
echo "current pid:" $$
#rndsample, mtc, pooling/trecpool, pooling/incrementalpool 
task=$1
directory=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/$1
directorytojud=$(find $directory/qrels -name "*.pqrel" -printf "%h\n" | sort -u)
fullqrel=/GW/D5data-2/khui/qrel/completeqrel/adhoc/qrels.adhoc.wt
outdir=$directory/predeval
outf=$outdir/pred

mkdir -p $outdir
#if [[ -e "$outf" ]];
#then
#	echo "deleting exist folder $outf"
#	rm $outf
#fi

pidarray=()
# predict evaluation with trec setting
(
for qreld in $directorytojud;
do

	(
		outstr=$(python $PWD/evalpred.py -f $fullqrel -q $qreld)
		for year in 13 14 12 11 10
			#09 10 11 12
		do
			if [ "$task" == "rndsample" ] || [ "$task" == "statAPl" ]
			then
				percent=$(echo $qreld|awk -F/ '{print $(NF-1)}')
				sid=$(echo $qreld|awk -F/ '{print $NF}')
				qrelname=$year"-"$percent"-"$sid
			else
				percent=$(echo $qreld|awk -F/ '{print $(NF)}')
				qrelname=$year"-"$percent
			fi
			echo -e $outstr | grep "^$year"|awk '{$1="'$qrelname'";print $0}' >> $outf
		done
		echo $qreld finished
	)&
done
wait
)
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo "$year finished: "$DIFF
