trecruns=/GW/D5data-2/khui/trecrun/adhoc/orignialruns
outputfolder=$trecruns/perqueryn
if [ -e $outputfolder ]
then
	echo removing $outputfolder 
	rm -rf $outputfolder
fi
mkdir -p $outputfolder
(
(
year=13
for run in `ls $trecruns/$year`
do
	for ((i= 201;i<= 250;i++))
	do
		partnum=$(echo $run | awk -F. '{print NF}')

		if [ $partnum -gt 2 ]
		then
			fname=$(echo $run | awk -F. '{print $(NF-1)"-"$NF}')
		else
			fname=$(echo $run | awk -F. '{print $NF}')
		fi
		rname=$(head -n 1 $trecruns/$year/$run | awk '{print $6}')

		if [ "$rname" != "$fname" ]
		then
			runname=$(echo $rname"-"$fname)	
		else
			runname=$(echo $rname)
		fi
		cat $trecruns/$year/$run | awk -v qid=$i -v rn=$runname '$1==qid {print $1" "$2" "$3" "$4" "$5" "rn}' | sort -n -k4,4 \
			>> $outputfolder/$i
	done

done
echo $year finished
)&

(
year=14
for run in `ls $trecruns/$year`
do
	for ((i= 251;i<= 300;i++))
	do
		partnum=$(echo $run | awk -F. '{print NF}')

		if [ $partnum -gt 2 ]
		then
			fname=$(echo $run | awk -F. '{print $(NF-1)"-"$NF}')
		else
			fname=$(echo $run | awk -F. '{print $NF}')
		fi
		rname=$(head -n 1 $trecruns/$year/$run | awk '{print $6}')

		if [ "$rname" != "$fname" ]
		then
			runname=$(echo $rname"-"$fname)	
		else
			runname=$(echo $rname)
		fi
		echo $fname $rname $runname
		cat $trecruns/$year/$run | awk -v qid=$i -v rn=$runname '$1==qid {print $1" "$2" "$3" "$4" "$5" "rn}' | sort -n -k4,4 \
			>> $outputfolder/$i
	done
done
echo $year finished
)&
#(
#year=11
#for run in `ls $trecruns/$year`
#do
#	for ((i= 101;i<= 150;i++))
#	do
#		cat $trecruns/$year/$run | awk -v qid=$i '$1==qid {print $1" "$2" "$3" "$4" "$5" "$6}' >> $outputfolder/$i
#	done
#done
#echo $year finished
#)&
#(
#year=12
#for run in `ls $trecruns/$year`
#do
#	for ((i= 151;i<= 200;i++))
#	do
#		cat $trecruns/$year/$run | awk -v qid=$i '$1==qid {print $1" "$2" "$3" "$4" "$5" "$6}' >> $outputfolder/$i
#	done
#done
#echo $year finished
#)&
wait
)
