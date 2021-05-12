# Disparity Computing from Stereo Vision
Disparity Computing of rectified images of the same scene captured from two different viewpoints.

# Introduction
Stereo vision is used to find the 3d dimensions of a scene. Triangulation method is used to calculate the depth of the objects in the 2D image. In Stereo vison, we will have a left and right image captured using 2 cameras. In this we are trying to imitate the human vison. Comparing the left and right image, we can see that there is a displacement for the objects due to the vision angle. This displacement in the correspondence points of two images of the same scene that are captured from two different viewpoints is defined as the disparity. In the triangulation method, depth is inversely proposal to disparity. If disparity is large, then the object is near to the camera and vice versa. Calculating the disparity is an important step in the calculation of depth.                                                                                                                                                                                                                                                                                                     ![image](https://user-images.githubusercontent.com/29349268/118021628-083ee680-b38e-11eb-849b-da3b45093192.png)

**Fig:** Above figure explains how triangulation method is used to calculate the depth of an image.  Using similar triangles property, we get depth Z = (fT) / disparity. 

# Disparity Computing Procedure
In this assignment, I am finding the disparity map using the Appearance Based Point matching.  Few assumptions are made as part of the calculation that both the cameras are placed with small baseline performance and are kept at the same vertical height. Therefore, the disparity between 2 points will be present only in the horizontal line.
In this method, an image patch, g(y) with size (2*N+1)x(2*N+1) will be takes from one of the images. This image patch will be compared with patches of same size in the horizontal direction (since our assumption is disparity is present in the horizontal direction). Smallest Sum-of-Squares Difference (SSD) technique is used to find the most matching image patches. In this techniques, square of pixel vice difference between 2 patches is calculated. The patches which has the minimum SSD is considers as the match.

![image](https://user-images.githubusercontent.com/29349268/118021886-4dfbaf00-b38e-11eb-928c-1449cd29c809.png)

But in our case, we assume that there is no disparity in vertical direction x, therefore we can avoid x

![image](https://user-images.githubusercontent.com/29349268/118021954-62d84280-b38e-11eb-89a6-c79ebff8f3c6.png)

![image](https://user-images.githubusercontent.com/29349268/118021732-21e02e00-b38e-11eb-89b6-98ba6f58e287.png)

**Fig:** In the above figure an image patch is extracted from the Right image and compared with multiple image patches from the left Image. The image patch with minimum SSD is considerd as match and differece in displacement of that patches in both the images is considerd as disparity.

The difference in the horizontal pixel positions of the matching patches, is chosen as the disparity of that point. This will be noted for creating the disparity map. 
In the code implementation, image patch g(y) is taken from the right stereo image and compared with the reference image I(x) patch from the left stereo image. The disparity calculated between the matching images is updated in the middle index of the image patch in the disparity matrix.

# Sample disparity maps created

![image](https://user-images.githubusercontent.com/29349268/118022259-c1052580-b38e-11eb-9574-16c3e73d6273.png)

-----------------------------------------------------------------------------------------------------------------

![image](https://user-images.githubusercontent.com/29349268/118022365-e3973e80-b38e-11eb-861d-d6d1fcfca357.png)

# Observations 
Below are the observations noted
**1**.	From the disparity maps above, we can observe that the objects which are far from the cameras has low disparity. This is correct as Z is inversely proportional to the disparity.

![image](https://user-images.githubusercontent.com/29349268/118022672-29540700-b38f-11eb-870c-c45735e4a131.png)

**Fig:** In the above image and disparity map, we can observe that the circled building is far away compared to the other building. In the disparity map, we can see that the circled portion is dark (low disparity value). 

**2**.	From the disparity maps above, we can see that the Appearance Based Point matching does not work well on surfaces that are similar. This is because in similar surfaces, it will be difficult to find the matching reference patch as there will be multiple patches resembling the image patch. So even though there can be a large disparity, during checking least SSD, it may match with another similar image patch with low disparity. 

![image](https://user-images.githubusercontent.com/29349268/118022729-412b8b00-b38f-11eb-9cb1-ee6de8421348.png)

**Fig:**  In the above figure, you can observe that the circles portions are similar areas. This circles aras are near to the camera, so according to triangualtion disparity values should be high. But we can observe that the disparity values are low(dark) due to the similarity in surrounding pixels.

**3**.	Increasing the image patch size will smoothen the disparity map. This can be considerd as a hyper parameter. Using larger image patches can improve the results in similar pixel surrounded areas. If the image patch size is small, we can observe that it has good precision but sensitive to noise. If the image patch is big, we can observe that it’s robust to noise but precision decresases.

![image](https://user-images.githubusercontent.com/29349268/118022786-53a5c480-b38f-11eb-9f91-94d642825a71.png)

**Fig:** In the above figures we can observe that the disparity map created using 7x7 image patch is smoother than 3x3. 

# Improvement suggestion in current point matching algorithm
# Semi-Global matching algorithm
From the disparity images produced by the point matching using the small SSD technique, we can observe that the pixels which are close to each other can have a high difference in the disparity values. But in reality, the nearby pixels should have an almost similar disparity variation. This issue can be mitigated by penalising the jumps in disparity between adjacent pixels.
Semi-Global matching algorithm penalises the jumps in adjacent pixels variation. This algorithm mainly has 2 parts, 1) Pixel matching, find a good match in the other image, which is same as block matching and 2) Regularization term to penalise the disparity jumps.  Combining these 2 factors, the resulting disparity image will be smoother than the ordinary point matching.

![image](https://user-images.githubusercontent.com/29349268/118023035-a1223180-b38f-11eb-9911-869f1f69e055.png)

**Fig**: Comparison Of resulting disparity maps of Point Matching and SGBM

From the above images, we can observe that the resulting disparity images of SGBM are smoother and have less disparity jump between neighbouring pixels compared to the ordinary point matching disparity map
