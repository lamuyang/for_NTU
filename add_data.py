import pkl_input,get_data
stop_word = ["研究","探討","為","例","<<",">>","分析","比較","此","各","一些","使得","後來","很多","在於","我國","我們","of","at","它","其"]
def stopword(raw_list):
    new_list = []
    for i in raw_list:
        new_i = []
        for j in i:
            if j not in stop_word:
                new_i.append(j)
        new_list.append(new_i)
    return new_list
def get_blank_list(list):
    tem_list = []
    for i in list:
        tem = ""
        for j in i :
            tem = tem + j +" "
        tem_list.append(tem)
    # print("確認長度：",len(tem_list))
    return tem_list
def main_process():
    name,keyword,abstract,content,reference = [],[],[],[],[]
    allfields_list = get_data.get_mongodb_row("LINS")
    raw_name,keyword,raw_abstract,raw_content,raw_reference = get_data.pre_data(name,keyword,abstract,content,reference,allfields_list)
    new_keyword = []
    for i in keyword:
        temp_temp = []
        temp = i.split("、")
        new_keyword.append(temp)
    WS_name = stopword(pkl_input.open_pkl("./NewPklData/washed_WS_CKIP_WIKI_keyword_name.pkl"))
    WS_abstract = stopword(pkl_input.open_pkl("./NewPklData/washed_WS_CKIP_WIKI_keyword_abstract.pkl"))
    WS_reference = stopword(pkl_input.open_pkl("./NewPklData/washed_WS_CKIP_WIKI_keyword_reference.pkl"))
    return WS_name,WS_abstract,WS_reference,new_keyword

def list_conbine_without_reference():
    WS_conbine = []
    WS_name,WS_abstract,WS_reference,new_keyword = main_process()
    for i in range(0,len(WS_name)):
        new_list = []
        new_list.extend(WS_name[i])
        new_list.extend(WS_abstract[i])
        new_list.extend(new_keyword[i])
        WS_conbine.append(new_list)
    return WS_conbine
def blank_conbine_without_reference():
    WS_conbine = []
    WS_name,WS_abstract,WS_reference,new_keyword = main_process()
    for i in range(0,len(WS_name)):
        new_list = []
        new_list.extend(WS_name[i])
        new_list.extend(WS_abstract[i])
        new_list.extend(new_keyword[i])
        WS_conbine.append(new_list)
    return get_blank_list(WS_conbine)
def list_conbine_with_reference():
    WS_conbine = []
    WS_name,WS_abstract,WS_reference,new_keyword = main_process()
    for i in range(0,len(WS_name)):
        new_list = []
        new_list.extend(WS_name[i])
        new_list.extend(WS_abstract[i])
        new_list.extend(new_keyword[i])
        new_list.extend(WS_reference[i])
        WS_conbine.append(new_list)
    return WS_conbine
def list_conbine_with_reference():
    WS_conbine = []
    WS_name,WS_abstract,WS_reference,new_keyword = main_process()
    for i in range(0,len(WS_name)):
        new_list = []
        new_list.extend(WS_name[i])
        new_list.extend(WS_abstract[i])
        new_list.extend(new_keyword[i])
        new_list.extend(WS_reference[i])
        WS_conbine.append(new_list)
    return get_blank_list(WS_conbine)

