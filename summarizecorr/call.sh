#echo removing /scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/gnucorrall
#rm -rf /scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/gnucorrall
#mkdir -p /scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/gnucorrall


#msimmethods=( aones-cosine-0.0  aones-rbf-0.0  appri-cosine-0.0  appri-rbf-0.0 aones-cosine-0.8  aones-rbf-0.8  appri-cosine-0.8  appri-rbf-0.8 srk-cosine-0.0  srk-rbf-0.0 srk-cosine-0.8  srk-rbf-0.8 )
#msimalias=( onecos0 onerbf0 aprcos0 aprrbf0 onecos8 onerbf8 aprcos8 aprrbf8 srkcos0 srkrbf0 srkcos8 srkrbf8 )

msimmethods=( aones-rbf-0.8  srk-rbf-0.8 )
msimalias=( onerbf8 srkrbf8 )
for i in ${!msimmethods[@]};
do
	method=${msimmethods[$i]}
	malias=${msimalias[$i]}
        nohup bash summarize.sh maxsim/$method $malias > log/$method.log 2>&1
        echo maxsim/$method finished
done
exit
(
(
nohup bash summarize.sh pooling/incrementalpool ipool > log/ipool.log 2>&1
echo pooling/incrementalpool finished
)&
(
nohup bash summarize.sh mtc mtc > log/mtc.log 2>&1
echo mtc finished
)&
(
nohup bash summarize.sh rndsample rnd > log/rnd.log 2>&1
echo rndsample finished
)&
(
nohup bash summarize.sh pooling/trecpool tpool > log/tpool.log 2>&1
echo pooling/trecpool finished
)&
wait
)

