# AI-Minesweeper-


## About Minesweeper
Minesweeper is logic-based game played on rectangular board whose object is to locate a predetermined number of randomly-placed ”mines” in the by clicking on ”safe” squares while avoiding the squares with mines. If the player clicks on a mine, the game ends. Otherwise, a number between 0 and 8 is displayed that identifies the total number of mines present in the eight neighboring squares. Therefore, finding a square containing ”8” indicated that all eight adjacent squares contain mines, while if a zero is uncovered, there are no mines in the surrounding squares. A square suspected of containing a mine may be marked with flag.


## Deeper Analysis

While minesweeper can be solved with logic alone in most cases there will be times when logic wont help. Here the agent also known as the player will have to choose a random coordinate and hope luck is on there side by revealing a safe cell.
![alt text](example.png)

Here we can see that there are two possible scenarios that can play out here.
The goal is to see if a AI agent can use any other inference before falling back to luck which is choosing a random coordinate due to insufficient knowledge of the board.


## Representation
A board size of n*n dimension size was used with a total of four boards to help infer logic from them. For this report a board size of 30*30 was used with a mine density of [0,100,200,300,400,500,600,700,800,900]. Each mine density ran a total of 10 games. Moreover when the agent unluckily hits a mine it will keep track of the count and continue on instead of ending the game. This will help us gather new findings and see if there are other inferences that can be used on top of logic to help the agent in successfully flagging mines.

The four boards are:
1. Minesweeper Board
      -  Can be known as the “answer key board”
      -  Consists of the adjacent mine count for each cell and for mine cells
it has a value of 9
2. Player Board
      -   Start off with all -1’s and it gets updated every time a new cell is opened by updating the cells -1 with whatever is at those coordinates in the minesweeper board.
    
    
3. Revealed Board
      - Every time a cell is opened on the player board it will get updated here to fully guarantee that it has been a visited cell and the agent was able to deduce everything from it such as updating its knowledge base.
      - 1 means visited while 0 is unvisited
      - The game will continue on until the revealed board has no more 0’s

4. Flagged board
      - Will all have 0’s and the assumed mines will be marked as 1’s
 
### Knowledge Base  
To represent the knowledge base a dictionary was used and for every key,value pair in the dictionary, it was considered a sentence.

Here a sentence in the knowledge base can be read as: 

      - “At (x,y) coordinate, we can infer that there are k coordinates that are unrevealed neighbors and out of them the clue tells us there are m mines within them.”

How it was programmed :

      - Key : coordinate , Value : (clue : mine count , unrevealed neighbors)

## What can the agent infer?
Whenever a new cell is revealed the agent will add it to the knowledge base as a sentence. Once this sentence has been added to the dictionary, it will update its existing sentences in the knowledge base where these new cell coordinates will be removed from those sentences’ unrevealed neighbors. This is being done by the agent because unrevealed neighbors are only supposed to have coordi- nates that haven’t been visited guaranteeing the agent that it will have the most up-to-date information about the board after making that move. When it do this thd agents knowledge base is able to deduce everything it can from every possible move that can happen on the board.


## How the agent makes a decision
The agent starts out by selecting a random coordinate as its first move. If this was a mine it will keep track of the unlucky mine hits it had. Otherwise, it will reveal it on the player board. During the next iteration based on the mine count clue and it being revealed on the player board , the agent will try to see if it can safely reveal more cells or flag mines that are 100 percent true based on logic alone. For instance, if a mine count was 2 and the agent had marked some 2 neighboring cells as flags then theoretically it can open the other 6 possible neighbors with confidence. Likewise, if te agent wasn’t able to deduce any safe cells while analyzing the player board it will try to see if it can use logic to flag any cells as mines that it is 100 percent sure of. For instance, if a cell had a mine count of 5 and 3 have been revealed as safes already then theoretically the rest of the mines are 100 percent mines which can be flagged. If both these logic’s don’t help the agent infer anything it will call a subset check method where we will try to see if any sentences unrevealed neighbors is a sub- set of another sentence in the knowledge base. If it is then the agent will do a little more digging meaning it will do sentence B values minus sentence A values.



For Example:

-Sentence B: “ At coordinate 5,5 we can infer that there are (4,4) ,(5,4) ,(4,6) (5,6), (6,5) , (6,6) coordinates that are unrevealed neighbors and out of them the clue tells us there is 1 mine within them.”

-Sentence A: “ At coordinate 4,5 we can infer that there are (4,4) (5,4) (4,6) (5,6) coordinates that are unrevealed neighbors and out of them the clue tells us there is 1 mine within them.”

-Sentence B - A: We can infer that coordinate (6,5) (6,6) doesn’t have a mine guaranteeing it is 100 percent safe because its mine count will equal to 0
Likewise, if the remaining unrevealed coordinates count matches the clue which isn’t 0 we can infer that it is 100 percent a mine we can flag. The agent will try this subset with each and every element taking O(n2) time.


If this fails it will fall to its last resort with is selecting a random coordinate to open. Then it will repeat those above steps in that order until the entire board has been revealed with ones in the revealed board.

