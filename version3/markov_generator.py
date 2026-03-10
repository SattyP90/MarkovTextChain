import random
import re
from collections import Counter


def load_text(filename):

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read().lower()

    sentences = text.split(".")
    return sentences

#using a trigram model for better context and creativity
# boden combinational creativity 
def build_trigram_table(sentences):

    trigram_table = {}

    for sentence in sentences:

        sentence = re.sub(r'[^a-z\s]', '', sentence)
        words = sentence.split()

        if len(words) < 3:
            continue

        for i in range(len(words) - 2):

            w1 = words[i]
            w2 = words[i + 1]
            w3 = words[i + 2]

            key = (w1, w2)

            if key not in trigram_table:
                trigram_table[key] = []

            trigram_table[key].append(w3)

    return trigram_table

#frequency weighted random choice for more natural generation
#if a pair has multiple continuations, more common ones are more likely to be chosen, but rarer ones can still appear for creativity
def weighted_choice(words):

    counts = Counter(words)

    choices = list(counts.keys())
    weights = list(counts.values())

    return random.choices(choices, weights=weights)[0]


def generate_sentence(trigram_table, start_pair, min_length=7, max_length=15):
    """Generate sentence with variable length for natural variety"""
    
    #random target length within range
    target_length = random.randint(min_length, max_length)
    
    w1, w2 = start_pair
    sentence = [w1, w2]

    for _ in range(target_length - 2):

        key = (w1, w2)

        if key not in trigram_table:
            break

        next_word = weighted_choice(trigram_table[key])

        sentence.append(next_word)

        w1, w2 = w2, next_word

    return " ".join(sentence)


def build_word_frequencies(sentences):
    """Build word frequency dictionary for rarity scoring"""
    from collections import Counter
    
    word_freq = Counter()
    
    for sentence in sentences:
        sentence = re.sub(r'[^a-z\s]', '', sentence)
        words = sentence.split()
        word_freq.update(words)
    
    return word_freq


def build_trigram_set(sentences):
    """Build set of all trigrams in corpus for novelty checking"""
    trigram_set = set()
    
    for sentence in sentences:
        sentence = re.sub(r'[^a-z\s]', '', sentence)
        words = sentence.split()
        
        if len(words) >= 3:
            for i in range(len(words) - 2):
                trigram_set.add((words[i], words[i+1], words[i+2]))
    
    return trigram_set