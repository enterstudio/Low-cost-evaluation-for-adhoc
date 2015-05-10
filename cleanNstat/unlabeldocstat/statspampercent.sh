# qid cwid spam score
spamperquery=/home/khui/workspace/script/pythonscript/2stagecluster/main/comparativestudy/cleanNstat/outdir/spamcwid
outf=/home/khui/workspace/script/pythonscript/2stagecluster/main/comparativestudy/cleanNstat/outdir/statspampercent.out
for qid in {51..200}
do
	cat $spamperquery/$qid.out | \
		awk 'START {count=0;rown=0;} {rown++} $3<70{count++} END{printf "%d\t%.1f%%\n",'$qid',(count/rown)*100}' \
		>>$outf
done

