import pytesseract
import pyautogui as auto
from mss import mss
import cv2
import numpy as np
import population as pop
import time

sct = mss()

seven_template = cv2.imread('seven.png', 0)
# (X, Y, Width, Height) Box to capture

#100% Zoom
##mon = {'top': 460, 'left': 764, 'width': 372, 'height': 186}
##text_window = {'top': 79, 'bottom': 114, 'left': 76, 'right': 294}

#200% Zoom
mon = {'top': 350, 'left': 577, 'width': 744, 'height': 373}
text_window = {'top': 165, 'bottom': 227, 'left': 152, 'right': 588}
medal_window = {'top': 33, 'bottom': 43, 'left': 33, 'right': 43}

def run():

    # Generate Initial Population
    pop.sixth_day(30)

    generation = 0

    # Wait for User to Press 'Space' (Start)
    print ('Waiting for User to Start...')
    img = np.array(sct.grab(mon))
   # cv2.imshow('img', img)
    #cv2.waitKey(0)
    while participant_lost(img):
        img = np.array(sct.grab(mon))
    print ('Starting Evolution')

    running = True # Literally Running
    while running:

        generation += 1
        print ('\nGeneration: {}'.format(generation))

        for participant in pop.participants:
            auto.press('space') # Restart Race
            img = np.array(sct.grab(mon))

            # Execute Moves in Order Until Participant has Lost
            while not participant_lost(img = np.array(sct.grab(mon))):
                participant.nextMove()
                img = np.array(sct.grab(mon))

            # Read Score                       
            img = np.array(sct.grab(mon))
            score = read_score(img)
            participant.fitness = score

        pop.evolve()
        pop.display_stats()

def read_score(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Crop Text and Medal Windows
    img_text = img_gray[text_window['top']:text_window['bottom'], text_window['left']:text_window['right']]
    #cv2.imshow('image', img_text)
   # cv2.waitKey(0)
    # Binarize Text
    ret, text_binary = cv2.threshold(img_text, 127, 255, cv2.THRESH_BINARY)

    text = str(pytesseract.image_to_string(text_binary))
    text = text.replace(' ', '')

##    if '1' in text:
##        res = cv2.matchTemplate(img_text, seven_template, cv2.TM_CCOEFF_NORMED)
##        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
##        top_left = max_loc
##        w, h = seven_template.shape[::-1]
##        bottom_right = (top_left[0] + w, top_left[1] + h)
##        print (res)
##        print (cv2.minMaxLoc(res))
##        cv2.rectangle(img_text,top_left, bottom_right, 255, 2)
##        cv2.imshow('Text', img_text)
##        cv2.waitKey(0)
    try:
        raw_score = float(text[:len(text)-6])
    except ValueError:
        print ('Could not successfully read score')
        raw_score = -1000
    return raw_score

def save_population(filename):
    with open(filename, 'w') as csvfile:
        writer = csv.writer(delimiter=',')

def participant_lost(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img_medal = img_hsv[medal_window['top']:medal_window['bottom'], medal_window['left']:medal_window['right'], :]
    # Look for Yellow Medal
    medal_mean_hue = int(np.mean(np.mean(img_medal, axis=0), axis=0)[0] + .5)
    # Participant Lost, Detected Yellow Medal
    return medal_mean_hue == 30

if __name__ == "__main__":
    run()
