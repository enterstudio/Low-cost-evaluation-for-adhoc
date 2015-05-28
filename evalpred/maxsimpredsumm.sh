#msimmethods=( srk-rbf-0.8  aones-rbf-0.8 appri-rbf-0.8 aones-cosine-0.0  aones-rbf-0.0  appri-cosine-0.0  appri-rbf-0.0 aones-cosine-0.8  appri-cosine-0.8  srk-cosine-0.0  srk-rbf-0.0 srk-cosine-0.8  )
#msimalias=( onecos0 onerbf0 aprcos0 aprrbf0 onecos8 onerbf8 aprcos8 aprrbf8 srkcos0 srkrbf0 srkcos8 srkrbf8 )

msimmethods=( srk-rbf-0.8  aones-rbf-0.8 srk-cosine-0.8 appri-cosine-0.8 aones-cosine-0.8 )
msimalias=( srkrbf8 onerbf8 srkcos8 aprcos8 aprcos8 )
for ind in ${!msimmethods[@]};
do
	method=${msimmethods[$ind]}
	malias=${msimalias[$ind]}
	nohup bash summarize.sh maxsim/$method $malias > log/$method.log 2>&1
	echo maxsim/$method finished
done
