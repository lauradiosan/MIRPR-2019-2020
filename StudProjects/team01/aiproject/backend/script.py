import nibabel as nib
import numpy as np
from PIL import Image
# Get nibabel image object
img = nib.load("1.nii")

# Get data from nibabel image object (returns numpy memmap object)
img_data = img.get_data()
# Convert to numpy ndarray (dtype: uint16)
img_data_arr = np.asarray(img_data)
img = Image.fromarray(img_data_arr[:,:,0], 'L')
img.save("image.jpeg")