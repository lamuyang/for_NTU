from ckiptagger import data_utils, construct_dictionary, WS, POS, NER
import os
import get_data

name = []
keyword = []
abstract = []
content = []
reference = []
allfields_list = get_data.get_mongodb_row("LINS")
name,keyword,abstract,content,reference = get_data.pre_data(name,keyword,abstract,content,reference,allfields_list)
def ws_save(list,name_of_thelist):
    import pickle
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    ws = WS("./data", disable_cuda=False)

    word_sentence_list = ws(
        list,
        sentence_segmentation = True, # To consider delimiters
        segment_delimiter_set = {",", "。", ":", "?", "!", ";","-","──","》","《","\n"}
    )
    del ws
    print(word_sentence_list)
    final = []
    for i in word_sentence_list:
        final.append(i)
    with open(name_of_thelist, 'wb') as fp:
        pickle.dump(final, fp)
    fp.close()
    return len(final)

ws_save(name,"./Pkl_data/WS_name.pkl")
ws_save(abstract,"./Pkl_data/WS_abstract.pkl")
# ws_save(content)
ws_save(reference,"./Pkl_data/WS_reference.pkl")