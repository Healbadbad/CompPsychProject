
def wordToVec(word):
	''' convert the word to a one-of-n feature vector'''
	vec = []

	for letter in word:
		subvec = []
		for k in range(27):
			if ord(letter)-96 == k:
				subvec.append(1)
			else:
				subvec.append(0)
		vec.append(subvec)

	#Fill in the rest of the empty letters
	for k in range(19-len(word)):
		subvec = [1]
		for k in range(26):
			subvec.append(0)
		vec.append(subvec)
	return vec	

def vecToWord(vec):
	word = ''
	for k in range(19):
		for i in range(27):
			if vec[k*27 + i] == 1:
				word = word + chr(i+96)
				break
	return word

print(len(wordToVec('`abcdefg')))

print("\n")

print(sum(wordToVec('`abcdefg'), []))


print(vecToWord(sum(wordToVec('`abcdefg'), [])))