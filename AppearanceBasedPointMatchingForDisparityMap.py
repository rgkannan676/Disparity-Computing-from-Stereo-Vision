#This Assignment is done using Google Collab
import sys, os
from PIL import Image
import numpy as np
import math

##Sample image files are stored inside my Google Drive.
##Below code snippet is to traverse to the right path were the images are store.
def traverseToGoogleDriveFolder():
  if 'google.colab' in sys.modules:
    from google.colab import drive
    drive.mount('/content/gdrive',force_remount=True)
    os.chdir('/content/gdrive')
    folder_name = 'workFolder'
    import subprocess
    path_to_folder = subprocess.check_output('find . -type d -name ' + str(folder_name), shell=True).decode("utf-8")
    path_to_folder = path_to_folder.replace('\n',"")
    os.chdir(path_to_folder)
      ##Traversal to the folder were images are kept completed.


## Method to find the Sum Of Square Difference between two image patches
def getSumOfSquareDifference(imagePatch,referenceImagePatch):
  try:
    h,w,c= imagePatch.shape
  except:
    #if 1 channel images is passed
    h,w= imagePatch.shape
    c=1
  sumOfSquareDifference=0
  for ch in range(0,c):
    for wd in range(0,w):
      for hg in range(0,h):
        if c==1:
          sumOfSquareDifference += (int(imagePatch[hg,wd]) - int(referenceImagePatch[hg,wd])) **2
        else:
          sumOfSquareDifference += (int(imagePatch[hg,wd,ch]) - int(referenceImagePatch[hg,wd,ch])) **2
  return sumOfSquareDifference

## Method to find the disparity matrix between 2 image matrixes by checking the least square difference
## imageRefernce is the right stereo image
## imageToCompare is the left stereo image
## filterParam decides the N param which decides then image patch size
## disparityThreshold is the maximum disparity threshold to reduce the outlier’s impact in the disparity map
def getDisparityMatrix(imageRefernce, imageToCompare, imageSizeParam, disparityThreshold): 
  try:
    h,w,c= imageRefernce.shape
  except:
    h,w= imageRefernce.shape
    c=1

  # N to define the image patch size
  N=imageSizeParam

  # image Patch Size g(y) is 2 * N + 1
  imagePatchSize=(2 * N + 1 )

  # Initializing for row index extracting image Patch g(y)
  filterRowStart=0
  filterRowEnd = imagePatchSize

  # Initializing matrix to capture the image disparity
  disparityMatrix = np.zeros(leftImageArray.shape)
  
  
  # Loop to cover the height of the image for extracting the image patches
  while filterRowEnd <= h:

    # Initialize the image patch g(y) column index
    filterColumnStart=0
    filterColumnEnd = imagePatchSize

    # Loop to cover the width of the image for extracting the image patches
    while filterColumnEnd <= w:

      if(c==1):
        imagePatch = imageRefernce[filterRowStart:filterRowEnd,filterColumnStart:filterColumnEnd]
      else:
        # extracting the image patch g(y) from Right stereo image. This will be compared with Left stereo image.
        imagePatch = imageRefernce[filterRowStart:filterRowEnd,filterColumnStart:filterColumnEnd,:]

      # initializing parameters to process the least square value.
      smallestLeastsquareValue=float('inf')
      leastSquareColumn=0

      # Initializing the row index of the reference patch I(y) as same as the image patch due to assumption that disparity in only in the horizontal direction.
      referenceImageRowStart=filterRowStart
      referenceImageRowEnd = filterRowEnd
      
      # Flag to adjust refernce image patch column size
      allowOnePass=False
      if w - imagePatchSize < filterColumnStart:
        allowOnePass=True

      # initializing refernce image patch I(y)  
      referenceImagColumnStart= w - imagePatchSize
      referenceImagColumnEnd = w
       
      # Loop to cover the width of the image for extracting the reference image patch g(y) and compare with above image patch I(x) and find the least square difference details.  
      while referenceImagColumnStart >=filterColumnStart or allowOnePass:
        # Mark that the last column refernce image patch is completed.
        allowOnePass=False

        if(c==1):
          # extracting for channel =1
          referenceImagePatch = imageToCompare[referenceImageRowStart:referenceImageRowEnd,referenceImagColumnStart:referenceImagColumnEnd]
        else:
          # extracting the reference patch I(y) from the Left Stereo image, which will be compared with the image patch g(y).
          referenceImagePatch = imageToCompare[referenceImageRowStart:referenceImageRowEnd,referenceImagColumnStart:referenceImagColumnEnd,:]

        # Calculate the least square difference between image patch g(y) and I(y).
        leastSquareValue = getSumOfSquareDifference(imagePatch,referenceImagePatch)

        # Compare the least square value and update the values if it is less than the previous value.
        if(leastSquareValue <= smallestLeastsquareValue):
          smallestLeastsquareValue=leastSquareValue
          leastSquareColumn=referenceImagColumnStart                  

        # update the reference image index to get the next reference patch I(y) 
        referenceImagColumnStart -=1
        referenceImagColumnEnd -=1 
      
      # Calculate the disparity by finding difference in column index between image patch g(y) and reference image I(x)
      # Converts all the high outlier disparity values to the disparityThreshold.
      disparity = disparityThreshold if abs(leastSquareColumn - filterColumnStart) > disparityThreshold else abs(leastSquareColumn - filterColumnStart)
      
      # update the middle pixel index of image Patch with the disparity value.
      disparityMatrix[math.floor((filterRowStart+filterRowEnd)/2),math.floor((filterColumnStart+filterColumnEnd)/2)] = disparity
      
      # update the reference image index to get the next image patch g(y) in horizontal direction.
      filterColumnStart +=1
      filterColumnEnd +=1

 
    # update the refrence image index to get the next image patch g(y) in vertical direction.
    filterRowStart+=1
    filterRowEnd+=1

  
  # Steps to normalize the disparity and map it to the 0-255 range for creating disparity image.
  maxDisparity= float(np.amax(disparityMatrix))
  minDisparity = float(np.amin(disparityMatrix))
  disparityMatrix = np.floor(((disparityMatrix - minDisparity)/(maxDisparity-minDisparity))*255.0)

  return disparityMatrix 


#Traversing to google drive folder.
try:
  traverseToGoogleDriveFolder()
except subprocess.CalledProcessError as cmderr:
  print ('Error occured while traversing to google drive.')
  print (cmderr.output)
  exit(0) #exiting further execution as folder traverse failed.

# Image names
imagePairs = ['corridor','triclopsi2']

# Loop to get the images.
for imagePair in imagePairs:
  leftImage = Image.open(imagePair+'l.jpg')
  rightImage= Image.open(imagePair+'r.jpg')


  # Setting the disparity threshold as per practical intuition to avoid outliers.
  if imagePair == 'triclopsi2':
    disparityThreshold=100
  else:
    disparityThreshold=20

  # Converting images into arrays for comparison.
  leftImageArray = np.array(leftImage)
  rightImageArray = np.array(rightImage)
  
  # Loop to iterate and create disparity image by changing image patch size parameter.
  for filterParameter in range(1,4):
    # Get the disparity matrix from images. 1,2,3 filter parametrs are passed to get the correspoding disparity images.
    disparityMatrix = getDisparityMatrix(rightImageArray,leftImageArray,filterParameter,disparityThreshold)
    # Convert diparity matrix to image.
    disparityMatrixImage = Image.fromarray(disparityMatrix.astype(np.uint8),mode='RGB') 
    #Save the disparity image.
    disparityMatrixImage.save("./latestDisaparity_"+imagePair+"_"+str(filterParameter)+".jpg")
