import getopt
import sys
import CancerModel as Cancer
from numpy import *
sys.path.append('lib/')
from pbnt.Graph import *
from pbnt.Distribution import *
from pbnt.Node import *
from pbnt.Inference import *

class Node:
	def __init__(self, children, parents, probability, value):
		self.children = children
		self.parents = parents
		self.probability = probability
		self.value = value

def main():
	BayesNet = Cancer.cancer()
	engine = JunctionTreeEngine(BayesNet)

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hg:j:m:v", ["help", "conditional=", "joint=", "marginal="])
	except getopt.GetoptError as err:
        # print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2)
	output = None
	verbose = False
	for o, a in opts:
		if o == "-v":
			verbose = True 
		elif o in ("-h", "--help"):
			print "-g is flag for conditional probability\n-j is flag for joint probability\n-m is flag for marginal probability"
			sys.exit()
		elif o in ("-g", "--conditional"):
			args = a
			conditionalProbablity(args, engine, BayesNet)
		elif o in ("-j", "--joint"):
			args = a
			jointProbability(args, BayesNet)
		elif o in ("-m", "--marginal"):
			args = a
			marginalProbability(args, engine, BayesNet)
		else:
			assert False, "unhandled option"

#############################################
# Calculates conditional probability for one var
# args is argument passed in, Engine is the 
# junctionTreeEngine from the toolbox, and Bayes
# Net is the the net.
def conditionalProbablity(args, Engine, BayesNet):
	a = args
	conditionalArray = []
	conditionalNodes = []
	conditionalType = []
	conditionalBool = []
	conditionalArray = parseConditionalArgs2(a)
	arglookup = parseConditionalArgs1(a)
	# for c|p~s, gives c node
	for node in BayesNet.nodes:
		if node.id == 0 and arglookup == 'p':
			toCalculate = node
		if node.id == 1 and arglookup == 's':
			toCalculate = node
		if node.id == 2 and arglookup == 'c':
			toCalculate = node
		if node.id == 3 and arglookup == 'x':
			toCalculate = node
		if node.id == 4 and arglookup == 'd':
			toCalculate = node

	# for c|p~s, appends p and s nodes to conditionalNode array
	for node in BayesNet.nodes:
		for arg in conditionalArray:
			conditionalType.append(checkArgs(arg))
			arg = findArgValue(arg)
			if node.id == 0 and arg == 'p':
				conditionalNodes.append(node)
			if node.id == 1 and arg == 's':
				conditionalNodes.append(node)
			if node.id == 2 and arg == 'c':
				conditionalNodes.append(node)
			if node.id == 3 and arg == 'x':
				conditionalNodes.append(node)
			if node.id == 4 and arg == 'd':
				conditionalNodes.append(node)

	# converts p and s nodes to booleans i.e. p - true, ~s is false
	for arg in conditionalType:
		if arg == "lower":
			conditionalBool.append(True)
		if arg == "squiggle":
			conditionalBool.append(False)
	for arr_index, node in enumerate(conditionalNodes):
		Engine.evidence[node] = conditionalBool[arr_index]

	Q = Engine.marginal(toCalculate)[0]

	index = Q.generate_index([False], range(Q.nDims))
	conditionalProbablity = Q[index]
	print "The condtional probability of", arglookup, "given",  ', '.join(conditionalArray), "is: ", conditionalProbablity
	return conditionalProbablity


def jointProbability(args, BayesNet):
	print "\nThe joint probability for " + args + " is:\n"
	argtype = checkArgs(args)
	arglookup = findArgValue(args)
	for node in BayesNet:
		if node.value == arglookup:
			if argtype == "lower":
				return
			if argtype == "upper":
				return
			if argtype == "squiggle":
				return

#############################################
# Calculates marginal probability for one var
# args is argument passed in, Engine is the 
# junctionTreeEngine from the toolbox, and Bayes
# Net is the the net.
def marginalProbability(args, Engine, BayesNet):

	arglookup = findArgValue(args)
	for node in BayesNet.nodes:
		if node.id == 0 and arglookup == 'p':
			toCalculate = node
		if node.id == 1 and arglookup == 's':
			toCalculate = node
		if node.id == 2 and arglookup == 'c':
			toCalculate = node
		if node.id == 3 and arglookup == 'x':
			toCalculate = node
		if node.id == 4 and arglookup == 'd':
			toCalculate = nodes

	Q = Engine.marginal(toCalculate)[0]
	argtype = checkArgs(args)
	if argtype == "lower":
		index = Q.generate_index([True], range(Q.nDims))
		print "The marginal probability of " + args + "=true: ", Q[index]
		return Q[index]
	elif argtype == "squiggle":
		index = Q.generate_index([False], range(Q.nDims))
		print "The marginal probability of " + args + "=false: ", Q[index]
		return Q[index]
	elif argtype == "upper":
		print "do something"

#############################################
# given part i.e. p|c~x will return ['c', '~x']
def parseConditionalArgs2(args):
	given = args.split("|", 1)[1]
	given = list(given)
	given = iter(given)
	conditionalArgs2 = []
	skip = False
	for string in given:
		if string == "~":
			conditionalArgs2.append("~" + given.next())
			continue
		else:
			conditionalArgs2.append(string)
	return conditionalArgs2

#############################################
# toCalculate part i.e. p|c~x will return string p
def parseConditionalArgs1(args):
	given = args.split("|", 1)[0]
	return given

#############################################
# checks if the argument was true/false or a 
# probability distribution
def checkArgs(args):
	if args.islower():
		if "~" in args:
			return "squiggle"
		else:
			return "lower"
	elif args.isupper():
		return "upper"

#############################################
# returns the letter of the arg in lowercase
def findArgValue(args):
	if args.islower():
		if "~" in args:
			return args.translate(None, '~')
		else:
			return args
	elif args.isupper():
		return args.lower()

if __name__ == "__main__":
	main()