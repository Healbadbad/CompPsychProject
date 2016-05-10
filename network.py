import numpy as np
import theano
import theano.tensor as T
import random
import lasagne
import warnings
warnings.filterwarnings('ignore', module='lasagne')

epochs = 20

in_layer = lasagne.layers.InputLayer(shape=(None, 19, 27)) # Arbitrary number of examples, 19 letters, 27 possibilities
H1_layer = lasagne.layers.DenseLayer(in_layer, 200, nonlinearity = lasagne.nonlinearities.sigmoid)
H2_layer = lasagne.layers.DenseLayer(H1_layer, 200, nonlinearity = lasagne.nonlinearities.sigmoid)
net = lasagne.layers.DenseLayer(H2_layer, 513, nonlinearity = lasagne.nonlinearities.sigmoid)

# Generate some data
net_output = lasagne.layers.get_output(net)
# As a loss function, we'll use Theano's squared error function.
# This should work fairly well for regression
true_output = T.ivector('true_output')
loss = T.mean(lasagne.objectives.squared_error(net_output, true_output))

# Retrieving all parameters of the network is done using get_all_params,
# which recursively collects the parameters of all layers connected to the provided layer.
all_params = lasagne.layers.get_all_params(net)
# Now, we'll generate updates using Lasagne's SGD function
# Finding a good learning rate is a challenge for large numbers since the squared error will explode
# if there is a large range, it should be processed to have a smaller range
updates = lasagne.updates.sgd(loss, all_params, learning_rate=0.2) 
# Finally, we can compile Theano functions for training and computing the output.
# Note that because loss depends on the input variable of our input layer,
# we need to retrieve it and tell Theano to use it.
train = theano.function([in_layer.input_var, true_output], loss, updates=updates)
get_output = theano.function([in_layer.input_var], net_output)

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

def thresh(vec):
    vec2 = []
    for item in vec:
        if item > 0.5:
            vec2.append(1)
        else:
            vec2.append(0)
    return vec2

datafile = open('chosenWords.txt')
X = []
Y = []

while True:
	line = datafile.readline()
	if line=='':		# EOF
		break
	base, future = line.split(',')
	if future == '':	# There were some problems with the library
		continue
	future = future[:-1] # Remove the newline
	X.append(wordToVec(base))
	Y.append(sum(wordToVec(future),[]))

train([wordToVec('yell')],sum(wordToVec('yelled'),[]))

for epic in range(epochs):
	print epic
	for index in range(len(X)):
		train([X[index]],Y[index])

# for index in range(len(X)):
# 	(get_output([wordToVec(X[index])],sum(wordToVec(Y[index]),[]))
print vecToWord(thresh(get_output([wordToVec('yell')])[0]))


# # Train the network
# for k in range(5): #number of epochs
# 	for k in range(samples):
# 		train([in_data[k]], [out_data[k]])

# # Test our network, overfitting isn't really a problem with 5 total nodes.
# print (get_output([[50,50]])) #Should be around 400
# print(net.W.get_value())
