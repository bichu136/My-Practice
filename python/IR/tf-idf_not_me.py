import nltk
import pickle
import os
import re
import math
import difflib
try:
    from nltk import sent_tokenize
    from nltk import word_tokenize
    from nltk.probability import FreqDist
    from nltk.corpus import stopwords
    from nltk.stem import PorterStemmer, SnowballStemmer
except:
    nltk.download("stopwords")
    nltk.download("punkt")

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
    arr_file = []
    for doc_file in os.listdir(docs_path):
        filename = os.path.join(docs_path, doc_file)
        arr_file.append(filename)
        text = get_text_from_file(filename)
        words = get_words_from_text(text)
        for word in words:
            if word not in arr.keys():
                arr[word] = {'tf': 1, 'num_doc': 1, 'index': []}
                arr[word]['index'].append([id, 1])
            else:
                arr[word]['tf'] += 1
                if arr[word]['index'][-1][0] == id:
                    arr[word]['index'][-1][1] += 1
                else:
                    arr[word]['index'].append([id, 1])
                    arr[word]['num_doc'] += 1
        id += 1
    count_file = id
    return arr, count_file, arr_file

def calc_tf_idf(tf, num_doc, count):
    #return round(count*(1 + math.log2(num_doc)), 2)
    return count*num_doc

def convert_tf_idf_arr(arr, count_file):
    tf_idf = dict()
    for keys, values in arr:
        tf_idf[keys] = [
            [
                item[0],
                calc_tf_idf(values['tf'], count_file*1.0/values['num_doc'], item[1])
            ] for item in values['index']
        ]
    return tf_idf

def convert_tf_idf_to_normalization(tf_idf_arr):
    norm_arr = dict()
    tf_idf_normalization_arr = tf_idf_arr
    for values in tf_idf_arr.values():
        for value in values:
            if value[0] not in norm_arr.keys():
                norm_arr[value[0]] = math.pow(value[1], 2)
            else:
                norm_arr[value[0]] += math.pow(value[1], 2)
    print(norm_arr)
    for key in norm_arr.keys():
        norm_arr[key] = math.sqrt(norm_arr[key])
    for keys, values in tf_idf_normalization_arr.items():
        for i, value in enumerate(values):
            tf_idf_normalization_arr[keys][i][1] /= norm_arr[value[0]]
    return tf_idf_normalization_arr

def get_data_train():
    # try:
    #     pkl_file = open('./input/data/inverted.pickle', 'rb')
    #     norm_arr = pickle.load(pkl_file)
    #     pkl_file = open('./input/data/index.pickle', 'rb')
    #     arr_file = pickle.load(pkl_file)
    # except:
        docs_path = "./input/Cranfield"
        arr, count_file, arr_file = build_inverted_index(docs_path)
        sorted_arr = sorted(arr.items())
        tf_idf_arr = convert_tf_idf_arr(sorted_arr, count_file)

        norm_arr = convert_tf_idf_to_normalization(tf_idf_arr)
        # for keys, values in norm_arr.items():
        #     print(keys, values)

        with open(os.path.join('input', 'data', 'inverted.pickle'), mode='wb') as f:
            pickle.dump(norm_arr, f)
        f.close()
        with open(os.path.join('input', 'data', 'index.pickle'), mode='wb') as f:
            pickle.dump(arr_file, f)

        return norm_arr, arr_file

def convert_query_to_norm(text, dictionary):
    arr = dict()
    words = get_words_from_text(text)
    for word in words:
        if word in dictionary:
            if word not in arr.keys():
                arr[word] = 1
            else:
                arr[word] += 1
    sqr = 0
    for item in arr.keys():
        sqr += arr[item] * arr[item]
    sqrt = math.sqrt(sqr)
    for item in arr.keys():
        arr[item] = arr[item] / sqrt
    return arr

def relevance(norm_train, norm_query):
    arr = dict()
    for key in norm_query.keys():
        arr[key] = [
            [item[0], norm_query[key] * item[1]]
            for item in norm_train.get(key)
        ]

    arr_ans = dict()
    for keys, values in arr.items():
        for value in values:
            if value[0] not in arr_ans.keys():
                arr_ans[value[0]] = value[1]
            else:
                arr_ans[value[0]] += value[1]
    print(arr_ans)
    return arr_ans

def search(query, norm_data):
    norm_query = convert_query_to_norm(query, norm_data.keys())
    q = relevance(norm_data, norm_query)
    q_rankings = sorted(q.items(), key=lambda item: item[1], reverse=True)
    return q_rankings

def get_query_from_file(filename):
    text = get_text_from_file(os.path.join('input', filename))
    text = text.rstrip("\n")
    cutLine = text.split('\n')
    query = dict()
    for index, line in enumerate(cutLine):
        cutTab = line.split('\t')
        query[index] = cutTab
    return query

def get_data_ground_truth():
    path = os.path.join('input', 'RES')
    data = dict()

    for file in os.listdir(path):
        filename = os.path.join(path, file)
        text = get_text_from_file(filename)
        text = text.rstrip('\n')
        cutLine = text.split('\n')
        for index, line in enumerate(cutLine):
            cutTab = line.split('\t') # cutTab[1] chua can quan tam toi do chua can dung
            cutSpace = cutTab[0].split(" ")
            if cutSpace[0] not in data.keys():
                data[cutSpace[0]] = [cutSpace[1]]
            else:
                data[cutSpace[0]].append(cutSpace[1])
    return data

def openQuery():
    file_query = "query.txt"
    queries = get_query_from_file(file_query)
    return queries

def searchByListQueries(norm_data, queries):
    answer = dict()
    for keys, query in queries.items():
        ans = search(query[1], norm_data)
        answer[query[0]] = ans
    return answer

def rebuild_result_after_queries(result_after_search_queries):
    result = dict()
    for keys, values in result_after_search_queries.items():
        for value in values:
            if keys not in result.keys():
                result[keys] = [value[0]]
            else:
                result[keys].append(value[0])
    return result

def get_average_precision(result_i, ground_truth_i):
    result = dict()
    for value in ground_truth_i:
        result[value] = False

    true = 0
    for value_result in result_i:
        try:
            if ground_truth_i.index(str(value_result)) >= 0:
                result[str(value_result)] = True
                true += 1
        except:
            pass

    k = 0
    i = 0
    validation_result = {'R': [], 'P': []}
    for keys, values in result.items():
        i += 1
        if result[keys]:
            k += 1
            validation_result['R'].append(float(k / true))
            validation_result['P'].append(float(k / i))
    try:
        return sum(validation_result['P'])/len(validation_result['P'])
    except:
        return 0

def build_MAP(result_after_search_query, ground_truth):
    result = dict()
    MAP = 0
    for keys, values in ground_truth.items():
        MAP += get_average_precision(result_after_search_query[keys], values)
    return MAP/len(ground_truth)

def main():
    norm_data, arr_file = get_data_train()
    # get index by filename
    # for i in range(len(arr_file)):
    #     if difflib.SequenceMatcher(None, arr_file[i], "./input/Cranfield\\7.txt").ratio() == 1:
    #         print(str(i) + arr_file[i])
    # data_answer = get_data_answer()
    # print(data_answer)

    # kết quả sự thật
    ground_truth = get_data_ground_truth()

    # kết quả sau khi query
    listQueries = openQuery()
    result_after_search_queries = searchByListQueries(norm_data, listQueries)
    # print(result_after_search_queries)
    rebuild_result_after_query = rebuild_result_after_queries(result_after_search_queries)
    # print(rebuild_result_after_query)
    # Đánh giá mô hình
    MAP = build_MAP(rebuild_result_after_query, ground_truth)
    print("MAP: ", str(MAP))
main()