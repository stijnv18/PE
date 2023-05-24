import deeplake
ds = deeplake.load("hub://activeloop/coco-text-train")
dataloader = ds.pytorch(num_workers=0, batch_size=4, shuffle=False)