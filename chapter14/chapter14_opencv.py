import cv2

# Load the trained model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# You may need to change the index depending on your computer and camera
video_capture = cv2.VideoCapture(1)

while True:
    # Get an image frame
    ret, frame = video_capture.read()

    # Convert it to grayscale and run detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray)

    # Draw a rectangle around the faces
    for x, y, w, h in faces:
        cv2.rectangle(
            img=frame,
            pt1=(x, y),
            pt2=(x + w, y + h),
            color=(0, 255, 0),
            thickness=2,
        )

    # Display the resulting frame
    cv2.imshow("Chapter 14 - OpenCV", frame)

    # Break when key "q" is pressed
    if cv2.waitKey(1) == ord("q"):
        break

video_capture.release()
cv2.destroyAllWindows()
