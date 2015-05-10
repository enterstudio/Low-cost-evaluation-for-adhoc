spamfile=/GW/D5data/ClueWeb09/supplemental/spam/clueweb09spam.Fusion
cwidlist=$PWD/outdir/unlabelperq
#unlabeledcwids.out
outdir=$PWD/outdir/spamcwid
mkdir -p $outdir
(
for qid in {51..200}
do
	if [ -e $cwidlist/$qid.out ]
	then
		(
		while read -r line
		do
			qid=$(echo $line | awk '{print $1}')
			cwid=$(echo $line | awk '{print $2}')
			spamline=$(fgrep -m 1 $cwid $spamfile|awk '{print $1}')
			echo $qid $cwid $spamline >>  $outdir/$qid.out
		done < $cwidlist/$qid.out
		)&
	fi
done
wait
)
