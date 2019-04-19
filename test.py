from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import logging
import os
import sys
import collections
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                    level=logging.INFO,
                    stream=sys.stdout)
import cv2
import numpy as np
import scipy as scp
import scipy.misc
import tensorflow as tf
import matplotlib.pyplot as plt
flags = tf.app.flags
FLAGS =flags.FLAGS

#sys.path.insert(1,'incl')

from incl.seg_utils import seg_utils as seg

try:
    import tensorvision.utils as tv_utils
    import tensorvision.core as core
except ImportError:
    logging.error("could not import the submodules.")
    logging.error("Please execute:"
                  "'git submodule update --init --recursive'")
    exit(1)



flags.DEFINE_string('logdir',None,'Path to logdir')
flags.DEFINE_string('input_image',None,'Image to apple KittiSeg.')
flags.DEFINE_string('output_image',None,'Image to apple KittiSeg.')


default_run = 'wy_2017_11_13_20.11' #change into your own model like KittiSeg_2017_12_12_08.30 
weights_url = ("ftp://mi.eng.cam.ac.uk/"
               "pub/mttt2/models/KittiSeg_pretrained.zip")

def maybe_download_and_extract(runs_dir):
    logdir = os.path.join(runs_dir,default_run)

    if os.path.exists(logdir):
        return
    if not os.path.exists(logdir):
        os.makedirs(runs_dir)
        download_name=tv_utils.download(weights_url,runs_dir)
        logging.info("Extracting KittiSeg_pretrained.zip")

        import zipfile
        zipfile.ZipFile(download_name,'r').extractall(runs_dir)
        return

def main(_):
    tv_utils.set_gpus_to_use()
    if FLAGS.input_image is None:
        logging.error("No input_image was given.")
        logging.info(
            "Usage: python demo.py --input_image data/test.png "
            "[--output_image output_image] [--logdir /path/to/weights] "
            "[--gpus GPUs_to_use] ")
        exit(1)

    if FLAGS.logdir is None:
        if 'TV_DIR_RUNS' in os.environ:
            runs_dir = os.path.join(os.environ['TV_DIR_RUNS'],'KittiSeg')

        else:
            runs_dir = 'RUNS'
        maybe_download_and_extract(runs_dir)
        logdir =os.path.join(runs_dir,default_run)
    else:
        logging.info("Using weights found in {}".format(FLAGS.logdir))
        logdir = FLAGS.logdir

    hypes = tv_utils.load_hypes_from_logdir(logdir, base_path='hypes')

    logging.info("Hypes loaded successfully.")

    # Loading tv modules (encoder.py, decoder.py, eval.py) from logdir
    modules = tv_utils.load_modules_from_logdir(logdir)
    logging.info("Modules loaded successfully. Starting to build tf graph.")

   #create tf graph and build net

    with tf.Graph().as_default():
        image_pl = tf.placeholder(tf.float32)
        image  = tf.expand_dims(image_pl,0)
        prediction =core.build_inference_graph(hypes,modules,image=image)

        logging.info("Graph build successfully.")

        sess = tf.Session()
        saver =tf.train.Saver()

        core.load_weights(logdir,sess,saver)
    input_image = FLAGS.input_image
    #logging.info("start inference using {} as input".format(input_image))

    cap=cv2.VideoCapture(0) #live camera and change as video path if you have save video 
    while True:
        #image_bgr = cv2.imread(input_image)
        #b, g, r = cv2.split(image_bgr)  # get b,g,r
        #image = cv2.merge([r, g, b])  # switch it to rgb
        ret,image =cap.read()

        if hypes['jitter']['reseize_image']:
            image_height = hypes['jitter']['image_height']
            image_width  = hypes['jitter']['image_width']
            image = scp.misc.imresize(image,size=(image_height,image_width),inerp ='cubic')

        feed ={image_pl:image}
        softmax = prediction['softmax']
        output =sess.run([softmax],feed_dict=feed)

    #reshape
        shape = image.shape
        output_image = output[0][:,1].reshape(shape[0],shape[1])

        rb_image =seg.make_overlay(image,output_image)
        threshold = 0.5

        street_prediction = output_image>threshold

        green_image = tv_utils.fast_overlay(image,street_prediction)
        cv2.imshow('ori',green_image)         #live camera: imshow or video:save
        if cv2.waitKey(25) & 0xFF == ord('q'):  #live camera imshow, delete if occur error in video show
            cv2.destroyAllWindows()
            break

   # cv2.imshow('road',green_image)

   # plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
   # plt.show()
   #cv2.waitKey()
   #cv2.destroyAllWindows()


if __name__ == '__main__':
    tf.app.run()