#!/usr/bin/python

import sys, getopt, random
import time
import errno

class geneIdentity:
	def __init__(self, queryName, refName, identity):
		self.queryName = queryName
		self.queryAbbreviation = (queryName.split("|")[5]).strip()
		self.refName = refName
		self.refAbbreviation = (refName.split("|")[5]).strip()
		self.identity = identity

	def printIdentity(self):
		print self.queryAbbreviation + " " + self.refAbbreviation + " " + str(self.identity)

def getGroupString(group, name, fullSequenceName):
	geneString = ""
	count = 0
	for sequence in group:
		if count != 0:
			geneString += "\t"
		if fullSequenceName:
			geneString += sequence
		else:
			geneName = sequence.split("|")[5]
			assert(geneName != "")
			geneString += geneName
		count += 1
		geneString = geneString.replace("Streptomyces", "parY")
		geneString = geneString.replace("Bifidobacteria", "ileS")
	geneString += ""
	return name + "\t" + str(count) + "\t" + geneString + "\n"


geneNames = []
inputFilename = "CARD_VS_CARD.out"
geneNamesFilename = ""
ARONamesFilename = ""
outputGroupFilename = "groups.txt"
outputTSVFilename = "gene_identities_table.txt"
queryNames = list()
geneIdentities = list()
minIdentity = 80.0
printTSVFile = False
printGroupsOfOne = False
printFullSequenceNames = False

try:
	opts, args = getopt.getopt(sys.argv[1:],"hvsf:i:o:t:g:a:")
except getopt.GetoptError:
	print "Option not recognised. -h for help."
	print "AMR_gene_grouper.py  -f <blast filename> -g <genes filename> -a <ARO filename> -o <output file for groups>"
	sys.exit()
for opt, arg in opts:
	if opt == "-h":
		print "AMR_gene_grouper.py  -f <blast filename> -o <output file for groups>"
		print "Options:"
		print "	 -f <filename>     | name of file containing blast results"
		print "	 -g <filename>     | name of file containing a list of genes to compare"
		print "	 -a <filename>     | name of file containing and list of ARO numbers for genes to compare"
		print "	 -o <filename>     | name of file to write groups to"
		print "	 -t <filename>     | name of file to write tsv table of identities to"
		print "	 -i <min identity> | minimum identity to group genes together with (%)"
		print "	 -v                | print groups containing one gene"
		print "	 -s                | print full sequence names in group output "
		sys.exit()
	elif opt in ("-f"):
		inputFilename = arg
	elif opt in ("-i"):
		minIdentity = float(arg)
	elif opt in ("-o"):
		outputGroupFilename = arg
	elif opt in ("-t"):
		printTSVFile = True
		outputTSVFilename = arg
	elif opt in ("-g"):
		geneNamesFilename = arg
	elif opt in ("-v"):
		printGroupsOfOne = True
	elif opt in ("-a"):
		ARONamesFilename = arg
	elif opt in ("-s"):
		printFullSequenceNames = True

if ARONamesFilename and geneNamesFilename:
	print "Please provide either a file containing ARO numbers, or a file containing gene names (not both!)"
	sys.exit()

# Make a list of the ARO numbers to search the blast file with.
if ARONamesFilename:
	try:
		with open(ARONamesFilename, 'r') as AROListFile:
			for line in AROListFile:
				# bit of sanity checking?
				line = line.strip()
				geneNames.append(line)
	except (OSError, IOError) as e: 
		if getattr(e, 'errno', 0) == errno.ENOENT:
			print "Error: Could not open file " + ARONamesFilename
			sys.exit(2)

if geneNamesFilename:
	try:
		with open(geneNamesFilename, 'r') as geneListFile:
			for line in geneListFile:
				# bit of sanity checking?
				line = line.strip()
				geneNames.append(line)
	except (OSError, IOError) as e: 
		if getattr(e, 'errno', 0) == errno.ENOENT:
			print "Error: Could not open file " + geneNamesFilename
			sys.exit(2)

# Go through all the blast alignments and create a geneIdentity object for each alignment that
# contains genes with names from the list.
try:
	with open(inputFilename, 'r') as inputFile:
		currentAROs = list()
		warnedSequences = list()
		for line in inputFile:
			fields = line.split()
			sequenceName = fields[0]
			queryARO = sequenceName.split("|")[4]
			queryGene = sequenceName.split('|')[5]
			# Check that we haven't added this sequence name already
			if not sequenceName in queryNames:
				# Check that we don't already have a sequence with the same ARO
				if queryARO in currentAROs:
					if sequenceName not in warnedSequences:
						warnedSequences.append(sequenceName)
						print "Warning: Found multiple sequences for " + queryARO  + ". Ignoring sequence " + sequenceName
				else:
					if not geneNamesFilename and not ARONamesFilename:
						queryNames.append(sequenceName)
						currentAROs.append(queryARO)
					elif geneNamesFilename:
						if queryGene in geneNames:
							queryNames.append(sequenceName)
							currentAROs.append(queryARO)
					elif ARONamesFilename:
						if queryARO in geneNames:
							queryNames.append(sequenceName)
							currentAROs.append(queryARO)

		# Check to see if we have found every gene, give warning for ones that are missing
		for geneName in geneNames:
			found = False
			for queryName in queryNames:
				if ARONamesFilename:
					if geneName == queryName.split("|")[4].strip():
						found = True
						break
				elif geneNamesFilename:
					if geneName in queryName.split("|")[5]:
						found = True
						break
			if not found:
				print "Warning: Could not find sequence for " + geneName + "."

		inputFile.seek(0)
		for line in inputFile:
			fields = line.split("\t")
			queryName = fields[0]
			refName = fields[1]
			identity = fields[2]
			if queryName in queryNames and refName in queryNames:
				geneIdentities.append(geneIdentity(queryName, refName, float(identity)))

except (OSError, IOError) as e: 
	if getattr(e, 'errno', 0) == errno.ENOENT:
		print "Could not open file " + inputFilename
		sys.exit(2)

# Make a dictionary containing the gene names as keys and a unique index as a value.
queryDict = dict()
count = 0
for query in queryNames:
	queryDict[query] = count
	count += 1

# Make a matrix containing the identity of gene i and gene j.
n = len(queryNames)
identities = [[0 for x in range(n)] for y in range(n)]
for geneIdentity in geneIdentities:
	i = queryDict[geneIdentity.queryName]
	j = queryDict[geneIdentity.refName]
	# Some pairs of genes have multiple alignments(!?), take the best.
	if geneIdentity.identity > identities[i][j] and geneIdentity.identity > identities[j][i]:
		identities[i][j] = geneIdentity.identity
		identities[j][i] = geneIdentity.identity


# Sort the identities first by query and then by identity.
geneIdentities.sort(key=lambda x: (x.queryName, x.identity), reverse=True)

groups = list()

# Partition the genes into groups based on similarity.
# Note that the order in which this is done could change the groups - the groups are NOT uniquely determined. Other partitions may be possible.
for geneIdentity in geneIdentities:
	if geneIdentity.identity < minIdentity:
		continue
	# Add the query to a group if it's not in one already.
	newGroupForQuery = True
	newGroupForRef = True
	queryGroup = [geneIdentity.queryName]
	for group in groups:
		if geneIdentity.queryName in group:
			newGroupForQuery = False
			queryGroup = group
		if geneIdentity.refName in group:
			newGroupForRef = False

	if newGroupForRef:
		# Add the ref to the query group only if the identity of ref with the other group members is > minIdentity.
		refIdent = geneIdentity.identity
		refIndex = queryDict[geneIdentity.refName]
		canAddRef = True
		for member in queryGroup:
			memberIndex = queryDict[member]
			if identities[memberIndex][refIndex] < minIdentity or member == geneIdentity.refName:
				canAddRef = False
				break
		if canAddRef:
			queryGroup.append(geneIdentity.refName)

	if newGroupForQuery:
		groups.append(queryGroup)

# Dictionary with the groups as values and a unique name as key.
groupDict = dict()

# Make some group names.
for group in groups:
	if printGroupsOfOne or len(group) > 1:
		groupPrefix = ""
		for sequence in group:
			gene = sequence.split('|')[5]
			family = gene[:3]
			if family not in groupPrefix:
				if len(groupPrefix) > 0:
					groupPrefix += "-"
				groupPrefix += family
		counter = 1
		groupName = groupPrefix + "-" + str(counter)
		while groupName in groupDict.keys():
			counter += 1 
			groupName = groupPrefix + "-" + str(counter)
		assert(groupName not in groupDict.keys())
		groupDict[groupName] = group

# Print the groups that contain more than one gene
with open(outputGroupFilename, 'w') as groupFile:
	for name, group in groupDict.items():
		groupFile.write(getGroupString(group, name, printFullSequenceNames))

# Write a TSV file containing the matrix of group identities with appropriate headers.
# This can be imported into Excel.
if printTSVFile:
	try:
		with open(outputTSVFilename, 'w') as tsvFile:
			line = " Sequence Name\tGene"
			for group in groups:
				for gene in group:
					line += "\t"
					line += gene.split('|')[5]
			line += "\n"
			tsvFile.write(line)

			for group in groups:
				for gene in group:
					line = gene + "\t" + gene.split('|')[5]
					index1 = queryDict[gene]
					for group_2 in groups:
						for gene_2 in group_2:
							index2 = queryDict[gene_2]
							line += "\t"
							line += str(identities[index1][index2])
					line +="\n"
					tsvFile.write(line)

	except (OSError, IOError) as e: 
		if getattr(e, 'errno', 0) == errno.ENOENT:
			print "Could not open file " + outputFilename
			sys.exit(2)





