import re,random
from gensim import corpora,models,similarities
import pkl_input,get_data,descan
stop_word = ["研究","探討","為","例","<<",">>","分析","比較","此","各","一些"]
def stopword(raw_list):
    new_list = []
    for i in raw_list:
        new_i = []
        for j in i:
            if j not in stop_word:
                new_i.append(j)
        new_list.append(new_i)
    return new_list
    
name,keyword,abstract,content,reference = [],[],[],[],[]
allfields_list = get_data.get_mongodb_row("LINS")
raw_name,keyword,raw_abstract,raw_content,raw_reference = get_data.pre_data(name,keyword,abstract,content,reference,allfields_list)
new_keyword = []
for i in keyword:
    temp_temp = []
    temp = i.split("、")
    # print(temp)
    new_keyword.append(temp)
# print(new_keyword)

def get_blank_list(list):
    tem_list = []
    for i in list:
        tem = ""
        for j in i :
            tem = tem + j +" "
        tem_list.append(tem)
    # print("確認長度：",len(tem_list))
    return tem_list
WS_name = stopword(pkl_input.open_pkl("./NewPklData/washed_WS_CKIP_WIKI_keyword_name.pkl"))
WS_abstract = stopword(pkl_input.open_pkl("./NewPklData/washed_WS_CKIP_WIKI_keyword_abstract.pkl"))
WS_reference = stopword(pkl_input.open_pkl("./NewPklData/washed_WS_CKIP_WIKI_keyword_reference.pkl"))
WS_conbine = []
for i in range(0,len(WS_name)):
    new_list = []
    new_list.extend(WS_name[i])
    new_list.extend(WS_abstract[i])
    new_list.extend(new_keyword[i])
    WS_conbine.append(new_list)


import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer,TfidfTransformer
class KMeans:
    def cal_dist(self, p0, p1):
        """
        比較兩點的距離
        """
        return np.sqrt(np.sum((p0-p1)**2))
    
    def nearest_cluster_center(self, point, cluster_centers):
        """
        找到距離 point 最近的中心點
        """
        min_dist = float("inf")
        m = cluster_centers.shape[0]
        for i in range(m):
            d = self.cal_dist(point, cluster_centers[i])
            if min_dist > d:
                min_dist = d
        return min_dist 

    def get_centroids(self, datapoints, k):
        """
        K-means++ 演算法，取得初始化中心點
        """
        clusters = np.array([random.choice(datapoints)])
        dist = np.zeros(len(datapoints))
        
        for i in range(k-1):
            sum_dist = 0
            for j, point in enumerate(datapoints):
                dist[j] = self.nearest_cluster_center(point, clusters)
                sum_dist += dist[j]
            
            sum_dist *= random.random()
            for j, d in enumerate(dist):
                sum_dist = sum_dist - d
                if sum_dist <= 0:
                    clusters = np.append(clusters, [datapoints[j]], axis=0)
                    break
        
        return clusters
        
        
    def kmeans_plus_plus(self, datapoints, k=2):
        """
        K-means 演算法
        """
        # 定義資料維度
        d = datapoints.shape[1]
        # 最大的迭代次數
        Max_Iterations = 1000

        cluster = np.zeros(datapoints.shape[0])
        prev_cluster = np.ones(datapoints.shape[0])

        cluster_centers = self.get_centroids(datapoints, k)

        iteration = 0
        while np.array_equal(cluster, prev_cluster) is False or iteration > Max_Iterations:
            iteration += 1
            prev_cluster = cluster.copy()

            # 將每一個點做分群
            for idx, point in enumerate(datapoints):
                min_dist = float("inf")
                for c, cluster_center in enumerate(cluster_centers):
                    dist = self.cal_dist(point, cluster_center)
                    if dist < min_dist:
                        min_dist = dist  
                        cluster[idx] = c   # 指定該點屬於哪個分群

            # 更新分群的中心
            for k in range(len(cluster_centers)):
                new_center = np.zeros(d)
                members = 0
                for point, c in zip(datapoints, cluster):
                    if c == k:
                        new_center += point
                        members += 1
                if members > 0:
                    new_center = new_center / members
                cluster_centers[k] = new_center

        return cluster
WS_conbine = get_blank_list(WS_conbine)
tfidf_vectorizer = TfidfVectorizer()
tfidf = tfidf_vectorizer.fit_transform(WS_conbine)
# print(tfidf)
tfidf = tfidf.toarray()
k = 1
for k in range(1,11):
    Kmeans_cluster = KMeans()
    cluster_result = Kmeans_cluster.kmeans_plus_plus(tfidf, k)
    # print(cluster_result)
    cluster = [[] for _ in range(k)]
    # print(cluster)

    for idx, c in enumerate(cluster_result):
        cluster[int(c)].append(raw_name[idx])

    with open("temp_tot.txt","a") as file:
        for c, result in enumerate(cluster):
            # print('Cluster {}: {}'.format(c, ' '.join(result)))
            file.write('\nCluster {}: {}\n'.format(c, ' ,'.join(result)))
            temp = len(result)
            file.write(f'以上包含{temp}項')
        file.write(f'\n====================\n')



# vectorizer = CountVectorizer()
# transformer = TfidfTransformer()
# tfidf = transformer.fit_transform(vectorizer.fit_transform(WS_conbine))
# bag_of_words = vectorizer.get_feature_names()
# weight = tfidf.toarray()

# news_most_related_words = {}
# for i in range(len(weight)): 
#     w = dict(zip(bag_of_words, weight[i]))
#     w = sorted(w.items(), key=lambda x: x[1], reverse=True)
#     top_10 = []
#     for word, prob in w[:20]:
#         if prob > 0:
#             top_10.append(word)
#     news_most_related_words.update({raw_name[i]: top_10})
# print(type(news_most_related_words))
# with open("top_important_word.txt","w") as file:
#     num = 0
#     for i,j in news_most_related_words.items():
#         file.write(f"No.{num}:{i}, {j}\n")
#         num +=1
#         print(i,j)



