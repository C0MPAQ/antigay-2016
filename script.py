#!/usr/bin/python
import os
import numpy as np
#%matplotlib inline
import matplotlib.pyplot as plt
import argparse
import sys
import caffe

GPU_ID = 0
caffe.set_mode_gpu()
caffe.set_device(GPU_ID)


class NullWriter(object):
    def write(self, arg):
        pass

realstdout = sys.stdout
returnvalue = True

parser = argparse.ArgumentParser(description='Predicts age and sex of images.')
parser.add_argument("-nogay", help="return true if not male", action='store_true')
parser.add_argument("-nokids", help="return true if age > 12", action='store_true')
parser.add_argument("-nojailbait", help="return true if age > 18", action='store_true')
parser.add_argument("image", help="your input image", type=str)

args = parser.parse_args()

if not (args.nokids or args.nojailbait or args.nogay):
    print 'ERROR: need one of nogay nojailbait nokids'
    sys.exit(-1)

if not (args.image):
    print 'ERROR: Please supply an image'
    sys.exit(-1)

sys.stdout = NullWriter()

caffe_root = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, caffe_root + 'python')

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'


mean  = caffe.io.blobproto_to_array(caffe.io.caffe_pb2.BlobProto.FromString(open('./mean.binaryproto', "rb").read()))[0]

# if you get "Mean shape incompatible with input shape." Error, you have to fix the pycaffe library yourself
# See:
# http://stackoverflow.com/questions/30808735/error-when-using-classify-in-caffe

if args.nogay:
    gender_net = caffe.Classifier('./deploy_gender.prototxt', './gender_net.caffemodel',
                       mean=mean,
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))
if args.nokids or args.nojailbait:
    age_net = caffe.Classifier('./deploy_age.prototxt', './age_net.caffemodel',
                       mean=mean,
                       channel_swap=(2,1,0),
                       raw_scale=255,
                       image_dims=(256, 256))

#age_list=['(0, 2)','(4, 6)','(8, 12)','(15, 20)','(25, 32)','(38, 43)','(48, 53)','(60, 100)']
#gender_list=['Male','Female']

age_list=[0,4,8,15,25,38,48,60]
gender_list=[False,True]

input_image = caffe.io.load_image(args.image)

outstr = ""

if args.nokids or args.nojailbait:
    age = age_list[(age_net.predict([input_image])[0].argmax())]
    if age < 18 and args.nojailbait:
        returnvalue = False
    if age < 12 and args.nokids:
        returnvalue = False

#    outstr += "age >= "+str(age)+" "

if args.nogay:
    gender = gender_list[(gender_net.predict([input_image])[0].argmax())]
    if not gender:
        returnvalue = False

 #   outstr += "sex = "+("female" if gender else "male")+" "

sys.stdout = realstdout
#print args.image+" :: "+outstr

if returnvalue:
    sys.exit(0)
else:
    print args.image
    sys.exit(1)
