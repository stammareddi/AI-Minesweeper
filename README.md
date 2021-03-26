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
       – Start off with all -1’s and it gets updated every time a new cell is opened by updating the cells -1 with whatever is at those coordinates in the minesweeper board.
3. Revealed Board
– Every time a cell is opened on the player board it will get updated here to fully guarantee that it has been a visited cell and the agent was able to deduce everything from it such as updating its knowledge base.
– 1 means visited while 0 is unvisited
– The game will continue on until the revealed board has no more 0’s

