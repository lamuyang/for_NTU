from pickle import APPEND
import pkl_input
def write_dif(raw_object,WIKI_object,file_name):
    catch_raw = []
    catch_WIKI = []
    with open(file_name,"w") as file:
        for i in range(0,len(raw_object)):
            if raw_object[i] != WIKI_object[i]:
                file.write(f"No.{i},{len(raw_object[i])},{len(WIKI_object[i])}"+"\n")
                file.write(str(raw_object[i])+"\n")
                file.write(str(WIKI_object[i])+"\n")
                catch_raw.append(raw_object[i])
                catch_WIKI.append(WIKI_object[i])
                file.write("\n")
    return catch_raw,catch_WIKI

def catch_dif(raw_list,list_WIKI,file_name,file_name2):
    short_ver = []
    for i in range(0,len(raw_list)):
        tem = []
        for j in raw_list[i]:
            tem.append(j)
        for j in list_WIKI[i]:
            tem.append(j)
        # print(tem)
        tem =set(tem)
        temtem = set(tem)
        for j in raw_list[i]:
            # print(tem)
            if j in tem:
                tem.remove(j)
        for j in list_WIKI[i]:
            # print(temtem)
            if j in temtem:
                temtem.remove(j)
        fin = []
        # print(F"tem:{tem}")
        # print(F"temtem:{temtem}")
        fin.append(list(temtem))
        fin.append(list(tem))
        if temtem != set():
            print(fin)

            with open(file_name,"a") as file:
                file.write(F"{fin}\n")
            for i in fin[1]:
                    if i not in short_ver:
                        short_ver.append(i)
    for i in short_ver:
            with open(file_name2,"a") as file:
                    file.write(F"{i}\n")


raw_name = pkl_input.open_pkl("./Pkl_data/WS_name.pkl")
WIKI_name = pkl_input.open_pkl("./Pkl_data/WIKI_WS_name.pkl")
keyword_name = pkl_input.open_pkl("./Pkl_data/keyword_WS_name.pkl")
ngram_name = pkl_input.open_pkl("./Pkl_data/ngram_WS_name.pkl")
all_name = pkl_input.open_pkl("./Pkl_data/all_WIKI_WS_name.pkl")

raw_abstract = pkl_input.open_pkl("./Pkl_data/WS_abstract.pkl")
WIKI_abstract = pkl_input.open_pkl("./Pkl_data/WIKI_WS_abstract.pkl")
keyword_abstract = pkl_input.open_pkl("./Pkl_data/keyword_WS_abstract.pkl")
ngram_abstract = pkl_input.open_pkl("./Pkl_data/ngram_WS_abstract.pkl")
all_abstract = pkl_input.open_pkl("./Pkl_data/all_WIKI_WS_abstract.pkl")

raw_reference = pkl_input.open_pkl("./Pkl_data/WS_reference.pkl")
WIKI_reference = pkl_input.open_pkl("./Pkl_data/WIKI_WS_reference.pkl")
keyword_reference = pkl_input.open_pkl("./Pkl_data/keyword_WS_reference.pkl")
ngram_reference = pkl_input.open_pkl("./Pkl_data/ngram_WS_reference.pkl")
all_reference = pkl_input.open_pkl("./Pkl_data/all_WIKI_WS_reference.pkl")


name_dif_raw,name_dif_ngram = write_dif(raw_name,ngram_name,"./dif/raw_ngram_name_dif.txt")
catch_dif(name_dif_raw,name_dif_ngram,"./dif/POINT_raw_ngram_name_dif.txt","./dif/short_raw_ngram_name_dif.txt")

abstract_dif_raw,abstract_dif_ngram = write_dif(raw_abstract,ngram_abstract,"./dif/raw_ngram_abstract_dif.txt")
catch_dif(abstract_dif_raw,abstract_dif_ngram,"./dif/POINT_raw_ngram_abstract_dif.txt","./dif/short_raw_ngram_abstract_dif.txt")

reference_dif_raw,reference_dif_ngram = write_dif(raw_reference,ngram_reference,"./dif/raw_ngram_reference_dif.txt")
catch_dif(reference_dif_raw,reference_dif_ngram,"./dif/POINT_raw_ngram_reference_dif.txt","./dif/short_raw_ngram_reference_dif.txt")

print("done")