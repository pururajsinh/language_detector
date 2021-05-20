'''
\
data/train/en/all_en.txt \
data/train/es/all_es.txt \
data/test/

 Uncomment line 32-34 and 66 and comment line 28-30 and 63 
 for implementing potter stemmer and linear interpolation.
 
 Line 32-34: Potter Stemmer
 Line 63: add one smoothening
 Line 66: linear interpolation soomthening
'''


import argparse
import os,re
import collections
import math
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

def preprocess(line):

    line = line.rstrip()
    line = line.lower()
    
    line = re.sub("[^a-z ]", '', line)
    tokens = line.split()
    tokens = ['$'+token+'$' for token in tokens]

#    tokens = word_tokenize(line)
#    ps = PorterStemmer()
#    tokens = ['$'+ps.stem(token)+'$' for token in tokens]
    
    return tokens


def create_model(path):
    # This is just some Python magic ...
    # unigrams will return 0 if the key doesn't exist
    unigrams = collections.defaultdict(int)
    # and then you have to figure out what bigrams will return
    bigrams = collections.defaultdict(lambda: collections.defaultdict(int))
    bigramProb = collections.defaultdict(lambda: collections.defaultdict(int))
    _lambda = 0.5
    f = open(path, 'r')
    tokenCount = 0

    for l in f.readlines():
        tokens = preprocess(l)
        tokenCount+=len(tokens)
        if len(tokens) == 0:
            continue
        for token in tokens:
              for i in range(len(token) -2 ):
                    unigrams[token[i]]+=1
                    bigrams[token[i]][token[i+1]]+=1
              pass
    for key, value in unigrams.items():
          for key2, value2 in unigrams.items():
#                add one smoothing
                bigramProb[key][key2] = math.log(((bigrams[key][key2]) +1 / (value + 27)))
                
#                linear interpolation
#                bigramProb[key][key2] = math.log(_lambda * (2 ** ((bigrams[key][key2])/value)) + _lambda * (2 ** ((unigrams[key]/tokenCount))))
    return (bigramProb)


def predict(file, model_en, model_es):
    prediction = None
    probEng = 0
    probSpan = 0
    
    f = open(file, 'r')
    for l in f.readlines():
        tokens = preprocess(l)
        if len(tokens) == 0:
            continue
        for token in tokens:
              for i in range(len(token) - 2):
                    probEng+=model_en[token[i]][token[i+1]]
                    probSpan+=model_es[token[i]][token[i+1]]
                    
    if(probEng<probSpan):
        prediction = 'Spanish'
    else:
        prediction = 'English'
        
    return prediction


def main(en_tr, es_tr, folder_te):
    # DO NOT CHANGE THIS METHOD

    # STEP 1: create a model for English with en_tr
    model_en = create_model(en_tr)

    # STEP 2: create a model for Spanish with es_tr
    model_es = create_model(es_tr)

    # STEP 3: loop through all the files in folder_te and print prediction
    folder = os.path.join(folder_te, "en")
    print("Prediction for English documents in test:")
    for f in os.listdir(folder):
        f_path =  os.path.join(folder, f)
        print(f"{f}\t{predict(f_path, model_en, model_es)}")
    
    folder = os.path.join(folder_te, "es")
    print("\nPrediction for Spanish documents in test:")
    for f in os.listdir(folder):
        f_path =  os.path.join(folder, f)
        print(f"{f}\t{predict(f_path, model_en, model_es)}")


if __name__ == "__main__":
    # DO NOT CHANGE THIS CODE

    parser = argparse.ArgumentParser()
    parser.add_argument("PATH_TR_EN",
                        help="Path to file with English training files")
    parser.add_argument("PATH_TR_ES",
                        help="Path to file with Spanish training files")
    parser.add_argument("PATH_TEST",
                        help="Path to folder with test files")
    args = parser.parse_args()

    main(args.PATH_TR_EN, args.PATH_TR_ES, args.PATH_TEST)
