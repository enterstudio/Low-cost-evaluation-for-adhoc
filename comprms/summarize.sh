START=$(date +%s.%N)

task=$1
samplen=$2
directory=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/$task
rmsdir=$directory/rmse
outdir=$directory/gnucorr
#measures=( statap )
measures=( bpref indap infap tmap )
#measures=( pmapn )

#if [ -d $outdir ]
#then
#	echo removing $outdir
#	rm -rf $outdir
#fi
mkdir -p $outdir
mkdir -p $rmsdir
for evalm in ${measures[@]}
do
	intf=$rmsdir/$evalm.rms
	python $PWD/summarize.py -f $intf -s $samplen \
		> $outdir/$samplen-$evalm-rmse
	cp $outdir/$samplen-$evalm-rmse /scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/gnucorrall/
	cp $outdir/$samplen-$evalm-rmse /home/khui/workspace/script/gnuplot/comparative/data/rmse/
done



