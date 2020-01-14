import jieba as jieba
from gensim import corpora, models, similarities
import jieba
import pandas as pd
from tabulate import tabulate

# data loading
texts_dataframe = pd.read_csv("../Data/exportDrumLiber.csv")

keyword ='Vreau sa merg la litoralul Mării Negre si as vrea sa vizitez Canalul Dunăre-Marea Neagră'
# keyword= input("Your query:")

texts = [jieba.lcut(str(text[1])) for text in texts_dataframe["LocatieDescriere"].iteritems()]
dictionary = corpora.Dictionary(texts)
feature_cnt = len(dictionary.token2id)
corpus = [dictionary.doc2bow(text) for text in texts]
tfidf = models.TfidfModel(corpus)
kw_vector = dictionary.doc2bow(jieba.lcut(keyword))
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features = feature_cnt)
sim = index[tfidf[kw_vector]]
sim_dict = {}
for i in range(len(sim)):
    sim_dict[i+1]=sim[i]



#print similarities
print("Similarities: ")
for x in sorted(sim_dict, key=sim_dict.get, reverse=True)[:3]:
    print(sim_dict[x], )
#print top 3 locations:
print(sorted(sim_dict, key=sim_dict.get, reverse=True)[:3])
pd.options.display.max_colwidth = 1000
tops = [texts_dataframe.iloc[[number-1]] for number in sorted(sim_dict, key=sim_dict.get, reverse=True)[:3]]
for x in tops:
    touristic_place_name = str(x["LocName"]).split(".")[1].split("Name")[0]
    location=str(x["LocatieLocalitate"]).split("Name")[0][4:]
    description = str(x["LocatieDescriere"]).split("Name")[0][4:]
    print(touristic_place_name, location, description)
