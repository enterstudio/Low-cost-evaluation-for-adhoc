START=$(date +%s.%N)

#statAP statAPool
task=statAP
directory=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/$task

tmpdir=/scratch/GW/pool0/khui/tmp/statap/comp`basename $directory`
qrelfs=$directory/prels
directorytojud=$(find $qrelfs -name "*.prel" -printf "%h\n" | sort -u)
outdir=$directory/evals
echo "current pid:" $$

trecrunfolder=/GW/D5data-2/khui/trecrun/adhoc/normrun30qrel
treceval='/home/khui/workspace/evaltool/mtc-eval'


for measure in statap
do
#	if [[ -d "$outdir/$measure" ]];
#	then
#		echo "deleting exist folder $outdir/$measure"
#		rm -rf $outdir/$measure
#	fi
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
	statmap=$(perl statAP_MQ_eval_v4.pl $1 $2 |grep 'statMAP_on_valid_topics'|awk -F= '{print $NF}');
	echo $runname" "$statmap >> "$outdir/statap/$3"
}

pidarray=()
# predict evaluation with trec setting
for qreld in $directorytojud;
do
	for year in 13 14
		#09 10 11 12
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
				if [ -e $qreld/$qid.prel ]
				then
					cat $qreld/$qid.prel | sort -u
				elif [  "$task" == "mtc" ]
				then
                                        doneqid=$(find $donedir -name "$qid-*.prel")
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
				if [ -e $qreld/$qid.prel ]
				then
					cat $qreld/$qid.prel | sort -u
				elif [  "$task" == "mtc" ]
				then
                                        doneqid=$(find $donedir -name "$qid-*.prel")
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
				if [ -e $qreld/$qid.prel ]
				then
					cat $qreld/$qid.prel | sort -u
				elif [  "$task" == "mtc" ]
				then
                                        doneqid=$(find $donedir -name "$qid-*.prel")
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
				if [ -e $qreld/$qid.prel ]
				then
					cat $qreld/$qid.prel | sort -u
				elif [  "$task" == "mtc" ]
				then
                                        doneqid=$(find $donedir -name "$qid-*.prel")
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
				if [ -e $qreld/$qid.prel ]
				then
					cat $qreld/$qid.prel | sort -u
				elif [  "$task" == "mtc" ]
				then
                                        doneqid=$(find $donedir -name "$qid-*.prel")
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
				if [ -e $qreld/$qid.prel ]
				then
					cat $qreld/$qid.prel | sort -u
				elif [  "$task" == "mtc" ]
				then
                                        doneqid=$(find $donedir -name "$qid-*.prel")
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
