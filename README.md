# AI-Solvers
Used concepts of Machine Learning Algorithms to create an AI solver for Sokoban, enhanced Ken Ken, Othello, Sudoku, and Word Search.
Sokoban is a game where a robot (the controller) pushes boxes from a square to target squares. This grid also consists of obstacle squares.
The idea was to use Iterative Astar to find the shortest distance to reach the goal state of all boxes on the target square.
Enhanced Ken Ken is a different form of Sudoku. It follows all the rules of normal sudoku except for the given information and the fact that it can have a variable dimension nxn.
The given information in enhanced ken ken is not the values of some squares but the result of adding, subtracting, multiplying, or dividing a group of squares.
The idea was to use the concepts of Constraint Satisfaction Problems like backpropagating with inference to find a set of solutions that satisfies all constraints.
Othello is a game that uses black and white pieces for opposing players. The aim of the game is to have more pieces than your opponent.
The idea was to use alpha-beta pruning along with caching and ordering to minimize the time complexity to find optimal moves.
Sudoku is solved utilizing the concepts of Constraint Satisfaction Problems where only the correct values are assigned.
WordSearch is solved utilizing concept of matrices in linear algebra where a word is search in all 90 degree directions.
