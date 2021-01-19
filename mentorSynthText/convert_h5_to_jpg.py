import os
import sys
import h5py
import numpy as np
from PIL import Image


hdf = h5py.File(sys.argv[1],'r')
hdf_key = list(hdf.keys())[0]
print (hdf['data'])
data = list(hdf[hdf_key])
if not os.path.exists('output'):
    os.mkdir('output')
for i in data:
    print (f'[*]Processing {i}')
    array = hdf[hdf_key + "/" + i][:]
    img = Image.fromarray(array.astype('uint8'), 'RGB')
    img.save(os.path.join('output', os.path.splitext(i)[0] + '.jpg'), "JPEG")
    img.show()
