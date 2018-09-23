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
        first_name = random.choice(first_names).rstrip('\n')
        last_name = random.choice(last_names).rstrip('\n')
        p = Participant(first_name, last_name)
        participants.append(p)


def evolve():
    print ('Evolving')

def child(parent1, parent2, algorithm):

    if random.randint(0, 1):
        first_name = parent1.first_name
        last_name = parent2.last_name
    else:
        first_name = parent2.first_name
        last_name = parent1.last_name
    
    if algorithm == 'Random':
        num_moves = len(parent1.moves)
        moves = []
        for i in range(num_moves):
            if random.randint(0, 1):
                moves.append(parent1.moves[i])
            else:
                moves.append(parent2.moves[i])

def display_fitness():
    for p in participants:
        p.display_fitness()

# Displays the Entire Population
def display_population():
    for p in participants:
        p.display()
