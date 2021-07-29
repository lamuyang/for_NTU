import pkl_input
def write_dif(raw_object,WIKI_object,file_name):
    with open(file_name,"w") as file:
        for i in range(0,len(raw_object)):
            if raw_object[i] != WIKI_object[i]:
                file.write(f"No.{i},{len(raw_object[i])},{len(WIKI_object[i])}"+"\n")
                file.write(str(raw_object[i])+"\n")
                file.write(str(WIKI_object[i])+"\n")
                file.write("\n")
raw_name = pkl_input.open_pkl("./Pkl_data/WS_name.pkl")
WIKI_name = pkl_input.open_pkl("./Pkl_data/WIKI_WS_name.pkl")

raw_abstract = pkl_input.open_pkl("./Pkl_data/WS_abstract.pkl")
WIKI_abstract = pkl_input.open_pkl("./Pkl_data/WIKI_WS_abstract.pkl")

raw_reference = pkl_input.open_pkl("./Pkl_data/WS_reference.pkl")
WIKI_reference = pkl_input.open_pkl("./Pkl_data/WIKI_WS_reference.pkl")

write_dif(raw_name,WIKI_name,"./dif/name_dif")
write_dif(raw_abstract,WIKI_abstract,"./dif/abstract_dif")
write_dif(raw_reference,WIKI_reference,"./dif/reference_dif")
