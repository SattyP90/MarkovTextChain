import math
from collections import Counter


def novelty_score(sentence, corpus_bigrams, corpus_trigrams=None):
    """Score based on new bigram and trigram combinations"""
    words = sentence.split()

    if len(words) < 2:
        return 0

    bigrams = [(words[i], words[i+1]) for i in range(len(words)-1)]
    new_bigrams = sum(1 for pair in bigrams if pair not in corpus_bigrams)
    bigram_novelty = new_bigrams / len(bigrams) if bigrams else 0
    
    # Also check trigrams if available
    if corpus_trigrams and len(words) >= 3:
        trigrams = [(words[i], words[i+1], words[i+2]) for i in range(len(words)-2)]
        new_trigrams = sum(1 for tri in trigrams if tri not in corpus_trigrams)
        trigram_novelty = new_trigrams / len(trigrams) if trigrams else 0
        return (bigram_novelty * 0.6 + trigram_novelty * 0.4)
    
    return bigram_novelty


def word_rarity_score(sentence, word_frequencies):
    """Score based on use of rare words (inverse document frequency-like)"""
    words = sentence.split()
    if not words:
        return 0
    
    total_words = sum(word_frequencies.values())
    rarity_scores = []
    
    for word in words:
        if word in word_frequencies:
            # more rare words get higher scores
            freq = word_frequencies[word]
            idf = math.log(total_words / (freq + 1)) # word rarity score, add 1 to avoid division by zero
            rarity_scores.append(idf)
        else:
            rarity_scores.append(0)
    
    return sum(rarity_scores) / len(rarity_scores) if rarity_scores else 0


def entropy_score(sentence): # higher entropy means more unpredictability and potential creativity
    """Calculate Shannon entropy - higher means more unpredictable"""
    words = sentence.split()
    if len(words) < 2:
        return 0
    
    word_counts = Counter(words)
    total = len(words)
    
    entropy = 0
    for count in word_counts.values():
        prob = count / total
        entropy -= prob * math.log2(prob)
    
    #normalize by max possible entropy
    max_entropy = math.log2(total) if total > 1 else 1
    return entropy / max_entropy


def lexical_diversity_score(sentence): #measures vocabulary variety 
    """Type-token ratio with adjustment for length"""
    words = sentence.split()
    if not words:
        return 0
    
    unique_ratio = len(set(words)) / len(words)
    
    #bonus for longer sentences with high diversity
    length_bonus = min(len(words) / 15, 1.0)
    
    return unique_ratio * (0.7 + 0.3 * length_bonus)


def coherence_score(sentence):
    """Better coherence heuristics"""
    words = sentence.split()
    length = len(words)
    
    #penalize very short sentences
    if length < 5:
        return 0.3
    
    #penalize very long sentences
    if length > 20:
        return 0.4
    
    #check for excessive repetition
    word_counts = Counter(words)
    max_repeat = max(word_counts.values())
    if max_repeat > length * 0.4:  # More than 40% repetition
        return 0.3
    
    #optimal length range
    if 7 <= length <= 15:
        return 1.0
    
    return 0.7


def creativity_score(sentence, corpus_bigrams, word_frequencies=None, corpus_trigrams=None):
    """Enhanced multi-factor creativity scoring"""
    
    #core novelty - how new are the combinations
    novelty = novelty_score(sentence, corpus_bigrams, corpus_trigrams)
    
    #lexical diversity - variety of words used
    diversity = lexical_diversity_score(sentence)
    
    #entropy - unpredictability of word patterns
    entropy = entropy_score(sentence)
    
    #coherence - reasonable structure
    coherence = coherence_score(sentence)
    
    #word rarity - using less common words
    rarity = 0
    if word_frequencies:
        rarity = word_rarity_score(sentence, word_frequencies)
        # Normalize rarity to 0-1 range (assuming typical IDF range 0-5)
        rarity = min(rarity / 3, 1.0)
    
    #weufghted combination
    score = (
        novelty * 0.35 +        #new combinations matter most
        diversity * 0.25 +      #variety of vocabulary
        entropy * 0.15 +        #unpredictability adds creativity
        rarity * 0.15 +         #uncommon words
        coherence * 0.10        #still needs to make some sense
    )
    
    return round(score * 10, 3)  #scale to 0-10