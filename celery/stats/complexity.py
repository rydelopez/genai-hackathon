import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import cmudict

import numpy as np


nltk.download('punkt')
nltk.download('cmudict')

# Initialize the CMU Pronouncing Dictionary for syllable counting
d = cmudict.dict()

def count_syllables(word):
    """
    Function to count the number of syllables in a word.
    Returns the number of syllables if the word is found in the CMU dict, otherwise estimates based on vowels.
    """
    if word.lower() in d:
        return max([len([s for s in lst if s[-1].isdigit()]) for lst in d[word.lower()]])
    else:
        # Fallback syllable count estimation for words not in CMU dict
        return sum(1 for char in word if char.lower() in 'aeiou')


def fkgl(text):
    """
    Function to calculate the Flesch-Kincaid Grade Level of a given text.
    """
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    syllables = sum(count_syllables(word) for word in words)
    
    words_per_sentence = len(words) / len(sentences)
    syllables_per_word = syllables / len(words)
    
    fkgl_score = 0.39 * words_per_sentence + 11.8 * syllables_per_word - 15.59

    return min(max(0, fkgl_score / 10), 1)


def measure_complexity(student_text: str, default_score=0.5) -> float:
    fkgl_score = fkgl(student_text)
    return fkgl_score


def measure_convo_complexity(conversation: ChatSession) -> float:
    complexity_amts = []

    for msg in conversation:
        if msg.type == "human":
            complexity_amts.append(measure_complexity(msg.contents))

    return {
        "avg_complexity": float(np.mean(complexity_amts))
    }