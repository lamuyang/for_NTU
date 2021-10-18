from re import I
from gensim import corpora,models,similarities
import pkl_input,get_data,descan
stop_word = ["研究","探討","為","例","<<",">>","分析","比較","此","各","一些"]
def stopword(raw_list):
    new_list = []
    for i in raw_list:
        new_i = []
        for j in i:
            if j not in stop_word:
                new_i.append(j)
        new_list.append(new_i)
    return new_list
    
name,keyword,abstract,content,reference = [],[],[],[],[]
allfields_list = get_data.get_mongodb_row("LINS")
raw_name,keyword,raw_abstract,raw_content,raw_reference = get_data.pre_data(name,keyword,abstract,content,reference,allfields_list)
new_keyword = []
for i in keyword:
    temp_temp = []
    temp = i.split("、")
    # print(temp)
    new_keyword.append(temp)
# print(new_keyword)

def get_blank_list(list):
    tem_list = []
    for i in list:
        tem = ""
        for j in i :
            tem = tem + j +" "
        tem_list.append(tem)
    # print("確認長度：",len(tem_list))
    return tem_list


WS_name = stopword(pkl_input.open_pkl("./NewPklData/washed_WS_CKIP_WIKI_keyword_name.pkl"))
WS_abstract = stopword(pkl_input.open_pkl("./NewPklData/washed_WS_CKIP_WIKI_keyword_abstract.pkl"))
WS_reference = stopword(pkl_input.open_pkl("./NewPklData/washed_WS_CKIP_WIKI_keyword_reference.pkl"))
WS_conbine = []
for i in range(0,len(WS_name)):
    new_list = []
    new_list.extend(WS_name[i])
    new_list.extend(WS_abstract[i])
    new_list.extend(new_keyword[i])
    WS_conbine.append(new_list)
# print(WS_conbine[0])
def test(raw_list1,raw_list2):
    dictionary = corpora.Dictionary(raw_list2)
    # print(dictionary.keys())
    # print(dictionary.token2id)
    corpus = [dictionary.doc2bow(doc) for doc in raw_list2]
    doc_test_vec = dictionary.doc2bow(raw_list1)
    tfidf = models.TfidfModel(corpus)
    # print(tfidf[doc_test_vec])
    index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
    sim = index[tfidf[doc_test_vec]]
    # print(sim)
    # print(sorted(enumerate(sim), key=lambda item: -item[1]))
    return sorted(enumerate(sim), key=lambda item: -item[1])
# print(test(WS_conbine[27],WS_conbine))
# print(get_blank_list(WS_conbine)[0])
# WS_conbine = get_blank_list(WS_conbine)
# print(WS_conbine)
# print(descan.main_fun(WS_conbine,1.3237510005995812,4))

name_similaraty = []
for i in range(1,len(WS_reference)):
    name_similaraty.append(test(WS_conbine[i],WS_conbine))
num =1
for i in name_similaraty:
    print(f"{num}")
    for j in range(0,3):
        print(i[j])
    print("========")
    num +=1