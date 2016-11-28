# python-word-vector
This is a python implementation of google word2vector algorithm.

This implementation cludes CBOW and skip-gram,both by Hierarchy Softmax.

Nagative sample method is not provided.

Training dataset is 10,000 documents of Chinese news,which can be replaced by other languages.
 
To start,try this steps:
    
    1.   cd scripts
 
    2.   sh demo_word2vec.sh (it takes about 20minutes to train)
 
    3.   sh demo_distance.sh 
 
 
Notes:

    1.  The format converting tool in bin folder is provided by https://github.com/marekrei/convertvec.git
 
    2.  Distance counting tool is just the original version of google C program 

    3.  Please email me if you have any questions: www.7zai@163.com


