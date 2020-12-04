# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 11:38:04 2020

@author: matheo
"""

import cv2 
import numpy as np 

cap = cv2.VideoCapture(0)
min_sintap = 1.1 - 0.1
max_sintap = 1.506 + 0.1
min_contap = 0.674 - 0.1 
max_contap = 0.962 +0.1


while(1): 
    
    _,frame = cap.read()
    frame = cv2.GaussianBlur(frame,(7,7),0)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    #filtrar el color de piel https://es.wikipedia.org/wiki/Carne_(color)
    
    lower_skin = np.array([0,10,60])
    upper_skin = np.array([20,150,255])
    mask = cv2.inRange(hsv,lower_skin,upper_skin)
    
    #aplicar operadores morfológicos 
    shape   = cv2.MORPH_RECT 
    ksize   = (21,21)
    shape2  = cv2.MORPH_ELLIPSE 
    kernel2 = cv2.getStructuringElement(shape2,ksize)
    kernel  = cv2.getStructuringElement(shape,ksize)
    filtro  = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    filtro  = cv2.morphologyEx(filtro,cv2.MORPH_CLOSE,kernel2)
    
    res = cv2.bitwise_and(frame,frame,mask = filtro)
    
    #sacar el contorno de la cara 
    contours,hierarchy = cv2.findContours(filtro.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #calcular el minimo rectangulo contenedor 
    for contour in contours: 
        
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        phi = h/w
        print ("el h/w es" ,phi)
         
        #clasificador con los valores max y min de phi 
        if phi <= max_sintap and phi >= min_sintap:
            cv2.putText(frame,'pongase el tapabocas por favor',(25,10),2,0.8,(0,0,255),1,cv2.LINE_AA)
            print("póngase el tapabocas por favor") 
        else: 
            if phi <= max_contap and phi >= min_contap:
                cv2.putText(frame,'cumple al menos un protocolo de bioseguridad',(25,100),2,0.8,(0,255,255),1,cv2.LINE_AA)
                print("cumple al menos un protocolo de bioseguridad")
           
    
    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('img_apertura',filtro)
    cv2.imshow('res',res)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()


        