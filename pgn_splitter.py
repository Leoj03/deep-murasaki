#!/usr/bin/env python
#
# pgn_splitter.py -- splits large .pgn files into the bunch of smaller ones
# to make use of the multiprocessing and making sure all CPU cores are loaded
# evenly instead of one core maxed to 100% processing one large single file.

import sys, os

WAYS_TO_SPLIT = 7	# should load up to 7 cores

if len(sys.argv) < 2 :
	sys.exit('USAGE: pgn_splitter file.pgn')

if not sys.argv[1].endswith( '.pgn' ) :
	sys.exit('Invalid file: ' + sys.argv[1] )

num = 0
events = 0
name = sys.argv[1][:-4]
line = ''

with open( sys.argv[1] ) as fin :
	while True :
		line = fin.readline()
		if len(line) == 0 : break
		if line.startswith( '[Event' ) :
			events += 1

	split_threshold = events / WAYS_TO_SPLIT + 4;
	print events, 'events, splitting', WAYS_TO_SPLIT, 'ways by', split_threshold

	events = 0
	fin.seek( 0 )	# rewind

	while True :
		new_name = '%s.%03d.pgn' % (name, num)
		print new_name
		with open( new_name, 'wb' ) as fout :
			if len(line) :
				fout.write(line)
			num += 1
			while True :
				line = fin.readline()
				if len(line) == 0 : break

				if line.startswith( '[Event' ) :
					events += 1
					if events > split_threshold :
						events = 0
						break

				fout.write(line)

		if events : break

