START=$(date +%s.%N)

task=$1
samplen=$2
directory=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/$task
corrdir=$directory/corrs
outdir=$directory/gnucorr
#measures=( statap )
measures=( bpref indap infap tmap )
#measures=( pmapn )
corrms=( kendalltau pearsonr )
corralias=( tau r )

if [ -d $outdir ]
then
	echo removing $outdir
#	rm -rf $outdir
fi
mkdir -p $outdir

for i in ${!corrms[@]}
do
	corrm=${corrms[$i]}
	corra=${corralias[$i]}
	for evalm in ${measures[@]}
	do
		intf=$corrdir/$corrm/$evalm.corr
		python $PWD/summarize.py -f $intf -s $samplen \
			> $outdir/$samplen-$evalm-$corra
	done
done
cp $outdir/* /scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/gnucorrall/


