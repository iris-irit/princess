import sys,os
import pymongo
from pymongo import MongoClient
import numpy as np
import pprint
import operator



#collections = ["NP2003_50",'NP2004_50',"TD2003_50", 'TD2004_50', 'HP2003_50','HP2004_50','OHSUMED_50']
collections = ["NP2003_10", "NP2003_100", "NP2003_1000", "NP2004_10", "NP2004_100", "NP2004_1000", "HP2003_10", "HP2003_100", "HP2003_1000", "HP2004_10", "HP2004_100", "HP2004_1000", "TD2003_10", "TD2003_100", "TD2003_1000", "TD2004_10", "TD2004_100", "TD2004_1000", "OHSUMED_10", "OHSUMED_100", "OHSUMED_1000"]

combinateurs = ["RRF", "Borda", "Combsum","Combmnz"]


	
def generate_file(c,f,n): 
	# ********************************************
	# Pour une feature argv[1] et une collection argv[2] passees en parametre, 
	# renvoie un fichier argv[3] au format trev_eval contenant les documents tries selon feature par requete
	# ********************************************

	
	def isDocOk(q,d,c):
		pathBest = "/projets/iris/PROJETS/PRINCESS/code/tools/best_competitors_letor/"+c.upper()+"/docs/"+q+".txt"
		tab = []
		with open(pathBest,"r") as file :
			for l in file:
				tab.extend(l.split(" "))
			#print tab
			#sys.exit()
		return d in tab

	# ********************************************
	# CONNEXION DANS MONGODB
	# ********************************************

	collection_name = c.lower()
	feature = f
	fileout_name = n

	connection = MongoClient(host='co2-ni01.irit.fr',port=28018)
	db = connection.princess
	collection = db[collection_name]
	print collection_name
	queries = collection.distinct('query')
	print queries
	for q in queries:
		print q
		valFeatures = {}
		# la requete qui liste tous les documents 
		list = collection.find({'query':q},{'_id':0,'docs':1})
		for d in list[0]['docs'] :
			#print d
			if len(valFeatures)  < 50 :
				#if isDocOk(q,d['doc_name'],c):
					#print "ok"
					#trouve = False
					#for f in d['features'] :
						#if f == feature:
							#trouve = True
							#valFeatures.setdefault(d['doc_name'], 0.0)
							#valFeatures[d['doc_name']] = d['features'][f]
					#if not trouve:
						#valFeatures.setdefault(d['doc_name'], 0.0)

				
				trouve = False
				for f in d['features'] :
					if f == feature:
						trouve = True
						valFeatures.setdefault(d['doc_name'], 0.0)
						valFeatures[d['doc_name']] = d['features'][f]
					if not trouve:
						valFeatures.setdefault(d['doc_name'], 0.0)


		sortedList = sorted(valFeatures.items(),key=operator.itemgetter(1), reverse=True)
		#for e in valFeatures:
		#	print e, valFeatures[e]

		print "****"

		with open(fileout_name, "a") as f:
			for i,e in enumerate(sortedList):
				print "************"
				f.write(q+" Q0 "+e[0]+" "+str(i+1)+" "+str(e[1])+" "+feature+"\n")


for col in collections:
	dirCol = "/projets/iris/PROJETS/PRINCESS/results_is/combinateurs/"+col
	#os.system("rm -r "+dirCol)
	#os.system("mkdir "+dirCol)
	print col
	if "OHS" in col:
		for el in ["f"+str(i) for i in range(1,46)]:
			print el
			generate_file(col,el,dirCol+'/'+el+".txt")
		param = " ".join([dirCol+'/f'+str(i)+".txt" for i in range(1,46)])
		for comb in combinateurs :
			print comb
			command = "/logiciels/java1.8/bin/java Main -combinateur "+comb+" -runs "+param+" >  "+"/projets/iris/PROJETS/PRINCESS/results_is/combinateurs/"+col+"/"+comb+".txt"
			print command
			os.system(command)
	else : 
		for el in ["f"+str(i) for i in range(1,65)]:
			print el
			generate_file(col,el,dirCol+'/'+el+".txt")
		param = " ".join([dirCol+'/f'+str(i)+".txt" for i in range(1,65)])
		for comb in combinateurs :
			print comb
			command = "/logiciels/java1.8/bin/java Main -combinateur "+comb+" -runs "+param+" >  "+"/projets/iris/PROJETS/PRINCESS/results_is/combinateurs/"+col+"/"+comb+".txt"
			print command
			os.system(command)






