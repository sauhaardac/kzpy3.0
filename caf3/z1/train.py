#! /usr/bin/python 
#//anaconda/bin/python

import caffe
from kzpy3.utils import *


solver_file_path = opjh("kzpy3/caf3/z1/solver.prototxt")
weights_file_path = opjD('z1/z1_iter_3000.caffemodel') #None #

os.chdir(home_path) # this is for the sake of the train_val.prototxt



def setup_solver():
	solver = caffe.SGDSolver(solver_file_path)
	for l in [(k, v.data.shape) for k, v in solver.net.blobs.items()]:
		print(l)
	for l in [(k, v[0].data.shape) for k, v in solver.net.params.items()]:
		print(l)
	return solver


def safe_solver_step(solver,n=100000):
    while True:
        try:
            solver.step(n)
        except Exception, e: 
            print e


if __name__ == '__main__':
	caffe.set_device(0)
	caffe.set_mode_gpu()
	solver = setup_solver()
	if weights_file_path != None:
		print "loading " + weights_file_path
		solver.net.copy_from(weights_file_path)
	solver.step(10000)
	#safe_solver_step(solver)
