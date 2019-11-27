# ParkinGo

The problem of finding available parking spaces for your car is a common problem of each big city. Having an intelligent app do the searching of a free parking spot could considerably improve the parking experience.

 parking space detection system based on images provided by CCTVs could  at a relatively low cost.

#### Table of contents
[Motivation](#motivation)

[Algorithm](#algorithm)

[Application design](#application-design)

[Mind map](#mind-map)

### Motivation

ParkinGo was inspired by situations that everyone of us encountered at some moment in their lives: blindly circling a big parking area in search for a free spot, not knowing which parking lots will have free spots and so on. Statistically speaking, the average time spent searching for a parking spot represents \textbf{7.8 minutes}. This is a waste of time and can also cause traffic congestion. 
There are solutions which try to solve the mentioned problem, for example systems that work by counting cars at the parking lot entrance. Howether, their disadvantage is that they don't provide concrete informations about available spots, leaving the task of finding the place to the driver. A more precise solution involves sensors which would provide information about each spot specifically. However, this solution implies higher costs of c.a \textbf{\$40} per unit. 
This inspired us to implement an alternative approach which will be using video provided by already installed surveillance cameras.
This method would imply that our app knows where the parking spots are, and is using a Machine Learning algorithm to make a prediction regarding the occupancy of each parking spot. Displaying the real-time information on a webpage would make it accessible to everyone, which win turn would definetely save the driver's time and considerably reduce traffic problems.

### Algorithm

The algorithm uses a Convolutional Neural Network to predict whether a parking slot is occupied or free. Of course, the Network has no way of knowing how a car looks like. This is where the training phase comes in. In simple terms, this means that we give a big set of parking spot images to the algorithm, our dataset, which have been manually classified into occupied and free. The algorithm then uses this images to "learn" how an empty parking spot and an occupied one should look like. The training is done in more steps called epochs, each time trying to achive better results by adjusting the parameters used for the learning. As a result we get a model which could then make predictions based on the information it used to learn. In our application, this means telling if an image of a parking spot looks like it has a car parked on it or not. Both of our models have correctly classified 98% of spots.

Of course, the model has its limitations, like poor light conditions, blurred or obstructed image regions. 

### Application design

As mentioned earlier, the ultimate goal of the application is to obtain information about the availability of parking spots from a video. 
For the demo, we used a recorded sequence from a live stream video of a parking lot in Hicksville, New York, USA. Each parking spot was manually marked so the algorithm would know the location of the spots on the image. Then at each n seconds the current frame is extracted from the video and passed to the algorithm which crops each spot from the big image and uses the model to makes predictions on its occupancy. The client then gets the result and displays it on a webpage in form of a grid of red and green boxes, for occupied and free spots, respectively. The position of the boxes in the grid corresponds to those of the spots, so the user can easily identify the location of the empty parking spot.  

![](/flow.jpg)

### Mind map

In a real life scenario, the Youtube video could be replaced by a live stream from a parking lot surveillance camera so the app could provide real time information about the parking lot occupancy. Another thing to take into consideration would be different weather and lightning conditions. We also focus on the accessibility 
of the processed information in real-time, for which we will try to optimize our model to achive the best balance between accurate results and small processing time.
