import random
import re

#read text file
with open("diaryofwhimpy.txt", "r", encoding="utf-8") as file:
    text = file.read()

#convert to lowercase
text = text.lower()

#split text into sentences using '.'
sentences = text.split(".")

trigram_table = {}

for sentence in sentences:
    
    #remove punctuation except spaces
    sentence = re.sub(r'[^a-z\s]', '', sentence)

    words = sentence.split()

    #skip short sentences
    if len(words) < 3:
        continue

    #build trigram relationships
    for i in range(len(words) - 2):
        w1 = words[i]
        w2 = words[i + 1]
        w3 = words[i + 2]

        key = (w1, w2)

        if key not in trigram_table:
            trigram_table[key] = []

        trigram_table[key].append(w3)

#generate 20 sentences
for _ in range(20):
    start = random.choice(list(trigram_table.keys()))
    w1, w2 = start

    sentence = [w1, w2]

    for _ in range(8):  # already have 2 words
        key = (w1, w2)

        if key not in trigram_table:
            break

        next_word = random.choice(trigram_table[key])
        sentence.append(next_word)

        w1, w2 = w2, next_word

    print(" ".join(sentence))