START=$(date +%s.%N)

#statAPl rndsample, mtc, pooling/trecpool, pooling/incrementalpool
task=$1
directory=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/$1

tmpdir=/scratch/GW/pool0/khui/tmp/measure4/`basename $directory`
qrelfs=$directory/qrels
directorytojud=$(find $qrelfs -name "*.bqrel" -printf "%h\n" | sort -u)
outdir=$directory/evals
echo "current pid:" $$

trecrunfolder=/GW/D5data-2/khui/trecrun/adhoc/normrun30qrel
treceval=/home/khui/workspace/evaltool/trec_eval.9.0


for measure in tmap indap infap bpref
do
	if [[ -d "$outdir/$measure" ]];
	then
		echo "deleting exist folder $outdir/$measure"
		rm -rf $outdir/$measure
	fi
	mkdir -p "$outdir/$measure"
done

if [[ -d "$tmpdir" ]]
then
	echo "deleting exist folder $tmpdir"
	rm -rf $tmpdir
fi
mkdir -p $tmpdir

treceval(){
	# 1:qrel, 2:run 3:output
	# output: map P@20 R@20
	runname=$(head -1 $2 |awk '{print $6}')
	cd $treceval
	map=$(./trec_eval -m map $1 $2 | awk '{print $3}')
	indmap=$(./trec_eval -J -m map $1 $2 | awk '{print $3}')
	infmap=$(./trec_eval -m infAP $1 $2 | awk '{print $3}')
	bpref=$(./trec_eval -m bpref $1 $2 | awk '{print $3}')
	# output: runname, ndcg@20, err@20
#	measures=$(./gdeval.pl -c -k 20 $1 $2  | grep "amean" | awk -F, '{print $3" "$4}')
	echo $runname" "$map >> "$outdir/tmap/$3"
	echo $runname" "$indmap >> "$outdir/indap/$3"
	echo $runname" "$infmap >> "$outdir/infap/$3"
	echo $runname" "$bpref >> "$outdir/bpref/$3"
}

pidarray=()
# predict evaluation with trec setting
for qreld in $directorytojud;
do
	for year in 11 12 13 14 
	do
		if [ "$task" == "rndsample" ] || [ "$task" == "statAPl" ] || [ "$task" == "statAP" ]
		then
			percent=$(echo $qreld|awk -F/ '{print $(NF-1)}')
			sid=$(echo $qreld|awk -F/ '{print $NF}')
			qrelname=$year"-"$percent"-"$sid
		else
			percent=$(echo $qreld|awk -F/ '{print $(NF)}')
			qrelname=$year"-"$percent
		fi
		if [  "$task" == "mtc" ] && [  `echo $percent'=='1|bc -l` -eq 1 ]
		then
			continue
		fi
		qrelf=$(echo $tmpdir/$qrelname)
		if [ $year -eq 09 ]
		then
			(
			for qid in {1..50}
			do
				if [ -e $qreld/$qid.bqrel ]
				then
					cat $qreld/$qid.bqrel | sort -u
				elif [  "$task" == "mtc" ]
				then
                                        doneqid=$(find $donedir -name "$qid-*.bqrel")
                                        if [ `echo $doneqid|wc -l` -eq 1 ]
                                        then
                                                cat $doneqid | sort -u
                                        fi
				fi
			done
			) >> $qrelf
		elif [ $year -eq 10 ]
		then
			(
			for qid in {51..100}
			do
				if [ -e $qreld/$qid.bqrel ]
				then
					cat $qreld/$qid.bqrel | sort -u
				elif [  "$task" == "mtc" ]
				then
                                        doneqid=$(find $donedir -name "$qid-*.bqrel")
                                        if [ `echo $doneqid|wc -l` -eq 1 ]
                                        then
                                                cat $doneqid | sort -u
                                        fi
				fi
			done
			) >> $qrelf
		elif [ $year -eq 11 ]
		then
			(
			for qid in {101..150}
			do
				if [ -e $qreld/$qid.bqrel ]
				then
					cat $qreld/$qid.bqrel | sort -u
				elif [  "$task" == "mtc" ]
				then
                                        doneqid=$(find $donedir -name "$qid-*.bqrel")
                                        if [ `echo $doneqid|wc -l` -eq 1 ]
                                        then
                                                cat $doneqid | sort -u
                                        fi
				fi
			done
			) >> $qrelf
		elif [ $year -eq 12 ]
		then
			(
			for qid in {151..200}
			do
				if [ -e $qreld/$qid.bqrel ]
				then
					cat $qreld/$qid.bqrel | sort -u
				elif [  "$task" == "mtc" ]
				then
                                        doneqid=$(find $donedir -name "$qid-*.bqrel")
                                        if [ `echo $doneqid|wc -l` -eq 1 ]
                                        then
                                                cat $doneqid | sort -u
                                        fi
				fi
			done
			) >> $qrelf
		elif [ $year -eq 13 ]
		then
			(
			for qid in {201..250}
			do
				if [ -e $qreld/$qid.bqrel ]
				then
					cat $qreld/$qid.bqrel | sort -u
				elif [  "$task" == "mtc" ]
				then
                                        doneqid=$(find $donedir -name "$qid-*.bqrel")
                                        if [ `echo $doneqid|wc -l` -eq 1 ]
                                        then
                                                cat $doneqid | sort -u
                                        fi
				fi
			done
			) >> $qrelf
		elif [ $year -eq 14 ]
		then
			(
			for qid in {251..300}
			do
				if [ -e $qreld/$qid.bqrel ]
				then
					cat $qreld/$qid.bqrel | sort -u
				elif [  "$task" == "mtc" ]
				then
                                        doneqid=$(find $donedir -name "$qid-*.bqrel")
                                        if [ `echo $doneqid|wc -l` -eq 1 ]
                                        then
                                                cat $doneqid | sort -u
                                        fi
				fi
			done
			) >> $qrelf
		fi
		(
			for trecrun in `ls $trecrunfolder/$year`;
			do
				#ndeval for the original list
				treceval "$qrelf"  "$trecrunfolder/$year/$trecrun" \
					"${qrelname}" &
			done
			wait
			echo $qrelname done
		)
	done
done
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo "$year finished: "$DIFF
