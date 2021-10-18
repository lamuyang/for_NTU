import pickle
with open("./NewPklData/NER_CKIP_WIKI_keyword_reference.pkl","rb") as fp:
    NER = pickle.load(fp)
with open("./NewPklData/NER_CKIP_WIKI_keyword_name.pkl","rb") as fp:
    NER1 = pickle.load(fp)
with open("./NewPklData/NER_CKIP_WIKI_keyword_abstract.pkl","rb") as fp:
    NER2 = pickle.load(fp)
Type_list = ['DATE',"CARDINAL","TIME","ORDINAL","QUANTITY","PERCENT","GPE","PERSON"]
tot = []
NER_add_list = []
FAC = []
for i in NER:
    for j in i:

        if j[2] == "FAC":
            if j[3] not in FAC:
                FAC.append(j[3])
        if j[2] not in Type_list :
            if j[3] not in tot:
                tot.append(j[2]+":"+j[3])
            if j[3] not in NER_add_list:
                NER_add_list.append(j[3])
print(FAC)
print(len(FAC))
# print(tot)
# Ed
# New Models of Collection Development for the 
#  andCost in the New Knowledge Environment
# 63.編輯部
# 65.編審部
# print(NER_add_list)
# print(len(NER_add_list))
