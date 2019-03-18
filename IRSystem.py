import os
import string
import tkinter
from tkinter import *
import subprocess as sub

def printButton():
    query = entry_2.get()
    print(query)

def QueryButton():
    dir = entry_1.get()
    qqq = entry_2.get()
    #txt = text_1.get()
    # get stopwords---sw1
    sw = open("english-stop.txt")
    sw1 = sw.read().split()

    # get original document list with punctuations and numbers
    #dir = "data/"
    dlist = []
    tmp = []
    for dn in os.listdir(dir):
        m1 = []
        f = open(dir + dn)  # get content
        d = f.read()
        d = d.split()
        for j in d:
            j = j.lower()
            m1.append(j)  # in a document a term can repeat
            if j not in tmp:
                tmp.append(j)
        dlist.append(m1)

    # remove punctuations and numbers
    d1 = []
    for m in tmp:
        pp = m.translate(str.maketrans('', '', string.punctuation)).lower()
        ppp = pp.translate(str.maketrans('', '', '1234567890'))
        d1.append(ppp)

    # build term list
    terml = []
    for q in d1:
        if q in sw1 or q == '':
            continue
        else:
            if q not in terml:
                terml.append(q)
    terml.sort()  # sort term list

    doc = []
    # build doc without stopwords punctuations and numbers
    for a in dlist:
        m2 = []
        for b in a:  # remove stopwords, punctuations and numbers in docs
            pp = b.translate(str.maketrans('', '', string.punctuation)).lower()
            ppp = pp.translate(str.maketrans('', '', '1234567890'))
            if ppp != "" and ppp not in sw1:
                m2.append(ppp)
        doc.append(m2)

    freql = []  # record term frequency
    for c in terml:
        s = 0
        for docs in doc:
            s += docs.count(c)
        freql.append(s)

    # user query

    query = qqq.lower()  # lower the query
    qy = query.split()
    if 'and' in qy:  # the signal of query containing logic word(s)
        logic = 1
    elif 'or' in qy:
        logic = 2
    else:  # no logic words
        logic = 3

    # use linked-list data structure to store term, its frequency and posting list
    def queryw(x):
        idx = []
        if logic == 3:  # sigal word
            tmp = []
            tmp.append(x[0])
            # print(x[0])
            for f in range(len(doc)):
                if x[0] in doc[f]:  # traverse all the documents to get posting list
                    tmp.append(f)  # posting list
            for _ in tmp:
                idx.append(_)
            # if query == terml[e]:
            # print(idx)
        else:
            k = []
            for _ in x:
                if 'or' in x:
                    x.pop(x.index('or'))
                elif 'and' in x:
                    x.pop(x.index('and'))
            for _ in range(len(x)):
                tmm = []
                # link_list = LinkedList()
                tup = (x[_], freql[terml.index(x[_])])
                tmm.append(tup)
                for f in range(len(doc)):
                    if x[_] in doc[f]:
                        tmm.append(f)
                k.append(tmm[1:])
            if logic == 2:  # 'or'
                # print(1)
                for m in k:  # union
                    for n in m:
                        if n not in idx:
                            idx.append(n)
            elif logic == 1:  # 'and'
                for m in range(1, len(k)):  # intersection
                    u = [val for val in k[m - 1] if val in k[m]]
                    for _ in u:
                        idx.append(_)
        return idx

    def queryp(x):
        idx = []
        for w in range(len(x)):
            LLL = []
            for k in doc:  # doc is a 2 dimentional list, k is a document
                LL = []
                if x[w] in k:
                    # link_list1 = LinkedList()
                    tmm = []
                    tup = (doc.index(k), k.count(x[w]))
                    tmm.append(tup)
                    for index, s in enumerate(k):
                        if s == x[w]:
                            tmm.append(index)
                    LL.append(tmm)
                if LL != []:
                    for _ in LL:
                        LLL.append(_)
            if LLL != []:
                idx.append(LLL)
        result = []
        # print(idx)
        if len(idx[0]) >= len(idx[1]):
            idx0_d = [c[0] for c in idx[0]]
            idx0_docid = []
            for _ in idx0_d:
                idx0_docid.append(_[0])
            # print(idx0_docid)
            for i, c in enumerate(idx[1]):
                if idx[1][i][0][0] in idx0_docid:
                    for j in range(1, len(idx[1][i])):
                        # print(idx[1][i][0][0])
                        if idx[1][i][j] - 1 in idx[0][idx0_docid.index(idx[1][i][0][0])]:
                            result.append(idx[1][i][0][0])
        elif len(idx[0]) < len(idx[1]):
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

    # index=queryw(qy)
    if ('and' not in qy) and ('or' not in qy) and len(qy) > 1:
        index = queryp(qy)
    else:
        index = queryw(qy)

    # return document content
    cnt = 0
    c = 0
    docname = []
    for dn in os.listdir(dir):
        docname.append(dn)
        if cnt in index:
            docname.append(dn)
            ff=open(dir+dn)
            f1=ff.read()
            var1='['+dn+']'+':'+'\n'
            text_1.insert('insert', var1)
            var2=f1+'\n'
            text_1.insert('insert', var2)
            #print(dn)
        cnt += 1  # every dn, cnt should +1
    """
    a = []
    for _ in range(len(docname)):
        for k in index:
            if k == _ and docname[_] not in a:
                #print(docname[_])
                #text_1.insert(INSERT, docname[_])
                #a.append(docname[_])
                var=docname[_]+'\n'
                text_1.insert('insert',var)

    #txt.insert(INSERT, a)
    """

root = Tk()
root.geometry()

label_1 = Label(text='Directory')
label_1.pack()
entry_1 = Entry()
entry_1.pack()
label_2 = Label(text='Query')
label_2.pack()
entry_2 = Entry()
entry_2.pack()
label_3 = Label(text='Relevant Docs')
label_3.pack()

#label_1.grid(row=0)
#label_2.grid(row=1)
#label_3.grid(row=2)
#entry_1.grid(row=0,column=1,sticky=W)
#entry_2.grid(row=1,column=1,sticky=W)

scroll = tkinter.Scrollbar()
queryButton= Button(text='Go', width=5,command=QueryButton)
#queryButton.grid(row=5,column=1,sticky=E)
queryButton.pack()
text_1=Text(root)
#text_1.grid(row=2,column=1)
#text_1.pack()
scroll.pack(side=tkinter.RIGHT,fill=tkinter.Y) # side是滚动条放置的位置，上下左右。fill是将滚动条沿着y轴填充
text_1.pack(side=tkinter.LEFT,fill=tkinter.Y) # 将文本框填充进wuya窗口的左侧，
# 将滚动条与文本框关联
scroll.config(command=text_1.yview) # 将文本框关联到滚动条上，滚动条滑动，文本框跟随滑动
text_1.config(yscrollcommand=scroll.set) # 将滚动条关联到文本框




root.title('IRsystem')
root.mainloop()