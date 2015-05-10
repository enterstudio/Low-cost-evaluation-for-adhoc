echo "current pid:" $$
timestamp=`date +%y%m%d%H%M`
qrelf=/GW/D5data-2/khui/qrel/completeqrel/adhocquery
outputfolder=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/statAP/prels
inputfolder=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/statAP/includprob
samplerates="0.01 0.05 0.1 0.15 0.2 0.25 0.3 0.35 0.4 0.45 0.5 0.55 0.6 0.65 0.7 0.75 0.8 0.85 0.9 0.95"

directorytojud=$(find $inputfolder -name "*.ipqrel" -printf "%h\n" | sort -u)

ipf2prel(){
	# 1:ipf
	qid=$(head -1 $1|awk '{print $1}')
	outf=$outdir/$qid.prel
	qidqrel=$(less  $qrelf/$qid)
	while read -r line;
	do
		#echo $qrelf/$qid
		cwid=$(echo $line|awk '{print $3}')
		label=$(echo $qidqrel|grep $cwid | awk '{print $NF}')
		echo $line | awk '{print $1" "$3" "'$label'" "2" "$NF}' >> $outf
	done < $1
}


for percent in $samplerates
do
	mkdir -p $outputfolder/$percent
done

for dir in $directorytojud
do
	percent=$(echo $dir|awk -F/ '{print $NF}')
	outdir=$outputfolder/$percent
	for ipf in `ls $dir`
	do
		ipf2prel $dir/$ipf
	done
	exit
done
