from glob import glob
import torch
import easyocr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from tqdm.notebook import tqdm
import csv

print(torch.cuda.is_available())

plt.style.use('ggplot')

annot = pd.read_parquet('annot.parquet')
imgs = pd.read_parquet('img.parquet')
img_fns = glob('train_val_images/train_images/copied_images/*')

fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(plt.imread(img_fns[0]))
ax.axis('off')
# plt.show()

image_id = img_fns[0].split('/')[-1].split('.')[0]
annot.query('image_id == @image_id')

fig, axs = plt.subplots(10, 10, figsize=(20, 20))
axs = axs.flatten()
results_list = []

for i in range(5):
    axs[i].imshow(plt.imread(img_fns[i]))
    axs[i].axis('off')
    
    image_id = img_fns[i].split('/')[-1].rstrip('.jpg')
    n_annot = len(annot.query('image_id == @image_id'))
    axs[i].set_title(f'{image_id} - {n_annot}')
    
    reader = easyocr.Reader(['en'], gpu = True)
    results = reader.readtext(img_fns[i])
    
    threshold = 0.5
    filtered_results = []
    for result in results:
        if result[2] >= threshold:
            filtered_results.append(result)
    res = pd.DataFrame(filtered_results, columns=['bbox','text','conf'])
    res['image_id'] = image_id
    results_list.append(res)
    print(res)
all_results = pd.concat(results_list, ignore_index=True)
all_results.to_csv('ocr_results.csv', index=False)
    
img_fns = glob('train_val_images/train_images/copied_images/*')