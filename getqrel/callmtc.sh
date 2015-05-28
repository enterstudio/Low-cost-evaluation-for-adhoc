cd /home/khui/workspace/script/pythonscript
timestamp=`date +%y%m%d`
trecrun=/GW/D5data-2/khui/trecrun/adhoc/perquery30qrel
qrelf=/GW/D5data-2/khui/qrel/completeqrel/adhocquery
outputfolder=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/mtc/qrels
if [ -d $outputfolder ];
then
	echo 'removing ' $outputfolder
	rm -rf $outputfolder
fi
for ((i=$1; i<=$2; i++))
do
	time0=$(date +"%s")
	qid=$i
	python $PWD/2stagecluster/main/comparativestudy/getqrel/mtc.py \
		-q $qid \
		-o $outputfolder \
		-r $trecrun/$qid \
		-j $qrelf/$qid
	time1=$(date +"%s")
	diff=$(($time1-$time0))
	echo finished `hostname` $id $qid $(($diff / 60)) miniutes $diff seconds
done
