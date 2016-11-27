unzip ../data/10000_lines.zip -d ../data/
nohup python ../src/word2vec.py >log.txt 2>&1 &
