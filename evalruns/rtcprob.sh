START=$(date +%s.%N)
echo "current pid:" $$

task=$1
directory=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/$task
tmpdir=/scratch/GW/pool0/khui/tmp/rtcprob/$task
qrelfs=$directory/qrels
directorytojud=$(find $qrelfs -name "*.bqrel" -printf "%h\n" | sort -u)
mtceval='/home/khui/workspace/evaltool/mtc-eval'
trecruns=/GW/D5data-2/khui/trecrun/adhoc/normrun30qrel
ereloutdir=$directory/rtcprob
erellogdir=$ereloutdir/log
if [ -e $ereloutdir ]
then
	echo removing $ereloutdir
	rm -rf $ereloutdir
fi
mkdir -p $ereloutdir $erellogdir

if [[ -d "$tmpdir" ]]
then
        echo "deleting exist folder $tmpdir"
        rm -rf $tmpdir
fi
mkdir -p $tmpdir


for qreld in $directorytojud;
do
	(
	for year in 09 10 11 12
	do
		(
		if [ "$task" == "rndsample" ]
		then
			sid=$(echo $qreld|awk -F/ '{print $NF}')
			percent=$(echo $qreld|awk -F/ '{print $(NF-1)}')
			qrelname=$year"-"$percent"-"$sid
		else
			percent=$(echo $qreld|awk -F/ '{print $(NF)}')
			qrelname=$year"-"$percent
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
				fi
			done
			) >> $qrelf
		fi
		$mtceval/expert -q $qrelf -d $trecruns/$year >$ereloutdir/$qrelname.erel 2>$erellogdir/$qrelname.log
		echo $qrelname $task finished
		)&
	done
	wait
	)
done


END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo output erel finished: $DIFF
