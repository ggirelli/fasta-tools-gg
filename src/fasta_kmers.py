#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# 
# Author: Gabriele Girelli
# Email: gigi.ga90@gmail.com
# Version: 1.0.0
# Date: 20170706
# Description:	split sequence line at a given position (default 80 nt, as for
# 				fasta format definition). If negative position is given, keeps
# 				the whole sequence on a single line. Helpful for analyses.
# 
# ------------------------------------------------------------------------------



# DEPENDENCIES =================================================================

import argparse

# PARAMETERS ===================================================================

# Add script description
parser = argparse.ArgumentParser(
	description = 'Generate k-mers from fasta file.'
)

# Add mandatory arguments
parser.add_argument('k', type = int, nargs = 1,
	help = "Oligo length in nt.")
parser.add_argument('fasta', type = str, nargs = 1,
	help = 'Path to input fasta file.')

# Parse arguments
args = parser.parse_args()

# Assign to in-script variables
fa_in = args.fasta[0]
k = args.k[0]

# FUNCTIONS ====================================================================

def mk_oligo(eid, eseq, k):
	"""Make k-mers from provided sequence.

	Args:
		eid (string): element ID.
		eseq (string): element sequence.
		k (int): oligo length.

	Return:
		string: fasta-like oligo sequence.
	"""
	eseq = [eseq[i:min(i + k, len(eseq))]for i in range(0, len(eseq), k)]

	faseq = ["> %s:o%d\n%s" % (eid, i, format_element(eseq[i]))
		for i in range(len(eseq))]

	return("\n".join(faseq))

def format_element(eseq):
	"""Format a sequence element using FASTA format (split in lines of 80 chr).

	Args:
		eseq (string): element sequence.

	Return:
		string: lines of 80 chr
	"""
	k = 80
	eseq = [eseq[i:min(i + k, len(eseq))]for i in range(0, len(eseq), k)]
	return("\n".join(eseq))

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
				print(mk_oligo(*e, k))

				# Reset sequence
				e[1] = ""

			# Save ID
			e[0] = line[1:].strip()
			continue
		else:
			# Save sequence
			e[1] += line.strip()
			continue
print(mk_oligo(*e, k))

# Close file pointers
fi.close()

# END ==========================================================================

################################################################################
