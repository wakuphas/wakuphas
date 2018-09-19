awk '/avg/' backup/aiport/train_log_3600.txt | awk '{print $3}' > avg.txt
awk '/avg/' backup/aiport/train_log_3600.txt | awk -F ":" '{print $1}' > epochs.txt
paste -d " " epochs.txt avg.txt > epochavg.txt

rm epochs.txt avg.txt