import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
#import mpld3
import matplotlib.pyplot as plt
from textblob import TextBlob
import numpy as np
from yaml import serialize_all 


#ref:https://stackoverflow.com/questions/33587667/extracting-all-nouns-from-a-text-file-using-nltk
#ref:http://brandonrose.org/clustering#Tf-idf-and-document-similarity
#http://www.davidsbatista.net/blog/2018/02/28/TfidfVectorizer/
# load nltk's SnowballStemmer as variabled 'stemmer'

# from nltk.stem.snowball import SnowballStemmer
# stemmer = SnowballStemmer("english") 

# def tokenize_and_stem(text):
#     # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
#     tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
#     filtered_tokens = []
#     # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
#     for token in tokens:
#         if re.search('[a-zA-Z]', token):
#             filtered_tokens.append(token)
#     stems = [stemmer.stem(t) for t in filtered_tokens]
#     #return stems
#     return filtered_tokens

def dummy_fun(doc):
    return doc

#import json file to a dataframe
data_df = pd.read_json('faculty_research_interest.json', orient='split') 

#define vectorizer parameters
#####################################################################
# from sklearn.feature_extraction.text import TfidfVectorizer
# tfidf_vectorizer = TfidfVectorizer(max_df=0.4, max_features=200000,
#                                  min_df=0.0, stop_words='english',
#                                  use_idf=True, tokenizer=dummy_fun, token_pattern=None,
#                                 smooth_idf=True, norm = 'l2')
# #process the content
# for index, row in data_df.iterrows():
#     text_noun_phrases = TextBlob(row['content']).noun_phrases
#     seprated_noun_phrases = [t for term in text_noun_phrases for t in term.split(' ')]
#     text_noun_phrases += seprated_noun_phrases
#     row['content'] = text_noun_phrases
#     data_df['content'].iloc[index] = text_noun_phrases

# tfidf_matrix = tfidf_vectorizer.fit_transform(data_df['content'])
# print(type(tfidf_matrix))
# #save the tfidf_matrix
# import scipy.sparse
# scipy.sparse.save_npz('tfidf_matrix.npz', tfidf_matrix)
#####################################################################
# X = scipy.sparse.load_npz('tfidf_matrix.npz')
# print(X)

#terms = tfidf_vectorizer.get_feature_names()
################################################################
# from sklearn.metrics.pairwise import cosine_similarity
# similarity = cosine_similarity(tfidf_matrix)
################################################################
#print(dist)
#make histogram of the similarity
# dist_list = similarity[:,0]
# n, bins, patches = plt.hist(dist_list, 50, density=True, facecolor='g', alpha=0.75)
# plt.show()
# plt.close()

#################################################################
# clusters = []
# for i in range(similarity.shape[0]):
#     new_cluster = []
#     add_to_new_cluster = True
#     for cluster in clusters:      
#         #if cluster is not '' and []:
#         if similarity[cluster[0],i] > 0.3:
#             cluster.append(i)
#             add_to_new_cluster = False
#     if add_to_new_cluster:
#         new_cluster.append(i)
#         clusters.append(new_cluster)

# for cluster in clusters:
#     if len(cluster) > 1:
#         for i in cluster:
#             print('{}, {}, {}'.format(i,data_df['name'].iloc[i],data_df['affiliation'].iloc[i]))
#         print("\nNext cluster is:\n")
#################################################################



import scipy.sparse
X = scipy.sparse.load_npz('tfidf_matrix.npz')
print(X.shape)
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(X)
#flaten_X = [[x for row in X for x in row]]

#make histogram of the similarity
# dist_list = similarity[:,0]
# for i in range(1,similarity.shape[0]):
#     dist_list = np.concatenate((dist_list, similarity[:,i]))
# print(dist_list.shape)

# n, bins, patches = plt.hist(dist_list, 50, density=True, facecolor='g', alpha=0.75)
# plt.show()
# plt.close()

for i in range(similarity.shape[0]):
    for j in range(i, similarity.shape[0]):
        if similarity[i,j] > 0.9 and similarity[i,j] < 0.98 and data_df['affiliation'].iloc[i] != data_df['affiliation'].iloc[j]:
            print("{},{}\n and\n {},{}\n################################################"
            .format(data_df['name'].iloc[i], data_df['affiliation'].iloc[i], data_df['name'].iloc[j], data_df['affiliation'].iloc[j]))

