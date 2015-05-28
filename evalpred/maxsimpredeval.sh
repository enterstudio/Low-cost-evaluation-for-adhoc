msimmethods=( appri-rbf-0.8 aones-cosine-0.0  aones-rbf-0.0  appri-cosine-0.0  appri-rbf-0.0 aones-cosine-0.8  aones-rbf-0.8  appri-cosine-0.8  srk-cosine-0.0  srk-rbf-0.0 srk-cosine-0.8  srk-rbf-0.8 )
for method in ${msimmethods[@]};
do
	nohup bash callpred.sh maxsim/$method > log/$method.log 2>&1
	echo maxsim/$method finished
done
