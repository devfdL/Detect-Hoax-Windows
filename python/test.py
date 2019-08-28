from PIL import Image
import pytesseract
import argparse
import cv2
import os
import time
 
def ImgData():
    start = time.time()
    # load the example image and convert it to grayscale
    image = cv2.imread('../img/info.jpg')
    while True:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        filename = "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)

        # load the image as a PIL/Pillow image, apply OCR, and then delete
        #the temporary file
        text = pytesseract.image_to_string(Image.open(filename))
        os.remove(filename)
        print(text)
        os.remove('../data/text.txt')
        f = open('../data/text.txt','a')
        f.write(text)

        # show the output images
        cv2.imshow("Image", image)
        #cv2.imshow("Output", gray)

        if len(text) > 1:
            break

    end = time.time()
    estimated = end - start
    print('\ncomplete in ' + str(estimated) +'s')
    image.release()
    cv2.destroyAllWindows()

ImgData()


