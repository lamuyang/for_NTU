import pkl_input
import numpy as np
stop_word = ["研究","探討","為","例","<<",">>","分析","比較"]
def stopword(raw_list):
    new_list = []
    for i in raw_list:
        new_i = []
        for j in i:
            if j not in stop_word:
                new_i.append(j)
        new_list.append(new_i)
    return new_list
# def get_blank_list(list):
#     tem_list = []
#     for i in list:
#         tem = ""
#         for j in i :
#             tem = tem + j +" "
#         tem_list.append(tem)
#     # print("確認長度：",len(tem_list))
#     return tem_list

def get_word_vector(list_word1,list_word2):

    # 列出所有的词,取并集
    key_word = list(set(list_word1 + list_word2))
    # 给定形状和类型的用0填充的矩阵存储向量
    word_vector1 = np.zeros(len(key_word))
    word_vector2 = np.zeros(len(key_word))
 
    # 计算词频
    # 依次确定向量的每个位置的值
    for i in range(len(key_word)):
        # 遍历key_word中每个词在句子中的出现次数
        for j in range(len(list_word1)):
            if key_word[i] == list_word1[j]:
                word_vector1[i] += 1
        for k in range(len(list_word2)):
            if key_word[i] == list_word2[k]:
                word_vector2[i] += 1
    # 输出向量
    # print(word_vector1)
    # print(word_vector2)
    # return word_vector1, word_vector2
    dist1=float(np.dot(word_vector1,word_vector2)/(np.linalg.norm(word_vector1)*np.linalg.norm(word_vector2)))
    return dist1

WS_name = stopword(pkl_input.open_pkl("./NewPklData/washed_WS_CKIP_WIKI_keyword_name.pkl"))
WS_abstract = stopword(pkl_input.open_pkl("./NewPklData/washed_WS_CKIP_WIKI_keyword_abstract.pkl"))
WS_reference = stopword(pkl_input.open_pkl("./NewPklData/washed_WS_CKIP_WIKI_keyword_reference.pkl"))
# for i in WS_abstract:
#     print(i)
name_similaraty = []
for i in range(0,len(WS_reference)):
    temp = []
    for j in range(0,len(WS_name)):
        temp.append(get_word_vector(WS_name[i],WS_name[j]))
    name_similaraty.append(temp)
print(name_similaraty)