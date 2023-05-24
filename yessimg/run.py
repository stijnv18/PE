from glob import glob

import easyocr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from tqdm.notebook import tqdm

plt.style.use('ggplot')
annot = pd.read_parquet('annot.parquet')
imgs = pd.read_parquet('img.parquet')
img_fns = glob('a/b/*')
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(plt.imread(img_fns[3]))
ax.axis('off')
# plt.show()
image_id = img_fns[0].split('/')[-1].split('.')[0]
annot.query('image_id == @image_id')
fig, axs = plt.subplots(5, 5, figsize=(20, 20))
axs = axs.flatten()
for i in range(113):
    axs[i].imshow(plt.imread(img_fns[i]))
    axs[i].axis('off')
    image_id = img_fns[i].split('/')[-1].rstrip('.jpg')
    n_annot = len(annot.query('image_id == @image_id'))
    axs[i].set_title(f'{image_id} - {n_annot}')
    reader = easyocr.Reader(['en'], gpu = True)
    results = reader.readtext(img_fns[i])
    res = pd.DataFrame(results, columns=['bbox','text','conf'])
    print(res)
img_fns = glob('train_val_images/train_images/copied_images/*')
plt.show()