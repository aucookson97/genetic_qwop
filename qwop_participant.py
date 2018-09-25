import pyautogui as auto
import time
import random

num_moves = 10

# Time is in Seconds
min_time_press = 0.0
max_time_press = 1.0
min_time_release = 0.0
max_time_release = 1.0


class Participant():


    def __init__(self, first_name, last_name, moves=None):

        self.first_name = first_name
        self.last_name = last_name
        self.fitness = 0.0
        self.current_move = 0

        if moves == None:
            self.moves = []
            # Generate Random Move List
            for i in range(num_moves):
                keys = random.randint(0, 15)
                time_press = min_time_press + random.random() * (max_time_press - min_time_press)
                time_release = min_time_release + random.random() * (max_time_release - min_time_release)
                self.moves.append(Move(keys, time_press, time_release))
        else:
            self.moves = moves

    def nextMove(self):
        self.moves[self.current_move].execute()
        self.current_move += 1
        if self.current_move >= len(self.moves):
            self.current_move = 0

    def move(self):
        for m in self.moves:
            m.execute()

    def display_fitness(self):
        print ('{} {}: {}'.format(self.first_name, self.last_name, self.fitness))

    def display(self):
        print ()
        print ('Name: {} {}'.format(self.first_name, self.last_name))
        print ('\tFitness: {}'.format(self.fitness))
        print ('\tMove List:')
        for m in self.moves:
            keys = ''
            if m.keys & 8:
               keys += 'Q'
            if m.keys & 4:
               keys += 'W'
            if m.keys & 2:
               keys += 'O'
            if m.keys & 1:
               keys += 'P'
            print ('\t\tKeys: {}'.format(keys))
            print ('\t\t\tPress Time: {}'.format(m.time_press))
            print ('\t\t\tRelease Time: {}'.format(m.time_release)  )


class Move():

    def __init__(self, keys, time_press, time_release):

        # Binary, QWOP
        self.keys = keys
        # Time Keys are Pressed
        self.time_press = time_press
        # Time to wait after move 
        self.time_release = time_release

    def mutate(self):
        keys = random.randint(0, 15)
        time_press = min_time_press + random.random() * (max_time_press - min_time_press)
        time_release = min_time_release + random.random() * (max_time_release - min_time_release)
        self.keys = keys
        self.time_press = time_press
        self.time_release = time_release

    def execute(self):
        if self.keys & 8: #Q
            auto.keyDown('q')
        if self.keys & 4: #W
            auto.keyDown('w')
        if self.keys & 2: #O
            auto.keyDown('o')
        if self.keys & 1: #P
            auto.keyDown('p')
            
        time.sleep(self.time_press)

        auto.keyUp('q')
        auto.keyUp('w')
        auto.keyUp('o')
        auto.keyUp('p')

        time.sleep(self.time_release)


    
