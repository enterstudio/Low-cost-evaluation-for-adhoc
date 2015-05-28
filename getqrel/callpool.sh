cd /home/khui/workspace/script/pythonscript
timestamp=`date +%y%m%d%H%M`
echo "current pid:" $$ `hostname`
trecrun=/GW/D5data-2/khui/trecrun/adhoc/normrun30qrel/perqueryn
qrelf=/GW/D5data-2/khui/qrel/completeqrel/adhoc/perquery
outputfolder=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/pooling10

#if [ -d $outputfolder ];
#then
#	echo 'removing ' $outputfolder
#	rm -rf $outputfolder
#fi

mkdir -p $outputfolder

for ((i=$1; i<=$2; i++))
do
	qid=$i
	python $PWD/2stagecluster/main/comparativestudy/getqrel/pool.py \
		-q $qid \
		-o $outputfolder \
		-r $trecrun/$qid \
		-j $qrelf/$qid
	echo finished `hostname` $timestamp $qid
done
