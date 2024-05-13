#include <stdio.h>
#include <stdbool.h>

void fillSudoko(const int Size, int sudoko [Size][Size]){
    for (int i = 0; i < Size; i++) {
        for (int j = 0; j < Size; j++) {
            if (sudoko[i][j] == 0) {
                int numbers[Size];
                for (int i = 0; i < Size; i++) {
                    numbers[i] = i + 1;
                }
                for (int k = i + 1; k < Size; k++) {
                    for (int l = 0; l < Size; l++) {
                        if (sudoko[k][j] == numbers[l]) {
                            numbers[l] = 0;
                        }
                    }
                }
                for (int k = i - 1; k > -1; k--) {
                    for (int l = 0; l < Size; l++) {
                        if (sudoko[k][j] == numbers[l]) {
                            numbers[l] = 0;
                        }
                    }
                }
                for (int k = j + 1; k < Size; k++) {
                    for (int l = 0; l < Size; l++) {
                        if (sudoko[i][k] == numbers[l]) {
                            numbers[l] = 0;
                        }
                    }
                }
                for (int k = j - 1; k > -1; k--) {
                    for (int l = 0; l < Size; l++) {
                        if (sudoko[i][k] == numbers[l]) {
                            numbers[l] = 0;
                        }
                    }
                }
                for (int k = 0; k < Size; k++) {
                    if (numbers[k] > 0) {
                        sudoko[i][j] = numbers[k];
                    }
                }
            }
        }
    }
}