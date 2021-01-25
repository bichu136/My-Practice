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
    # nltk.download("punkt")
class HyperParams:
    pass       
    

def preprocess_text(text):
    processed_text = text.lower()
    processed_text = processed_text.replace("’", "'")
    processed_text = processed_text.replace("“", '"')
    processed_text = processed_text.replace("”", '"')

    non_words = re.compile(r"[^A-Za-z']+")
    processed_text = re.sub(non_words, ' ', processed_text)

    return processed_text
def n_gram(str,n):
    return [str[i:i+n] for i in range(len(str)-(n-1))]

def get_token_from_str(str):
    processed_str = preprocess_text(str)

    tokens = n_gram(processed_str,5)
    return tokens

def get_text_from_file(filename):
    with open(filename, encoding='cp1252', mode='r') as f:
        text = f.read()
    f.close()
    return text
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
    # text = StemSentence(text)
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
    arr_file = []
    id = 0
    for doc_file in os.listdir(docs_path):
        arr_file.append(doc_file.split('.')[0])
        filename = os.path.join(docs_path, doc_file)
        text = get_text_from_file(filename)
        words = get_token_from_str(text)

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

    return arr, arr_file


def calc_tf_idf(count, num_doc, tf):
    return math.log(tf * (1 + math.log2(count / num_doc)))
    # return math.log(-(tf * (1 + math.log2(count / num_doc))))


def convert_tf_idf_arr(arr):
    for keys, values in arr.items():
        arr[keys]['index'] = [
            [
                item[0],
                calc_tf_idf(values['count'], values['num_doc'], item[1])
            ] for item in values['index']
        ]
    return arr


def get_vector_length_of_docs(tf_idf_index):
    docs_length = dict()
    for key, values in tf_idf_index.items():
        for value in values['index']:
            if value[0] not in docs_length.keys():
                docs_length[value[0]] = math.pow(value[1], 2)
            else:
                docs_length[value[0]] += math.pow(value[1], 2)
    for key in docs_length.keys():
        docs_length[key] = math.sqrt(docs_length[key])
    return docs_length


def get_data_train():
    try:
        pkl_file = open('./input/data/inverted.pickle', 'rb')
        tf_idf_index = pickle.load(pkl_file)
        docs_length = pickle.load(pkl_file)
        pkl_file.close()

        pkl_file = open('./input/data/index.pickle', 'rb')
        arr_file = pickle.load(pkl_file)
        pkl_file.close()

    except:
        docs_path = "./input/Cranfield"
        arr, arr_file = build_inverted_index(docs_path)
        tf_idf_index = convert_tf_idf_arr(arr)
        docs_length = get_vector_length_of_docs(tf_idf_index)

        with open(os.path.join('input', 'data', 'inverted.pickle'), mode='wb') as f:
            pickle.dump(tf_idf_index, f)
            pickle.dump(docs_length, f)
        f.close()

        with open(os.path.join('input', 'data', 'index.pickle'), mode='wb') as f:
            pickle.dump(arr_file, f)
        f.close()

    return tf_idf_index, docs_length, arr_file

def relevant_between_words_cosine(tf_idf_index,tf_idf_for_querry,q_word_with_count,docs_length):
    # nhân query vô index
    relevant_between_words = {
        word: [[
            item[0],
            item[1] * tf_idf_for_querry[word]
        ] for item in tf_idf_index[word]['index']
        ]
        for word in q_word_with_count.keys()
        if word in tf_idf_index.keys()
    }
    # find q length
    q_length = 0
    for key, value in tf_idf_for_querry.items():
        q_length += math.pow(value, 2)
    q_length = math.sqrt(q_length)

    # cộng các document có ở trên
    q_score = dict()
    for _, value in relevant_between_words.items():
        for i in value:
            if i[0] not in q_score.keys():
                q_score[i[0]] = i[1]
            else:
                q_score[i[0]] += i[1]
    for key in q_score.keys():
        q_score[key] = 1 - (q_score[key] / (docs_length[key] * (q_length + 0.01)))**2
    
    return q_score

def relevant_between_words_manhattan(tf_idf_index,tf_idf_for_querry,q_word_with_count,docs_length):
    # nhân query vô index
    relevant_between_words = {
        word: [[
            item[0],
            math.sqrt((item[1] - tf_idf_for_querry[word])**2)
        ] for item in tf_idf_index[word]['index']
        ]
        for word in q_word_with_count.keys()
        if word in tf_idf_index.keys()
    }
    # cộng các document có ở trên
    q_score = dict()
    for _, value in relevant_between_words.items():
        for i in value:
            if i[0] not in q_score.keys():
                q_score[i[0]] = i[1]
            else:
                q_score[i[0]] += i[1]
    return q_score
def relevant_between_words_euclidean(tf_idf_index,tf_idf_for_querry,q_word_with_count,docs_length):
    # nhân query vô index
    relevant_between_words = {
        word: [[
            item[0],
            (item[1] - tf_idf_for_querry[word])**2
        ] for item in tf_idf_index[word]['index']
        ]
        for word in q_word_with_count.keys()
        if word in tf_idf_index.keys()
    }
    # cộng các document có ở trên
    q_score = dict()
    for _, value in relevant_between_words.items():
        for i in value:
            if i[0] not in q_score.keys():
                q_score[i[0]] = i[1]
            else:
                q_score[i[0]] += i[1]
    for key in q_score.keys():
        q_score[key] = math.sqrt(q_score[key])
    return q_score
def get_relevant_ranking_for_query(query, tf_idf_index, docs_length, arr_file):
    # lấy từ trong query
    
    q_words = get_token_from_str(query)
    # đếm từ
    q_word_with_count = dict()
    for word in q_words:
        if word not in q_word_with_count.keys():
            q_word_with_count[word] = 1
        else:
            q_word_with_count[word] += 1

    # tính tf_idf cho các từ trong query
    tf_idf_for_querry = {
        word: calc_tf_idf(
            tf_idf_index[word]['count'],
            tf_idf_index[word]['num_doc'],
            q_word_with_count[word]
        )
        for word in q_word_with_count.keys()
        if word in tf_idf_index.keys()
    }

    q_score = relevant_between_words_cosine(tf_idf_index,tf_idf_for_querry,q_word_with_count,docs_length)

    # a = sorted(q_score.items(), key=lambda item: item[1], reverse=True)
    print(len(q_score))
    q_score_linked_with_files = {
        arr_file[key]: value
        for key, value in q_score.items()
    }
    a = sorted(q_score_linked_with_files.items(),
               key=lambda item: item[1], reverse=False)
    # print('a',a[0],a[1])
    x_retrieved = []
    for i in a:
        x_retrieved.append(i[0])
    return x_retrieved


def open_queries():
    result = dict()
    for i in open("./input/query.txt").readlines():
        t = i.split('\t')
        result[t[0]] = t[1]
    return result


def get_data_ground_truth():
    path = os.path.join('input', 'RES')
    data = dict()

    for file in os.listdir(path):
        filename = os.path.join(path, file)
        text = get_text_from_file(filename)
        text = text.rstrip('\n')
        cutLine = text.split('\n')
        for index, line in enumerate(cutLine):
            # cutTab[1] chua can quan tam toi do chua can dung
            cutTab = line.split('\t')
            cutSpace = cutTab[0].split(" ")
            if cutSpace[0] not in data.keys():
                data[cutSpace[0]] = [cutSpace[1]]
            else:
                data[cutSpace[0]].append(cutSpace[1])
    return data


def get_Average_Precision(x_retrieved, relevant_docs):
    # find R_Precision value
    R_TH = 20
    validation_result = {'R': [], 'P': []}
    c = 0
    # print('r_dóc',relevant_docs)
    if x_retrieved ==[]:
        return 0
    for i in range(len(x_retrieved[:len(relevant_docs)])):
        if x_retrieved[i] in relevant_docs:
            c += 1
        validation_result['R'].append((c / len(relevant_docs)))
        validation_result['P'].append((c / (i + 1)))
    return sum(validation_result['P']) / len(validation_result['P'])

tf_idf_index, docs_length, arr_file = get_data_train()

def validation():
    
    queries = open_queries()
    list_of_x_retrieved = dict()
    for key, value in queries.items():
        list_of_x_retrieved[key] = get_relevant_ranking_for_query(
            value, tf_idf_index, docs_length, arr_file)
    # Bắt đầu đánh giá mô hình.
    data_ground_truth = get_data_ground_truth()

    Average_precision_of_all_x_retrieved = \
        {
            key: get_Average_Precision(value, data_ground_truth[key])
            for key, value in list_of_x_retrieved.items()
        }
    MAP = 0
    for key, value in Average_precision_of_all_x_retrieved.items():
        MAP += value
    MAP = MAP / len(Average_precision_of_all_x_retrieved)
    print("MAP:", MAP)

def Retrieve(query):
    return get_relevant_ranking_for_query(query, tf_idf_index, docs_length, arr_file)
validation()
