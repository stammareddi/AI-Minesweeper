
from numpy import random

clockwise_moves = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
"""

5,5

4,5 up 
4,6 up right 
5,6 right
6,7 down right 
6,5 down 
6,4 down left 
5,4 left
4,4 up left 
"""

dim = 30
bombs = [100, 300, 500, 700]

player_board = [[-1 for row in range(dim)] for col in range(dim)]
visited_board = [[0 for row in range(dim)] for col in range(dim)]
flagged_board = [[0 for row in range(dim)] for col in range(dim)]
not_revealed = []
revealed_cells = [] #  does not mean visited
mine_list = []
explode_count = 0
kb = {}

def reset_globals():
    global player_board
    global visited_board
    global flagged_board
    global not_revealed
    global revealed_cells
    global mine_list
    global kb

    player_board = [[-1 for row in range(dim)] for col in range(dim)]
    visited_board = [[0 for row in range(dim)] for col in range(dim)]
    flagged_board = [[0 for row in range(dim)] for col in range(dim)]
    not_revealed = []
    revealed_cells = []  # does not mean visited
    mine_list = []
    kb = {}

def main():
    global explode_count
    smart_agent_bomb_explode_count = []
  
    smart_agent_bomb_explode_count.append(runner(1,500))
    """
    smart_agent_bomb_explode_count.append(runner(10,100))
    smart_agent_bomb_explode_count.append(runner(10,200))
    smart_agent_bomb_explode_count.append(runner(10,300))
    smart_agent_bomb_explode_count.append(runner(10,4000))
    smart_agent_bomb_explode_count.append(runner(10,500))
   
    """
    print("Smart agent data 10 runs for bomb counts of 50,100,200,300,400,500,600,700,800,850")
    print(smart_agent_bomb_explode_count)
    #print(explode_count)


def runner(times,bomb):
    explode_count = 0
    while times != 0:
        board = generate_board(dim, bomb)
        # push all cords into not_revelaed array
        for i in range(dim):
            for j in range(dim):
                not_revealed.append((i, j))

        # keep making moves until all cordinates have been visted/flagged/mine hit
        while len(not_revealed) > 0:
           explode_count = get_move(board, explode_count)

        reset_globals()
        times -= 1
    return explode_count




def print_board(board):
    print(" Board ")
    for row in board:
        print(row)


def print_visited():
    print(" ")
    print(" Visited Board ")
    for row in visited_board:
        print(row)


def print_player():
    print(" ")
    print(" Player Board ")
    for row in player_board:
        print(row)


def print_flagged():
    print(" ")
    print(" Flagged Board ")
    for row in flagged_board:
        print(row)


def check_win():
    for row in range(dim):
        for col in range(dim):
            if player_board[row][col] == -1:
                return False
    return True


def generate_mines(dim, mines):
    mine_list = []
    mines_left = mines

    while mines_left != 0:
        x = random.choice(dim - 1)
        y = random.choice(dim - 1)

        valid = (x, y) not in mine_list
        if valid:
            mine_list.append((x, y))
            mines_left -= 1
    return mine_list


def generate_board(dim, mines):
    # generate 2d array of 0
    board = [[0 for row in range(dim)] for col in range(dim)]

    # create mine list and put into board with clues
    mine_list = generate_mines(dim, mines)
    for (x, y) in mine_list:
        board[x][y] = 9
        for x1, y1 in clockwise_moves:
            inbounds = True if 0 <= x + x1 < dim and 0 <= y + y1 < dim and board[x + x1][y + y1] != 9 else False
            if inbounds:
                board[x + x1][y + y1] += 1
    return board


def find_hidden_neighbor(position):
    board = visited_board
    hidden_neighbor = 0
    x = position[0]
    y = position[1]
    for x1, y1 in clockwise_moves:
        inbounds = True if 0 <= x + x1 < dim and 0 <= y + y1 < dim else False
        if inbounds:
            if board[x + x1][y + y1] == 0:
                hidden_neighbor += 1
    return hidden_neighbor


def find_revealed_safe_neighbor(position):
    v_board = visited_board
    p_board = player_board
    revealed_safe_neighbor = 0
    x = position[0]
    y = position[1]
    for x1, y1 in clockwise_moves:
        inbounds = True if 0 <= x + x1 < dim and 0 <= y + y1 < dim else False
        if inbounds:
            if v_board[x+x1][y+y1] == 1 and p_board[x+x1][y+y1] != 9:
                revealed_safe_neighbor += 1
    return revealed_safe_neighbor


def neighbors_count(position):
    x = position[0]
    y = position[1]
    neighbors = 0
    for x1, y1 in clockwise_moves:
        inbounds = True if 0 <= x + x1 < dim and 0 <= y + y1 < dim else False
        if inbounds:
            neighbors += 1
    return neighbors


def insert_kb(board, position):
    x = position[0]
    y = position[1]
    clue = board[x][y]
    unrevealed_neighbors = set()

    if clue == 0:
        return

    for x1, y1 in clockwise_moves:
        inbounds = True if 0 <= x + x1 < dim and 0 <= y + y1 < dim else False
        if inbounds:
            if player_board[x+x1][y+y1] == -1:
                unrevealed_neighbors.add((x+x1, y+y1))
            elif flagged_board[x+x1][y+y1] == 1:
                clue -= 1
    if unrevealed_neighbors == set(): # checks if empty
        return
    else:
        result = {position: {"clue": clue, "neighbors": unrevealed_neighbors}} # sentence
        kb.update(result)


"""

2 sentecens in the kb  A and B

A and B 

A.issubsetofB


kb 
A : clue : 1   unrevealed _ 5,5 5,6 


B : clue : 2  unrevaled _  5,5 5,6 4,5 , 6,6


new sentence clue : 1 unreavled : 4,5 , 6,6


playerboard 


secnoirs that we are 100% sure of 

 A + B = 0

 D + E + C = 3 

"""

def check_subset(board):
    altered = False
    for position in kb:
        current_set = kb.get(position).get("neighbors")
        current_clue = kb.get(position).get("clue")
        for entry in kb:
            if entry != position:
                entry_set = kb.get(entry).get("neighbors")
                if current_set.issubset(entry_set):
                    entry_clue = kb.get(entry).get("clue")
                    difference_set = entry_set.difference(current_set)
                    diff_set_size = len(difference_set)
                    subtracted_size = abs(current_clue - entry_clue)
                    if diff_set_size > 0:
                        if subtracted_size == 0:
                            # print("comparing positions", position, entry)
                            # print("diff were all safe", difference_set)
                            # print("current set", current_set)
                            # print("entry set", entry_set)
                            for coordinates in difference_set:
                                x = coordinates[0]
                                y = coordinates[1]
                                player_board[x][y] = board[x][y]
                                visited_board[x][y] = 1
                                if revealed_cells.count((x, y)) == 0:
                                    revealed_cells.append((x, y))
                                if not_revealed.count((x, y)) > 0:
                                    not_revealed.remove((x, y))
                            altered = True
                            return altered
                        elif subtracted_size == diff_set_size:
                            # print("comparing positions", position, entry)
                            # print("diff were all mines", difference_set)
                            # print("current set", current_set)
                            # print("entry set", entry_set)
                            for coordinates in difference_set:
                                x = coordinates[0]
                                y = coordinates[1]
                                flagged_board[x][y] = 1
                                visited_board[x][y] = 1
                                player_board[x][y] = 9
                                if not_revealed.count((x, y)) > 0:
                                    not_revealed.remove((x, y))
                            altered = True
                            return altered
    return altered

def update_kb():
    for position in kb:
        neighbors = kb.get(position).get("neighbors")
        neighbors_list =  list(neighbors)
        clue = kb.get(position).get("clue")
        for coordinate in neighbors_list:
            x = coordinate[0]
            y = coordinate[1]
            if player_board[x][y] == 9:
                neighbors_list.remove(coordinate)
                clue -= 1
                kb[position]["clue"] = clue
            elif player_board[x][y] != -1:
                neighbors_list.remove(coordinate)
        kb[position]["neighbors"]= set(neighbors_list)

    # knowledge_to_add = []
    #
    # for position in kb:
    #     for secondposition in kb:
    #         if position != secondposition:
    #             position_neighbors = set(kb.get(position).get("neighbors"))
    #             #print(position_neighbors)
    #             secondpositon_neighbors = set(kb.get(secondposition).get("neighbors"))
    #             #print(secondpositon_neighbors)
    #             if position_neighbors.issubset(secondpositon_neighbors):
    #                knowledge_to_add.append((position ," neighnbors are a subset of ", secondposition , " neighbors "))
    #
    #             if secondpositon_neighbors.issubset(position_neighbors):
    #                  knowledge_to_add.append((secondposition ," neighnbors are a subset of ", position , " neighbors \n"))
    #
    # print("updated knowledge to add are ", knowledge_to_add )
                

    """

    itertation 1 --> random select 
    0,0 -> some clue

    add to kb 
        0,0 some clue -> 0,1 1,1 1,0


    itertation 2 --> random select 
    1,0 -> some clue

    add to kb 
      A  0,0    1 -> 0,1 1,1 
      B  1,0    1 -> 0,1 1,1 2,1 2,0 

    is B a subset of A? False
    is A a subset of B? True 
      1,0  0 -> 2,1 2,0 


    itertation 2B --> random select 
    1,0 -> some clue

    add to kb 
      A  0,0    1 -> 0,1 1,1 
      B  1,0    1 -> 0,1 1,1 
         1,0    1 -> 2,1 2,0 
    

    is B a subset of A? False
    is A a subset of B? True 
      1,0  1 -> 2,1 2,0 
    





    knowledge_to_add = []
    for position in kb:
        for secondpositon in kb:
            if position != secondpositon:
                position_neighbors = set(kb.get(position).get("neighbors"))
                #print(position_neighbors)
                secondpositon_neighbors = set(kb.get(secondpositon).get("neighbors"))
                #print(secondpositon_neighbors)
                if position_neighbors.issubset(secondpositon_neighbors):
                    print('position neighbors are subset of second positions neighbors')

                    result = {secondpositon : {"clue": secondpositon.get("clue") - position.get("clue"), "neighbors":  set(secondpositon_neighbors- position_neighbors)}}
                    kb.update(result)
                if secondpositon_neighbors.issubset(position_neighbors):
                    print('second position neighbors are subset of  positions neighbors')
                    result = {position : {"clue": position.get("clue") - secondpositon.get("clue"), "neighbors":  set(position_neighbors) - set(secondpositon_neighbors)}}
                    kb.update(result)
   

    """


def find_flagged_neighbor(position):
    board = flagged_board
    flagged_neighbor = 0
    x = position[0]
    y = position[1]
    for x1, y1 in clockwise_moves:
        inbounds = True if 0 <= x + x1 < dim and 0 <= y + y1 < dim else False
        if inbounds:
            if board[x+x1][y+y1] == 1:
                flagged_neighbor += 1
    return flagged_neighbor


def compare_boards(board):
    for x in range(dim):
        for y in range(dim):
            if board[x][y] != player_board[x][y]:
                print(x,y)
                return False
    return True
# If, for a given cell, the total number of mines (the clue) minus
# the number of revealed mines is the number of hidden neighbors,
# every hidden neighbor is a mine.


def condition1():
    altered = False
    for coordinate in revealed_cells:
        x = coordinate[0]
        y = coordinate[1]
        clue = player_board[x][y]
        total_marked_mine = find_flagged_neighbor((x,y))
        hidden_neighbors = find_hidden_neighbor((x,y))
        condition_met = clue - total_marked_mine == hidden_neighbors
        if condition_met:
            # marks hidden neighbors as bombs
            for x1, y1 in clockwise_moves:
                inbounds = True if 0 <= x + x1 < dim and 0 <= y + y1 < dim else False
                if inbounds:
                    if visited_board[x + x1][y + y1] == 0:
                        flagged_board[x + x1][y + y1] = 1
                        visited_board[x + x1][y + y1] = 1
                        player_board[x + x1][y + y1] = 9
                        not_revealed.remove((x+x1,y+y1))
            revealed_cells.remove(coordinate)
            if kb.get(coordinate):
                kb.pop(coordinate)
            altered = True
            break
    return altered

def condition2(board): # reveal safe cordinates 
    altered = False
    for coordinate in revealed_cells:
        x = coordinate[0]
        y = coordinate[1]
        safe_clue = neighbors_count((x,y)) - player_board[x][y]
        revealed_safe = find_revealed_safe_neighbor((x,y))
        hidden_neighbors = find_hidden_neighbor((x, y))
        condition_met = (safe_clue - revealed_safe == hidden_neighbors) # remaining cells are safe if mine count is infered
        if condition_met:
            for x1, y1 in clockwise_moves:
                inbounds = True if 0 <= x + x1 < dim and 0 <= y + y1 < dim else False
                if inbounds:
                    if visited_board[x+x1][y+y1] == 0: # has not been visted
                        player_board[x+x1][y+y1] = board[x+x1][y+y1]
                        revealed_cells.append((x+x1,y+y1))
                        insert_kb(board, (x+x1,y+y1))
                        not_revealed.remove((x+x1,y+y1))
                        visited_board[x + x1][y + y1] = 1
            revealed_cells.remove(coordinate)
            if kb.get(coordinate):
                kb.pop(coordinate)
            altered = True
            break
    return altered


def choose_random(board, explode_count):
    choosing = True
    while choosing:
        if len(not_revealed) > 0:
            a = random.randint(0, len(not_revealed))
            coordinate = not_revealed[a]
            not_revealed.pop(a)
            x = coordinate[0]
            y = coordinate[1]
            if visited_board[x][y] == 0:  # hasn't been visited already
                player_board[x][y] = board[x][y]  # update player board
                visited_board[x][y] = 1
                if player_board[x][y] == 9:  # coordinate selected is mine
                    flagged_board[x][y] = 1
                    explode_count += 1
                    # print(" unlucky cordinte of bomb hit at", (x,y))
                else:
                    revealed_cells.append(coordinate)
                    insert_kb(board, coordinate)
                choosing = False
    update_kb()
    return explode_count


def get_move(board, explode_count):

    #print("There are ", len(revealed_cells), " cordinates that have been revealed" )
    if len(revealed_cells) > 0:
        condition_2 = condition2(board)
        if condition_2:
            update_kb()
            
            return explode_count
           
        else:
            condition_1 = condition1()
            if condition_1:
                update_kb()
                return explode_count
                
            else:
                subset_check = check_subset(board)
                if subset_check:
                    update_kb()
                    
                    return explode_count
                else:
                

                    return choose_random(board, explode_count)

    else:
        return choose_random(board, explode_count)

 
    """
    # a flagged cell means that it has a mine
    if did_visit_cells == False: # if adj mine count == mine count val then rest of cells 100% safe
        for x in range(dim):
            for y in range(dim):
                if visited_board[x][y] == 0: # hasn't been visited 
                    # get adj mine count 
                    adj_mine_count = find_flagged_neighbor(flagged_board,(x,y))

                    # open adj safe neighbors if mine count matches 
                    if player_board[x][y] == adj_mine_count: ## if mines have all been marked then in theory rest can be opened as well 
                        for x1,y1 in clockwise_moves:
                            valid_cell = 0 <= x + x1 < dim and 0 <= y + y1 < dim and flagged_board[x+x1][y+y1] == 0
                            if valid_cell:
                                player_board[x+x1][y+y1] = player_board[x+x1][y+y1] # open all those safe cells 
                        visited_board[x][y] == 1
                        did_visit_cells = True



 {(1, 4): {'clue': 2, 'neighbors': [(0, 4), (2, 4), (2, 3), (1, 3), (0, 3)]}
 (4, 0): {'clue': 1, 'neighbors': [(3, 0), (3, 1), (4, 1)]}
 (0, 1): {'clue': 2, 'neighbors': [(0, 2), (1, 2), (1, 1), (1, 0), (0, 0)]}
 (3, 4): {'clue': 0, 'neighbors': [(2, 4), (4, 4), (4, 3), (3, 3), (2, 3)]}}
                
    if did_visit_cells == False:
        for x in range(dim):
            for y in range(dim):
                if player_board[x][y] >=0 and player_board[x][y] <=8 and visited_board[x][y] == 0:
                    total_neighbor_count = 0
                    adj_visited_cell_count = 0

                    for x1,y1 in clockwise_moves: # check 8 valid moves 
                        is_valid_neighbor = 0 <= x + x1 < dim and 0 <= y + y1 < dim  
                        if is_valid_neighbor: 
                            total_neighbor_count+=1 
                            if player_board[x+x1][y+y1] >=0 and player_board[x+x1][y+y1] <=8: # has been opened 
                                adj_visited_cell_count+=1

                    if player_board[x][y] == (total_neighbor_count - adj_visited_cell_count):
                        for x1,y1 in clockwise_moves:
                            is_supposed_mine_cell = 0 <= x + x1 < dim and 0 <= y + y1 < dim  and player_board[x+X1][y+y1] == -1
                            if is_supposed_mine_cell:
                                flagged_bombs+=1
                                flagged_board[x+x1][y+y1] = 1
                                player_board[x+x1][y+y1] = 10
                        did_flag_cells = True        
    """


    """
    3 Scenerios 

    1. Visiting cells - if visited and has a matching bomb count then in theory all adj cells can be opened 
        for the cells in the visited_board 
            if == 0:
                find how many adj bombs that cell has 
                if adj bomb count matches unvisited but opened player board cell val
                    open all the remaining elements in player_board
                mark cell as visited (1)
                update boolean 
            else continue 

    

    2. Flagging Mine - if 8-adj visited cell = mine count then all are mines 
        If step 1 is false then try to run this...
            for each cell in the player_board:
                If cell val in range of 1-8 then
                    count # of valid adj visited cells 
                        if cell val == (8 - adj # visited cells) && hasn't been visited:
                            flag it on flagged board 
                            incremecnt mine_countfinder 
                            mark that bomb as visited on visited board 


    3. Generating random coordinate 
        - generate random coordinate
        - check if random coordinate hasn't been visited 
            -  Open cell on board
                if mine
                    incrment unluckymineselectcount 
                    update as flag 
                    mark as visited 
                else 
                    display adj mine count only
                        note to remmber : next iteration will mark it as visited
    """



if __name__ == "__main__":
        main()
