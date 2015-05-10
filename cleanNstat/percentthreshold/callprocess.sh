corrdir=/home/khui/workspace/script/gnuplot/comparative/data/kendalltau
#rmse
#kendalltau
outdir=/home/khui/workspace/script/pythonscript/2stagecluster/main/comparativestudy/cleanNstat/outdir/corrthreshold
if [ ! -d $outdir ]
then
	mkdir $outdir
fi

(
for f in `ls $corrdir`
do
	(
	python processcorr.py -i "$corrdir/$f" > $outdir/$f
	echo finished $f
	)&
done
wait
)
echo $corrdir all finished

