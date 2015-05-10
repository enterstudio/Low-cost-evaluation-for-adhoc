selectname=( rnd ipool statAP statAPl msim )
metrics=( indAP infAP bpref tMAP pMAP )
process=( getqrel predict evalbqrel evalpred corr rmse summarize )
echo -e \\t ${process[@]}
for sn in ${selectname[@]}
do
	for mn in ${metrics[@]}
	do
		echo -e $sn+$mn
	done
done
