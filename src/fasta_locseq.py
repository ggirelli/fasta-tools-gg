#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# 
# Author: Gabriele Girelli
# Email: gigi.ga90@gmail.com
# Version: 1.0.0
# Date: 20170808
# Project: GPSeq
# Description:	find sequence location in a FASTA file. Designed to identify
# 				cutsites or similar sequences in big fasta files (e.g.,
# 				reference genome,...).
# 
# ------------------------------------------------------------------------------



# DEPENDENCIES =================================================================

import argparse

# PARAMETERS ===================================================================


# Add script description
parser = argparse.ArgumentParser(
	description = 'Find locations of a sequence in a FASTA file.'
)

# Add mandatory arguments
parser.add_argument('haystack', type = str, nargs = 1,
	help = 'FASTA file to bsearched for sequence locations.')
parser.add_argument('needle', type = str, nargs = 1,
	help = 'Sequence string to be looked for in the FASTA file.')

# Add arguments with default value
parser.add_argument('-p', type = str, nargs = 1, metavar = 'prefix',
	help = """Name prefix. Default: 'loc_'""", default = ["loc_"])

# Add flags
parser.add_argument('-g',
	action = 'store_const', dest = 'glob',
	const = True, default = False,
	help = 'Global location name. Requires sorted FASTA.')

# Parse arguments
args = parser.parse_args()

# Assign to in-script variables
fain_path = args.haystack[0]
needle = args.needle[0]
prefix = args.p[0]
glob = args.glob

# FUNCTIONS ====================================================================

def search_needle(line, needle, curr_head, curr_pos, loc_counter, prefix):
	# Search current sequence line
	# 
	# Args:
	# 	line (string): sequence string to be searched for (haystack).
	# 	needle (string): sequence to be searched.
	# 	curr_head (string): current header for printing locations.
	# 	curr_pos (int): current position, for multi-line sequence.
	# 	loc_counter (int): position ID, incremental and unique.
	# 	prefix (string): prefix for name column.
	# 
	# Returns:
	# 	
	
	needle_len = len(needle)
	keep_iterating = True		# Iterating condition
	last_index = -needle_len	# Position of last location in current line,
								# set to -needle_len to start search from 0
								# and then continue accordingly.

	while ( keep_iterating ):
		# Use try to capture absence of more hit through index()
		try:
			if last_index + needle_len >= len(line):
				# Stop iterating if the end was reached
				keep_iterating = False
			else:
				# Look for hits
				last_index = line.index(needle,
					last_index + needle_len)

				# If found, print it
				print("%s\t%d\t%d\t%s%d" % (
					curr_head,
					last_index + curr_pos +1,				# +1 for 1-indexing
					last_index + curr_pos + needle_len +1,	# +1 for 1-indexing
					prefix, loc_counter))

				# And increase location ID
				loc_counter += 1
		except ValueError:
			# No more instances in current line, move on
			keep_iterating = False

	return((loc_counter, last_index))

# RUN ==========================================================================

needle_len = len(needle)	# Needle length
curr_head = ""				# Current header for printing locations
prev_seq = ""				# Previous sequence for boundary search
curr_pos = 0				# Current position, for multi-line sequence
loc_counter = 1				# Position ID, incremental and unique

# Cycle through the file
with open(fain_path, 'r') as fain:

	# Line by line
	for line in fain:
		line = line.strip()

		if '>' == line[0]:
			# If it's a header line, reset and proceed
			curr_head = line[1:]
			curr_pos = 0
			prev_seq = ""

			# Reset location counter if element-wise (not global)
			if not glob:
				loc_counter = 1
		else:
			# Otherwise, look for the needle
			line = line.upper()

			# Check line length
			if needle_len > len(line):
				continue

			# Search border
			border = prev_seq + line[:(needle_len-1)]
			loc_counter, last_index = search_needle(border, needle,
				curr_head, curr_pos - len(prev_seq), loc_counter, prefix)

			# Search current line
			loc_counter, last_index = search_needle(line, needle,
				curr_head, curr_pos, loc_counter, prefix)

			# Save current 
			prev_seq = line[max(len(line)-needle_len, last_index + needle_len):]
			curr_pos += len(line)

# Close file buffer
fain.close()

# END ==========================================================================

################################################################################
