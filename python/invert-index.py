full_text="""
Answers to a query may not all be relevant to the information need
A document is relevant if it is one that the user perceives as containing information of value with respect to their information need 
How good are the returned answers
"""
docs = full_text.split('\n')
my_dict = dict()
for doc in docs:
    for word in doc.split():
        my_dict[word.lower()] =[]
for i in range(len(docs)):
    for word in docs[i].split():
        my_dict[word.lower()].append(i)
for key in sorted(my_dict.keys()): 
    print("{}:{}".format(key,my_dict[key]))
