import os
import string
import tkinter
from tkinter import *
from tkinter import messagebox

#get stopwords---sw1
def getstopwords():
    sw=open("english-stop.txt")
    sw1=sw.read().split()
    return sw1

def getoridocl(d):#d is dir
#get original document list with punctuations and numbers
#dir="data/"
    dlist=[]
    tmp=[]
    for dn in os.listdir(d):
        m1=[]
        f = open(d+dn)#get content
        d=f.read()
        d=d.split()
        for j in d:
            j = j.lower()
            m1.append(j)#in a document a term can repeat
            if j not in tmp:
                tmp.append(j)
        dlist.append(m1)
    return dlist,tmp

def buildterml(t,x):#t=tmp,x=sw1
    # remove punctuations and numbers
    d1 = []
    for m in t:
        pp = m.translate(str.maketrans('', '', string.punctuation)).lower()
        ppp = pp.translate(str.maketrans('', '', '1234567890'))
        d1.append(ppp)
    # build term list
    terml = []
    for q in d1:
        if q in x or q == '':
            continue
        else:
            if q not in terml:
                terml.append(q)
    terml.sort()  # sort term list
    return terml

def builddocl(dlist,x):#x=sw1
    doc = []
    # build doc without stopwords punctuations and numbers
    for a in dlist:
        m2 = []
        for b in a:  # remove stopwords, punctuations and numbers in docs
            pp = b.translate(str.maketrans('', '', string.punctuation)).lower()
            ppp = pp.translate(str.maketrans('', '', '1234567890'))
            if ppp != "" and ppp not in x:
                m2.append(ppp)
        doc.append(m2)
    return doc

def termfreq(x,y):#x=terml,y=doc
    freql = []  # record term frequency
    for c in x:
        s = 0
        for docs in y:
            s += docs.count(c)
        freql.append(s)

def queryprocess(x):#x=input()
    query = x.lower()  # lower the query
    qy = query.split()
    if 'and' in qy:  # the signal of query containing logic word(s)
        logic = 1
    elif 'or' in qy:
        logic = 2
    else:  # no logic words
        logic = 3
    return logic,qy

def queryw(x,logic,doc):#x=qy
    idx = []
    if logic==3:#sigal word
        tmp=[]
        tmp.append(x[0])
        #print(x[0])
        for f in range(len(doc)):
            if x[0] in doc[f]:#traverse all the documents to get posting list
                tmp.append(f) #posting list
        for _ in tmp:
            idx.append(_)
        #if query == terml[e]:
        #print(idx)
    else:
        k = []
        for _ in x:
            if 'or' in x:
                x.pop(x.index('or'))
            elif 'and' in x:
                x.pop(x.index('and'))
        for _ in range(len(x)):
            tmm = []
            #link_list = LinkedList()
            tup = (x[_], freql[terml.index(x[_])])
            tmm.append(tup)
            for f in range(len(doc)):
                if x[_] in doc[f]:
                    tmm.append(f)
            k.append(tmm[1:])
        if logic==2:#'or'
            #print(1)
            for m in k:#union
                for n in m:
                    if n not in idx:
                        idx.append(n)
        elif logic==1:#'and'
            for m in range(1,len(k)) :#intersection
                u = [val for val in k[m-1] if val in k[m]]
                for _ in u:
                    idx.append(_)
    return idx

def queryp(x,logic,doc):
    idx=[]
    for w in range(len(x)):
        LLL = []
        for k in doc:#doc is a 2 dimentional list, k is a document
            LL = []
            if x[w] in k:
                #link_list1 = LinkedList()
                tmm=[]
                tup = (doc.index(k), k.count(x[w]))
                tmm.append(tup)
                for index,s in enumerate(k) :
                    if s == x[w]:
                        tmm.append(index)
                LL.append(tmm)
            if LL != []:
                for _ in LL:
                    LLL.append(_)
        if LLL!= []:
            idx.append(LLL)
    result=[]
    #print(idx)
    if len(idx[0])>=len(idx[1]):
        idx0_d=[c[0] for c in idx[0]]
        idx0_docid=[]
        for _ in idx0_d:
            idx0_docid.append(_[0])
        #print(idx0_docid)
        for i,c in enumerate(idx[1]):
            if idx[1][i][0][0] in idx0_docid:
                for j in range(1,len(idx[1][i])):
                    #print(idx[1][i][0][0])
                    if idx[1][i][j]-1 in idx[0][idx0_docid.index(idx[1][i][0][0])]:
                        result.append(idx[1][i][0][0])
    elif len(idx[0])<len(idx[1]):
        idx1_d = [c[0] for c in idx[1]]
        idx1_docid = []
        for _ in idx1_d:
            idx1_docid.append(_[0])
        for i, c in enumerate(idx[0]):
            if idx[0][i][0][0] in idx1_docid:
                for j in range(1, len(idx[0][i])):
                    # print(idx[1][i][0][0])
                    if idx[0][i][j] + 1 in idx[1][idx1_docid.index(idx[0][i][0][0])]:
                        result.append(idx[0][i][0][0])
    return result

def query(qy,logic,doc):#qy
    #index=queryw(qy)
    if ('and'not in qy) and ('or' not in qy) and len(qy)>1:
        index=queryp(qy,logic,doc)
    else:
        index=queryw(qy,logic,doc)
    return index

def printcontent(index,dir):
    cnt = 0
    c = 0
    docname = []
    for dn in os.listdir(dir):
        docname.append(dn)
    a = []
    for _ in range(len(docname)):
        for k in index:
            if k == _ and docname[_] not in a:
                print(docname[_])
                a.append(docname[_])