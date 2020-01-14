import numpy as np
from nltk.tokenize import word_tokenize
import re
import json
from keras.models import Sequential, load_model

from backend.intent_classification.data_cleanup import cleaning, create_tokenizer, encoding_doc, \
    padding_doc, one_hot, word_tokenizer, unique_intent, max_length_cleaned_words

'''
input: filename - string - the name of the file to read the data from
output: intent - dataframe object consisting of the column [Intent], unique_intent - list (set of intents from the dataframe that are unique),
        sentences - dataframe object consisting of the columns [Sentence]
description: reads the data from file, loads into a dataframe then splits the dataframe into 2 dataframes consisting of a column each
             and a list of unique intens
'''

def predictions(text, model):
    clean = re.sub(r'[^ a-z A-Z 0-9]', " ", text)
    test_word = word_tokenize(clean)
    test_word = [w.lower() for w in test_word]
    test_ls = word_tokenizer.texts_to_sequences(test_word)
    # Check for unknown words
    if [] in test_ls:
        test_ls = list(filter(None, test_ls))

    test_ls = np.array(test_ls).reshape(1, len(test_ls))

    x = padding_doc(test_ls, max_length_cleaned_words)

    pred = model.predict_proba(x)
    return pred


def get_final_output(pred, classes):
    predictions = pred[0]
    classes = np.array(classes)
    ids = np.argsort(-predictions)
    classes = classes[ids]
    predictions = -np.sort(-predictions)
    final_dict = {}
    for i in range(pred.shape[1]):
        final_dict[str(classes[i])] = str(predictions[i])
    result = json.dumps(final_dict)
    return result


'''
Call this for prediction output
'''
def get_result(sentence):
    model = load_model("model.h5")
    pred = predictions(sentence, model)
    return get_final_output(pred, unique_intent)


print(get_result("Hi"))