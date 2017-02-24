START=$(date +%s.%N)

year=$1
predqrel=/scratch/GW/pool0/khui/result/2stagelowcost/maxsimweight/disagree
directorytojud=$(find $predqrel -name "*.qrel" -printf "%h\n" | sort -u)

resdir=/scratch/GW/pool0/khui/result/2stagelowcost/maxsimweight/disagree/qrelcorr/$year
task=disagree
computeCorrDir=/home/khui/workspace/script/pythonscript/2stagecluster/main/maxsimweight/stat
echo "current pid:" $$


trecrunfolder=/GW/D5data-2/khui/trecrun/adhoc/normrun100/$year
origbinary=/GW/D5data-2/khui/qrel/completeqrel/binary/qrels.adhoc.wt$year
original=/GW/D5data-2/khui/qrel/completeqrel/adhoc/qrels.adhoc.wt$year
tmpfolder="/scratch/GW/pool0/khui/tmp/$task/$year"
treceval=/home/khui/workspace/evaltool/trec_eval.9.0

resdir="$resdir"
if [[ -d "$resdir" ]];
then
	rm -rf $resdir
	echo "deleting exist folder $resdir"
fi
mkdir -p "$resdir"

if [[ -d "$tmpfolder" ]];
then
	rm -rf $tmpfolder;
	echo "deleting exist folder $tmpfolder"	
fi

mkdir -p $tmpfolder/intermediaeval
mkdir -p $tmpfolder/pqrel

ndeval(){
	#1:qrel, 2:run 3:output
	cd $ndevalfolder
	./ndeval $1 $2 | grep 'amean' | awk -F, '{print $1","$4","$13","$14","$22}' \
	>> "$tmpfolder/intermediaeval/$3"
}

treceval(){
	# 1:qrel, 2:run 3:output
	# output: map P@20 R@20
	runname=$(basename $2)
	cd $treceval
	measures=$(./trec_eval -c -J -m map_cut.20 -m P.20 -m recall.20 $1 $2 | awk '{print $1" "$3}')
	MAP=$(echo $measures | awk '{print $6}')
#	R20=$(echo $measures | awk '{print $4}')
#	P20=$(echo $measures | awk '{print $2}')
	# output: runname, ndcg@20, err@20
	measures=$(./gdeval.pl -c -k 20 $1 $2  | grep "amean" | awk -F, '{print $3" "$4}')
#	ndcg20=$(echo $measures | awk '{print $1}')
	err20=$(echo $measures | awk '{print $2}')
	echo $runname" "$err20" "$MAP >> "$tmpfolder/intermediaeval/$3"
}


# output format: runname ERR-IA alpha-nDCG NRBP Srec
for trecrun in `ls $trecrunfolder`;
do
	#process trecrun
	treceval $origbinary "$trecrunfolder/$trecrun" "origbinary"
done

for trecrun in `ls $trecrunfolder`;
do
	#process trecrun
	treceval $original "$trecrunfolder/$trecrun" "original"
done


pidarray=()
# predict evaluation with trec setting
for qreld in $directorytojud;
do
	percent=$(echo $qreld|awk -F/ '{print $(NF)}')
	wn=$(echo $qreld|awk -F/ '{print $(NF-1)}')
	threshold=$(echo $qreld|awk -F/ '{print $(NF-2)}')
	qrelname=$year"-"$wn"-"$threshold"-"$percent
	qrelf=$(echo $tmpfolder/pqrel/$qrelname)
	cat $qreld/*.qrel >> ${qrelf}
	{
		for trecrun in `ls $trecrunfolder`;
		do
			#ndeval for the original list
			treceval "$qrelf"  "$trecrunfolder/$trecrun" \
				"${qrelname}" &
			arr+=($!)
		done
	}
	for i in "${arr[@]}"
	do
		#echo "Waiting for "$i
		wait $i
	done
	(
		echo "INFO: Computing correlation for $qrelname"
		python $computeCorrDir/computeCorre.py \
			-o "$tmpfolder/intermediaeval/original" \
			-x "$tmpfolder/intermediaeval/${qrelname}" \
			-n "$qrelname orig" \
			-t "tau" \
			>> "$resdir/$qrelname"
		python $computeCorrDir/computeCorre.py \
			-o "$tmpfolder/intermediaeval/origbinary" \
			-x "$tmpfolder/intermediaeval/${qrelname}" \
			-n "$qrelname origbin" \
			-t "tau" \
			>> "$resdir/$qrelname"
	)&
done
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo "$year finished: "$DIFF
