#!/bin/bash
# simple job queue: keeps at most 2 gen_certp.py processes; jobs = lines of queue.txt ("<args> | <logname>")
cd /Users/cubres/Documents/Clauding/erdos-hunt/claude644_work/genp_sep
while true; do
  n=$(pgrep -f "Python gen_certp.py" | wc -l | tr -d ' ')
  if [ "$n" -lt 2 ]; then
    line=$(head -1 queue.txt 2>/dev/null)
    if [ -z "$line" ]; then sleep 30; continue; fi
    tail -n +2 queue.txt > queue.tmp && mv queue.tmp queue.txt
    args=${line%%|*}; lg=$(echo ${line##*|} | tr -d ' ')
    echo "$(date +%H:%M:%S) launch $args -> logs/$lg" >> logs/queue.log
    nohup nice python3 gen_certp.py $args > logs/$lg 2>&1 &
    sleep 5
  fi
  sleep 20
done
