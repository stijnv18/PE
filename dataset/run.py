from deeplake.transforms import ToFloat

ds = deeplake.load("hub://activeloop/coco-text-train")
dataloader = ds.pytorch(num_workers=0, batch_size=4, shuffle=False)

transform = ToFloat() # use the ToFloat transform directly

ds.visualize() # visualize the dataset
