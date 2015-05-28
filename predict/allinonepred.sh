#msimmethods=( appri-cosine-0.8 srk-rbf-0.8 srk-cosine-0.8 aones-cosine-0.0  aones-rbf-0.0  appri-cosine-0.0  appri-rbf-0.0 aones-cosine-0.8  aones-rbf-0.8  srk-cosine-0.0  srk-rbf-0.0 )
# appri-rbf-0.8
msimmethods=( appri-rbf-0.8 appri-rbf-0.0 )
(
for method in ${msimmethods[@]};
do
	(
	nohup bash callpred.sh maxsim/$method > log/${method}1314.log 2>&1
	echo maxsim/$method finished
	)
done
wait
)
exit
#nohup bash compcorr.sh pooling/incrementalpool > log/ipool.log 2>&1
#echo pooling/incrementalpool finished
(
(
nohup bash compcorr.sh rndsample > log/rnd.log 2>&1
echo rndsample finished
)&
(
nohup bash compcorr.sh mtc > log/mtc.log 2>&1
echo mtc finished
)&
(
nohup bash compcorr.sh pooling/trecpool > log/tpool.log 2>&1
echo pooling/trecpool finished
)&
wait
)
