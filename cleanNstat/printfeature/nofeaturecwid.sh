featuref=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/cleandata/cwid2did.out
allcwids=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/cleandata/top30cwidlist.out
outf=/home/khui/workspace/script/pythonscript/2stagecluster/main/comparativestudy/cleanNstat/outdir/nofeaturecwid.out
count=0
while read -r line
do
	if ! fgrep -Fq $line $featuref;
	then
		((count++))
		echo $line >> $outf
	fi
done < $allcwids
echo $count
