import pytesseract
from mss import mss
import cv2
import numpy as np


sct = mss()
# (X, Y, Width, Height) Box to capture

#100% Zoom
##mon = {'top': 460, 'left': 764, 'width': 372, 'height': 186}
##text_window = {'top': 79, 'bottom': 114, 'left': 76, 'right': 294}

#200% Zoom
mon = {'top': 357, 'left': 577, 'width': 744, 'height': 373}
text_window = {'top': 158, 'bottom': 227, 'left': 152, 'right': 588}

while 1:
    img = np.array(sct.grab(mon))
   # img_text = cv2.imread('C:\\Users\\Aidan\\Documents\\git_repos\\genetic_qwop\\example_text.png')
    img_text = img[text_window['top']:text_window['bottom'], text_window['left']:text_window['right'], :]
    ret, text_binary = cv2.threshold(img_text, 127, 255, cv2.THRESH_BINARY)

    

    cv2.imshow('test', text_binary)
    text = pytesseract.image_to_string(text_binary)
    print (text)
    #Press 'Q' to quit
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

