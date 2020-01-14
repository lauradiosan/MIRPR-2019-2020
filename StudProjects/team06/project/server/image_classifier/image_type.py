'''An enum for all the types of images the classifier can recognize.'''
from enum import Enum

class ImageType(Enum):
    """An enum for all the types of images the classifier can recognize.
    
    This has to be ordered."""
    FOREST = 0
    SAND_BEACH = 1
    SNOW_MOUNTAIN = 2
    OTHERS = 3
