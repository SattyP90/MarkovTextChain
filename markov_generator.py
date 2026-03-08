import random
import re

def build_trigram_table(filename):
    trigram_table = {}

    #read file
    with open(filename, "r", encoding="utf-8") as file:
        text = file.read()

    #convert to lowercase
    text = text.lower()

    #split sentences by period
    sentences = text.split(".")

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

    return trigram_table




def generate_sentence(trigram_table, length=10):

    start = random.choice(list(trigram_table.keys()))
    w1, w2 = start

    sentence = [w1, w2]

    for _ in range(length - 2):

        key = (w1, w2)

        if key not in trigram_table:
            break

        next_word = random.choice(trigram_table[key])
        sentence.append(next_word)

        w1, w2 = w2, next_word

    return " ".join(sentence)




def generate_sentences(trigram_table, count=20, length=10):

    sentences = []

    for _ in range(count):
        sentence = generate_sentence(trigram_table, length)
        sentences.append(sentence)

    return sentences


# for running as a script
if __name__ == "__main__":

    trigram_table = build_trigram_table("diaryofwhimpy.txt")

    sentences = generate_sentences(trigram_table, 20, 10)

    for s in sentences:
        print(s)