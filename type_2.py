from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import os,re
import get_data

def remove_punctuation(line):
    rule = re.compile("[^a-zA-Z0-9\\u4e00-\\u9fa5]")
    line = rule.sub(' ',line)
    return line

name = []
keyword = []
abstract = []
content = []
reference = []
allfields_list = get_data.get_mongodb_row("LINS")
name,keyword,abstract,content,reference = get_data.pre_data(name,keyword,abstract,content,reference,allfields_list)
def ws_save(list,name_of_thelist):
    import pickle
    with open("corpus_wikidict_PAGETITLE.pkl", 'rb') as fp:
        WIKI_DIC = pickle.load(fp)
    WIKI_dictionary = construct_dictionary(WIKI_DIC)
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    ws = WS("./data", disable_cuda=False)

    word_sentence_list = ws(
        list,
        sentence_segmentation = True, # To consider delimiters
        segment_delimiter_set = {",", "。", ":", "?", "!", ";","-","──","》","《","\n"},
        recommend_dictionary = WIKI_dictionary,
    )
    del ws
    # print(word_sentence_list)
    final = []
    for i in word_sentence_list:
        new_i = []
        for j in i:
            j = remove_punctuation(j)
            if j != "" and j != " " and j != "\n":
                new_i.append(j)
        final.append(new_i)
    print(final)
    # for i in word_sentence_list:
    #     final.append(i)
    with open(name_of_thelist, 'wb') as fp:
        pickle.dump(final, fp)
    fp.close()
    return len(final)

ws_save(name,"./Pkl_data/WIKI_WS_name.pkl")
ws_save(abstract,"./Pkl_data/WIKI_WS_abstract.pkl")
# ws_save(content)
ws_save(reference,"./Pkl_data/WIKI_WS_reference.pkl")