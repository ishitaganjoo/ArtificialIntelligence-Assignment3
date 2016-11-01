###################################
# CS B551 Fall 2016, Assignment #3
#
# Your names and user ids:
#
# (Based on skeleton code by D. Crandall)
#
#
####
# Put your report here!!
####

import random
import math
import time

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):
        return 0

    # Do the training!
    def train(self, data):
        initialProbDict = {}
        transitionProbDict = {}
        emissionProbDict = {}
        countWordsDict = {}
        for item in data:
            #if element not in dict, count is 1, else fetch the value and increment the count
            #to do : divide
            #count the observed vars
            tupleWords = item[0]
            #print tupleWords
            for i in range(0,len(tupleWords)):
                if tupleWords[i] not in countWordsDict:
                    countWordsDict[tupleWords[i]] = 1
                else:
                    countWordsDict[tupleWords[i]] = countWordsDict[tupleWords[i]] + 1   
            #print("dict of words", countWordsDict["transferred"])    
            if item[1][0] not in initialProbDict:
                initialProbDict[item[1][0]] = 1
            else:
                initialProbDict[item[1][0]] = initialProbDict[item[1][0]] + 1    
            for i in range(0, len(item[1])):
                if i<len(item[1])-1: #else index out of range
                    if item[1][i]+item[1][i+1] not in transitionProbDict:
                        transitionProbDict[item[1][i]+item[1][i+1]] = 1
                    else:
                        transitionProbDict[item[1][i]+item[1][i+1]] = transitionProbDict[item[1][i]+item[1][i+1]] + 1
                    
                if item[0][i]+'@'+item[1][i] not in emissionProbDict: # check both elements of the tuple
                    emissionProbDict[item[0][i]+'@'+item[1][i]] = 1
                else:
                    emissionProbDict[item[0][i]+'@'+item[1][i]] = emissionProbDict[item[0][i]+'@'+item[1][i]] + 1
                           
        sumInitialProb = sum(initialProbDict.values())
        initialProbDict.update({n: float( initialProbDict[n])/ float(sumInitialProb)for n in initialProbDict.keys()})
        sumTranstnProb = sum(transitionProbDict.values())
        initialProbDict.update({n: float( transitionProbDict[n])/ float(sumTranstnProb)for n in transitionProbDict.keys()})
        listKeys = emissionProbDict.keys()
        for key in listKeys:
            word  = key.split('@')
            emissionProbDict[key] = float(emissionProbDict[key])/float(countWordsDict[word[0]])
        pass

    # Functions for each algorithm.
    #
    def simplified(self, sentence):
        return [ [ [ "noun" ] * len(sentence)], [[0] * len(sentence),] ]

    def hmm(self, sentence):
        return [ [ [ "noun" ] * len(sentence)], [] ]

    def complex(self, sentence):
        return [ [ [ "noun" ] * len(sentence)], [[0] * len(sentence),] ]


    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It's supposed to return a list with two elements:
    #
    #  - The first element is a list of part-of-speech labelings of the sentence.
    #    Each of these is a list, one part of speech per word of the sentence.
    #
    #  - The second element is a list of probabilities, one per word. This is
    #    only needed for simplified() and complex() and is the marginal probability for each word.
    #
    def solve(self, algo, sentence):
        if algo == "Simplified":
            return self.simplified(sentence)
        elif algo == "HMM":
            return self.hmm(sentence)
        elif algo == "Complex":
            return self.complex(sentence)
        else:
            print "Unknown algo!"

