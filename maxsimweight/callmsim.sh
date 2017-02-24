cd /home/khui/workspace/script/pythonscript
timestamp=`date +%y%m%d%H%M`
threshold=$3
trecrun=/GW/D5data-2/khui/trecrun/adhoc/perquery
qrelf=/GW/D5data-2/khui/qrel/completeqrel/adhocquery
outputfolder=/scratch/GW/pool0/khui/result/2stagelowcost/GreedySimi
featurefile=/GW/D5data-2/khui/features/termweight/adhoc/perquery
#if [ -d $outputfolder ];
#then
#	echo 'removing ' $outputfolder
#	rm -rf $outputfolder
#fi
#mkdir -p $outputfolder
echo `hostname` $timestamp $BASHPID
wns=( aones entropy kld srk )
kns=( rbf linear cosine )
for kn in "${kns[@]}"
do
	for wn  in "${wns[@]}"
	do
		(				                
		for ((i=$1;i<=$2;i++))
		do
			qid=$i
			python $PWD/2stagecluster/main/maxsimweight/main.py \
				-f $featurefile/$qid \
				-q $qid \
				-o $outputfolder \
				-r $trecrun/$qid \
				-j $qrelf/$qid \
				-w $wn \
				-t $threshold \
				-k $kn
			echo finished `hostname` $id $qid $threshold $wn $kn
		done
		) &
		sleep 2
	done
done
