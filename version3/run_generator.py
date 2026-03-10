import random
import re

from markov_generator import *
from creativity_evaluator import *
from novelty_filter import *

print("Loading corpus and building models...")
sentences = load_text("diaryofwhimpy.txt")

trigram_table = build_trigram_table(sentences)

#build word frequencies for rarity scoring
word_frequencies = build_word_frequencies(sentences)

#build corpus bigrams
corpus_bigrams = set()

for s in sentences:
    words = re.sub(r'[^a-z\s]', '', s).split()
    for i in range(len(words)-1):
        corpus_bigrams.add((words[i], words[i+1]))

#build corpus trigrams for better novelty detection
corpus_trigrams = build_trigram_set(sentences)

#build start pairs from real sentences
start_pairs = []

for s in sentences:
    words = re.sub(r'[^a-z\s]', '', s).split()
    if len(words) >= 2:
        start_pairs.append((words[0], words[1]))

print(f"Corpus loaded: {len(sentences)} sentences")
print(f"Vocabulary: {len(word_frequencies)} unique words")
print(f"Generating 500 candidate sentences...\n")

generated_results = []
attempts = 0
max_attempts = 1000

#generate sentences with more attempts for better quality
while len(generated_results) < 500 and attempts < max_attempts:
    attempts += 1
    
    start = random.choice(start_pairs)
    
    #variable length for natural variety
    sentence = generate_sentence(trigram_table, start, min_length=7, max_length=15)

    if not is_novel(sentence, sentences):
        continue

    if not quality_filter(sentence):
        continue

    #enhanced creativity score with all factors
    score = creativity_score(sentence, corpus_bigrams, word_frequencies, corpus_trigrams)

    generated_results.append((sentence, score))

print(f"Generated {len(generated_results)} quality sentences from {attempts} attempts")
print("Applying diversity filter and ranking...\n")

#sort by creativity
generated_results.sort(key=lambda x: x[1], reverse=True)

#apply semantic diversity filter to top candidates
top_diverse = semantic_diversity_filter(generated_results[:50], min_distance=3)

#get top results
top_five = top_diverse[:5] if len(top_diverse) >= 5 else generated_results[:5]



print("Top 5 Most Creative Sentences")

for i, (sentence, score) in enumerate(top_five, start=1):
    print(f"\n{i}. {sentence}")
    print(f"   Creativity Score: {score}/10")




# savvve outputs
# with open("outputs.txt", "w", encoding="utf-8") as f:

#     f.write("Top 3 Most Creative Sentences\n\n")

#     for i, (sentence, score) in enumerate(top_three, start=1):
#         f.write(f"{i}. {sentence} | Score: {score}\n")

#     f.write("\nAll Generated Sentences (Ranked)\n\n")

#     for sentence, score in generated_results:
#         f.write(f"{sentence} | Score: {score}\n")


# print("\n300 sentences generated and ranked.")
# print("Results saved to outputs.txt")