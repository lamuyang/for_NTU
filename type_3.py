import os,re,pickle
from typing_extensions import final
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import get_data,pkl_input
# ngram_add = ["社區總體營造","資訊偶遇","數位典藏","參考服務","書目資源共享","開放原始碼軟體","生物醫學","智慧圖書館","國家圖書館","資訊超載","網路互動工具","連續性資源","繼續教育"]
part_of_sentance = ["A","Na","Nc","Ncd","Nb","Nep","Neqa","Neqb","Nes","Nh","Nv","VA","VAC","VB","VC","VCL","VD","VF","VE","VG","VH","VHC","VI","VJ","VK","VL","V_2","FW"]
part_of_sentance_for_reference = ["A","Na","Nc","Ncd","Nb","Nep","Neqa","Neqb","Nes","Nh","Nv","VA","VAC","VB","VC","VCL","VD","VF","VE","VG","VH","VHC","VI","VJ","VK","VL","V_2"]

def remove_punctuation(line):
    rule = re.compile("[^a-zA-Z0-9\\u4e00-\\u9fa5]")
    line = rule.sub(' ',line)
    return line
def remove_number(line):
    rule = re.compile('[0-9]+')
    line = rule.sub(' ',line)
    return line
def remove_space(line):
    while "  " in line:
        rule = re.compile('  ')
        line = rule.sub(' ',line)
    return line

def ws_to_list(list,pkl_name,r_dic = {},force_dic = {}):
    new_list = []
    for i in list:
        i = i.replace('\n', '').replace('\r', '')
        new_list.append(i)
    os.environ["CUDA_VISIBLE_DEVICES"] = "0" 
    ws = WS("./data", disable_cuda=False)
    ner = NER("./data", disable_cuda=False)
    r_dic = construct_dictionary(r_dic)
    force_dic = construct_dictionary(force_dic)
    word_sentence_list = ws(
        new_list,
        sentence_segmentation = True, # To consider delimiters
        segment_delimiter_set = {",", "。", ":", "?", "!", ";","-","──","》","《","\\n",'民', '年', '月', '頁','日'," "},
        recommend_dictionary = r_dic,
        coerce_dictionary = force_dic,
    )
    del ws,ner
    with open(pkl_name, 'wb') as fp:
        pickle.dump(word_sentence_list, fp)
    print("WS done")
    return word_sentence_list

def pos_to_list(word_sentence_list,pkl_name):
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    pos = POS("./data", disable_cuda=False)
    pos_sentence_list = pos(word_sentence_list)
    del pos
    with open(pkl_name, 'wb') as fp:
        pickle.dump(pos_sentence_list, fp)
    print("POS done")
    return pos_sentence_list

def ner_to_list(word_sentence_list,pos_sentence_list,pkl_name):
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    ner = NER("./data", disable_cuda=False)
    entity_sentence_list = ner(word_sentence_list, pos_sentence_list)
    del ner
    with open(pkl_name, 'wb') as fp:
        pickle.dump(entity_sentence_list, fp)
    print("NER done")
    return entity_sentence_list

def wash_ws_result(WS_list,POS_list,WS_pkl_name,POS_pkl_name,file_name,part_of_Sentence):
    ND_filter = ["1","2","3","4","5","6","7","8","9","0","年","月","日","週"]
    new_ws_list = []
    new_pos_list = []
    for i in range(0,len(WS_list)):
        # print(POS_list[i])
        # print(WS_list[i])
        new_WS = []
        new_POS = []
        for j in range(0,len(WS_list[i])):
            # print(POS_list[i][j]) 
            if POS_list[i][j] in part_of_Sentence:
                new_WS.append(WS_list[i][j])
                new_POS.append(POS_list[i][j])
            elif POS_list[i][j] == "Nd":
                temp = 0
                for z in WS_list[i][j]:
                    if z in ND_filter:
                        temp += 1
                        print(z)
                        print(temp)
                if temp == 0:
                    new_WS.append(WS_list[i][j])
                    new_POS.append(POS_list[i][j])
                    print(WS_list[i][j])

        new_ws_list.append(new_WS)
        new_pos_list.append(new_POS)
    # for i in range(0,len(new_ws_list)):
        # print(new_ws_list[i])
        # print(new_pos_list[i])
        # print("===============")
    with open(WS_pkl_name, 'wb') as fp:
        pickle.dump(new_ws_list, fp)
    with open(POS_pkl_name, 'wb') as fp:
        pickle.dump(new_pos_list, fp)
    with open(file_name,"w") as file:
        for i , j in zip(new_ws_list,new_pos_list):
            for word,pos in zip(i,j):
                file.write(f"{word}({pos})  ")
            file.write("\n=================\n")
    print("washed done")

name,keyword,abstract,content,reference = [],[],[],[],[]
allfields_list = get_data.get_mongodb_row("LINS")
raw_name,keyword,raw_abstract,raw_content,raw_reference = get_data.pre_data(name,keyword,abstract,content,reference,allfields_list)

new_keyword = []
for i in keyword:
    temp = i.split("、")
    for i in temp:
        new_keyword.append(i)
keyword_dic = {}
for i in new_keyword:
    keyword_dic[i] = 1
#ngram_add = ["社區總體營造","資訊偶遇","數位典藏","參考服務","書目資源共享","開放原始碼軟體","生物醫學","智慧圖書館","國家圖書館","資訊超載","網路互動工具","連續性資源","繼續教育"]
with open("corpus_wikidict_PAGETITLE.pkl", 'rb') as fp:
    WIKI_DIC = pickle.load(fp)

n_gram = ["臺灣學研究","嬰幼兒","WorldCat","文史工作室","臺灣佛教圖書館","縮微資料","全民健康保險","文史工作室","中國國民黨","農業改良場","中央健康保險","內政部建築研究所"]
n_gram_dic = {}
for i in n_gram:
    n_gram_dic[i] = 1
#==========================
# CKIP_WS_name = ws_to_list(raw_name,"./NewPklData/CKIP_WS_name.pkl") #完成
# CKIP_keyword_WS_name = ws_to_list(raw_name,"./NewPklData/CKIP_keyword_WS_name.pkl",{},keyword_dic)
# CKIP_WIKI_WS_name = ws_to_list(raw_name,"./NewPklData/CKIP_WIKI_WS_name.pkl",WIKI_DIC)
# CKIP_WIKI_keyword_WS_name = ws_to_list(raw_name,"./NewPklData/CKIP_WIKI_keyword_WS_name.pkl",WIKI_DIC,keyword_dic)
# CKIP_WIKI_Ngram_WS_name = ws_to_list(raw_name,"./NewPklData/CKIP_WIKI_Ngram_WS_name.pkl",WIKI_DIC,n_gram_dic)
# # write file
# pkl_input.read_to_txt("./NewPklData/CKIP_WS_name.pkl","./NewPklData/CKIP_WS_name.txt")
# pkl_input.read_to_txt("./NewPklData/CKIP_keyword_WS_name.pkl","./NewPklData/CKIP_keyword_WS_name.txt")
# pkl_input.read_to_txt("./NewPklData/CKIP_WIKI_WS_name.pkl","./NewPklData/CKIP_WIKI_WS_name.txt")
# pkl_input.read_to_txt("./NewPklData/CKIP_WIKI_keyword_WS_name.pkl","./NewPklData/CKIP_WIKI_keyword_WS_name.txt")


# # ws_to_list(raw_name,"./NewPklData/CKIP_WIKI_n-gram_WS_name.pkl")
# # ws_to_list(raw_name,"./NewPklData/CKIP_n-gram_WS_name.pkl")
# # ws_to_list(raw_name,"./NewPklData/CKIP_WIKI_n-gram_WS_name.pkl")
# CKIP_POS_name = pos_to_list(CKIP_WS_name,"./NewPklData/POS_CKIP_name.pkl")
# CKIP_keyword_POS_name = pos_to_list(CKIP_keyword_WS_name,"./NewPklData/POS_CKIP_keyword_name.pkl")
# CKIP_WIKI_POS_name = pos_to_list(CKIP_WIKI_WS_name,"./NewPklData/POS_CKIP_WIKI_name.pkl")
# CKIP_WIKI_keyword_POS_name = pos_to_list(CKIP_WIKI_keyword_WS_name,"./NewPklData/POS_CKIP_WIKI_keyword_name.pkl")
# CKIP_WIKI_Ngram_POS_name = pos_to_list(CKIP_WIKI_Ngram_WS_name,"./NewPklData/POS_CKIP_WIKI_Ngram_name.pkl")

# CKIP_NER_name = ner_to_list(CKIP_WS_name,CKIP_POS_name,"./NewPklData/NER_CKIP_name.pkl")
# CKIP_keyword_NER_name = ner_to_list(CKIP_keyword_WS_name,CKIP_keyword_POS_name,"./NewPklData/NER_CKIP_keyword_name.pkl")
# CKIP_WIKI_NER_name = ner_to_list(CKIP_WIKI_WS_name,CKIP_WIKI_POS_name,"./NewPklData/NER_CKIP_WIKI_name.pkl")
# CKIP_WIKI_keyword_NER_name = ner_to_list(CKIP_WIKI_keyword_WS_name,CKIP_WIKI_keyword_POS_name,"./NewPklData/NER_CKIP_WIKI_keyword_name.pkl")
# CKIP_WIKI_Ngram_NER_name = ner_to_list(CKIP_WIKI_Ngram_WS_name,CKIP_WIKI_Ngram_POS_name,"./NewPklData/NER_CKIP_WIKI_Ngram_name.pkl")

# wash_ws_result(CKIP_WS_name,CKIP_POS_name,"./NewPklData/washed_WS_CKIP_name.pkl","./NewPklData/washed_POS_CKIP_name.pkl","temp_name1.txt",part_of_sentance)
# wash_ws_result(CKIP_keyword_WS_name,CKIP_keyword_POS_name,"./NewPklData/washed_WS_CKIP_keyword_name.pkl","./NewPklData/washed_POS_CKIP_keyword_name.pkl","temp_name2.txt",part_of_sentance)
# wash_ws_result(CKIP_WIKI_WS_name,CKIP_WIKI_POS_name,"./NewPklData/washed_WS_CKIP_WIKI_name.pkl","./NewPklData/washed_POS_CKIP_WIKI_name.pkl","temp_name3.txt",part_of_sentance)
# wash_ws_result(CKIP_WIKI_keyword_WS_name,CKIP_WIKI_keyword_POS_name,"./NewPklData/washed_WS_CKIP_WIKI_keyword_name.pkl","./NewPklData/washed_POS_CKIP_WIKI_keyword_name.pkl","temp_name4_1.txt",part_of_sentance)
# wash_ws_result(CKIP_WIKI_Ngram_WS_name,CKIP_WIKI_Ngram_POS_name,"./NewPklData/washed_WS_CKIP_WIKI_Ngram_name.pkl","./NewPklData/washed_POS_CKIP_WIKI_Ngram_name.pkl","temp_name4_2.txt",part_of_sentance)

# print("Name done")
''' sample
CKIP_WIKI_Ngram_WS_reference = ws_to_list(raw_reference,"./NewPklData/CKIP_WIKI_Ngram_WS_reference.pkl",WIKI_DIC,n_gram_dic)
CKIP_WIKI_Ngram_POS_reference = pos_to_list(CKIP_WIKI_Ngram_WS_reference,"./NewPklData/POS_CKIP_WIKI_Ngram_reference.pkl")
CKIP_WIKI_Ngram_NER_reference = ner_to_list(CKIP_WIKI_Ngram_WS_reference,CKIP_WIKI_Ngram_POS_reference,"./NewPklData/NER_CKIP_WIKI_Ngram_reference.pkl")
wash_ws_result(CKIP_WIKI_Ngram_WS_reference,CKIP_WIKI_Ngram_POS_reference,"./NewPklData/washed_WS_CKIP_WIKI_Ngram_reference.pkl","./NewPklData/washed_POS_CKIP_WIKI_Ngram_reference.pkl","temp_reference4_2.txt",part_of_sentance)
'''
# #==========================

# CKIP_WS_abstract = ws_to_list(raw_abstract,"./NewPklData/CKIP_WS_abstract.pkl") #完成
# CKIP_keyword_WS_abstract = ws_to_list(raw_abstract,"./NewPklData/CKIP_keyword_WS_abstract.pkl",{},keyword_dic) 
# CKIP_WIKI_WS_abstract = ws_to_list(raw_abstract,"./NewPklData/CKIP_WIKI_WS_abstract.pkl",WIKI_DIC)
# CKIP_WIKI_keyword_WS_abstract = ws_to_list(raw_abstract,"./NewPklData/CKIP_WIKI_keyword_WS_abstract.pkl",WIKI_DIC,keyword_dic)
# CKIP_WIKI_Ngram_WS_abstract = ws_to_list(raw_abstract,"./NewPklData/CKIP_WIKI_Ngram_WS_abstract.pkl",WIKI_DIC,n_gram_dic)
# #write_file
# pkl_input.read_to_txt("./NewPklData/CKIP_WS_abstract.pkl","./NewPklData/CKIP_WS_abstract.txt")
# pkl_input.read_to_txt("./NewPklData/CKIP_keyword_WS_abstract.pkl","./NewPklData/CKIP_keyword_WS_abstract.txt")
# pkl_input.read_to_txt("./NewPklData/CKIP_WIKI_WS_abstract.pkl","./NewPklData/CKIP_WIKI_WS_abstract.txt")
# pkl_input.read_to_txt("./NewPklData/CKIP_WIKI_keyword_WS_abstract.pkl","./NewPklData/CKIP_WIKI_keyword_WS_abstract.txt")
# # ws_to_list(raw_abstract,"./NewPklData/CKIP_WIKI_n-gram_WS_abstract.pkl")
# # ws_to_list(raw_abstract,"./NewPklData/CKIP_n-gram_WS_abstract.pkl")
# # ws_to_list(raw_abstract,"./NewPklData/CKIP_WIKI_n-gram_WS_abstract.pkl")
# CKIP_POS_abstract = pos_to_list(CKIP_WS_abstract,"./NewPklData/POS_CKIP_abstract.pkl")
# CKIP_keyword_POS_abstract = pos_to_list(CKIP_keyword_WS_abstract,"./NewPklData/POS_CKIP_keyword_abstract.pkl")
# CKIP_WIKI_POS_abstract = pos_to_list(CKIP_WIKI_WS_abstract,"./NewPklData/POS_CKIP_WIKI_abstract.pkl")
# CKIP_WIKI_keyword_POS_abstract = pos_to_list(CKIP_WIKI_keyword_WS_abstract,"./NewPklData/POS_CKIP_WIKI_keyword_abstract.pkl")
# CKIP_WIKI_Ngram_POS_abstract = pos_to_list(CKIP_WIKI_Ngram_WS_abstract,"./NewPklData/POS_CKIP_WIKI_Ngram_abstract.pkl")

# CKIP_NER_abstract = ner_to_list(CKIP_WS_abstract,CKIP_POS_abstract,"./NewPklData/NER_CKIP_abstract.pkl")
# CKIP_keyword_NER_abstract = ner_to_list(CKIP_keyword_WS_abstract,CKIP_keyword_POS_abstract,"./NewPklData/NER_CKIP_keyword_abstract.pkl")
# CKIP_WIKI_NER_abstract = ner_to_list(CKIP_WIKI_WS_abstract,CKIP_WIKI_POS_abstract,"./NewPklData/NER_CKIP_WIKI_abstract.pkl")
# CKIP_WIKI_keyword_NER_abstract = ner_to_list(CKIP_WIKI_keyword_WS_abstract,CKIP_WIKI_keyword_POS_abstract,"./NewPklData/NER_CKIP_WIKI_keyword_abstract.pkl")
# CKIP_WIKI_Ngram_NER_abstract = ner_to_list(CKIP_WIKI_Ngram_WS_abstract,CKIP_WIKI_Ngram_POS_abstract,"./NewPklData/NER_CKIP_WIKI_Ngram_abstract.pkl")

# wash_ws_result(CKIP_WS_abstract,CKIP_POS_abstract,"./NewPklData/washed_WS_CKIP_abstract.pkl","./NewPklData/washed_POS_CKIP_abstract.pkl","temp_abstract1.txt",part_of_sentance)
# wash_ws_result(CKIP_keyword_WS_abstract,CKIP_keyword_POS_abstract,"./NewPklData/washed_WS_CKIP_keyword_abstract.pkl","./NewPklData/washed_POS_CKIP_keyword_abstract.pkl","temp_abstract2.txt",part_of_sentance)
# wash_ws_result(CKIP_WIKI_WS_abstract,CKIP_WIKI_POS_abstract,"./NewPklData/washed_WS_CKIP_WIKI_abstract.pkl","./NewPklData/washed_POS_CKIP_WIKI_abstract.pkl","temp_abstract3.txt",part_of_sentance)
# wash_ws_result(CKIP_WIKI_keyword_WS_abstract,CKIP_WIKI_keyword_POS_abstract,"./NewPklData/washed_WS_CKIP_WIKI_keyword_abstract.pkl","./NewPklData/washed_POS_CKIP_WIKI_keyword_abstract.pkl","temp_abstract4_1.txt",part_of_sentance)
# wash_ws_result(CKIP_WIKI_Ngram_WS_abstract,CKIP_WIKI_Ngram_POS_abstract,"./NewPklData/washed_WS_CKIP_WIKI_Ngram_abstract.pkl","./NewPklData/washed_POS_CKIP_WIKI_Ngram_abstract.pkl","temp_abstract4_2.txt",part_of_sentance)

# print("AB done")
# #==========================


# CKIP_WS_reference = ws_to_list(raw_reference,"./NewPklData/CKIP_WS_reference.pkl") #完成
# CKIP_keyword_WS_reference = ws_to_list(raw_reference,"./NewPklData/CKIP_keyword_WS_reference.pkl",{},keyword_dic) 
# CKIP_WIKI_WS_reference = ws_to_list(raw_reference,"./NewPklData/CKIP_WIKI_WS_reference.pkl",WIKI_DIC)
# CKIP_WIKI_keyword_WS_reference = ws_to_list(raw_reference,"./NewPklData/CKIP_WIKI_keyword_WS_reference.pkl",WIKI_DIC,keyword_dic)
# CKIP_WIKI_Ngram_WS_reference = ws_to_list(raw_reference,"./NewPklData/CKIP_WIKI_Ngram_WS_reference.pkl",WIKI_DIC,n_gram_dic)
# #write_file
# pkl_input.read_to_txt("./NewPklData/CKIP_WS_reference.pkl","./NewPklData/CKIP_WS_reference.txt")
# pkl_input.read_to_txt("./NewPklData/CKIP_keyword_WS_reference.pkl","./NewPklData/CKIP_keyword_WS_reference.txt")
# pkl_input.read_to_txt("./NewPklData/CKIP_WIKI_WS_reference.pkl","./NewPklData/CKIP_WIKI_WS_reference.txt")
# pkl_input.read_to_txt("./NewPklData/CKIP_WIKI_keyword_WS_reference.pkl","./NewPklData/CKIP_WIKI_keyword_WS_reference.txt")
# # ws_to_list(raw_reference,"./NewPklData/CKIP_WIKI_n-gram_WS_reference.pkl")
# # ws_to_list(raw_reference,"./NewPklData/CKIP_n-gram_WS_reference.pkl")
# # ws_to_list(raw_reference,"./NewPklData/CKIP_WIKI_n-gram_WS_reference.pkl")
# CKIP_POS_reference = pos_to_list(CKIP_WS_reference,"./NewPklData/POS_CKIP_reference.pkl")
# CKIP_keyword_POS_reference = pos_to_list(CKIP_keyword_WS_reference,"./NewPklData/POS_CKIP_keyword_reference.pkl")
# CKIP_WIKI_POS_reference = pos_to_list(CKIP_WIKI_WS_reference,"./NewPklData/POS_CKIP_WIKI_reference.pkl")
# CKIP_WIKI_keyword_POS_reference = pos_to_list(CKIP_WIKI_keyword_WS_reference,"./NewPklData/POS_CKIP_WIKI_keyword_reference.pkl")
# CKIP_WIKI_Ngram_POS_reference = pos_to_list(CKIP_WIKI_Ngram_WS_reference,"./NewPklData/POS_CKIP_WIKI_Ngram_reference.pkl")

# CKIP_NER_reference = ner_to_list(CKIP_WS_reference,CKIP_POS_reference,"./NewPklData/NER_CKIP_reference.pkl")
# CKIP_keyword_NER_reference = ner_to_list(CKIP_keyword_WS_reference,CKIP_keyword_POS_reference,"./NewPklData/NER_CKIP_keyword_reference.pkl")
# CKIP_WIKI_NER_reference = ner_to_list(CKIP_WIKI_WS_reference,CKIP_WIKI_POS_reference,"./NewPklData/NER_CKIP_WIKI_reference.pkl")
# CKIP_WIKI_keyword_NER_reference = ner_to_list(CKIP_WIKI_keyword_WS_reference,CKIP_WIKI_keyword_POS_reference,"./NewPklData/NER_CKIP_WIKI_keyword_reference.pkl")
# CKIP_WIKI_Ngram_NER_reference = ner_to_list(CKIP_WIKI_Ngram_WS_reference,CKIP_WIKI_Ngram_POS_reference,"./NewPklData/NER_CKIP_WIKI_Ngram_reference.pkl")

# wash_ws_result(CKIP_WS_reference,CKIP_POS_reference,"./NewPklData/washed_WS_CKIP_reference.pkl","./NewPklData/washed_POS_CKIP_reference.pkl","temp_reference1.txt",part_of_sentance_for_reference)
# wash_ws_result(CKIP_keyword_WS_reference,CKIP_keyword_POS_reference,"./NewPklData/washed_WS_CKIP_keyword_reference.pkl","./NewPklData/washed_POS_CKIP_keyword_reference.pkl","temp_reference2.txt",part_of_sentance_for_reference)
# wash_ws_result(CKIP_WIKI_WS_reference,CKIP_WIKI_POS_reference,"./NewPklData/washed_WS_CKIP_WIKI_reference.pkl","./NewPklData/washed_POS_CKIP_WIKI_reference.pkl","temp_reference3.txt",part_of_sentance_for_reference)
# wash_ws_result(CKIP_WIKI_keyword_WS_reference,CKIP_WIKI_keyword_POS_reference,"./NewPklData/washed_WS_CKIP_WIKI_keyword_reference.pkl","./NewPklData/washed_POS_CKIP_WIKI_keyword_reference.pkl","temp_reference4_1.txt",part_of_sentance_for_reference)
# wash_ws_result(CKIP_WIKI_Ngram_WS_reference,CKIP_WIKI_Ngram_POS_reference,"./NewPklData/washed_WS_CKIP_WIKI_Ngram_reference.pkl","./NewPklData/washed_POS_CKIP_WIKI_Ngram_reference.pkl","temp_reference4_2.txt",part_of_sentance_for_reference)



# final_
ngram_keyword_dic = {}
ngram_keyword_dic.update(keyword_dic)
ngram_keyword_dic.update(n_gram_dic)

print("start final")
CKIP_WIKI_Ngram_keyword_WS_name = ws_to_list(raw_name,"./NewPklData/final_CKIP_WIKI_Ngram_keyword_WS_name.pkl",WIKI_DIC,ngram_keyword_dic)
CKIP_WIKI_Ngram_keyword_POS_name = pos_to_list(CKIP_WIKI_Ngram_keyword_WS_name,"./NewPklData/final_POS_CKIP_WIKI_Ngram_keyword_name.pkl")
CKIP_WIKI_Ngram_keyword_NER_name = ner_to_list(CKIP_WIKI_Ngram_keyword_WS_name,CKIP_WIKI_Ngram_keyword_POS_name,"./NewPklData/final_NER_CKIP_WIKI_Ngram_keyword_name.pkl")
wash_ws_result(CKIP_WIKI_Ngram_keyword_WS_name,CKIP_WIKI_Ngram_keyword_POS_name,"./NewPklData/final_washed_WS_CKIP_WIKI_Ngram_keyword_name.pkl","./NewPklData/final_washed_POS_CKIP_WIKI_Ngram_keyword_name.pkl","final_temp_name4_3.txt",part_of_sentance)
print("final name done")
CKIP_WIKI_Ngram_keyword_WS_abstract = ws_to_list(raw_abstract,"./NewPklData/final_CKIP_WIKI_Ngram_keyword_WS_abstract.pkl",WIKI_DIC,ngram_keyword_dic)
CKIP_WIKI_Ngram_keyword_POS_abstract = pos_to_list(CKIP_WIKI_Ngram_keyword_WS_abstract,"./NewPklData/final_POS_CKIP_WIKI_Ngram_keyword_abstract.pkl")
CKIP_WIKI_Ngram_keyword_NER_abstract = ner_to_list(CKIP_WIKI_Ngram_keyword_WS_abstract,CKIP_WIKI_Ngram_keyword_POS_abstract,"./NewPklData/final_NER_CKIP_WIKI_Ngram_keyword_abstract.pkl")
wash_ws_result(CKIP_WIKI_Ngram_keyword_WS_abstract,CKIP_WIKI_Ngram_keyword_POS_abstract,"./NewPklData/final_washed_WS_CKIP_WIKI_Ngram_keyword_abstract.pkl","./NewPklData/final_washed_POS_CKIP_WIKI_Ngram_keyword_abstract.pkl","final_temp_abstract4_3.txt",part_of_sentance)
print("final name abstract")
CKIP_WIKI_Ngram_keyword_WS_reference = ws_to_list(raw_reference,"./NewPklData/final_CKIP_WIKI_Ngram_keyword_WS_reference.pkl",WIKI_DIC,ngram_keyword_dic)
CKIP_WIKI_Ngram_keyword_POS_reference = pos_to_list(CKIP_WIKI_Ngram_keyword_WS_reference,"./NewPklData/final_POS_CKIP_WIKI_Ngram_keyword_reference.pkl")
CKIP_WIKI_Ngram_keyword_NER_reference = ner_to_list(CKIP_WIKI_Ngram_keyword_WS_reference,CKIP_WIKI_Ngram_keyword_POS_reference,"./NewPklData/final_NER_CKIP_WIKI_Ngram_keyword_reference.pkl")
wash_ws_result(CKIP_WIKI_Ngram_keyword_WS_reference,CKIP_WIKI_Ngram_keyword_POS_reference,"./NewPklData/final_washed_WS_CKIP_WIKI_Ngram_keyword_reference.pkl","./NewPklData/final_washed_POS_CKIP_WIKI_Ngram_keyword_reference.pkl","final_temp_reference4_3.txt",part_of_sentance_for_reference)
print("final name reference")
