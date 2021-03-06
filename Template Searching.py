import cv2
from PIL import Image, ImageGrab, ImageDraw, ImageFilter
import numpy as np
from matplotlib import pyplot as plt
import pytesseract


template = cv2.imread('poker/pics/ps/qs.png')
img = cv2.imread('poker/pics/ps/screenshot w7.png')

def find_card_in_image(template, img):

    img2 = img.copy()
    w, h = template.shape[1],template.shape[0]

    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    all_top_lefts = []
    for meth in methods:
        img = img2.copy()
        method = eval(meth)

        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        loc = np.where(res <= 0.1)

        print(res.shape)
        print img.shape
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

        cv2.imwrite(meth+' res.png', img)
        #print('image located at: ',top_left, ' for method:',meth)
        bottom_right = (top_left[0] + w, top_left[1] + h)
        all_top_lefts.append(top_left[0])
        cv2.rectangle(img,top_left, bottom_right, 255, 2)


        #plt.subplot(121),plt.imshow(res,cmap = 'gray')
        #plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        #plt.subplot(122),plt.imshow(img,cmap = 'gray')
        #plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        #plt.suptitle(meth)

        #plt.show()

    return np.mean(all_top_lefts), np.std(all_top_lefts)



values = "23456789TJQKA"
suites = "CDHS"
for x in values:
    for y in suites:
        path = 'poker/pics/ps/'+x+y+'.png'
        template = cv2.imread(path)
        img = cv2.imread('poker/pics/ps/screenshot w7.png')
        print(x+y,"found at", find_card_in_image(template, img))

#x= 'q'
#y = 's'
#print(x+y,"found at", find_card_in_image(template, img))
img_orig =Image.open('snip1.png')
#basewidth = 200
#wpercent = (basewidth / float(img_orig.size[0]))
#hsize = int((float(img_orig.size[1]) * float(wpercent)))
#img_resized = img_orig.resize((basewidth, hsize), Image.ANTIALIAS)

#img_min = img_resized.filter(ImageFilter.MinFilter)
#img_med = img_resized.filter(ImageFilter.MedianFilter)
#img_mod = img_orig.filter(ImageFilter.ModeFilter).filter(ImageFilter.SHARPEN)




#print pytesseract.image_to_string(img_orig)