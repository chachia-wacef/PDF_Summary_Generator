import cv2
import numpy as np
import pytesseract

########################################################################################
def detectColor(img, hsv):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #cv2.imshow('imageHSV',imgHSV)
    lower = np.array([hsv[0], hsv[2], hsv[4]])
    upper = np.array([hsv[1], hsv[3], hsv[5]])
    #'Threshold' l'image pour obtenir seulement une couleur
    mask = cv2.inRange(imgHSV, lower, upper)
    #extraction des parties importants de l'image
    imgResult = cv2.bitwise_and(img, img, mask=mask)
    return imgResult

########################################################################################
def getContours(img, imgDraw, cThr=[100, 100], showCanny=False, minArea=50, filter=0, draw=False):
    imgDraw = imgDraw.copy()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])

    kernel = np.array((10, 10))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=1)
    imgClose = cv2.morphologyEx(imgDial, cv2.MORPH_CLOSE, kernel)

    if showCanny: 
      cv2.imshow('image contours',imgClose)

    contours, hiearchy = cv2.findContours(imgClose, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    finalCountours = []
    for i in contours:
        area = cv2.contourArea(i)
        if area > minArea:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            bbox = cv2.boundingRect(approx)
            if filter > 0:
                if len(approx) == filter:
                    finalCountours.append([len(approx), area, approx, bbox, i])
            else:
                finalCountours.append([len(approx), area, approx, bbox, i])

    finalCountours = sorted(finalCountours, key=lambda x: x[1], reverse=True)

    if draw:
        for con in finalCountours:
            x, y, w, h = con[3]
            cv2.rectangle(imgDraw, (x, y), (x + w, y + h), (255, 0, 255), 3)
            # cv2.drawContours(imgDraw,con[4],-1,(0,0,255),2)
            
    return imgDraw, finalCountours


########################################################################################
#enregistrer les phrases extraites
def saveText(highlightedText):
  with open('HighlightedText.txt', 'w') as f:
    for text in highlightedText:
      f.writelines(f'\n{text}')

##############################################   Main Program   ##########################################

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'



path = 'image1.png'
#Upper color
#lower_red = np.array([170,50,50])
#upper_red = np.array([180,255,255])
#lower = np.array([hsv[0], hsv[2], hsv[4]])
#upper = np.array([hsv[1], hsv[3], hsv[5]])


hsv = [170,180,50,255,50,255]

#### Step 1 ####
img = cv2.imread(path)
img = cv2.resize(img,(1000,1000),interpolation = cv2.INTER_NEAREST)
cv2.imshow('my image',img)
#### Step 2 ####
imgResult = detectColor(img, hsv)
cv2.imshow('detect color',imgResult)
#### Step 3 & 4 ####
imgContours, contours = getContours(imgResult, img, showCanny=False, #to show detected contours
                                    minArea=50, filter=0,   ###if filter > 0 , it represent the number of sides of the polygon detected 
                                    cThr=[200, 100], draw=False) ###to draw or not the detected contours
cv2.imshow('Final contours',imgContours)
print(len(contours))

cv2.waitKey(0)
#when we close all precedent windows , the extraction and the saving of text will begin

#######################
#Next step : we will crop these contours , then use the pytesseract library to extract text in this cropped images
#######################

highlightedText = []

for con in contours:
    x, y, w, h = con[3]
    img_text = imgContours[y:y+h,x:x+w]
    img_text1 = cv2.cvtColor(img_text,cv2.COLOR_BGR2RGB)
    cv2.imshow('imagetext',img_text1)
    texts = pytesseract.image_to_data(img_text1,output_type='data.frame') #it give us a dataframe
    print('****************************')
    ch = ''
    for k in range(len(texts)):
        el = texts['text'].iloc[k]
        if el is not np.NaN :
            ch = ch + el + ' '
    print(ch) 
    if len(ch) > 0 :
        highlightedText.append(ch) 

saveText(highlightedText)
    
####Next possibles steps :
#optimization of the result of pytesseract
