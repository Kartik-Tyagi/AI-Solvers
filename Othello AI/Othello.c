#include <stdio.h>
#include <stdbool.h>
#include <math.h>

int main() {
    int n;
    //Creating board
    printf ("Enter the board dimension: ");
    scanf ("%d", &n);

    char board[26][26];

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            board[i][j] = 'U';
        }
    }
    
    board[(n / 2) - 1][(n / 2) - 1] = 'W';
    board[n / 2][n / 2] = 'W';
    board[(n / 2) - 1][n / 2] = 'B';
    board[n / 2][(n / 2) - 1] = 'B';

    printBoard(board, n);
    //Taking the current configurations to print current board
    char configuration[672][4];

    printf ("Enter board configuration:\n");

    int count = 0;
    
    do {
        scanf ("%s", &configuration[count][0]);
        board[configuration[count][1] - 'a'][configuration[count][2] - 'a'] = configuration[count][0];
        count = count + 1;
    } while (configuration[count - 1][0] != '!' && configuration[count - 1][1] != '!' && configuration[count - 1][2] != '!');

    int row, col;

    printBoard(board, n);
    //New variable for direction
    int dir_count;
    double row_dir = 1, col_dir = 0;
    int rowDir, colDir;
    //Printing possible moves for white
    printf ("Available moves for W:\n");
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (board[i][j] == 'U') {
                dir_count = 0;
                while (dir_count < 8) {
                    int rowDir = row_dir;
                    int colDir = col_dir;
                    if (checkLegalInDirection(board, n, i, j, 'W', rowDir, colDir)) {
                        printf ("%c%c\n", 'a' + i, 'a' + j);
                        dir_count = 10;
                    }
                    double temp = row_dir;
                    row_dir = rint((row_dir/1.41421356237) + (col_dir/1.41421356237));
                    col_dir = rint((col_dir/1.41421356237) - (temp/1.41421356237));
                    dir_count = dir_count + 1;
                }
            }
        }
    }
    //Printing possible moves for black
    printf ("Available moves for B:\n");
    
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (board[i][j] == 'U') {
                dir_count = 0;
                while (dir_count < 8) {
                    int rowDir = row_dir;
                    int colDir = col_dir;
                    if (checkLegalInDirection(board, n, i, j, 'B', rowDir, colDir)) {
                        printf ("%c%c\n", 'a' + i, 'a' + j);
                        dir_count = 10;
                    }
                    double temp = row_dir;
                    row_dir = rint((row_dir/1.41421356237) + (col_dir/1.41421356237));
                    col_dir = rint((col_dir/1.41421356237) - (temp/1.41421356237));
                    dir_count = dir_count + 1;
                }
            }
        }
    }
    //printing new move
    char move[3];

    printf ("Enter a move:\n");
    scanf ("%s", move);

    bool valid = false;
    char colour;

    dir_count = 0;
    while (dir_count < 8) {
        int rowDir = row_dir;
        int colDir = col_dir;
        if (checkLegalInDirection(board, n, (int)move[1] - (int)'a', (int)move[2] - (int)'a', move[0], rowDir, colDir)) {
            row = (int)move[1] - (int)'a';
            col = (int)move[2] - (int)'a';
            do { //Changing board
                board[row][col] = move[0];
                row = row + rowDir;
                col = col + colDir;
                colour = board[row][col];
            } while (positionInBounds(n, row, col) && colour != move[0]);
            valid = true;
        }
        double temp = row_dir;
        row_dir = rint((row_dir/1.41421356237) + (col_dir/1.41421356237));
        col_dir = rint((col_dir/1.41421356237) - (temp/1.41421356237));
        dir_count = dir_count + 1;
    }
    if(valid) {
        printf ("Valid move.\n");
    } else {
        printf ("Invalid move.\n");
    }

    printBoard(board, n); //printing final board

    return 0;
}

void printBoard(char board[][26], int n) { //printing current board
    char full_board[n + 1][n + 2];
    full_board[0][0] = ' ';
    for (int i = 0; i < n + 1; i++) {
        full_board[i][1] = ' ';
    }
    for (int i = 2; i < n + 2; i++) {
        full_board[0][i] = (char)'a' + i - 2;
    }
    for (int i = 1; i < n + 1; i++) {
        full_board[i][0] = (char)'a' + i - 1;
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            full_board[i + 1][j + 2] = board[i][j];
        }
    }
    for (int i = 0; i < n + 1; i++) {
        for (int j = 0; j < n + 2; j++) {
            printf ("%c",full_board[i][j]);
        }
        printf ("\n");
    }
}

bool positionInBounds(int n, int row, int col) { //checking legal row and col
    return (row < n && col < n && row >= 0 && col >= 0);
}

bool checkLegalInDirection(char board[][26], int n, int row, int col, char colour, int deltaRow, int deltaCol) { //checking legal move
    int count = 0;
    if (board[row][col] == 'U') {
        if (colour == 'W') {
            do {
                row = row + deltaRow;
                col = col + deltaCol;
                if (positionInBounds(n, row, col)) {
                    colour = board[row][col];
                }
                count = count + 1;
            } while (positionInBounds(n, row, col) && colour == 'B');
            if (colour == 'W' && count > 1) {
                return true;
            } else {
                return false;
            }
        } else if (colour == 'B') {
            do{
                row = row + deltaRow;
                col = col + deltaCol;
                if (positionInBounds(n, row, col)) {
                    colour = board[row][col];
                }
                count = count + 1;
            } while (positionInBounds(n, row, col) && colour == 'W');
            if (colour == 'B' && count > 1) {
                return true;
            } else {
                return false;
            }
        }
    } else {
        return false;
    }
}