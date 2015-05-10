corrdir=/home/khui/workspace/script/gnuplot/comparative/data
outf=/home/khui/workspace/script/pythonscript/2stagecluster/main/comparativestudy/cleanNstat/outdir/gnuplot.stat
if [ -f $outf ]
then
	rm $outf
fi

(
for exp in kendalltau rmse
do
	for f in `ls $corrdir/$exp`
	do
		(

		python statcorr.py -i "$corrdir/$exp/$f" -e $exp >> $outf
		echo finished $f
		)&
	done
done
wait
)
echo $corrdir all finished

