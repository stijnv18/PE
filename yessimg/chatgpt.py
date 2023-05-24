from glob import glob
import pandas as pd
import easyocr
import matplotlib.pyplot as plt

plt.style.use('ggplot')

# load annotations and image information
annot = pd.read_parquet('annot.parquet')
imgs = pd.read_parquet('img.parquet')
img_fns = glob('a/b/*')

# display first image
fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(plt.imread(img_fns[0]))
ax.axis('off')

# get image id from filename and query annotations
image_id = img_fns[0].split('/')[-1].split('.')[0]
annot.query('image_id == @image_id')

# display first 5 images with OCR results
fig, axs = plt.subplots(5, figsize=(20, 20))
results_list = []

for i in range(5):
    axs[i].imshow(plt.imread(img_fns[i]))
    axs[i].axis('off')
    
    image_id = img_fns[i].split('/')[-1].rstrip('.jpg')
    n_annot = len(annot.query('image_id == @image_id'))
    axs[i].set_title(f'{image_id} - {n_annot}')

    # perform OCR on image
    reader = easyocr.Reader(['en'], gpu=True)
    results = reader.readtext(img_fns[i])
    
    # filter OCR results by confidence threshold
    threshold = 0.5
    filtered_results = [result for result in results if result[2] >= threshold]
    res = pd.DataFrame(filtered_results, columns=['bbox', 'text', 'conf'])
    res['image_id'] = image_id
    results_list.append(res)
    print(res)

# concatenate OCR results and save to CSV file
all_results = pd.concat(results_list, ignore_index=True)
all_results.to_csv('ocr_results.csv', index=False)