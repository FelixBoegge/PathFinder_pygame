---------------------------PathFinder Visualization-------------------------------

I dove into three different path finder algorithms,
namely Breath First Search (BFS), Depth First Search
(DFS) and A* and the ‘pygame’ library.

THE ALGORITHMS
BFS, DFS and A* are three different methods to traverse through graphs.
BFS basically works with a queue, where all neighboring nodes of the
current node are put into the queue. In each iteration the next node 
will be popped from the queue, set as the current node and in turn it’s 
neighbors will be added to the queue. Each node that was visited will
be added to a ‘visited’ set, to keep track of where we already had been, 
and to avoid traversing nodes multiple times. In practice, the visited
areas spreads circular.

The DFS algorithm works similar but uses a stack to store the neighbors
of the current node. Consequently, the algorithm traverses deeply into one
direction until it finds the end or a dead end, then it pops off the top
of the stack, one by one, until it finds a node, or in other words a new
path and traverses into this new direction deeply. It can be seen as a
recursive behavior.

The A* algorithm is a bit more complex and already takes the position of
the end into account. It uses a heuristic function to determine, the most
probably, best direction. In my code, the heuristic function represents the 
distance of the current node to the end node. In a checkerboard pattern,
where legal moves are up, down, left and right, the distance is  
h = abs(xcurrent – xend) + abs(ycurrent – yend).

In the scope of this project, the weight of an edge between two nodes are
not considered, as they are all one. The board is a 50x50 checkerboard with 
white spots that can be visited and black spots that represent a wall. The 
checkerboard pattern can be considered a graph, where each node, except 
the edge nodes, have four neighboring nodes.

THE VISUALIZATION
I visualized the board, from here on called the maze and the three algorithms
with ‘pygame’, a useful Python library, where a window can be created, and individual
elements can be displayed. The first left click on the maze will always create the start
spot. Similarly, if the start spot is set the next left click always creates the end
spot. Afterwards each left click creates a wall. The mouse can also stay pressed, and
when moved, a wall will be drawn along the path of the curser. Similarly, with the 
right mouse button, every spot can be reset to blank.

On the right-hand side sits the selection bar. Here one of the three algorithms can be
selected. After one of the algorithms successfully found a path to the end, the steps,
or in other words, how often the current position changed, and the path length are
monitored. Furthermore, instead of drawing your own maze, there are four default mazes
that can be selected. The ‘Return’ button sets the algorithm back and can also interrupt 
a running algorithm, but not erase the maze. ‘Reset’ clears the entire maze. ‘Start’
starts the algorithm.

The orange and turquoise spots depict the start and end respectively, red dots indicate
spots that have been visited already. Green dots indicate the open spots, they are the
current neighbors, that will be set to current in the next iterations. Prior, the A* algorithm 
already run and the needed steps and the found path length are shown next to the selection 
button. As soon as this  happens, the path is drawn in purple from the end back to the start.
Prior, the A* and BFS algorithms run, the records on the right can be compared.

The BFS and A* algorithm will, by nature, always find the shortest path, but the DFS algorithm
might find a way faster. Since the A* algorithm takes the end spot into account, it has an
advantage over the BFS.
