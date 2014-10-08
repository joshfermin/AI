from sys import maxsize
import itertools
import sys
import numpy as np # for numpy array

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
		print self.i_movesRemaining
		for key in self.i_move:
			moveKey = (key[0], None)
		if self.i_depth >= 0: # how far down the tree you want to calculate
			if moveKey == ('BOT RIGHT', None):
				for i in range((self.i_totalDistrict / 2), self.i_totalDistrict):
					del self.i_movesRemaining['BOT ROW ' + str(i), None]
					del self.i_movesRemaining['LEFT COL ' + str(i), None]
				print self.i_movesRemaining
			print "\n"
			# self.children.append(Node(self.i_depth))
		pass

	def Score(self, choice, player):
		d = 0
		r = 0
		for neighborhood in choice:
			if neighborhood == "D":
				d = d + 1
			elif neighborhood == "R":
				r = r - 1
		size = len(choice)

		if player == "MAX":
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
		else:
			if d == size:
				score = 2
			elif d > (size / 2):
				score = 1
			elif r == d:
				score =0
			elif r > (size / 2):
				score = -1
			elif r == size:
				score = -2

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
	i_curPlayer = "MAX" # max will start
	for key in i_move:
		i_value = key[1]
	max_init_node = Node(i_depth, i_curPlayer, i_move, i_movesRemaining, totalDistricts, i_value)
	print "*"*30 + "\n MAX = D \n MIN = R \n" + "*"*30

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

def firstMove(choices, lengthOfChoice):
	scorearray = []
	returnarray = []
	score = 0
	size = lengthOfChoice
	for choice in choices:
		d = 0 
		r = 0
		for i in choice:
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
		scorearray.append(score)
	bestmove_scorearray = np.asarray(scorearray)
	bestmoveindex = bestmove_scorearray.argmax(axis=0)
	bestmove = choices[bestmoveindex]
	returnarray.append(bestmoveindex)
	returnarray.append(bestmove)
	return returnarray

def firstMoveDictionary(choices, lengthOfChoice):
	newChoiceDictionary = dict()
	scorearray = []
	returnList = []
	score = 0
	size = lengthOfChoice
	for choice in choices:
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

def convertToNeighborhoodMatrix(inputtxt):
	Neighborhood = open(inputtxt, 'r')
	neighborhoodMatrix = map(lambda line: line.rstrip('\n'), Neighborhood)
	neighborhoodMatrix = [map(str, line.split(' ')) for line in neighborhoodMatrix]
	return neighborhoodMatrix

def minimaxSearch(node, depth, player):
	if (depth == 0) or (abs(node.i_value == maxsize)):
		return node.i_value
	if (player == 1):
		bestValue = -maxsize
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

























