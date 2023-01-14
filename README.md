# Crossword solving as CSP

The theory behind solving a crossword as a CSP problem is very simple to implement and understand. The very basic algorithm to search for solutions is Depth-first search (DFS) which is trivial for implementation.
Having only DFS is very ineffective, as there must be a way to rate our current state and our next possible moves to pick best branch to search. A block or unit to which we want to find an optimal 
word may be represented as a *'Position'*, containing information about its starting position (row, column), length and direction. Besides this it is very helpful to find the given position's 'neigbors'
(other positions intersecting our block/unit). As a very first step we create a set of possible words for every position (a set of words of a specific length that will fit our position). This will later on be updated 
with every move, to ensure arc-consistency and mainly prematurely catch a position with no possible words with the current combination of words.

After the setup is done, we want to start our DFS algorithm, where we firstly order our positions with a **Minimal Remaining Value (MRV)** heurestic. There are possibilities to add weights based on specific rules,
however the main idea is to execute a search via a position with the least possible words, since generally this would mean we would exhaust the possibilities faster, either finding a solution or moving on to the next position.

Once an optimal position is selected, we must pick the right word to use. For this we sort our position's possible word set with **Least Constraining Value (LCV)** heurestic, where we check each word and evaluate how 
big of an impact will it have on our neighbors. Here we can either ignore the impact on our neighbors (this will drastically slow the search for simple crosswords), count in the impact or add a specific weight to each impact.

After chosing an optimal position and placing a word, we must check how we impacted all other positions **(AC3 algorithm)**. The basic idea is to start with the position we changed, iterate through our neighbors and update the position's word set based
on the new constraints. If the word set is changed, we possibly affected the given posistion's neighbors, meaning we follow the same procedure with them until we havent changed a word set, a word set is empty (we used a word which will not 
lead to a solution) or we checked and updated all positions in the crossword.
 
Also after placing a word, we check our neighbors whether we haven't completed their word as a by-product.


## Usage

Within `CrossWordSolver.py`  change the default input files (word dictionary, crossword grids):
```
    dict_path = 'words.txt'
    grids = load_grids('krizovky.txt')
```

Currently the mentioned 'tactics' to our heurestics are used as followed in our sample grids:
```
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
        9: (grids[9], False, False, False)
    }
```

Solver finds a solution to every crossword (besides the last one, which does not have a solution) within 25 seconds:
```
Time elapsed per crossword:
	CW #1	SUCCESS	0.0
	CW #2	SUCCESS	0.16500020027160645
	CW #3	SUCCESS	0.6489989757537842
	CW #4	SUCCESS	0.7040083408355713
	CW #5	SUCCESS	0.9770016670227051
	CW #6	SUCCESS	0.1428375244140625
	CW #7	SUCCESS	9.258829593658447
	CW #8	SUCCESS	6.575526475906372
	CW #9	SUCCESS	7.552755832672119
	CW #10	FAILED	29.978804349899292

Total time to solve:	56.00376296043396
```

After the execution we may see a short time statistic for each crossword with a result.



## License

[MIT](https://choosealicense.com/licenses/mit/)