import queue
import time
import numpy as np

from Utils import *
from CrossWord import CrossWord


class CrossWordSolver:
    def __init__(self):
        # different heurestic settings
        self.rank_word = False
        self.position_length = False
        self.letter_frequency = False

        self.word_sets = []
        self.prev_word_sets = []
        self.prev_positions = []
        self.CW: CrossWord = None

    # Prepare all needed variables, start solving the given crossword and return the outcome
    def solve(self, cw, tactics):
        self.rank_word, self.position_length, self.letter_frequency = tactics

        cw.positions.sort(key=lambda pos: pos.id)
        self.word_sets = [words[position.l] for position in cw.positions]

        self.CW = cw
        self.prev_positions = []
        self.prev_word_sets = []

        return self.csp()

    # Recursively solves a crossword
    def csp(self):
        # all positions have a word in this state, we're done solving
        if len(self.CW.positions) == 0:
            return True

        # sorting positions based on the amount of words able to use on them (MRV)
        if self.position_length:
            self.CW.positions.sort(key=lambda pos: len(self.word_sets[pos.id]) * pos.l)
        else:
            self.CW.positions.sort(key=lambda pos: len(self.word_sets[pos.id]))

        for position in self.CW.positions:
            ranked_words = self.rank_words(position)

            while not ranked_words.empty():
                word = ranked_words.get()[1]
                prev_text = self.CW.text_at_pos(position)

                self.write_word(position, word)

                if not self.check_arc(position):
                    self.undo_write(position, prev_text)
                    return False

                if self.csp():
                    return True

                self.undo_write(position, prev_text)

        return False

    # Rank a positions available word set based on different heurestics and return them in a queue:
    # 1. No heurestic at all, just check if we dont block our neighbors
    # 2. Ranking words based on the amount of possible words of our neighbors
    # 3. Ranking words based on neighbors as well their letter frequencies
    def rank_words(self, position):
        ranked = queue.PriorityQueue()

        for word in self.word_sets[position.id]:
            rank, add = 0, True
            for neighbor in position.neighbors:

                # only if the given neigbor doesnt have a word filled yet
                if neighbor in self.CW.positions:
                    p_i, n_i = self.CW.intersections[position.id, neighbor.id]
                    count = 0
                    for neighbor_word in self.word_sets[neighbor.id]:
                        if neighbor_word[n_i] == word[p_i]:
                            count += 1

                    if count == 0:
                        add = False
                        break

                    if self.rank_word and not self.letter_frequency:
                        rank += count
                    if self.letter_frequency:
                        rank += (count * letter_frequency[word[p_i]])
            if add:
                ranked.put((rank, word))

        return ranked

    # Check the current games arc consistency and update possible words set to all
    # positions which have been affected by the last move
    def check_arc(self, starting_position):
        queue = [starting_position]
        visited = set()

        while queue:
            position = queue.pop(0)
            visited.add(position.id)

            position_words = np.array([list(word) for word in self.word_sets[position.id]])
            letter_sets = [set(position_words[:, col]) for col in range(position.l)]

            for neighbor in position.neighbors:
                if neighbor in self.CW.positions:
                    p_i, n_i = self.CW.intersections[position.id, neighbor.id]

                    invalid = set(filter(lambda w: w[n_i] not in letter_sets[p_i], self.word_sets[neighbor.id]))

                    if invalid == self.word_sets[neighbor.id]:
                        return False

                    if len(invalid) > 0:
                        queue.append(neighbor)
                        self.word_sets[neighbor.id] = self.word_sets[neighbor.id] - invalid

        return True

    # save copy of current game state game and write a new word on grid
    def write_word(self, position, word):
        self.prev_word_sets.append(self.word_sets[:])
        self.prev_positions.append(self.CW.positions[:])

        self.CW.write_word(position, word)
        self.CW.positions.remove(position)
        self.word_sets[position.id] = set()
        self.word_sets[position.id].add(word)

        # check if by filling a word, whether one of our intersecting positions
        # hasn't been completed + check word validity (in case of error we restore our changes)
        finished_neighbors = []
        for neighbor in position.neighbors:
            txt = self.CW.text_at_pos(neighbor)
            if neighbor in self.CW.positions and ' ' not in txt:
                finished_neighbors.append((neighbor, txt))

        for neighbor, txt in finished_neighbors:
            self.CW.positions.remove(neighbor)
            self.word_sets[neighbor.id] = set()
            self.word_sets[neighbor.id].add(txt)

    # restore the previous state of the game from last copy
    def undo_write(self, position, prev_text):
        self.CW.positions = self.prev_positions.pop()
        self.word_sets = self.prev_word_sets.pop()
        self.CW.write_word(position, prev_text)


################################ MAIN PROGRAM #################################

if __name__ == "__main__":
    # Load data:
    dict_path = 'words.txt'
    grids = load_grids('krizovky.txt')
    words, letter_frequency = get_dictionary(dict_path)

    # pair grids with various tactics that work best for them
    # 1: Rank words by their affect on neighboring positions 
    # 2. Rank positions based on their length as well (the longer the higher priority)
    # 3. Rank words based letter frequency
    grids_with_tactics = {
        0: (grids[0], True, False, False),
        1: (grids[1], True, False, False),
        2: (grids[2], True, False, False),
        3: (grids[3], True, True, False),
        4: (grids[4], False, False, False),
        5: (grids[5], True, False, False),
        6: (grids[6], False, False, True),
        7: (grids[7], False, False, True),
        8: (grids[8], False, False, False),
        9: (grids[9], False, True, False)     
    }

    # All tactic combinations for the last crossword as a proof of no solution
    # cw10_combinations = {
    #     0: (grids[9], True, True, True),
    #     1: (grids[9], True, True, False),
    #     2: (grids[9], True, False, True),
    #     3: (grids[9], True, False, False),
    #     4: (grids[9], False, True, True),
    #     5: (grids[9], False, True, False),
    #     6: (grids[9], False, False, True),
    #     7: (grids[9], False, False, False)
    # }

    solver = CrossWordSolver()

    ##### CW TESTING #####
    grid_to_tests = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    solve_results = dict()
    for i in grid_to_tests:
        grid_entry = grids_with_tactics[i]
        grid = grid_entry[0]
        solver_tactics = grid_entry[1:]

        cw = CrossWord(grid)
        print("\n\033[95m\033[92mCrossword #{} being solved:\033[0m".format(i + 1))
        cw.print_grid()

        start = time.time()
        outcome = solver.solve(cw, solver_tactics)
        end = time.time()

        if outcome:
            print("\n\033[93mSolved crossword:\033[0m")
            cw.print_grid()
        else:
            print("\n\033[91mCOULDNT FIND RESULT ¯\_(ツ)_/¯")

        solve_results[i] = (outcome, end - start)

    print("\n\033[93mTime elapsed per crossword:\033[0m")

    for i, result in solve_results.items():
        outcome, time = result

        if outcome:
            print("\t\033[92mCW #{}\tSUCCESS\t\033[0m{}".format(i + 1, time))
            
        else:
            print("\t\033[91mCW #{}\tFAILED\t\033[0m{}".format(i + 1, time))

        total_time += time


    print('\n\033[95mTotal time to solve:\t{}'.format(total_time))
    
