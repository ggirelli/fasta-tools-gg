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
	description = 'Generate k-mers from fasta file.'
)

# Add mandatory arguments
parser.add_argument('k', type = int, nargs = 1,
	help = "Oligo length in nt.")
parser.add_argument('fastaInput', type = str, nargs = 1,
	help = 'Path to input fasta file.')
parser.add_argument('fastaOutput', type = str, nargs = 1,
	help = 'Path to output with outfmt 6.')

# Parse arguments
args = parser.parse_args()

# Assign to in-script variables
fa_in = args.fastaInput[0]
fa_out = args.fastaOutput[0]
k = args.k[0]

# Log to screen the settings
print("""
Settings:
               FASTA input : %s
              FASTA output : %s
                         K : %d

""" % (fa_in, fa_out, k))

# FUNCTIONS ====================================================================

# RUN ==========================================================================

# Point to output file
fo = open(fa_out, 'w')

# Go through the input line by line
with open(fa_in, 'r') as fi:
	# Save current ID
	curr_id = None

	for line in fi:
		# Check if it's an ID line or a sequence line
		if line.strip().startswith('>'):
			# Save ID
			curr_id = line[1:].strip()
			continue
		else:
			# Retreive sequence
			seq = line.strip()
			seq_len = len(seq)

			# Generate oligos
			oligos = [seq[i:(i + k)] for i in range(seq_len - k + 1)]

			# Write oligos
			for oi in range(len(oligos)):
				sout = "> %s:O%d\n%s\n" % (curr_id, oi, oligos[oi])
				fo.write(sout)

# Close file pointers
fi.close()
fo.close()

# END ==========================================================================

################################################################################