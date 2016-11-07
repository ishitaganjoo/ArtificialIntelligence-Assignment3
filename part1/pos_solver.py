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
from collections import OrderedDict
import collections
import sys

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
        self.probListComplex = []
        self.complexTransitionProb={}
        self.transitDict={}
        self.mostLikelyStateSeqCompDict={}
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling
    def posterior(self, sentence, label):
        '''totalProbPos=sum(self.countPosDict.values())
        p = float(self.countPosDict[label[0]])/float(totalProbPos)
        probEmssnLastWord = self.emissionProbDict[sentence[len(sentence)-1], label[len(label)-1]]
        prob=1
        for i in range(0,len(label)-1):
            #transition prob * emission prob
            prob = prob*self.transitionProbDict[label[i],label[i+1]] * self.emissionProbDict[sentence[i],label[i]]
        prob = prob*p*probEmssnLastWord
        if prob==0:
            prob=1e-80
        return math.log(prob)'''
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
            if sentence[i] not in self.countWordsDict.keys():
                self.countWordsDict[sentence[i]]=1e-80
            for j in self.countPosDict:
                dictKey=(sentence[i],j) #changed to tuple
                if dictKey in self.emissionProbDict.keys():
                    currentprob = float(self.emissionProbDict[dictKey]) * float(self.countPosDict[j])/float(self.countWordsDict[sentence[i]])
                else:
                    currentprob = 1e-80
                if maxprob < currentprob:
                    maxprob = currentprob
                    mostPosDict[sentence[i]] = j+'@'+str(maxprob)

        return [[ [mostPosDict[sentence[i]].split('@')[0] for i in range(len(sentence))]], [ ['%.2f'%(float(mostPosDict[sentence[i]].split('@')[1])) for i in range(len(sentence))], ]]

    
    def hmm(self, sentence):
        
        self.mostLikelyPOSList = [] #empty it for each sentence
        listPOS = ['adj','adv','adp','conj','det','noun','num','pron','prt','verb','x','.']
        for i in range(0,len(sentence)):
            finalSeqDict = {}
            for j in range(0,len(listPOS)):
                
                if i==0:
                    if (sentence[i],listPOS[j]) in self.emissionProbDict:
                        finalSeqDict[listPOS[j]] = [self.initialProbDict[listPOS[j]]*self.emissionProbDict[(sentence[i],listPOS[j])], listPOS[j]] 
                    else:
                        finalSeqDict[listPOS[j]] = [1e-80,listPOS[j]]    
                                
                else:
                    maxProb = 0
                    path = listPOS[j]
                    for k in listPOS:
                        if (k,listPOS[j]) not in self.transitionProbDict:
                            prob = 1e-80
                        else:
                            prob = self.mostLikelyPOSList[i-1][k][0]* self.transitionProbDict[(k,listPOS[j])]    
                        if prob > maxProb and prob!=1e-80:
                            maxProb = prob
                            path = k
                       
                    if maxProb== 0:
                        maxProb =1e-80   
                    if (sentence[i],listPOS[j]) in self.emissionProbDict:
                        finalSeqDict[listPOS[j]] = [maxProb*self.emissionProbDict[(sentence[i],listPOS[j])] , path]
                    else:
                        finalSeqDict[listPOS[j]] = [maxProb* (1e-80), path]    
                    
            self.mostLikelyPOSList.append(finalSeqDict)
            
        #implement BackTracking
        lastDict = self.mostLikelyPOSList[-1]
        maxVal=0
        tag,likelyKey='',''
        for key in lastDict:
            val = lastDict[key][0]
            if lastDict[key][0]>maxVal:
                maxVal = lastDict[key][0]
                tag = lastDict[key][1]
                likelyKey = key
        finalPath = collections.deque()    
        if len(sentence)>1:
            finalPath.appendleft(likelyKey)
            
        finalPath.appendleft(tag)
        
        for i in range(len(sentence)-2,0,-1):
            tag = self.mostLikelyPOSList[i][tag][1]     
            finalPath.appendleft(tag)  
       
        return [ [finalPath], []]

    def returnSum(self,j,listPOS):
        prob = 1e-80
        path = ''
        for i in listPOS:
            if (i,j) not in self.transitionProbDict:
                self.transitionProbDict[(i,j)] = 1e-80
            prob = prob + self.viterbiStateDict[i] * self.transitionProbDict[(i,j)]
            
        return prob
    
    def complex(self, sentence):
        self.mostLikelyPOSList = [] #empty it for each sentence
        self.probListComplex = []
        listPOS = ['adj','adv','adp','conj','det','noun','num','pron','prt','verb','x','.']
        for i in range(0,len(sentence)):
            for j in range(0,len(listPOS)):
                if i==0:
                    if (sentence[i],listPOS[j]) in self.emissionProbDict:
                        
                        self.viterbiStateDict[listPOS[j]] = self.initialProbDict[listPOS[j]]*self.emissionProbDict[(sentence[i],listPOS[j])] 
                    else:
                       
                        self.viterbiStateDict[listPOS[j]] = 1e-80  
                                
                else:
                    #formula changed
                    value = self.returnSum(listPOS[j],listPOS)
                    if (sentence[i],listPOS[j]) not in self.emissionProbDict:
                        self.viterbiStateDict[listPOS[j]] = value * 1e-80
                   
                    else:
                        self.viterbiStateDict[listPOS[j]] =  value * self.emissionProbDict[(sentence[i],listPOS[j])]    
                    
            #pick the maximum probable POS from the dict
            key, prob = max(self.viterbiStateDict.iteritems(), key=lambda x:x[1])
            self.mostLikelyPOSList.append(key)
            self.probListComplex.append(prob)
        print("length of pos list", len(self.mostLikelyPOSList))
        print("length of complex prob list", len(self.probListComplex))    
        return [[self.mostLikelyPOSList], [] ]

       
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

