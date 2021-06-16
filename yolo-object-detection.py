# -*- coding: utf-8 -*-
"""
Created on Sun May 30 18:27:59 2021

@author: lenovo
"""

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

f = open('files/coco.txt')


classnames = []

classnames = f.read().split('\n')
    
# print(classnames)
# print(len(classnames))

modelconfiguration = "files/yolov3.cfg"
modelweights = "files/yolov3.weights"

# Create our network and make it read from Darknet and it takes 
# 2 argument configuration file nand weights file.
net = cv2.dnn.readNetFromDarknet(modelconfiguration, modelweights)
# Declare that we will use OpenCV as the backend
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
# Declare that we want to use CPU
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def findObjects(outputs, img):
    H, W, CH = img.shape
    
    # this list will store values of x, y, width and height
    bbox = []
    
    # this list will contain all class id's
    classIds = []
    
    # confidence values
    confs = []
    
    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            # confidence threshold = 0.5
            if confidence > 0.5:
                # element number 3 is width and index 2
                # element number 4 is height index 3
                # we multiply by width and height to get pixel value
                w, h = int(det[2] * W), int(det[3] * H)
                x, y = int((det[0] * W) - w / 2), int((det[1] * H) - h / 2)
                bbox.append([x,y,w,h])
                classIds.append(classId)
                confs.append(float(confidence))
                
                
                
    print(len(bbox))
    # 0.5: confidence threshold
    # 0.3: nms threshold it should be reduced to decrease number of boxes
    indices = cv2.dnn.NMSBoxes(bbox, confs, 0.3, 0.5)
                
    for i in indices:
        i = i[0]
        box = bbox[i]
        x, y, w,h = box[0], box[1], box[2], box[3]
        
        cv2.rectangle(img, (x, y), (x+w,y+h), (0,255,0), 3)
        cv2.putText(img, classnames[classIds[i]].upper(), (x, y-10), 0, 0.6, (255,255,255), 2)
    
while cap.isOpened():
    
    ret, img = cap.read()
    
    # Network only accepts image format of type blob
    # 1- the img to convert.
    # 2- divide it by 255
    # 3- set width and height we use yolo 320.
    # 4- default parameters
    # 5- crop = False
    blob = cv2.dnn.blobFromImage(img, 1/255, (320,320), [0,0,0], 1, crop=False)
    
    # set blob as input to network
    net.setInput(blob)
    
    # from yolo concolutional neural network we have 3 prediction of output
    # so we need to know the names of these output layers
    # so we can refer to them in our network
    layerNames = net.getLayerNames()
    # print(layerNames[199])
    
    outputNames = [layerNames[i[0] - 1] for i in net.getUnconnectedOutLayers() ]
    # print(outputNames)
    
    outputs = net.forward(outputNames)
    # print(len(outputs))
    
    # print(outputs[0].shape)
    # print(outputs[1].shape)
    # print(outputs[2].shape)
    # print(outputs[0][0])
    
    findObjects(outputs, img)
    
    cv2.imshow("image", img)
    
    if cv2.waitKey(1) == ord('x'):
        break
    
cap.release()
cv2.destroyAllWindows()


