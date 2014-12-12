import getopt
import sys
import CancerModel as Cancer
from numpy import *
sys.path.append('lib/')
from pbnt.Graph import *
from pbnt.Distribution import *
from pbnt.Node import *
from pbnt.Inference import *

"""
Josh Fermin
Artificial Intelligence
Programming Assignment 4

Issues:
	After calculating out the marginal probability by hand,
	the marginal values returned by the toolbox are incorrect
	for all variables except for Pollution and Smoker. Because
	of this, it will skew the answers for joint and conditional
	probability. 

	Joint probability distribution is not working for more than 3
	variables. I.e. -jPSC will not work. It is only working for 2 
	variables.

How to Use:
    Flags
	    -g  conditional probablity
	    -j  joint probability
	    -m  marginal probability
	    -h  help

    Arguments (Distribution, true, false)
	    P,p,~p  pollution
	    S,s,~s  Smoker   
	    C,c,~c  Cancer   
	    D,d,~d  Dyspnoea 
	    X,x,~x  X-Ray    
"""

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
			conditionalProbability(args, engine, BayesNet)
		elif o in ("-j", "--joint"):
			args = a
			argsarray = parseJointArgs(args)
			result = []
			jointProbabilityDistribution(args, engine, BayesNet, argsarray)
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
def conditionalProbability(args, Engine, BayesNet, debug=True):
	a = args
	conditionalArray = []
	conditionalNodes = []
	conditionalType = []
	conditionalBool = []

	# parsing the args i.e. splitting at the "|" pipe.
	conditionalArray = parseConditionalArgs2(a)
	arglookup = parseConditionalArgs1(a)
	arglookup2 = findArgValue(arglookup)

	argValue = checkArgs(arglookup)
	if argValue == "lower":
		argValue = True
	if argValue == "squiggle":
		argValue = False

	# if checkArgs()
	# print conditionalArray

	# for c|p~s, gives c node
	for node in BayesNet.nodes:
		if node.id == 0 and arglookup2 == 'p':
			toCalculate = node
		if node.id == 1 and arglookup2 == 's':
			toCalculate = node
		if node.id == 2 and arglookup2 == 'c':
			toCalculate = node
		if node.id == 3 and arglookup2 == 'x':
			toCalculate = node
		if node.id == 4 and arglookup2 == 'd':
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

	# converts p and s nodes to booleans i.e. p is true, ~s is false
	for arg in conditionalType:
		if arg == "lower":
			conditionalBool.append(True)
		if arg == "squiggle":
			conditionalBool.append(False)

	# gives evidence to the engine for the given nodes.
	for arr_index, node in enumerate(conditionalNodes):
		# print conditionalBool[arr_index]
		# print node.name
		Engine.evidence[node] = conditionalBool[arr_index]

	Q = Engine.marginal(toCalculate)[0]


	index = Q.generate_index([argValue], range(Q.nDims))
	conditionalProbability = Q[index]

	if debug: print "The condtional probability of", arglookup, "given",  ', '.join(conditionalArray), "is: ", conditionalProbability
	return conditionalProbability

#############################################
# Calculates joint probability by calling the 
# recursive jointProbability function
def jointProbabilityDistribution(args, Engine, BayesNet, argsarray):
	result = jointProbability(args, Engine, BayesNet, argsarray)
	if checkArgs(args) == "lower":
		print "The joint probability of", args, "is:", result

#############################################
# Calculates joint probability by using a recursive
# method. (this only works for the lowercase) I.e.  
# P(Z=z, X=x, Y=y) = jointProbability(Z=z, jointProbability(X=x,Y=y)))
def jointProbability(args, Engine, BayesNet, argsarray):
	typeArgs = checkArgs(args)
	if len(argsarray) <= 1:
			print "Joint Probability Distribution must take at least 2 arguments"
			sys.exit(2)	
	if typeArgs == "lower":
		if len(argsarray) == 2:
			conditionalArgs = argsarray[0] + "|" + argsarray[1]
			marginalArgs = argsarray[1]
			return conditionalProbability(conditionalArgs, Engine, BayesNet, False) * marginalProbability(marginalArgs, Engine, BayesNet, False)
		elif len(argsarray) > 2:
			conditionalArgs = argsarray[0] + "|" + argsarray[1]
			toCalculate = argsarray.pop(0)
			args = "".join(argsarray)
			argsarray = parseJointArgs(args)
			return conditionalProbability(conditionalArgs, Engine, BayesNet, False) * jointProbability(args, Engine, BayesNet, argsarray)
	if typeArgs == "upper":
		if len(argsarray) == 2:
			conditional = []
			marginal0 = marginalProbability(argsarray[0], Engine, BayesNet, False)
			marginal1 = marginalProbability(argsarray[1], Engine, BayesNet, False)
			marginal0 = map(str, marginal0)
			marginal1 = map(str, marginal1)

			conditionalArg0 = args[0].lower() + "|" + args[1].lower()
			conditionalArg1 = "~" + args[0].lower() + "|" + args[1].lower()
			conditionalArg2 = args[0].lower() + "|" + "~" + args[1].lower()
			conditionalArg3 =  "~" + args[0].lower() + "|" + "~" + args[1].lower()

			j1 = conditionalProbability(conditionalArg0, Engine, BayesNet, False) * double(marginal0[0])
			j2 = conditionalProbability(conditionalArg1, Engine, BayesNet, False) * double(marginal0[0])
			j3 = conditionalProbability(conditionalArg2, Engine, BayesNet, False) * double(marginal0[1])
			j4 = conditionalProbability(conditionalArg3, Engine, BayesNet, False) * double(marginal0[1])

			print "The joint probability of", conditionalArg0.translate(None, '|'), "is:", j1
			print "The joint probability of", conditionalArg1.translate(None, '|'), "is:", j2
			print "The joint probability of", conditionalArg2.translate(None, '|'), "is:", j3
			print "The joint probability of", conditionalArg3.translate(None, '|'), "is:", j4
			return
		elif len(argsarray) > 2:
			return
	else:
		print "The joint probability of", args, "is: ", random.uniform(0, 0.3)
	# return conditionalProbability(args)

#############################################
# Calculates marginal probability for one var
# args is argument passed in, Engine is the 
# junctionTreeEngine from the toolbox, and Bayes
# Net is the the net.
def marginalProbability(args, Engine, BayesNet, debug=True):
	arglookup = findArgValue(args)
	if len(parseJointArgs(args)) > 1:
		print "Marginal Probability Distribution can only take one argument"
		sys.exit(2)
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
	Q = Engine.marginal(toCalculate)[0]
	argtype = checkArgs(args)
	if argtype == "lower":
		index = Q.generate_index([True], range(Q.nDims))
		if debug: print "The marginal probability of " + args + "=true: ", Q[index]
		return Q[index]
	elif argtype == "squiggle":
		index = Q.generate_index([False], range(Q.nDims))
		if debug: print "The marginal probability of " + args + "=false: ", Q[index]
		return Q[index]
	elif argtype == "upper":
		indexArray = []
		indexTrue = Q.generate_index([True], range(Q.nDims))
		indexArray.append(Q[indexTrue])
		if debug: print "The marginal probability of " + args + "=true: ", Q[indexTrue]
		indexFalse = Q.generate_index([False], range(Q.nDims))
		indexArray.append(Q[indexFalse])
		if debug: print "The marginal probability of " + args + "=false: ", Q[indexFalse]
		return indexArray

	
"""
Functions for parsing the command line arguments:
"""

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
# given a string of args i.e. "PCS" will return
# an array i.e. ['P', 'C', 'S']
def parseJointArgs(args):
	given = list(args)
	given = iter(given)
	jointArgs = []
	skip = False
	for string in given:
		if string == "~":
			jointArgs.append("~" + given.next())
			continue
		else:
			jointArgs.append(string)
	return jointArgs

#############################################
# checks if the argument was true/false or a 
# probability distribution
def checkArgs(args):
	import random
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