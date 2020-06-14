import nltk
import pickle
import re
import numpy as np
import requests
import pandas as pd

nltk.download('stopwords')
from nltk.corpus import stopwords

# Paths for all resources for the bot.
RESOURCE_PATH = {
    'INTENT_RECOGNIZER': 'intent_recognizer.pkl',
    'TAG_CLASSIFIER': 'tag_classifier.pkl',
    'TFIDF_VECTORIZER': 'tfidf_vectorizer.pkl',
    'THREAD_EMBEDDINGS_FOLDER': 'thread_embeddings_by_tags',
    'WORD_EMBEDDINGS': 'word_embeddings.tsv',
}


def text_prepare(text):
    """Performs tokenization and simple preprocessing."""

    replace_by_space_re = re.compile('[/(){}\[\]\|@,;]')
    bad_symbols_re = re.compile('[^0-9a-z #+_]')
    stopwords_set = set(stopwords.words('english'))

    text = text.lower()
    text = replace_by_space_re.sub(' ', text)
    text = bad_symbols_re.sub('', text)
    text = ' '.join([x for x in text.split() if x and x not in stopwords_set])

    return text.strip()


def load_embeddings(embeddings_path):
    """Loads pre-trained word embeddings from tsv file.

    Args:
      embeddings_path - path to the embeddings file.

    Returns:
      embeddings - dict mapping words to vectors;
      embeddings_dim - dimension of the vectors.
    """

    # Hint: you have already implemented a similar routine in the 3rd assignment.
    # Note that here you also need to know the dimension of the loaded embeddings.
    # When you load the embeddings, use numpy.float32 type as dtype

    ########################
    #### YOUR CODE HERE ####
    ########################

    # remove this when you're done
    raise NotImplementedError(
        "Open utils.py and fill with your code. In case of Google Colab, download"
        "(https://github.com/hse-aml/natural-language-processing/blob/master/project/utils.py), "
        "edit locally and upload using '> arrow on the left edge' -> Files -> UPLOAD")


def question_to_vec(question, embeddings, dim):
    """Transforms a string to an embedding by averaging word embeddings."""

    # Hint: you have already implemented exactly this function in the 3rd assignment.

    ########################
    #### YOUR CODE HERE ####
    ########################

    # remove this when you're done
    raise NotImplementedError(
        "Open utils.py and fill with your code. In case of Google Colab, download"
        "(https://github.com/hse-aml/natural-language-processing/blob/master/project/utils.py), "
        "edit locally and upload using '> arrow on the left edge' -> Files -> UPLOAD")


def unpickle_file(filename):
    """Returns the result of unpickling the file content."""
    with open(filename, 'rb') as f:
        return pickle.load(f)

    
def store_recognizer(input_string, store_list, all_store_dict):
    '''
    takes as input an input string and finds the bubble tea store name
    always returns the base form of the name that is in the database
    '''
    
    for store_name in store_list:
        if re.search(store_name, input_string):
            # Find correct form
            for key_string, val_list in all_store_dict.items():
                if store_name in val_list:
                    return key_string
    return None

def get_location(input_string):
    output = re.findall("[0-9][0-9][0-9][0-9][0-9][0-9]",input_string)
    if len(output) > 0:
        return output[0]
    else:
        return None
    
    
def get_coords(input_postal):
    response = requests.get('https://developers.onemap.sg/commonapi/search',
                            params={'searchVal':input_postal,
                                   'returnGeom':'Y',
                                   'getAddrDetails':'N'},
                            verify=False)

    json_response = response.json()
    
    if (json_response['found'] >= 1) and (response.status_code==200):
        x_coord = float(json_response['results'][0]['X'])
        y_coord = float(json_response['results'][0]['Y'])

    else:
        x_coord = 30554.79254
        y_coord = 36683.05713
    
    return x_coord, y_coord


def calc_euclidean(coord1, coord2):
    return np.linalg.norm(np.array(coord1) - np.array(coord2), ord=2)


def calc_fastest_time(input_postal, brand, bbt_locations):
    try:
        x_coord, y_coord = get_coords(input_postal)
        #def get_nearest(input_postal, brand, bbt_locations):
        subframe = bbt_locations[bbt_locations['Brand'] == brand]
        dist_list_x = subframe['X'].values.tolist()
        dist_list_y = subframe['Y'].values.tolist()
        euclidean_list = []
        for candx,candy in zip(dist_list_x, dist_list_y):
            euclidean_list.append(calc_euclidean([x_coord, y_coord], [candx, candy]))

        subframe['distance'] = euclidean_list
        subframe.sort_values('distance', inplace=True)
        best_place = subframe.iloc[0]
        best_dist = best_place['distance']
        best_add = best_place['Location_Address']
        time_taken = best_dist/120.4
    
        return time_taken, best_add
    except:
        return 5, '10 Nanyang Green'