import pickle,os,sys
import numpy as np
import pkl_input
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer,TfidfVectorizer,CountVectorizer

def get_tf_idf(corpus):
    vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
    tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
    weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
    print(vectorizer.fit_transform(corpus))
    print(vectorizer.fit_transform(corpus).todense())
    
    for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        # print (u"-------這裡輸出第",i,u"類文本的tf-idf權重------")
        tem_tem = []
        for j in range(len(word)):
            if weight[i][j] != 0.0:
                # print(word[j],weight[i][j])
                tem_tem.append([[word[j]],[weight[i][j]]])
def test02(corpus):
    vectorizer=CountVectorizer()  #该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频  
    count=vectorizer.fit_transform(corpus)#将文本转为词频矩阵
    print(vectorizer.vocabulary_)
    word=vectorizer.get_feature_names()#获取词袋模型中的所有词语 
    print(word) 
    print(vectorizer.fit_transform(corpus))
    print(vectorizer.fit_transform(corpus).todense())#显示词频矩阵

    transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值  
    tfidf=transformer.fit_transform(count)#计算tf-idf 
    print(tfidf)
    weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重  
    print(weight)

    for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        print (u"-------這裡輸出第",i,u"類文本的tf-idf權重------")
        tem_tem = []
        for j in range(len(word)):
            if weight[i][j] != 0.0:
                print(word[j],weight[i][j])
                tem_tem.append([[word[j]],[weight[i][j]]])
def get_blank_list(list):
    tem_list = []
    for i in list:
        tem = ""
        for j in i :
            tem = tem + j +" "
        tem_list.append(tem)
    # print("確認長度：",len(tem_list))
    return tem_list
def tfidf(data_list, max_df, min_df):
    tfidf_vectorizer = TfidfVectorizer(norm="l2", max_df=max_df, min_df=min_df)
    # max_df=0.7 表示若單詞在70%的文件裡都出現過，則視為高頻詞，對文件分類無幫助，會剔除這個詞。
    # min_df=2 表示若單詞出現次數過低，只出現2次以下(含)，對文件分類無幫助，會剔除這個詞。
    # max_features=500 進一步過濾辭典大小，會根據TF-IDF權重由高到低排序，取前20000個權重高的單詞構成辭典。

    X_tfidf = tfidf_vectorizer.fit_transform(data_list)
    print(X_tfidf.shape)

    tfidf_array = X_tfidf.toarray()
    # print(tfidf_array.shape)

    tfidf_T_array = X_tfidf.T.toarray()
    # print(tfidf_T_array.shape)

    terms = tfidf_vectorizer.get_feature_names()
    # 得到詞典單詞 (words)，根據索引即可得到每個類別裡權重最高的那些單詞了。
    # print(len(words))
    # https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction
    # https://stackoverflow.com/questions/54745482/what-is-the-difference-between-tfidf-vectorizer-and-tfidf-transformer

    return tfidf_vectorizer, X_tfidf, tfidf_array, tfidf_T_array, terms

WS_name = pkl_input.open_pkl("./Pkl_data/All_WS_name.pkl")
WS_abstract = pkl_input.open_pkl("./Pkl_data/All_WS_abstract.pkl")
WS_reference = pkl_input.open_pkl("./Pkl_data/All_WS_reference.pkl")

# name_vet = get_tf_idf(get_blank_list(WS_name))
# print(name_vet)
# np.save("name_vect",name_vet)

# tfidf_vectorizer, X_tfidf, tfidf_array, tfidf_T_array, terms = tfidf(get_blank_list(WS_name),0.9,2)
# print(tfidf_array)


# from sklearn.feature_extraction.text import TfidfTransformer 
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.feature_extraction.text import CountVectorizer
# import pandas as pd
# import math
# from sklearn.preprocessing import normalize

# d1 = '國家 圖書館 古籍 服務 實務 研究 '
# d2 = '服務 學習 之 反思   圖書 資訊 學系 學生 與 被 服務 單位 觀點 分析 '
# d3 = '歷史學系 大學生 撰寫 課程 論文 之 資訊 行為 研究   以 輔仁 大學 為 例 '

# vectorizer = TfidfVectorizer(sublinear_tf=False, stop_words=None, norm='l2')
# tfidf = vectorizer.fit_transform(get_blank_list(WS_name))
# df_tfidf = pd.DataFrame(tfidf.toarray(),columns=vectorizer.get_feature_names(), index=get_blank_list(WS_name))
# print("TFIDF")
# print(df_tfidf)