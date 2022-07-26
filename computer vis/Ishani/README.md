https://onedrive.live.com/redir?resid=83CF8A3A689B2810%21550&authkey=%21AkV45quH2w-O34o&page=View&wd=target%28Drishti%20Rani.one%7C3c7e552d-4085-48ea-a956-60b27c3b4df0%2FUntitled%20Page%7C2e985ff9-3ee4-4c96-9275-557162b06369%2F%29&wdorigin=NavigationUrl

Notes on ANN:
- has 1-D Features 
- so not that accurate as compared to CNN 

Hence CNN to be implemented for now:
	WHEN WE USE THE CONVULUTIONAL OPERATION IT IS KNOWN AS FEATURE EXTRACTION PARRT AND IN THE SECOND PART WHERE WE USE DENSE NEURAL NETWORK IT IS CALLED THE CLASSIFICATION
Libraries to be used:
PILLOW- required to read an image and do some image processing
we need to store image as matrix 


Should we Resize?
yes. 
To process such big images network will become very big and training will be affected as a lot of memory will be consumed 
On resizing will our accuracy also go down? It might or it might not be but for most of the tasks it does not get reduced 
imp: 
Np.array--The pil image needs to be converted to a numpy array to do further tasks
Imageslist.append--As there are many images so we append all the images in a python list 
There is a dataframe which has all the file names in there so we have to read the pandas dataframe and then pass to this function node data 

Where to work :
KAGGLE IS BETTER AS IT HAS DATA SETS ALSO! But colab is also usable 
	
 LOSS FUNCTION:
We need to find loss function so binary cross entropy is used for when we have to classify bw 2 classes
For many classes we have to use categorical cross entropy  
Sparse categorical Cross entropy 

We need to use an OPTIMISER 
TO optimise our loss function and lessen it 
Which one to use(still need to research)
Best optimiser is adam but can use different like RMS PROP

need function to flatten ---- which one to use ?  

ACTIVATION FUNCTIONS TO USE :
1. SOFTMAX (better)
2. TANH 
3. SIGMOID
4. more


POOLING (VERY IMPORTANT )

Main purpose: 
	1. reduce the size of the image so that computer doesn't get a shock  
	2. Reduce size of features so that we get less layers in order reduce the input down to something more manageable  
	3. Pooling takes a filter and slides the filter along the input according to a stride unlike convolutional layers  which use weights 
	4. Pooling uses operations 


Max pooling: when we put the maximum number from the feature map
Max pooling + convolutional helps with position invariant feature detection means it doesn't matter where the eyes or ears are 
Feature map: 

There is average pooling also 

Benefits of pooling:
	1. Reduces dimensions +computation 
	2. Reduce overfitting as there are less parameters 
	3. Model is tolerant towards variations and distortions 

YOLO 
https://www.v7labs.com/blog/yolo-object-detection Good resource 

QUESTIONS WHICH NEED TO BE ANSWERED
	1. What are different activation functions ? Why they are used and why some others are not used?
	2. Difference between a SIGMOID function and a SOFTMAX function.
	3. Which activation functions are used and why not.etc.
	4. What is gradient descent ?
	5. What is Back- Propagation? Mathematically explain
	6.  What is binary cross entropy ?
	7. Function to get accuracy
  8. WHICH POOLING FUNTION TO USE?
  9. 




