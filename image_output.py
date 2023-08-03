import cv2
import matplotlib.pyplot as plt
image1_path=input("enter the original image path : ")
image2_path=input("enter the stego image path :")


image1=cv2.imread(image1_path)
image2=cv2.imread(image2_path)

plt.figure(figsize=(12,8))


plt.subplot(121)
plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis('off')


plt.subplot(122)
plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
plt.title("Stego Image")
plt.axis('off')
plt.show()





