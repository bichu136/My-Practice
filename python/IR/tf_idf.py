import nltk
import pickle
import os
import re
import math
import matplotlib.pyplot as plt
import time
try:
    from nltk import sent_tokenize
    from nltk import word_tokenize
    from nltk.probability import FreqDist
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer, SnowballStemmer
except:
    nltk.download("stopwords")
    nltk.download("punkt")

QUERIES_PATH = "./input/TEST/query.txt"
GROUND_TRUTH = "./input/TEST/RES/"
## validation global variable
R_th = 20
def preprocess_text(text):
    processed_text = text.lower()
    processed_text = processed_text.replace("’", "'")
    processed_text = processed_text.replace("“", '"')
    processed_text = processed_text.replace("”", '"')

    non_words = re.compile(r"[^A-Za-z']+")
    processed_text = re.sub(non_words, ' ', processed_text)

    return processed_text

def get_text_from_file(filename):
    with open(filename, encoding='cp1252', mode='r') as f:
        text = f.read()
    f.close()
    return text

# word tokenize + stem English words
def StemSentence(sentence):
    porter = PorterStemmer()
    token_words = word_tokenize(sentence)
    # fd = FreqDist(token_words)
    # fd.plot()
    stem_sentence = []
    for word in token_words:
        stem_sentence.append(porter.stem(word))
        stem_sentence.append(" ")
    return "".join(stem_sentence)

def get_words_from_text(text):
    text = StemSentence(text)
    stop_words = set(stopwords.words('english'))
    processed_text = preprocess_text(text)

    # xóa stopwords
    words = [
        w for w in processed_text.split()
            if w not in stop_words
    ]

    return words

def build_inverted_index(docs_path):
    arr = dict()
    id = 0
    for doc_file in os.listdir(docs_path):
        filename = os.path.join(docs_path, doc_file)
        text = get_text_from_file(filename)
        words = get_words_from_text(text)

        for word in words:
            if word not in arr.keys():
                arr[word] = {'count': 1, 'num_doc': 1, 'index': []}
                arr[word]['index'].append([id, 1])
            else:
                arr[word]['count'] += 1
                if arr[word]['index'][-1][0] == id:
                    arr[word]['index'][-1][1] += 1
                else:
                    arr[word]['index'].append([id, 1])
                    arr[word]['num_doc'] += 1
        id += 1

    return arr

def calc_tf_idf(total_count,num_doc, term_freq_in_doc):
    # return term_freq_in_doc*(1 + math.log2(term_freq_in_doc/total_count))
    return total_count/num_doc  * term_freq_in_doc

def tf_idf_arr(arr):
    tf_idf_arr = dict()
    for keys, values in arr.items():
        arr[keys]['index'] = [
            [
                item[0],
                calc_tf_idf(values['count'], values['num_doc'], item[1])
            ] for item in values['index']
        ]
    docs_length = get_vector_length_of_docs(arr)
    for keys, values in arr.items():
        arr[keys]['index'] = [
            [
                item[0],
                item[1]*docs_length[item[0]]
            ] for item in values['index']
        ]
    return arr
def get_vector_length_of_docs(tf_idf_index):
    docs_length = dict()
    for key,value in tf_idf_index.items():
        for i in value['index']:
            if i[0] not in docs_length.keys():
                docs_length[i[0]] = i[1]*i[1]
            else:
                docs_length[i[0]] += i[1]*i[1]
    for key in docs_length.keys():
        docs_length[key]= math.sqrt(docs_length[key])
    return docs_length
def get_relevant_ranking_for_query(query,tf_idf_index,docs_length,docs_path):
    # lấy từ trong query 
    q_words = get_words_from_text(query)

    # đếm từ 
    q_word_with_count = dict()
    for word in q_words:
            if word not in q_word_with_count.keys():
                q_word_with_count[word] = 1
            else:
                q_word_with_count[word] += 1

    # tính tf_idf cho các từ trong query      
    
    # find q length
    q_length = 0
    
    # nhân query vô index
    tf_idf_for_querry =  {word:calc_tf_idf(tf_idf_index[word]['count'],tf_idf_index[word]['num_doc'],q_word_with_count[word]) for word in q_word_with_count.keys() if word in tf_idf_index.keys() }
    for key,value in tf_idf_for_querry.items():
        q_length += value*value
    q_length = math.sqrt(q_length)
    tf_idf_for_querry =  {word:tf_idf_for_querry[word]/q_length for word in tf_idf_for_querry.keys() if word in tf_idf_index.keys() }
    relevant_between_words = {
            word:[ [item[0],item[1]*tf_idf_for_querry[word]] for item in tf_idf_index[word]['index']]
            for word in q_word_with_count.keys() if word in tf_idf_for_querry.keys()
    }
    # cộng các document có ở trên 
    q_score = dict()
    for _, value in relevant_between_words.items():
        for i in value:
            if i[0] not in q_score.keys():
                q_score[i[0]]=i[1]
            else:
                q_score[i[0]]+=i[1]
    # for key in q_score.keys():
    #     q_score[key] = q_score[key]/(docs_length[key]*(q_length))
    
    a = sorted(q_score.items(), key=lambda item: item[1])
    
    x = [i.split('.')[0] for i in os.listdir(docs_path)]
    # for i in a[:5]:
    #     print(x[i[0]],i[1])
    # for i in a[-5:]:
    #     print(x[i[0]],i[1])
    q_score_linked_with_files = {
        x[key]:value
        for key, value in q_score.items()
    }
    a = sorted(q_score_linked_with_files.items(), key=lambda item: item[1],reverse=True)
    x_retrieved = []
    for i in a[:20]:
        x_retrieved.append(i[0])
    return x_retrieved
def open_queries():
    path = QUERIES_PATH
    result = dict()
    for i in open(path).readlines():
        t = i.split('\t')
        result[t[0]] = t[1]
    return result
def get_R_precision(x_retrieved,q_ids):
    #get the ground truth documents
    y = open(GROUND_TRUTH+q_ids+".txt").readlines()
    relevant_docs = []
    for i in y:
        relevant_docs.append(i.split()[1])
    #find R_Precision value
    validation_result = {'R':[],'P':[]}
    c = 0
    for i in range(R_th):
        if x_retrieved[i] in relevant_docs:
            c+=1
        validation_result['R'].append((c/len(relevant_docs)))
        validation_result['P'].append((c/(i+1)))
    return validation_result['R'][-1], validation_result['P'][-1]
def get_Average_Precision(x_retrieved,q_ids):
    #get the ground truth documents
    y = open(GROUND_TRUTH+q_ids+".txt").readlines()
    relevant_docs = []
    for i in y:
        relevant_docs.append(i.split()[1])
    #find R_Precision value
    validation_result = {'R':[],'P':[]}
    c = 0
    for i in range(R_th):
        if x_retrieved[i] in relevant_docs:
            c+=1
        validation_result['R'].append((c/len(relevant_docs)))
        validation_result['P'].append((c/(i+1)))
    return sum(validation_result['P'])/len(validation_result['P'])
def main():
    docs_path = "./input/Cranfield"
    arr = build_inverted_index(docs_path)
    
    tf_idf_index = tf_idf_arr(arr)
    docs_length = get_vector_length_of_docs(tf_idf_index)
    # for keys, item in tf_idf_index.items():
    #     print(keys, item)

    
    queries = open_queries()
    list_of_x_retrieved = dict()
    for key,value in queries.items():
        list_of_x_retrieved[key] = get_relevant_ranking_for_query(value,tf_idf_index,docs_length,docs_path)
    #Bắt đầu đánh giá mô hình.
    
    Average_precision_of_all_x_retrieved = {
                                        key:get_Average_Precision(value,key) 
                                        for key,value in list_of_x_retrieved.items()
                                    }
    for k,v in Average_precision_of_all_x_retrieved.items():
        print(k,v)
    MAP = 0
    for key, value in Average_precision_of_all_x_retrieved.items():
        MAP+=value
    MAP=MAP/len(Average_precision_of_all_x_retrieved)
    print(MAP)

main()