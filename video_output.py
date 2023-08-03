import cv2
import matplotlib.pyplot as plt

# Open the first video file
video1_path =input("enter the original video path : ")
video1_capture = cv2.VideoCapture(video1_path)

# Open the second video file
video2_path =input("enter the stego video path : ")
video2_capture = cv2.VideoCapture(video2_path)

# Create a matplotlib figure with two subplots
fig, axes = plt.subplots(1, 2)

while True:
    # Read a frame from the first video
    ret1, frame1 = video1_capture.read()

    # Read a frame from the second video
    ret2, frame2 = video2_capture.read()

    if not ret1 or not ret2:
        break

    # Convert the frames from BGR to RGB format
    frame1_rgb = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
    frame2_rgb = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

    # Display the frames side by side using matplotlib
    axes[0].imshow(frame1_rgb)
    axes[0].axis('off')
    axes[0].set_title('Original video')

    axes[1].imshow(frame2_rgb)
    axes[1].axis('off')
    axes[1].set_title("Stego video")

    plt.pause(0.0001)

    # Clear the current axis to update the frames
    axes[0].cla()
    axes[1].cla()

# Release the video captures and close the figure
video1_capture.release()
video2_capture.release()
plt.close(fig)