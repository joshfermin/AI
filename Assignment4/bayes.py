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

Collaborated with: Edward Zhu, Louis Bouddhou, Sheefali Tewari

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
def conditionalProbability(args, engine, BayesNet, debug=True):
	conditionalTuples = []

	left, given = parseConditionalArgs(args)

	leftTuple = bruteforcetuple(BayesNet, left)

	#list of tuples for given conditions
	for letter in given:
		conditionalTuples.append(bruteforcetuple(BayesNet, letter))

	for condition, truth in conditionalTuples:
		engine.evidence[condition] = truth

	# left side of | 
	toCalculate, leftTruth = leftTuple

	Q = engine.marginal(toCalculate)[0]
	index = Q.generate_index([leftTruth], range(Q.nDims))
	conditionalProbablity = Q[index]

	if debug: print "The conditional probability of", toCalculate.name, "=", leftTruth, ", given", given, "is: ", conditionalProbablity
	return conditionalProbablity

#############################################
# Calculates joint probability by calling the 
# recursive jointProbability function
def jointProbabilityDistribution(args, Engine, BayesNet, argsarray):
	result = jointProbability(args, Engine, BayesNet, argsarray)
	print "The joint probability of", args, "is:", result

#############################################
# Calculates joint probability by using a recursive
# method. (this only works for the lowercase) I.e.  
# P(Z=z, X=x, Y=y) = jointProbability(Z=z, jointProbability(X=x,Y=y)))
def jointProbability(args, engine, BayesNet, argsarray):
	typeArgs = checkArgs(args)
	if typeArgs == "lower":
		if len(argsarray) <= 1:
			print "Joint Probability Distribution must take at least 2 arguments"
			sys.exit(2)
		elif len(argsarray) == 2:
			conditionalArgs = argsarray[0] + "|" + argsarray[1]
			marginalArgs = argsarray[1]
			return conditionalProbability(conditionalArgs, engine, BayesNet, False) * marginalProbability(marginalArgs, engine, BayesNet, False)
		elif len(argsarray) > 2:
			conditionalArgs = argsarray[0] + "|" + argsarray[1]
			toCalculate = argsarray.pop(0)
			args = "".join(argsarray)
			argsarray = parseJointArgs(args)
			return conditionalProbability(conditionalArgs, engine, BayesNet, False) * jointProbability(args, engine, BayesNet, argsarray)
	elif typeArgs == "upper":
		print "upper"
		if len(argsarray) <= 1:
			print "Joint Probability Distribution must take at least 2 arguments"
			sys.exit(2)
		elif len(argsarray) == 2:
			conditionalArgs = argsarray[0] + "|" + argsarray[1]
			marginalArgs = argsarray[1]
			return conditionalProbability(conditionalArgs, engine, BayesNet, False) * marginalProbability(marginalArgs, engine, BayesNet, False)
		elif len(argsarray) > 2:
			conditionalArgs = argsarray[0] + "|" + argsarray[1]
			toCalculate = argsarray.pop(0)
			args = "".join(argsarray)
			argsarray = parseJointArgs(args)
			return conditionalProbability(conditionalArgs, engine, BayesNet, False) * jointProbability(args, engine, BayesNet,  argsarray)
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

def parseConditionalArgs(args):
	splitPipe = args.split('|')
	left = splitPipe[0]
	right = splitPipe[1]

	given = list(right)
	given = iter(given)
	conditionalArgs2 = []
	skip = False
	for string in given:
		if string == "~":
			conditionalArgs2.append("~" + given.next())
			continue
		else:
			conditionalArgs2.append(string)
	query = left
	return query, conditionalArgs2

def bruteforcetuple(BayesNet, letter, joint_distrib=False):
	for node in BayesNet.nodes:
		if node.id == 0:
			pollution = node
		if node.id == 1:
			smoker = node
		if node.id == 2:
			cancer = node
		if node.id == 3:
			xray = node
		if node.id == 4:
			dyspnoea = node

	if letter == 'p':
		returntuple = (pollution, True)
	elif letter == 's':
		returntuple = (smoker, True)
	elif letter == 'c':
		returntuple = (cancer, True)
	elif letter == 'x':
		returntuple = (xray, True)
	elif letter == 'd':
		returntuple = (dyspnoea, True)
	elif letter == '~p':
		returntuple = (pollution, False)
	elif letter == '~s':
		returntuple = (smoker, False)
	elif letter == '~c':
		returntuple = (cancer, False)
	elif letter == '~x':
		returntuple = (xray, False)
	elif letter == '~d':
		returntuple = (dyspnoea, False)
	else:
		print "Please give a good condition."
		exit()
	return returntuple

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