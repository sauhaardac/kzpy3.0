from kzpy3.vis import *
import h5py

f = h5py.File(opjD("mytestfile.hdf5"), "w")

dset = f.create_dataset("mydataset", (100000,), dtype='f')

dset[...] = np.random.randn(100000)

hist(dset)