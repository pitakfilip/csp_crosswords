def load_words(path):
    # Loads all words from file
    return open(path, 'r').read().splitlines()


def load_grids(path):
    # Loads empty grids from file
    raw = open(path, 'r').read().split('\n\n')
    per_rows = [grid.rstrip().split('\n') for grid in raw]
    per_char = [[list(row) for row in grid] for grid in per_rows]
    return per_char

# creates a simple dictionary of words sorted by their lengths and another
# dictionary of letter frequencies in the whole data set of words
def get_dictionary(path):
    words = dict()
    letter_frequency = dict()
    for word in load_words(path):
        l = len(word)
        if l not in words.keys():
            words[l] = set()
        words[l].add(word)

        for letter in word:
            if letter not in letter_frequency.keys():
                letter_frequency[letter] = 0
            letter_frequency[letter] += 1

    return words, letter_frequency
