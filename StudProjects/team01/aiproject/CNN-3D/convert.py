import os
import nibabel as nb
import numpy as np
from matplotlib.cm import get_cmap
from imageio import mimwrite
from skimage.transform import resize


def parse_filename(filepath):
    '''
    Parse input file path into directory, basename and extension.
    
    Parameters
    ----------
        - filepath: string
        Input name that will be parsed into directory, basename and extension.
    Returns:
    ----------
        - dirname: str
            File directory.
        - basename: str
            File name without directory and extension.
        - ext: str
            File extension.
    '''
    path = os.path.normpath(filepath)
    dirname = os.path.dirname(path)
    filename = path.split(os.sep)[-1]
    basename, ext = filename.split(os.extsep, 1)

    return dirname, basename, ext


def load_and_prepare_image(filename, size = 1):
    '''
    Load and prepare image data.
    
    Parameters
    ----------
        - filename1: str
            Input file (eg. /john/home/image.nii.gz)
        - size: float
            Image resizing factor.
    Returns
    ----------
        - out_img: numpy array
    '''
    # Load NIfTI file
    data = nb.load(filename).get_data()

    # Pad data array with zeros to make the shape isometric
    maximum = np.max(data.shape)

    out_img = np.zeros([maximum] * 3)

    a, b, c = data.shape
    x, y, z = (list(data.shape) - maximum) / -2

    out_img[int(x):a + int(x),
            int(y):b + int(y),
            int(z):c + int(z)] = data

    out_img /= out_img.max()        # scale image values between 0-1

    # Resize image by the following factor
    if size != 1:
        out_img = resize(out_img, [int(size * maximum)] * 3)

    maximum = int(maximum * size)

    return out_img, maximum


def create_mosaic_normal(out_img, maximum):
    '''
    Create grayscale image.
    
    Parameters
    ----------
        - out_img: numpy array
        - maximum: int
    Returns:
    ----------
        - new_img: numpy array
    '''
    new_img = np.array(
        [np.hstack((
            np.hstack((
                np.flip(out_img[i, :, :], 1).T,
                np.flip(out_img[:, maximum - i - 1, :], 1).T)),
            np.flip(out_img[:, :, maximum - i - 1], 1).T))
         for i in range(maximum)])

    return new_img


def write_gif_normal(filename, size = 1, fps = 18):
    '''
    Procedure for writing grayscale image.
    
    Parameters
    ----------
        - filename: str
            Input file (eg. /john/home/image.nii.gz).
        - size: float
            Between 0 and 1.
        - fps: int
            Frames per second.
    '''
    # Load NIfTI and put it in right shape
    out_img, maximum = load_and_prepare_image(filename, size)

    # Create output mosaic
    new_img = create_mosaic_normal(out_img, maximum)

    # Figure out extension
    ext = '.{}'.format(parse_filename(filename)[2])

    # Write gif file
    mimwrite(filename.replace(ext, '.gif'), new_img,
             format = 'gif', fps = int(fps * size))

    return filename.replace(ext, '.gif')

