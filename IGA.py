import itertools
import math
import random

class IGA():
    def __init__(self, population_size, mutation_prob, number_of_data):
        super(IGA, self).__init__()
        self.population_size = population_size
        self.generation = 0
        self.mutation_prob = mutation_prob
        '''number_of_data: ["height", "body shape", "lower body", "upper body",
                            "right_hand", "left_hand", "hair", "shape of face",
                            "eyes", "nose", "mouth", "ears"]'''
        self.number_of_data = number_of_data
        self.population = []
        self.selected_features = []
        self.chromosome_length = {0: 2, 1: 1, 2: 7, 3: 7, 4: 7, 5: 7, 6: 7,
                                  7: 7, 8: 7, 9: 7, 10: 7, 11: 7}

    def _generate_characters(self, num_of_characters):
        character = []
        for i in range(num_of_characters*len(self.number_of_data) + 1):
            index = (i + 1) % len(self.number_of_data)
            chromosome = random.randint(0, self.number_of_data[i%len(self.chromosome_length)] - 1)
            character.append(bin(chromosome)[2:].zfill(self.chromosome_length.get(i%len(self.chromosome_length))))
            if index == 0:
                self.population.append(character)
                character = []

    def _initial_population(self):
        self.generation += 1
        self._generate_characters(self.population_size)

    def _crossover(self, character_index):
        for chromosome_index, chromosome in enumerate(self.population[character_index][2:]):
            child_chromosome = math.ceil((int(chromosome, 2) + int(self.population[character_index+1][chromosome_index+2], 2)) / 2)
            self.population[character_index][chromosome_index+2] = bin(child_chromosome)[2:].zfill(7)
        del self.population[character_index+1]


    def _mutation(self):
        for index, characters in enumerate(self.population):
            for component_index, chromosome in enumerate(characters):
                component_not_exist = True
                while component_not_exist:
                    new_chromosome = []
                    for gene in chromosome:
                        mutation_prob = random.uniform(0, 1)
                        if self.mutation_prob > mutation_prob:
                            gene = 1 - int(gene)
                        new_chromosome.append(gene)
                    new_chromosome = ''.join(map(str, new_chromosome))
                    if int(new_chromosome, 2) < self.number_of_data[component_index]:
                        self.population[index][component_index] = new_chromosome
                        component_not_exist = False

    def _features_spreads(self):
        self.selected_features, spreaded_features = [], []
        for feature in self.population:
            self.selected_features.append(feature[:2])
        self.selected_features.sort()
        self.selected_features = list(self.selected_features for self.selected_features,_ in itertools.groupby(self.selected_features))
        num_of_selected_features = len(self.selected_features)
        if num_of_selected_features < 4:
            spreads = math.floor(self.population_size / num_of_selected_features)
            for feature in self.selected_features:
                for i in range(spreads):
                    spreaded_features.append(feature)
            self.selected_features = spreaded_features

    def _features_inherit(self):
        for index in range(len(self.population)):
            self.population[index][0] = self.selected_features[index][0]
            self.population[index][1] = self.selected_features[index][1]

    def _next_generation(self, selected_character):
        self.population = [a for a, b in zip(self.population, selected_character) if b == 1]
        if self.population:
            self._features_spreads()
            for i in range(math.floor(len(self.population) / 2)):
                self._crossover(i)
            self._features_inherit()
            self._mutation()
        if len(self.population) < self.population_size:
            self._generate_characters(self.population_size - len(self.population))
        self.generation += 1
