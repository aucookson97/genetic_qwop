from qwop_participant import Participant
from math import sqrt, log
import random
import operator

first_name_file = 'first_names.txt'
last_name_file = 'last_names.txt'

total_participants = 0

participants = []

chance_mutation = .01 # Percent chance for any move to mutate (0-1)

percent_top_survive = .3 # Percent of highest fitness that will always survive

# Create Initial Population
def sixth_day(num_participants):
    global total_participants
    total_participants = num_participants
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
    print (total_participants)
    print ('Evolving')
    display_fitness()
    crossover()
    mutate()

def crossover():

    num_survive = int(len(participants) * percent_top_survive + .5)

    participants.sort(key=operator.attrgetter('fitness'), reverse=True)
    participants_copy = participants.copy()

    # The first x% are guarunteed to survive
    del participants[num_survive:]
    
    # The rest have a decaying chance of survival
    for i in range(num_survive, len(participants_copy)):  
        chance = 1.0/sqrt(2) * log(i, 10)
        if (random.random() >= chance):
            participants.append(participants_copy[i])

    children = []

    # Populate the rest of the list with children
    for i in range(total_participants - len(participants)):
        parent1 = random.choice(participants)
        parent2 = random.choice(participants)

        while (parent1 == parent2):
            parent2 = random.choice(participants)
        children.append(child(parent1, parent2, 'RANDOM'))
    participants.extend(children)

      
def mutate():
    for p in participants:
        for i in range(len(p.moves)):
            if (random.random() < chance_mutation):
                p.moves[i].mutate()
                

def child(parent1, parent2, algorithm):
    if random.randint(0, 1):
        first_name = parent1.first_name
        last_name = parent2.last_name
    else:
        first_name = parent2.first_name
        last_name = parent1.last_name
    
    if algorithm == 'RANDOM':
        num_moves = len(parent1.moves)
        moves = []
        for i in range(num_moves):
            if random.randint(0, 1):
                moves.append(parent1.moves[i])
            else:
                moves.append(parent2.moves[i])
    
    return Participant(first_name, last_name, moves)

def display_stats():
    total_fitness = 0
    for i in range(len(participants)):
        total_fitness += participants[i].fitness
    mean_fitness = float(total_fitness) / len(participants)
    
    print ('Population Statistics:')
    print ('\tAverage Fitness: {}'.format(mean_fitness))
    

def display_fitness():
    for p in participants:
        p.display_fitness()

# Displays the Entire Population
def display_population():
    for p in participants:
        p.display()

