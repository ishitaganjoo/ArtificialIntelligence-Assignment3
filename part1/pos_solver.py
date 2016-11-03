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
from time import sleep

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    def __init__(self):
        self.initialProbDict = {}
        self.transitionProbDict = {}
        self.emissionProbDict = {}
        self.countWordsDict = {}
        self.countPosDict = {}
        self.mostPosDict = {}
        self.viterbiStateDict = {}
        self.mostLikelyStateSeqDict = {}
        self.mostLikelyPOSList = []
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):
        return 0

    # Do the training!
    def train(self, data):
        for item in data:
            #if element not in dict, count is 1, else fetch the value and increment the count
            #to do : divide
            #count the observed vars
            tupleWords = item[0]
            tuplePos = item[1]
            #print tupleWords
            for i in range(0,len(tupleWords)):
                if tupleWords[i] not in self.countWordsDict:
                    self.countWordsDict[tupleWords[i]] = 1
                else:
                    self.countWordsDict[tupleWords[i]] = self.countWordsDict[tupleWords[i]] + 1

                if tuplePos[i] not in self.countPosDict:
                    self.countPosDict[tuplePos[i]] = 1
                else:
                    self.countPosDict[tuplePos[i]] = self.countPosDict[tuplePos[i]] + 1

            if item[1][0] not in self.initialProbDict:
                self.initialProbDict[item[1][0]] = 1
            else:
                self.initialProbDict[item[1][0]] = self.initialProbDict[item[1][0]] + 1
            for i in range(0, len(item[1])):
                if i<len(item[1])-1: #else index out of range
                    if (item[1][i],item[1][i+1]) not in self.transitionProbDict:
                        self.transitionProbDict[(item[1][i],item[1][i+1])] = 1
                    else:
                        self.transitionProbDict[(item[1][i],item[1][i+1])] = self.transitionProbDict[(item[1][i],item[1][i+1])] + 1
                    
                if (item[0][i],item[1][i]) not in self.emissionProbDict: # check both elements of the tuple
                    self.emissionProbDict[(item[0][i],item[1][i])] = 1
                else:
                    self.emissionProbDict[(item[0][i],item[1][i])] = self.emissionProbDict[(item[0][i],item[1][i])] + 1

        sumInitialProb = sum(self.initialProbDict.values())
        self.initialProbDict.update({n: float( self.initialProbDict[n])/ float(sumInitialProb)for n in self.initialProbDict.keys()})
        
        listKeysTranstn = self.transitionProbDict.keys()
        for key in listKeysTranstn:
            self.transitionProbDict[key] = float(self.transitionProbDict[key])/float(self.countPosDict[key[0]])
            
        listKeys = self.emissionProbDict.keys()
        for key in listKeys:
            self.emissionProbDict[key] = float(self.emissionProbDict[key])/float(self.countPosDict[key[1]])
        pass

    # Functions for each algorithm.
    #
    def simplified(self, sentence):
        mostPosDict=self.mostPosDict
        for i in range(0,len(sentence)):
            maxprob=0;
            for j in range(0,len(self.countPosDict.keys())):
                dictKey=(sentence[i],self.countPosDict.keys()[j]) #changed to tuple
                if dictKey in self.emissionProbDict.keys():
                    currentprob = float(self.emissionProbDict[dictKey]) * float(self.countPosDict[self.countPosDict.keys()[j]])/float(self.countWordsDict[sentence[i]])+1
                else:
                    currentprob = 1
                if maxprob < currentprob:
                    maxprob = currentprob
                    mostPosDict[sentence[i]] = self.countPosDict.keys()[j]+'@'+str(maxprob-1)

        return [[ [mostPosDict[sentence[i]].split('@')[0] for i in range(len(sentence))]], [ ['%.2f'%(float(mostPosDict[sentence[i]].split('@')[1])) for i in range(len(sentence))], ]]

    def returnMax(self,j,listPOS,emissionProb):
        maxProb = 0
        path = ''
        for i in listPOS:
            if (i,j) not in self.transitionProbDict:
                self.transitionProbDict[(i,j)] = 0.000001
            prob = self.viterbiStateDict[i] * self.transitionProbDict[(i,j)]
            if prob > maxProb:
                maxProb = prob
                path = i
        self.mostLikelyStateSeqDict[j] = maxProb*emissionProb  
        return maxProb
    
    def hmm(self, sentence):
        #print("transition prob dict", self.transitionProbDict)
        self.mostLikelyPOSList = [] #empty it for each sentence
        listPOS = ['adj','adv','adp','conj','det','noun','num','pron','prt','verb','x','.']
        for i in range(0,len(sentence)):
            for j in range(0,len(listPOS)):
                if (sentence[i],listPOS[j]) not in self.emissionProbDict:
                    self.emissionProbDict[(sentence[i],listPOS[j])] = 0.000001
                emissionProb = self.emissionProbDict[(sentence[i],listPOS[j])]
                if i==0:
                    #formula is initialProb*emissionProb
                    self.viterbiStateDict[listPOS[j]] = self.initialProbDict[listPOS[j]]*emissionProb 
                    self.mostLikelyStateSeqDict[listPOS[j]] = self.initialProbDict[listPOS[j]]*emissionProb   
                else:
                    #formula changed
                    maxValue = self.returnMax(listPOS[j],listPOS,emissionProb)
                    self.viterbiStateDict[listPOS[j]] =  maxValue * emissionProb
            #pick the maximum probable POS from the dict
            key, _ = max(self.mostLikelyStateSeqDict.iteritems(), key=lambda x:x[1])
            self.mostLikelyPOSList.append(key)
            self.mostLikelyStateSeqDict = {}
                 
        print("sentence is", sentence)
        time.sleep(3)            
        print("most likely pos is",self.mostLikelyPOSList)            
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

