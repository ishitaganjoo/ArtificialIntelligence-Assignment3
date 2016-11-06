#!/usr/bin/python
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2016
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
from scipy.misc import imsave
from random import randint
import sys


class mountainRidgeFinding:

	def __init__(self, edge_strength, gt_row, gt_col):
		self.edge_strength = edge_strength
		self.gt_row = gt_row
		self.gt_col = gt_col

	def calculateRandomGradient(self):
		firstRandom = randint(0, edge_strength.shape[1]-1)
		
		maxGradient = []
		sample = []
		
		for i in range(0 , len(edge_strength)):
			maxGradient.append(edge_strength[i][firstRandom])
		sample.append(maxGradient.index(max(maxGradient)))
		#print("here",sample)
		return(firstRandom, sample[0])

	def calculateSample(self, xCoord, yCoord):
		#print(xCoord, yCoord)
		sampleList = []
		for i in range(0, xCoord):
			newList = []
			for j in range(0, yCoord):
				jFloat = float(j)
				yCoordFloat = float(yCoord)
				if(j == 0):
					newList.append(edge_strength[j][i] * (0.001))
				else:
					newList.append(edge_strength[j][i]*(jFloat/yCoordFloat))
			sampleList.append(newList.index(max(newList)))
		#print("first", sampleList)
		for i in range(xCoord, edge_strength.shape[1]):
			newList = []
			for j in range(yCoord, edge_strength.shape[0]):
				jFloat = float(j)
				yFloat = float(edge_strength.shape[0])
				if(j == yCoord):
					prob = 0.99
					newList.append(edge_strength[j][i]* prob)
				else:
					newList.append(edge_strength[j][i]*((yFloat - yCoord)/ yFloat))
			sampleList.append(newList.index(max(newList)))
		return sampleList

	def sample2(self):
		sampleList = []
		xCoord = edge_strength.shape[1]
		yCoord = edge_strength.shape[0]
		for i in range(0, xCoord):
			newList = []
			for j in range(0, yCoord):
				if(i == 0):
					newList.append(edge_strength[j][i])
				else:
					lastRow = sampleList[len(sampleList)-1]
					if(lastRow > j):
						distanceFromLastRow = lastRow - j
						newList.append(edge_strength[j][i] * (1.0 / distanceFromLastRow ))
					elif(lastRow == j):
						newList.append(edge_strength[j][i])
					else:
						distanceFromLastRow = j - lastRow
						newList.append(edge_strength[j][i] * (1.0 / distanceFromLastRow))
			sampleList.append(newList.index(max(newList)))
		return sampleList

	def sample3(self):
		#xCoord = edge_strength.shape[1]
		sampleList = []
		yCoord = edge_strength.shape[0]
		finalXCoord = edge_strength.shape[1]
		coordTuple = self.calculateRandomGradient()
		xCoord = coordTuple[0]
		sampleList.insert(0, coordTuple[1])
		for i in range(xCoord-1 , -1, -1):
			newList = []
			gradientSum = 0
			for k in range(0, yCoord):
				gradientSum += edge_strength[k][i]
			for j in range(0, yCoord):
				lastRow = sampleList[0]
				if(lastRow > j):
					distanceFromLastRow = lastRow - j
					newList.append((edge_strength[j][i] / gradientSum) * (1.0 / distanceFromLastRow))
				elif(lastRow == j):
					newList.append(edge_strength[j][i] / gradientSum)
				else:
					distanceFromLastRow = j - lastRow
					newList.append((edge_strength[j][i] / gradientSum) * (1.0 / distanceFromLastRow))
			sampleList.insert(0, newList.index(max(newList)))
		
		for i in range(xCoord+1, finalXCoord):
			newList = []
			gradientSum = 0
			for k in range(0, yCoord):
				gradientSum += edge_strength[k][i]
			for j in range(0, yCoord):
				lastRow = sampleList[len(sampleList)-1]
				if(lastRow > j):
					distanceFromLastRow = lastRow - j
					newList.append((edge_strength[j][i] / gradientSum) * (1.0 / distanceFromLastRow))
				elif(lastRow == j):
					newList.append(edge_strength[j][i] / gradientSum) 
				else:
					distanceFromLastRow = j - lastRow
					newList.append((edge_strength[j][i] / gradientSum) * (1.0 / distanceFromLastRow))
			sampleList.append(newList.index(max(newList)))
		return sampleList

	def sample4(self):
		sampleList = []
		yCoord = int(gt_row)
		xCoord = int(gt_col)
		finalXCoord = edge_strength.shape[1]
		finalYCoord = edge_strength.shape[0]
		sampleList.insert(0, yCoord)
		'''
		for i in range(0, finalXCoord):
			for j in range(yCoord-10, yCoord+10):
				edge_strength[j][i] *= 100'''
		for i in range(xCoord-1, -1, -1):
			newList = []
			gradientSum = 0
			for k in range(0, finalYCoord):
				gradientSum += edge_strength[k][i]
			for j in range(0, finalYCoord):
				lastRow = sampleList[0]
				if(lastRow > j):
					distanceFromLastRow = lastRow - j
					if(distanceFromLastRow > 2):
						newList.append(((edge_strength[j][i] / gradientSum) * 0.01) * (1.0 / distanceFromLastRow))
					else:
						newList.append((edge_strength[j][i] / gradientSum) * (1.0 / distanceFromLastRow))
				elif(lastRow == j):
					newList.append(edge_strength[j][i] / gradientSum)
				else:
					distanceFromLastRow = j - lastRow
					if(distanceFromLastRow > 2):
						newList.append(((edge_strength[j][i] / gradientSum) * 0.01) * (1.0 / distanceFromLastRow))
					else:
						newList.append((edge_strength[j][i] / gradientSum) * (1.0 / distanceFromLastRow))
			sampleList.insert(0, newList.index(max(newList)))
		for i in range(xCoord+1, finalXCoord):
			newList = []
			gradientSum = 0
			for k in range(0, finalYCoord):
				gradientSum += edge_strength[k][i]
			for j in range(0, finalYCoord):
				lastRow = sampleList[len(sampleList) - 1]
				if(lastRow > j):
					distanceFromLastRow = lastRow - j
					if(distanceFromLastRow > 2):
						newList.append(((edge_strength[j][i] / gradientSum) * 0.01) * (1.0 / distanceFromLastRow))
					else:
						newList.append((edge_strength[j][i] / gradientSum) * (1.0 / distanceFromLastRow))
				elif(lastRow == j):
					newList.append(edge_strength[j][i] / gradientSum)
				else:
					distanceFromLastRow = j - lastRow
					if(distanceFromLastRow > 2):
						newList.append(((edge_strength[j][i] / gradientSum) * 0.01) * (1.0 / distanceFromLastRow))
					else:
						newList.append((edge_strength[j][i] / gradientSum) * (1.0 / distanceFromLastRow))
			sampleList.append(newList.index(max(newList)))
		return sampleList
					
				 
		

	def mainClass(self):
		#coordTuple = self.calculateRandomGradient()
		#sampleList = self.calculateSample(coordTuple[0], coordTuple[1])
		'''
		samples = []
		for i in range(0, 500):
			coordTuple = self.calculateRandomGradient()
			samples.append(self.calculateSample(coordTuple[0], coordTuple[1]))'''
		print(edge_strength.shape[0], edge_strength.shape[1])
		listOfSamples = []
		for i in range(0, 1):
			listOfSamples.append(self.sample3())
		samples2 = self.sample2()
		humanSample = self.sample4()
		return (listOfSamples,samples2, humanSample)

# calculate "Edge strength map" of an image
#
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return filtered_y**2

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( max(y-thickness/2, 0), min(y+thickness/2, image.size[1]-1 ) ):
            image.putpixel((x, t), color)
    return image

# main program
#
(input_filename, output_filename, gt_row, gt_col) = sys.argv[1:]

# load in image 
input_image = Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength(input_image)
imsave('edges.jpg', edge_strength)

# You'll need to add code here to figure out the results! For now,
# just create a horizontal centered line.
#ridge = [ edge_strength.shape[0]/2 ] * edge_strength.shape[1]

ridge = []

#print("length1",len(edge_strength[0]))
#print("length",len(edge_strength))
#print("shape", edge_strength.shape)

for i in range(0, len(edge_strength[0])):
	newList = []
	for j in range(0, len(edge_strength)):
		newList.append(edge_strength[j][i])
	ridge.append(newList.index(max(newList)))
'''
newList2 = []
for i in range(0, 1):
	newList = []
	for j in range(0, len(edge_strength)):
		newList.append(edge_strength[j][i])
	newList2.append(newList.index(max(newList)))
	#ridge.append(newList.index(max(newList)))

firstPixel = newList2[0]
print(firstPixel)
ridge.append(firstPixel)
for i in range(1, len(edge_strength[0])):
	newList = []
	for j in range(firstPixel - 125, firstPixel + 125):
		#print(j)
		newList.append(edge_strength[j][i])
	ridge.append(newList.index(max(newList)) + firstPixel-125) 
	

#print(newList2)
#print(ridge)


#print(edge_strength.shape[1])

firstRandom = randint(0,500)

maxGradient = []
sampleList = []

for i in range(0, len(edge_strength)):
	maxGradient.append(edge_strength[i][firstRandom])
sampleList.append(maxGradient.index(max(maxGradient)))

#print(firstRandom)
#print(sampleList)'''


mountain = mountainRidgeFinding(edge_strength, gt_row, gt_col)
sampleList = mountain.mainClass()
#print("sample",len(sampleList[0]))

sampleListOld = sampleList[0]
sampleListNew = sampleList[1]
humanSample = sampleList[2]
#print(sampleListOld)

newRidge2 = []
for i in range(0, len(sampleListOld[0])):
	newDict = {}
	for j in range(0, len(sampleListOld)):
		if(newDict.get(sampleListOld[j][i]) != None):
			value = newDict[sampleListOld[j][i]]
			newDict[sampleListOld[j][i]] = value + 1
		else:
			newDict[sampleListOld[j][i]] = 1
	#print(newDict)
	newRidge2.append(max(newDict, key=(lambda key: newDict[key])))
#print(newRidge2)

# output answer
imsave(output_filename, draw_edge(input_image, ridge, (255, 0, 0), 5))
imsave(output_filename, draw_edge(input_image, newRidge2, (0, 255, 0), 5))
imsave(output_filename, draw_edge(input_image, humanSample, (0, 0, 255), 5))
