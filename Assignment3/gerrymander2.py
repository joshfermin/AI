from sys import maxsize
import itertools
import sys
import numpy as np # for numpy array

# do not edit! added by PythonBreakpoints
from pdb import set_trace as _breakpoint


class Node:
	def __init__(self, i_depth, i_player, i_move, i_movesRemaining, i_totalDistrict, i_value = 0):
		self.i_depth = i_depth
		self.i_player = i_player # true player (MAX), false player (MIN)
		self.i_move = i_move
		self.i_movesRemaining = i_movesRemaining
		self.i_totalDistrict = i_totalDistrict
		self.i_value = i_value
		self.children = []
		self.CreateChildren()

	def CreateChildren(self):
		# print self.i_movesRemaining
		# print "\n"
		for key in self.i_move:
			moveKey = (key[0], None)
		if self.i_depth >= 0: # how far down the tree you want to calculate
		# DELETING INVALID MOVES
			if moveKey == ('BOT RIGHT', None):
				self.DeleteRightCol()
				self.DeleteBotRows()
			if moveKey == ('BOT LEFT', None):
				self.DeleteLeftCol()
				self.DeleteBotRow(s)
			if moveKey == ('TOP RIGHT', None):
				self.DeleteRightCol()
				self.DeleteTopRows()
			if moveKey == ('TOP LEFT', None):
				self.DeleteLeftCol()
				self.DeleteTopRows()
			for i in range((self.i_totalDistrict / 2), self.i_totalDistrict):
				if moveKey == ('TOP ROW ' + str(i), None):
					self.DeleteSpecificDistrict('TOP ROW ' + str(i))
				if moveKey == ('LEFT COL ' + str(i), None):
					self.DeleteSpecificDistrict('LEFT COL ' + str(i))
			for i in range((self.i_totalDistrict / 2), self.i_totalDistrict):
				if moveKey == ('BOT ROW ' + str(i), None):
					self.DeleteSpecificDistrict('BOT ROW ' + str(i))
				if moveKey == ('RIGHT COL ' + str(i), None):
					self.DeleteSpecificDistrict('RIGHT COL ' + str(i))
		newMoveDictionary = self.Score(self.i_movesRemaining, self.i_player)
		# print newMoveDictionary
		# self.children.append(Node(self.i_depth - 1, -self.i_player, None, newMoveDictionary, self.i_totalDistrict, ))
			# self.children.append(Node(self.i_depth - 1, -self.i_player, v, self.Score))


	def Score(self, movesRemaining, player):
		size = self.i_totalDistrict
		newMoveDictionary = dict()
		scorearray = []
		returnList = []
		score = 0
		for neighborhood in movesRemaining:
			for i in movesRemaining[neighborhood]:
				newMoveDictionary[(neighborhood,score)] = movesRemaining[neighborhood]
		print newMoveDictionary
		# if player == 1:
		# 	for key in newChoiceDictionary:
		# 		if(key[1] ==  max(k[1] for k, v in newChoiceDictionary.iteritems() if v != 0)):
		# 			bestkey = key
		# elif player == -1:
		# 	for key in newChoiceDictionary:
		# 		if(key[1] ==  min(k[1] for k, v in newChoiceDictionary.iteritems() if v != 0)):
		# 			bestkey = key
		# bestchoice = {bestkey: newMoveDictionary[bestkey]}
		# del newMoveDictionary[bestkey]
		# returnList.append(bestchoice)
		# returnList.append(newMoveDictionary)
		return newMoveDictionary

	############################################################
	# Matches on one key, since our dictionary uses a list of two
	# keys, need a method to match only on one.
	def PartialMatch(self, key, d):
	    for k, v in d.iteritems():
	        if all(k1 == k2 or k2 is None  for k1, k2 in zip(k, key)):
	        	yield k

	############################################################
	# The following functions delete districts from the remaining
	# moves dictionary.
	def DeleteSpecificDistrict(self, key):
		deleteKey = list(self.PartialMatch((key, None), self.i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		del self.i_movesRemaining[deleteKey]

	def DeleteBotRows(self):
		for i in range((self.i_totalDistrict / 2), self.i_totalDistrict):
			deleteKey = list(self.PartialMatch(('BOT ROW ' + str(i), None), self.i_movesRemaining))
			deleteKey = tuple(itertools.chain(*deleteKey))
			del self.i_movesRemaining[deleteKey]

	def DeleteTopRows(self):
		for i in range(0, (lengthOfChoice / 2)):
			deleteKey = list(self.PartialMatch(('TOP ROW ' + str(i), None), self.i_movesRemaining))
			deleteKey = tuple(itertools.chain(*deleteKey))
			del self.i_movesRemaining[deleteKey]

	def DeleteLeftCol(self):
		for i in range(0, (lengthOfChoice / 2)):
			deleteKey = list(self.PartialMatch(('LEFT COL ' + str(i), None), self.i_movesRemaining))
			deleteKey = tuple(itertools.chain(*deleteKey))
			del self.i_movesRemaining[deleteKey]

	def DeleteRightCol(self):
		for i in range((self.i_totalDistrict / 2), self.i_totalDistrict):
			deleteKey = list(self.PartialMatch(('RIGHT COL ' + str(i), None), self.i_movesRemaining))
			deleteKey = tuple(itertools.chain(*deleteKey))
			del self.i_movesRemaining[deleteKey]

	def DeleteTopLeft(self):
		deleteKey = list(self.PartialMatch(('TOP LEFT'), None), self.i_movesRemaining)
		deleteKey = tuple(itertools.chain(*deleteKey))
		del self.i_movesRemaining[deleteKey]

	def DeleteTopRight(self):
		deleteKey = list(self.PartialMatch(('TOP RIGHT'), None), self.i_movesRemaining)
		deleteKey = tuple(itertools.chain(*deleteKey))
		del self.i_movesRemaining[deleteKey]

	def DeleteBotLeft(self):
		deleteKey = list(self.PartialMatch(('BOT LEFT'), None), self.i_movesRemaining)
		deleteKey = tuple(itertools.chain(*deleteKey))
		del self.i_movesRemaining[deleteKey]

	def DeleteBotRight(self):
		deleteKey = list(self.PartialMatch(('BOT RIGHT'), None), self.i_movesRemaining)
		deleteKey = tuple(itertools.chain(*deleteKey))
		del self.i_movesRemaining[deleteKey]

############################################################
# Function that is called when user runs this python script
def main():
	neighborhoodMatrix = convertToNeighborhoodMatrix(sys.argv[1])
	neighborhoodMatrix = np.asarray(neighborhoodMatrix)
	totalNeighborhoods = len(list(itertools.chain(*neighborhoodMatrix))) # get number of choices
	totalDistricts = len(neighborhoodMatrix)

	######### INITIALIZE FIRST MOVE OF GAME TREE #############
	moveDictionary = dict() # dictionary with total moves left
	allMoves = getAllMoves(neighborhoodMatrix, totalDistricts) 
	moveDictionary = allMoves[1] # dictionary with moves (top row/ bot row, left col/ right col)
	init_move = firstMoveDictionary(moveDictionary, totalDistricts) # get first move as a dicitonary
	i_move = init_move[0] # first 
	i_movesRemaining = init_move[1]
	print "Total Neighborhoods: " + str(totalNeighborhoods) + "\n" + "Total Districts should be: " + str(totalDistricts)
	i_depth = 4 # depth of tree you want to calculate
	i_curPlayer = 1 # max will start
	for key in i_move:
		i_value = key[1]
	max_init_node = Node(i_depth, i_curPlayer, i_move, i_movesRemaining, totalDistricts, i_value)
	print "*"*30 + "\n MAX = D \n MIN = R \n" + "*"*30

############################################################
# gets all the initial moves for the game and puts it into a dictionary
# returns list of choices as a list and choices as a dictionary.
# matrix = neighborhood matrix
# lengthOfChoice = size of district
def getAllMoves(matrix, lengthOfChoice):
	choices = []
	rowarray = []
	columnarray = []
	leftcol = []
	rightcol = []
	toprow = []
	botrow = []
	choiceDictionary = dict()
	for i in range(len(matrix)): # add all columns/row choices
		column = matrix[:,i].tolist()
		row = matrix[i,:].tolist()
		choices.append(column) # column
		choices.append(row) # row
		columnarray.append(column)
		rowarray.append(row)
	if lengthOfChoice == 4: # for small matrix [4x4]
		# upper left square
		choices.append([matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]]) 
		choiceDictionary["TOP LEFT"] = [matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]]
		# upper right square
		choices.append([matrix[0][-1], matrix[0][-2], matrix[1][-1], matrix[1][-2]])
		choiceDictionary["TOP RIGHT"] = [matrix[0][-1], matrix[0][-2], matrix[1][-1], matrix[1][-2]]
		# bottom left sqare
		choices.append([matrix[-1][0], matrix[-2][0], matrix[-1][1], matrix[-1][2]])
		choiceDictionary["BOT LEFT"] = [matrix[-1][0], matrix[-2][0], matrix[-1][1], matrix[-1][2]]
		# bottom right square
		choices.append([matrix[-1][-1], matrix[-2][-1], matrix[-1][-2], matrix[-2][-2]])
		choiceDictionary["BOT RIGHT"] = [matrix[-1][-1], matrix[-2][-1], matrix[-1][-2], matrix[-2][-2]]
	if lengthOfChoice == 8: # for large neighborhood [8 x 8]
		choices.append([matrix[0][0], matrix[0][1], matrix[0][2], matrix[0][3], matrix[1][0], matrix[1][1]]) 
		choiceDictionary["TOP LEFT"] = [matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]]

	for i in range(0, (lengthOfChoice / 2)):
		choiceDictionary["LEFT COL " + str(i)] = columnarray[i]
		choiceDictionary["TOP ROW " + str(i)] = rowarray[i]
	for i in range((lengthOfChoice / 2), lengthOfChoice):
		rightcol.append(columnarray[i])
		choiceDictionary["RIGHT COL " + str(i)] = columnarray[i]	
		choiceDictionary["BOT ROW " + str(i)] = rowarray[i]
	returnarray = []
	returnarray.append(choices)
	returnarray.append(choiceDictionary)
	return returnarray # returns choices and choice dictionary 

############################################################
# Get the first move to start the game and the game tree 
# returns list of best move and dictionary without best move
# choices = all move dictionary
# lenghthOfChoice = size of a district
def firstMoveDictionary(choices, lengthOfChoice):
	newChoiceDictionary = dict()
	scorearray = []
	returnList = []
	score = 0
	size = lengthOfChoice
	for choice in choices:
		# print choice
		d = 0 
		r = 0
		for i in choices[choice]:
			if i == "D":
				d = d + 1
			if i == "R":
				r = r + 1
		if r == size:
			score = 2
		elif r > (size / 2):
			score = 1
		elif r == d:
			score =0
		elif d > (size / 2):
			score = -1
		elif d == size:
			score = -2
		newChoiceDictionary[(choice,score)] = choices[choice] 
	for key in newChoiceDictionary:
		if(key[1] ==  max(k[1] for k, v in newChoiceDictionary.iteritems() if v != 0)):
			bestkey = key
	bestchoice = {bestkey: newChoiceDictionary[bestkey]}
	del newChoiceDictionary[bestkey]
	returnList.append(bestchoice)
	returnList.append(newChoiceDictionary)
	return returnList

############################################################
# Converts the neighborhood txt file into list that is turned
# into a numpy array in the main function.
# inputtxt = text that contains matrix
def convertToNeighborhoodMatrix(inputtxt):
	Neighborhood = open(inputtxt, 'r')
	neighborhoodMatrix = map(lambda line: line.rstrip('\n'), Neighborhood)
	neighborhoodMatrix = [map(str, line.split(' ')) for line in neighborhoodMatrix]
	return neighborhoodMatrix

def minimaxSearch(node, depth, player):
	if (depth == 0) or (abs(node.i_value == maxsize)):
		return node.i_value
	if (player == 1):
		for i in range(len(node.children)):
			child = node.children[i]
			i_val = minimaxSearch(child, i_depth - 1, -1) # drill to bottom of tree, reducing depth, flipping players
			if(abs(maxsize*i_player - i_val) < abs(maxsize * i_player - bestvalue)): # checking distance from where we want to be to where we are with child, if closer to the goal of +inf or -inf then store vale
				bestvalue = i_val
		return bestvalue
	else:
		bestvalue = maxsize
		for i in range(len(node.children)):
			child = node.children[i]
			i_val = minimaxSearch(child, i_depth - 1, 1) # drill to bottom of tree, reducing depth, flipping players
			if(abs(maxsize*i_player - i_val) < abs(maxsize * i_player - bestvalue)): # checking distance from where we want to be to where we are with child, if closer to the goal of +inf or -inf then store vale
				bestvalue = i_val
		return bestvalue

if __name__ == "__main__":
	main()

























