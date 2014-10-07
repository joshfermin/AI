from sys import maxsize
import itertools
import sys

class Node:
	def __init__(self, i_depth, i_player, i_choicesRemaining, i_value = 0):
		self.i_depth = i_depth
		self.i_player = i_player # true player (MAX), false player (MIN)
		self.i_choicesRemaining = i_choicesRemaining
		self.i_value = i_value
		self.children = []
		self.CreateChildren()

	def CreateChildren(self):
		self.i_choicesRemaining
		if self.i_depth >= 0: # stop function at depth 0
			# for i in range(1,)
			v = self.i_choicesRemaining - i # how many spots remain
			self.children.append(Node(self.i_depth - 1, -self.i_player, v, self.Score))

	def Score(self, value):
		if (value == 'D'):
			return maxsize * self.i_player
		elif (value == 'R'):
			return maxsize * -self.i_player

def main():
	neighborhoodMatrix = convertToNeighborhoodMatrix(sys.argv[1])
	totalNeighborhoods = len(list(itertools.chain(*neighborhoodMatrix))) # get number of choices
	totalDistricts = len(neighborhoodMatrix)

	i_depth = 4 # depth of tree you want to calculate
	i_curPlayer = 1 # max will start 
	print "*"*30 + "\n MAX = R \n MIN = D \n" + "*"*30

def convertToNeighborhoodMatrix(inputtxt):
	Neighborhood = open(inputtxt, 'r')
	neighborhoodMatrix = map(lambda line: line.rstrip('\n'), Neighborhood)
	neighborhoodMatrix = [map(str, line.split(' ')) for line in neighborhoodMatrix]
	print neighborhoodMatrix
	return neighborhoodMatrix

def WinCheck(finalDistrictArray, playerNum):
	pass


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

# def minimaxSearch(node, i_depth, i_player):
# 	if (i_depth == 0) or (abs(node.i_value == maxsize)): # check if we are depth at 0 or reach a node that is win or lose condition
# 		return node.i_value # pass best choice up to parent node

# 	bestvalue = maxsize * -i_player # assign value of inf * player number ( start with max )

# 	for i in range(len(node.children)): #go to children
# 		child = node.children[i]
# 		i_val = minimaxSearch(child, i_depth - 1, -i_player) # drill to bottom of tree, reducing depth, flipping players
# 		if(abs(maxsize*i_player - i_val) < abs(maxsize * i_player - bestvalue)): # checking distance from where we want to be to where we are with child, if closer to the goal of +inf or -inf then store vale
# 			bestvalue = i_val
	
# 	return bestvalue



# rules
	# select districts one at a time
	# 



# self - used to attach variables and functions to a class
	# constructor - function that is called when class instance is created
		# def __init__(self):
			# self.y = 5

# implement minimax search to find optimal move for MAX and MIN to play perfect game
# MAX and MIN searching for district alignment in best interest
# MAX party selects move that maximizes utility
# MIN party selects move that minimizes utility
# MAX as favored party, MIN is spoiler.9

#http://www.neverstopbuilding.com/minimax
#https://www.youtube.com/watch?v=fInYh90YMJU