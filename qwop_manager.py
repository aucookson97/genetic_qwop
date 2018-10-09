import pytesseract
import pyautogui as auto
from mss import mss
import cv2
import numpy as np
import population as pop
import time
import sys, getopt
from os import mkdir, path

#pytesseract.pytesseract.tesseract_cmd = 'C:\\Users\\Aidan\\AppData\\Local\\Programs\\Python\\Python37-32\\Lib\\site-packages\\pytesseract'
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

num_trials = 1 # How many tries each participant gets to prove its worth
speedhack = 1.0
time_limit = 300 / speedhack # Maximum Time for each participant in seconds


sct = mss()

# (X, Y, Width, Height) Box to capture

#100% Zoom
##mon = {'top': 460, 'left': 764, 'width': 372, 'height': 186}
##text_window = {'top': 79, 'bottom': 114, 'left': 76, 'right': 294}

#200% Zoom
#mon = {'top': 350, 'left': 577, 'width': 744, 'height': 373}
#text_window = {'top': 165, 'bottom': 227, 'left': 152, 'right': 588}
#medal_window = {'top': 33, 'bottom': 43, 'left': 33, 'right': 43}

#Internet Explorer
mon = {'top': 350, 'left': 560, 'width': 782, 'height': 392}
text_window = {'top': 169, 'bottom': 236, 'left': 197, 'right': 597}
medal_window = {'top': 32, 'bottom': 42, 'left': 33, 'right': 43}

def run(input_file, output_dir, pop_size, max_gen, verbose):

    if not path.exists('Worlds'):
        mkdir('Worlds')

    if output_dir == '':
        dt = time.strftime("%Y%m%d_%H%M%S")
        output_dir = 'World_' + dt
    try:
        mkdir('Worlds\\' + output_dir)
    except FileExistsError:
        print ('Directory {} Exists! Potential Data Overwrite!'.format(output_dir))
        ans = '1'
        while (ans != 'Y' and ans != 'N'):
            ans = input('Continue[Y/N]? ')
        if ans == 'N':
            sys.exit(0)

    # Generate Initial Population
    if input_file == '':
        pop.sixth_day(pop_size)
        #pop.clones(10)
    else:
        pop.load_population(input_file)

    generation = 0

    # Wait for User to Press 'Space' (Start)
    print ('Waiting for User to Start...')
    img = np.array(sct.grab(mon))
   # cv2.imshow("img", img)
   # cv2.waitKey(0)
    while participant_lost(img):
        img = np.array(sct.grab(mon))

    print ('Starting Evolution')

    generaton = 0
    while generation < max_gen:

        generation += 1
        print ('\n\n***Generation {}***'.format(generation))

        participant_num = 0
        for participant in pop.participants:

            best_fitness = -1000.0
            participant_num += 1
            print ('G{}: {} {} ({}/{})'.format(generation, participant.first_name, participant.last_name, participant_num, len(pop.participants)))
            for i in range(num_trials):
                participant.current_move = 0
                auto.press('space') # Restart Race
                img = np.array(sct.grab(mon))

                # Execute Moves in Order Until Participant has Lost
                start_time = time.time()
                time.sleep(.5 / speedhack) #Wait for participant to reach the ground
                while not participant_lost(img = np.array(sct.grab(mon))):
                    if (time.time() - start_time >= time_limit):
                        kill_participant()
                    else:
                        participant.nextMove()
                    img = np.array(sct.grab(mon))


                # Read Score                       
                img = np.array(sct.grab(mon))
                score = read_score(img)
                if score > best_fitness:
                    best_fitness = score
                print ('\t\tTrial Fitness: {}'.format(score))

            participant.fitness = best_fitness   
            print ('\tBest Fitness: {}'.format(best_fitness))

        pop_save_name = 'Worlds\\' + output_dir + '\\' + 'Population.csv'.format(generation)
        stats_save_name = 'Worlds\\' + output_dir + '\\' + 'Stats.csv'.format(generation)

        pop.save_population(pop_save_name, generation, verbose)
        pop.save_stats(stats_save_name, generation)
        pop.display_stats()
        pop.evolve()

def kill_participant():
    print ('Time Limit Reached! Executing Participant...')
    auto.keyDown('q')
    auto.keyDown('w')
    time.sleep(.25 / speedhack)
    auto.keyUp('q')
    auto.keyUp('w')
    auto.keyDown('p')
    auto.keyDown('o')
    time.sleep(.25 / speedhack)
    auto.keyUp('p')
    auto.keyUp('o')
    time.sleep(.25 / speedhack)
    auto.keyDown('q')
    auto.keyDown('p')
    time.sleep(.25 / speedhack)
    auto.keyUp('q')
    auto.keyUp('p')
    auto.keyDown('w')
    auto.keyDown('o')
    time.sleep(.25 / speedhack)
    auto.keyUp('w')
    auto.keyUp('o')

def read_score(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Crop Text and Medal Windows
    img_text = img_gray[text_window['top']:text_window['bottom'], text_window['left']:text_window['right']]
   # cv2.imshow('image', img_text)
    #cv2.waitKey(0)
    # Binarize Text
    ret, text_binary = cv2.threshold(img_text, 127, 255, cv2.THRESH_BINARY)

    text = str(pytesseract.image_to_string(text_binary))
    text = text.replace(' ', '')

##    if '1' in text:p
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
    
    input_file = ''
    output_dir = ''
    pop_size = 30
    max_gen = 500
    verbose = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hvi:o:p:g:', ["ifile=","odir=", "pop=", "gen=", "--verbose"])
    except getopt.GetoptError:
        print ('qwop_manager.py -i <input_file(csv)> -o <output_directory> -p <Population Size (int)> -g <# Generations (int)> -v (Verbose)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('qwop_manager.py -i <input_file(csv)> -o <output_directory> -p <Population Size (int)> -g <# Generations (int)> -v (Verbose)')
            sys.exit()
        elif opt in ("-p", "--pop"):
            pop_size = int(arg)
        elif opt in ("-g", "--gen"):
            max_gen = int(arg)
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--odir"):
            output_dir = arg
        elif opt in ("-v", "--verbose"):
            verbose = True

    #print ('Input File: {}'.format(input_file))
    #print ('Output Dir: {}'.format(output_dir))

    if (pop_size % 2 == 1): # Make Sure Population is Even
        pop_size += 1
        
    run(input_file, output_dir, pop_size, max_gen, verbose)
