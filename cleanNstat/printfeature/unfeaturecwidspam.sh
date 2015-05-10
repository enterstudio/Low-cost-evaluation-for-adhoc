spamfile=/GW/D5data/ClueWeb09/supplemental/spam/clueweb09spam.Fusion
cwidlist=$PWD/outdir/nofeaturecwid.out
outf=$PWD/outdir/nofeaturrecwidspam.out
while read -r line
do
	spamline=$(fgrep -m 1 $line $spamfile|awk '{print $1}')
	echo $line $spamline >>  $outf
done < $cwidlist
