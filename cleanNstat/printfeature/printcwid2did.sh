id=`date +"%m%d%M%H"`.`hostname`.$BASHPID.$1
echo $id
javaworkspace=/home/khui/workspace/javaworkspace
export HADOOP_CLASSPATH=`find /home/khui/workspace/javaworkspace/lib/ -name "*.jar" | tr '\n' ':'`
export HADOOP_OPTS="-Xms10G -Xmx10G"
export JAVA_HOME=${javaworkspace}"/java-7-sun"
export PATH=$PATH:$JAVA_HOME/bin

hadoop jar $javaworkspace/CdEval.jar de.mpii.nuse.util.WriteCwid2Did

echo `basename $0`' is finished for '$id' at time: '`date +"%m%d%M%H"`
