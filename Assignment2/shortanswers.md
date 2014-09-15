##AI Assignment 2
###Short Answers - Josh Fermin


1. Is the exploration order what you would have expected?
	- Yes, the exploration order is what I would have expected. This is only if we assume that the left direction ("west") has a priority over the down direction("south"). This algorithm explores all possible paths to the goal to the maximum depth, which is what DFS does therefore it does what is expected.
2. Does Pacman actually go to all the explored squares on his way to the goal? Hint: If you use a Stack as your data structure, the solution found by your DFS algorithm for mediumMaze should have a length of 130 (provided you push successors onto the fringe in the order provided by getSuccessors; you might get 246 if you push them in the reverse order).
	- When I ran the medium maze with the DFS algorithm, its clear that pacman has a priority for the left direction, and from there he explores the first path to the goal. It is clear that he does not actually go through all of the explored squares on his way to the goal 
3. Is this a least cost solution? If not, what is depth-first search doing wrong?
	- This is not a least cost solution, the problem with DFS is the stop criterion. In BFS you search through every vertice as you put it in the frontier. In DFS all you do is search as far as you can down through one path in the tree, and then stop when you find a solution. 
	- In other words, DFS may explore some longer paths before shorter paths while BFS explores all paths of equal length before continuing. 
4. What happens on openmaze for the various search strategies?
	- DFS on openMaze searches 576 nodes and finds a path with a total cost of 298 in 0.1 seconds
	- BFS on openMaze searches 682 nodes and finds a path with a total cost of 54 in 0.1 seconds.
	- UCS on openMaze searches 682 nodes and finds a path with a total cost of 54 in 0.2 seconds.
	- astar with the Manhattan Heuristic searches 535 nodes and finds a path with a total cost of 54 in 0.2 seconds
	- Overall, astar with the Manhattan Heuristic performs the best with the least amount of nodes expanded and the best total cost.
