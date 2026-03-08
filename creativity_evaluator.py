from markov_generator import build_trigram_table, generate_sentences

#build the trigram table
trigram_table = build_trigram_table("diaryofwhimpy.txt")

#load corpus words for novelty comparison
corpus_words = set()

with open("diaryofwhimpy.txt", "r", encoding="utf-8") as f:
    text = f.read().lower()
    corpus_words = set(text.split())


#novelty
def novelty_score(sentence):
    words = sentence.split()
    unique_words = set(words)

    # proportion of unique words
    return len(unique_words) / len(words)


#coherence
def coherence_score(sentence):
    words = sentence.split()

    score = 0

    # reward normal sentence length
    if 8 <= len(words) <= 12:
        score += 2

    # penalise repetition
    if len(words) == len(set(words)):
        score += 2

    return score


# total score
def total_score(sentence):
    return novelty_score(sentence) + coherence_score(sentence)


#generate and evaluete sentences
sentences = generate_sentences(trigram_table)

best_sentence = None
best_score = -1

for s in sentences:
    score = total_score(s)
    print(f"{s}  | score = {score}")

    if score > best_score:
        best_score = score
        best_sentence = s


print("\nBest sentence:")
print(best_sentence)
