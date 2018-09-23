from qwop_participant import Participant
import random

first_name_file = 'first_names.txt'
last_name_file = 'last_names.txt'

participants = []

# Create Initial Population
def sixth_day(num_participants):
    #Load Name Files 
    file_first = open(first_name_file, 'r+')
    first_names = [line for line in file_first.readlines()]
    file_last = open(last_name_file, 'r+')
    last_names = [line for line in file_last.readlines()]

    for i in range(num_participants):
        name = random.choice(first_names).rstrip('\n') + ' ' + random.choice(last_names).rstrip('\n')
        p = Participant(name)
        participants.append(p)


# Displays the Entire Population
def display_population():
    for p in participants:
        p.display()
