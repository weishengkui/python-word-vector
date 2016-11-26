#!/usr/bin/env python 
import heapq

class node(object):
    def __init__(self,data,left=None,right=None):
        self.original = data
        if isinstance(data,(list,tuple)):
            self.original = data[0]
            self.data = data[1]
        else:
            self.data = data
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.data)

    def __cmp__(self,other):
        return cmp(self.data,other.data)

class huffman(object):
    def __init__(self,data):
        temp = [node(x) for x in data]
        self.tag = ""
        self.hidden_count = 0
        self.leaf_count = 0
        
        self.huffman_code = []
        h = []
        for item in temp:
            heapq.heappush(h,item)
        while True:
            first = heapq.heappop(h)
            if not h:
                self.root = first
                break
            second = heapq.heappop(h)
            newnode = node(["hiddenNode",first.data+second.data],first,second)  
            heapq.heappush(h,newnode)
        
    def get_code(self):
        self.hidden_count = 0
        self.leaf_count = 0
        self.huffman_code = []
        
        self.travel(self.root)
        print "hidden_count:",self.hidden_count
        print "leaf_count:",self.leaf_count
        
        return self.huffman_code

    def travel(self,root):        
        if not root:
            return
        if not root.left and not root.right:
            self.huffman_code.append((root.original,self.tag))
            self.tag = self.tag[:-1]
            self.leaf_count += 1
            return
        if root.left or root.right:
            self.hidden_count += 1
        self.tag += "1"
        self.travel(root.left)
        self.tag += "0"
        self.travel(root.right)
        self.tag = self.tag[:-1]
 

if __name__ == '__main__':
    temp = [("nihao",2),3,5,7]
    print temp,len(temp)
    a = huffman(temp)
    code = a.get_code()
    print code,len(code)





