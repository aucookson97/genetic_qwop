from qwop_participant import Participant, Move
from math import sqrt, log, exp, e
import random
import operator
import csv
from os.path import isfile

first_name_file = 'first_names.txt'
last_name_file = 'last_names.txt'
first_names = []
last_names = []

total_participants = 0

participants = []

chance_mutation = .03 # Percent chance for any move to mutate (0-1)

percent_top_survive = .05 # Percent of highest fitness that will always survive


# Create Initial Population
def sixth_day(num_participants):
    global total_participants, first_names, last_names
    total_participants = num_participants
    #Load Name Files 
    file_first = open(first_name_file, 'r+')
    first_names = [line for line in file_first.readlines()]
    file_last = open(last_name_file, 'r+')
    last_names = [line for line in file_last.readlines()]

    for i in range(num_participants):
        first_name = getFirstName()
        last_name = getLastName()
        p = Participant(first_name, last_name)
        participants.append(p)

def clones(num_participants):
    global total_participants, first_names, last_names
    total_participants = num_participants
    #Load Name Files 
    file_first = open(first_name_file, 'r+')
    first_names = [line for line in file_first.readlines()]
    file_last = open(last_name_file, 'r+')
    last_names = [line for line in file_last.readlines()]
    
    first_name = getFirstName()
    last_name = getLastName()
    p = Participant(first_name, last_name)

    for i in range(num_participants):
        participants.append(p)

def evolve():
    #crossover_generational()
    crossover_steadystate()
    mutate()
    random.shuffle(participants)

def crossover_generational():
    participants.sort(key=operator.attrgetter('fitness'), reverse=True)
    participants_copy = participants.copy()

    del participants[:]

    for i in range(int(len(participants_copy) / 2 + .5)):
        parent1 = selectParent(participants_copy, None)
        parent2 = selectParent(participants_copy, parent1)
        participants.extend(reproduce(parent1, parent2, 'ONEPOINT'))

    if (len(participants) % 2 == 1): #One too many children, kill one
        del participants[len(participants)-1]

# Keep the x% top individuals and replace the rest with children
def crossover_steadystate():

    num_survive = int(len(participants) * percent_top_survive + .5)

    participants.sort(key=operator.attrgetter('fitness'), reverse=True)

    pop_size = len(participants)

    for i in range(num_survive, len(participants)):
        if participants[i].fitness < 0:
            del participants[i:]
            break
    
    participants_copy = participants.copy()

    # The first x% are guarunteed to survive
    #del participants[num_survive:]
    for i in range(int((pop_size - len(participants)) / 2 + .5)):
        parent1 = selectParent(participants_copy, None)
        parent2 = selectParent(participants_copy, parent1)
        participants.extend(reproduce(parent1, parent2, 'ONEPOINT'))

    if (len(participants) % 2 == 1): #One too many children, kill one
        del participants[len(participants)-1]

#Roulette Wheel Selection Exp
def selectParent(p, other_parent):
    size = len(p)
    parent = other_parent
    while parent == other_parent:
        #selection = int(-log(random.random()) * size/4)
        yint = e - 1.0
        selection = int(-size*log(random.random()*yint+1)+size)
        if selection >= len(p):
            selection = len(p) - 1
        parent = p[selection]
    return parent

#Roulette Wheel Selection
##def selectParent(p, other_parent):
##    parent = other_parent
##    while (parent == other_parent):
##        total_area = 0
##        for i in range(len(p)):      
##            slice_size = 1.0/sqrt(2) * log(i, 10)
##            total_area += slice_size
##        selection = random.random() * total_area
##
##        last_area = 0
##        for i in range(len(p)):
##            next_area = last_area + 1.0/sqrt(2) * log(i, 10)
##            if (selection >= last_area and selection < area):
##                parent = p[i]
##            last_area += area
##    return parent
      
def mutate():
    num_survive = int(len(participants) * percent_top_survive + .5)
    for i in range(num_survive, len(participants)):
        p = participants[i]
        for i in range(len(p.moves)):
            if (random.random() < chance_mutation):
                p.moves[i].mutate()
                

def reproduce(parent1, parent2, algorithm):
##    if random.randint(0, 1):
##        first_name = parent1.first_name
##        last_name = parent2.last_name
##    else:
##        first_name = parent2.first_name
##        last_name = parent1.last_name
        
    moves1 = []
    moves2 = []
    if algorithm == 'UNIFORM': #Each Allele is randomly selected from P1 or P2
        num_moves = len(parent1.moves)
        for i in range(num_moves):
            if random.randint(0, 1):
                moves1.append(parent1.moves[i])
                moves2.append(parent2.moves[i])
            else:
                moves1.append(parent2.moves[i])
                moves2.append(parent1.moves[i])
    if algorithm == 'ONEPOINT': # DNA Substrings are combined at a specific split point
        num_moves = len(parent1.moves)
        split_point = random.randint(0, num_moves)
        #if random.randint(0, 1) == 0:
        moves1 = parent1.moves[:split_point] + parent2.moves[split_point:]
        #else:
        moves2 = parent2.moves[:split_point] + parent1.moves[split_point:]
    
    return [Participant(getFirstName(), getLastName(), moves1, parent1, parent2),
            Participant(getFirstName(), getLastName(), moves2, parent2, parent1)]

def save_population(filename, generation, verbose):
   # print ('Saving Current Population to {}'.format(filename))
    if not isfile(filename):
        with open(filename, 'a', newline = '') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['First Name', 'Last Name', 'Parent 1', 'Parent 2', 'Fitness'])
    if verbose:
        command = 'a'
    else:
        command = 'w'
    with open(filename, command, newline = '') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if command == 'w':
            writer.writerow(['First Name', 'Last Name', 'Parent 1', 'Parent 2', 'Fitness'])
        writer.writerow(['Generation', generation])
        for p in participants:
            row = []
            parents = p.getParents()
            row.extend([p.first_name, p.last_name, p.fitness, parents[0], parents[1]])
            for m in p.moves:
                row.extend([m.keys, m.time_press, m.time_release])
            writer.writerow(row)

def load_population(filename):
    global participants
    del participants[:]
    print ('Loading Population from {}'.format(filename))
    with open(filename, 'r', newline = '') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] == 'Generation' or row[0] == 'First Name':
                continue
            moves = []
            for i in range(5, len(row), 3):
                moves.append(Move(int(row[i]), float(row[i+1]), float(row[i+2])))
            participants.append(Participant(row[0], row[1], moves, row[2], row[3]))
    print ('Successfully Loaded {} Participants'.format(len(participants)))

def save_stats(filename, generation):
    if not isfile(filename):
        with open(filename, 'a', newline = '') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['Mutation Chance', chance_mutation * 100])
            writer.writerow(['Steady State Percent', percent_top_survive])
            writer.writerow(['Generation', 'Minimum Fitness', 'Maximum Fitness', 'Mean Fitness'])
    
   # print ('Saving Generation Statistics to {}'.format(filename))
    with open(filename, 'a', newline = '') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        min_fit, max_fit = fitness_bounds()
        writer.writerow([generation, min_fit, max_fit, mean_fitness()])
           
def display_stats():
    print ('Population Statistics:')
    min_fit, max_fit = fitness_bounds()
    print ('\tMinimum Fitness: {}'.format(min_fit))
    print ('\tMaximum Fitness: {}'.format(max_fit))
    print ('\tAverage Fitness: {}'.format(mean_fitness()))

def getFirstName():
    first_name = random.choice(first_names).rstrip('\n')
    return first_name

def getLastName():
    last_name = random.choice(last_names).rstrip('\n')
    return last_name

def display_fitness():
    for p in participants:
        p.display_fitness()

# Displays the Entire Population
def display_population():
    for p in participants:
        p.display()

def mean_fitness():
    total_fitness = 0
    for i in range(len(participants)):
        total_fitness += participants[i].fitness
    return float(total_fitness) / len(participants)

def fitness_bounds():
    max_fit = -10000
    min_fit = 10000
    for p in participants:
        if p.fitness > max_fit:
            max_fit = p.fitness
        if p.fitness < min_fit:
            min_fit = p.fitness
    return (min_fit, max_fit)

