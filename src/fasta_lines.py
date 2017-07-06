#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# 
# Author: Gabriele Girelli
# Email: gigi.ga90@gmail.com
# Version: 1.0.0
# Date: 20170706
# Description:	generate oligos of length k from the provided fasta file.
# 
# Note:
# 	The fasta file should have each sequence in one line.
# 
# ------------------------------------------------------------------------------



# DEPENDENCIES =================================================================

import argparse

# PARAMETERS ===================================================================

# Add script description
parser = argparse.ArgumentParser(
	description = 'Manages fasta file sequence line length.'
)

# Add mandatory arguments
parser.add_argument('fasta', type = str, nargs = 1,
	help = 'Path to input fasta file.')

# Add arguments with default value
parser.add_argument('-k', type = int, nargs = 1,
	help = """
	Sequence line length in nt. If 0, one line per sequence.
	""", default = [80])

# Parse arguments
args = parser.parse_args()

# Assign to in-script variables
fa_in = args.fasta[0]
k = args.k[0]

# FUNCTIONS ====================================================================

def format_element(eid, eseq, k):
	"""Format a sequence element using FASTA format and k sequence length.

	Args:
		eid (string): element ID.
		eseq (string): element sequence.
		k (int): sequence line length.

	Return:
		string: "> %s\n%s" % (eid, eseq_split_by_k)
	"""
	if k > 0:
		eseq = [eseq[i:min(i + k, len(eseq))]for i in range(0, len(eseq), k)]
		eseq = "\n".join(eseq)
	return("> %s\n%s" % (eid, eseq))

# RUN ==========================================================================

# Go through the input line by line
with open(fa_in, 'r') as fi:
	# Element: (ID, seq)
	e = [False, ""]

	for line in fi:
		# Check if it's an ID line or a sequence line
		if line.strip().startswith('>'):
			if type(e[0]) == type(''):
				# Write previous sequence
				print(format_element(*e, k))

				# Reset sequence
				e[1] = ""

			# Save ID
			e[0] = line[1:].strip()
			continue
		else:
			# Save sequence
			e[1] += line.strip()
			continue
print(format_element(*e, k))

# Close file pointers
fi.close()

# END ==========================================================================

################################################################################
