from glob import glob
import time
import easyocr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#from PIL import Image
from tqdm.notebook import tqdm
import matplotlib.patches as patches



plt.style.use('ggplot')
annot = pd.read_parquet('annot.parquet')
imgs = pd.read_parquet('img.parquet')
#img_fns = glob('train_val_images/train_images/*')
img_fns = glob('a/b/*')
#fig, ax = plt.subplots(figsize=(10, 10))
#ax.imshow(plt.imread(img_fns[0]))
#ax.axis('off')
#plt.show()
image_id = img_fns[0].split('/')[-1].split('.')[0]
annot.query('image_id == @image_id')
#fig, axs = plt.subplots(10, 10, figsize=(20, 20))
#axs = axs.flatten()
start_Time = time.time()
for i in range(100):
    img = plt.imread(img_fns[i])
    #axs[i].imshow(img)
    #axs[i].axis('off')
    image_id = img_fns[i].split('/')[-1].rstrip('.jpg')
    n_annot = len(annot.query('image_id == @image_id'))
    #axs[i].set_title(f'{image_id} - {n_annot}')
    # Read text from image
    reader = easyocr.Reader(['en'], gpu = False)
    start_Time = time.time()
    results = reader.readtext(img_fns[i])#,rotation_info=[90, 180 ,270])
    stop_Time = time.time()
    Timediff = stop_Time-start_Time
    print(Timediff)
    res = pd.DataFrame(results, columns=['bbox','text','conf'])
    

    #results = reader.readtext(img_fns[i])
    #res = pd.DataFrame(results, columns=['bbox','text','conf'])
    # Sort text by confidence and only keep text with a confidence greater than 0.5
    res = res.sort_values('conf', ascending=False)
    res = res[res['conf'] > 0.3]
    # Show image and draw bounding boxes around text
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(img)
    ax.axis('off')
    for bbox, text, conf in res[['bbox', 'text', 'conf']].values:
        x_min, y_min = bbox[0]
        x_max, y_max = bbox[2]
        rect = patches.Rectangle((x_min, y_min), x_max - x_min, y_max - y_min, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)
        ax.text(x_min, y_min - 10, f"{text} ({conf:.2f})", fontsize=10, color='r', ha='left', va='top')
    plt.show()
#img_fns = glob('train_val_images/train_images/*')
stop_Time = time.time()

run_Time =stop_Time-start_Time
print(round(run_Time,0))


