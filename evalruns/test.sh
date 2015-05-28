rundir=/GW/D5data-2/khui/trecrun/adhoc/normrun30qrel/09
qrelf=/scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/statAP/prels/0.2/11/fusion.09.test
for f in `ls $rundir`;
do 
	statmap=$(perl statAP_MQ_eval_v4.pl $qrelf $rundir/$f|grep 'statMAP_on_valid_topics'|awk -F= '{print $NF}'); 
	runn=$(head -n 1 $rundir/$f|awk '{print $NF}');
	echo $runn $statmap;
done
