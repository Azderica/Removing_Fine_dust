#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

#define MAP_SIZE 300
#define FIND_SIZE 12
#define weight 0.5

int main(void)
{
    int dust_map[MAP_SIZE][MAP_SIZE];
    int a = 45;
    int b = 45;
    int c = 45;
    int d = 40;
    int i, j, sum, max_sum = 0;
    int box_i, box_j;
    int find_x, find_y;
    clock_t start, end;

    start = clock();
    dust_map[0][0] = a;
    dust_map[0][MAP_SIZE - 1] = b;
    dust_map[MAP_SIZE - 1][0] = c;
    dust_map[MAP_SIZE - 1][MAP_SIZE - 1] = d;

    // init dust map
    for (j = 1; j < MAP_SIZE - 1; j++)
    {
        dust_map[0][j] = (dust_map[0][0] * (MAP_SIZE - j) + dust_map[0][MAP_SIZE - 1] * j) / MAP_SIZE;
        dust_map[MAP_SIZE - 1][j] = (dust_map[MAP_SIZE - 1][0] * (MAP_SIZE - j) + dust_map[MAP_SIZE - 1][MAP_SIZE - 1] * j) / MAP_SIZE;
    }
    for (i = 1; i < MAP_SIZE - 1; i++)
    {
        for (j = 0; j < MAP_SIZE; j++)
        {
            dust_map[i][j] = (dust_map[0][j] * (MAP_SIZE - i) + dust_map[MAP_SIZE - 1][j] * i) / MAP_SIZE;
        }
    }

    // weight for corner
    // corner may have many dust
    for (i = 0; i < 300; i++)
    {
        for (j = 0; j < 300; j++)
        {
            dust_map[i][j] = dust_map[i][j] * (((i - 149) * (i - 150) + (j - 149) * (j - 150)) / (0.5 * MAP_SIZE * MAP_SIZE) * weight + (1 - weight));
        }
    }

    // find spot - 10*10
    for (i = 1; i <= MAP_SIZE / FIND_SIZE; i++)
    {
        for (j = 1; j <= MAP_SIZE / FIND_SIZE; j++)
        {
            sum = 0;
            for (box_i = (i - 1) * FIND_SIZE; box_i < i * FIND_SIZE; box_i++)
            {
                for (box_j = (j - 1) * FIND_SIZE; box_j < j * FIND_SIZE; box_j++)
                {
                    sum += dust_map[box_i][box_j];
                }
            }
            printf("%d ", sum);
            if (sum > max_sum)
            {
                find_x = i;
                find_y = j;
                max_sum = sum;
            }
        }
        printf("\n");
    }

    // for check, print all
    // for(i=0; i<300; i++){
    //     for(j=0; j<300; j++)
    //         printf("%d ", dust_map[i][j]);
    //     printf("\n");
    // }

    end = clock();
    printf("(X : %d, Y : %d)\n", find_x, find_y);
    find_x = find_x * FIND_SIZE - 0.5 * FIND_SIZE;
    find_y = find_y * FIND_SIZE - 0.5 * FIND_SIZE;
    printf("(X : %d, Y : %d)\n", find_x, find_y);
    printf("Time : %f\n", (float)(end - start) / CLOCKS_PER_SEC);
    return 0;
}