import cv2
import os
import argparse
import plaque_size_tool as pst
import pandas as pd
import util

args = util.parse_args()
FILENAME = args['image']
FILENAME_NOEXT = os.path.splitext(FILENAME)[0]

source = 0
camera = cv2.VideoCapture(source)
if camera is None or not camera.isOpened():
    raise Exception('Unable to open video source: '+str(source))

processing = False
count=0
resizeWidth = 600

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

print("Press 's' to save image and process plaques")
print("Press 'x' to exit program")

while True:
    if not processing:
        return_value, image = camera.read()
        resize = ResizeWithAspectRatio(image, width=resizeWidth) # Resize by width OR

        #gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        #cv2.imshow('image',gray)
        cv2.imshow('image',resize)
    
    #if count==limit or cv2.waitKey(1)& 0xFF == ord('s'):
    if cv2.waitKey(1)& 0xFF == ord('s'):
        print("Processing image...")
        processing = True
        cv2.imwrite(FILENAME,image)

        #CALL = "plaque_size_tool.py -i "+FILENAME+" -p 90 -small"
        #print(CALL)
        #os.system(CALL)
        foundList = pst.main(args) #raw output ./out/data-green-FILE.csv, edited image in ./out/out_FILENAME
        numFound = foundList[0]
        print(numFound,'plaques found')
        if numFound > 0:
            DATAOUTPATH = 'out/data-green-'+FILENAME_NOEXT+'.csv'
            summary = pd.read_csv(DATAOUTPATH)
            print(summary.head())

        IMAGEOUTPATH = 'out/out_'+FILENAME
        imgOut = cv2.imread(IMAGEOUTPATH) #, 0) 
        resizeOut = ResizeWithAspectRatio(imgOut, width=resizeWidth) # Resize by width OR
        cv2.imshow('image2',resizeOut)
        processing = False
        #break
    #count +=1
    if cv2.waitKey(1)& 0xFF == ord('x'):
        break

camera.release()
cv2.destroyAllWindows()




