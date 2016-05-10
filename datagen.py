import en

rawdata = open("bigOlDictionary.txt")

chosenWords = {}
while True:
	word = rawdata.readline()
	if word == '':
		break
	word = word[:-1]
	if en.is_verb(word):
		if en.verb.infinitive(word) != '':
			chosenWords[en.verb.infinitive(word)] = en.verb.past_participle(en.verb.infinitive(word))

data = open("chosenWords.txt", 'w')
for word in chosenWords:
	data.write(word + ',' + chosenWords[word] + '\n')