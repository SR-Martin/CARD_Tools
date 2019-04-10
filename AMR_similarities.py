#!/usr/bin/python

import sys, getopt, random
import time
import errno

geneNames = [ 	"ACT-15", "ACT-16", "ACT-17", "ACT-18", "ACT-20", "ACT-22", "ACT-23", "ACT-24", "ACT-25", "ACT-27", "ACT-31", "ACT-32",
				"ACT-33", "ACT-36", "ACT-37", "ACT-5", "ACT-7", "CMY-104", "MIR-11", "OXA-2", "blaZ", "SHV-104", "SHV-107", "SHV-109",
				"SHV-122", "SHV-14", "SHV-150", "SHV-157", "SHV-178", "SHV-186", "SHV-188", "SHV-31", "SHV-35", "SHV-36", "SHV-43", 
				"SHV-52", "SHV-61", "SHV-63", "SHV-80", "SHV-85", "SHV-94", "mecA", "mecC", "mecR1", 

				"acrA", "acrB", "acrD", "acrE", "acrF", "acrS", "adiY", "amrB", "baeR", "baeS", "cpxA", "cpxR", "CRP", "emeA",
				"emrA", "emrB", "emrD", "emrE", "emrK", "emrR", "emrY", "evgA", "evgS", "fyuA", "gadE", "gadW", "gadX", "H-NS",
				"kdpE", "IsaE", "marA", "mdfA", "mdtA", "mdtB", "mdtC", "mdtD", "mdtE", "mdtF", "mdtG", "mdtH","mdtL", "mdtM",
				"mdtN", "mdtO", "mdtP", "mepA", "mexB", "mexD", "mexF", "mexK", "mexN", "mexQ", "mgrA", "norA", "qacA", "ramA",
				"robA", "smeB", "smeE", "tolC", "vgaC",

				 "alaS", "cysB", "parY", "AAC(6')-Ib", "AAC(6')-Ib7", "AAC(6')-Ie", "aad(6)", "aadA", "aadA21", "aadA24", "ANT(4')-Ib",
				 "APH(3')-IIIa", "bacA", "arnA", "PmrB", "PmrC", "PmrE", "PmrF", "mphC", "patA", "oqxA", "oqxB", "FosA2", "FosA5", 
				 "fusB", "tlrC", "ileS", "mfd", "QnrB36", "sat-4", "leuO", "sul1", "tetK", "tetL", "tetM", "dfrA14", "dfrC", "dfrE",
				 "vanRG" ]

class geneIdentity:
	def __init__(self, queryName, refName, identity):
		self.queryName = queryName
		self.refName = refName
		self.identity = str(identity)


#make a list of query names containing the genes we're interested in
inputFilename = "CARD_VS_CARD.out"
outputFilename = "gene_identities_table.txt"
queryNames = list()
geneIdentities = list()
try:
	with open(inputFilename, 'r') as inputFile:
		for line in inputFile:
			fields = line.split()
			queryName = fields[0]
			queryGene = (queryName.split("|")[5]).strip()
			if queryGene in geneNames and not queryName in queryNames:
				queryNames.append(queryName)

			#for gene in geneNames:
			#	if gene in queryName and not queryName in queryNames:
			#		queryNames.append(queryName)

		inputFile.seek(0)
		for line in inputFile:
			fields = line.split()
			queryName = fields[0]
			refName = fields[1]
			identity = fields[2]
			if queryName in queryNames and refName in queryNames:
				geneIdentities.append(geneIdentity(queryName, refName, identity))

except (OSError, IOError) as e: 
	if getattr(e, 'errno', 0) == errno.ENOENT:
		print "Could not open file " + inputFilename
		sys.exit(2)

#queryNames.sort(key = lambda x: x.split('|')[5])

queryNamesSorted = list()

for gene in geneNames:
	for query in queryNames:
		queryGene = (query.split("|")[5]).strip()
		if queryGene == gene:
			queryNamesSorted.append(query)

print str(len(queryNames)) + ", " + str(len(queryNamesSorted))
assert(len(queryNames) == len(queryNamesSorted))
queryNames = queryNamesSorted
queryDict = dict()
count = 0
for query in queryNamesSorted:
	queryDict[query] = count
	count += 1

n = len(queryNamesSorted)
identities = [[0 for x in range(n)] for y in range(n)]

for geneIdentity in geneIdentities:
	i = queryDict[geneIdentity.queryName]
	j = queryDict[geneIdentity.refName]
	identities[i][j] = geneIdentity.identity


try:
	with open(outputFilename, 'w') as outputFile:
		line = "------------------------\t -----"
		for query in queryNamesSorted:
			line += "\t"
			line += query.split('|')[5]
		line += "\n"
		outputFile.write(line)
		for i in range(n):
			line = queryNamesSorted[i] + "\t" + queryNamesSorted[i].split('|')[5]
			for j in range(n):
				line += "\t"
				line += str(identities[i][j])
			line +="\n"
			outputFile.write(line)

except (OSError, IOError) as e: 
	if getattr(e, 'errno', 0) == errno.ENOENT:
		print "Could not open file " + outputFilename
		sys.exit(2)






