import get_data

name,keyword,abstract,content,reference = [],[],[],[],[]
allfields_list = get_data.get_mongodb_row("LINS")
raw_name,keyword,raw_abstract,raw_content,raw_reference = get_data.pre_data(name,keyword,abstract,content,reference,allfields_list)

filter = ["0","1","2","3","4","5","6","7","8","9"]

def get_start_end(list_of_word):
    temp_first = []
    temp_second = []
    for i in range(0,len(list_of_word)):
        if list_of_word[i] == "（"  or list_of_word[i] == "("  :
            temp_first.append(i)
            # print(start)
        if list_of_word[i] == "）" or list_of_word[i] == ")" :
            temp_second.append(i)
                # print(end)
    return temp_first,temp_second

def get_chinese_reference(refernece_list):
    word_list = refernece_list.split("\n")
    fail = []
    chinese_reference_title = []
    web = []
    deweb = []
    raw_final = []
    for i in word_list:
        if i.find("http://") == -1 and i.find("https://") == -1:
            deweb.append(i)
        else:
            web.append(i)
    # print(deweb)
    for i in deweb:
        # print(type(i))
        sentence_list = list(i)
        if sentence_list.count("。") >= 2:
            # print(sentence_list)
            # print(sentence_list.count("。"))
            start_list,end_list = get_start_end(sentence_list)
            # print(f"start = {start_list}")
            # print(f"end = {end_list}")
            try:
                start = start_list[0]
                end = end_list[0]
                if end - start > 5:
                    # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    check = []
                    for d in range(start+1,end):
                        if sentence_list[d] not in filter:
                            check.append(d)
                    end = check[0]
                temp = []
                for j in range(start+1,end):
                    check_year = 0
                    # print(type(sentence_list[j]))
                    if sentence_list[j] not in filter:
                        check_year == 1
                        fail_format = ("".join(sentence_list))
                        fail.append(f"1:{fail_format}")
                    if check_year == 0:
                        for j in range(end-1,len(sentence_list)):
                            if sentence_list[j] == '。':
                                temp.append(j)
                # print(temp)
                temp_title = []
                if len(temp) < 2:
                    # print("fail")
                    fail_format = ("".join(sentence_list))
                    fail.append(f"2:{fail_format}")
                else:
                    for j in range(temp[0]+1,temp[1]):
                        temp_title.append(sentence_list[j])
                    raw_final.append("".join(sentence_list))
                    # print("".join(sentence_list).find("http://"))
                    # print("".join(sentence_list).find("https://"))
                    final = "".join(temp_title)
                    chinese_reference_title.append(final)
            # for i in chinese_reference_title:
            #     print(i)
            except :#IndexError:
                fail_format = ("".join(sentence_list))
                fail.append(f"3:{fail_format}")
        else:
            fail_format = ("".join(sentence_list))
            fail.append(f"4:{fail_format}")
    return chinese_reference_title,raw_final,fail
# !@$#@%^&*(^%$#$&*()*_&(&*^&%$#^%#^@&%*^()%^@#$#%^&*&(*(*^&%^$%#$@#^%&*()(^&%$#@#%^&*(*^%$#@$%^&*()))))
chinese_reference_title = []
tot_fail = []
for i in range(0,len(raw_reference)):
    washed_list,raw_final,fail = get_chinese_reference(raw_reference[i])
    # print("===========================")
    # print(i)
    chinese_reference_title.append(washed_list)
    tot_fail.append(fail)

with open("./washed_title.txt","w") as file:
    count = 1
    for i in chinese_reference_title:
        file.write(f"{count}\n")
        count +=1
        for j in i:
            file.write(j)
            file.write("\n")

        file.write("\n"+"=============================="+"\n")

with open("./fail.txt","w") as file:
    count = 1
    for i in tot_fail:
        file.write(f"{count}\n")
        count +=1
        for j in i:
            if j != "":
                file.write(j)
                file.write("\n")

        file.write("\n"+"=============================="+"\n")



# washed_list,raw_final = get_chinese_reference(raw_reference[44])
# print("===========================")

# for j in range(0,len(washed_list)):
#     print(raw_final[j])
#     print(washed_list[j])
#     print("===========")
# print(len(washed_list))


# print(raw_reference[9])



    # 9 卡卡 21
#  43 ['劉', '詩', '平', '。', '2', '0', '0', '4', '。', '知', '識', '密', '集', '服', '務', '業', '的', '創', '新', '研', '究', '-', '以', '工', '研', '院', '全', '溫', '層', '物', '流', '技', '術', '的', '創', '新', '服', '務', '系', '統', '發', '展', '為', '例', '。', '未', '出', '版', '之', '碩', '士', '論', '文', '，', '國', '立', '政', '治', '大', '學', '科', '技', '管', '理', '研', '究', '所', '碩', '士', '，', '台', '北', '市', '。']
# print(raw_reference[21])