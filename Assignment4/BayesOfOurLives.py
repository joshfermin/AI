import getopt
import sys

class Node:
	def __init__(self, children, parents, probability, value):
		self.children = children
		self.parents = parents
		self.probability = probability
		self.value = value

def main():
	BayesNet = CreateBayesNet();
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hgjm:v", ["help", "conditional=", "joint=", "marginal="])
	except getopt.GetoptError as err:
        # print help information and exit:
		print str(err) # will print something like "option -a not recognized"
		sys.exit(2)
	output = None
	verbose = False
	for o, a in opts:
		if o == "-v":
			verbose = True # what does this do?
			# somehow makes args work
		elif o in ("-h", "--help"):
			print "-g is flag for conditional probability\n-j is flag for joint probability\n-m is flag for marginal probability"
			sys.exit()
		elif o in ("-g", "--conditional"):
			args = a
			conditionalProbablity(args, BayesNet)
		elif o in ("-j", "--joint"):
			args = a
			jointProbability(args, BayesNet)
		elif o in ("-m", "--marginal"):
			args = a
			marginalProbability(args, BayesNet)
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

def marginalProbability(args, BayesNet):
	# TODO: function to determine what args is
	print "\nThe marginal probability for " + args + " is:\n"
	argtype = checkArgs(args)
	arglookup = findArgValue(args)
	for node in BayesNet:
		if node.value == arglookup:
			if argtype == "lower":
				prettyPrint(node.probability, args)
				return node.probability
			elif argtype == "upper":
				prettyPrint(node.probability, args.lower())
				inverseProbabilities = dict()
				for key in node.probability:
					inverseProbabilities[key] = (1 - node.probability[key])
				prettyPrint(inverseProbabilities, "~" + args.lower())
			elif argtype == "squiggle":
				inverseProbabilities = dict()
				for key in node.probability:
					inverseProbabilities[key] = (1 - node.probability[key])
				prettyPrint(inverseProbabilities, args)
			# sum up values in dict
	return

def prettyPrint(dictionary, args):
	print "{:<8} {:<10}".format("P", "P(" + args + ")")
	print "-------------"
	for k, v in dictionary.iteritems():
		print "{:<8} {:<10}".format(k, v)
	print "\n"

def checkArgs(args):
	if args.islower():
		if "~" in args:
			return "squiggle"
		else:
			return "lower"
	elif args.isupper():
		return "upper"
	
def findArgValue(args):
	if args.islower():
		if "~" in args:
			return args.translate(None, '~')
		else:
			return args
	elif args.isupper():
		return args.lower()


def CreateBayesNet():
	Pollution = Node([], None, {'L':0.9}, "p")
	Smoker = Node([], None, {'T':0.3}, "s")
	Cancer = Node([], [], {'H T':0.05, 'H F':0.02, 'L T':0.03, 'L F':0.001}, "c")
	Dysponea = Node(None, [], {'T':0.65, 'F':0.30}, "d")
	Xray = Node(None, [], {'T':0.90, 'F':0.20}, "x")

	p_children = []
	p_children.append(Cancer)
	Pollution.children = p_children

	s_children = []
	s_children.append(Cancer)
	Smoker.children = s_children

	c_parents = []
	c_parents.append(Pollution)
	c_parents.append(Smoker)
	Cancer.parents = c_parents

	c_children = []
	c_children.append(Xray)
	c_children.append(Dysponea)
	Cancer.children = c_children

	d_parents = []
	d_parents.append(Cancer)
	Dysponea.parents = d_parents

	x_parents = []
	x_parents.append(Cancer)
	Xray.append = x_parents

	BayesNet = []
	BayesNet.append(Pollution)
	BayesNet.append(Smoker)
	BayesNet.append(Cancer)
	BayesNet.append(Dysponea)
	BayesNet.append(Xray)

	return BayesNet


if __name__ == "__main__":
	main()

#http://healthyalgorithms.com/2011/11/23/causal-modeling-in-python-bayesian-networks-in-pymc/
