featurefile=/GW/D5data-2/khui/features/termweight/adhocn/tfidffeaturecw12.out
qidcwidlist=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/cleandata/cwid2didcw12.out
#/home/khui/workspace/script/pythonscript/2stagecluster/main/comparativestudy/cleanNstat/outdir/top30qidcwidlist.out
outdir=/GW/D5data-2/khui/features/termweight/adhocn/perquery
#rm -rf $outdir
#mkdir -p $outdir
while read -r line
do
	cwid=$(echo $line | awk '{print $1}')
#	fgrep $cwid $qidcwidlist
	while read -r qidcwid
	do
		qid=$(echo $qidcwid | awk '{print $1}')
		echo $line >> $outdir/$qid
	done < <(fgrep $cwid $qidcwidlist)
done < $featurefile
