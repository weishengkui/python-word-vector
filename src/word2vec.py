#!/usr/bin/env python
#coding:utf8
from huffman import huffman 
import numpy as np
import random
import pdb
import sys

word_code_dict = {}
hidden_vector_dict = {}
word_vector_size = 30
window = 3
alpha = 0.01
train_file_name = "../data/10000_lines.txt"
result_file_name ="../data/result_vector.txt" 
cbow = 0
max_loop = 1
min_count = 5
all_lines = open(train_file_name).readlines()
all_words_num = 0

def read_train_data():
    global word_code_dict,hidden_vector_dict,all_words_num
    for line in all_lines:
        data = line.strip().split()
        for item in data:
            if item not in word_code_dict:
                word_code_dict[item] = 1
            else:
                word_code_dict[item] += 1
    min_key_list = [k for k in word_code_dict if word_code_dict[k] < min_count]
    all_words_num = sum(word_code_dict.itervalues())

    for key in min_key_list:
        del word_code_dict[key]
    #building_huffman_tree
    myhuffman = huffman(word_code_dict.items())
    word_code_dict = dict(myhuffman.get_code())
    for k,v in word_code_dict.iteritems():
        for i in range(0,len(v)):
            hidden = v[:i]+'x'
            if hidden not in hidden_vector_dict:
                hidden_vector = np.random.randn(word_vector_size)
                hidden_vector_dict[hidden] = hidden_vector
        word_vector = np.random.randn(word_vector_size)
        word_code_dict[k] = [v,word_vector]

def generate_samples(all_lines):
    samples = []
    for line in all_lines:
        data = line.strip().split() 
        if len(data) < window *2 + 1:
            continue
        #generate samples by window
        mywordIndex = window
        while mywordIndex + window <= len(data):
            contexts = data[mywordIndex - window:mywordIndex] +\
                     data[mywordIndex + 1: mywordIndex+window + 1]
            targets = [data[mywordIndex]]
            targets = filter(lambda x : x in word_code_dict,targets)
            contexts = filter(lambda x : x in word_code_dict,contexts)
            if not targets or not contexts:
                mywordIndex += 1
                continue
            #skip-gram
            if cbow != 1:
                contexts,targets = targets,contexts
            samples.append([contexts,targets])
            mywordIndex += 1
    return samples


def train():
    global word_code_dict,hidden_vector_dict
    read_train_data()
    samples = generate_samples(all_lines)
    x_all_g = np.zeros(word_vector_size)
    print "Start training."
    for loop in range(max_loop):
        #SGD
        count = 0
        for contexts,targets in samples:
            rate  = 1./len(contexts)
            x_all = rate * np.sum(word_code_dict[x][1] for x in contexts)
            x_all_g = x_all_g * 0 #reset zero
            for target in targets: 
                huffman_code = word_code_dict[target][0]
                #training from top to down
                for i,v in enumerate(huffman_code):
                    huffman_key = huffman_code[:i] + "x"
                    y = 1 if v != '0' else -1
                    w = hidden_vector_dict[huffman_key]
                    g = (1.0/(1+np.exp(np.dot(w,x_all)*y) ) ) * -y
                    x_all_g += g * w
                    w_g = g * x_all
                    hidden_vector_dict[huffman_key] -= alpha * w_g
            for x in contexts:
                word_code_dict[x][1] -= alpha * x_all_g * rate
            
            count += 1
            if count % 2000 == 0:
                print("training {0} sample of {1} in {2}th out of {3} loops".format(count,len(samples),loop,max_loop))
                sys.stdout.flush()
    #write result
    fw = open(result_file_name,"w")
    fw.write(str(len(word_code_dict))+" "+str(word_vector_size)+"\n")  
    for k,v in word_code_dict.iteritems():
        fw.write(k)
        for item in v[1]:
            fw.write(" "+str(item))  
        fw.write("\n")
    fw.close()
    print "Finished."

if __name__ == '__main__':
    print "Start training:"
    print "Vocab size:",len(word_code_dict)
    print "Vector size:",word_vector_size
    print "Window:",window
    print "cbow:",cbow 
    train()






