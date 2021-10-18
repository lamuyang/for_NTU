import pkl_input
title = pkl_input.open_pkl("./NewPklData/final_NER_CKIP_WIKI_Ngram_keyword_name.pkl")
abstract = pkl_input.open_pkl("./NewPklData/final_NER_CKIP_WIKI_Ngram_keyword_abstract.pkl")
reference = pkl_input.open_pkl("./NewPklData/final_NER_CKIP_WIKI_Ngram_keyword_reference.pkl")

fin_name = pkl_input.open_pkl("./NewPklData/final_washed_WS_CKIP_WIKI_Ngram_keyword_name.pkl")
fin_abstract = pkl_input.open_pkl("./NewPklData/final_washed_WS_CKIP_WIKI_Ngram_keyword_abstract.pkl")
fin_reference = pkl_input.open_pkl("./NewPklData/final_washed_WS_CKIP_WIKI_Ngram_keyword_reference.pkl")

ws_POS_reference = pkl_input.open_pkl("./NewPklData/final_washed_POS_CKIP_WIKI_Ngram_keyword_reference.pkl")
def check(data,name,number):
    temp = []
    count = 0
    for i in data:
        for j in i :
            j = list(j)
            if name in j[number]:
                # print(j)
                # print(count)
                if j not in temp:
                    temp.append(j[3])
        count +=1
        # break
    print("=============")
    return temp
# check(reference,"杜威",3)
# print(len(fin_reference[0]))
# print(len(ws_POS_reference[0]))

count = 0
for i in fin_reference:
    for j in i:
        if "杜威" in j:
            print(i)
        break
# print(fin_reference[58])
# print("=============")
# print(fin_reference[134])

# from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
# ner = NER("./data", disable_cuda=False)
# entity_sentence_list = ner(fin_reference, ws_POS_reference)
# del ner
import pickle
# with open("00000_temp_NER.pkl", 'wb') as fp:
#         pickle.dump(entity_sentence_list, fp)

# print(entity_sentence_list[58])
# print(entity_sentence_list[134])
new_ner = pkl_input.open_pkl("00000_temp_NER.pkl")
temp = check(new_ner,"PERSON",2)
# print(temp)

new_ws = []

for i in fin_reference:
    temtem = []
    for j in i:
        if j not in temp:
            temtem.append(j)
    new_ws.append(temtem)

with open("de_named_final_WS_refernece.pkl", 'wb') as fp:
        pickle.dump(new_ws, fp)
print(len(new_ws))
print(fin_reference[9]) 
print(len(fin_reference[9]))
print(new_ws[9]) 
print(len(new_ws[9]))

# ”,&  ,
# 為、例
# 日、期
# ——