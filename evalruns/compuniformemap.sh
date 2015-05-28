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
emapoutdir=$directory/evals/uniemap
emaplogdir=$emapoutdir/log
if [ -e $emapoutdir ]
then
	echo removing $emapoutdir
	rm -rf $emapoutdir
fi
mkdir -p $emapoutdir $emaplogdir

#if [[ -d "$tmpdir" ]]
#then
#        echo "deleting exist folder $tmpdir"
#        rm -rf $tmpdir
#fi
#mkdir -p $tmpdir


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
		$mtceval/evaluate -o 2 \
			-q $qrelf \
			-d $trecruns/$year \
			2>$emaplogdir/$qrelname.log \
			1 | sed -n '/run eMAP eRprec eP5 eP10 eP15 eP20 eP30 eP100/,/^$/p' | awk 'NR>1 {print $1" "$2}'| sed '$d' \
			>$emapoutdir/$qrelname
		echo $qrelname $task finished
		)&
	done
	wait
	)
done


END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo output erel finished: $DIFF
