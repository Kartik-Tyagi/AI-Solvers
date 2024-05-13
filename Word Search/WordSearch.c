#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

void printFoundLocation(int rowDir, int colDir) {
    if (rowDir == 1) {
        if (colDir == -1) {
            printf ("south-west");
        } else if (colDir == 0) {
            printf ("south");
        } else {
            printf ("south-east");
        }
    } else if (rowDir == -1) {
        if (colDir == -1) {
            printf ("north-west");
        } else if (colDir == 0) {
            printf ("north");
        } else {
            printf ("north-east");
        }
    } else {
        if (colDir == 1) {
            printf ("east");
        } else {
            printf ("west");
        }
    }
}

bool search1D(char word[], int wordSize, const int Size, char grid[Size][Size], int row, int col, int rowDir, int colDir) {
    int count = 0;
    int word_count = 0;
    while (count < wordSize) {
        if (word[count] == grid[row][col] && row > -1 && col > -1 && row < Size && col < Size) {
            word_count = word_count + 1;
        }
        row = row + rowDir;
        col = col + colDir;
        count = count + 1;
    }
    return (count == word_count);
}

void search2D(char word[], int wordSize, const int Size, char grid[Size][Size]) {
    char first_letter = word[0];
    double row_dir = 1;
    double col_dir = 0;
    int count;
    bool stop = false;
    for (int i = 0; i < Size; i++) {
        for (int j = 0; j < Size; j++) {
            if (first_letter == grid[i][j]) {
                count = 0;
                while (count < 8 && !stop) {
                    int rowDir = row_dir;
                    int colDir = col_dir;
                    if (search1D(word, wordSize, Size, grid, i, j, rowDir, colDir)) {
                        printf ("Word found at row %d and column %d in the ", i, j);
                        printFoundLocation(rowDir, colDir);
                        printf (" direction.");
                        stop = true;
                    }
                    double temp = row_dir;
                    row_dir = rint((row_dir/1.41421356237) + (col_dir/1.41421356237));
                    col_dir = rint((col_dir/1.41421356237) - (temp/1.41421356237));
                    count = count + 1;
                }
            }
        }
    }
}