# from util import *
from numpy import *
from math import log
import copy
import sys
import itertools
import getopt

MAX_PRINTING_SIZE = 30
PRODUCTION = True

class HMM:
    """ HMM Class that defines the parameters for HMM """
    def __init__(self, states, outputs):
        """If the hmm is going to be trained from data with labeled states,
        states should be a list of the state names.  If the HMM is
        going to trained using EM, states can just be range(num_states)."""
        self.states = states
        self.outputs = outputs
        n_s = len(states)
        n_o = len(outputs)
        self.num_states = n_s
        self.num_outputs = n_o
        self.initial = zeros(n_s)
        self.transition = zeros([n_s,n_s])
        self.observation = zeros([n_s, n_o])

    def check(self):
        check_model((self.initial, self.transition, self.observation))

    def set_hidden_model(self, init, trans, observ):
        """ Debugging function: set the model parameters explicitly """
        self.num_states = len(init)
        self.num_outputs = len(observ[0])
        self.initial = array(init)
        self.transition = array(trans)
        self.observation = array(observ)
        self.check()
        self.compute_logs()

    def log_prob_of_sequence(self, sequence):
	    model = (self.initial, self.transition, self.observation) 
	    alpha, loglikelyhood = get_alpha(sequence, model)
	    return loglikelyhood

    def most_likely_states(self, sequence, debug=False):
        """Return the most like sequence of states given an output sequence.
        Uses Viterbi algorithm to compute this.
        """
        # Code modified from wikipedia
        # Modifications: use logs, don't compute total prob of sequence
        cnt = 0
        states = range(0, self.num_states)
        T = {}
        for state in states:
            ##          V.path   V. prob.
            T[state] = ([state], self.log_initial[state])
        for output in sequence:
            cnt += 1
            if debug:
                if cnt % 500 == 0:
                    print "processing sequence element %d" % cnt
                    sys.stdout.flush()
            U = {}
            for next_state in states:
                argmax = None
                valmax = None
                for source_state in states:
                    (v_path, v_prob) = T[source_state]
                    p = (self.log_observation[source_state][output] +
                         self.log_transition[source_state][next_state])
                    v_prob += p
                    if valmax is None or v_prob > valmax:
                        argmax = v_path
                        valmax = v_prob
                # Using a nested (reversed) list for performance
                # reasons: the wikipedia code does a list copy, which
                # causes problems with long lists.  The reverse is
                # needed to make the flatten easy. 
                argmax = [next_state, argmax]
                U[next_state] = (argmax, valmax)
            T = U
        ## apply sum/max to the final states:
        argmax = None
        valmax = None
        for state in states:
            (v_path, v_prob) = T[state]
#            print "%s  %s" % T[state]
            if valmax is None or v_prob > valmax:
                argmax = v_path
                valmax = v_prob
                
        # Kept the list as in reverse order, and nested to make things fast.
        print "THIS IS ARGMAX", argmax
        ans = flatten(argmax)
        print "THIS IS ANS", ans
        # ans = custom_flatten(argmax)
        ans.reverse()
        return ans[:-1]


    def compute_logs(self):
        """Compute and store the logs of the model"""
        f = lambda xs: map(log, xs)
        self.log_initial = f(self.initial)
        self.log_transition = map(f, self.transition)
        self.log_observation = map(f, self.observation)

    def __repr__(self):
        if len(self.states) > MAX_PRINTING_SIZE:
            statestr = " <too many states to print (%d)>" % len(self.states)
        else:
        	# print self.states # ['Rainy', 'Sunny']
            statestr = ", ".join(self.states)
        if len(self.outputs) > MAX_PRINTING_SIZE:
            outputstr = " <too many outputs to print (%d)>" % len(self.outputs)
        else:
        	# print self.outputs # ['walk', 'shop', 'clean']
            outputstr = ", ".join(self.outputs)
        return """states = %s
observations = %s
%s
""" % (statestr,
       outputstr,
       string_of_model((self.initial, self.transition, self.observation), ""))

def flatten(lis):
    """Given a list, possibly nested to any level, return it flattened."""
    new_lis = []
    for item in lis:
        if type(item) == type([]):
            new_lis.extend(flatten(item))
        else:
            new_lis.append(item)
    return new_lis

def get_alpha(obs, model):
    """ Returns the array of alphas and the log likelyhood of the sequence.

    Note: doing normalization as described in Ghahramani '01--just normalizing
    both alpha and beta to sum to 1 at each time step."""

    normalize = PRODUCTION
    (initial, tran_model, obs_model) = model
    N = shape(tran_model)[0]
    n = len(obs)
    loglikelyhood = 0

    # indexes: alpha[time,state]
    alpha = zeros((n,N))
    alpha[0,:] = initial * obs_model[:,obs[0]]
    if normalize:
        normalization = sum(alpha[0,:])
        alpha[0,:] /= normalization
        # adding the logs of the normalization gives the 
        # log likelyhood of the sequence.  Why?
        loglikelyhood += log(normalization)

    for t in range(1,n):
        for j in range(N):
            s = sum(tran_model[:,j]*alpha[t-1,:])
            alpha[t,j] = s * obs_model[j,obs[t]]
        if normalize: 
            normalization = sum(alpha[t,:])
            loglikelyhood += log(normalization)
            alpha[t,:] /= normalization
    
    if not normalize:
        loglikelyhood = log (sum(alpha[n-1,:]))
        
    return alpha, loglikelyhood

def format_array(arr):
    s = shape(arr)
    if s[0] > MAX_PRINTING_SIZE or (len(s) == 2 and s[1] > MAX_PRINTING_SIZE):
        return "[  too many values (%s)   ]" % str(s)

    if len(s) == 1:
        return  "[  " + (
            " ".join(["%.6f" % float(arr[i]) for i in range(s[0])])) + "  ]"
    else:
        lines = []
        for i in range(s[0]):
            lines.append("[  " + "  ".join(["%.6f" % float(arr[i,j]) for j in range(s[1])]) + "  ]")
        return "\n".join(lines)

def string_of_model(model, label):
    (initial, tran_model, obs_model) = model
    return """
Model: %s 
initial: 
%s

transition: 
%s

observation: 
%s

""" % (label, 
       format_array(initial),
       format_array(tran_model),
       format_array(obs_model))

def check_model(model):
    """Check that things add to one as they should"""
    (initial, tran_model, obs_model) = model
    for state in range(len(initial)):
        assert((abs(sum(tran_model[state,:]) - 1)) <= 0.01)
        assert((abs(sum(obs_model[state,:]) - 1)) <= 0.01)
        assert((abs(sum(initial) - 1)) <= 0.01)

def print_model(model, label):
    check_model(model)
    print string_of_model(model, label)  

def get_wikipedia_model():
    # From the rainy/sunny example on wikipedia (viterbi page)
    hmm = HMM(['Rainy','Sunny'], ['walk','shop','clean'])
    init = [0.6, 0.4]
    trans = [[0.7,0.3], [0.4,0.6]]
    observ = [[0.1,0.4,0.5], [0.6,0.3,0.1]]
    hmm.set_hidden_model(init, trans, observ)
    return hmm

def test():
    hmm = get_wikipedia_model()
    print "HMM is:"
    print hmm
    
    seq = [0,1,2]
    logp = hmm.log_prob_of_sequence(seq)
    p = exp(logp)
    print "prob ([walk, shop, clean]): logp= %f  p= %f" % (logp, p)
    print "most likely states (walk, shop, clean) = %s" % hmm.most_likely_states(seq)

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hp:o:", ["help", "problem=", "option="])
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
			print "-p is problem flag 1 - 3\n-o is hmm order flag"
			sys.exit()
		elif o in ("-p", "--problem"):
			if int(a) > 3 or int(a) < 1:
				assert False, "Not a valid problem number"
			else:
				problem = int(a)
				# print problem
		elif o in ("-o", "--option"):
			if int(a) > 2 or int(a) < 1:
				assert False, "Not a valid hmm order flag"
			else:
				option = int(a)
				# print option
		else:
			assert False, "unhandled option"
	if option == 2:
		print "Funcitonality not implemented"



if __name__ == "__main__":
    main()