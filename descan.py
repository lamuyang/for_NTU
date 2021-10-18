from gensim import models
import pkl_input
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.pipeline import make_pipeline
from pprint import pprint
import logging
from time import time
import numpy as np
import os
from sklearn.cluster import DBSCAN
import pandas as pd
def get_blank_list(list):
    tem_list = []
    for i in list:
        tem = ""
        for j in i :
            tem = tem + j +" "
        tem_list.append(tem)
    # print("確認長度：",len(tem_list))
    return tem_list
def tfidf(data_list, max_df=0.8, min_df=2):
    tfidf_vectorizer = TfidfVectorizer(norm="l2", max_df=max_df, min_df=min_df)
    # max_df=0.7 表示若單詞在70%的文件裡都出現過，則視為高頻詞，對文件分類無幫助，會剔除這個詞。
    # min_df=2 表示若單詞出現次數過低，只出現2次以下(含)，對文件分類無幫助，會剔除這個詞。
    # max_features=500 進一步過濾辭典大小，會根據TF-IDF權重由高到低排序，取前20000個權重高的單詞構成辭典。

    X_tfidf = tfidf_vectorizer.fit_transform(data_list)
    # print(X_tfidf.shape)

    tfidf_array = X_tfidf.toarray()
    # print(tfidf_array.shape)

    tfidf_T_array = X_tfidf.T.toarray()
    # print(tfidf_T_array.shape)

    terms = tfidf_vectorizer.get_feature_names()
    # 得到詞典單詞 (words)，根據索引即可得到每個類別裡權重最高的那些單詞了。
    # print(len(words))
    # https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction
    # https://stackoverflow.com/titleuestions/54745482/what-is-the-difference-between-tfidf-vectorizer-and-tfidf-transformer

    return tfidf_vectorizer, X_tfidf, tfidf_array, tfidf_T_array, terms

def main_fun(main_list,eps = 0.5,min_samples = 5):
    tfidf_vectorizer, X_tfidf, tfidf_array, tfidf_T_array, terms = tfidf(main_list, max_df=0.8, min_df=2)
    dbscan_clf = DBSCAN(eps, min_samples)
    frame = pd.DataFrame(tfidf_array)
    label = dbscan_clf.fit_predict(tfidf_array)
    # print(tfidf_array)
    print(label)

    import matplotlib.pyplot as plt
    plt.rcParams['font.sans-serif']=['Noto Sans CJK TC'] #用来正常显示中文标签
    # plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

    k = 3  # 此处k取 2*2 -1 
    k_dist = select_MinPts(tfidf_array,k)
    k_dist.sort()
    plt.plot(np.arange(k_dist.shape[0]),k_dist[::-1])
    eps = k_dist[::-1][15]
    print(eps)
    # plt.scatter(15,eps,color="r")
    # plt.plot([0,15],[eps,eps],linestyle="--",color = "r")
    # plt.plot([15,15],[0,eps],linestyle="--",color = "r")
    # plt.show()
    # # %matplotlib inline

    # unititleue_labels = set(dbscan_clf.labels_)
    # colors = [plt.cm.Spectral(each)
    #         for each in np.linspace(0, 1, len(unititleue_labels))]
            
    # core_samples_mask = np.zeros_like(dbscan_clf.labels_, dtype=bool)
    # core_samples_mask[dbscan_clf.core_sample_indices_] = True
    # # https://noto-website-2.storage.googleapis.com/pkgs/NotoSansCJKtc-hinted.zip

    # svd = TruncatedSVD(15)
    # normalizer = Normalizer(copy=False)
    # lsa = make_pipeline(svd, normalizer)

    # X = lsa.fit_transform(X_tfidf)

    # for k, col in zip(unititleue_labels, colors):
    #     if k == -1:
    #         col = [0, 0, 0, 1]

    #     class_member_mask = (dbscan_clf.labels_ == k)

    #     xy = X[class_member_mask & core_samples_mask]
    #     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
    #             markeredgecolor='k', markersize=14)

    #     xy = X[class_member_mask & ~core_samples_mask]
    #     plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
    #             markeredgecolor='k', markersize=6)

    # plt.title('大致聚类数: %d' % n_clusters_)
    plt.savefig('py.png')
    # return 100*(n_noise_/237)
    # db = DBSCAN(eps=0.2, min_samples=4).fit(X)


    # labels = db.labels_

    # print(labels)
def select_MinPts(data,k):
    k_dist = []
    for i in range(data.shape[0]):
        dist = (((data[i] - data)**2).sum(axis=1)**0.5)
        dist.sort()
        k_dist.append(dist[k])
    return np.array(k_dist)

def stopword(raw_list):
    new_list = []
    for i in raw_list:
        new_i = []
        for j in i:
            if j not in stop_word:
                new_i.append(j)
        new_list.append(new_i)
    return new_list

stop_word = ["研究","探討","為","例","<<",">>","分析","比較"]
WS_name = get_blank_list(stopword(pkl_input.open_pkl("./NewPklData/washed_WS_CKIP_WIKI_keyword_name.pkl")))
WS_abstract = get_blank_list(stopword(pkl_input.open_pkl("./NewPklData/washed_WS_CKIP_WIKI_keyword_abstract.pkl")))
WS_reference = get_blank_list(stopword(pkl_input.open_pkl("./NewPklData/washed_WS_CKIP_WIKI_keyword_reference.pkl")))


# print(len(stopword(WS_name)))


# main_fun(WS_reference,0.95, 2)

# print(WS_name[0])
# eps = 0.01
# min_samples = 2
# num = 0
# data = []
# for i in range(1000):
#     for j in range(100):
#         print(eps)
#         print(min_samples)
#         print("===========")
#         noise = main_fun(WS_name,eps,min_samples)
#         num +=1
#         temp = [noise],[eps,min_samples]
#         data.append(temp)
#         eps+=0.25
#         if noise == 0.0 or eps > 1:
#             break
#     eps = 0.05
#     min_samples+=0.1
#     if min_samples > 10:
#         break
# for i in data:
#     print(i)



