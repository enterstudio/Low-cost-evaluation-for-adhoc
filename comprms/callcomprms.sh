#msimmethods=( appri-rbf-0.8 aones-cosine-0.0  aones-rbf-0.0  appri-cosine-0.0  appri-rbf-0.0 aones-cosine-0.8  aones-rbf-0.8  appri-cosine-0.8  srk-cosine-0.0  srk-rbf-0.0 srk-cosine-0.8  srk-rbf-0.8 )
msimmethods=( aones-rbf-0.8  )
(
for method in ${msimmethods[@]};
do
	(
	nohup bash comprms.sh maxsim/$method > log/$method.log 2>&1
	echo maxsim/$method finished
	)
done
wait
)
exit
#nohup bash comprms.sh pooling/incrementalpool > log/ipool.log 2>&1
#echo pooling/incrementalpool finished
(
(
nohup bash comprms.sh rndsample > log/rnd.log 2>&1
echo rndsample finished
)&
(
nohup bash comprms.sh mtc > log/mtc.log 2>&1
echo mtc finished
)&
(
nohup bash comprms.sh pooling/trecpool > log/tpool.log 2>&1
echo pooling/trecpool finished
)&
wait
)
