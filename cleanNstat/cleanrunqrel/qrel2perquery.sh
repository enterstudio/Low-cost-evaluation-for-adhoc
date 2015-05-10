qrel=/GW/D5data-2/khui/qrel/completeqrel/adhoc/qrels.adhoc.wt$1
outputfolder=/GW/D5data-2/khui/qrel/completeqrel/adhoc/perquerynn
mkdir -p $outputfolder
for ((i=$2;i<=$3;i++))
do
	cat $qrel | awk -v qid=$i '$1==qid {print}' >> $outputfolder/$i
	echo $i finished
done
