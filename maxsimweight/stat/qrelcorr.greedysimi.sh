START=$(date +%s.%N)

predqrel=/scratch/GW/pool0/khui/result/2stagelowcost/GreedySimi
directorytojud=$(find $predqrel -name "*.qrel" -printf "%h\n" | sort -u)

resdir=$predqrel/qrelcorr
task=greedysimi
computeCorrDir=/home/khui/workspace/script/pythonscript/2stagecluster/main/maxsimweight/stat
echo "current pid:" $$ $(hostname)


trecrunfolder=/GW/D5data-2/khui/trecrun/adhoc/normrun100
origbinary=/GW/D5data-2/khui/qrel/completeqrel/binary/qrels.adhoc.wt
original=/GW/D5data-2/khui/qrel/completeqrel/adhoc/qrels.adhoc.wt
tmpfolder="/scratch/GW/pool0/khui/tmp/$task"
treceval=/home/khui/workspace/evaltool/trec_eval.9.0

#resdir="$resdir"
#if [[ -d "$resdir" ]];
#then
#	echo "deleting exist folder $resdir"
#	rm -rf $resdir
#fi
#mkdir -p "$resdir"
#
#if [[ -d "$tmpfolder" ]];
#then
#	echo "deleting exist folder $tmpfolder"	
#	rm -rf $tmpfolder;
#fi
#
#mkdir -p $tmpfolder/intermediaeval
#mkdir -p $tmpfolder/pqrel
#
#treceval(){
#	# 1:qrel, 2:run 3:output
#	# output: map P@20 R@20
#	runname=$(basename $2)
#	cd $treceval
#	measures=$(./trec_eval -c -J -m map_cut.20 -m P.20 -m recall.20 $1 $2 | awk '{print $1" "$3}')
#	MAP=$(echo $measures | awk '{print $6}')
##	R20=$(echo $measures | awk '{print $4}')
##	P20=$(echo $measures | awk '{print $2}')
#	# output: runname, ndcg@20, err@20
#	measures=$(./gdeval.pl -c -k 20 $1 $2  | grep "amean" | awk -F, '{print $3" "$4}')
##	ndcg20=$(echo $measures | awk '{print $1}')
#	err20=$(echo $measures | awk '{print $2}')
#	echo $runname" "$err20" "$MAP >> "$tmpfolder/intermediaeval/$3"
#}
#
#waitfinish(){
#	# 1: arr the pid array
#	# 2: string mesg, the name
#	declare -a arrlocal=("${!1}")
#	echo wait for $2
#	for pid in ${arrlocal[@]}
#	do
#		wait $pid
#	done
#	echo $2 finished
#
#}
#
#
## evaluate with complete trec eval
#for year in 09 10 11 12
#do
#	(
#	for trecrun in `ls $trecrunfolder/$year`;
#	do
#		#process trecrun
#		treceval $origbinary$year "$trecrunfolder/$year/$trecrun" "origbinary$year"
#		treceval $original$year "$trecrunfolder/$year/$trecrun" "original$year"
#	done
#	)&
#	arr+=($!)
#done
#waitfinish arr[@] completejud
#unset arr
#
## predict evaluation with trec setting
#for qreld in $directorytojud;
#do
#	(
#	percent=$(echo $qreld|awk -F/ '{print $(NF)}')
#	wn=$(echo $qreld|awk -F/ '{print $(NF-1)}')
#	threshold=$(echo $qreld|awk -F/ '{print $(NF-2)}')
#	kernel=$(echo $qreld|awk -F/ '{print $(NF-3)}')
#	for year in 09 10 11 12
#	do
#		(
#		qrelname=$year"-"$kernel"-"$wn"-"$threshold"-"$percent
#		qrelf=$(echo $tmpfolder/pqrel/$qrelname)
#		cat $qreld/*.qrel | sort -u  >> ${qrelf}
#		for trecrun in `ls $trecrunfolder/$year`;
#		do
#			#ndeval for the incomplete jud
#			treceval "$qrelf"  "$trecrunfolder/$year/$trecrun" "${qrelname}"
#		done
#		)&
#		arryear+=($!)
#	done
#	waitfinish arryear[@] $kernel"-"$wn"-"$threshold"-"$percent
#	unset arryear
#	)&
#	arr+=($!)
#	while [ ${#arr[@]} -ge 32 ]
#	do
#		echo wait ${#arr[@]} cat-jud-incomplete
#		for i in ${!arr[@]}
#		do
#			wait ${arr[$i]}
#			unset arr[$i]
#		done
#	done
#done
#waitfinish arr[@] cat-jud-incomplete-all
#unset arr

for year in 09 10 11 12
do
	mkdir -p $resdir/$year
done

for qreld in $directorytojud;
do
	percent=$(echo $qreld|awk -F/ '{print $(NF)}')
	wn=$(echo $qreld|awk -F/ '{print $(NF-1)}')
	threshold=$(echo $qreld|awk -F/ '{print $(NF-2)}')
	kernel=$(echo $qreld|awk -F/ '{print $(NF-3)}')
	for year in 09 10 11 12
	do
		(
		qrelname=$year"-"$kernel"-"$wn"-"$threshold"-"$percent
		qrelf=$(echo $tmpfolder/pqrel/$qrelname)
		echo "INFO: Computing correlation for $qrelname"
		python $computeCorrDir/computeCorre.py \
			-o "$tmpfolder/intermediaeval/original$year" \
			-x "$tmpfolder/intermediaeval/${qrelname}" \
			-n "$qrelname orig" \
			-t "tau" \
			>> "$resdir/$year/$qrelname"
		python $computeCorrDir/computeCorre.py \
			-o "$tmpfolder/intermediaeval/origbinary$year" \
			-x "$tmpfolder/intermediaeval/${qrelname}" \
			-n "$qrelname origbin" \
			-t "tau" \
			>> "$resdir/$year/$qrelname"
		)&
		arr+=($!)
	done
	while [ ${#arr[@]} -ge 64 ]
	do
		echo wait ${#arr[@]} computecorr
		for i in ${!arr[@]}
		do
			wait ${arr[$i]}
			unset arr[$i]
		done
	done
done
waitfinish arr[@] computecorr

END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo "$year finished: "$DIFF
