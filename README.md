# Solve_Hua_Rong_Dao
Implementing a solver for the Hua Rong Dao sliding puzzle using A* and Manhattan distance heuristic. Hua Rong Dao is a sliding puzzle that is popular in China.

**Astar soln:***

I find the distance between the current position and the goal position of the 4 by 4 piece. I add that distance with depth + 1 to determine which level of the search tree I am looking at. Thereby, my final heuristic is the distance between the goal and the current position of the 4 by 4 piece added with the depth + 1.  

This heuristic is admissible because it assumes there is an absence of other pieces on the board. The lack of obstacles on the board would allow the 4 by 4 piece to easily move the goal position. Knowing the distance, it has to travel, the 4 by 4 piece can easily be moved since there is no other piece blocking it from reaching the goal position. 
