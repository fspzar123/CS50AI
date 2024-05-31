# traffic.py
Understanding the first part of the code was easy but keras was something new and which I had never tried before.Then coming to the model building part of the program,
## load_data
The load_data function should accept as an argument data_dir, representing the path to a directory where the data is stored.We assume that data_dir will contain one directory named after each category, numbered 0 through NUM_CATEGORIES - 1. Inside each category directory will be some number of image files. But we have to resize the image using the OpenCV's imread to read the image and then resize the image using the resize function. 'labels' should be a list of integers, representing the category number for each of the corresponding 'images' in the images list.Finallyreturn image arrays and labels for each image in the data set.
## get_model
The input to the neural network will be of the shape (IMG_WIDTH, IMG_HEIGHT, 3) (that is, an array representing an image of width IMG_WIDTH, height IMG_HEIGHT, and 3 values for each pixel for red, green, and blue).
The number of layers and the types of layers you include in between are
* First 2D Convolution Layer and MaxPooling Layer with an input image of 32 pixels and three channels along with relu activation
* Second 2D Convolution Layer and MaxPooling Layer with an input image of 64 pixels and three channels along with relu activation
* Third 2D Convolution Layer and MaxPooling Layer with an input image of 32 pixels and three channels along with relu activation
* Then we flatten the to form a one dimensional array
* First dense (fully connected) layer also with relu activation
* Finally the output dense layer

 accuracy: 0.9670 - loss: 0.1618
