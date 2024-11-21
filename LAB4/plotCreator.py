import matplotlib.pyplot as plt

file = open('LAB4/output.txt', 'r', encoding='utf-8')
lines = file.readlines()

def tokenize(lines):
    tokens = dict()
    i = 0
    while i < len(lines)-1:
        lines[i] = lines[i].strip()
        if not lines[i].startswith('  Rank'):
            token = lines[i]
            values = []
            i += 1
            while i < len(lines) and lines[i].startswith('  Rank'):
                _, entropy = lines[i].split(':')
                values.append(float(entropy))
                i += 1
            tokens[token] = values
        else:
            i += 1
    return tokens

tokens = tokenize(lines)

def plot_entropies(tokens):
    for token, values in tokens.items():
        if len(values) == 0:
            continue
        plt.figure()
        plt.plot(range(len(values)), values, label=token)
        plt.xlabel('Rank')
        plt.ylabel('Entropy')
        plt.title(f'{token.split('(')[0]}')
        plt.savefig(f'{token.split('(')[0]}.jpg')
        plt.close()

plot_entropies(tokens)

file.close()