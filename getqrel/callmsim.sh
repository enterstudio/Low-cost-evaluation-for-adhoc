echo `hostname` $timestamp $BASHPID
timestamp=`date +%y%m%d%H%M`
trecrun=/GW/D5data-2/khui/trecrun/adhoc/normrun30qrel/perqueryn
qrelf=/GW/D5data-2/khui/qrel/completeqrel/adhoc/perquery
outputfolder=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/maxsim
featurefile=/GW/D5data-2/khui/features/termweight/adhocn/perquery
#if [ -d $outputfolder ];
#then
#	echo 'removing ' $outputfolder
#	rm -rf $outputfolder
#fi
mkdir -p $outputfolder

wns=( appri )
#( aones srk appri )
kns=( rbf )
#( rbf cosine )
thresholds=( 0.8 0.0 )
(
for threshold in "${thresholds[@]}"	
do
	for kn in "${kns[@]}"
	do
		for wn  in "${wns[@]}"
		do
			(				                
			for ((i=$1;i<=$2;i++))
			do
				qid=$i
				python $PWD/maxsim.py \
					-f $featurefile/$qid \
					-q $qid \
					-o $outputfolder \
					-r $trecrun/$qid \
					-j $qrelf/$qid \
					-w $wn \
					-t $threshold \
					-k $kn
			done
			echo finished `hostname` $id $threshold $wn $kn
			)& 
		done
	done
done
wait
)

