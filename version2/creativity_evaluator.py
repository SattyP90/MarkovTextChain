from version2.markov_generator import build_trigram_table, generate_sentences

# Build model
trigram_table = build_trigram_table("LOTF.txt")

# Load corpus for novelty comparison
with open("LOTF.txt", "r", encoding="utf-8") as f:
    corpus_words = set(f.read().lower().split())

#sentence lenght score
def length_score(words):

    length = len(words)

    if 8 <= length <= 12:
        return 2
    elif 6 <= length <= 14:
        return 1
    return 0


#vocabulary diversity score
def diversity_score(words):

    unique_ratio = len(set(words)) / len(words)

    if unique_ratio > 0.9:
        return 2
    elif unique_ratio > 0.75:
        return 1
    return 0

#repetition penalty
def repetition_penalty(words):

    repeats = len(words) - len(set(words))

    if repeats == 0:
        return 2
    elif repeats == 1:
        return 1
    return 0


#novelty score
def novelty_score(words):

    rare_words = [w for w in words if w not in corpus_words]

    ratio = len(rare_words) / len(words)

    if ratio > 0.4:
        return 2
    elif ratio > 0.2:
        return 1
    return 0


# bigram repetition penalty
def bigram_penalty(words):

    bigrams = []

    for i in range(len(words) - 1):
        bigrams.append((words[i], words[i+1]))

    unique = len(set(bigrams))

    if unique == len(bigrams):
        return 2
    elif unique >= len(bigrams) - 1:
        return 1
    return 0


#overall sentence score
def score_sentence(sentence):

    words = sentence.split()

    score = 0

    score += length_score(words)
    score += diversity_score(words)
    score += repetition_penalty(words)
    score += novelty_score(words)
    score += bigram_penalty(words)

    return score


#generate and evaluate sentences
sentences = generate_sentences(trigram_table, 100, 10)

best_sentence = None
best_score = -1

for s in sentences:

    score = score_sentence(s)

    print(f"{s}  | score = {score}")

    if score > best_score:
        best_score = score
        best_sentence = s


print("\nBest sentence:")
print(best_sentence)
print("Score:", best_score)