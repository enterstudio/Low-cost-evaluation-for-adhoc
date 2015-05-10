START=$(date +%s.%N)
echo "current pid:" $$
trecruns=/GW/D5data-2/khui/trecrun/adhoc/normrun30qrel/perquery
for qid in {1..200}
do
	if [ -e $trecruns/$qid ]
	then
		cat $trecruns/$qid | awk '{print $3}'|sort -u | awk '{print '$qid'" "$1}' >> $PWD/log/tmpcwid.out
	fi
done
cat $PWD/log/tmpcwid.out | sort -u > $PWD/top30qidcwidlist.out


END=$(date +%s.%N)
DIFF=$(echo "$END - $START" | bc)
echo output cwid list finished: $DIFF
