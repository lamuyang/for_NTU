import pkl_input
name = pkl_input.open_pkl("./NewPklData/CKIP_WIKI_keyword_WS_name.pkl")
abstract = pkl_input.open_pkl("./NewPklData/CKIP_WIKI_keyword_WS_abstract.pkl")
reference = pkl_input.open_pkl("./NewPklData/CKIP_WIKI_keyword_WS_reference.pkl")
def all_count(list):
    list_count = {}
    for i in list:
        for j in i:
            if j not in list_count:
                list_count[j] = 1
            else:
                list_count[j] = list_count[j] +1
    # print(list_count)
    print(sorted(list_count.items(), key=lambda d: d[1],reverse=True) )

def count_by_id(list):
    all_list_count = []
    for i in list:
        list_count = {}
        for j in i:
            if j not in list_count:
                list_count[j] = 1
            else:
                list_count[j] = list_count[j] +1
        all_list_count.append(list_count)
    for i in all_list_count:
        print(sorted(i.items(), key=lambda d: d[1],reverse=True) )
# count_by_id(name)
all_count(reference)
