"""
Hand Tracing Module
By: Murtaza Hassan
Youtube: http://www.youtube.com/c/MurtazasWorkshopRoboticsandAI
Website: https://www.murtazahassan.com/
"""
 
import cv2
import mediapipe as mp
import time
import numpy as np
 
def find_len(a,b):
    x_len = a[1] - b[1]
    y_len = a[2] - b[2]
    return x_len**2 + y_len**2
 
def define_hand(img, lmList):
    key_press = 0
    pTime = 0
    cTime = 0
    list_of_features = [(0,5),(5,17),(17,0),(0,12),(12,16),(16,0),(9,10),(13,14)]
    key_input = True
    theta = np.array([
        [2.05064067563293e-06,-0.000351904972591015,	0.000256264733679187,	-0.000664684035815538,	0.00164841870612607,	-0.00103133317102957,	-0.00181393223446957,	-0.00270035346719531,	0.00245218403159737],
        [-9.06142907134185e-07,	-4.26633711249395e-05,	-0.000233358553995727,	0.00118144602783613,	-0.000986811128077120,	-0.00221609762951796,	0.000643575904861927,	0.00355762904201848,	-0.00195007203539372],
        [-7.44440148995003e-07,	0.00169185514753723,	1.73327428023696e-05,	-0.00345986744073806,	-0.000930933014666823,	0.000475494569325931,	0.00193878841202408,	-0.00306845835630751,	-0.00323873616320661],
        ])
    feature = np.ones([9,1])
    
    
    paper, scissor, rock = (2,0,1)
    ans = 'None'
    startt = 1
    
    try:
        for i,j in list_of_features:
            feature[startt,0] = find_len(lmList[i], lmList[j])
            startt += 1
        ans = theta.dot(feature)
        ans = np.argmax(ans)
        
        if ans == rock:
            return True
        else:
            return False
    except:
        pass
    return False
 

