from sys import maxsize
import itertools
import sys
import numpy as np # for numpy array

class Node:
	def __init__(self, i_depth, i_player, i_move, i_movesRemaining, i_value = 0):
		self.i_depth = i_depth
		self.i_player = i_player # true player (MAX), false player (MIN)
		self.i_value = i_value
		self.i_move = i_move
		self.i_movesRemaining = i_movesRemaining
		self.children = []
		self.CreateChildren()


	def CreateChildren(self):
		# if self.i_depth >= 0: # how far down the tree you want to calculate
		# 	if self.i_move = 
		# 	self.children.append(Node(self.i_depth))
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
	allMoves = getAllMoves(neighborhoodMatrix, totalDistricts)
	allMoves = np.asarray(allMoves)
	init_move = firstMove(allMoves, totalDistricts)
	print len(allMoves)
	allMoves = np.delete(allMoves, init_move[0], axis=0)
	init_move = init_move[1]
	print allMoves
	print "Total Neighborhoods: " + str(totalNeighborhoods) + "\n" + "Total Districts should be: " + str(totalDistricts)
	i_depth = 4 # depth of tree you want to calculate
	i_curPlayer = "MAX" # max will start
	max_init_node = Node(i_depth, i_curPlayer, init_move, allMoves)
	print "*"*30 + "\n MAX = R \n MIN = D \n" + "*"*30

def getAllMoves(matrix, lengthOfChoice):
	choices = []
	for i in range(len(matrix)): # add all columns/row choices
		column = matrix[:,i].tolist()
		row = matrix[i,:].tolist()
		choices.append(column) # column
		choices.append(row) # row
	if lengthOfChoice == 4: # for small matrix
		# upper left square
		choices.append([matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]]) 
		# upper right square
		choices.append([matrix[0][-1], matrix[0][-2], matrix[1][-1], matrix[1][-2]])
		# bottom left sqare
		choices.append([matrix[-1][0], matrix[-2][0], matrix[-1][1], matrix[-1][2]])
		# bottom right square
		choices.append([matrix[-1][-1], matrix[-2][-1], matrix[-1][-2], matrix[-2][-2]])
	return choices

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

def convertToNeighborhoodMatrix(inputtxt):
	Neighborhood = open(inputtxt, 'r')
	neighborhoodMatrix = map(lambda line: line.rstrip('\n'), Neighborhood)
	neighborhoodMatrix = [map(str, line.split(' ')) for line in neighborhoodMatrix]
	#print neighborhoodMatrix
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
		# print (str(i_depth*i_player) + ") " + " "*i_depth +str(bestvalue)
		return bestvalue
	else:
		bestvalue = maxsize
		for i in range(len(node.children)):
			child = node.children[i]
			i_val = minimaxSearch(child, i_depth - 1, 1) # drill to bottom of tree, reducing depth, flipping players
			if(abs(maxsize*i_player - i_val) < abs(maxsize * i_player - bestvalue)): # checking distance from where we want to be to where we are with child, if closer to the goal of +inf or -inf then store vale
				bestvalue = i_val
		# print (str(i_depth*i_player) + ") " + " "*i_depth +str(bestvalue)
		return bestvalue

if __name__ == "__main__":
	main()





