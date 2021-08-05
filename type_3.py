from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import os,re
import get_data,pkl_input

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

def ws_save(list,keyword,name_of_thelist):
    all_dic = {}
    import pickle
    with open("corpus_wikidict_PAGETITLE.pkl", 'rb') as fp:
        WIKI_DIC = pickle.load(fp)
    all_dic.update(WIKI_DIC)
    ngram_add = ["社區總體營造","資訊偶遇","數位典藏","參考服務","書目資源共享","開放原始碼軟體","生物醫學","智慧圖書館","國家圖書館","資訊超載","網路互動工具","連續性資源","繼續教育"]
    keyword_list = []
    for i in keyword:
        if i not in keyword_list:
            keyword_list.append(i)
    for i in ngram_add:
        all_dic[i] = 1
    for i in keyword_list:
        all_dic[i] = 1

    all_dic = construct_dictionary(all_dic)
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    ws = WS("./data", disable_cuda=False)

    word_sentence_list = ws(
        list,
        sentence_segmentation = True, # To consider delimiters
        segment_delimiter_set = {",", "。", ":", "?", "!", ";","-","──","》","《","\n",'民', '年', '月', '頁','日'," "},
        recommend_dictionary = all_dic,
    )
    del ws

    # print(word_sentence_list)
    print("done")

    with open(name_of_thelist, 'wb') as fp:
        pickle.dump(word_sentence_list, fp)
    fp.close()
    for i in range(0,len(name)):
        if name[i] != word_sentence_list[i]:
            print(name[i])
            print(word_sentence_list[i])
            print("==========")
name = []
keyword = []
abstract = []
content = []
reference = []
allfields_list = get_data.get_mongodb_row("LINS")
raw_name,keyword,raw_abstract,raw_content,raw_reference = get_data.pre_data(name,keyword,abstract,content,reference,allfields_list)

new_keyword = []
for i in keyword:
    temp = i.split("、")
    for i in temp:
        new_keyword.append(i)
print(new_keyword)

def pre_process(raw_list):
    new_list = []
    for i in raw_list:
        new_i = ""
        i = remove_punctuation(i)
        i = remove_number(i)
        i = remove_space(i)
        new_i = new_i + i
        new_list.append(new_i)
    # for i in new_list:
    #     print(i)
    return new_list
name = pre_process(raw_name)
ws_save(name,new_keyword,"./Pkl_data/All_WS_name.pkl")
# print(pkl_input.open_pkl("./Pkl_data/WIKI_WS_name.pkl"))

abstract = pre_process(raw_abstract)
ws_save(abstract,new_keyword,"./Pkl_data/All_WS_abstract.pkl")
# print(pkl_input.open_pkl("./Pkl_data/WIKI_WS_abstract.pkl"))

reference = pre_process(raw_reference)
ws_save(reference,new_keyword,"./Pkl_data/All_WS_reference.pkl")
# print(pkl_input.open_pkl("./Pkl_data/WIKI_WS_reference.pkl"))