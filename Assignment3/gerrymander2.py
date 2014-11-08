from sys import maxsize
import itertools
import sys
import numpy as np # for numpy array

# do not edit! added by PythonBreakpoints
from pdb import set_trace as _breakpoint

finalDistricts = list()

class Node:
	############################################################
	# Class for game tree, contains depth, the player number, the
	# current move, the moves remaining, total districts, and the
	# value assigned to that node.
	def __init__(self, i_depth, i_player, i_move, i_movesRemaining, i_totalDistrict, i_value = 0):
		self.i_depth = i_depth
		self.i_player = i_player # 1 player (MAX), -1 player (MIN)
		self.i_move = i_move
		self.i_movesRemaining = i_movesRemaining
		self.i_totalDistrict = i_totalDistrict
		self.i_value = i_value
		self.children = []
		self.DeleteIllegalMoves()
		# self.CreateChildren()

	############################################################
	# Used for the minimax algorithm to get the min and the max
	# of an array of children
	def __cmp__(self, other):
		return cmp(self.i_value, other.i_value)

	############################################################
	# Method for creating children for the game tree.
	# 
	def CreateChildren(self):
		movesRemaining = list()
		moveDictionary = self.i_movesRemaining
		newMoveDictionary = self.DeleteIllegalMoves()
		if self.i_depth >= 0: # how far down the tree you want to calculate 
			if len(newMoveDictionary) > 0: 
				i_value = []
				i_move = []
				newKeys = newMoveDictionary.keys()
				i_children = []
				for i in newKeys:
					i_value.append(i[1])
					i_move.append({i:newMoveDictionary[i]})
				for i in range(0, len(newMoveDictionary)):
					movesRemaining.append(self.i_movesRemaining)
				# print len(newMoveDictionary)
				# print self.i_move
				for i in range(0, len(newMoveDictionary)):
					print movesRemaining[i]
					self.children.append(Node(self.i_depth - 1, -self.i_player, i_move[i], movesRemaining[i], self.i_totalDistrict, i_value[i]))
				# print "my move is:" + str(self.i_move)
		# for child in self.children:
			# print "my child is:" + str(child.i_move)
			# print child.children

	############################################################
	# Method for deleting illegal moves based upon the node's 
	# current move. 
	def DeleteIllegalMoves(self):
		for key in self.i_move:
			moveKey = (key[0], None)
		# DELETING INVALID MOVES
		if moveKey == ('BOT RIGHT', None):
			self.DeleteRightCol()
			self.DeleteBotRows()
			self.DeleteBotRight()
		if moveKey == ('BOT LEFT', None):
			self.DeleteLeftCol()
			self.DeleteBotRows()
			self.DeleteBotLeft()
		if moveKey == ('TOP RIGHT', None):
			self.DeleteRightCol()
			self.DeleteTopRows()
			self.DeleteTopRight()
		if moveKey == ('TOP LEFT', None):
			self.DeleteLeftCol()
			self.DeleteTopRows()
			self.DeleteTopLeft()
		for i in range((self.i_totalDistrict / 2), self.i_totalDistrict):
			if moveKey == ('BOT ROW ' + str(i), None):
				self.DeleteSpecificDistrict('BOT ROW ' + str(i))
				self.DeleteLeftCol()
				self.DeleteRightCol()
				self.DeleteBotLeft()
				self.DeleteBotRight()
			if moveKey == ('RIGHT COL ' + str(i), None):
				self.DeleteSpecificDistrict('RIGHT COL ' + str(i))
				self.DeleteTopRows()
				self.DeleteBotRows()
				self.DeleteTopRight()
				self.DeleteBotRight()
		for i in range(0 , self.i_totalDistrict):
			if moveKey == ('TOP ROW ' + str(i), None):
				self.DeleteSpecificDistrict('TOP ROW ' + str(i))
				self.DeleteLeftCol()
				self.DeleteRightCol()
				self.DeleteTopRight()
				self.DeleteTopLeft()
			if moveKey == ('LEFT COL ' + str(i), None):
				self.DeleteSpecificDistrict('LEFT COL ' + str(i))
				self.DeleteTopRows()
				self.DeleteBotRows()
				self.DeleteTopLeft()
				self.DeleteBotLeft()
		newMoveDictionary = self.i_movesRemaining
		return newMoveDictionary

	def CreateChildrenHelper(self, moveDictionary):
		if (len(moveDictionary) > 0):
			i_value = []
			i_move = []
			i_movesRemaining = []
			newKeys = moveDictionary.keys()
			newMoveDictionary = moveDictionary
			for i in newKeys:
				i_value.append(i[1])
				i_move.append({i:newMoveDictionary[i]})
			for i in range(0, len(i_move)):
				self.children.append(Node(self.i_depth - 1, -self.i_player, i_move[i], moveDictionary, self.i_totalDistrict, i_value[i]))
	
	############################################################
	# Matches on one key, since our dictionary uses a list of two
	# keys, need a method to match only on one.
	def PartialMatch(self, key, d):
	    for k, v in d.iteritems():
	    	# print k
	        if all(k1 == k2 or k2 is None  for k1, k2 in zip(k, key)):
	        	yield k

	############################################################
	# The following functions delete districts from the remaining
	# moves dictionary. These are used to delete invalid districts
	def DeleteSpecificDistrict(self, key):
		deleteKey = list(self.PartialMatch((key, None), self.i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		if not deleteKey:
			return
		else:
			del self.i_movesRemaining[deleteKey]

	def DeleteBotRows(self):
		for i in range((self.i_totalDistrict / 2), self.i_totalDistrict):
			deleteKey = list(self.PartialMatch(('BOT ROW ' + str(i), None), self.i_movesRemaining))
			deleteKey = tuple(itertools.chain(*deleteKey))
			if not deleteKey:
				return
			else:
				del self.i_movesRemaining[deleteKey]

	def DeleteTopRows(self):
		for i in range(0, (self.i_totalDistrict / 2)):
			deleteKey = list(self.PartialMatch(('TOP ROW ' + str(i), None), self.i_movesRemaining))
			deleteKey = tuple(itertools.chain(*deleteKey))
			if not deleteKey:
				return
			else:
				del self.i_movesRemaining[deleteKey]

	def DeleteLeftCol(self):
		for i in range(0, (self.i_totalDistrict / 2)):
			deleteKey = list(self.PartialMatch(('LEFT COL ' + str(i), None), self.i_movesRemaining))
			deleteKey = tuple(itertools.chain(*deleteKey))
			if not deleteKey:
				return
			else:
				del self.i_movesRemaining[deleteKey]

	def DeleteRightCol(self):
		for i in range((self.i_totalDistrict / 2), self.i_totalDistrict):
			deleteKey = list(self.PartialMatch(('RIGHT COL ' + str(i), None), self.i_movesRemaining))
			deleteKey = tuple(itertools.chain(*deleteKey))
			if not deleteKey:
				return
			else:
				del self.i_movesRemaining[deleteKey]

	def DeleteTopLeft(self):
		deleteKey = list(self.PartialMatch(('TOP LEFT', None), self.i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		if not deleteKey:
			return
		else:
			del self.i_movesRemaining[deleteKey]

	def DeleteTopRight(self):
		deleteKey = list(self.PartialMatch(('TOP RIGHT', None), self.i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		if not deleteKey:
			return
		else:
			del self.i_movesRemaining[deleteKey]

	def DeleteBotLeft(self):
		deleteKey = list(self.PartialMatch(('BOT LEFT', None), self.i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		if not deleteKey:
			return
		else:
			del self.i_movesRemaining[deleteKey]

	def DeleteBotRight(self):
		deleteKey = list(self.PartialMatch(('BOT RIGHT', None), self.i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		if not deleteKey:
			return
		else:
			del self.i_movesRemaining[deleteKey]

########################
# Standard main function
def main():
	neighborhoodMatrix = convertToNeighborhoodMatrix(sys.argv[1])
	neighborhoodMatrix = np.asarray(neighborhoodMatrix)
	totalNeighborhoods = len(list(itertools.chain(*neighborhoodMatrix))) # get number of choices
	totalDistricts = len(neighborhoodMatrix)
	print "*"*30
	print "Neighborhood: \n" + str(neighborhoodMatrix)
	
	######### INITIALIZE FIRST MOVE OF GAME TREE #############
	moveDictionary = dict() # dictionary with total moves left
	allMoves = getAllMoves(neighborhoodMatrix, totalDistricts) 
	moveDictionary = allMoves[1] # dictionary with moves (top row/ bot row, left col/ right col)
	init_move = firstMoveDictionary(moveDictionary, totalDistricts) # get first move as a dicitonary
	i_move = init_move[0] # first 
	i_movesRemaining = init_move[1]
	# print i_move
	initialMoveDictionary = DeleteIllegalMoves(i_move, i_movesRemaining, totalDistricts)
	# print initialMoveDictionary
	print "Total Neighborhoods: " + str(totalNeighborhoods)
	print "*"*30 + "\n"
	i_depth = 100 # depth of tree you want to calculate
	i_curPlayer = 1 # max will start
	for key in i_move:
		i_value = key[1]
		i_choice = key[0]
		i_key = key
	max_init_node = Node(i_depth, i_curPlayer, i_move, i_movesRemaining, totalDistricts, i_value)
	# print max_init_node.children
	for child in max_init_node.children:
		print child.i_move
	print "*"*30 + "\n MAX = D \n MIN = R \n" + "*"*30 +"\n"
	
	finalDistricts.append(i_move[i_key])
	print "*"*30
	print "District: " + str(i_choice) + " " + str(i_move[i_key])
	minimaxSearchMod(initialMoveDictionary, -1, totalDistricts)
	print "*"*30
	print "\n"
	finalDecision()


def finalDecision():
	Rdistricts = 0
	Ddistricts = 0
	print "*"*30
	for district in finalDistricts:
		r = 0
		d = 0
		for neighborhood in district:
			if neighborhood == "R":
				r = r + 1
			if neighborhood == "D":
				d = d + 1
		if r > d:
			print "R has won district: " + str(district)
			Rdistricts = Rdistricts + 1
		if r < d:
			print "D has won district: " + str(district)
			Ddistricts = Ddistricts + 1
	print "*"*30
	print "\n"
	print "*"*30
	if Rdistricts > Ddistricts:
		print "Rabbits have won!"
	if Ddistricts > Rdistricts:
		print "Dogs have won!"
	if Rdistricts == Ddistricts:
		print "It's a Tie!"
	print "*"*30

############################################################
# gets all the initial moves for the game and puts it into a dictionary
# returns list of choices as a list and choices as a dictionary.
# This starts the game tree. VALID MOVES: are all rows/columns, and then
# the four corner squares.
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
		choices.append([matrix[0][0], matrix[0][1], matrix[0][2], matrix[0][3], matrix[1][0], matrix[1][1], matrix[1][2], matrix[1][3]]) 
		choiceDictionary["TOP LEFT"] = [matrix[0][0], matrix[0][1], matrix[0][2], matrix[0][3], matrix[1][0], matrix[1][1], matrix[1][2], matrix[1][3]]

		choices.append([matrix[0][-1], matrix[0][-2], matrix[0][-3], matrix[0][-4], matrix[1][-1], matrix[1][-2], matrix[1][-3], matrix[1][-4]])
		choiceDictionary["TOP RIGHT"] = [matrix[0][-1], matrix[0][-2], matrix[0][-3], matrix[0][-4], matrix[1][-1], matrix[1][-2], matrix[1][-3], matrix[1][-4]]

		choices.append([matrix[-1][0], matrix[-2][0], matrix[-3][0], matrix[-4][0], matrix[-1][1], matrix[-1][2], matrix[-1][3], matrix[-1][4]])
		choiceDictionary["BOT LEFT"] = [matrix[-1][0], matrix[-2][0], matrix[-3][0], matrix[-4][0], matrix[-1][1], matrix[-1][2], matrix[-1][3], matrix[-1][4]]

		choices.append([matrix[-1][-1], matrix[-2][-1], matrix[-3][-1], matrix[-4][-1], matrix[-1][-2], matrix[-2][-2], matrix[-3][-2], matrix[-4][-2]])
		choiceDictionary["BOT RIGHT"] = [matrix[-1][-1], matrix[-2][-1], matrix[-3][-1], matrix[-4][-1], matrix[-1][-2], matrix[-2][-2], matrix[-3][-2], matrix[-4][-2]]

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
# the dictionary contains scores for each othe possible choices
#
# THIS IS THE UTILITY FUNCTION. You get 2 pts for all opponent
# district. 1 for majority opponent district. 0 for equal district
# -1 if you group your district, and -2 if district is all yours.
#
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

############################################################
# Template minimax search algorithm
# Used layout of this algorithm to fit the problem, in the modified alg
def minimaxSearch(node, depth, player):
	if (depth == 0):
		return node.i_value
	if (player == 1):
		bestvalue = -3
		for i in range(len(node.children)):
			child = node.children[i]
			i_val = minimaxSearch(child, depth - 1, -1) # drill to bottom of tree, reducing depth, flipping players
			bestvalue = max(bestvalue, i_val)
		return bestvalue
	else:
		bestvalue = 3
		for i in range(len(node.children)):
			child = node.children[i]
			i_val = minimaxSearch(child, depth - 1, 1) # drill to bottom of tree, reducing depth, flipping players
			bestvalue = min(bestvalue, i_val)
		return bestvalue

############################################################
# Modified minimax search algorithm to fit the scope of this
# gerrymandering problem. Looks through children to find mac
# or min depending on the player number. (player 1 is max)
# (player -1 is min)
def minimaxSearchModified(node, depth, player):
	if not node.children:
		return node.i_move
	if (player == 1):
		children = []
		for i in range(len(node.children)):
			children.append(node.children[i])
		bestchoice = max(children)
		minimaxSearchModified(bestchoice, depth - 1, -1)
	if (player == -1):
		children = []
		for i in range(len(node.children)):
			children.append(node.children[i])
		bestchoice = min(children)
		minimaxSearchModified(bestchoice, depth - 1, 1)

def minimaxSearchMod(moveDictionary, player, totalDistricts):
	if not moveDictionary:
		return
	if (player == 1):
		for key in moveDictionary:
			if(key[1] ==  max(k[1] for k, v in moveDictionary.iteritems())):
				bestkey = key
				bestchoice = {bestkey: moveDictionary[bestkey]}
		# print bestchoice
		newMoveDictionary = DeleteIllegalMoves(bestchoice, moveDictionary, totalDistricts)
		# print "\n"
		printMoves(bestchoice)
		minimaxSearchMod(newMoveDictionary, -1, totalDistricts)

	if (player == -1):
		for key in moveDictionary:
			if(key[1] ==  min(k[1] for k, v in moveDictionary.iteritems())):
				bestkey = key
				bestchoice = {bestkey: moveDictionary[bestkey]}
		
		newMoveDictionary = DeleteIllegalMoves(bestchoice, moveDictionary, totalDistricts)
		printMoves(bestchoice)
		# print "\n"
		minimaxSearchMod(newMoveDictionary, 1, totalDistricts)
				# print bestchoice

def printMoves(bestchoice):
	for key in bestchoice:
		i_choice = key[0]
		i_key = key

	print "District: " + str(i_choice) + " " +  str(bestchoice[i_key])
	finalDistricts.append(bestchoice[i_key])

def DeleteIllegalMoves(i_move, moveDictionary, totalDistricts):
		for key in i_move:
			moveKey = (key[0], None)
		# DELETING INVALID MOVES
		if moveKey == ('BOT RIGHT', None):
			DeleteRightCol(moveDictionary, totalDistricts)
			DeleteBotRows(moveDictionary, totalDistricts)
			DeleteBotRight(moveDictionary, totalDistricts)
		if moveKey == ('BOT LEFT', None):
			DeleteLeftCol(moveDictionary, totalDistricts)
			DeleteBotRows(moveDictionary, totalDistricts)
			DeleteBotLeft(moveDictionary, totalDistricts)
		if moveKey == ('TOP RIGHT', None):
			DeleteRightCol(moveDictionary, totalDistricts)
			DeleteTopRows(moveDictionary, totalDistricts)
			DeleteTopRight(moveDictionary, totalDistricts)
		if moveKey == ('TOP LEFT', None):
			DeleteLeftCol(moveDictionary, totalDistricts)
			DeleteTopRows(moveDictionary, totalDistricts)
			DeleteTopLeft(moveDictionary, totalDistricts)
		for i in range((totalDistricts / 2), totalDistricts):
			if moveKey == ('BOT ROW ' + str(i), None):
				DeleteSpecificDistrict(moveDictionary, 'BOT ROW ' + str(i))
				DeleteLeftCol(moveDictionary, totalDistricts)
				DeleteRightCol(moveDictionary, totalDistricts)
				DeleteBotLeft(moveDictionary, totalDistricts)
				DeleteBotRight(moveDictionary, totalDistricts)
			if moveKey == ('RIGHT COL ' + str(i), None):
				DeleteSpecificDistrict(moveDictionary, 'RIGHT COL ' + str(i))
				DeleteTopRows(moveDictionary, totalDistricts)
				DeleteBotRows(moveDictionary, totalDistricts)
				DeleteTopRight(moveDictionary, totalDistricts)
				DeleteBotRight(moveDictionary, totalDistricts)
		for i in range(0 , totalDistricts):
			if moveKey == ('TOP ROW ' + str(i), None):
				DeleteSpecificDistrict(moveDictionary, 'TOP ROW ' + str(i))
				DeleteLeftCol(moveDictionary, totalDistricts)
				DeleteRightCol(moveDictionary, totalDistricts)
				DeleteTopRight(moveDictionary, totalDistricts)
				DeleteTopLeft(moveDictionary, totalDistricts)
			if moveKey == ('LEFT COL ' + str(i), None):
				DeleteSpecificDistrict(moveDictionary, 'LEFT COL ' + str(i))
				DeleteTopRows(moveDictionary, totalDistricts)
				DeleteBotRows(moveDictionary, totalDistricts)
				DeleteTopLeft(moveDictionary, totalDistricts)
				DeleteBotLeft(moveDictionary, totalDistricts)
		newMoveDictionary = moveDictionary
		# print newMoveDictionary
		return newMoveDictionary

def DeleteSpecificDistrict(i_movesRemaining, key):
		deleteKey = list(PartialMatch((key, None), i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		if not deleteKey:
			return
		else:
			del i_movesRemaining[deleteKey]

def DeleteBotRows(i_movesRemaining, i_totalDistrict):
	for i in range((i_totalDistrict / 2), i_totalDistrict):
		deleteKey = list(PartialMatch(('BOT ROW ' + str(i), None), i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		if not deleteKey:
			return
		else:
			del i_movesRemaining[deleteKey]

def DeleteTopRows(i_movesRemaining, i_totalDistrict):
	for i in range(0, (i_totalDistrict / 2)):
		deleteKey = list(PartialMatch(('TOP ROW ' + str(i), None), i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		if not deleteKey:
			return
		else:
			del i_movesRemaining[deleteKey]

def DeleteLeftCol(i_movesRemaining, i_totalDistrict):
	for i in range(0, (i_totalDistrict / 2)):
		deleteKey = list(PartialMatch(('LEFT COL ' + str(i), None), i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		if not deleteKey:
			return
		else:
			del i_movesRemaining[deleteKey]

def DeleteRightCol(i_movesRemaining, i_totalDistrict):
	for i in range((i_totalDistrict / 2), i_totalDistrict):
		deleteKey = list(PartialMatch(('RIGHT COL ' + str(i), None), i_movesRemaining))
		deleteKey = tuple(itertools.chain(*deleteKey))
		if not deleteKey:
			return
		else:
			del i_movesRemaining[deleteKey]

def DeleteTopLeft(i_movesRemaining, i_totalDistrict):
	deleteKey = list(PartialMatch(('TOP LEFT', None), i_movesRemaining))
	deleteKey = tuple(itertools.chain(*deleteKey))
	if not deleteKey:
		return
	else:
		del i_movesRemaining[deleteKey]

def DeleteTopRight(i_movesRemaining, i_totalDistrict):
	deleteKey = list(PartialMatch(('TOP RIGHT', None), i_movesRemaining))
	deleteKey = tuple(itertools.chain(*deleteKey))
	if not deleteKey:
		return
	else:
		del i_movesRemaining[deleteKey]

def DeleteBotLeft(i_movesRemaining, i_totalDistrict):
	deleteKey = list(PartialMatch(('BOT LEFT', None), i_movesRemaining))
	deleteKey = tuple(itertools.chain(*deleteKey))
	if not deleteKey:
		return
	else:
		del i_movesRemaining[deleteKey]

def DeleteBotRight(i_movesRemaining, i_totalDistrict):
	deleteKey = list(PartialMatch(('BOT RIGHT', None), i_movesRemaining))
	deleteKey = tuple(itertools.chain(*deleteKey))
	if not deleteKey:
		return
	else:
		del i_movesRemaining[deleteKey]

def PartialMatch(key, d):
    for k, v in d.iteritems():
    	# print key
    	# print zip(k,key)
        if all(k1 == k2 or k2 is None for k1, k2 in zip(k, key)):
        	# print k
        	yield k



if __name__ == "__main__":
	main()

























