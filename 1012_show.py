import pkl_input,get_data

name,keyword,abstract,content,reference = [],[],[],[],[]
allfields_list = get_data.get_mongodb_row("LINS")
raw_name,keyword,raw_abstract,raw_content,raw_reference = get_data.pre_data(name,keyword,abstract,content,reference,allfields_list)



name = pkl_input.open_pkl("./NewPklData/final_washed_WS_CKIP_WIKI_Ngram_keyword_name.pkl")
name_pos = pkl_input.open_pkl("./NewPklData/final_washed_POS_CKIP_WIKI_Ngram_keyword_name.pkl")

reference = pkl_input.open_pkl("./NewPklData/final_washed_WS_CKIP_WIKI_Ngram_keyword_reference.pkl")
reference_pos = pkl_input.open_pkl("./NewPklData/final_washed_POS_CKIP_WIKI_Ngram_keyword_reference.pkl")

abstract = pkl_input.open_pkl("./NewPklData/final_washed_WS_CKIP_WIKI_Ngram_keyword_abstract.pkl")
abstract_pos = pkl_input.open_pkl("./NewPklData/final_washed_POS_CKIP_WIKI_Ngram_keyword_abstract.pkl")

with open("./show/name.txt","w") as name_file:
    for i in range(0,len(name)):
        print(raw_name[i])
        name_file.write(raw_name[i]+"\n")
        temp = ""
        for j in range(0,len(name[i])):
            w_p = ""
            w_p += name[i][j]
            w_p += f" ({name_pos[i][j]}), "
            temp+= w_p
        print(temp)
        name_file.write(temp+"\n")
        print("========")
        name_file.write("========"+"\n")

with open("./show/abstract.txt","w") as abstract_file:
    for i in range(0,len(abstract)):
        print(raw_abstract[i])
        abstract_file.write(raw_abstract[i]+"\n")
        temp = ""
        for j in range(0,len(abstract[i])):
            w_p = ""
            w_p += abstract[i][j]
            w_p += f" ({abstract_pos[i][j]}), "
            temp+= w_p
        print(temp)
        abstract_file.write(temp+"\n")
        print("========")
        abstract_file.write("========"+"\n")

with open("./show/reference.txt","w") as reference_file:
    for i in range(0,len(reference)):
        print(raw_reference[i])
        reference_file.write(raw_reference[i]+"\n")
        temp = ""
        for j in range(0,len(reference[i])):
            w_p = ""
            w_p += reference[i][j]
            w_p += f" ({reference_pos[i][j]}), "
            temp+= w_p
        print(temp)
        reference_file.write(temp+"\n")
        print("========")
        reference_file.write("========"+"\n")

