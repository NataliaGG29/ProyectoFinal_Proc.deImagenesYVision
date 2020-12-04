# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 16:12:23 2020

@author: matheo
"""

import cv2 
import numpy as np 

cap = cv2.VideoCapture(0)
N = 0                    #variable para controlar cada cuanto se toma un dato 
i = 0                    #variable encargada de realizar el promedio
prom_suma = 0            #variable que lleva el acumulado de la suma
prom = 0                 #variable que lleva el promedio acumulado 

while(1): 
    
    _,frame   = cap.read()
    frame = cv2.GaussianBlur(frame,(7,7),0)        #aplicar filtro para quitar ruido
    
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)    #pasar a HSV
    
    #filtrar el color de piel https://es.wikipedia.org/wiki/Carne_(color)
    
    lower_skin = np.array([0,10,60])
    upper_skin = np.array([20,150,255])            #umbrales para el color piel
    mask = cv2.inRange(hsv,lower_skin,upper_skin)  #para mostrar solo el rostro
    
    #aplicar operadores morfológicos 
    shape   = cv2.MORPH_RECT                       
    ksize   = (19,19)                              
    shape2  = cv2.MORPH_ELLIPSE 
    kernel2 = cv2.getStructuringElement(shape2,ksize)
    kernel  = cv2.getStructuringElement(shape,ksize)
    filtro  = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    filtro  = cv2.morphologyEx(filtro,cv2.MORPH_CLOSE,kernel2)
    
    res = cv2.bitwise_and(frame,frame,mask = filtro) #aplicar un AND para mostrar el rostro a color
    
    #sacar el contorno de la cara 
    contours,hierarchy = cv2.findContours(filtro.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    N = N + 1
    #calcular el minimo rectangulo contenedor de la cara
    for contour in contours: 
       
        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        
        #esta parte del codigo se encarga de recoger datos y promediarlos
        if N == 70:
            print ("el ancho del rectangulo es",w)
            print ("el alto del rectangulo es",h)
            phi = h/w
            print ("el h/w es" ,phi)
            N = 0
            if i != 30:
                i = i +1
                prom_suma = (prom_suma + phi)
                prom = prom_suma/i
                print ("se han tomado", i, "datos")
                print ("el promedio de la constante phi es", prom)
      
    cv2.imshow('frame',frame)
    cv2.imshow('frame_fil',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('img_apertura',filtro)
    cv2.imshow('res',res)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()


        
