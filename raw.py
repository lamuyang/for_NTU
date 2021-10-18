import get_data
import re
name,keyword,abstract,content,reference = [],[],[],[],[]
allfields_list = get_data.get_mongodb_row("LINS")
raw_name,keyword,raw_abstract,raw_content,raw_reference = get_data.pre_data(name,keyword,abstract,content,reference,allfields_list)

temp = raw_reference[2]
# print(temp)
temp = temp.replace('\n','').replace('\r','').replace('，','。')
# print(temp)
temp = temp.split("。")
print(temp)
count = 0
for i in temp:
    count += 1
    if count == 2:
        print(i)
        print("==================")
    if count == 3:
        count = 0
    