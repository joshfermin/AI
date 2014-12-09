#! /usr/bin/python
# viterbi.py

# imports
from __future__ import division
# from optparse import OptionParser
import getopt
import sys

from util import *
from dataset import DataSet
from hmm import HMM

@print_timing
def run_viterbi(hmm, d, debug=False):
	"""Run the viterbi algorithm for each test sequence in the given dataset"""
	total_error = 0
	total_n = 0
	if debug:
		print "\nRunning viterbi on each test sequence..."
	for i in range(len(d.test_output)):
		if debug:
			print "Test sequence %d:" % i
		errors = 0
		most_likely = [d.states[j] for j in hmm.most_likely_states(d.test_output[i])]
		actual = [d.states[j] for j in d.test_state[i]]
		n = len(most_likely)
	#       print "len(most_likely) = %d  len(actual) = %d" % (n, len(actual))
		for j in range(n):
			if debug:
				print "%s     %s      %s" % (
				actual[j], most_likely[j], d.outputs[d.test_output[i][j]])
			if actual[j] != most_likely[j]:
				errors += 1
			if debug:
				print "errors: %d / %d = %.3f\n" % (errors, n, errors * 1.0 / n)
	total_error += errors
	total_n += n

	err =  total_error * 1.0 / total_n
	if debug:
		print "Total mistakes = %d / %d = %f" % (total_error, total_n, err)
	return err


def train_hmm_from_data(data_filename, debug=False):
	if debug:
		print "\n\nReading dataset %s ..." % data_filename
	data_filename = normalize_filename(data_filename)
	d = DataSet(data_filename)
	#if options.verbose:
	#   print d
	if debug:
		print "Building an HMM from the full training data..."
	hmm = HMM(d.states, d.outputs)
	hmm.learn_from_labeled_data(d.train_state, d.train_output)
	if debug:
		print "The model:"
		print hmm
	return (hmm, d)

def main(argv=None):
	HMMorder = 1
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hp:o:f:", ["help", "problem=", "option=", "file="])
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
		elif o in ("-f", "--file"):
			filename = a
			print filename
		elif o in ("-o", "--option"):
			if int(a) > 2 or int(a) < 1:
				assert False, "Not a valid hmm order flag"
			else:
				option = int(a)
		else:
			assert False, "unhandled option"
	if option == 2:
		print "Functionality not implemented"
		HMMorder = 2


	if problem == 1:
	  hmm, d = train_hmm_from_data(filename, verbose)
	  err_full = run_viterbi(hmm, d , True)

		# robot
		# hmm = get_robot_model()
  #       print "HMM is:"
  #       print hmm
		
  #       seq = [0,1,2]
  #       logp = hmm.log_prob_of_sequence(seq)
  #       p = exp(logp)
  #       print "prob ([]): logp= %f  p= %f" % (logp, p)
  #       print "most likely states (walk, shop, clean) = %s" % hmm.most_likely_states(seq)

	# elif problem == 2:
	# 	# typo correction
	# elif problem == 3:
		# topic change

if __name__ == "__main__":
	main()
	# main()