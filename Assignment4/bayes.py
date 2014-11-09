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
	conditional = []
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
			parseConditionalArgs(a)
			# conditionalProbablity(args, BayesNet)
		elif o in ("-j", "--joint"):
			args = a
			jointProbability(args, BayesNet)
		elif o in ("-m", "--marginal"):
			arglookup = findArgValue(a)
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
			args = a
			marginalProbability(args, BayesNet, engine, toCalculate)
		else:
			assert False, "unhandled option"

def conditionalProbablity(args, BayesNet):
	print "\nThe conditional probability for " + args + " is:\n"
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

def marginalProbability(args, BayesNet, Engine, toCalculate):
	arglookup = findArgValue(args)
	Q = Engine.marginal(toCalculate)[0]
	argtype = checkArgs(args)
	
	if argtype == "lower":
		index = Q.generate_index([True], range(Q.nDims))
		print "The marginal probability of " + args + "=true: ", Q[index]
	elif argtype == "squiggle":
		index = Q.generate_index([False], range(Q.nDims))
		print "The marginal probability of " + args + "=false: ", Q[index]
	elif argtype == "upper":
		print "do something"
	# elif argtype == "upper":
	# 	prettyPrint(node.probability, args.lower())
	# 	inverseProbabilities = dict()
	# 	for key in node.probability:
	# 		inverseProbabilities[key] = (1 - node.probability[key])
	# 	prettyPrint(inverseProbabilities, "~" + args.lower())
	# elif argtype == "squiggle":
	# 	inverseProbabilities = dict()
	# 	for key in node.probability:
	# 		inverseProbabilities[key] = (1 - node.probability[key])
	# 	prettyPrint(inverseProbabilities, args)
			# sum up values in dict
	return 

def prettyPrint(dictionary, args):
	print "{:<8} {:<10}".format("P", "P(" + args + ")")
	print "-------------"
	for k, v in dictionary.iteritems():
		print "{:<8} {:<10}".format(k, v)
	print "\n"

def parseConditionalArgs(args):
	given = args.split("|", 1)[1]
	print given

	return 

def checkArgs(args):
	# checks the type of args
	if args.islower():
		if "~" in args:
			return "squiggle"
		else:
			return "lower"
	elif args.isupper():
		return "upper"
	
def findArgValue(args):
	# returns the letter of the arg in lowercase
	if args.islower():
		if "~" in args:
			return args.translate(None, '~')
		else:
			return args
	elif args.isupper():
		return args.lower()

if __name__ == "__main__":
	main()

#http://healthyalgorithms.com/2011/11/23/causal-modeling-in-python-bayesian-networks-in-pymc/
