# Simple "digit recognition" example for neural networks and OpenCV
#

import numpy
import cv2

# Input vectors for neural network. Spaces correspond to zeros,
# non-spaces to ones.  There are 10 inputs, each corresponding to a
# digit, and 10 outputs. The hope is to match each input to the
# correct output.
input_strings = [

    'XXX' + \
    'X X' + \
    'X X' + \
    'X X' + \
    'XXX',

    'XX ' + \
    ' X ' + \
    ' X ' + \
    ' X ' + \
    'XXX',

    'XXX' + \
    '  X' + \
    'XXX' + \
    'X  ' + \
    'XXX',

    'XXX' + \
    '  X' + \
    'XXX' + \
    '  X' + \
    'XXX',

    'X X' + \
    'X X' + \
    'XXX' + \
    '  X' + \
    '  X',

    'XXX' + \
    'X  ' + \
    'XXX' + \
    '  X' + \
    'XXX',


    'XXX' + \
    'X  ' + \
    'XXX' + \
    'X X' + \
    'XXX',


    'XXX' + \
    '  X' + \
    '  X' + \
    '  X' + \
    '  X',


    'XXX' + \
    'X X' + \
    'XXX' + \
    'X X' + \
    'XXX',


    'XXX' + \
    'X X' + \
    'XXX' + \
    '  X' + \
    'XXX',

]

# The number of elements in an input vector, i.e. the number of nodes
# in the input layer of the network.
ninputs = len(input_strings[0])

# 8 hidden nodes.  If you change this to, for instance, 2, the network
# won't work well.
nhidden = 15

# We should have one output for each input vector (i.e., the digits
# 0-9).
noutput = len(input_strings)

# Create arrays for input and output. OpenCV neural networks expect
# each row to correspond to a single input or target output vector.
inputs = numpy.empty( (len(input_strings), len(input_strings[0])), 'float' )
targets = -1 * numpy.ones( (len(input_strings), len(input_strings)), 'float' )

# Convert input strings to binary zeros and ones, and set the output
# array to all -1's with ones along the diagonal.
for i in range(len(input_strings)):
    a = numpy.array(list(input_strings[i]))
    f = (a != ' ').astype('float')
    inputs[i,:] = f[:]
    targets[i,i] = 1

# Create an array of desired layer sizes for the neural network
layers = numpy.array([ninputs, nhidden, noutput])

# Create the neural network
nnet = cv2.ANN_MLP(layers)

# Some parameters for learning.  Step size is the gradient step size
# for backpropogation.
step_size = 0.001

# Momentum can be ignored for this example.
momentum = 0.0

# Max steps of training
nsteps = 80000

# Error threshold for halting training
max_err = 0.0000001

# When to stop: whichever comes first, count or error
condition = cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS

# Tuple of termination criteria: first condition, then # steps, then
# error tolerance second and third things are ignored if not implied
# by condition
criteria = (condition, nsteps, max_err)

# params is a dictionary with relevant things for NNet training.
params = dict( term_crit = criteria, 
               train_method = cv2.ANN_MLP_TRAIN_PARAMS_BACKPROP, 
               bp_dw_scale = step_size, 
               bp_moment_scale = momentum )

# Train our network
num_iter = nnet.train(inputs, targets,
                      None, params=params)

# Create a matrix of predictions
predictions = numpy.empty_like(targets)
#predictions = numpy.empty( (1 , 15), float)
x = numpy.array([[1.,1.,1.,1.,0.,1.,1.,1.,1.,1., 0.,1.,   1.,1.,1.],
                 [1.,1.,1.,1.,0.,1.,1.,1.,1.,1., 0.,1.,   1.,1.,1.],
                 [1.,1.,1.,1.,0.,1.,1.,1.,1.,1., 0.,1.,   1.,1.,1.],
                 [1.,1.,1.,1.,0.,1.,1.,1.,1.,1., 0.,1.,   1.,1.,1.],
                 [1.,1.,1.,1.,0.,1.,1.,1.,1.,1., 0.,1.,   1.,1.,1.],
                 [1.,1.,1.,1.,0.,1.,1.,1.,1.,1., 0.,1.,   1.,1.,1.],
                 [1.,1.,1.,1.,0.,1.,1.,1.,1.,1., 0.,1.,   1.,1.,1.],
                 [1.,1.,1.,1.,0.,1.,1.,1.,1.,1., 0.,1.,   1.,1.,1.],
                 [1.,1.,1.,1.,0.,1.,1.,1.,1.,1., 0.,1.,   1.,1.,1.],
                 [1.,1.,1.,1.,0.,1.,1.,1.,1.,1., 0.,1.,   1.,1.,1.]]) 
# See how the network did.
nnet.predict(x, predictions) #x = predictions
#y = numpy.array([1,1,1 ,1,0,1, 1,0,1, 1,1,1, 1,0,1]) 
# Compute sum of squared errors

sse = numpy.sum( (targets[0] - predictions)**2 )
print "----"
print targets[0]
print "----"
#sse =4
# Compute # correct
true_labels = numpy.argmax( targets, axis=0 )
pred_labels = numpy.argmax( predictions, axis=0 )
num_correct = numpy.sum( true_labels == pred_labels )

print 'ran for %d iterations' % num_iter
print 'inputs:'
print inputs
print 'targets:'
print targets
print 'predictions:'
print predictions
print 'sum sq. err:', sse
print 'accuracy:', float(num_correct) / len(true_labels)



print "----"
mn = 500
ind = -1
for i in range(len(targets)):
    x= numpy.sum( (targets[i] - predictions)**2 )
    if x<mn:
        mn = x
        ind = i
print "ZZZZZZ"
print mn,ind
print "----"
