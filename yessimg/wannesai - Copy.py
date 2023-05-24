from glob import glob
import time
import easyocr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from tqdm.notebook import tqdm
import matplotlib.patches as patches

plt.style.use('ggplot')
annot = pd.read_parquet('annot.parquet')
imgs = pd.read_parquet('img.parquet')
img_fns = glob('copied_images/*')
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
    reader = easyocr.Reader(['en'], gpu = True)
    results = reader.readtext(img_fns[i])
    res = pd.DataFrame(results, columns=['bbox','text','conf'])

    # Sort text by confidence and only keep text with a confidence greater than 0.5
    res = res.sort_values('conf', ascending=False)
    res = res[res['conf'] > 0.5]

    # Show image with bounding boxes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    ax1.imshow(img)
    ax1.axis('off')
    print(res)
    for j, row in res.iterrows():
        bbox = row['bbox']
        text = row['text']
        conf = row['conf']
        color = plt.cm.get_cmap('hsv')(j/len(res))
        
        # Draw bounding box on image
        x_min, y_min = bbox[0]
        x_max, y_max = bbox[2]
        rect = patches.Rectangle((x_min, y_min), x_max-x_min, y_max-y_min, linewidth=1, edgecolor=color, facecolor='none')
        ax1.add_patch(rect)
        
        # Add text to the right of the image
        ax2.text(0, 1.0-(j/30), f"{text} ({conf:.2f})", fontsize=10, color=color, ha='left', va='center')
        ax2.axis('off')

    plt.subplots_adjust(wspace=0.05)
    plt.show()
#img_fns = glob('train_val_images/train_images/*')
stop_Time = time.time()

run_Time =stop_Time-start_Time
print(round(run_Time,0))
