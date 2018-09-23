import pytesseract
from mss import mss
import cv2
import numpy as np
import population as pop

sct = mss()
# (X, Y, Width, Height) Box to capture

#100% Zoom
##mon = {'top': 460, 'left': 764, 'width': 372, 'height': 186}
##text_window = {'top': 79, 'bottom': 114, 'left': 76, 'right': 294}

#200% Zoom
mon = {'top': 357, 'left': 577, 'width': 744, 'height': 373}
text_window = {'top': 158, 'bottom': 227, 'left': 152, 'right': 588}
medal_window = {'top': 33, 'bottom': 43, 'left': 33, 'right': 43}

def run():

    pop.sixth_day(10)
    pop.display_population()

    running = False
    while running:
        img = np.array(sct.grab(mon))
        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Crop Text and Medal Windows
        img_text = img_gray[text_window['top']:text_window['bottom'], text_window['left']:text_window['right']]
        img_medal = img_hsv[medal_window['top']:medal_window['bottom'], medal_window['left']:medal_window['right'], :]

        # Binarize Text
        ret, text_binary = cv2.threshold(img_text, 127, 255, cv2.THRESH_BINARY)

        # Look for Yellow Medal
        medal_mean_hue = int(np.mean(np.mean(img_medal, axis=0), axis=0)[0] + .5)
     
        if medal_mean_hue == 30: # Participant Lost, Detected Yellow Medal
            text = str(pytesseract.image_to_string(text_binary))
           
            text = text.replace(' ', '')
            try:
                raw_score = float(text[:len(text)-6])
            except ValueError:
                print ('Could not successfully read score')
                raw_score = -1000
                
            
            print ('Score: {}'.format(raw_score))

        #Press 'Q' to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    run()
