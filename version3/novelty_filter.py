# def is_novel(sentence, corpus_sentences):

#     sentence = sentence.strip()

#     for s in corpus_sentences:

#         if sentence in s:
#             return False

#     return True

#bigram novelty filter

# def is_novel(sentence, corpus_bigrams):

#     words = sentence.split()

#     bigrams = [(words[i], words[i+1]) for i in range(len(words)-1)]

#     new_pairs = 0

#     for pair in bigrams:
#         if pair not in corpus_bigrams:
#             new_pairs += 1

#     novelty_ratio = new_pairs / len(bigrams)

#     return novelty_ratio

# bigram novelty filter with threshold
#check generated sentence bigrams against corpus bigrams, require at least 30% new bigrams for novelty
def is_novel(sentence, corpus_sentences):
    """Check if sentence is truly novel (not substring of corpus)"""
    sentence = sentence.strip()

    for s in corpus_sentences:
        if sentence in s:
            return False

    return True


def quality_filter(sentence):
    """Enhanced quality filtering with better heuristics"""
    words = sentence.split()

    # Remove very short sentences
    if len(words) < 6:
        return False
    
    # Remove very long sentences (likely runaway generation)
    if len(words) > 20:
        return False

    # Remove excessive repetition
    word_counts = {}
    for word in words:
        word_counts[word] = word_counts.get(word, 0) + 1
    
    max_repetition = max(word_counts.values())
    if max_repetition > len(words) * 0.4:  # No word should appear >40% of time
        return False
    
    # Check for immediate repetition patterns (word word)
    for i in range(len(words) - 1):
        if words[i] == words[i + 1]:
            return False
    
    # Check lexical diversity - at least 60% unique words
    if len(set(words)) < len(words) * 0.6:
        return False

    return True


def semantic_diversity_filter(sentences, min_distance=3):
    """Filter out sentences that are too similar to each other"""
    if not sentences:
        return sentences
    
    diverse_sentences = [sentences[0]]
    
    for sentence, score in sentences[1:]:
        words_new = set(sentence.split())
        
        is_diverse = True
        for existing, _ in diverse_sentences:
            words_existing = set(existing.split())
            
            # Jaccard similarity
            intersection = len(words_new & words_existing)
            union = len(words_new | words_existing)
            similarity = intersection / union if union > 0 else 0
            
            # If too similar, skip it
            if similarity > 0.7:
                is_diverse = False
                break
        
        if is_diverse:
            diverse_sentences.append((sentence, score))
    
    return diverse_sentences