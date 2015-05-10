id=`date +"%m%d%M%H"`.`hostname`.$BASHPID
echo $id
javaworkspace=/home/khui/workspace/javaworkspace
output=/GW/D5data-2/khui/features/termweight/adhocn
#/GW/D5data-2/khui/features/termweight/adhocn/perquery
indexroot=file:///GW/D5data-2/khui/index/cw12qrelrevised
#file:///scratch/GW/pool0/khui/result/2stagelowcost/comparativestd/cleandata/cwid2didcw12.out
#file:///GW/D5data-2/khui/index/cw09atop30qrel
#indexroot=file:///local/khui/index/cw09-a
#file:///GW/D5data-2/khui/index/cw09-a
export HADOOP_CLASSPATH=`find /home/khui/workspace/javaworkspace/lib/ -name "*.jar" | tr '\n' ':'`
export HADOOP_OPTS="-Xms20G -Xmx20G"
export JAVA_HOME=${javaworkspace}"/java-7-sun"
export PATH=$PATH:$JAVA_HOME/bin

if [ "`hostname`" == "sedna" ];then  indexroot=file:///GW/D5data-2/khui/index/cw09-a; fi

echo "indexroot " $indexroot
echo "output " $output
hadoop jar $javaworkspace/CdEval.jar de.mpii.nuse.novelty.eval.task.PrintAdhocFeatures -r $indexroot -o $output
echo `basename $0`' is finished for '$id' at time: '`date +"%m%d%M%H"`
