import sys

import cv2
import tensorflow as tf
import mediapipe as mp
import numpy as np


cap = cv2.VideoCapture(0)
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.7)
model = tf.keras.models.load_model(r"models\airost_demo_facemask.h5")
while True:
    a, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_coordinates = face_detection.process(frame)
    #print(frame.shape)
    if face_coordinates.detections:
        coordinates = []
        faces = []
        for i in face_coordinates.detections:
            coor = [i.location_data.relative_bounding_box.xmin*640 *0.95, i.location_data.relative_bounding_box.ymin*480 *0.95,
                    i.location_data.relative_bounding_box.xmin*640*1.05 + i.location_data.relative_bounding_box.width*640*1.05 ,
                    i.location_data.relative_bounding_box.ymin*480*1.05 + i.location_data.relative_bounding_box.height*480*1.05]
            xdiff = coor[2] - coor[0]
            ydiff = coor[3] - coor[1]
            if xdiff < ydiff:
                diffneed = ydiff - xdiff
                coor[0] -= diffneed / 2
                coor[2] += diffneed / 2
            else:
                diffneed = xdiff - ydiff
                coor[1] -= diffneed / 2
                coor[3] += diffneed / 2
            coor = np.array(coor).astype("int")
            coordinates.append(coor)
            cropped_face = frame[coor[1]:coor[3], coor[0]:coor[2]]
            if cropped_face.any():
                cropped_face = cv2.resize(cropped_face, (224,224))
                faces.append(cropped_face)
            # print(frame.shape)
            
        if len(faces) != 0:
            results = model(np.array(faces))
            # print(results)
            results = np.array(results)
            # print(results)
            classes = ["wear wrongly", "wearing", "not wearing"]
            output_print = []
            for i in results:
                index = np.argmax(i)
                # print(index)
                predicted = classes[index]
                string_to_print = "{} : {} %".format(predicted, round(np.max(i)*100, 2))
                output_print.append(string_to_print)
    
            # draw bounding box on webcam
            if len(coordinates) != 0:
                for o, i in enumerate(output_print):
                    frame = cv2.rectangle(frame, (coordinates[o][0], coordinates[o][1]), (coordinates[o][2], coordinates[o][3]), (0,255,0), thickness=1,
                                          lineType= cv2.LINE_AA)
                    frame = cv2.putText(frame, i, (coordinates[o][0], coordinates[o][1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), thickness=1,
                                          lineType= cv2.LINE_AA)

        # for i in coordinates:
        #     frame = cv2.rectangle(frame, )

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imshow("feed", frame)
    if cv2.waitKey(1) == 27:
        break
