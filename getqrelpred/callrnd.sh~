timestamp=`date +%y%m%d%H%M`
trecrun=/GW/D5data-2/khui/trecrun/adhoc/normrun30qrel/perquery
qrelf=/GW/D5data-2/khui/qrel/completeqrel/adhoc/perquery
outputfolder=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/rndsample/qrels
samplerates="0.01 0.05 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 0.15 0.25 0.35 0.45 0.55 0.65 0.75 0.85 0.95"
#"0.01 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95"

#if [ -d $outputfolder ];
#then
#	echo 'removing ' $outputfolder
#	rm -rf $outputfolder
#fi


for ((qid=$1; qid<=$2; qid++))
do
	(
	for percent in $samplerates
	do
		(
		python $PWD/rndsample.py \
			-q $qid \
			-r $trecrun/$qid \
			-o $outputfolder \
			-j $qrelf/$qid \
			-p $percent
		echo finished `hostname` $timestamp $qid $percent
		)&
	done
	wait
	)
done
