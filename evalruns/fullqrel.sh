START=$(date +%s.%N)
echo "current pid:" $$
resdir=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/fullqrel10
trecrunfolder=/GW/D5data-2/khui/trecrun/adhoc/normrun30qrel/peryearn
#/GW/D5data-2/khui/trecrun/adhoc/normrun30qrel
original=/GW/D5data-2/khui/qrel/completeqrel/adhoc/qrels.adhoc.wt
treceval=/home/khui/workspace/evaltool/trec_eval.9.0

resdir="$resdir"
#if [[ -d "$resdir" ]];
#then
#	rm -rf $resdir
#	echo "deleting exist folder $resdir"
#fi
mkdir -p "$resdir"


treceval(){
	# 1:qrel, 2:run 3:output
	# output: map
	runname=$(head -1 $2 |awk '{print $6}')
	cd $treceval
	map=$(./trec_eval -m map $1 $2 | awk '{print $3}')
	echo $runname" "$map >> "$resdir/$3map"
}


for year in 13 
	#14
	#09 10 11 12
do
	echo processing $year
	for trecrun in `ls $trecrunfolder/$year`;
	do
		#process trecrun
		treceval $original$year $trecrunfolder/$year/$trecrun $year
	done
done
END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo "finished: "$DIFF
