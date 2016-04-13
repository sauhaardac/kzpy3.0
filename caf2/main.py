from argparse import ArgumentParser

#############################################################
#
if __name__ == '__main__':
	parser = ArgumentParser('Caffe model.\n')
	parser.add_argument("--model",type=str, help="--train")
	parser.add_argument("--define", action="store_true", help="--define")
	parser.add_argument("--train", type=int, help="--train")
	parser.add_argument("--test", type=int, help="--test")
	parser.add_argument("--latest", action="store_true", help="Load latest model")
	args = parser.parse_args()
	if args.model:
		exec("from kzpy3.caf2.models."+args.model+".model import *")
		print dis['model_name']
	if args.define:
		print('--define.')
		define()
	if args.train:
		print('--train.')
		solver = setup_solver(dis['model_name'])
		if args.latest:
			print('--latest')
			solver = load_latest(solver,dis['model_name'],'.caffemodel')
		collect_data()
		train_solver(solver,args.train)
	if args.test:
		solver = setup_solver(dis['model_name'])
		if args.latest:
			print('--latest')
			solver = load_latest(solver,dis['model_name'])
		collect_data()
		test_solver(solver,args.test)
#
#############################################################
