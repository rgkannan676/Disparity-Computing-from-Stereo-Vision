#Code for implementing the Semi-Global matching algorithm using the Open CV library
%matplotlib inline
#This Assignment is done using Google Collab
import sys, os
from PIL import Image
import numpy as np
import cv2
from matplotlib import pyplot as plt

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
  # Reading Left and Right images
  imgL = cv2.imread(imagePair+'l.jpg',0)
  imgR = cv2.imread(imagePair+'r.jpg',0)
  #Compute the diparity. BlockSize determines the image patch size
  stereo = cv2.StereoSGBM_create(blockSize=5)
  disparity = stereo.compute(imgL,imgR)
  #Ploting the image disparity
  plt.imshow(disparity,'gray')
  plt.show()