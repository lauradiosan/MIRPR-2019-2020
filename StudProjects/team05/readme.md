# Project Faraday

### A project that will bring safety down the streets of every city


## Project Purpose & Scope

<p>Traffic participants will benefit from an application that will make their driver's life easier and will increase the degree of safety on the roads around the globe.</p>
<p>The application will successfully detect in real time obstacles such as pedestrian and other cars. It will recognize signs and traffic markings and it will be able to detect the current weather and road conditions.</p>

## Technologies

<p>For this project we will use python as a programming language together with some helpful libraries.</p>

* Flask
* OpenCV
* PyTorch
* Numpy

### Flask


<p>Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries.It has no database abstraction layer, form validation, or any other components where pre-existing third-party libraries provide common functions. However, Flask supports extensions that can add application features as if they were implemented in Flask itself. Extensions exist for object-relational mappers, form validation, upload handling, various open authentication technologies and several common framework related tools.
</p>
<p>Jinja is a web template engine for the Python programming language and is licensed under a BSD License created by Armin Ronacher.It is a text-based template language and thus can be used to generate any markup as well as sourcecode.</p>

```html
<!DOCTYPE html>
<html>
  <head>
    <title>{{ variable|escape }}</title>
  </head>
  <body>
  {%- for item in item_list %}
    {{ item }}{% if not loop.last %},{% endif %}
  {%- endfor %}
  </body>
</html>
```

### OpenCV
<p>OpenCV (Open Source Computer Vision) is a library of programming functions mainly aimed at real-time computer vision. In simple language it is library used for Image Processing. It is mainly used to do all the operation related to Images.</p>
<p>What it can do: </p>

1. Read and Write Images
1. Detection of faces and its features
1. Detection of shapes like circle, rectangle, etc. in a image. E.g. Detection of a coin in images.
1. Text recognition in images. e.g Reading number plates.
1. Modifying image quality and colors
1. Developing Augmented Reality apps.
<p>OpenCV supports the deep learning frameworks TensorFlow, Torch/PyTorch and Caffe.</p>

### PyTorch
<p>PyTorch is an open source machine learning library based on the Torch library, used for applications such as computer vision and natural language processing. It is primarily developed by Facebook's artificial intelligence research group. It is free and open-source software released under the Modified BSD license.</p>
<p>PyTorch provides two high-level features</p>

* Tensor computing (like NumPy) with strong acceleration via graphics processing units (GPU)

* Deep neural networks built on a tape-based autodiff system

#### PyTorch tensors

<p>Tensors, while from mathematics, are different in programming, where they can be treated as multidimensional array data structures (arrays). Tensors in PyTorch are similar to NumPy arrays, but can also be operated on a CUDA-capable Nvidia GPU. PyTorch supports various types of tensors.</p>

### NumPy

<p>NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays.</p>

<p>NumPy targets the CPython reference implementation of Python, which is a non-optimizing bytecode interpreter. Mathematical algorithms written for this version of Python often run much slower than compiled equivalents. NumPy addresses the slowness problem partly by providing multidimensional arrays and functions and operators that operate efficiently on arrays, requiring rewriting some code, mostly inner loops using NumPy.</p>

<p>Python bindings of the widely used computer vision library OpenCV utilize NumPy arrays to store and operate on data. Since images with multiple channels are simply represented as three-dimensional arrays, indexing, slicing or masking with other arrays are very efficient ways to access specific pixels of an image. The NumPy array as universal data structure in OpenCV for images, extracted feature points, filter kernels and many more vastly simplifies the programming workflow and debugging.</p>

**Array creation**
```python
>>> import numpy as np
>>> x = np.array([1, 2, 3])
>>> x
array([1, 2, 3])
>>> y = np.arange(10)  # like Python's range, but returns an array
>>> y
array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

```

**Linear algebra**
```python
>>> from numpy.random import rand
>>> from numpy.linalg import solve, inv
>>> a = np.array([[1, 2, 3], [3, 4, 6.7], [5, 9.0, 5]])
>>> a.transpose()
array([[ 1. ,  3. ,  5. ],
       [ 2. ,  4. ,  9. ],
       [ 3. ,  6.7,  5. ]])
>>> inv(a)
array([[-2.27683616,  0.96045198,  0.07909605],
       [ 1.04519774, -0.56497175,  0.1299435 ],
       [ 0.39548023,  0.05649718, -0.11299435]])
>>> b =  np.array([3, 2, 1])
>>> solve(a, b)  # solve the equation ax = b
array([-4.83050847,  2.13559322,  1.18644068])
>>> c = rand(3, 3) * 20  # create a 3x3 random matrix of values within [0,1] scaled by 20
>>> c
array([[  3.98732789,   2.47702609,   4.71167924],
       [  9.24410671,   5.5240412 ,  10.6468792 ],
       [ 10.38136661,   8.44968437,  15.17639591]])
>>> np.dot(a, c)  # matrix multiplication
array([[  53.61964114,   38.8741616 ,   71.53462537],
       [ 118.4935668 ,   86.14012835,  158.40440712],
       [ 155.04043289,  104.3499231 ,  195.26228855]])
>>> a @ c # Starting with Python 3.5 and NumPy 1.10
array([[  53.61964114,   38.8741616 ,   71.53462537],
       [ 118.4935668 ,   86.14012835,  158.40440712],
       [ 155.04043289,  104.3499231 ,  195.26228855]])
```
**Incorporation with OpenCV**
```python
>>> import numpy as np
>>> import cv2
>>> r = np.reshape(np.arange(256*256)%256,(256,256))  # 256x256 pixel array with a horizontal gradient from 0 to 255 for the red color channel
>>> g = np.zeros_like(r)  # array of same size and type as r but filled with 0s for the green color channel
>>> b = r.T # transposed r will give a vertical gradient for the blue color channel
>>> cv2.imwrite('gradients.png', np.dstack([b,g,r]))  # OpenCV images are interpreted as BGR, the depth-stacked array will be written to an 8bit RGB PNG-file called 'gradients.png'
True
```



## Object Detection

<p>Object detection is a computer technology related to computer vision and image processing that deals with detecting instances of semantic objects of a certain class (such as humans, buildings, or cars) in digital images and videos. Well-researched domains of object detection include face detection and pedestrian detection. Object detection has applications in many areas of computer vision, including image retrieval and video surveillance.</p>

<p>It is widely used in computer vision tasks such as face detection, face recognition, video object co-segmentation. It is also used in tracking objects, for example tracking a ball during a football match, tracking movement of a cricket bat, or tracking a person in a video.</p>

### Concept

<p>Every object class has its own special features that helps in classifying the class – for example all circles are round. Object class detection uses these special features. For example, when looking for circles, objects that are at a particular distance from a point (i.e. the center) are sought. Similarly, when looking for squares, objects that are perpendicular at corners and have equal side lengths are needed. A similar approach is used for face identification where eyes, nose, and lips can be found and features like skin color and distance between eyes can be found.</p>

### Methods

<p>Methods for object detection generally fall into either machine learning-based approaches or deep learning-based approaches. For Machine Learning approaches, it becomes necessary to first define features using one of the methods below, then using a technique such as support vector machine (SVM) to do the classification. On the other hand, deep learning techniques are able to do end-to-end object detection without specifically defining features, and are typically based on convolutional neural networks (CNN).</p>

* Machine Learning approaches: 
    * Viola–Jones object detection framework based on Haar features
    * Scale-invariant feature transform(SIFT)
    * Histogram of oriented gradients(HOG) features

* Deep Learning approaches: 
    * Region Proposals (R-CNN, Fast R-CNN, Faster R-CNN)
    * Single Shot MultiBox Detector (SSD) 
    * **You Only Look Once (YOLO)**



## YOLO: Real-Time Object Detection

<p>You only look once (YOLO) is a state-of-the-art, real-time object detection system.</p>

<p>YOLO is popular because it achieves high accuracy while also being able to run in real-time. The algorithm “only looks once” at the image in the sense that it requires only one forward propagation pass through the neural network to make predictions. After non-max suppression (which makes sure the object detection algorithm only detects each object once), it then outputs recognized objects together with the bounding boxes.</p>

<p>With YOLO, a single CNN simultaneously predicts multiple bounding boxes and class probabilities for those boxes. YOLO trains on full images and directly optimizes detection performance. This model has a number of benefits over other object detection methods:</p>

* YOLO is extremely fast
* YOLO sees the entire image during training and test time so it implicitly encodes contextual information about classes as well as their appearance.
* YOLO learns generalizable representations of objects so that when trained on natural images and tested on artwork, the algorithm outperforms other top detection methods.


<img src="finaldetections.jpeg"
     alt="Markdown Monster icon"
     style="float: center; margin-right: auto;" />
<br>
<br>
<p>Further research was conducted resulting in the December 2016 paper “YOLO9000: Better, Faster, Stronger,” by Redmon and Farhadi, both from the University of Washington, that provided a number of improvements to the YOLO detection method including the detection of over 9,000 object categories by jointly optimizing detection and classification.</p>

<p>Even more recently, the same researchers wrote another paper in April 2018 on their progress with evolving YOLO even further, “YOLOv3: An Incremental Improvement”.</p>

<img src="boundingboxes.png"
     alt="Markdown Monster icon"
     style="float: center; margin-right: auto;" />
<br>
<br>
<br>
### Class Prediction

<p>Bounding boxes with dimension priors and location
prediction. We predict the width and height of the box as offsets
from cluster centroids. We predict the center coordinates of the
box relative to the location of filter application using a sigmoid
function</p>

<p>Each box predicts the classes the bounding box may contain using multilabel classification. We do not use a softmax
as we have found it is unnecessary for good performance,
instead we simply use independent logistic classifiers. During training we use binary cross-entropy loss for the class
predictions</p>

<p>This formulation helps when we move to more complex
domains like the Open Images Dataset. In this dataset
there are many overlapping labels (i.e. Woman and Person).
Using a softmax imposes the assumption that each box has
exactly one class which is often not the case. A multilabel
approach better models the data.</p>

<p>YOLOv3 predicts boxes at 3 different scales. Our system extracts features from those scales using a similar concept to feature pyramid networks [Feature Pyramid Networks For Object Detection](https://arxiv.org/abs/1612.03144). From our base feature extractor we add several convolutional layers. The last
of these predicts a 3-d tensor encoding bounding box, objectness, and class predictions. In our experiments with
COCO [Microsoft COCO: Common Objects in Context](https://arxiv.org/abs/1405.0312) we predict 3 boxes at each scale so the tensor is
N × N × [3 ∗ (4 + 1 + 80)] for the 4 bounding box offsets,
1 objectness prediction, and 80 class predictions.</p>

<img src="backbone.png"
     alt="Markdown Monster icon"
     style="float: center; margin-right: auto;" />
<br>


<p>Comparison of backbones. Accuracy, billions of operations, billion floating point operations per second, and FPS for
various networks.</p>
<p>
Each network is trained with identical settings and tested
at 256×256, single crop accuracy. Run times are measured
on a Titan X at 256 × 256. Thus Darknet-53 performs on
par with state-of-the-art classifiers but with fewer floating
point operations and more speed. Darknet-53 is better than
ResNet-101 and 1.5× faster. Darknet-53 has similar performance to ResNet-152 and is 2× faster.
Darknet-53 also achieves the highest measured floating
point operations per second. This means the network structure better utilizes the GPU, making it more efficient to evaluate and thus faster. That’s mostly because ResNets have
just way too many layers and aren’t very efficient.</p>


### Training

<p>We use the Darknet neural network framework for training
and testing.</p>

<p>Darknet is an open source neural network framework written in C and CUDA.</p>



