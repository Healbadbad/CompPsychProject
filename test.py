import en

data = open('chosenWords.txt')

maxlenb = 0
maxlenf = 0
maxb = ''
maxf = ''


while True:
	line = data.readline()
	if line=='':		# EOF
		break
	base, future = line.split(',')
	if future == '':	# There were some problems with the library
		continue
	future = future[:-1] # Remove the newline
	if len(base) > maxlenb:
		maxlenb = len(base)
		maxb = base
	if len(future) > maxlenf:
		maxlenf = len(future)
		maxf = future


print maxb, maxlenb, maxf, maxlenf