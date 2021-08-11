import os,re,pickle
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import get_data,pkl_input
ngram_add = ["社區總體營造","資訊偶遇","數位典藏","參考服務","書目資源共享","開放原始碼軟體","生物醫學","智慧圖書館","國家圖書館","資訊超載","網路互動工具","連續性資源","繼續教育"]
part_of_sentance = ["A","Na","Nb","Nc","Ncd","Nd","Nep","Neqa","Neqb","Nes","Nf","Nh","Nv","VA","VAC","VB","VC","VCL","VD","VF","VE","VG","VH","VHC","VI","VJ","VK","VL","V_2","FW"]

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

def wash_ws_result(WS_list,POS_list,WS_pkl_name,POS_pkl_name,file_name):
    new_ws_list = []
    new_pos_list = []
    for i in range(0,len(WS_list)):
        # print(POS_list[i])
        # print(WS_list[i])
        new_WS = []
        new_POS = []
        for j in range(0,len(WS_list[i])):
            # print(POS_list[i][j]) 
            if POS_list[i][j] in part_of_sentance:
                new_WS.append(WS_list[i][j])
                new_POS.append(POS_list[i][j])
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

#==========================
CKIP_WS_name = ws_to_list(raw_name,"./NewPklData/CKIP_WS_name.pkl") #完成
CKIP_keyword_WS_name = ws_to_list(raw_name,"./NewPklData/CKIP_keyword_WS_name.pkl",{},keyword_dic)
CKIP_WIKI_WS_name = ws_to_list(raw_name,"./NewPklData/CKIP_WIKI_WS_name.pkl",WIKI_DIC)
CKIP_WIKI_keyword_WS_name = ws_to_list(raw_name,"./NewPklData/CKIP_WIKI_keyword_WS_name.pkl",WIKI_DIC,keyword_dic)
# write file
pkl_input.read_to_txt("./NewPklData/CKIP_WS_name.pkl","./NewPklData/CKIP_WS_name.txt")
pkl_input.read_to_txt("./NewPklData/CKIP_keyword_WS_name.pkl","./NewPklData/CKIP_keyword_WS_name.txt")
pkl_input.read_to_txt("./NewPklData/CKIP_WIKI_WS_name.pkl","./NewPklData/CKIP_WIKI_WS_name.txt")
pkl_input.read_to_txt("./NewPklData/CKIP_WIKI_keyword_WS_name.pkl","./NewPklData/CKIP_WIKI_keyword_WS_name.txt")


# ws_to_list(raw_name,"./NewPklData/CKIP_WIKI_n-gram_WS_name.pkl")
# ws_to_list(raw_name,"./NewPklData/CKIP_n-gram_WS_name.pkl")
# ws_to_list(raw_name,"./NewPklData/CKIP_WIKI_n-gram_WS_name.pkl")
CKIP_POS_name = pos_to_list(CKIP_WS_name,"./NewPklData/POS_CKIP_name.pkl")
CKIP_keyword_POS_name = pos_to_list(CKIP_keyword_WS_name,"./NewPklData/POS_CKIP_keyword_name.pkl")
CKIP_WIKI_POS_name = pos_to_list(CKIP_WIKI_WS_name,"./NewPklData/POS_CKIP_WIKI_name.pkl")
CKIP_WIKI_keyword_POS_name = pos_to_list(CKIP_WIKI_keyword_WS_name,"./NewPklData/POS_CKIP_WIKI_keyword_name.pkl")

CKIP_NER_name = ner_to_list(CKIP_WS_name,CKIP_POS_name,"./NewPklData/NER_CKIP_name.pkl")
CKIP_keyword_NER_name = ner_to_list(CKIP_keyword_WS_name,CKIP_keyword_POS_name,"./NewPklData/NER_CKIP_keyword_name.pkl")
CKIP_WIKI_NER_name = ner_to_list(CKIP_WIKI_WS_name,CKIP_WIKI_POS_name,"./NewPklData/NER_CKIP_WIKI_name.pkl")
CKIP_WIKI_keyword_NER_name = ner_to_list(CKIP_WIKI_keyword_WS_name,CKIP_WIKI_keyword_POS_name,"./NewPklData/NER_CKIP_WIKI_keyword_name.pkl")

wash_ws_result(CKIP_WS_name,CKIP_POS_name,"./NewPklData/washed_WS_CKIP_name.pkl","./NewPklData/washed_POS_CKIP_name.pkl","temp_name1.txt")
wash_ws_result(CKIP_keyword_WS_name,CKIP_keyword_POS_name,"./NewPklData/washed_WS_CKIP_keyword_name.pkl","./NewPklData/washed_POS_CKIP_keyword_name.pkl","temp_name2.txt")
wash_ws_result(CKIP_WIKI_WS_name,CKIP_WIKI_POS_name,"./NewPklData/washed_WS_CKIP_WIKI_name.pkl","./NewPklData/washed_POS_CKIP_WIKI_name.pkl","temp_name3.txt")
wash_ws_result(CKIP_WIKI_keyword_WS_name,CKIP_WIKI_keyword_POS_name,"./NewPklData/washed_WS_CKIP_WIKI_keyword_name.pkl","./NewPklData/washed_POS_CKIP_WIKI_keyword_name.pkl","temp_name4.txt")

print("Name done")
#==========================

CKIP_WS_abstract = ws_to_list(raw_abstract,"./NewPklData/CKIP_WS_abstract.pkl") #完成
CKIP_keyword_WS_abstract = ws_to_list(raw_abstract,"./NewPklData/CKIP_keyword_WS_abstract.pkl",{},keyword_dic) 
CKIP_WIKI_WS_abstract = ws_to_list(raw_abstract,"./NewPklData/CKIP_WIKI_WS_abstract.pkl",WIKI_DIC)
CKIP_WIKI_keyword_WS_abstract = ws_to_list(raw_abstract,"./NewPklData/CKIP_WIKI_keyword_WS_abstract.pkl",WIKI_DIC,keyword_dic)
#write_file
pkl_input.read_to_txt("./NewPklData/CKIP_WS_abstract.pkl","./NewPklData/CKIP_WS_abstract.txt")
pkl_input.read_to_txt("./NewPklData/CKIP_keyword_WS_abstract.pkl","./NewPklData/CKIP_keyword_WS_abstract.txt")
pkl_input.read_to_txt("./NewPklData/CKIP_WIKI_WS_abstract.pkl","./NewPklData/CKIP_WIKI_WS_abstract.txt")
pkl_input.read_to_txt("./NewPklData/CKIP_WIKI_keyword_WS_abstract.pkl","./NewPklData/CKIP_WIKI_keyword_WS_abstract.txt")
# ws_to_list(raw_abstract,"./NewPklData/CKIP_WIKI_n-gram_WS_abstract.pkl")
# ws_to_list(raw_abstract,"./NewPklData/CKIP_n-gram_WS_abstract.pkl")
# ws_to_list(raw_abstract,"./NewPklData/CKIP_WIKI_n-gram_WS_abstract.pkl")
CKIP_POS_abstract = pos_to_list(CKIP_WS_abstract,"./NewPklData/POS_CKIP_abstract.pkl")
CKIP_keyword_POS_abstract = pos_to_list(CKIP_keyword_WS_abstract,"./NewPklData/POS_CKIP_keyword_abstract.pkl")
CKIP_WIKI_POS_abstract = pos_to_list(CKIP_WIKI_WS_abstract,"./NewPklData/POS_CKIP_WIKI_abstract.pkl")
CKIP_WIKI_keyword_POS_abstract = pos_to_list(CKIP_WIKI_keyword_WS_abstract,"./NewPklData/POS_CKIP_WIKI_keyword_abstract.pkl")

CKIP_NER_abstract = ner_to_list(CKIP_WS_abstract,CKIP_POS_abstract,"./NewPklData/NER_CKIP_abstract.pkl")
CKIP_keyword_NER_abstract = ner_to_list(CKIP_keyword_WS_abstract,CKIP_keyword_POS_abstract,"./NewPklData/NER_CKIP_keyword_abstract.pkl")
CKIP_WIKI_NER_abstract = ner_to_list(CKIP_WIKI_WS_abstract,CKIP_WIKI_POS_abstract,"./NewPklData/NER_CKIP_WIKI_abstract.pkl")
CKIP_WIKI_keyword_NER_abstract = ner_to_list(CKIP_WIKI_keyword_WS_abstract,CKIP_WIKI_keyword_POS_abstract,"./NewPklData/NER_CKIP_WIKI_keyword_abstract.pkl")

wash_ws_result(CKIP_WS_abstract,CKIP_POS_abstract,"./NewPklData/washed_WS_CKIP_abstract.pkl","./NewPklData/washed_POS_CKIP_abstract.pkl","temp_abstract1.txt")
wash_ws_result(CKIP_keyword_WS_abstract,CKIP_keyword_POS_abstract,"./NewPklData/washed_WS_CKIP_keyword_abstract.pkl","./NewPklData/washed_POS_CKIP_keyword_abstract.pkl","temp_abstract2.txt")
wash_ws_result(CKIP_WIKI_WS_abstract,CKIP_WIKI_POS_abstract,"./NewPklData/washed_WS_CKIP_WIKI_abstract.pkl","./NewPklData/washed_POS_CKIP_WIKI_abstract.pkl","temp_abstract3.txt")
wash_ws_result(CKIP_WIKI_keyword_WS_abstract,CKIP_WIKI_keyword_POS_abstract,"./NewPklData/washed_WS_CKIP_WIKI_keyword_abstract.pkl","./NewPklData/washed_POS_CKIP_WIKI_keyword_abstract.pkl","temp_abstract4.txt")

print("AB done")
#==========================


CKIP_WS_reference = ws_to_list(raw_reference,"./NewPklData/CKIP_WS_reference.pkl") #完成
CKIP_keyword_WS_reference = ws_to_list(raw_reference,"./NewPklData/CKIP_keyword_WS_reference.pkl",{},keyword_dic) 
CKIP_WIKI_WS_reference = ws_to_list(raw_reference,"./NewPklData/CKIP_WIKI_WS_reference.pkl",WIKI_DIC)
CKIP_WIKI_keyword_WS_reference = ws_to_list(raw_reference,"./NewPklData/CKIP_WIKI_keyword_WS_reference.pkl",WIKI_DIC,keyword_dic)
#write_file
pkl_input.read_to_txt("./NewPklData/CKIP_WS_reference.pkl","./NewPklData/CKIP_WS_reference.txt")
pkl_input.read_to_txt("./NewPklData/CKIP_keyword_WS_reference.pkl","./NewPklData/CKIP_keyword_WS_reference.txt")
pkl_input.read_to_txt("./NewPklData/CKIP_WIKI_WS_reference.pkl","./NewPklData/CKIP_WIKI_WS_reference.txt")
pkl_input.read_to_txt("./NewPklData/CKIP_WIKI_keyword_WS_reference.pkl","./NewPklData/CKIP_WIKI_keyword_WS_reference.txt")
# ws_to_list(raw_reference,"./NewPklData/CKIP_WIKI_n-gram_WS_reference.pkl")
# ws_to_list(raw_reference,"./NewPklData/CKIP_n-gram_WS_reference.pkl")
# ws_to_list(raw_reference,"./NewPklData/CKIP_WIKI_n-gram_WS_reference.pkl")
CKIP_POS_reference = pos_to_list(CKIP_WS_reference,"./NewPklData/POS_CKIP_reference.pkl")
CKIP_keyword_POS_reference = pos_to_list(CKIP_keyword_WS_reference,"./NewPklData/POS_CKIP_keyword_reference.pkl")
CKIP_WIKI_POS_reference = pos_to_list(CKIP_WIKI_WS_reference,"./NewPklData/POS_CKIP_WIKI_reference.pkl")
CKIP_WIKI_keyword_POS_reference = pos_to_list(CKIP_WIKI_keyword_WS_reference,"./NewPklData/POS_CKIP_WIKI_keyword_reference.pkl")

CKIP_NER_reference = ner_to_list(CKIP_WS_reference,CKIP_POS_reference,"./NewPklData/NER_CKIP_reference.pkl")
CKIP_keyword_NER_reference = ner_to_list(CKIP_keyword_WS_reference,CKIP_keyword_POS_reference,"./NewPklData/NER_CKIP_keyword_reference.pkl")
CKIP_WIKI_NER_reference = ner_to_list(CKIP_WIKI_WS_reference,CKIP_WIKI_POS_reference,"./NewPklData/NER_CKIP_WIKI_reference.pkl")
CKIP_WIKI_keyword_NER_reference = ner_to_list(CKIP_WIKI_keyword_WS_reference,CKIP_WIKI_keyword_POS_reference,"./NewPklData/NER_CKIP_WIKI_keyword_reference.pkl")

wash_ws_result(CKIP_WS_reference,CKIP_POS_reference,"./NewPklData/washed_WS_CKIP_reference.pkl","./NewPklData/washed_POS_CKIP_reference.pkl","temp_reference1.txt")
wash_ws_result(CKIP_keyword_WS_reference,CKIP_keyword_POS_reference,"./NewPklData/washed_WS_CKIP_keyword_reference.pkl","./NewPklData/washed_POS_CKIP_keyword_reference.pkl","temp_reference2.txt")
wash_ws_result(CKIP_WIKI_WS_reference,CKIP_WIKI_POS_reference,"./NewPklData/washed_WS_CKIP_WIKI_reference.pkl","./NewPklData/washed_POS_CKIP_WIKI_reference.pkl","temp_reference3.txt")
wash_ws_result(CKIP_WIKI_keyword_WS_reference,CKIP_WIKI_keyword_POS_reference,"./NewPklData/washed_WS_CKIP_WIKI_keyword_reference.pkl","./NewPklData/washed_POS_CKIP_WIKI_keyword_reference.pkl","temp_reference4.txt")
