PIDS=`ps axf|grep kworker | grep -v grep|awk '{print $1}'`
for p in $PIDS;do
  echo 'kill'$p
done
