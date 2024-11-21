from collections import Counter
import math

def compute_entropy(text):
    """Compute the entropy of a sequence of symbols."""
    char_count = Counter(text)
    total_chars = len(text)
    return -sum((count / total_chars) * math.log2(count / total_chars) for count in char_count.values())

def compute_conditional_entropy(text, rank):
    """Compute the conditional entropy for a given rank."""
    if rank == 0:
        return compute_entropy(text)

    # Create n-grams and prefixes
    ngrams = [tuple(text[i:i + rank]) for i in range(len(text) - rank + 1)]
    prefixes = [ngram[:-1] for ngram in ngrams]

    ngram_count = Counter(ngrams)
    prefix_count = Counter(prefixes)

    # Compute conditional entropy
    total_ngrams = len(ngrams)
    entropy = 0
    for ngram, count in ngram_count.items():
        prefix = ngram[:-1]
        conditional_prob = count / prefix_count[prefix]
        joint_prob = count / total_ngrams
        entropy += joint_prob * -math.log2(conditional_prob)
    return entropy

def read_file(file_path):
    """Read a file's content as a string."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def analyze_text(file_path, rank=4):
    """Compute the entropy and conditional entropy of a text file at character and word levels."""
    text = read_file(file_path)

    # entropy for chars
    char_entropies = [compute_conditional_entropy(list(text), r) for r in range(rank + 1)]

    # entropy for words
    words = text.split()
    words_entropies = [compute_conditional_entropy(words, r) for r in range(rank + 1)]

    return char_entropies, words_entropies

def print_entropies(entropies, label, rank, file):
    file.write(f"{label} Entropies (Ranks 0 to {rank}):\n")
    for r, entropy in enumerate(entropies):
        file.write(f"  Rank {r}: {entropy:.4f}\n")
    file.write("\n")

rank = 4

# English and Latin sample analysis
english_norm = 'LAB4/data/norm_wiki_en.txt'
latin_norm = 'LAB4/data/norm_wiki_la.txt'

english_char_entropies, english_word_entropies = analyze_text(english_norm, rank)
latin_char_entropies, latin_word_entropies = analyze_text(latin_norm, rank)

with open('LAB4/output.txt', 'w', encoding='utf-8') as output_file:
    output_file.write("\n")
    print_entropies(english_char_entropies, "English Character-Level", rank, output_file)
    output_file.write("\n") 
    print_entropies(english_word_entropies, "English Word-Level", rank, output_file)

    output_file
    print_entropies(latin_char_entropies, "Latin Character-Level", rank, output_file)
    output_file.write("\n")
    print_entropies(latin_word_entropies, "Latin Word-Level", rank, output_file)

    # Sample files analysis
    sample_files = [f'LAB4/data/sample{i}.txt' for i in range(6)]

    output_file.write("Sample Text Analysis:\n")
    for sample_file in sample_files:
        char_entropy, word_entropy = analyze_text(sample_file, rank)
        output_file.write(f"\n")
        print_entropies(char_entropy, f"{sample_file.split('/')[2]} Character-Level", rank, output_file)
        print_entropies(word_entropy, f"{sample_file.split('/')[2]} Word-Level", rank, output_file)
