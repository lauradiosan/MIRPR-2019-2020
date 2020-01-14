# Useful stuff that I wish I knew 3 days ago
# Documentation nibabel - https://nipy.org/nibabel/nibabel_images.html
# Some tutorial for preparing custom data for CNN - https://www.youtube.com/watch?v=j-3vuBynnOE&list=PLQVvvaa0QuDfhTox0AjmQ6tvTgMBZBEXN&index=2
# Some tutorial for CNN - https://www.youtube.com/watch?v=WvoLTXIjBYU&list=PLQVvvaa0QuDfhTox0AjmQ6tvTgMBZBEXN&index=3

import os
import numpy as np
import nibabel as nib
from nibabel.testing import data_path
import matplotlib.pyplot as plt
import cv2
import random
import pickle
import numpy as np
from nilearn.image import resample_img
from nibabel.viewers import OrthoSlicer3D
import nibabel as nib



DATADIR = "simple_data"
CATEGORIES = ["HCM", "NOR","DCM","RV","MINF"]
IMG_SIZE = 256

training_data = []



def rescale_affine(input_affine, voxel_dims=[1, 1, 1], target_center_coords=None):
    '''
    This function uses a generic approach to rescaling an affine to arbitrary
    voxel dimensions. It allows for affines with off-diagonal elements by
    decomposing the affine matrix into u,s,v (or rather the numpy equivalents)
    and applying the scaling to the scaling matrix (s).

    Parameters
    ----------
	    - input_affine : np.array of shape 4,4
	        Result of nibabel.nifti1.Nifti1Image.affine
	    - voxel_dims : list
	        Length in mm for x,y, and z dimensions of each voxel.
	    - target_center_coords: list of float
	        3 numbers to specify the translation part of the affine if not using the same as the input_affine.

    Returns
    ----------
	    - target_affine : 4x4 matrix
	        The resampled image.
    '''
    # Initialize target_affine
    target_affine = input_affine.copy()
    # Decompose the image affine to allow scaling
    u, s, v = np.linalg.svd(target_affine[:3, :3], full_matrices=False)

    # Rescale the image to the appropriate voxel dimensions
    s = voxel_dims

    # Reconstruct the affine
    target_affine[:3, :3] = u @ np.diag(s) @ v

    # Set the translation component of the affine computed from the input
    # image affine if coordinates are specified by the user.
    if target_center_coords is not None:
        target_affine[:3, 3] = target_center_coords

    return target_affine


def resize_nii_files(nii):
	'''
	Resizing a nifty image.
	
	Parameters
    ----------
		- nii, nifty image
	Returns
    ----------
		- nifty image, the newly interpolated nifty image
	'''
	img_data = np.array(nii.dataobj)
	img_shape = nii.shape

	target_shape = np.array((256, 256, 10))
	new_affine = rescale_affine(nii.affine, [target_shape[0]/img_shape[0], target_shape[1]/img_shape[1], target_shape[2]/img_shape[2]])

	new_img = resample_img(nii, target_affine=new_affine, target_shape=target_shape, interpolation='linear')
	new_img_data = np.array(new_img.dataobj)

	return new_img_data


def create_training_data():
	'''
	Creating the list with the training data. 
	
	Returns
    ----------
		- list, 
			The training_data list with data in it.
	'''
	for category in CATEGORIES:
		path = os.path.join(DATADIR, category)
		class_num = CATEGORIES.index(category)
		for img in os.listdir(path):
			try:
				img_path = os.path.join(path, img)
				img_nii = nib.load(img_path)
				aux = resize_nii_files(img_nii)
				img_array = np.array(aux)
				new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
				training_data.append([new_array, class_num])
			except Exception as e:
				print("=== Ai o exceptie - ", e)
	random.shuffle(training_data)


def save_data():
	'''
	Saves the training data in 2 pickle files.
	
	Output 
    ----------
		- 2 pickle files, X.pickle and y.pickle with the corresponding
			features (X.pickle) and labels (y.pickle) 
	'''
	X = []
	y = []

	for features, label in training_data:
		X.append(features)
		y.append(label)

	X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 10)

	pickle_out = open("X.pickle", "wb")
	pickle.dump(X, pickle_out)
	pickle_out.close()

	pickle_out = open("y.pickle", "wb")
	pickle.dump(y, pickle_out)
	pickle_out.close()


def load_data():
	'''
	Loading the data from the pickle files. 
	
	Returns  
    ----------
		- one array with the training images
		- one array with the training labels corresponding to the above images
		- one array with the testing images
		- one array with the testing labels corresponding to the above images
	'''
	train_images = pickle.load(open("X.pickle", "rb")) 
	train_labels = pickle.load(open("y.pickle", "rb")) 
	test_images = pickle.load(open("X.pickle", "rb")) 
	test_labels = pickle.load(open("y.pickle", "rb"))

	train_images = np.array(train_images)
	train_labels = np.array(train_labels)

	testing_coeficient = len(train_images) // 5			   		# 20% from the train data 
	test_images = np.array(test_images[0:testing_coeficient])
	test_labels = np.array(test_labels[0:testing_coeficient])

	train_labels = train_labels.reshape((len(train_labels), 1))
	test_labels = test_labels.reshape((len(test_labels), 1))
	
	return (train_images, train_labels), (test_images, test_labels)