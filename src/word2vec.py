#!/usr/bin/python
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
fix_layer_1 = False
max_loop = 1
min_count = 5
all_lines = open(train_file_name).readlines()

def read_train_data():
    global word_code_dict,hidden_vector_dict
    for line in all_lines:
        data = line.strip().split()
        for item in data:
            if item not in word_code_dict:
                word_code_dict[item] = 1
            else:
                word_code_dict[item] += 1
    min_key_list = [k for k in word_code_dict if word_code_dict[k] < min_count]
    for key in min_key_list:
        del word_code_dict[key]
    #built_huffan_tree
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

def train():
    global word_code_dict,hidden_vector_dict
    read_train_data()
    for loop in range(max_loop):
        total_count = 0
        line_count = 0
        for line in all_lines:
            line_count += 1
            data = line.strip().split() 
            if len(data) < window *2 + 1:
                continue
            #generate samples by window
            samples = []
            mywordIndex = window
            while mywordIndex + window <= len(data):
                contexts = data[mywordIndex-window:mywordIndex] +\
                         data[mywordIndex+1: mywordIndex+window+1]
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
            for contexts,targets in samples:
                x_all = np.sum(word_code_dict[x][1] for x in contexts)
                x_all_g = np.zeros(word_vector_size)
                for target in targets: 
                    huffman_code = word_code_dict[target][0]
                    #training from top to down
                    for i,v in enumerate(huffman_code):
                        huffman_key = huffman_code[:i] + "x"
                        y = 1 if v != '0' else -1
                        w = hidden_vector_dict[huffman_key]
                        g = (1.0/(1+np.exp(np.dot(w,x_all)*y) ) ) * -y
                        x_all_g += g * w
                        if loop != max_loop -1 or not fix_layer_1:
                            w_g = g * x_all
                            hidden_vector_dict[huffman_key] -= alpha * w_g
                for x in contexts:
                    word_code_dict[x][1] -= alpha * x_all_g / len(targets)
                
                total_count += 1
                if total_count % 500 == 0:
                    print "loop:%d,word_count:%d,line_count:%d/%d" % (loop,total_count,line_count,len(all_lines))
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






