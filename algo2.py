# Faraz Ahmad

# 2. Sentence selection based summarization using important words
import math
import sys
import glob
import operator


from stemming.porter2 import stem
# i got the above stemming lib from this download link
# https://pypi.python.org/pypi/stemming/1.0#downloads
# unzip the installation file and put the stemming folder 
# in Lib folder in your python installation directory



punc=(",./\;'?&-(){}|")

def suggestArticleTopic(filePath, stopwordsSet):
	tmpdt = {}
	fh = open(filePath)
	for line in fh:
		tmpline = line.translate(None, punc).strip()
		words = tmpline.split()
		for w in words:
			if w.lower() not in stopwordsSet:
				tmpdt[w] = tmpdt.get(w,0) + 1
	sorted_tmpdt = sorted(tmpdt.items(), key=operator.itemgetter(1), reverse=True)
	suggestedTitle = ""
	for i in range(0,10):
		suggestedTitle = suggestedTitle + sorted_tmpdt[i][0] + " "
	fh.close()
	# print suggestedTitle
	return suggestedTitle


def makeFreqDictionaryOfSentenceWords(s1):
	words1 = s1.split();
	dt1 = {}
	for w in words1:
		if w.lower() not in stopwords:
			dt1[stem(w.lower())] = dt1.get(stem(w.lower()),0) + 1
	return dt1

def computeCosineScore(dt1, dt2):
	score = 0
	
	# numerator a.b
	for k in dt1.keys():
		score = score + dt1[k]*dt2.get(k,0)

	# denominator |a||b|
	sq1 = 0
	sq2 = 0
	for k in dt1.keys():
		sq1 = sq1 + dt1[k]*dt1[k]

	for k in dt2.keys():
		sq2 = sq2 + dt2[k]*dt2[k]

	if sq1==0 or sq2==0:
		score = 0
	else:
		score = score / (math.sqrt(sq1)*math.sqrt(sq2))
	return score


folder_path = ""
if (len(sys.argv) == 2):
	folder_path = sys.argv[1]
else:
	print "Correct format of running this is assignment5algo2.py [space] folder_path"
	quit()

folders = folder_path.split("\\")
folder_path = ""
for w in folders:
	folder_path = folder_path + w + "\\"

# get stopwords in a set stopwords
stopwords = set()
fh = open('stopwords.txt')
for line in fh:
	stopwords.add(line.strip())
fh.close()



all_scores = []
all_lines = []
all_indices = []
all_fnames = []

for filename in glob.glob(folder_path + 'input*.txt'):
	# open file
	fh = open(filename)
	fnam = filename.split('\\')
	# get title of the input file
	articleName =  suggestArticleTopic(filename, stopwords)
	all_fnames.append(fnam[len(fnam)-1])
	tdt = makeFreqDictionaryOfSentenceWords(articleName)
	# read all lines
	scores = []
	lines = []
	for line in fh:
		lines.append(line)
		tmpline = line.translate(None, punc).strip()
		s1 = tmpline
		sdt = makeFreqDictionaryOfSentenceWords(s1)
		# print sdt
		# print tdt
		# compute score of each line
		scores.append(computeCosineScore(sdt, tdt))
	fh.close()
	all_lines.append(lines)
	all_scores.append(scores)
	all_indices.append( sorted(range(len(scores)), key=lambda k: scores[k], reverse=True) )
	
# select some top scoring lines to include in summary
c = 0
for val in all_lines:
	no_of_lines_in_doc = len(val)
	no_of_selected_lines = no_of_lines_in_doc * 0.4;
	outputSet = set()
	outputList = []
	tmp_indices = all_indices[c][:int(no_of_selected_lines)]
	tmp_indices = sorted(tmp_indices)
	for i in range(0, int(no_of_selected_lines)):
		if val[tmp_indices[i]] not in outputSet:
			outputSet.add(val[tmp_indices[i]])
			outputList.append(val[tmp_indices[i]])

	f = open('outputPart2' + all_fnames[c], 'w')
	c = c + 1; 
	for l in outputList:
		f.write(l)
	f.close()

