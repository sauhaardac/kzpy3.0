from kzpy3.utils import *
###########
'''
e.g.
from kzpy3.vis import *; kzpy_vis_test()
'''
################

import matplotlib.pyplot as plt  # the Python plotting package

PP,FF = plt.rcParams,'figure.figsize'


def kzpy_vis_test():
    img_dic = get_some_images()
    ppff = PP[FF]
    PP[FF] = 3,3
    mi(img_dic['bay'],'bay')
    PP[FF] = ppff
    plt.figure('hist')
    plt.hist(np.random.randn(10000),bins=100)
    True



# - These allow for real-time display updating
from cStringIO import StringIO
import scipy.ndimage as nd
import PIL.Image
from IPython.display import clear_output, Image, display
def showarray(a, fmt='jpeg'):
    a = np.uint8(np.clip(255.0*z2o(a), 0, 255))
    f = StringIO()
    PIL.Image.fromarray(a).save(f, fmt)
    display(Image(data=f.getvalue()))



def mi( image_matrix, figure_num = 1, subplot_array = [1,1,1], \
        img_title = '', img_xlabel = 'x', img_ylabel = 'y', cmap = 'gray', toolBar = False ):
    """My Imagesc, displays a matrix as grayscale image

        e.g.,

            from kzpy import *
            from kzpy.img import *
            mi(np.random.rand(256,256),99,[1,1,1],'random matrix')

    """
    if toolBar == False:
        plt.rcParams['toolbar'] = 'None'
    else:
        plt.rcParams['toolbar'] = 'toolbar2'

    f = plt.figure(figure_num)

    if True:
        f.subplots_adjust(bottom=0.05)
        f.subplots_adjust(top=0.95)
        f.subplots_adjust(wspace=0.1)
        f.subplots_adjust(hspace=0.1)
        f.subplots_adjust(left=0.05)
        f.subplots_adjust(right=0.95)
    if False:
        f.subplots_adjust(bottom=0.0)
        f.subplots_adjust(top=0.95)
        f.subplots_adjust(wspace=0.0)
        f.subplots_adjust(hspace=0.1)
        f.subplots_adjust(left=0.0)
        f.subplots_adjust(right=1.0)
    f.add_subplot(subplot_array[0],subplot_array[1],subplot_array[2])
    imgplot = plt.imshow(image_matrix, cmap)
    imgplot.set_interpolation('nearest')
    plt.axis('off')
    if len(img_title) > 0:# != 'no title':
        plt.title(img_title)


def mp(args,figure_num=1, subplot_array=[1,1,1],
       title='', xlabel='', ylabel='', xlim=[], ylim=[], toolBar=False):

    if toolBar == False:
        plt.rcParams['toolbar'] = 'None'
    else:
        plt.rcParams['toolbar'] = 'toolbar2'

    f = plt.figure(figure_num)

    if False:
        f.subplots_adjust(bottom=0.05)
        f.subplots_adjust(top=0.95)
        f.subplots_adjust(wspace=0.1)
        f.subplots_adjust(hspace=0.1)
        f.subplots_adjust(left=0.05)
        f.subplots_adjust(right=0.95)

    f.add_subplot(subplot_array[0],subplot_array[1],subplot_array[2])
    imgplot = plt.plot(*args)
    if len(title) > 0:# != 'no title':
        plt.title(title)
    else:
        plt.title(str(subplot_array[2]))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if len(xlim)==2:
        plt.xlim(xlim)    
    if len(ylim)==2:
        plt.ylim(ylim)


def yb_color_modulation_of_grayscale_image(img,y,b,opt_lower_contrast=True):

    if len(np.shape(img))>2:
        img = np.mean(img,axis=2)
    img = z2o(img)

    if opt_lower_contrast:
        print('low contrast option')
        img = (1.0+img)/3.0

    y = z2o(y)
    b = z2o(b)

    ci = np.zeros((np.shape(img)[0],np.shape(img)[1],3))
    print(np.shape(ci))
    for i in range(3):
        ci[:,:,i] = 1.0*img
    ci = ci/np.max(ci)

    for i in range(3):
        ci[:,:,i] *= (1-y)
    for i in [0,1]:
        ci[:,:,i] += y

    for i in range(3):
        ci[:,:,i] *= (1-b)
    for i in [2]:
        ci[:,:,i] += b
        
    return ci

    
 
def get_some_images():
    '''
    Load some images that can be used for demos, etc.
    e.g., img_dic = get_some_images(); mi(img_dic['bay'])
    '''
    img_dic = {}
    img_dic['bay'] = imread(opj(home_path,'Pictures','bay2.png'))
    return img_dic



# take an array of shape (n, height, width) or (n, height, width, channels)
# and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)
def vis_square(data_in, padsize=1, padval=0):
    data = data_in.copy()
    data -= data.min()
    data /= data.max()
    
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    
    return data