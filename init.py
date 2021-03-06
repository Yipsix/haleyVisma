import face_recognition
import cv2
import pyttsx3
import time
import data
import ai


print('loads trained data')
known_face_names = []

for person in data.export_data():   
    known_face_names.append([person[0], person[1], None])

known_face_encodings = []

for face_encoding in known_face_names:
    known_face_encodings.append(face_encoding[1])

print('done loading')

engine = pyttsx3.init()

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
im = cap.read()[1] #because reasons

r = cv2.selectROI(im)
process_this_frame = True

frameCount = 0

while (True):

    ret, frame = cap.read()
    # zoom in
    crop_img = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    
    smallImg = cv2.resize(crop_img, (0,0), fx=0.25, fy=0.25) 
    rgb_small_frame = smallImg[:, :, ::-1]
    # Only process every other frame of video to save time
    if frameCount % 4 = 0:
        frameCount = 0
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(
            rgb_small_frame, face_locations)

        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
                ai.addPerson(name)
            else:
                ai.foundUnknownPerson()

    frameCount = frameCount + 1

    big = cv2.resize(crop_img, (0,0), fx=5, fy=5) 
    cv2.imshow('Video', big)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
