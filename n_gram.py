import pkl_input
from operator import itemgetter
import re
def list2freqdict(mylist):
    mydict=dict()
    for ch in mylist:
        mydict[ch]=mydict.get(ch,0)+1
    return mydict
def list2bigram(mylist):
    return [mylist[i:i+2] for i in range(0,len(mylist)-1)]

def list2trigram(mylist):
    return [mylist[i:i+3] for i in range(0,len(mylist)-2)]

def bigram2freqdict(mybigram):
    mydict=dict()
    for (ch1,ch2) in mybigram:
        mydict[(ch1,ch2)]=mydict.get((ch1,ch2),0)+1
    return mydict

def trigram2freqdict(mytrigram):
    mydict=dict()
    for (ch1,ch2,ch3) in mytrigram:
        mydict[(ch1,ch2,ch3)]=mydict.get((ch1,ch2,ch3),0)+1
    return mydict
def freq2report(freqlist,file_name):
    chs=str()
    # print('Char(s)\tCount')
    # print('=============')
    with open(file_name,"w") as fileobj:
        for (token,num) in freqlist:
            for ch in token:
                chs=chs+" ("+ch+")"
            # print(chs,'\t',num)
            fileobj.write(f"{chs}\t{num}\n")
            chs=''
    print("done")
def remove_punctuation(line):
    rule = re.compile("[^a-zA-Z0-9\\u4e00-\\u9fa5]")
    line = rule.sub(' ',line)
    return line
def auto_depunctuation(raw_list):
    new_list = []
    for i in raw_list:
        new_i = []
        for j in i:
            j = remove_punctuation(j)
            if j != "":
                new_i.append(j)
        new_list.append(new_i)
    return new_list
raw_name = pkl_input.open_pkl("./NewPklData/CKIP_WIKI_keyword_WS_reference.pkl")
print(len(raw_name))
print(raw_name[0])
# raw_abstract = pkl_input.open_pkl("./Pkl_data/WS_abstract.pkl")
# raw_reference = pkl_input.open_pkl("./Pkl_data/WS_reference.pkl")
name = auto_depunctuation(raw_name)
# abstract = auto_depunctuation(raw_abstract)
# reference = auto_depunctuation(raw_reference)
big_fin = {}
tri_fin = {}
for i in name:
    big_fin.update(bigram2freqdict(list2bigram(i)))
    tri_fin.update(trigram2freqdict(list2trigram(i)))
# for i in abstract:
#     big_fin.update(bigram2freqdict(list2bigram(i)))
#     tri_fin.update(trigram2freqdict(list2trigram(i)))
# for i in reference:
#     big_fin.update(bigram2freqdict(list2bigram(i)))
#     tri_fin.update(trigram2freqdict(list2trigram(i)))


# print(big_fin)
big_sorted = sorted(big_fin.items(), key=itemgetter(1), reverse=True)
tri_sorted = sorted(tri_fin.items(), key=itemgetter(1), reverse=True)
print(big_sorted)
bi_over_than_one = []
for (word,num) in big_sorted:
    if num >1:
        bi_over_than_one.append((word,num))
print(bi_over_than_one)
freq2report(bi_over_than_one,"./ngram_data/bi_reference.txt")
tri_over = []
for (word,num) in tri_sorted:
    if num >1:
        tri_over.append((word,num))
# print(bi_over_than_one)
freq2report(tri_over,"./ngram_data/tri_reference.txt")
# print(tri_over)