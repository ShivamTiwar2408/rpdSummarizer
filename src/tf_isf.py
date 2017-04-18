import xml.etree.ElementTree as ET
import re
import math
import decimal


tf_isf_feature = []

def tf_isf(root,merge=0): 
	tfFinalList = []
	df_dictionary = {}
	idf_dictionary = {}
	doc_sent_count = []
	doc_count = 0
	sent_ids=[]
	for doc in root.iter('DOC'):
		tf_per_sent_list = []
		n_sentences = 0
		idlst=[]

		for text in doc.iter('Text'):
			for sentence in text.iter('Sent'):
				id=sentence.attrib['id']
				idlst.append(id)
				n_sentences = n_sentences + 1
				tf_sent_dict = {}
				sentence.text = sentence.text.lower()
				words = sentence.text.split(' ')
				for i in words:
					m = re.search("[a-z]+",i)
					if m != None:
						keyword = m.group()
						if keyword in tf_sent_dict:
							tf_sent_dict[keyword] = tf_sent_dict[keyword] + 1
						else:
							tf_sent_dict.update({keyword:1})
				tf_per_sent_list.append(tf_sent_dict)

		sent_ids.append(idlst)#sentence ids 

		tfFinalList.append(tf_per_sent_list)
		doc_sent_count.append(n_sentences)
	
	for sent_list in tfFinalList:
		for dicts in sent_list:
			maxtf = 0
			for w in dicts:
				if dicts[w] > maxtf:
					maxtf = dicts[w]
			for w in dicts:
				dicts[w] = dicts[w] / float(maxtf)
	
	sf_list = []
	
	for sent_list in tfFinalList:
		sf = {}
		for dicts in sent_list:
			for w in dicts:
				if w in sf:
					sf[w] = sf[w] + 1
				else:
					sf.update({w:1})								
		sf_list.append(sf)
	
	isf_list = []
	
	id = 0
	for dict1 in  sf_list:
		isf_dict = {}
		for w in dict1:
			isf = 0
			val1 = doc_sent_count[id] / float(1 + dict1[w])
			if val1 > 0:
				isf = math.log(val1 , 10)
			
			isf_dict.update({w:isf})
		id = id + 1		
		isf_list.append(isf_dict)
		
		
	#print isf_list[0]
	
	id = 0
	for doc in tfFinalList:
		for sentdic in doc:
			for w in sentdic:
				isf_dict = isf_list[id]
				if w in isf_dict:
					sentdic[w] = sentdic[w] * isf_dict[w]
				else:
					sentdic[w] = 0	
	id = id + 1
					
	#print tfFinalList[0]				
	#print sf_list[1]	
	#print tfFinalList[0]
	if merge==0:
		return tfFinalList,sent_ids	
	else:
		ans={}
		#tf_isf_feature
		#[[{},{},{}..],[],[],..]
		#list which contains list of dictionaries.
		# the list represents a whole chunk
		# the sublist represent a doc
		# the dictionaries have (word:tf-isf) key-pair
		for i,doc in enumerate(tfFinalList):
			for j,sent in enumerate(doc):
				score=0
				l=len(sent)+1
				for key in sent.iterkeys():
					score+=sent[key] # add tf_isf of words
				score/=(l*1.0)
				ans[sent_ids[i][j]]=round(decimal.Decimal(score),4)

		return ans #sent-id : noralized total tf_isf score 



def tf_isf_main(filename):
	filepath="splitted/" + filename
	tree = ET.parse(filepath)
	root = tree.getroot()
	tf_isf_feature = tf_isf(root)
	#print "hello"
	#print tf_isf_feature
	

