START=$(date +%s.%N)

task=$1
samplen=$2
directory=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/$task
preddir=$directory/predeval
outdir=$directory/gnucorr
measures=( pred )
# 'TP', 'TN', 'FP', 'FN', 'missrate', 'precision', 'recall', 'f1'
corrms=( f1 )
corralias=( f1 )

mkdir -p $outdir

for i in ${!corrms[@]}
do
	corrm=${corrms[$i]}
	corra=${corralias[$i]}
	for evalm in ${measures[@]}
	do
		intf=$preddir/$evalm
		python $PWD/summarize.py -f $intf -s $samplen -m $corrm \
			> $outdir/$samplen-$evalm-$corra
	done
done
#cp $outdir/* /scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/gnucorrall/


