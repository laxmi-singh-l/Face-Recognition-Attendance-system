import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

# Path to the folder containing the training images
path = 'Training_images'
images = []
classNames = []

# Load images and class names
try:
    myList = os.listdir(path)
    print("Training images:", myList)
except FileNotFoundError:
    print(f"Error: Directory '{path}' not found.")
    exit()

for cl in myList:
    curImg = cv2.imread(os.path.join(path, cl))
    if curImg is not None:
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])
    else:
        print(f"Error loading image: {cl}")
print("Class Names:", classNames)

# Function to find encodings for the loaded images
def findEncodings(images):
    encodeList = []
    for idx, img in enumerate(images):
        print(f"Original Image {idx} dtype: {img.dtype}, shape: {img.shape}")

        # Ensure the image is in uint8 format
        if img.dtype != np.uint8:
            img = img.astype(np.uint8)
            print(f"Converted Image {idx} to dtype: {img.dtype}")

        # Ensure the image is in RGB format
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        print(f"Image {idx} after RGB conversion dtype: {img.dtype}, shape: {img.shape}")

        # Display the image for manual inspection
        cv2.imshow(f"Image {idx}", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print(f"No face found in image {idx}. Skipping this image.")
        except Exception as e:
            print(f"Error processing image {idx}: {str(e)}")
    return encodeList

# Function to mark attendance in a CSV file
def markAttendance(name):
    filename = 'Attendance.csv'
    try:
        with open(filename, 'r+') as f:
            myDataList = f.readlines()
            nameList = [line.split(',')[0] for line in myDataList]

            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')
                print(f"Attendance marked for {name}")
    except FileNotFoundError:
        print(f"Error: '{filename}' not found. Creating a new one.")
        with open(filename, 'w') as f:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'Name,Time\n{name},{dtString}')
            print(f"Attendance marked for {name}")

# Encode the known faces
encodeListKnown = findEncodings(images)
if not encodeListKnown:
    print("No encodings found. Exiting.")
    exit()
print('Encoding Complete')

# Capture video from webcam
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture image from webcam. Exiting.")
        break

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            markAttendance(name)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
