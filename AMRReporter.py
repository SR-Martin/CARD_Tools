#!/usr/bin/python

import sys, getopt, random
import time
import errno

inputFilename = ''
queryIDs = dict()
minIdentity = 90
minLength = 0.9
min2Identity = 75
min2Length = 0.75

try:
	opts, args = getopt.getopt(sys.argv[1:],"hf:i:l:")
except getopt.GetoptError:
	print "Option not recognised, -h for help."
	print "AMRReporter.py -f <input filename>  -i <min identity (%) for hit> -l <min length (proportion of ref) for hit>" 
	sys.exit()
for opt, arg in opts:
	if opt == "-h":
		print "AMRReporter.py -f <input filename>  -i <min identity (%) for hit> -l <min length (proportion of ref) for hit>"
		print ""
		print "Writes out a list of all ref sequences found in each query sequence, with minimum alignment length and identity as specified.\
The input file should be a TSV alignment file in the format:\n\t <query name> \t <ref name> \t <identity> \t <alignment length> \t <query length> \t <ref length>\n\
e.g.. a BLAST file in the above format of query sequences against a gene database. The output would then indicate the genes that are found in each sequence."
		sys.exit()
	elif opt in ("-f"):
		inputFilename = arg
	elif opt in ("-i"):
		minIdentity = float(arg)
	elif opt in ("-l"):
		minLength = float(arg)

try:
	with open(inputFilename, 'r') as inputFile:
		for line in inputFile:
			fields = line.split()
			queryName 		= fields[0]
			refName 		= fields[1]
			identity 		= float(fields[2])
			alignmentLength = int(fields[3])
			queryLength 	= int(fields[4])
			refLength 		= int(fields[7])

			if not queryName in queryIDs:
				queryIDs[queryName] = list()
			if not refName in queryIDs[queryName]:
				lengthProp = alignmentLength / refLength
				if identity >= minIdentity and lengthProp >= minLength:
					queryIDs[queryName].append(refName)
except (OSError, IOError) as e: 
	if getattr(e, 'errno', 0) == errno.ENOENT:
		print "Could not open file " + readIDFilename
		sys.exit(2)

for key, value in queryIDs.items():
	value.append("-------75%--90%--------")

try:
	with open(inputFilename, 'r') as inputFile:
		for line in inputFile:
			fields = line.split()
			queryName 		= fields[0]
			refName 		= fields[1]
			identity 		= float(fields[2])
			alignmentLength = int(fields[3])
			queryLength 	= int(fields[4])
			refLength 		= int(fields[7])

			if not refName in queryIDs[queryName]:
				lengthProp = alignmentLength / refLength
				if identity >= min2Identity and lengthProp >= min2Length:
					queryIDs[queryName].append(refName)
except (OSError, IOError) as e: 
	if getattr(e, 'errno', 0) == errno.ENOENT:
		print "Could not open file " + readIDFilename
		sys.exit(2)

for key, value in queryIDs.items():
	hitsList = ""
	for ref in value:
		hitsList += ref + ", "
	print key + " , " + hitsList + "\n"





