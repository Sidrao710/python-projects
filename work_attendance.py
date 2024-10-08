import cv2
import face_recognition as fr
import os
import numpy
from datetime import datetime


# create database
path = 'Employees'
my_images = []
employees_names = []
employee_list = os.listdir(path)

for name in employee_list:
    this_image = cv2.imread(f'{path}\\{name}')
    my_images.append(this_image)
    employees_names.append(os.path.splitext(name)[0])

print(employees_names)

#encode images
def encode(images):

    # create new list
    encoded_list = []

    #convert all the images to rgb
    for image in images:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # encode
        encoded = fr.face_encodings(image)[0]

        #add to the list
        encoded_list.append(encoded)

    #retrun encoded list
    return encoded_list

# record attendance
def record_attendance(person):


encoded_employee_list = encode(my_images)

# take a web cam picture

capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# read the captured image
success, image = capture.read()

if not success:
    print('Capture could not be taken')
else:
    # recognize a face in that capture
    captured_face = fr.face_locations(image)

    # encode the captured face
    encoded_captured_face = fr.face_encodings(image, captured_face)

    # search for a match
    for face, location_face in zip(encoded_captured_face, captured_face):
        matches = fr.compare_faces(encoded_employee_list, face)
        distances = fr.face_distance(encoded_employee_list, face)

        print(distances)

        match_index = numpy.argmin(distances)

        # show coincidences if any
        if distances[match_index] > 0.6:
            print('Does not match any of our employees ')
        else:
            print("Have a nice working day")

            # serach for the name of the employee found
            employees_name = employees_names[match_index]

            y1, x2, y2, x1 = location_face
            cv2.rectangle(image,
                          (x1, y1),
                          (x2, y2),
                          (0, 255, 0),
                          2)
            cv2.rectangle(image,
                          (x1, y2),
                          (x2, y2),
                          (0, 255, 0),
                          cv2.FILLED)
            cv2.putText(image, employees_name,
                        (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_COMPLEX,
                        1,
                        (255, 255, 255),
                        2)


            # show the image obtained
            cv2.imshow('web image', image)

            # keep window open
            cv2.waitKey(0)

