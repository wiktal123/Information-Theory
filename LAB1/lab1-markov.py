import os, random

class load_data:
    current_directory = os.getcwd()
    paths = os.listdir(current_directory)

    def first_order(self):
        occurrencies = dict()
        total_chars = 0

        for path in self.paths:
            if path.startswith('norm'):
                with open(path, 'r') as file: 
                    lines = file.readlines()

                    for line in lines:
                        for char in line:
                            occurrencies[char] = occurrencies.get(char, 0) + 1
                            total_chars += 1

        probabilities = {char: occurrence / total_chars for char, occurrence in occurrencies.items()}
        return probabilities

    def second_order(self):
        occurrencies = dict()
        total_slices = 0

        for path in self.paths:
            if path.startswith('norm'):
                with open(path, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        for i in range(len(line) - 1):
                            slice = line[i:i+2]
                            if slice[0] not in occurrencies:
                                occurrencies[slice[0]] = dict()
                            occurrencies[slice[0]][slice[1]] = occurrencies[slice[0]].get(slice[1], 0) + 1
                            total_slices += 1

        probabilities = {char: {k: v / sum(occurrencies[char].values()) for k, v in occurrencies[char].items()}
                         for char in occurrencies}
        return probabilities

    def third_order(self):
        occurrencies = dict()

        for path in self.paths:
            if path.startswith('norm'):
                with open(path, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        for i in range(len(line) - 2):
                            slice = line[i:i+3]
                            if slice[0] not in occurrencies:
                                occurrencies[slice[0]] = dict()
                            if slice[1] not in occurrencies[slice[0]]:
                                occurrencies[slice[0]][slice[1]] = dict()

                            occurrencies[slice[0]][slice[1]][slice[2]] = occurrencies[slice[0]][slice[1]].get(slice[2], 0) + 1

        probabilities = {char1: {char2: {char3: count / sum(third_level.values())
                                         for char3, count in third_level.items()}
                                 for char2, third_level in second_level.items()}
                         for char1, second_level in occurrencies.items()}
        return probabilities

    def fifth_order(self):
        occurrencies = dict()

        for path in self.paths:
            if path.startswith('norm'):
                with open(path, 'r') as file:
                    lines = file.readlines()
                    for line in lines:
                        for i in range(len(line) - 4):
                            slice = line[i:i+5]

                            if slice[0] not in occurrencies:
                                occurrencies[slice[0]] = dict()
                            if slice[1] not in occurrencies[slice[0]]:
                                occurrencies[slice[0]][slice[1]] = dict()
                            if slice[2] not in occurrencies[slice[0]][slice[1]]:
                                occurrencies[slice[0]][slice[1]][slice[2]] = dict()
                            if slice[3] not in occurrencies[slice[0]][slice[1]][slice[2]]:
                                occurrencies[slice[0]][slice[1]][slice[2]][slice[3]] = dict()

                            occurrencies[slice[0]][slice[1]][slice[2]][slice[3]][slice[4]] = occurrencies[slice[0]][slice[1]][slice[2]][slice[3]].get(slice[4], 0) + 1

        probabilities = {
            char0: {
                char1: {
                    char2: {
                        char3: {
                            char4: count / sum(fifth_level.values())
                            for char4, count in fifth_level.items()
                        } for char3, fifth_level in fourth_level.items()
                    } for char2, fourth_level in third_level.items()
                } for char1, third_level in second_level.items()
            } for char0, second_level in occurrencies.items()
        }
        return probabilities

def generate_first_order(sentence_length, probabilities):
    sentence = ''.join(random.choices(list(probabilities.keys()), weights=probabilities.values(), k=sentence_length))
    return sentence

def generate_second_order(sentence_length, probabilities):
    sentence = generate_first_order(1, load_data().first_order())

    for _ in range(sentence_length - 1):
        prev = sentence[-1]
        next_chars = probabilities.get(prev, None)

        if next_chars:
            choice = random.choices(list(next_chars.keys()), weights=next_chars.values(), k=1)[0]
            sentence += choice
        else:
            sentence += generate_first_order(1, load_data().first_order())
    return sentence

def generate_third_order(sentence_length, probabilities):
    sentence = generate_second_order(2, load_data().second_order())

    for _ in range(sentence_length - 2):
        prev = sentence[-2:]
        next_chars = probabilities.get(prev[0], {}).get(prev[1], None)

        if next_chars:
            choice = random.choices(list(next_chars.keys()), weights=next_chars.values(), k=1)[0]
            sentence += choice
        else:
            sentence += generate_first_order(1, load_data().first_order())
    return sentence

def generate_fifth_order(sentence_length, probabilities):
    sentence = "probability " 

    for _ in range(sentence_length - len(sentence)):
        prev = sentence[-4:]
        next_chars = probabilities.get(prev[0], {}).get(prev[1], {}).get(prev[2], {}).get(prev[3], None)

        if next_chars:
            choice = random.choices(list(next_chars.keys()), weights=next_chars.values(), k=1)[0]
        else:
            choice = generate_first_order(1, load_data().first_order())

        sentence += choice

    return sentence


data = load_data()
print('1st order length 200:')
print(generate_first_order(200, data.first_order()))
print('3rd order length 200:')
print(generate_third_order(200, data.third_order()))
print('5th order length 200:')
print(generate_fifth_order(200, data.fifth_order()))
