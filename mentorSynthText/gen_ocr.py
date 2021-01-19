# Author: Ankush Gupta
# Date: 2015

"""
Entry-point for generating synthetic text images, as described in:

@InProceedings{Gupta16,
      author       = "Gupta, A. and Vedaldi, A. and Zisserman, A.",
      title        = "Synthetic Data for Text Localisation in Natural Images",
      booktitle    = "IEEE Conference on Computer Vision and Pattern Recognition",
      year         = "2016",
    }
"""

import numpy as np
import h5py
import os, sys, traceback
import os.path as osp
from synthgen_ocr import *
from common import *
import wget, tarfile
import colorama
from PIL import Image


colorama.init()

## Define some configuration variables:
NUM_IMG = -1 # no. of images to use for generation (-1 to use all available):
SECS_PER_IMG = 5 #max time per image in seconds

# path to the data-file, containing image, depth and segmentation:
DATA_PATH = 'data'
DB_FNAME = osp.join(DATA_PATH,'bg_img')
# url of the data (google-drive public file):
DATA_URL = 'http://www.robots.ox.ac.uk/~ankush/data.tar.gz'


def add_res_to_db(imgname,res,db,args):
  """
  Add the synthetically generated text image instance
  and other metadata to the dataset.
  """
  ninstance = len(res)
  for i in range(ninstance):
    dname = "%s_%d"%(imgname, i)
    db['data'].create_dataset(dname,data=res[i]['img'])
    # db['data'][dname].attrs['charBB'] = res[i]['charBB']
    db['data'][dname].attrs['wordBB'] = res[i]['wordBB']

    L = res[i]['txt']
    L = [n.encode("ascii", "ignore") for n in L]
    db['data'][dname].attrs['txt'] = L
    # save image
    im = Image.fromarray(res[i]['img'])
    im.save(args.IMAGE_FOLDER + dname + '.jpg')


def main(args):
  # open databases:
  print (colorize(Color.BLUE,'getting data..',bold=True))

  # open the output h5 file:
  out_db = h5py.File(args.OUT_FILE,'w')
  out_db.create_group('/data')
  print (colorize(Color.GREEN,'Storing the output in: '+args.OUT_FILE, bold=True))

  # get the names of the image files in the dataset:
  imnames = os.listdir(DB_FNAME)
  N = len(imnames)
  global NUM_IMG
  if NUM_IMG < 0:
    NUM_IMG = N
  start_idx,end_idx = 0,min(NUM_IMG, N)

  RV3 = RendererV3(DATA_PATH,max_time=SECS_PER_IMG)

  for i in range(start_idx,end_idx):
    imname = imnames[i]
    impath = os.path.join(DB_FNAME, imname)
    try:
      # get the image:
      img = np.array(Image.open(impath))
      # re-size uniformly:
      sz = img.shape[:2] #(417, 1071) basically the size of the image being passed in
      print (f'[*]SZ: {sz}') #edited in sz print statement
      img = img[:,:,:3]
      # get the pre-computed depth:
      depth = np.ones(sz)
      # get segmentation:
      seg = np.ones(sz).astype('float32') #mask the size of the entire image being passed in
      # area = np.array([(sz[0] * sz[1])//2, (sz[0] * sz[1])//2]) #original
      area = seg #edited to force area and seg (which is basically a mask of the whole image)
      label = np.array([1])

      print (colorize(Color.RED,'%d of %d'%(i,end_idx-1), bold=True))
      res = RV3.render_text(img,depth,seg,area,label,
                            ninstance=args.INSTANCE_PER_IMAGE,viz=args.viz)
      if len(res) > 0:
        # non-empty : successful in placing text:
        add_res_to_db(imname[:-4],res,out_db,args)
        print ("[+]Placed text")
      # visualize the output:
      else:
        print ('[-]Could not place text')
      if args.viz:
        print (colorize(Color.RED,'continue? (enter to continue, q to exit): ',True), end='')
        if 'q' in input():
          break
    except:
      traceback.print_exc()
      print (colorize(Color.GREEN,'>>>> CONTINUING....', bold=True))
      continue
  out_db.close()


if __name__=='__main__':
  import argparse
  parser = argparse.ArgumentParser(description='Genereate Synthetic Scene-Text Images')
  parser.add_argument('--viz',action='store_true',dest='viz',default=True,help='flag for turning on visualizations')
  parser.add_argument('--INSTANCE_PER_IMAGE',default=1,type=int,help='no. of times to use the same image')
  parser.add_argument('--OUT_FILE',default='results/st_5by7.h5',type=str,help='path to store output dataset .h5')
  parser.add_argument('--IMAGE_FOLDER',default='results/images/',type=str,help='path to store images')
  args = parser.parse_args()
  main(args)
