import math
import subprocess
from subprocess import Popen
from subprocess import call


# ********************************************
# FEATURES DOCUMENT/TERM-DEPENDANT
# ********************************************


# f1, f2, f3,f10,f11,f12,f46,f47,f48
def tf(doc,dumpIndexT):

	res = Popen(["grep","-e","^"+doc+" ",dumpIndexT],stdout=subprocess.PIPE).stdout.read()
	tRes = res.split(" ")
	if	(len(tRes) > 1):
		return [int(tRes[1]),math.log10(int(tRes[1])),int(tRes[2])]
	else :
		return [0,0,0]


# ********************************************
# FEATURES TERM-DEPENDANT
# ********************************************

# f4, f5, f6, f49, f50, f51
def idf(dumpIndexT,nbDocsIndex) :
	nbLines = Popen(["wc","-l",dumpIndexT],stdout=subprocess.PIPE).stdout.read()
	tLines = nbLines.split(" ")
	n = int(tLines[0]) - 1
	if n > 0 :
		return [nbDocsIndex/n,math.log10(nbDocsIndex/n)]
	else :
		return [0,0]

# ********************************************
# FEATURES FEAT-DEPENDANT
# ********************************************

# f7, f8, f9 , f22, f23, f24
def tfidf(tab,val):
	v = float(val[tab[0]]) * float(val[tab[1]])
	return [v,math.log10(v)]


# f13, f14, f15, f16, f17, f18,f19,f20,f21
def normalizedbysize(tab,val):
	
	return float(val[tab[0]]) / float(val[tab[1]])



# ********************************************
# FEATURES QUERY-DEPENDANT
# ********************************************

# f28 -> f45
def retevalmodel(param):
	
	print("[Start RetEval]")
	command = "/osirim/sig/CORPUS-TRAV/TREC-ADHOC/lemur-4.12/bin/RetEval"
	print(command+" "+param)
	call([command,param]) # Appel de retEval
	print("[RetEval ended]")


def runquerymodel(param, queryfile,resfile):
	
	print("[Start runquery]")
	command = "/osirim/sig/CORPUS-TRAV/TREC-ADHOC/indri-5.8/runquery/IndriRunQuery"
	print(command+" "+param+" "+queryfile+" > "+resfile)
	with open(resfile, "w") as outfile:
		call([command,param,queryfile],stdout=outfile) # Appel de Indrirunquery
	print("[runquery ended]")


