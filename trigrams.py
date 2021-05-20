#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 17:46:23 2020

@author: batman

Comments: Use of Bigrams in Place of trigrams.
"""
import argparse
import os, re
import collections
import math

def preprocess(line):
    # DO NOT CHANGE THIS METHOD unless you are done with bigrams and you are trying to get extra credit

    # get rid of the stuff at the end of the line (spaces, tabs, new line, etc.)
    line = line.rstrip()
    # lower case
    line = line.lower()
    # remove everything except characters and white space
    line = re.sub("[^a-z ]", '', line)
    # tokenized, not done "properly" but sufficient for now
    tokens = line.split()

    # update this when working with trigrams (need '$$')
    # you can also change the preprocessing (keep numbers, do not lower case, etc.)
    tokens = ['$$'+token+'$$' for token in tokens]
    
    return tokens


def create_model(path):
    # This is just some Python magic ...
    # unigrams will return 0 if the key doesn't exist
    unigrams = collections.defaultdict(int)
    # and then you have to figure out what bigrams will return
    bigrams = collections.defaultdict(lambda: collections.defaultdict(int))
    trigrams = collections.defaultdict(lambda: collections.defaultdict(int))
    bigram = collections.defaultdict(lambda: collections.defaultdict(int))
    f = open(path, 'r')
    c1 = ''
    c2 = ''
    tryWithTrigrams = 1
    ## You shouldn't visit a token more than once
    # FIXME Update the counts for unigrams and bigrams
    
    for l in f.readlines():
        tokens = preprocess(l)
        if len(tokens) == 0:
            continue
        for token in tokens:
              if(len(token) > 5):
                    for i in range(len(token)-3):
                          unigrams[token[i]]+=1
                          bigrams[token[i]][token[i+1]]+=1
                          c1 = token[i]
                          c2 = token[i+1]
                          trigrams[c1+c2][token[i+2]]+=1
                    pass
    for k1, v in unigrams.items():
          c1 = k1
          for k2, v2 in unigrams.items():
                c2 = k2
                if(tryWithTrigrams):
                      for k3, v3 in unigrams.items():
                            bigram[c1+c2][k3] = math.log((trigrams[c1+c2][k3] + 1) / (bigrams[c1][c2] + 26))
                else:
                       bigram[k1][k2] = math.log(((bigrams[k1][k2]) +1 / (v + 27)))

   
    return (bigram)


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
              if(len(token)>5):
                    for i in range(len(token)-3):
                          probEng+=model_en[token[i]+token[i+1]][token[i+2]]
                          probSpan+=model_es[token[i]+token[i+1]][token[i+2]]
                    
    if(probEng<probSpan):
        prediction = 'Spanish'
    else:
        prediction = 'English'

    # FIXME Use the model to make predictions.
    # FIXME: Predict whichever language gives you the highest (smoothed log) probability
    # - remember to do exactly the same preprocessing you did when creating the model (that's what it is a method)
    # - you may want to use an additional method to calculate the probablity of a text given a model (and call it twice)

    # prediction should be either 'English' or 'Spanish'
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
